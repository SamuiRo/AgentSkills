# AgentSkills

Skills for AI coding agents that came out of real, repeated work — not a collection.

Each one exists because the same context had to be explained to an agent at the start of session after session. Written down once, it now loads when the task matches.

Installing other people's skills rarely makes an agent better: it receives rules written for someone else's projects. Treat these as a starting point. Read them, keep what matches how you work, and change the rest.

## Skills

| Skill | What it does | Why it exists |
|---|---|---|
| [docs-and-versioning](plugins/docs-and-versioning/skills/docs-and-versioning/SKILL.md) | Role-based `docs/` structure (HANDOFF, ROADMAP, CHANGELOG, ARCHITECTURE, decisions, guides) and a versioning discipline: patch / minor / major decided by what a user can observe, manifests and changelog in the same commit. Includes structure and version-bump check scripts and doc templates. | Every new session started with the same explanation of where docs live and what counts as a breaking change. |
| [secure-repository-dependency-auditor](plugins/secure-repository-dependency-auditor/skills/secure-repository-dependency-auditor/SKILL.md) | Static inspection before installing packages or running an unfamiliar repository: lifecycle scripts, typosquatting, dependency confusion, release-age cooldown, pinning. Covers attacks aimed at the agent itself — prompt injection in repository files and web pages, hallucinated package names, poisoned skills and MCP servers. | An agent will run whatever install or build step a repository suggests. That should not depend on remembering to ask it to check first. |
| [design](plugins/design/skills/design/SKILL.md) | Base design procedure for websites, app UI, dashboards, slides and graphics: direction first, a few hard bans, countable budgets, render-and-look verification. `design_gate.py` counts the patterns that make UI code read as generated and keeps them from growing. | Default AI design converges on one look, and the same corrections were needed in every UI task. A project's own design skill builds on top of this one. |

## Install

### Claude Code (plugin marketplace)

```
/plugin marketplace add SamuiRo/AgentSkills
/plugin install docs-and-versioning@agent-skills
/plugin install secure-repository-dependency-auditor@agent-skills
/plugin install design@agent-skills
```

Install only the ones you need.

### Claude Code (plain skill folder)

Copy a skill folder from `plugins/<plugin>/skills/<skill>/` to:

- `~/.claude/skills/<skill>/` — for all projects, or
- `<project>/.claude/skills/<skill>/` — for one project.

Start a new session. The skill loads when a task matches its description.

### Other agents

Each skill is a `SKILL.md` with YAML front matter plus optional `references/`, `scripts/` and `templates/`. Any agent that reads skill folders can use it the same way.

## Before you install

Read every skill before installing it — these included. A skill is plain text, and the agent follows text. The scripts here run locally, make no network requests, and only read the project you point them at (`design_gate.py` also writes its own `.design-gate.json` when asked to update the baseline).

## Requirements

Python 3.8+ for the optional scripts (`check_docs_structure.py`, `check_version_bump.py`, `design_gate.py`).

## License

[MIT](LICENSE)
