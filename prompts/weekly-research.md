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
nights. Close with a sources list.

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
  - **`COULD NOT CHECK`** (exit 2) — not something to fix in the week. Stop and
    report it verbatim; the checks themselves are broken.

## Report back

After the files, summarise in chat:

- The two or three things most worth doing, and why
- Anything you couldn't verify
- Any vocabulary or region additions you'd propose to the brief
- Whether the week is unusually busy or quiet, and what that's driven by
