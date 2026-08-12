# Security Policy

## Supported Versions

Saveetha Labs follows a "rolling release" model for the main website at `saveetha-labs.github.io`.
All security updates are immediately applied to the `main` branch.

| Version | Supported          |
| ------- | ------------------ |
| main (latest) | ✅ Yes, always |
| Older commits   | ❌ Not supported |

Course repositories under the `saveetha-labs` org are supported individually —
check each repo's README for its status.

---

## Reporting a Vulnerability

### ⚠️ **DO NOT** create public issues for security vulnerabilities.

Public disclosure can put all users at risk before a fix is available.

### ✅ How to Report Privately

1. **Preferred method**: Email the maintainers directly via the GitHub organization
   [@saveetha-labs](https://github.com/saveetha-labs) profile contact

2. **Alternative**: Open a [private security vulnerability report](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability)
   directly on GitHub if the repository has Private Vulnerability Reporting enabled.

### What to Include in Your Report

Please provide as much detail as possible:

- **Type of vulnerability**: XSS, CSRF, data leakage, etc.
- **Steps to reproduce**: Clear, step-by-step instructions
- **Affected components**: Which pages / files are vulnerable
- **Proof of concept**: Screenshots, code snippets, or video
- **Potential impact**: What could an attacker do?
- **Suggested fix** (optional): Your idea for a patch

---

## Response Timeline

| Time Frame | Action |
| :--------: | :----- |
| **24 hours** | Acknowledge receipt of your report |
| **3–5 days** | Initial triage and severity assessment |
| **1–2 weeks** | Develop and test a fix |
| **At release** | Publicly acknowledge your contribution (with your permission) |

We aim to patch critical vulnerabilities within **72 hours** of confirmation.

---

## Scope

### In Scope

- Main website at `saveetha-labs.github.io`
- All HTML/CSS/JavaScript in this repository
- Course material accuracy (incorrect code could mislead students)

### Out of Scope

- Third-party services (GitHub Pages CDN, Google Fonts, etc.)
- Browser-specific bugs in unsupported browsers
- Theoretical issues with no practical impact
- Spam/phishing from user-created forks (report to GitHub directly)
- Vulnerabilities in third-party code snippets (report to upstream maintainers)

---

## Safe Harbor

We **will not** pursue legal action against anyone who:

- Reports a vulnerability in good faith
- Avoids privacy violations, data destruction, or service interruption
- Only accesses their own data / test accounts
- Gives reasonable time to patch before any public disclosure

If you're unsure whether something counts, **ask us first**.

---

## Educational Note

This project is **primarily educational**. The lab programs and code examples
are intended for student learning, not production use. While we strive for
accuracy and quality, some student-contributed code may not follow industry
security best practices by design (for learning purposes).

Always verify code independently before using it outside a lab environment.

---

**Thank you for keeping Saveetha Labs safe and secure for all learners.** 🛡️
