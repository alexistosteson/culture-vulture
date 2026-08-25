---
state: active
next: Nothing blocking. To publish a week: run the research prompt in `prompts/weekly-research.md` against `config/brief.yml`, save the result as `data/<monday>.json`, then in this repo run `python3 scripts/validate.py && python3 scripts/build.py` and commit — see [CLAUDE.md](CLAUDE.md) for the pipeline. Specs go in a root-level `specs/`, never `docs/` (the Pages web root); each declares its own tier per `delivery-tiers`.
tool: claude-code
updated: 2026-08-23
---

# Backlog — culture-vulture

## Utility now
<!-- utility-updated: 2026-08-22 -->
- serves the live weekly digest at https://alexistosteson.github.io/culture-vulture/ from `docs/index.html` + `docs/events.json` — the v0.5 Almanac front end (`97028e6`)
- `python3 scripts/build.py` projects `config/brief.yml` over the newest `data/<monday>.json` into `docs/events.json`, so repointing the site at another city is a config edit plus a rebuild
- `python3 scripts/validate.py` checks the week against `schema/events.schema.json`, the closed vocabularies and the date window; `.github/workflows/validate.yml` runs it on every push and fails the build when `docs/events.json` is stale
- `python3 ~/.claude/bin/tool-floor.py` enforces the `ruff.toml` floor (`F/ARG/B/RUF`) over `scripts/`, exit 0 (`d3c86da`)
- a cloud research run in the `bay-area-weekly` environment produces a full validated week and pushes it to a branch — session `cse_01QgrvpBt1hgaK2xo5LbQFBH` committed `c9c4345` "Week of 2026-08-17: 138 events", 0 errors, 0 warnings

Weekly Bay Area arts digest. One HTML file, one JSON file, no framework or
backend. Live at https://alexistosteson.github.io/culture-vulture/ · released
`v0.5.0` 2026-08-15 (the Almanac redesign; `v0.1.0` same day).

**Deliberately light on process, not unfinished.** It arrived as a downloaded
tarball with its own git history rather than through `new-swe-project`, so it
has no CONSTITUTION and no ritual docs — and per `delivery-tiers` it does not
owe them, because tier is declared per spec and most work here is `probe`. The
one gate that never relaxes, the tooling floor, is established (`ruff.toml`,
2026-08-15). This file plus [CLAUDE.md](CLAUDE.md) are the whole process
surface.

## Index

- small · Design port package is two designs stale — now snapshots a front end that no longer exists
- small · Full build-tier scaffold, only if a spec ever needs it — parked, see the row below for why it is not owed now
- done 2026-08-15 · `docs/events.json` caches aggressively — fixed in v0.5
- one-liner · Two rough edges in the v0.5 `¶` overlay — both seen in the shipped page
- **active** · The weekly run is automated and publishes unreviewed — the owner's two-phase check is outstanding

---

| Item | Context | Do it when |
|---|---|---|
| The weekly run is automated — and publishes unreviewed [blocker/s3/v2] → unblocks flipping `PUSH_TARGET` to `main` and the first unattended publish | **Spec 0.6, probe tier, 2026-08-16.** A Claude cloud routine (`trig_01PbVtXqFUdYDFam4JGQEWUY`, Opus 5, Mon 06:00 PT) runs `prompts/weekly-research.md`, validates, builds and pushes. Operating detail is in [RUNBOOK-weekly.md](RUNBOOK-weekly.md); the routine prompt is canonical there, so edit it there and paste, or the two drift.<br><br>**The accepted risk, recorded so it is not rediscovered later:** publication is unattended and `validate.py` checks schema, vocabulary and window, *not facts*. A hallucinated venue or a wrong date reaches the public site before anyone reads it. The alternative — push a branch, open a PR, merge by hand — was considered and rejected in favour of speed. On validator failure the routine commits nothing and last week stays up; that invariant, not the validator, is what keeps a broken week off the site.<br><br>**Two legs are untested by construction** and stay that way: the Pages deploy and the cold load of the live page, both exercised by every hand-published week. | **Now, and it is the owner's to do — nobody else can.** Phase 1: watch the first branch run end to end. Phase 2: break it on purpose and confirm it publishes nothing. Then flip `PUSH_TARGET` to `main` in both the routine and the runbook. Until phase 2 has been seen, the invariant protecting the site is untested. |
| Automated fact-check pass before an unattended publish [feature/s3] | **Owner-raised 2026-08-23**, while valuing the row above. `validate.py` checks schema, vocabulary and window — never facts — so the safety gap on an unattended publish is factual, not structural, and no amount of schema validation closes it. **Shape the owner described:** a separate subagent runs a fact-check pass before publish; verified facts go into the doc, unverified ones are removed, so a fully correct document reaches the public page — and a *what was found* flag goes up for the owner to review afterwards, to judge whether the brief itself needs changing. That last half is the point: the flag is how a recurring class of hallucination gets caught at the brief, not one venue at a time. Owner sized it "S or M?" — M pending a look at what a fact-check actually has to reach (venue existence, dates, ticket links) and whether any of it is offline-checkable. | Before `PUSH_TARGET` flips to `main` without a human reading every week. It is the cheaper half of the row above: the owner still watches one end-to-end run and breaks it on purpose, but this is what makes the steady state safe. |
| **Write the `specs/`-not-`docs/` layout constraint into `CLAUDE.md`.** Pages serves this repo from `main` + `/docs`, so anything written to `docs/HANDOFF.md`, `docs/handoff/` or `docs/superpowers/{specs,plans}` is publicly served — short-form probe specs therefore go in a root-level `specs/`. Also record that the template must not be copied piecemeal (its `CLAUDE.md` links a tree that would not exist). Then strike the parked-scaffold row. [feature/s2/v3] | Amended 2026-08-23 (Step 4, owner accepted the proposed rewrite). It replaced the parked *Full build-tier scaffold* record-row: the scaffold itself is genuinely not owed until a spec here is declared **build** tier, but the layout constraint inside it is live and was written nowhere a future session would read. The superseded analysis — the three scaffold options, the `docs/_config.yml` and `gh-pages` alternatives, and the project-scope probe declaration that does not apply — survives in this file's git history. | Now. The constraint is live; the scaffold it came from is still not owed. |
| ~~Design port package is two designs stale [bug/S]~~ | `handoff/claude-design/` snapshots the site **before** the Culture Vulture rename, before the outdoor-chip fix, and now before the whole v0.5 Almanac redesign (`97028e6`) — its `source/index.html` is a front end the project no longer has, its README cites commit `a1e7b0f`, and all five screenshots show the old masthead, the old Barlow/Inter type and the viridis ramp. **Regenerating it is no longer a re-screenshot — the package's own brief is superseded**, and the design it was built to hand off has been replaced by the Almanac handoff in `Website design exploration.zip`. A chip was spawned 2026-08-15 against the smaller version of this problem. The capture method still holds: `--window-size` alone silently produces desktop-layout images at mobile pixel widths; load the page in a fixed-width `<iframe>` and screenshot the wrapper. | Before handing the package to anyone. Decide first whether it is a port package at all now, or just archived. |
| ~~`docs/events.json` caches aggressively~~ | **Done 2026-08-15 in v0.5 (`97028e6`).** The page fetches `events.json?v=<timestamp>`, so a warm browser can no longer serve the previous build's data — the failure that twice looked like "the build didn't work" during development. `index.html` itself is still subject to the Pages CDN, so a hard reload is still the move after a deploy. | Closed. Delete this row at the next backlog tidy. |
| Two rough edges in the v0.5 `¶` overlay [bug/s1/v1] | Both observed in the shipped page 2026-08-15, neither serious enough to hold the release. **(a)** Adjacent selected region rows merge into one tinted block — the `#F1E8D6` wash swallows the `#EBE3D3` hairline between them, so two regions on read as one item. A darker `border-bottom` on `.region-row[data-on="true"]` separates them. **(b)** With the Venue block included, `CLEAR ALL` / `SHOW n` sit below the fold on a short laptop, so the primary action of the overlay is off-screen at rest. The block order is specified in the design handoff, so shortening it is a design decision, not a fix. | Next time the overlay is opened for any other reason. (a) is a two-line CSS change; (b) needs a call first. |
