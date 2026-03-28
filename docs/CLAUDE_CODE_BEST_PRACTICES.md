# Claude Code Best Practices — Implementation Status

**Based on:** [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice)
**Implemented:** 2026-03-28
**Last Updated:** 2026-03-28

---

## What Was Implemented

### Phase 1: Commands (DONE)

Location: `/Users/nitish/stocks automation/.claude/commands/`

| Command | File | Purpose | Status |
|---------|------|---------|--------|
| `/session-end` | `session-end.md` | Updates TODO.md, commits, pushes to GitHub | DONE |
| `/quick-screen` | `quick-screen.md` | Fast stock screening with quality scorecard (/25) | DONE |
| `/research` | `research.md` | Full multi-bagger research framework via subagent | DONE |
| `/portfolio-check` | `portfolio-check.md` | Live holdings vs research theses comparison | DONE |

**Token savings:** ~2000-3000 tokens per command invocation (vs typing instructions manually).

### Phase 2: Skill Migration (DONE)

Location: `/Users/nitish/stocks automation/.claude/skills/stock-research/`

| File | Purpose | Status |
|------|---------|--------|
| `SKILL.md` | Full research framework merged from COMPOSITE_SKILL.md + CLAUDE.md | DONE |
| `gotchas.md` | Known failure points, scoring criteria, data source warnings | DONE |
| `references/_TEMPLATE.md` | Copy of research template | DONE |
| `references/data-sources.md` | Approved data sources for India equity research | DONE |

**Key feature:** `context: fork` — research runs in isolated subagent, saving ~5000-10000 tokens from main context.

**What moved here:** The entire Multi-Bagger Framework (Phases 0-5) that was previously inline in CLAUDE.md. Now loads only when stock research is triggered.

### Phase 3: Rules Migration (DONE)

Location: `/Users/nitish/stocks automation/.claude/rules/`

| Rule File | Migrated From | Content |
|-----------|--------------|---------|
| `session-end.md` | `feedback_always_update_todo.md` | Update TODO.md + push at session end |
| `no-fabricated-data.md` | `feedback_no_fabricated_data.md` | Never make up stock data |
| `writing-quality.md` | `feedback_research_writing_quality.md` | Narrative over formula, with examples |
| `research-log-format.md` | `feedback_research_log_format.md` | Keep full content, merge into sections |
| `no-structural-changes.md` | `feedback_no_changes_without_asking.md` | Don't restructure without asking |
| `single-repo.md` | `feedback_no_duplicate_repo.md` | Single working copy only |
| `readme-accuracy.md` | `feedback_readme_accuracy.md` | Keep README in sync |

**Why:** Rules in `.claude/rules/` load deterministically every session. Memory files had staleness warnings and weren't guaranteed.

**TODO:** Remove the original memory files after confirming rules work (keep for 1 week as safety net).

### Phase 4: Agents (DONE)

Location: `/Users/nitish/stocks automation/.claude/agents/`

| Agent | File | Purpose |
|-------|------|---------|
| Research Analyst | `research-analyst.md` | Deep stock research with full framework access |
| Portfolio Reviewer | `portfolio-reviewer.md` | Portfolio monitoring against research theses |

Both configured for `claude-opus-4-6` model.

### Phase 5: Hooks (PENDING)

| Hook | Purpose | Status |
|------|---------|--------|
| Stop hook | Remind about TODO.md if not updated | PENDING — needs settings.json config |
| PostToolUse hook | Auto-render MD in Chrome after editing research files | PENDING — needs settings.json config |

### Phase 6: CLAUDE.md Optimization (PENDING)

| Item | Status |
|------|--------|
| Trim CLAUDE.md from 238 to ~70 lines | PENDING — waiting for skill verification |
| Move research framework to skill | DONE (skill has it, CLAUDE.md still has it as fallback) |
| Keep autonomy rules + data sources in CLAUDE.md | Will keep |

---

## Final Directory Structure

```
/Users/nitish/stocks automation/
├── .claude/
│   ├── commands/
│   │   ├── session-end.md
│   │   ├── quick-screen.md
│   │   ├── research.md
│   │   └── portfolio-check.md
│   ├── skills/
│   │   └── stock-research/
│   │       ├── SKILL.md
│   │       ├── gotchas.md
│   │       └── references/
│   │           ├── _TEMPLATE.md
│   │           └── data-sources.md
│   ├── agents/
│   │   ├── research-analyst.md
│   │   └── portfolio-reviewer.md
│   └── rules/
│       ├── session-end.md
│       ├── no-fabricated-data.md
│       ├── writing-quality.md
│       ├── research-log-format.md
│       ├── no-structural-changes.md
│       ├── single-repo.md
│       └── readme-accuracy.md
├── CLAUDE.md                        (to be trimmed in Phase 6)
├── skills/india-equity-report/      (old location, kept as archive)
└── ... (rest of project unchanged)
```

---

## What We Learned from the Best Practices Repo

### Key Principles Applied

1. **Commands over manual prompting** — If you do something daily, make it a `/command`
2. **Skills with `context: fork`** — Heavy analysis in isolated subagent, main context stays clean
3. **Rules over memory** — `.claude/rules/` loads deterministically; memory files don't
4. **Progressive disclosure** — Skill has references/ folder; gotchas grow over time
5. **Don't babysit** — Commands and agents do the work; user just invokes
6. **CLAUDE.md under 200 lines** — Move heavy content to skills, load on demand

### What We Chose NOT to Implement

- **Cloning the best practices repo** — It's a reference, not a dependency
- **Complex hook chains** — Starting simple; can add later
- **Agent teams with tmux/worktrees** — Overkill for single-user research workflow
- **Ralph Wiggum loop** — Not needed; research is interactive, not autonomous

---

## Phase 7: Meta-Refinement (repo's own adoption advice)

The repo warns: **"Vanilla cc is better than any workflows with smaller tasks."** We built 20 files. Before adding more, we must validate what actually helps.

### 7A. SKILL.md Refinement — Goals Over Steps (PENDING)

The repo says: **"Don't railroad Claude in skills — give goals and constraints, not prescriptive step-by-step."**

Our SKILL.md is ~200 lines of step-by-step procedure. Anti-pattern per the repo. Claude already knows how to research stocks — the skill should add our SPECIFIC rules only:
- Data source constraints (what's blocked, what's approved)
- Quality scorecard (our custom framework)
- Writing quality bar (narrative, not formula)
- Output location and format

**Action:** Trim SKILL.md to ~80 lines of goals + constraints. Move the step-by-step into `references/methodology.md` for Claude to consult IF needed, not force-feed.

### 7B. Test Before Scaling (PENDING)

The repo says: **"Prototype over PRD — build 20-30 versions instead of writing specs."**

**Action:** Test each command on a real stock in a fresh session:
- [ ] `/quick-screen KAYNES` — does it produce a useful verdict?
- [ ] `/research NEWGEN` — does the skill trigger correctly with context:fork?
- [ ] `/portfolio-check` — does it pull from Kite and cross-reference?
- [ ] `/session-end` — does it correctly detect changes and push?

After each test, note what worked/broke and iterate. Don't try to perfect before using.

### 7C. Operational Settings (PENDING)

The repo recommends these Claude Code config settings:

| Setting | Value | Why |
|---------|-------|-----|
| Thinking mode | `true` | See Claude's reasoning for better debugging |
| Output style | `explanatory` | Detailed output with insight boxes |
| Manual `/compact` at 50% | habit | Don't let auto-compact lose context |
| `/rename` sessions | habit | Label sessions for `/resume` later |
| `ultrathink` keyword | use in prompts | High-effort reasoning for complex analysis |

### 7D. Wildcard Permissions (PENDING)

The repo says: **"Use /permissions with wildcard syntax instead of dangerously-skip-permissions."**

Our `settings.local.json` is 60KB of individual command allowlists. Should be replaced with patterns:
- `Bash(python3 src/*)` — all analysis scripts
- `Bash(git *)` — all git operations
- `WebFetch(screener.in/*)` — all Screener.in pages
- `WebFetch(trendlyne.com/*)` — all Trendlyne pages

**Action:** Audit current allowlist, replace with ~20 wildcard patterns.

### 7E. Memory Cleanup (PENDING — after 1 week)

Once rules in `.claude/rules/` are confirmed working across multiple sessions:
- [ ] Remove `feedback_always_update_todo.md` from memory
- [ ] Remove `feedback_no_fabricated_data.md` from memory
- [ ] Remove `feedback_research_writing_quality.md` from memory
- [ ] Remove `feedback_research_log_format.md` from memory
- [ ] Remove `feedback_no_changes_without_asking.md` from memory
- [ ] Remove `feedback_no_duplicate_repo.md` from memory
- [ ] Remove `feedback_readme_accuracy.md` from memory
- [ ] Update MEMORY.md index to remove Standing Rules section (now in .claude/rules/)

---

## Implementation Order (Updated)

```
DONE:
  Phase 1: Commands (4 commands)
  Phase 2: Skill migration (SKILL.md + gotchas + references)
  Phase 3: Rules migration (7 rules)
  Phase 4: Agents (2 agents)

NEXT:
  Phase 7A: Trim SKILL.md to goals+constraints (not step-by-step)
  Phase 7B: Test all 4 commands on real stocks
  Phase 7C: Configure operational settings (thinking, output style)
  Phase 7D: Wildcard permissions (replace 60KB allowlist)

LATER (after validation):
  Phase 5: Hooks (stop + PostToolUse)
  Phase 6: CLAUDE.md trim (238 -> ~70 lines)
  Phase 7E: Memory cleanup (remove duplicate feedback files)
```

### Future Improvements to Consider

- [ ] Hook: auto-format code on save (PostToolUse)
- [ ] Hook: session-end reminder (Stop hook)
- [ ] `/compare` command: side-by-side stock comparison
- [ ] `/sector-screen` command: screen all stocks in a sector
- [ ] Quality scorecard as a separate skill with its own references
- [ ] Clean up old `skills/india-equity-report/` after migration confirmed
