# Runbook — the unattended weekly run

Root, not `docs/` — `docs/` is the GitHub Pages web root and anything there is
published.

The weekly digest is compiled and published by a **Claude cloud routine**, not
by a human and not by CI. Spec: [specs/0.6-weekly-autopublish.md](specs/0.6-weekly-autopublish.md).

- Routine console: <https://claude.ai/code/routines>
- Schedule: `0 13 * * 1` UTC = **Monday 06:00 America/Los_Angeles** while the
  Bay Area is on PDT. Cron is fixed UTC, so between November and March the run
  lands at 05:00 local. Harmless — the window is date-based, not clock-based —
  but that is why it looks an hour early in winter.

## What it does

Exactly the pipeline in [CLAUDE.md](CLAUDE.md), unattended: research per
`prompts/weekly-research.md` → write `data/<monday>.json` and
`digests/<monday>.md` → `validate.py` → `build.py` → commit → push.

**It publishes straight to the live site.** No review gate. `validate.py`
checks schema, vocabulary and window — not facts — so a wrong date or an
unverified lineup can go public before anyone reads it. That trade was made
deliberately; see the Decisions section of the spec.

**On validator failure it commits nothing.** One self-correction attempt, then
it stops and reports. The site keeps serving last week. There is no partial
publish.

**It may only write `data/`, `digests/` and `docs/events.json`.** Changing what
the digest *is* — the brief, the sources, the prompt, the page — is a human
edit, always.

## The routine prompt

The routine holds a copy of the text below. **This file is the canonical
version**: edit here, then paste into the routine so the two do not drift.

`PUSH_TARGET` is the one line that differs between the test phase and
production.

```
You are compiling and publishing this week's Culture Vulture digest for the
repository alexistosteson/culture-vulture. You are running unattended — there is
no human to ask, so where this prompt and the repo files disagree, the repo
files win, and where both are silent, do the conservative thing and say so in
your report.

PUSH_TARGET: main

Steps:

1. Read config/brief.yml, config/sources.yml, and prompts/weekly-research.md.
   prompts/weekly-research.md is your actual task specification — follow it in
   full, including its Verification pass checklist. This prompt only tells you
   how to run unattended.

2. Establish today's date from the environment, not from memory: run `date -u`.
   Compute the window from `schedule` in brief.yml — anchor on Monday,
   window_days forward. The data file is named for the window start:
   data/<window_start>.json.

3. Do the research and write:
     data/<window_start>.json
     digests/<window_start>.md

4. Install the validator's dependencies if they are missing, then validate:
     pip install pyyaml jsonschema
     python3 scripts/validate.py
   If it reports errors, fix the data file against those errors and run it once
   more. That is ONE correction attempt, not a loop.

5. If validate.py still reports errors after that one attempt: STOP. Commit
   nothing. Push nothing. Report the failure with the validator output quoted
   verbatim. Leaving last week published is the correct outcome — a stale week
   is better than a broken one.

6. If validate.py passes with zero errors:
     python3 scripts/build.py
   Then commit data/<window_start>.json, digests/<window_start>.md and
   docs/events.json in a single commit, and push to PUSH_TARGET. If PUSH_TARGET
   is not main, create that branch and push it; do not open a pull request.

   Commit message: "Week of <window_start>: <n> events" plus a one-line note on
   what dominates the week.

7. Never modify config/brief.yml, config/sources.yml, prompts/, scripts/,
   docs/index.html, or any workflow file. If the run seems to require changing
   one of those, do not — finish without it and say so in your report.

Report back, in this order:
  - Whether you published, and to what target. If you did not publish, why not.
  - The two or three things most worth doing this week, and why.
  - Anything you could not verify, and any event you marked low confidence.
  - Any vocabulary or region additions you would propose to brief.yml.
  - Whether the week is unusually busy or quiet, and what is driving that.
```

## Operating it

- **Run it now, off-schedule:** the Run button on the routine page, or ask a
  Claude Code session to run the routine.
- **Disable it:** toggle it off at <https://claude.ai/code/routines>. Weeks stop
  publishing; nothing else breaks. The manual pipeline in
  [CLAUDE.md](CLAUDE.md) still works and is unchanged.
- **A run failed:** read the run log from the routine page. The common causes,
  in the order worth checking — validator errors it could not fix (the report
  quotes them), no push permission, or a thin research week where too little
  cleared the brief.
- **A bad week went live:** `git revert` the routine's commit and push. The
  page picks up the previous week on the next load; `events.json` is fetched
  with a `?v=` cache-buster so no purge is needed.

## What is deliberately not tested

The Pages deploy and the cold load of the live page are exercised by every
hand-published week, and the routine's phase-1 check ran against a branch, so
neither was covered by that check. If the site ever fails to update while the
commit is visibly on `main`, that is a Pages problem, not a routine problem.
