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
> why publishing below is a `git merge`, not a pull request, and why the run's
> proposals are pushed as `proposal/…` branches that
> `.github/workflows/proposals.yml` turns into pull requests for the owner.

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
     python3 -m pip install pyyaml jsonschema ruff
     python3 scripts/validate.py
     python3 scripts/drift.py
     python3 scripts/build.py
   If validate.py reports errors, fix the data file against them and run it
   once more. That is ONE correction attempt, not a loop.

   drift.py compares this week with the weeks before it, and the gate in
   step 6 runs it again — so answer it here. prompts/weekly-research.md says
   how, in its Verification pass. In short: a BLOCK line for a new spelling
   means use the established spelling it names; a BLOCK line for a thin venue
   means look at that venue again, add what you find, and if it is still
   flagged write its line under "## Thin this week" in the digest, naming the
   venue and saying reached or unreached and what you checked. Both are things
   you fix and move on from. They are not a reason to stop. COULD NOT CHECK is
   a reason to stop.

5a. Commit the week on the week branch (it is not pushed or merged yet):
     git add data/<window_start>.json digests/<window_start>.md docs/events.json
     git commit -m "Week of <window_start>: <n> events" -m "<one line on what dominates the week>"
   Call this commit WEEK (git rev-parse HEAD).

5b. PROPOSALS. A proposal is a change to config/sources.yml or config/brief.yml
   that you would make but must not (step 8). Each becomes a pull request the
   owner accepts or turns down; nothing here ever merges one. Anything that is
   not a change to those two files — "did this venue reopen?", an idea for the
   prompts, scripts or page — is a QUESTION for the report, never a proposal.
   A proposal can never hold the week back: if anything in this step goes
   wrong, drop that proposal, turn it into a question, and carry on.

   Kinds, and one branch per decision the owner makes:
     upkeep      one per week: proposal/<window_start>/upkeep — routes,
                 fallback, coverage/omits, reading notes and observed_venues
                 for venues sources.yml already lists or watches
     new-venue   one per venue: proposal/<window_start>/new-venue-<venue> —
                 one new watched entry in sources.yml
     site-change one per change: proposal/<window_start>/site-change-<what> —
                 brief.yml, plus the docs/events.json build.py makes from it
   Slugs are short, lowercase, letters, digits and hyphens.

   (i) Bring earlier proposals up to date first. See where they stand:
     python3 scripts/proposals.py --status
   It reads GitHub's branches and outcome tags with git ls-remote and shows
   any decided since the ledger was written (it records them in (iii)). A line
   it prints after the table is an error: quote it in the report and leave
   that record alone. Never edit a status by hand.
   For each record still "waiting", fetch its branch and test it against WEEK:
     git fetch origin proposal/<id>
     git checkout -B check WEEK && git merge --no-ff --no-edit FETCH_HEAD
     bash scripts/verify.sh
   If it merges cleanly and passes, leave it. If not (site-change proposals
   will hit this, because docs/events.json is rebuilt every week), rebuild its
   one commit onto WEEK on a local branch of the same name — cherry-pick,
   resolving docs/events.json by re-running python3 scripts/build.py — re-run
   verify.sh, and add a line to the commit body:
     Refreshed <today>: rebuilt onto the week of <window_start>.
   It is pushed in step 7a. If a re-fetch shows its reason no longer holds,
   leave the branch alone and say so in the report — closing it is the owner's.
   Return to the week branch when done: git checkout week/<window_start>

   (ii) Draft this week's proposals. Read proposals/ledger.json first. Do not
   propose again anything a waiting proposal already covers, or anything
   declined, unless something new justifies it — and then the new proposal
   says what changed. Every address you write into sources.yml is one you
   fetched and read in this run. For each proposal:
     git checkout -b proposal/<window_start>/<slug> WEEK
   make the change — for a site-change, also run python3 scripts/build.py so
   docs/events.json goes with it — then commit it, ONE commit per branch, with
   this message:
     Proposal (<kind>): <one line a reader of the site would understand>

     What changes: <in plain words>
     Why: <in plain words>
     What a reader of the site would notice: <usually "nothing" for upkeep>
     Evidence:
     - <every address you fetched to justify it> — <what it returned>

     Proposal-by: weekly-run
   The first line becomes the pull request's title and the rest its
   description, which is all the owner reads to decide — so plain words, in
   that order, and no file paths in the first line. The last line must be
   exactly "Proposal-by: weekly-run": it is how the outcome tells the run's
   own proposal from one a session changed.
   Then run bash scripts/verify.sh on the branch. Exit 1 — delete the branch
   (git branch -D) and make the idea a question in the report.

   (iii) Record them. Back on the week branch, record the outcomes from (i),
   then add each surviving new proposal:
     python3 scripts/proposals.py --status --write --week <window_start>
     python3 scripts/proposals.py --add <window_start>/<slug> <kind> "<the one line>"
   then commit proposals/ledger.json as a second
   commit on the week branch:
     git commit -m "Proposals for the week of <window_start>" proposals/ledger.json
   If nothing changed in the ledger, skip the commit.

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

7. Only on exit 0 — merge and publish (the week was committed in 5a):
     git push -u origin week/<window_start>
     git checkout main && git merge --no-ff week/<window_start>
     git push origin main
   Retry a failed push up to 4 times with exponential backoff (2s, 4s, 8s, 16s).
   Confirm afterwards that origin/main really moved and that docs/events.json
   on main has your window and event count — report the numbers you saw.

7a. Only once origin/main has the week — push the proposals:
     git push origin proposal/<window_start>/<slug>                  (new ones)
     git push --force-with-lease origin proposal/<id>                (refreshed ones)
   Same retries as step 7. Each becomes a pull request within a minute or two;
   you need not check. Force-pushing is allowed for proposal/ branches and for
   nothing else. If the week did not merge, push no proposal branch at all and
   delete them locally: a proposal never arrives for a week that did not
   publish.

8. Do not modify config/brief.yml, config/sources.yml, prompts/, scripts/,
   docs/index.html, or any workflow file as part of a routine week. If the run
   seems to require it, finish without it: a change to sources.yml or
   brief.yml becomes a proposal (step 5b); anything else goes in your report.
   The one exception: if a source URL in sources.yml is provably dead or
   redirected, fix that URL and say so — a source file that lies costs listings
   every week it stays wrong.

Report back, in this order:
  - Whether you published, and the verify.sh result. If you did not publish,
    quote the failing checks verbatim.
  - The two or three things most worth doing this week, and why.
  - Every source you could not reach, and every event marked low confidence.
  - Every warning verify.sh listed, word for word, or "no warnings".
  - The proposals: each one opened (its branch and its one line), each one
    refreshed, each one decided since last week and how, and every error
    proposals.py printed. Then the questions that are not proposals.
  - Whether the week is unusually busy or quiet, and what is driving that.

Send a PushNotification if you did NOT publish, or if something needs a human.
If the week published cleanly and nothing is wrong, a notification is optional —
say it in the report and leave the phone alone.
```
