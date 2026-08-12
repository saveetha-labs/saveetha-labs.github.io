#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate crawlable per-repo static pages and regenerate sitemap.xml.

GitHub Pages serves the repo explorer dynamically via /repo/?repo=NAME, which is
invisible to crawlers that do not execute JavaScript. This script fetches the
public repository list from the GitHub API and writes:

    repo/<NAME>.html   -- static, SEO-friendly page per repository
    repo/_repos.json   -- repo metadata manifest (name, description, lastmod)
    sitemap.xml        -- sitemap with every repo page (pushed_at as lastmod)

Usage (CI - recommended, includes rendered README + top-level file listing):
    GH_TOKEN=<token> python scripts/generate_repo_pages.py

Usage (local - metadata only, one API request):
    python scripts/generate_repo_pages.py --no-readme

Environment variables:
    ORG        organization name        (default: saveetha-labs)
    BASE_URL   site base URL            (default: https://saveetha-labs.github.io)
    GH_TOKEN   GitHub token (raises the API rate limit); GITHUB_TOKEN is used as fallback
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import string
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

ORG = os.environ.get("ORG", "saveetha-labs")
BASE_URL = os.environ.get("BASE_URL", "https://saveetha-labs.github.io").rstrip("/")
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_DIR = os.path.join(_ROOT, "repo")
MANIFEST = os.path.join(REPO_DIR, "_repos.json")
SITEMAP = os.path.join(_ROOT, "sitemap.xml")
NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,99}$")
# Course repos are named like "CSA02-CProgramming", "UBA33-PrinciplesOfManagement", etc.
# Non-course repos (profile / tooling) are excluded unless --all is passed.
COURSE_RE = re.compile(r"^[A-Z]{2,4}\d{2}")
OG_IMAGE = BASE_URL + "/icons/og-banner.png"
# Never delete these when cleaning stale generated pages (they are hand-maintained site files).
PROTECTED = {"index.html"}


def log(*args):
    print(*args, file=sys.stderr)


def http_json(url: str, *, data=None, method: str | None = None, accept: str = "application/vnd.github+json") -> object | None:
    """GET/POST a URL and return parsed JSON, or None on any failure."""
    body = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(
        url, data=body, method=method,
        headers={
            "Accept": accept,
            "User-Agent": "saveetha-labs-sitemap-gen/1.0",
        },
    )
    if body is not None:
        req.add_header("Content-Type", "application/json")
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.load(resp)
    except Exception as exc:
        log(f"! request failed: {url} ({exc})")
        return None


def org_repos() -> list[dict]:
    """Fetch the account's public repos, newest push first. Falls back to the manifest."""
    url = f"https://api.github.com/orgs/{urllib.parse.quote(ORG)}/repos?per_page=100&type=public&sort=pushed"
    data = http_json(url)
    if not isinstance(data, list):
        log("! not an org; trying user endpoint")
        data = http_json(
            f"https://api.github.com/users/{urllib.parse.quote(ORG)}/repos?per_page=100&type=public&sort=pushed"
        )
    if isinstance(data, list) and data:
        repos = []
        for r in data:
            name = r.get("name", "")
            if not NAME_RE.match(name):
                continue
            repos.append({
                "name": name,
                "description": (r.get("description") or "").strip(),
                "pushed_at": r.get("pushed_at") or "",
                "default_branch": r.get("default_branch") or "main",
                "github_url": r.get("html_url") or f"https://github.com/{ORG}/{name}",
            })
        return repos
    log("! could not fetch org repos from API; falling back to existing manifest")
    return manifest_repos()


def manifest_repos() -> list[dict]:
    """Read the last-known repo list from repo/_repos.json so the sitemap is never wiped."""
    try:
        with open(MANIFEST, encoding="utf-8") as fh:
            manifest = json.load(fh)
    except Exception:
        return []
    return [
        {
            "name": r["name"],
            "description": r.get("description", ""),
            "pushed_at": r.get("pushed_at", ""),
            "default_branch": r.get("default_branch", "main"),
            "github_url": r.get("github_url", f"https://github.com/{ORG}/{r['name']}"),
        }
        for r in manifest.get("repos", [])
    ]


def readme_text(name: str, branch: str) -> str:
    """Fetch the raw README text for a repo (empty string on failure)."""
    url = f"https://api.github.com/repos/{urllib.parse.quote(ORG)}/{urllib.parse.quote(name)}/readme?ref={urllib.parse.quote(branch)}"
    try:
        req = urllib.request.Request(
            url,
            headers={
                "Accept": "application/vnd.github.raw",
                "User-Agent": "saveetha-labs-sitemap-gen/1.0",
            },
        )
        if TOKEN:
            req.add_header("Authorization", f"Bearer {TOKEN}")
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8", errors="replace")[:200_000]
    except Exception:
        return ""


def render_markdown(text: str) -> str:
    """Render Markdown to sanitized HTML via the GitHub API; falls back to a local parser."""
    result = http_json(
        "https://api.github.com/markdown",
        data={"text": text, "mode": "gfm"},
        method="POST",
    )
    if isinstance(result, str):
        return result
    return simple_markdown(text)


def simple_markdown(text: str) -> str:
    """Minimal dependency-free Markdown -> HTML fallback (no sanitization needed; input is HTML-escaped)."""
    out: list[str] = []

    def inline(s: str) -> str:
        s = html.escape(s)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        s = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2">\1</a>', s)
        return s

    def close_list():
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    def close_code():
        nonlocal in_code
        if in_code:
            out.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
            code_lines.clear()
            in_code = False

    in_code = False
    in_list = False
    code_lines: list[str] = []

    for line in text.splitlines():
        if line.strip().startswith("```"):
            close_list()
            close_code()
            in_code = not in_code
            continue
        if in_code:
            code_lines.append(line)
            continue

        stripped = line.strip()
        if not stripped:
            close_list()
            out.append("")
            continue

        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            close_list()
            level = len(m.group(1))
            out.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
            continue

        m = re.match(r"^\s*(?:[-*+]|\d+[.)])\s+(.*)$", line)
        if m:
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append("<li>" + inline(m.group(1)) + "</li>")
            continue

        close_list()
        out.append("<p>" + inline(line) + "</p>")

    close_list()
    close_code()
    return "\n".join(out)


def root_entries(name: str, branch: str) -> list[dict]:
    """Top-level contents of a repo (name + type). Empty list on failure."""
    url = f"https://api.github.com/repos/{urllib.parse.quote(ORG)}/{urllib.parse.quote(name)}/contents?ref={urllib.parse.quote(branch)}"
    data = http_json(url)
    if not isinstance(data, list):
        return []
    return [
        {"name": e.get("name", ""), "type": "dir" if e.get("type") == "dir" else "file"}
        for e in data
        if e.get("name")
    ]


def format_date(iso: str) -> str:
    if not iso:
        return ""
    try:
        return datetime.fromisoformat(iso.replace("Z", "+00:00")).strftime("%d %b %Y")
    except Exception:
        return iso[:10]


def build_jsonld(name: str, desc: str, page_url: str, github_url: str, lastmod: str) -> str:
    graph = [
        {
            "@context": "https://schema.org",
            "@type": "Course",
            "name": name,
            "description": desc,
            "url": page_url,
            "sameAs": github_url,
            "provider": {"@type": "EducationalOrganization", "name": "Saveetha Labs", "url": BASE_URL + "/"},
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Saveetha Labs", "item": BASE_URL + "/"},
                {"@type": "ListItem", "position": 2, "name": "Repository Explorer", "item": BASE_URL + "/repo/"},
                {"@type": "ListItem", "position": 3, "name": name, "item": page_url},
            ],
        },
    ]
    if lastmod:
        graph[0]["dateModified"] = lastmod
    dumped = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    return dumped.replace("<", "\\u003c")


NAV = string.Template("""
<nav class="site-nav">
    <div class="nav-inner">
        <a class="brand" href="../index.html">
            <span class="mark"></span>
            Saveetha <b>Labs</b>
        </a>
        <div class="nav-links">
            <a href="../index.html">Home</a>
            <a href="../docs.html">Docs</a>
            <a href="index.html">Explorer</a>
        </div>
    </div>
</nav>
""").substitute({})

FOOTER = string.Template("""
<footer>
    <div class="footer-inner">
        <div>© $year Saveetha Labs · Educational use only · MIT License</div>
        <a href="https://github.com/saveetha-labs" target="_blank" rel="noopener">GitHub</a>
    </div>
</footer>
""").substitute({"year": str(datetime.now(timezone.utc).year)})

README_SECTION = """
  <section class="panel readme">
    <h2>README</h2>
    $content
  </section>
"""

FILES_SECTION = """
  <section class="panel files">
    <h2>Contents</h2>
    <ul class="file-list">
      $items
    </ul>
  </section>
"""

PAGE_TEMPLATE = string.Template("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="theme-color" content="#030712">
<title>$title</title>
<meta name="robots" content="index, follow">
<meta name="description" content="$desc">
<link rel="canonical" href="$page_url">
<link rel="icon" type="image/png" sizes="32x32" href="../favicon-32x32.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Saveetha Labs">
<meta property="og:title" content="$title">
<meta property="og:description" content="$desc">
<meta property="og:url" content="$page_url">
<meta property="og:image" content="$og_image">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="$title">
<meta name="twitter:description" content="$desc">
<script type="application/ld+json">
$jsonld
</script>
<style>
:root {
    --bg: #030712;
    --card: #0f172a;
    --text: #f9fafb;
    --muted: #94a3b8;
    --accent: #38bdf8;
    --border: rgba(255,255,255,.08);
}
@media (prefers-color-scheme: light) {
    :root {
        --bg: #f5f7fb;
        --card: #ffffff;
        --text: #0f172a;
        --muted: #55647a;
        --accent: #0284c7;
        --border: rgba(15,23,42,.12);
    }
}
* { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body {
    font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
    min-height: 100vh;
}
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
.site-nav {
    position: sticky;
    top: 0;
    z-index: 10;
    border-bottom: 1px solid var(--border);
    background: rgba(3,7,18,.85);
    backdrop-filter: blur(8px);
}
@media (prefers-color-scheme: light) {
    .site-nav { background: rgba(245,247,251,.92); }
}
.nav-inner {
    max-width: 980px;
    margin: 0 auto;
    padding: 0 20px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
}
.brand { display: inline-flex; align-items: center; gap: 8px; font-weight: 700; color: var(--text); }
.mark {
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: radial-gradient(circle at 30% 30%, var(--accent), transparent 70%);
    box-shadow: 0 0 10px var(--accent);
}
.nav-links { display: flex; gap: 18px; }
.nav-links a { color: var(--muted); font-size: .92rem; }
.nav-links a:hover { color: var(--accent); text-decoration: none; }
main { max-width: 980px; margin: 0 auto; padding: 40px 20px 60px; }
.page-head { text-align: center; margin-bottom: 32px; }
.badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 5px 14px;
    border-radius: 999px;
    border: 1px solid var(--border);
    background: rgba(56,189,248,.08);
    color: var(--accent);
    font-size: .78rem;
    font-weight: 600;
    letter-spacing: .4px;
}
.dot { width: 7px; height: 7px; border-radius: 50%; background: var(--accent); box-shadow: 0 0 8px var(--accent); }
.page-head h1 {
    font-size: clamp(1.6rem, 4vw, 2.4rem);
    margin: 16px 0 8px;
    letter-spacing: -.3px;
    word-break: break-word;
}
.sub { color: var(--muted); max-width: 680px; margin: 0 auto 22px; }
.actions { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; margin-bottom: 14px; }
.btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 10px 18px;
    border-radius: 12px;
    font-size: .9rem;
    font-weight: 600;
    border: 1px solid transparent;
}
.btn.primary { background: var(--accent); color: #030712; }
.btn.primary:hover { filter: brightness(1.1); text-decoration: none; }
.btn.ghost { border-color: var(--border); color: var(--text); }
.btn.ghost:hover { border-color: var(--accent); text-decoration: none; }
.meta { color: var(--muted); font-size: .82rem; }
.panel {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
}
.panel h2 {
    font-size: 1.05rem;
    font-weight: 700;
    margin-bottom: 14px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
}
.readme { overflow-wrap: anywhere; }
.readme h1, .readme h2, .readme h3, .readme h4 { margin: 20px 0 8px; line-height: 1.35; }
.readme h1 { font-size: 1.4rem; }
.readme h2 { font-size: 1.2rem; }
.readme p, .readme ul, .readme ol { margin: 0 0 12px; }
.readme ul, .readme ol { padding-left: 22px; }
.readme li { margin-bottom: 4px; }
.readme code { background: rgba(56,189,248,.1); padding: 1px 5px; border-radius: 5px; font-size: .88em; }
.readme pre {
    background: rgba(0,0,0,.35);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px;
    overflow-x: auto;
    margin: 0 0 14px;
}
.readme pre code { background: none; padding: 0; }
.readme blockquote { border-left: 3px solid var(--accent); padding-left: 14px; color: var(--muted); margin: 0 0 12px; }
.readme img { max-width: 100%; height: auto; border-radius: 8px; }
.readme table { border-collapse: collapse; width: 100%; margin: 0 0 14px; }
.readme th, .readme td { border: 1px solid var(--border); padding: 8px 10px; text-align: left; font-size: .92rem; }
.file-list { list-style: none; display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 8px; }
.file-list a {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 9px 12px;
    border: 1px solid var(--border);
    border-radius: 10px;
    color: var(--text);
    font-size: .88rem;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
}
.file-list a:hover { border-color: var(--accent); text-decoration: none; }
.folder::before, .file::before {
    content: '';
    width: 10px;
    height: 10px;
    flex: none;
    border: 2px solid var(--accent);
    border-radius: 3px;
}
.folder::before { border-radius: 2px; }
footer {
    border-top: 1px solid var(--border);
    padding: 22px 20px;
    background: linear-gradient(to bottom, transparent, rgba(56,189,248,.03));
}
.footer-inner {
    max-width: 980px;
    margin: 0 auto;
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    align-items: center;
    justify-content: space-between;
    color: var(--muted);
    font-size: .82rem;
}
@media (max-width: 560px) {
    main { padding: 28px 16px 44px; }
    .panel { padding: 18px; }
    .nav-links { gap: 14px; }
    .footer-inner { flex-direction: column; text-align: center; }
}
</style>
</head>
<body>
$nav
<main>
    <header class="page-head">
        <div class="badge"><span class="dot"></span>Course Repository</div>
        <h1>$name</h1>
        <p class="sub">$desc</p>
        <div class="actions">
            <a class="btn primary" href="$explorer_url">Open Interactive Explorer</a>
            <a class="btn ghost" href="$github_url" target="_blank" rel="noopener">View on GitHub</a>
        </div>
        <p class="meta">Last updated: $lastmod$count</p>
    </header>
$readme_html
$files_html
</main>
$footer
</body>
</html>
""")


def safe_sub(value: str) -> str:
    """Escape literal dollar signs so string.Template does not treat them as placeholders."""
    return value.replace("$", "$$")


def render_page(repo: dict, readme_section: str, files_section: str) -> str:
    name = repo["name"]
    esc = html.escape
    desc = repo.get("description") or (
        f"Course repository for {name} by Saveetha Labs - notes, lab programs and study resources."
    )
    title = f"{name} - Saveetha Labs Course Repository"
    page_url = repo["page_url"]
    jsonld = build_jsonld(name, desc, page_url, repo["github_url"], repo["lastmod"])
    lastmod = format_date(repo.get("pushed_at")) or "N/A"
    count = f" · {repo['file_count']} items" if repo["file_count"] else ""
    values = {
        "title": safe_sub(esc(title)),
        "desc": safe_sub(esc(desc)),
        "page_url": safe_sub(page_url),
        "og_image": safe_sub(OG_IMAGE),
        "jsonld": safe_sub(jsonld),
        "name": safe_sub(esc(name)),
        "explorer_url": safe_sub(repo["explorer_url"]),
        "github_url": safe_sub(repo["github_url"]),
        "lastmod": safe_sub(esc(lastmod)),
        "count": safe_sub(count),
        "nav": safe_sub(NAV),
        "footer": safe_sub(FOOTER),
        "readme_html": safe_sub(readme_section),
        "files_html": safe_sub(files_section),
    }
    return PAGE_TEMPLATE.substitute(values)


def write_manifest(repos: list[dict], generated_at: str) -> None:
    data = {
        "generated_at": generated_at,
        "org": ORG,
        "base": BASE_URL,
        "repos": [
            {
                "name": r["name"],
                "description": r.get("description", ""),
                "pushed_at": r.get("pushed_at", ""),
                "lastmod": r.get("lastmod", ""),
                "default_branch": r.get("default_branch", "main"),
                "github_url": r.get("github_url", ""),
                "page": r["page_url"],
            }
            for r in repos
        ],
    }
    with open(MANIFEST, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def write_sitemap(repos: list[dict]) -> None:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        f'  <url><loc>{BASE_URL}/</loc><priority>1.0</priority></url>',
        f'  <url><loc>{BASE_URL}/docs.html</loc><priority>0.8</priority></url>',
        f'  <url><loc>{BASE_URL}/repo/</loc><priority>0.7</priority></url>',
    ]
    for r in repos:
        lm = f"<lastmod>{r['lastmod']}</lastmod>" if r.get("lastmod") else ""
        lines.append(f'  <url><loc>{BASE_URL}/repo/{r["name"]}.html</loc>{lm}<priority>0.6</priority></url>')
    lines.append("</urlset>")
    with open(SITEMAP, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--no-readme", action="store_true",
                        help="skip README / file-list fetches (metadata only, one API request)")
    parser.add_argument("--repo", help="only regenerate the given repo name (debug)")
    parser.add_argument("--all", action="store_true",
                        help="include non-course repos (profile/tooling) in the output")
    args = parser.parse_args()

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    os.makedirs(REPO_DIR, exist_ok=True)

    repos = org_repos()
    if not repos:
        log("ERROR: no repos available and no manifest fallback; aborting to protect sitemap.xml.")
        return 1
    if not args.all:
        repos = [r for r in repos if COURSE_RE.match(r["name"])]
    if args.repo:
        repos = [r for r in repos if r["name"] == args.repo]
        if not repos:
            log(f"ERROR: no repo named '{args.repo}' found.")
            return 1

    generated = []
    for repo in repos:
        name = repo["name"]
        branch = repo.get("default_branch") or "main"
        pushed = repo.get("pushed_at") or ""
        repo["lastmod"] = pushed[:10] if pushed else ""
        repo["page_url"] = f"{BASE_URL}/repo/{urllib.parse.quote(name)}.html"
        repo["explorer_url"] = f"{BASE_URL}/repo/?repo={urllib.parse.quote(name)}"

        readme_section = ""
        files_section = ""
        repo["file_count"] = 0
        if not args.no_readme:
            text = readme_text(name, branch)
            if text.strip():
                readme_section = README_SECTION.replace("$content", render_markdown(text))
            entries = root_entries(name, branch)
            if entries:
                repo["file_count"] = len(entries)
                items = "".join(
                    f'<li><a class="{html.escape(e["type"])}" '
                    f'href="{safe_sub(tree_or_blob_url(name, branch, e))}">{html.escape(e["name"])}</a></li>'
                    for e in entries
                )
                files_section = FILES_SECTION.replace("$items", items)

        page = render_page(repo, readme_section, files_section)
        with open(os.path.join(REPO_DIR, name + ".html"), "w", encoding="utf-8") as fh:
            fh.write(page)
        log(f"  wrote {name}.html")
        generated.append(repo)

    write_manifest(generated, generated_at)
    write_sitemap(generated)
    stale = [p for p in os.listdir(REPO_DIR)
             if p.endswith(".html") and p not in PROTECTED and p[:-5] not in {r["name"] for r in generated}]
    for p in stale:
        os.remove(os.path.join(REPO_DIR, p))
        log(f"  removed stale {p}")
    log(f"Done: {len(generated)} repo pages, {MANIFEST}, {SITEMAP}")
    return 0


def tree_or_blob_url(name: str, branch: str, entry: dict) -> str:
    org = urllib.parse.quote(ORG)
    repo = urllib.parse.quote(name)
    path = urllib.parse.quote(entry["name"])
    if entry["type"] == "dir":
        return f"https://github.com/{org}/{repo}/tree/{branch}/{path}"
    return f"https://github.com/{org}/{repo}/blob/{branch}/{path}"


if __name__ == "__main__":
    raise SystemExit(main())
