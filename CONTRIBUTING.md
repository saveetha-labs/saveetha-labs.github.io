# Contributing to Saveetha Labs

First off, thank you for taking the time to contribute! 🎉

Saveetha Labs is built by students, for students. Every contribution — no matter how small — helps thousands of learners. This document outlines the guidelines for contributing to the project.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [What Can I Contribute?](#what-can-i-contribute)
3. [Getting Started](#getting-started)
4. [Style Guidelines](#style-guidelines)
5. [Pull Request Process](#pull-request-process)
6. [Reporting Issues](#reporting-issues)
7. [Community](#community)

---

## Code of Conduct

This project and everyone participating in it are governed by the
[Saveetha Labs Code of Conduct](CODE_OF_CONDUCT.md).
By participating, you agree to abide by its terms.

---

## What Can I Contribute?

### 📝 Course Materials (Most Wanted!)
- Lab programs with explanations
- Well-commented code examples (C, C++, Python, Java, Prolog, etc.)
- Lecture notes and summaries
- Previous year question papers
- Assignment solutions with steps
- Reference links and study resources

### 🎨 Website Improvements
- UI/UX enhancements
- Responsive design fixes
- Performance optimizations
- Accessibility improvements
- New features (search, filters, visualizations)

### 📚 Documentation
- Improve README files
- Write tutorials and how-to guides
- Translate content to other languages
- Fix typos and grammatical errors

### 🐛 Bug Reports & Suggestions
- Report broken links or incorrect code
- Suggest new courses or features
- Report design inconsistencies

---

## Getting Started

### 1. Fork & Clone

```bash
# Fork the repository via the GitHub button, then:
git clone https://github.com/YOUR-USERNAME/saveetha-labs.github.io.git
cd saveetha-labs.github.io

# Add upstream remote to stay synced
git remote add upstream https://github.com/saveetha-labs/saveetha-labs.github.io.git
```

### 2. Stay Synced

```bash
# Before starting any work, sync with upstream
git fetch upstream
git checkout main
git merge upstream/main
```

### 3. Create a Branch

```bash
# Use descriptive branch names
git checkout -b feature/add-csa57-lab3-solutions
# or
git checkout -b fix/navbar-mobile-overflow
# or
git checkout -b docs/improve-readme-xxx
```

### 4. Make Your Changes

- Edit files locally using your favorite editor
- Follow the [Style Guidelines](#style-guidelines) below
- Test locally before committing

### 5. Commit & Push

```bash
# Stage your changes
git add .

# Commit with a clear message (see guidelines below)
git commit -m "Add: CSA57 Lab 3 - Searching algorithms (binary, linear)"

# Push to your fork
git push origin feature/add-csa57-lab3-solutions
```

### 6. Open a Pull Request

1. Go to [github.com/saveetha-labs/saveetha-labs.github.io](https://github.com/saveetha-labs/saveetha-labs.github.io)
2. Click **"Compare & pull request"**
3. Fill in the PR template:
   - Clear title describing what you changed
   - Explain **why** the change is needed
   - Include screenshots if relevant (for UI changes)
   - Link related issues (e.g., `Closes #123`)
4. Submit! 🚀

---

## Style Guidelines

### Commit Messages

Use the [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>: <description>

[optional body]
```

**Types:**
- `Add:` — New materials, files, features
- `Fix:` — Bug fixes, corrections
- `Update:` — Updates to existing content
- `Refactor:` — Code reorganization without behavior change
- `Docs:` — Documentation changes
- `Style:` — UI/visual changes, formatting
- `Remove:` — Remove files, features

**Examples:**
```
Add: CSA13 Lab 5 - NFA to DFA conversion programs
Fix: Correct boundary condition in CSA02 bubble sort
Docs: Update README with new course list
Style: Improve hover effects on repo cards
```

### Code Style

- **Comment your code** — Explain *why*, not just *what*
- Use consistent indentation (2 or 4 spaces, be consistent within files)
- Include a header comment with your name, date, and purpose
- For C/C++/Java programs, include sample input/output

**Example (C program):**
```c
/*
 * Binary Search Implementation
 * Author: Your Name
 * Date: 2026-08-12
 * Course: CSA57 - Fundamentals of Computing
 * Lab Set: 3
 *
 * Algorithm: Divide and conquer
 * Time Complexity: O(log n)
 * Space Complexity: O(1)
 */

#include <stdio.h>

int binarySearch(int arr[], int size, int target) {
    int low = 0, high = size - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (arr[mid] == target) return mid;
        else if (arr[mid] < target) low = mid + 1;
        else high = mid - 1;
    }
    return -1; // Not found
}

// ... rest of code
```

### HTML/CSS/JavaScript Style

- Use semantic HTML5 tags (`<section>`, `<article>`, `<nav>`, etc.)
- Follow CSS custom property conventions from `index.html` (`--accent`, `--bg`, etc.)
- Vanilla JavaScript only — no external libraries or frameworks
- Use `const` / `let` instead of `var`
- Add event listeners unobtrusively (not inline `onclick`)

---

## Pull Request Process

### What We Look For

✅ **Acceptable Contributions:**
- Well-commented, working code
- Accurate and relevant study materials
- Meaningful commit messages
- Follows style guidelines
- Passes basic sanity checks

⏳ **Requested Changes (Don't Worry!):**
- Missing comments or documentation
- Inconsistent formatting
- Minor bugs or edge cases
- Request for screenshots / more context

### Review Timeline

- Most PRs reviewed within **24–48 hours**
- If you don't hear back within a week, feel free to bump the thread
- Maintainers are student volunteers — patience appreciated! 🙏

### After Merging

- 🎉 Celebrate! You've contributed to open-source education
- Your GitHub profile gets a contribution graph entry
- You join the list of Saveetha Labs heroes on the README
- Keep contributing — every PR helps build your portfolio

---

## Reporting Issues

Found a problem? Great issue reports make Saveetha Labs better for everyone.

### When Reporting Issues, Include:

1. **Clear title** — Summarize the problem in one line
2. **Steps to reproduce** — What did you do to trigger the bug?
3. **Expected behavior** — What should happen?
4. **Actual behavior** — What actually happened? (Screenshots help!)
5. **Environment** — Browser, OS, screen size (for UI bugs)
6. **Suggested fix** — If you have an idea, share it!

### Issue Templates

- **Bug Report**: 🐛 Something is broken
- **Feature Request**: 💡 Something new you'd love to see
- **Content Request**: 📚 Missing course materials
- **Question**: ❓ Need help or clarification

---

## Community

### Where to Get Help

- **GitHub Discussions**: [orgs/saveetha-labs/discussions](https://github.com/orgs/saveetha-labs/discussions)
- **Issues**: For specific bugs or features
- **Classmates & Seniors**: Reach out on your college groups

### Recognition

- All contributors are listed in the repository graph
- Top contributors may be invited to join the Saveetha Labs org
- Build your public GitHub portfolio for placements
- Great talking points for interviews!

---

## Frequently Asked Questions

**Q: I'm new to Git/GitHub. Can I still contribute?**
A: Absolutely! Start with small fixes (typos, adding comments to code).
Here are great resources:
- [GitHub Git Handbook](https://guides.github.com/introduction/git-handbook/)
- [First Contributions Guide](https://github.com/firstcontributions/first-contributions)

**Q: Can I contribute course materials anonymously?**
A: You can use a pseudonym on GitHub if you prefer. The license still applies.

**Q: My code works but isn't "clean enough". Should I still submit?**
A: YES! Submit it. Reviewers will help polish it. Working code > perfect code.

**Q: How do I add a new course repository?**
A: Open an issue with the course code + name. Maintainers will create the repo and add you as a collaborator.

---

<div align="center">
  <h3>Thank You for Contributing! 💜</h3>
  <p>Every pull request, issue, and star helps create a better learning platform for thousands of Saveetha students.</p>
  <p>Made with ❤️ by students, for students.</p>
</div>
