# Spec — A public weekly note, linked from the site

## Tier

**production**, declared by the owner on 18 October 2026. The note is a new public page.
It publishes every week without anyone reading it first, and a wrong or leaky note
looks exactly like a right one. When the Almanac design was put live, that step was held
to the same level (`specs/0.5-almanac-redesign.md`). Owed: this spec, a pre-plan
code-safety audit over the files below, a written plan, an audit of the written code
before merge, the owner's behavioural check, and a block in the tier registry at merge.

**Where things go in this repository.** `docs/` is the published web root, so nothing
but site files goes there. The plan goes in `specs/plans/`. The tier registry the
`delivery-tiers` skill expects at `docs/handoff/tiers.md` goes at `specs/tiers.md`
instead, and `tier-check.py` is pointed at it if it allows; if it does not, say so in
the plan.

## Pre-plan audit

*(to be filled before the plan: `/nasa-code` over the files listed under "Files")*

## Why

The weekly run's closing report is the most readable thing the project makes: the two or
three things most worth doing, how busy the week is and why, what could not be reached,
and what is uncertain. It exists only in the run's own session. On 12 October the owner
asked that it "effectively become a public-facing release note, linked back from the
CultureVulture posting".

## Decided with the owner

- **Who it is for (12 October):** both people deciding what to do this week and people
  following how the project is made. One note, with the reader's part first.
- **"The posting" is the site (12 October).**
- **It publishes automatically with the week, exactly as the run wrote it (12 October).**
  He does not read it first. A mistake is corrected after the fact.
- **The design as mocked up is approved (18 October):**
  [`specs/mockups/weekly-note.html`](mockups/weekly-note.html). Every choice in it is
  binding unless it is listed under "Calls made by the session" below.

## What the reader sees

### On the site

- One line under the week's dates, "This week's note →", shown at every width,
  including phones (the intro sentence is hidden on phones, so the link cannot go there).
- **A week with no note shows no link.** Nothing ever reads "note missing".
- "Earlier notes" added to the small print at the foot of the site. (The mockup
  simplified that line. The live text names the brief and the schema, and stays.)

### The note (one page per week, each at a permanent address)

Reader's part, in this order:

1. Eyebrow "Culture Vulture · Weekly note"; the heading "The week of <date>"; the dates;
   a lede of one or two sentences.
2. **Most worth doing:** two or three picks, each with a title, a venue, when, a price
   and why. Optionally one or two "Also" mentions.
3. **Busy or quiet:** one paragraph on what is driving the week.
4. **What's missing or uncertain:** written as advice to a reader ("Check
   litquake.org"), not as a list of errors, including how many listings are uncertain.

Then **Behind this week**, set apart in a shaded box so a casual reader can stop before
it:

5. **What we couldn't reach:** in plain words.
6. **Changes proposed:** each with its current state (waiting, accepted or turned down)
   and a link to its pull request on GitHub.
7. **Open questions.**

Foot: back to this week's listings; earlier notes; "Written by the weekly run · corrected
after the fact if needed"; and the correction, if there is one.

**Never in public:** file and folder names, commands, the checks' names or internals,
the run's machine or tools, warnings quoted from the gate, or anything in backticks. The
full technical report stays in the run's session, as today.

## How it works

### The run writes words; the build supplies the facts

- The run writes **`notes/<window_start>.json`** at the repository root, beside `data/`
  and `digests/`. Its prose may contain numbers from its research ("six of its 80-plus
  events", "thirty years"). It never states **counts of this week's listings**, because
  the build supplies those: the page shows them in a facts line under the lede ("415
  listings · 21 uncertain") and in the "uncertain" item, never inside the run's
  sentences.
- `scripts/build.py` publishes it to **`docs/notes/<window_start>.json`**, adding facts
  taken from `data/<window_start>.json` and `proposals/ledger.json`: the dates; the
  total listings; how many listings are below `high` confidence, and out of how many;
  each pick's venue, dates, time and price **looked up from the listings it names**; and
  each proposal's current state. A note therefore cannot get a count, a date or a price
  wrong, and cannot pick an event that is not listed.
- The build also writes `docs/notes/index.json`, the list of weeks that have a published
  note, and sets a flag in `docs/events.json` when the newest week has one. The front
  page shows the link only when that flag is set.
- **Each build republishes every week's note**, so proposal states in older notes stay
  current. An older note that fails a check tightened since it was written keeps its last
  published copy, and the gate prints one `WARN` naming it; only the newest week's
  note can be newly withheld. A correction is an edit to `notes/<week>.json` plus a rebuild, and it records
  a short `corrected` line that the page shows at the foot.

### What the run writes (schema `schema/note.schema.json`)

`window_start`; `lede`; `picks` (2–3), each `{event_ids: [one or more], title, why,
where?}`, where `title` is a short display title ("heavens to betsy" for a listing
titled with its support acts) and `where` optionally shortens the venue ("Mid-Market,
San Francisco"). A pick naming several listings (two nights of one show) shows all their
dates ("Sat 17 & Sun 18"). Dates, times and prices always come from the listings.
`also` (0–2) has the same shape; `pulse` `{verdict: busy | typical | quiet, text}`; `gaps`
(reader-facing, 0–6), each `{title, text}`; `behind` `{unreached: [{source, text}],
questions: [text]}`; optional `corrected` `{date, text}`. Proposals are not written by
the run here: the build takes them from the ledger for that week. Exact field names and
lengths are the builder's call within this outline.

### What stops a bad note, and what does not

**A note can never stop a week from publishing** (constraint from the 12 October handoff,
and the project's standing failure is a stale site). So:

- The build publishes a note **only if it passes every check below**. Otherwise the week
  publishes without a note. The site then shows no link, and the gate prints a `WARN`
  naming the failed check, which the weekly report repeats like every warning.
- The checks:
  - it conforms to the schema;
  - every `event_ids` entry exists in that week's data, and a pick's listings share
    one venue;
  - **the public-safety check:** no text field contains a file or folder name, a file
    extension, a command, backticks, a gate keyword (`WARN`, `SKIP`, `BLOCK` and the
    like), a script name, a long hexadecimal identifier, or the run's own vocabulary
    (`sources.yml` and the like). The exact pattern list is the builder's, and it must
    not reject ordinary prose or a venue's own web address in the "missing" advice;
  - no field is empty where the page would show an empty heading.
- **The checks are proven able to fail:** they carry a replay of planted bad notes (one
  per check) and good notes, with recorded answers, run by `verify.sh` like `drift.py`'s
  self-test. A replay that stops catching a planted case is a failure (exit 1), not a
  warning.
- `verify.sh` also renders the note page headless, the way it renders the front page,
  and fails if the newest published note does not render its picks.

### The page

- **`docs/note.html`**, one file in the front page's style: the same colour tokens, the
  same type, light only, no `prefers-color-scheme` block, and no Bay Area geography in
  the page (CLAUDE.md). It reads `?week=YYYY-MM-DD` and fetches that week's JSON. With
  no `week` it shows the newest. A week with no note shows a short line pointing to the
  current listings.
- "Earlier notes" lists every week in `docs/notes/index.json`, newest first.
- A proposal's link goes to its pull request: GitHub's search for its branch, which works
  before and after it is decided.
- The fetch of a note's JSON uses the same cache-busting the front page uses for
  `events.json`.
- Phone layout is checked in a fixed-width frame, not with headless window size
  (CLAUDE.md, Testing).
- `index.html` changes are limited to the link line, its show-or-hide, and "Earlier
  notes" in the colophon.

### The run's instructions

- `prompts/weekly-research.md` gains a section **4. `notes/{window_start}.json`**. It
  covers what each part is for and who reads it; the voice (the brief's); the
  never-in-public list; that picks are the "two or three things most worth doing" the
  report already names, so the note and the report agree; and that numbers are never
  written, because the build supplies them. This file is read from the repository on
  every run, so it needs no paste.
- `prompts/weekly-run.md` step 7 adds `notes/<window_start>.json` **and the whole
  `docs/notes/` folder** to the files committed. The build rewrites every published
  note each week, and a link switched on with no note behind it is a broken page. Its report gains one line: whether the note published, and if not, the
  `WARN` that said why. This touches the same file as the proposals spec. Build that
  spec first, and fold this change into the same routine prompt update.

## Files

Touched or created, which is the scope of both audits:

- `docs/note.html` (new)
- `docs/index.html`
- `scripts/build.py`
- `scripts/note.py` (new, holding the checks and their replay; name is the builder's call)
- `scripts/verify.sh`
- `schema/note.schema.json` (new)
- `prompts/weekly-research.md`, `prompts/weekly-run.md`
- `.github/workflows/validate.yml`: add `notes/**` and `proposals/**` to the push
  filter, run the replay, and extend the "is current" check from `docs/events.json` to
  `docs/notes/`. The same extension applies to that check inside `verify.sh`.

## Order with the proposals spec

[`proposals-as-pull-requests.md`](proposals-as-pull-requests.md) (probe) is built first.
It creates `proposals/ledger.json`, which this note reads. If the ledger is missing or
empty, the "Changes proposed" part is simply left out.

## Calls made by the session (not decided by the owner)

- The page renders JSON in the browser, like the front page, rather than the build
  writing one HTML file per week. This keeps one page and a JSON file per week, which
  is the project's architecture.
- The mockup's proposal labels showed "waiting for review". The states shown come from
  the ledger, and they update each week because every build republishes every note.
- `pulse.verdict` has three values (busy, typical, quiet). The mockup showed only the
  text.
- A failed note is a warning and the week publishes without it, rather than the week
  being held back.

## Out of scope

- The mark on uncertain listings (its own `BACKLOG.md` row).
- Emailing or posting the note anywhere.
- Rewriting past weeks' reports into notes. The first note is the first week after this
  merges.

## Done when

1. `bash scripts/verify.sh` exits 0, with the note checks' replay shown able to fail: one
   planted case per check is caught, printing the number of cases replayed.
2. A note built from the 12 October report (hand-written by the build session as a
   **test fixture kept outside `notes/`**, so it never publishes), viewed locally at
   computer and phone width, has the mockup's parts, order and look. The mockup's facts
   line and pick details come from the data, so wording may differ.
3. A note that fails the public-safety check produces a published week with no link and
   a `WARN`, shown by rehearsal on a scratch copy.
4. The post-implementation code-safety audit has no open Critical or High findings.
5. **The owner's behavioural check**, as a click-by-click HTML page: open the site, find
   the link, read the note on a phone, open "Earlier notes", follow a proposal link.
6. After the first unattended run with a note: it published, it matches what the report
   said, and nothing on the never-in-public list appears. Record it below.

## Evidence

*(filled in as the build runs)*
