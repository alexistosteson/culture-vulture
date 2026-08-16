# Handoff — unattended weekly publish (spec 0.6)

State at 2026-08-16. Branch `spec/weekly-autopublish`, worktree
`../bay-week-autopublish`, commits `cf14996` (spec) + `865b7ed` (runbook +
backlog row). **Unmerged, local only.**

**The A/B question is settled — the answer is A, no write scope.** See the
settled section below; the open-question section that follows it is kept only
as the record of how it was framed.

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

Reads work (`git ls-remote` succeeded — since re-confirmed, see below). The
container is ephemeral, so `fd716ba` **is gone**; the run attached the two files
to its own cloud session, which is the only surviving copy.

**The second line above is not evidence and has been withdrawn.** That routine
has no GitHub MCP configured — its `allowed_tools` is
`Bash, Read, Write, Edit, Glob, Grep, WebSearch, WebFetch` and its only
`mcp_connections` entry is `Claude_Code_Remote`. `403 Resource not accessible by
integration` there is what an unavailable tool path returns, not a statement
about repo scope. Only the `git push` 403 ever carried information.

The failure invariant held: nothing published, `main` untouched, last week
still live, and it reported why. That is phase-2 evidence for free — for a
different failure cause than the one phase 2 was meant to exercise, but the
same invariant.

## SETTLED 2026-08-16 — the answer is A

**The session has no write scope. B is eliminated. Nothing publishes until
write access is granted; no amount of network or branch configuration fixes
it.**

Two runs settled it, both fired from the real routine with only the prompt
swapped — same `environment_id` (`env_012gzvmeBx7V662M3KyXRCCo`), same model,
same `sources`, same credential path — so nothing about the environment was a
variable. The weekly prompt was restored after each.

**Run `cse_01QYJXw9guEqLD6obSSAQwTr` — the discriminator.** The session was
provisioned **detached at `refs/heads/main`**, so it created no branch at all.
It appended one line to `BACKLOG.md`, committed locally (`482a52f`, exit 0), and
pushed straight to `main`:

    BR=main; git push origin HEAD:$BR
    fatal: unable to access 'https://github.com/alexistosteson/culture-vulture/': The requested URL returned error: 403
    exit=128

A push to the provisioned branch itself, with no branch creation anywhere in
the run, still 403s. **Push protection cannot explain that**, so B is dead and
the test branch was never the cause. Test 2 (branch creation) was skipped by
design once test 1 failed; nothing reached the remote, so cleanup was a no-op.
`git ls-remote` from a credentialed local checkout confirms `origin` still holds
exactly one head, `main` at `d5dfbb1`.

Note for anyone re-running this: `git branch --show-current` returns **empty**
in these sessions because HEAD is detached, so the natural
`git push origin HEAD:$(git branch --show-current)` dies locally on an invalid
refspec without ever touching the network — a false negative that looks like
nothing happened. Name the branch explicitly.

**Run `cse_011kr21c1XeQxM16aRyFc7zU` — read-only, to rule out the proxy.** The
first run's 403 had the same numeric shape as the egress proxy's
`CONNECT tunnel failed, response 403`, which raised a third possibility: that
pushes never reach GitHub at all. They do. Reads succeed through the same proxy:

    git ls-remote origin        → all refs, exit=0
    git fetch origin --dry-run  → tags fetched, exit=0
    curl https://api.github.com → 200
    curl https://example.com    → CONNECT tunnel failed, response 403
    curl https://pypi.org       → 200

`GIT_CURL_VERBOSE=1` shows the connection going to `127.0.0.1:34601` and the
`CONNECT tunnel: HTTP/1.1 negotiated` succeeding for github.com — while
`example.com` is refused at that same tunnel. So the proxy explicitly permits
GitHub and blocks everything not allowlisted. The environment also injects
`GH_TOKEN=proxy-injected`.

**Therefore the token the proxy injects is read-scoped.** The tunnel is open,
GitHub answers, and GitHub is what returns 403 on write. The fix is a
credential-scope change, not a network change — and specifically *not* the
Network access edit in the next section, which fixes a different problem and
will not make pushes work.

Still unverified, and worth verifying before asserting: whether `/web-setup`
from the terminal or authorizing the Claude GitHub App with write on this repo
actually changes what the *routine* gets, since the token is proxy-injected
rather than taken from a user session. Local `gh` cannot settle it — its token
isn't App-authorized, so `user/installations` returns 403 and
`repos/.../installation` returns 401.

## The original open question, kept for the record

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

**Outcome: the push 403'd. A.** See the settled section above.

## Second finding, independent of the above

**All outbound HTTP is blocked in the environment.** Every tier-1 venue, every
aggregator, even `example.com` → `EGRESS_BLOCKED` / curl `000`. Only WebSearch
reaches out. The `First` environment is on **Trusted** (package registries,
GitHub, cloud SDKs — matching the proxy's `noProxy` dump).

Re-confirmed 2026-08-16 in `cse_011kr21c1XeQxM16aRyFc7zU`:
`thechapelsf.com`, `dothebay.com` and `example.com` all return
`curl: (56) CONNECT tunnel failed, response 403`, while `pypi.org` and
`api.github.com` return 200. The full `no_proxy` value is worth knowing, since
hosts on it bypass the proxy entirely rather than being allowlisted through it:

    localhost,127.0.0.1,::1,127.0.0.0/8,0.0.0.0/8,::,169.254.0.0/16,
    anthropic.com,.anthropic.com,*.anthropic.com,registry.npmjs.org,jsr.io,
    npm.jsr.io,pypi.org,files.pythonhosted.org,index.crates.io,
    proxy.golang.org,host.docker.internal,10.0.0.0/8,172.16.0.0/12,
    192.168.0.0/16,100.64.0.0/10,.svc.cluster.local,*.svc.cluster.local

github.com is **not** in that list yet reads succeed, so GitHub is permitted
*through* the proxy rather than bypassing it — which is why the proxy is in a
position to inject `GH_TOKEN` on the way past.

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

- **Grant the routine write access to the repo — this blocks everything else.**
  Then re-run phase 1. Until it lands, the routine can research, validate and
  build, and will always fail at the last step.
- Phase 2 proper: break it on purpose, confirm it publishes nothing.
- Flip `PUSH_TARGET` to `main` in both the routine and `RUNBOOK-weekly.md`
  (the runbook is canonical — edit there, paste into the routine). Now known to
  be safe on its own terms — the branch was never what broke the push — but it
  changes nothing until write access exists.
- Merge `spec/weekly-autopublish` once the design is confirmed to work.

## How to run a diagnostic against the real routine

Worth writing down, because getting the environment right is the whole
difficulty and an ad-hoc cloud session does not reproduce it.

Swap only the prompt on `trig_01PbVtXqFUdYDFam4JGQEWUY` via the remote-trigger
API (`update`), keeping `environment_id`, `session_context.model`,
`allowed_tools`, `sources` and `mcp_connections` byte-identical — send the whole
`job_config` back rather than a partial, and save the weekly prompt first so it
can be restored. Read results with `list_runs` then `get_run_log`; the container
is destroyed at the end, so the run's final message is the only record and the
prompt must demand everything verbatim in it.

Two practical notes. Firing the routine programmatically is blocked by the
permission classifier, so a human clicks **Run now** in the console. And the
weekly prompt must be restored immediately — a diagnostic left installed will be
what Monday's cron fires.

## Accepted risk, unchanged

Auto-publish with no review gate. `validate.py` checks schema, vocabulary and
window — not facts. Recorded in the spec and the backlog row so it is not
rediscovered as a surprise.
