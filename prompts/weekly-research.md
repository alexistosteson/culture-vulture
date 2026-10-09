# Weekly research prompt

Paste this into a fresh Claude session on run day. It expects `config/brief.yml`
and `config/sources.yml` to be attached or pasted alongside it.

---

## Task

Compile this week's Bay Area arts and culture digest.

Read `config/brief.yml` first. It defines the window, the regions and their
order, what counts as interesting, what to exclude, and the voice. **Treat it as
the specification.** Where it conflicts with your own instincts about what
belongs in a listings digest, the brief wins. Where it's silent, use judgement
and say what you assumed.

Read `config/sources.yml` second. Work down the tiers: tier 1 venue calendars
give exact times and prices, tier 2 aggregators catch free and community events
that never reach a ticketing platform, tier 3 feeds give breadth but thin
detail. Prefer the highest tier that has the event. Tier 3 snippets frequently
omit the artist name — verify against tier 1 before publishing anything sourced
there.

Four keys on a `sources.yml` entry change what you do with it:

- **`fallback:`** — when the entry's `url` fails or returns nothing readable, try
  each address listed, in order, before calling the venue unreached. Each says
  what it gives. A fallback that carries only part of the programme is a floor.
- **`how:`** — the address is not read by fetching it; a plain fetch sees an
  empty page. Run the command the entry gives, from the repository root, with
  the entry's `url` and this week's window. It prints the venue's listings with
  local start times. `COULD NOT READ` means the venue is unreached — never that
  nothing is on — and belongs under "What could not be reached". The command
  handles a key that belongs to the venue: never print it, copy it, or write it
  into any file, and do not try to make the request yourself by another route.
  Check the city on each line before listing it.
- **`coverage: partial`** — the routes that work do not carry everything the
  venue puts on, and `omits:` says what is missing. List what the routes give,
  and report the omission every week (see "What could not be reached").
- **`season_ends:`** — nothing is expected from the entry after that date. Do not
  spend fetches looking, and do not report its silence as a failure.

## Window

Compute from `schedule` in the brief. Confirm today's date before you start; if
your sense of the date and the tool results disagree, trust the tools and say so.

## What to produce

**1. `data/{window_start}.json`** — the record set. Conform to
`schema/events.schema.json`. Every event needs `id`, `date`, `title`, `venue`,
`city`, `geo`, `type`, `venue_type`, `cost`. Use only the vocabularies declared
in `meta.vocab`; if something genuinely doesn't fit, propose a vocabulary
addition in your summary rather than inventing a value silently.

Notes on specific fields:

- `geo` — must match a region `id` from the brief. Assign by the city lists in
  `regions[].includes`; if a city isn't listed, pick by proximity and flag it.
- `note` — one or two sentences in the brief's voice. For music, this is the
  genre line: what it sounds like, its lineage, why this booking is or isn't
  notable. Never restate the title.
- `featured` — cap at `output.featured_max`. Reserve for genuinely exceptional
  bookings, not merely large ones.
- `confidence` — set to `low` when you're describing an act you couldn't verify,
  or a lineup that wasn't announced. Say so in the note too.

**2. `digests/{window_start}.md`** — the human digest. Group by
`output.group_by`, order within groups by `output.sort_within`. Open with a
"Week at a Glance" naming the dominant event, the busiest day, and the dead
nights. Close with three sections, in this order:

- **`## Thin this week`** — one line for each venue that has far fewer listings
  this week than in its own recent weeks. `scripts/drift.py` tells you which
  (see the verification pass); you do not have to work it out. Each line is a
  list item that **names the venue as the data file spells it, says `reached` or
  `unreached`, and says what you checked**:

  ```
  - **The Regency Ballroom** — reached; its JamBase page shows one show this
    week and nothing again until the 13th.
  - **DNA Lounge** — unreached; the October calendar page returned nothing
    readable on three attempts, and the JamBase mirror lists one concert.
  ```

  *Reached* means you read the venue's calendar, or a mirror of it, and the low
  count is what is really on. *Unreached* means you could not, and the count is
  a floor. Never write *reached* for a venue you only saw in a ticketing sweep.
  If nothing is thin, keep the heading and write "Nothing this week."
  `digests/2026-10-05.md` is a worked example.
- **`## What could not be reached`** — every source that failed, and what the
  failure cost. A venue can appear in both sections. **Every `sources.yml` entry
  marked `coverage: partial` gets a standing line here every week**, whether or
  not its count looks low, unless this week you read the venue's full calendar
  (say so instead). Name the venue, say what the route leaves out — its `omits:`
  — and stop there. Do not estimate how many listings that is; nobody knows:

  ```
  - **SFJAZZ** — partial, as every week: the mirror lists Miner Auditorium
    only. Joe Henderson Lab shows are missing unless listed above.
  - **DNA Lounge** — partial: its own calendar would not load for this run, so
    only the touring concerts on its mirrors are listed. The club nights, film
    nights and variety shows are missing.
  ```
- **`## Sources`**

**3. `docs/events.json`** — copy of the JSON the site reads. Run
`python3 scripts/build.py` to produce it.

## Editorial stance

The brief's `voice` section governs. Beyond it:

- **Rank things.** On a crowded night, say which is best and why. A digest where
  every listing reads equally weighted is a database, not an edit.
- **Flag conflicts.** When two good things overlap and the geography makes them
  incompatible, say so.
- **Surface friction.** Fog, street closures, garage closing times, lottery
  mechanics, sellout risk. See `local_knowledge` in sources.yml.
- **Mark uncertainty.** "Descriptor is lower-confidence — verify" is a better
  line than a confident guess.
- **Don't pad.** A thin week reported as thin is more useful than a thin week
  inflated with filler.

## Verification pass

Before finalising, check every part of the brief against what you retrieved:

- [ ] Every region in `regions` was actually searched, not just the dense ones
- [ ] Tier 1 venues polled directly, not inferred from aggregators
- [ ] Recurring events from `sources.yml` placed on their correct dates this window
- [ ] Nothing matching `exclusions.hard` made it in
- [ ] `outer` region entries clear `coverage.outer_threshold` — and if none do, say so
- [ ] Featured count within cap
- [ ] `python3 scripts/validate.py` passes with zero errors
- [ ] `python3 scripts/drift.py` exits 0. It compares this week with the weeks before
      it, and `scripts/verify.sh` runs it again as part of the merge gate — so run it
      here first and act on what it prints, rather than meeting it at the gate:
  - **A new spelling of an established venue** ("Fillmore" where every earlier week
    says "The Fillmore") — change the data file *and* the digest to the established
    spelling it names. Two spellings are two venues to everything that counts.
  - **A thin venue** ("Regency Ballroom: 1 listing(s) after 2, 2, 4, 5") — the venue
    has less than 40% of what it usually has. **Look again before you write
    anything**: re-read its calendar, try the route `sources.yml` gives, try its
    mirror. Add whatever you find to the data file and the digest. Then run
    `drift.py` again. If the venue is still flagged, write its line under
    `## Thin this week` as described above, and the check is satisfied. The line is
    not a formality — it is the difference between a quiet week and a missed one,
    and it is the only place a reader is told which.
  - **`COULD NOT CHECK`** (exit 2) — not something to fix in the week, with one
    exception: `no readable digest` means you ran it before writing
    `digests/{window_start}.md`. Write the digest first. Anything else, stop and
    report it verbatim; the checks themselves are broken.
  - **A `WARN` line** — does not stop the week and is not yours to fix in it. Two
    kinds name a venue: one that `sources.yml` says is watched and that has produced
    nothing in four weeks, and one that has been listed three weeks or more and is
    not in `sources.yml` at all. If you can see why — the venue's calendar would not
    load, its season has ended, it has closed — say so beside the warning. Do not
    edit `sources.yml` to make a warning go away. `scripts/verify.sh` counts the
    warnings in its summary line and lists them again beneath it.

## Report back

After the files, summarise in chat:

- The two or three things most worth doing, and why
- Anything you couldn't verify
- **Every `WARN` line the rot checks printed, word for word**, each with whatever you
  know about its cause. A warning nobody repeats is a warning nobody reads — the same
  rule the gate's SKIPPED checks follow. If there were none, say "no warnings"
- Any vocabulary or region additions you'd propose to the brief
- Whether the week is unusually busy or quiet, and what that's driven by
