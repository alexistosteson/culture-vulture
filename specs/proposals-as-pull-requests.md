# Spec — The weekly run's proposals arrive as pull requests

## Tier

**probe**, declared by the owner on 18 October 2026. That means a short-form spec, a
behavioural check the owner runs, and the run's own output as proof. No plan, no
code-safety audit, no tier registry and no merge ritual are owed. Nothing here reaches
the public on its own, because every proposal waits for the owner's click.

## Why

Each Monday the unattended run ends its report with changes it would make to the venue
list or the brief, and it makes none of them (`prompts/weekly-run.md` step 8). Those
proposals exist only in the report, which exists only in the run's own session, so
acting on one means a session re-reading prose. On 12 October there were eight
([`handoff/weekly-report-2026-10-12.md`](../handoff/weekly-report-2026-10-12.md)), and
none has been acted on.

The owner asked on 12 October that they arrive as pull requests, grouped rather than one
each. A pull request is a proposed change that the owner accepts with one click (Merge)
or turns down (Close). The design was agreed in chat on 18 October.

## What the owner sees

- Each Monday, **after the week has published**, GitHub shows him that week's proposals as
  pull requests. A proposal can never hold a week back: if the week does not publish,
  no proposals are opened.
- **One pull request per decision he has to make:**

  | Kind | One pull request per | What it may change | Example (12 Oct) |
  |---|---|---|---|
  | `upkeep` | week | `config/sources.yml` entries for venues already listed or already watched: routes, `fallback`, `coverage`/`omits`, reading notes, `observed_venues` | report items 1, 3, 4, 5 |
  | `new-venue` | venue | one new watched entry in `config/sources.yml` | item 2, Montalvo |
  | `site-change` | change | `config/brief.yml`, plus the rebuilt `docs/events.json` | item 7, Half Moon Bay and Stanford |

  Anything that is not a change to those two files, such as "did Starline reopen?", a
  call already made, or an idea for `prompts/`, `scripts/` or the page, stays a
  **question** in the report and in the weekly note. It never becomes a pull request.
- Each pull request's description says, in plain words and in this order: what changes;
  why; **what a reader of the site would notice if he accepts it** ("nothing" is the
  usual answer for upkeep); and the evidence, meaning every address the run fetched to
  justify it and what each returned. The site's checks run on it automatically.
- If he has not decided by the next Monday, the next run keeps it current and opens no
  duplicate (see "Keeping proposals current").
- A proposal he turns down is not proposed again unless something new justifies it, and
  the new proposal says what changed.

## The four-week trial (owner, 12 October)

Every proposal waits for his click for four weekly runs, counted from the first run that
opens one. If this build is live before the 26 October run, the trial covers 26 October
and 2, 9 and 16 November, and the **review is on 17 November**. The review counts:

- proposals accepted unchanged; accepted after a session changed them; turned down; and
  still waiting;
- **whether any accepted change cost listings**, meaning the venues it touched produced
  fewer listings in the weeks after it merged than before;
- how long each one waited.

**Assumed, and to be confirmed at the review, not before:** if the trial went well,
`upkeep` merges without him afterwards, and `new-venue` and `site-change` keep waiting
for him. Nothing in this build merges a proposal.

## How it works

### Who opens the pull request

The weekly routine can push branches but has no GitHub tools (`allowed_tools` is Bash,
Read, Write, Edit, Glob, Grep, WebSearch, WebFetch; confirmed 18 October). It does not
gain any. Instead:

- The run pushes each proposal as a branch named `proposal/<window_start>/<slug>`, where
  the slug is short and lowercase, for example `proposal/2026-10-26/upkeep` or
  `proposal/2026-10-26/new-venue-montalvo`.
- A new workflow, `.github/workflows/proposals.yml`, runs on a push to `proposal/**`. If
  that branch has no open pull request, it opens one against `main`. The title is the
  branch's newest commit subject, the body is that commit's message body, and it gets the
  labels `proposal`, `kind:<kind>` and `week:<window_start>`, creating any label that is
  missing. A pull request that already exists is left alone.
- On a later push to a branch that already has a pull request (a refresh, below), it
  leaves the title and description alone and adds a comment saying what was refreshed.
- On a pull request being closed, it **records the outcome as a tag**, then **deletes the
  `proposal/…` branch**. The tag is `proposal-outcome/<window_start>/<slug>/<outcome>`,
  where the outcome is `accepted`, `accepted-changed` (the branch had commits from
  someone other than the run) or `declined`, read from the event. Recording it from the
  event works with any merge button; the repository allows merge, squash and rebase
  merges (checked 18 October). A `proposal/…` branch that still exists therefore means
  "waiting". Nothing else ever deletes one.
- The workflow declares only the permissions it uses: `contents: write` to tag and delete,
  and `pull-requests: write` to open pull requests and comment on them.
- **Owner, once:** tick *Allow GitHub Actions to create and approve pull requests* under
  the repository's Settings → Actions → General. This is checked off from 18 October
  (it reads `can_approve_pull_request_reviews: false`, so the box is **not** ticked yet). The agent never changes a repository
  setting. The build gives him a click-by-click page for it. Nothing here approves a
  pull request.
- A pull request opened by the workflow's own token does not start the `pull_request` CI
  run. The checks still appear on it, because the branch push triggers the push CI run:
  every proposal touches `config/**`, which is in its path filter. Verify this on the
  first pull request.

### What the run does, and in what order

The weekly prompt gains a proposals step between the gate and publishing. The stage
order is fixed:

1. Research, data, digest and build, exactly as today.
2. **Commit the week** on the week branch: data, digest and `docs/events.json`, as
   step 7 commits them today.
3. **Draft proposals.** Write each proposal on its own local branch **cut from that week
   commit**, one commit per branch. The commit subject is
   `Proposal (<kind>): <one line a reader understands>`; the body is the description
   above. Every address written into `sources.yml` is one the run fetched and read this
   run (CLAUDE.md, rot-check spec). Run `bash scripts/verify.sh` on each branch. A branch
   that exits 1 is dropped and its idea goes into the report as a question.
4. **Record them.** Add each surviving proposal to `proposals/ledger.json` (below) as a
   second commit on the week branch, so the record publishes with the week.
5. The gate, then merge the week, exactly as today.
6. **Only if the week merged:** push the proposal branches. Because they were cut from
   the week branch and `main` now contains it, each pull request shows only its own
   change. If the week did not merge, push none and delete them locally.

Step 8 of the weekly prompt keeps its one exception: a source address that is provably
dead or redirected is still fixed directly, as today, because a wrong address costs
listings every week it stays wrong.

### The ledger: `proposals/ledger.json`

`proposals/ledger.json` is a list kept at the repository root, not under `docs/`. It holds
one record per proposal, and the run updates it in each week commit:

```json
{"id": "2026-10-26/new-venue-montalvo", "week": "2026-10-26", "kind": "new-venue",
 "summary": "Start watching Montalvo Arts Center in Saratoga",
 "status": "waiting", "decided_week": null}
```

`status` is `waiting`, `accepted`, `accepted-changed` or `declined`. The run reads it
from the remote with `git ls-remote`, with no GitHub tools: an outcome tag gives the
status, and a branch with no tag is `waiting`. A branch gone with no tag is reported as
an error, never guessed.

The ledger is how the run avoids re-proposing a declined change, and it is the source the
trial review counts from (cross-checked against the pull requests themselves). It is not served on the site;
the note's build copies proposal states out of it. The weekly
note will read it to show each proposal's state (see
[`weekly-public-note.md`](weekly-public-note.md)). A small script works the statuses out
and validates the file, and `scripts/verify.sh` runs its offline self-test. The script's
name and shape are the builder's call.

### Keeping proposals current

At the start of the proposals step, for each `waiting` record:

- If the branch still merges cleanly into the new `main` and passes `verify.sh`, leave it.
- If it does not, which `site-change` proposals will hit because `docs/events.json` is
  rebuilt every week: rebuild that one commit onto the new week, force-push the same
  branch name, and add a line to the description saying it was refreshed. Force-pushing
  a `proposal/…` branch is allowed. Force-pushing any other branch is not.
- If a re-fetch shows the reason no longer holds, leave the branch and say so in the
  report. Closing pull requests is the owner's job.
- A new item that duplicates a waiting proposal is not proposed again. Each week's new
  upkeep items get that week's own `upkeep` branch. If two upkeep branches conflict once
  one merges, the refresh rule above rebuilds the other.

### Also folded in

- **The schema check the run skipped.** Change the install line in `weekly-run.md` step 5
  to `python3 -m pip install pyyaml jsonschema ruff`, so the checker lands in the Python
  the gate runs. On 12 October a plain `pip` installed into another Python, the check
  reported SKIPPED, and it was hiding two bad listing ids. This closes that `BACKLOG.md`
  row.
- **The routine's stored prompt.** `weekly-run.md` changes, and the routine runs a pasted
  copy. Try updating the routine's stored prompt through the routine API (both copies,
  `job_config` and `session_request`), then read it back and compare. If the update is
  refused, give the owner the paste instructions at the top of `weekly-run.md` as a
  click-by-click page.

## Out of scope

- Merging any proposal, and turning on GitHub's auto-merge. That follows the review.
- Proposals that change `prompts/`, `scripts/`, `docs/index.html` or a workflow.
- The weekly note itself. That is its own spec, and this one only provides the ledger it
  reads.

## First exercise

The 12 October week's proposals, rebuilt by hand by the build session as the first three
real pull requests. **Re-fetch every address before writing it**, because six claims in
the 8 October route research were later overturned:

- `upkeep`: items 1, 3, 4 and 5;
- `new-venue`: item 2, Montalvo;
- `site-change`: item 7, Half Moon Bay and Stanford. It carries a rebuilt
  `docs/events.json`.

Items 6 (Starline) and 8 (the costume sale) go to the owner as questions.

## Done when

1. `bash scripts/verify.sh` exits 0 on the branch, and the ledger self-test is shown able
   to fail: plant one wrong status and show it caught, printing how many records were
   checked.
2. A test `proposal/…` branch pushed from this Mac opens a pull request with the right
   title, body and labels; checks appear on it; closing it deletes the branch. The test
   pull request is closed, not merged.
3. The three first-exercise pull requests are open, with checks green.
3a. A one-time run of the routine itself (not this Mac) pushes a test `proposal/…`
   branch and then force-pushes it. Earlier routines could push only some branches, so
   this is not assumed.
4. The stored routine prompt matches `weekly-run.md`, read back and compared.
5. **The owner's behavioural check**, as a click-by-click HTML page: he opens one of the
   three pull requests, reads its description, and says whether he could decide from it
   alone; then he accepts or turns it down.
6. After the first unattended run that opens proposals (26 October): the pull requests
   appeared after the week published, the ledger matches the remote, and nothing waiting
   was duplicated. Record it below.
7. The 17 November review is on Agent's Cal.

## Evidence

*(filled in as the build runs)*

**Done when 1 (18 Oct).** `verify.sh` exits 0 on `main` after merge `dac52af`. Planted
`"status": "approved"` in record 1 of the ledger: `--check` printed
`record 1 (2026-10-12/upkeep): status 'approved' is not one of waiting, accepted,
accepted-changed, declined` and exited 1; `verify.sh` printed
`FAIL  proposals.py`, `self-test passed: 15 cases, 19 records checked`, the same record
line, `passed 12   failed 1`, and exited 1. Reverted; `--check` back to
`ledger ok: 4 records checked`.

**Done when 2 (18 Oct).** Test branch pushed from this Mac opened PR #4: title from the
commit subject, body from the commit body without the trailer, labels `proposal`,
`kind:new-venue`, `week:2026-10-12`. Checks on it: `open` pass, `validate` pass. Closed
with `gh pr close`; the close run (`pull_request_target`) wrote tag
`proposal-outcome/2026-10-12/new-venue-pipeline-test/declined` and deleted the branch.
Test tag then deleted. Side effect: each proposal PR also starts a `pull_request`-event
`validate` run that GitHub parks as *action required* (PRs opened by the workflow token
need a maintainer's approval to run workflows). It does not appear among the PR's
checks; the push-event `validate` run covers the same commit.

**Done when 3 (18 Oct).** Four, not three (see the handoff for why). Ledger records added
and merged first (`dac52af`), then PRs #5 upkeep, #6 Neck of the Woods, #7 Montalvo,
#8 six more towns opened with correct labels; every one shows `open` pass and `validate`
pass. `--status` reads all four as `waiting`.

**Done when 5 (18 Oct, in part).** The owner read PR #7 (Montalvo) and answered, in
chat: "Yes, I could decide from the description alone." His accept or close had not
reached GitHub when checked (PR still open, no outcome tag); recorded when it does.

**Done when 7 (18 Oct).** On Agent's Cal for 17 November; the owner acknowledged it.
