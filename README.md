# AI Universal Agent

**AI Universal Agent** is a GitHub Actions bot that combines **multi‑language static analysis** with **LLM‑powered summarization** to deliver actionable pull request reviews. Instead of just failing builds or dumping analyzer logs, it acts like a **reviewer**: detecting issues, prioritizing fixes, and posting clear, structured feedback directly into your PRs.

---

## 🚀 What It Does
- **Detects languages & tools** in your repository (Java, Python, JavaScript, Ruby, Go, PHP, .NET, Docker, Terraform, Kubernetes).
- **Runs analyzers & security scanners** (Ruff, ESLint, Bandit, SpotBugs, PMD, Trivy, tfsec, Semgrep, and more).
- **Summarizes results with AI** into:
  - A repository health overview
  - A prioritized list of fixes with severity and suggested commands
  - Line‑level suggestions when available
- **Posts feedback directly in GitHub PRs** as comments — no extra dashboards or tools required.

---

## 🎯 Why It’s Different
- **Novel integration**: Traditional CI analyzers + AI summarization in one workflow.
- **Universal**: Works across multiple languages and infrastructure stacks.
- **Actionable**: Converts noisy logs into clear, prioritized recommendations.
- **Seamless**: Feedback appears right in the PR conversation, where developers need it.

---

## 🧠 One‑liner Pitch
> *AI Universal Agent: a GitHub Actions bot that reviews pull requests with static analyzers and LLMs, delivering actionable insights across any language.*
