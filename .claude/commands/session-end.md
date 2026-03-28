# Session End — Update TODO and Push

You MUST run this at the end of every session. Do not skip.

## Steps

1. **Detect what was done this session:**
   - Run `git diff --name-only` and `git diff --cached --name-only` in `/Users/nitish/stocks automation/`
   - Summarize the changes in 3-5 bullet points (what files changed, what was accomplished)

2. **Update TODO.md:**
   - Read `docs/TODO.md`
   - Under today's date header (`## YYYY-MM-DD`), add a `### Completed` section with the bullet points from step 1
   - If any new tasks were discovered during the session, add them to the appropriate backlog section
   - Do NOT remove or reorganize existing content — append only

3. **Stage and commit:**
   - `git add docs/TODO.md` plus any other unstaged work files
   - Commit with message: `session YYYY-MM-DD: [1-line summary of main accomplishment]`

4. **Push:**
   - `git push origin main` from `/Users/nitish/stocks automation/`
   - Confirm push succeeded. If it fails, report the error — do not force push.

5. **Confirm:** Print "Session end complete. TODO updated and pushed."
