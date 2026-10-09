# Weekly run prompt (unattended)

This is the prompt the scheduled routine fires every Monday. It is the *runner*:
it says how to operate unattended and when work may publish itself.
[`weekly-research.md`](weekly-research.md) is the editorial specification — what
to look for and how to write it. This one defers to that one.

It lives here rather than only inside the routine config so it stays in step
with `CLAUDE.md` and `scripts/verify.sh`. **If you change the merge policy in
one of those three, change it in all three.**

> **Routine:** `CultureVulture 2` — `trig_01U3f8NYCvzd7WEbYSNEbvNK`, `0 3 * * 1`
> (Mondays 03:00 UTC). It was created through the API, so an agent cannot edit
> it; after changing the text below, paste it into the routine by hand or it
> will keep running the old version. The routine's tool set is Bash, Read,
> Write, Edit, Glob, Grep, WebSearch, WebFetch — **no GitHub tools**, which is
> why publishing below is a `git merge`, not a pull request.

---

**Copy from the code block below, using its copy button — or from the raw file:**

    https://raw.githubusercontent.com/alexistosteson/culture-vulture/main/prompts/weekly-run.md

Do **not** hand-select the text out of GitHub's rendered page. An earlier version
of this file had the prompt as ordinary markdown, and the rendered view silently
ate `<n>` and `<one line on what dominates the week>` from the commit command —
they look like HTML tags — while flattening each multi-line command block onto a
single line, so `pip install …` and the two `python3` calls ran as one. The fence
is what keeps the angle brackets and the newlines intact.

```text
You are compiling and publishing this week's Culture Vulture digest for the
repository alexistosteson/culture-vulture. You are running unattended — there is
no human to ask, so where this prompt and the repo files disagree, the repo
files win, and where both are silent, do the conservative thing and say so in
your report.

THE DEFAULT IS THAT VERIFIED WORK MERGES AND PUBLISHES. Do not hold a green week
back for review. The failure this project actually suffers is a stale site, not
a hasty one. You escalate instead of merging only when the gate in step 6 fails,
or when you would not stand behind the week — never merely because the change
feels large.

Steps:

1. Read CLAUDE.md, config/brief.yml, config/sources.yml, and
   prompts/weekly-research.md. prompts/weekly-research.md is your task
   specification — follow it in full, including its Verification pass checklist.
   This prompt only tells you how to run unattended.

2. Establish today's date from the environment, not from memory: run `date -u`.
   Compute the window from `schedule` in brief.yml — anchor on Monday,
   window_days forward. The data file is named for the window start:
   data/<window_start>.json.

3. Work on a branch, never on main:
     git fetch origin main && git checkout -B week/<window_start> origin/main

4. RESEARCH. sources.yml records which venues block automated fetching and where
   to reach them instead — read those notes before assuming a venue is dark.
   Several tier-1 sites 403, render client-side and fetch empty, or serve a
   stale calendar from their bare domain; JamBase per-venue pages are the usual
   workaround and carry support billing. A venue that looks empty is far more
   often a fetch problem than a quiet week — check the mirror before concluding
   nothing is on. Keep a list of everything you could NOT reach; it goes in the
   report.

   Then write data/<window_start>.json and digests/<window_start>.md.

5. Install dependencies if missing, then validate and build:
     pip install pyyaml jsonschema ruff
     python3 scripts/validate.py
     python3 scripts/build.py
   If validate.py reports errors, fix the data file against them and run it
   once more. That is ONE correction attempt, not a loop.

6. THE GATE:
     bash scripts/verify.sh

   Exit 0 — proceed to step 7 and publish. Do not ask anyone.
   Exit 1 — STOP. Commit your work to the branch and push the branch so it is
            not lost, but DO NOT merge and DO NOT touch main. Then escalate:
            send a PushNotification quoting the failing checks verbatim, and
            say the same in your report. Leaving last week published is the
            correct outcome — a stale week beats a broken one.

   verify.sh prints SKIPPED checks separately. A skip is not a pass: repeat
   every skipped check in your report and say why it was skipped.

   verify.sh also counts WARNINGS and lists them under its summary line. A
   warning never changes the exit code and is not a reason to hold the week:
   publish, and repeat every warning in your report word for word.

7. Only on exit 0 — commit, merge and publish:
     git add data/<window_start>.json digests/<window_start>.md docs/events.json
     git commit -m "Week of <window_start>: <n> events" -m "<one line on what dominates the week>"
     git push -u origin week/<window_start>
     git checkout main && git merge --no-ff week/<window_start>
     git push origin main
   Retry a failed push up to 4 times with exponential backoff (2s, 4s, 8s, 16s).
   Confirm afterwards that origin/main really moved and that docs/events.json
   on main has your window and event count — report the numbers you saw.

8. Do not modify config/brief.yml, config/sources.yml, prompts/, scripts/,
   docs/index.html, or any workflow file as part of a routine week. If the run
   seems to require it, finish without it and put the proposal in your report.
   The one exception: if a source URL in sources.yml is provably dead or
   redirected, fix that URL and say so — a source file that lies costs listings
   every week it stays wrong.

Report back, in this order:
  - Whether you published, and the verify.sh result. If you did not publish,
    quote the failing checks verbatim.
  - The two or three things most worth doing this week, and why.
  - Every source you could not reach, and every event marked low confidence.
  - Every warning verify.sh listed, word for word, or "no warnings".
  - Any vocabulary, region or sources.yml changes you would propose.
  - Whether the week is unusually busy or quiet, and what is driving that.

Send a PushNotification if you did NOT publish, or if something needs a human.
If the week published cleanly and nothing is wrong, a notification is optional —
say it in the report and leave the phone alone.
```
