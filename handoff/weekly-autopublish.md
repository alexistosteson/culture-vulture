# Handoff — unattended weekly publish (spec 0.6)

State at 2026-08-16. Branch `spec/weekly-autopublish`, worktree
`../bay-week-autopublish`, commits `cf14996` (spec) + `865b7ed` (runbook +
backlog row). **Unmerged, local only.**

## Where it stands

Routine `trig_01PbVtXqFUdYDFam4JGQEWUY` exists and works — Opus 5, cron
`0 13 * * 1` (Mon 06:00 PDT), `PUSH_TARGET: routine-test/2026-08-17`.
Console: <https://claude.ai/code/routines/trig_01PbVtXqFUdYDFam4JGQEWUY>

Phase-1 run `cse_018N8rtsvuTMxcsJYuTciRRZ` did everything right except the
push. Research → `data/2026-08-17.json` (44 events) → `validate.py` **clean on
the first pass, 0 errors 0 warnings** → schema check → `build.py` → its own
forbidden-path check → commit `fd716ba` on `routine-test/2026-08-17`. Then:

    git push -u origin routine-test/2026-08-17
    fatal: ... The requested URL returned error: 403

    mcp__github__create_branch → 403 Resource not accessible by integration

Reads work (`git ls-remote` succeeded). The container is ephemeral, so
`fd716ba` **is gone**; the run attached the two files to its own cloud session,
which is the only surviving copy.

The failure invariant held: nothing published, `main` untouched, last week
still live, and it reported why. That is phase-2 evidence for free — for a
different failure cause than the one phase 2 was meant to exercise, but the
same invariant.

## THE OPEN QUESTION — run this first

Two explanations fit the 403s, and they point opposite ways.

**A — the session has no write scope.** What the run itself concluded.
`403 Resource not accessible by integration` is the classic missing
`contents: write` on a GitHub App.

**B — push protection.** The docs say the GitHub proxy allows `git push`
**only against the session's current working branch**. The session was
provisioned on `main`, then did `git checkout -b routine-test/2026-08-17` and
pushed that. If "current working branch" means the provisioned one, the proxy
refuses — with exactly these 403s, since both write paths traverse it.
`git config` in the run showed `http.proxyauthmethod basic` and injected
credentials, consistent with the proxy being in the path.

Under A nothing publishes until access is granted. **Under B write already
works and a push to `main` would have succeeded** — meaning the test branch,
chosen to be safe, is what broke it.

**The discriminator.** Start a cloud session on this repo. Have it append one
line to `BACKLOG.md` — no branch creation, stay on the provisioned `main` — and
push. Nothing under `docs/` changes, so the published page is byte-identical
whichever way it goes.

- Push succeeds → **B**. Write works; the design is sound as specified; flip
  `PUSH_TARGET` to `main` and re-run phase 1 against `main` directly.
- Push 403s → **A**. Grant write access, then re-run. Likely `/web-setup` from
  the terminal to sync the `gh` token, or authorizing the Claude GitHub App
  with write on this repo — **neither verified for routines specifically;
  verify before asserting it.**

Local `gh` cannot settle this: its token isn't App-authorized, so
`user/installations` returns 403 and `repos/.../installation` returns 401.

## Second finding, independent of the above

**All outbound HTTP is blocked in the environment.** Every tier-1 venue, every
aggregator, even `example.com` → `EGRESS_BLOCKED` / curl `000`. Only WebSearch
reaches out. The `First` environment is on **Trusted** (package registries,
GitHub, cloud SDKs — matching the proxy's `noProxy` dump).

This breaks `prompts/weekly-research.md`'s own rule that tier-1 venues be
polled directly and tier-3 snippets verified against them. The Aug 17 week was
built from search snippets alone — the run said so plainly rather than claiming
the checklist passed, and marked 6 events `low` / 15 `medium` confidence.

**Fix:** set the environment's Network access to **Custom**, keep "also include
default list of common package managers" checked (`validate.py` needs PyPI),
and paste the 41 hosts extracted from `config/sources.yml`:

    augusthallsf.com          gamh.com                  ritzsanjose.com
    bandsintown.com           guildtheatre.com          sanjose.events
    bimbos365club.com         hammertheatre.com         sanjosetheaters.org
    bottomofthehill.com       ivyroom.com               sapcenter.com
    brickandmortarmusic.com   jambase.com               sfjazz.org
    cafedunord.com            livenation.com            sfstation.com
    castrotheatre.com         mountainwinery.com        songkick.com
    dnalounge.com             museumca.org              sterngrove.org
    dothebay.com              paramountoakland.org      thechapelsf.com
    downtownsf.org            publicsf.com              theestorkclubopakland.com
    filoli.org                redwoodcity.org           thefoxoakland.com
                              rickshawstop.com          thegreekberkeley.com
                                                        theindependentsf.com
                                                        thenewparkway.com
                                                        thewarfieldtheatre.com
                                                        visitoakland.com
                                                        yoshis.com
                                                        *.funcheap.com

Setting it is not proof it works — open bug reports exist against allowlist
enforcement (all Cowork desktop, not cloud, so probably not this path). A run
that actually fetches a tier-1 calendar is the proof.

## Still owed

- Phase 2 proper: break it on purpose, confirm it publishes nothing.
- Flip `PUSH_TARGET` to `main` in both the routine and `RUNBOOK-weekly.md`
  (the runbook is canonical — edit there, paste into the routine).
- Merge `spec/weekly-autopublish` once the design is confirmed to work.

## Accepted risk, unchanged

Auto-publish with no review gate. `validate.py` checks schema, vocabulary and
window — not facts. Recorded in the spec and the backlog row so it is not
rediscovered as a surprise.
