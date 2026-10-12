# Handoff — two builds in design: proposals as pull requests, and a public weekly note · 12 October 2026

Session name: Draft the build spec for the rot-detection checks

Read `CLAUDE.md` first; it is binding. **`docs/` is the published web root.** The owner is a
non-technical product manager: bring him product choices in plain words, decide the
mechanics yourself, end on a recommendation.

## Changed since last session

- The rot-check build is closed. The owner's check passed (10 October) and the first
  unattended run published (12 October); both are recorded at the foot of
  [`specs/rot-checks-build.md`](../specs/rot-checks-build.md) §10. Nothing is owed there.
- `main` is the 12 October week: 415 listings, gate exit 0, 8 warnings.
- On 12 October the owner asked for two new things. **Neither is designed, specced or
  started.** This file is the state of that conversation.

## The two asks, in the owner's words

1. "the proposed changes should be proposed as PRs, with some degree of consolidation —
   there are 6-7 changes proposed this time, is it reasonable to consolidate some or better
   to have each one be a PR"
2. "the write up … should effectively become a public-facing release note, linked back
   from the CultureVulture posting"

The write-up he means is the run's closing report, saved verbatim at
[`weekly-report-2026-10-12.md`](weekly-report-2026-10-12.md). It existed only in the
run's own session until he pasted it.

## Where the conversation stands

Process: `superpowers:brainstorming` was invoked and the work classified as the heavier
path — each ask changes how the weekly run and the page fit together. Under this
project's rules that means **two short-form specs in root-level `specs/`, probe tier
unless the owner says otherwise, no plan document**, each approved by him before
anything is built.

**Told to the owner on 12 October** (he has not yet replied to any of it):

- *Answer to his consolidation question:* group, do not split one each. The rule
  recommended: **one pull request per decision he has to make**, because a pull request is
  accepted or declined whole — so never bundle something he might decline with things he
  would wave through. This week's eight proposals sort into three pull requests and two
  questions:

  | Group | Report items | Why together |
  |---|---|---|
  | A · Venue-list upkeep | 1 (six rooms), 3 (A.C.T. partial), 4 (Roxie read twice), 5 (Litquake) | Corrections to how existing coverage is recorded. Nothing a reader sees changes. Clears six warnings. |
  | B · A new venue to watch | 2 (Montalvo) | Adds a venue the project promises to check weekly. Removing one was ruled the owner's editorial call (rot-check spec, step 7); adding one is the same class. |
  | C · Region lists | 7 (Half Moon Bay, Stanford and the rest) | Changes the brief, and so what the site shows. |
  | Not a pull request | 6 (Starline: did it reopen?), 8 (the opera costume sale, already published) | A question to look into, and a call already made that he keeps or reverses. |

- *Understanding written back for the note:* he said "public-facing release note" and
  "linked back from the CultureVulture posting". **Assumed, and stated to him as an
  assumption:** "the posting" is the site's own page for the week, and the note is one
  page per week that stays at a permanent address.
- *The one question asked:* who the note is for — people deciding what to do this week,
  people following how the project is built, or both. Recommended: both, in one note with
  two parts — the reader's part first (what is most worth doing, busy or quiet, what is
  missing or uncertain), then a shorter "behind this week" part (what could not be
  reached and why, the changes proposed, linking to the pull requests).

**His answer to that question is the next thing needed.** If the new session opens
without it, ask it again, alone.

## Facts already established — do not re-derive

- **The run can open pull requests.** Cloud sessions opened #1, #2 and #3 in this
  repository from `claude/…` branches; all merged. CI runs on every `pull_request`,
  unfiltered. GitHub Actions here cannot create pull requests (workflow permissions are
  read-only) and nothing needs it to.
- **How the run is told things.** `prompts/weekly-run.md` (lines 118–134) says to put
  proposals in the report and gives the report's order. The routine's stored prompt is a
  paste of that file: a change to it reaches the run only when the owner pastes it again.
  `prompts/weekly-research.md` is read from the repository on every run, so anything
  written there needs no paste (rot-check spec §3).
- **The run edits nothing in `config/` or `prompts/` on `main`.** Pull-request branches
  keep that true: a proposal lives on its own branch and the run never merges it.
- **Every address written into the venue list is one that was fetched and read.** That
  rule has to hold inside a proposed pull request too.
- **A pull request that changes the brief must carry the rebuilt `docs/events.json`,**
  or CI fails it; and if a new week lands on `main` first, that file will conflict.
  Group C is where this bites. Not designed.
- **The report is saved nowhere by the run.** The digest is
  (`digests/<week>.md`, public on GitHub, 1,184 lines this week: Week at a Glance, a
  section per day, Thin this week, What could not be reached, Sources). The page links to
  neither; its footer (`docs/index.html`, near line 368) links only to the brief and the
  schema on GitHub.
- **A note on the site has to live under `docs/`** — it is the only published folder —
  and follows the page rules in `CLAUDE.md`: light only, no `prefers-color-scheme`, no
  geography hardcoded.
- The report as written contains things not fit for a public note as they stand: file
  and command names, the gate's internals, the run's machine. What is public and what is
  bookkeeping is the owner's call (the question above).
- A related row already in `BACKLOG.md`: the run's machine skips the schema check unless
  it installs the checker against the right Python. Fold the fix into whichever build
  edits the run's prompt.

## Read only these

- [`weekly-report-2026-10-12.md`](weekly-report-2026-10-12.md) — the raw material.
- `prompts/weekly-run.md` and the verification pass of `prompts/weekly-research.md`.
- `config/sources.yml` header, when group A is built.
- `BACKLOG.md` — the three rows added 12 October.

## Do not re-read

- Every earlier `handoff/session-*.md`.
- `specs/rot-checks-build.md` beyond the foot of §10, unless a rot check itself is in
  question.

## Next action

1. Get the owner's answer on who the note is for. One question at a time after that;
   likely next: whether the reader's part may quote the run's picks as written or is
   edited by him first, and whether a pull request the run opens may ever be merged
   without him.
2. Present each design to him, get his yes, then write the two short-form specs in
   `specs/` with a `## Tier` each.
3. Build on a branch per spec. For the pull-request build, **this week's groups A, B and
   C are the first exercise** — re-fetch every address before writing it.
4. Starline Social Club and the opera sale want an answer either way; bring them to the
   owner as questions, not pull requests.

## Constraints

- The Monday run fires 03:04 UTC every Monday. Anything it must do differently has to be
  in the repository — and in the pasted prompt, if `weekly-run.md` changes — before then.
- A stale site is this project's standing failure. Nothing here may add a step that can
  stop a week publishing.
- The DICE key is never written to any file. The repository is public.
- The main checkout has an untracked `specs/next-gen/`. It is not this work's; leave it.

## Lessons

- Merging from a worktree: `git merge-tree --write-tree origin/main HEAD` →
  `git commit-tree` with both parents → `git push origin <commit>:refs/heads/main`, then
  fast-forward the main checkout with `git -C`.
- A commit under a made-up author name is refused by this Mac's identity check; do not
  commit inside throwaway clones.
