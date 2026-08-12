# Support & Getting Help

Welcome to Saveetha Labs! We're here to help you succeed. This document covers all the ways you can get support.

---

## 📚 First: Check the Docs

90% of questions are already answered here:

| Resource | Link | Best For |
| :------- | :--- | :------- |
| **Main Website** | [saveetha-labs.github.io](https://saveetha-labs.github.io/) | Browsing all courses, searching resources |
| **Documentation** | [saveetha-labs.github.io/docs.html](https://saveetha-labs.github.io/docs.html) | Detailed course catalog, usage guides, FAQs |
| **README** | [README.md](README.md) | Project overview, quick start, structure |
| **Contributing Guide** | [CONTRIBUTING.md](CONTRIBUTING.md) | How to add materials, fix bugs |

---

## 💬 Ask Questions the Smart Way

### 1. Search Before Asking

Search through:
- ✅ [GitHub Issues (open & closed)](https://github.com/saveetha-labs/saveetha-labs.github.io/issues?q=)
- ✅ [GitHub Discussions](https://github.com/orgs/saveetha-labs/discussions)
- ✅ [Documentation page](https://saveetha-labs.github.io/docs.html)

### 2. Choose the Right Channel

| Your Situation | Where to Go |
| :------------- | :---------- |
| ❓ **General question** — "How do I access CSA13 materials?" | [GitHub Discussions](https://github.com/orgs/saveetha-labs/discussions) → **Q&A** category |
| 💡 **Feature idea** — "Can we add dark mode toggle?" | [GitHub Discussions](https://github.com/orgs/saveetha-labs/discussions) → **Ideas** category |
| 🐛 **Bug** — "Search bar doesn't work on mobile" | [Open a Bug Report](https://github.com/saveetha-labs/saveetha-labs.github.io/issues/new) |
| 📚 **Missing course** — "Can you add materials for CSA42?" | [Open a Content Request](https://github.com/saveetha-labs/saveetha-labs.github.io/issues/new) |
| 🔒 **Security issue** — Private vulnerability report | See [SECURITY.md](SECURITY.md) → Report privately |
| 👋 **Just want to say hi / connect** | [GitHub Discussions](https://github.com/orgs/saveetha-labs/discussions) → **General** or **Show & Tell** |

---

## 🚩 When Opening an Issue

Use these checklists to make sure your issue gets resolved fast!

### Bug Reports (Template Checklist)

```
✓ Clear, specific title
✓ Exact steps to reproduce the issue
✓ Expected behavior vs actual behavior
✓ Browser + device info (e.g., "Chrome 120 on Android 14")
✓ Screenshots / screen recording (if visual bug)
✓ Console errors (F12 → Console tab)
```

### Good vs. Bad Bug Reports

| ❌ Bad | ✅ Good |
| :---- | :----- |
| "Search doesn't work" | "Search returns no results when typing 'CSA13' in Firefox 120 on Windows 11. Console shows `ReferenceError: repositories is not defined` at line 872." |
| "The site looks broken on my phone" | "On iPhone 14 (Safari), the navigation menu overlaps the hero section when opened in landscape mode. See attached screenshot." |

---

## 🎯 Self-Help Troubleshooting

Try these before asking — they fix most common issues!

### Website Issues

1. **Hard Refresh** — Press `Ctrl + Shift + R` (or `Cmd + Shift + R` on Mac)
2. **Clear Cache** — Clear browser cache for `saveetha-labs.github.io`
3. **Disable Extensions** — Ad blockers or privacy extensions can break JS
4. **Try Incognito** — See if the bug happens without browser extensions
5. **Check Status** — Is [GitHub Pages up?](https://www.githubstatus.com/)

### Code / Material Issues

1. **Check Original Syllabus** — Cross-reference with your official course syllabus
2. **Try Alternative Approaches** — There's often more than one way to solve a problem
3. **Run Locally** — Clone the repo and execute on your machine (not just copy-paste)
4. **Compiler Errors?**
   - Check if you have the right compiler version
   - Google the exact error message first
   - Note the language standard needed (e.g., C++17 vs C99)

### Git / Forking Issues

1. **Sync Your Fork**
   ```bash
   git remote add upstream https://github.com/saveetha-labs/saveetha-labs.github.io.git
   git fetch upstream
   git merge upstream/main
   ```
2. **Undo Accidental Changes**
   ```bash
   # Discard all uncommitted changes (careful!)
   git checkout -- .
   ```
3. **Merge Conflicts?** Use [GitHub's merge conflict editor](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts/about-merge-conflicts) — it's simpler than it looks.

---

## 👨‍🏫 Academic Guidance

Saveetha Labs provides **supplementary** materials. Here's the correct way to use them:

| ✅ Do This | ❌ Don't Do This |
| :--------- | :-------------- |
| Use lab programs to **understand concepts** before your lab | Blindly copy-paste code into submissions |
| Compare your code with ours after you've written yours | Submit our code as your own (plagiarism!) |
| Use notes to **supplement** your lectures | Skip lectures and only read our notes |
| Report errors to help improve materials | Ignore bugs that will mislead other students |
| Build upon existing code with your own improvements | Redistribute materials without attribution |

---

## 🕐 Response Times

Maintainers are **student volunteers** with classes, exams, and personal lives.

| Type | Typical Response |
| :--- | :--------------- |
| Critical security issues | **< 24 hours** |
| High-impact bugs (site down, broken core features) | **1–2 days** |
| Regular issues / feature requests | **3–7 days** |
| General discussions | **Weekly check-ins** |

If it's been over a week and you haven't heard back:
1. Check if your post is in the right category
2. Add a polite bump comment: "Any update on this? Still encountering the issue."
3. For urgent academic matters, reach out to your class representatives or faculty.

---

## 🤝 Become a Helper!

The best way to learn is to **teach others**.

- ✅ **Answer questions** in GitHub Discussions
- ✅ **Review pull requests** — Leave helpful feedback on other students' PRs
- ✅ **Write tutorials** — Share how you solved a tricky problem
- ✅ **Mentor newcomers** — Help students make their first contribution

**Every answer you give becomes permanent documentation for future students!**

---

## 📞 Direct Contact

For private matters (personal issues, code of conduct reports, etc.), contact the maintainers through:

- GitHub organization profile: [@saveetha-labs](https://github.com/saveetha-labs)
- Create a **private discussion** if the feature is available

---

<div align="center">
  <h3>Learning Together, Building Together 💜</h3>
  <p>Saveetha Labs is 100% community-run. Your questions, answers, and contributions make this platform better for everyone.</p>
  <p>— The Saveetha Labs Team</p>
</div>
