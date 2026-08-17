# Handoff — unattended weekly publish (spec 0.6)

State at 2026-08-16, 16:20 UTC. Branch `spec/weekly-autopublish`, worktree
`../bay-week-autopublish`. **Unmerged**, except the sources expansion, which
was merged to `main` and pushed (`dcd84e1`).

**Research egress is fixed. The site has still never been published to by a
routine, and the push to `main` has still never been attempted.** Sections are
newest-first; each was accurate when written, and where they disagree the
higher one wins.

## Current state — 2026-08-16 evening, read this first

A second routine now exists, provisioned per `handoff/cloud-provisioning.md`,
and **three of that guide's assumptions turned out to be false.** The push to
`main` is still the one open question.

### The routine

**`trig_01U3f8NYCvzd7WEbYSNEbvNK` — "CultureVulture 2"**, created via
`RemoteTrigger`, **disabled**, and it must stay disabled until the probe below
passes. <https://claude.ai/code/routines/trig_01U3f8NYCvzd7WEbYSNEbvNK>

| Field | Value |
|---|---|
| Cron | `0 3 * * 1` UTC — the form renders it **"Runs every Sunday at 8:00 PM PDT"** |
| `PUSH_TARGET` | **`main`** — production, no review gate |
| Prompt | the `RUNBOOK-weekly.md` block verbatim, only that one line differing from the file |
| Environment | `bay-area-weekly` = **`env_0121fxAwdYCNbLp5CWDLB5uW`**, Network access **Full** |
| Model / tools / sources | cloned from `trig_01PbVtXqFUdYDFam4JGQEWUY` |

The owner chose `main` over the rehearsal target knowing the guide's two gates
are unmet. The original routine is untouched.

Cron is fixed UTC, so in PST this fires Sunday 19:00 local. The window is
unaffected either way — 03:00 UTC Monday is already Monday, which is what
`date -u` returns and what the prompt anchors on.

### Three things `cloud-provisioning.md` gets wrong

**1. The "Allow unrestricted git push" toggle does not exist.** There is no
Permissions section in the current routine edit form. The tab strip is
Connectors / Behavior / Notifications; **Behavior** holds only "Auto-fix pull
requests", and the repository chip is inert when clicked. Stage 6.2.1 is
unrunnable as written. Note [#44949](https://github.com/anthropics/claude-code/issues/44949)
reports a scheduled task pushing to `main` with no toggle at all, so its
absence is not by itself a blocker — untested, not disproven.

**2. Saving through the UI injects an output branch.** After the owner's save,
`job_config.ccr.session_context` carries a field the API-created routine did
not have:

    outcomes: [{git_repository: {git_info: {repo: "alexistosteson/culture-vulture",
                                           branches: ["claude/fervent-clarke"]}}}]

Unverified whether it binds. **If it does, the run lands on
`claude/fervent-clarke` regardless of `PUSH_TARGET: main` and the site never
updates — green everywhere, nothing published.** Plausibly this form models
"which branch the work lands on" as the replacement for the missing toggle. It
can be stripped with `RemoteTrigger update`, but a later UI save would re-add
it. Settle it against the probe's result before trusting a real run.

**3. An ad-hoc cloud session now does reproduce the environment.** The guide
says it does not, and that is stale — the composer at `claude.ai/code` has an
environment picker (cloud chip → **Cloud**), so a hand-driven session runs in
`bay-area-weekly` on the same credential path. This is why the probe below
needs no routine.

### Two smaller findings

**Environment ids are not surfaced anywhere in the UI**, and nothing in the
console needs them — environments are selected by name. `RemoteTrigger get` on
a routine pointed at one is how to read an id, which is what established
`env_0121fxAwdYCNbLp5CWDLB5uW`.

**The permission classifier refuses to create a routine whose prompt pushes to
`main`.** It permitted the weekly routine and blocked a minimal push probe. Any
future Stage-6.2-shaped experiment is a human action in the console, not a
`RemoteTrigger create`.

### Next — the owner's action, and nothing else should happen first

At <https://claude.ai/code>, select environment **`bay-area-weekly`**, attach
`alexistosteson/culture-vulture`, and run this as an ordinary session:

    Stay on the main branch; do not create or check out any branch.
    Append one line to digests/push-probe.log recording today's date and the
    value of CLAUDE_CODE_REMOTE_SESSION_ID. Commit only that file.
    Then run: git push origin main
    Report the exact output of the push command, success or failure, verbatim.
    Also report the output of `git rev-parse HEAD`.
    Do nothing else. Do not use --force. Do not delete anything.

Nothing under `docs/` changes, so the published page is byte-identical either
way. **Push succeeds** → resolve finding 2, then enable
`trig_01U3f8NYCvzd7WEbYSNEbvNK` and Sunday publishes for real. **Push 403s** →
the missing toggle is the blocker, findings 2 and 3 are moot, and Reference F.0
is the next move.

### Still owed, beyond the probe

- **Merge `spec/weekly-autopublish`.** `RUNBOOK-weekly.md` is still only on
  this branch, so the routine's prompt has no canonical copy on `main` and the
  two can drift unnoticed. This is the second handoff to say so.
- Everything in the older list below that the probe does not settle.

---

## Current state — 2026-08-16 afternoon

| Capability | State | Evidence |
|---|---|---|
| Push a new branch | Works | `c9c4345` on `routine-test/2026-08-17` |
| Push to an existing branch | Works | `cse_01QX2tqNBqDscFMrpvgLryB6` |
| **Push to `main`** | **Never attempted** | — |
| Delete a branch | Blocked, 403, no documented fix | two runs |
| Venue fetches, apex host | **Works** | `cse_01QgrvpBt1hgaK2xo5LbQFBH` |
| Venue fetches, `www.` subdomain | **Blocked** | same run |

### What changed today

**The allowlist was never saved.** Every hypothesis in the older section below
— wrong environment, cache needing a rebuild — was wrong. Environment `First`
(`env_012gzvmeBx7V662M3KyXRCCo`) was simply still on **Trusted**; a screenshot
of its dialog settled it in one look. It is now on **Custom** with the 41 apex
hosts.

**Apex entries do not cover subdomains.** With `theindependentsf.com`
allowlisted, the apex returns `301` to `www.theindependentsf.com`, which is then
refused with `CONNECT tunnel failed, response 403`. Most venues redirect this
way, so roughly twenty tier-1 sources are still unreachable. **Wildcards are
supported** — a leading `*.` matches every subdomain — so the fix is
`example.com` plus `*.example.com` per host, or simply setting Network access to
**Full**, which is what `handoff/cloud-provisioning.md` recommends and what this
project should probably do: there is no API for environments, so every allowlist
edit is a manual console edit forever.

**The environment editor has no page and no URL.** It is the cloud icon in the
row above the message box at claude.ai/code, and the same control below the
**Instructions** box in the routine *edit* form — not the routine detail page.
That cost this session and the two before it real time.

### The first properly-sourced week exists

Run `cse_01QgrvpBt1hgaK2xo5LbQFBH` (14:31Z, manual **Run now**) produced
`c9c4345` on `routine-test/2026-08-17`: **138 events**, validator clean on the
first pass, 0 errors, 0 warnings, schema errors 0. Confidence 65 high / 64
medium / 9 low, against 44 events and 6 low / 15 medium on the blocked run.
Regions: sf 88, east-bay 22, south-bay 20, peninsula 8, **outer 0** — the run
cloned `main` before the sources merge landed, so it had no `outer` venues.

**That branch contains a rebuilt `docs/events.json`. Merging it publishes the
week.** Reviewing it is the gate; merging it is the act.

### Repo changes

- **`dcd84e1` on `main`** (merged, pushed) — `config/sources.yml` gains an
  `outer` tier-1 group (Catalyst, Felton, Sweetwater), Roxie, and five East Bay
  venues, plus six editorial outlets in tier 2. `brief.yml` has always had an
  `outer` region that this file never covered.
- **`beb85fb` on this branch** — `RUNBOOK-weekly.md` now states that its prompt
  block is production (`PUSH_TARGET: main` publishes live), names the two
  conditions gating the first production paste, and fixes the direction of
  permitted drift: the installed routine may be more conservative than the file,
  never less.
- **`handoff/cloud-provisioning.md`** (this commit) — the from-scratch guide.

### The routine

`trig_01PbVtXqFUdYDFam4JGQEWUY`, weekly prompt restored, `PUSH_TARGET:
routine-test/2026-08-17`, cron unchanged, next fire Mon 2026-08-17 13:07Z.

**A trap worth not repeating: the previous handoff claimed the weekly prompt had
been restored, and it had not.** The routine was still holding a diagnostic
prompt that would have burned Monday's fire on a network test. Verify the
installed prompt with `RemoteTrigger get` rather than trusting a note that says
it was put back.

### What is actually owed now

1. **Decide Full vs Custom+wildcards** on `First`, and set it.
2. **Prove the push to `main`.** It has never been tried. The routine form has
   an undocumented **Allow unrestricted git push** toggle with an open bug
   (#58141) reporting 403 even when enabled. This is the one unknown standing
   between here and unattended publishing — see `handoff/cloud-provisioning.md`,
   which specifies an isolated probe for exactly this, and is honest that the
   two-routine fallback does not rescue it, since the merge routine needs the
   same permission.
3. **Merge `spec/weekly-autopublish`** so `RUNBOOK-weekly.md` exists on `main`.
   A guide that says "paste the block from the runbook" is useless while the
   runbook is only on a branch.
4. Read the digest for 17–23 Aug and decide whether to publish that week.
5. Decide how `routine-test/*` branches get cleaned up. Deletion is unavailable
   to routines and no setting changes it, so this is manual, forever.
6. Phase 2 proper: break it on purpose, confirm it publishes nothing.

### Accepted risk, unchanged

Auto-publish with no review gate. `validate.py` checks schema, vocabulary and
window — never facts. A wrong date or an invented lineup can go live before
anyone reads it. That trade was made deliberately.

---

# Superseded — the earlier record

Everything below was written this morning. Where it disagrees with the above,
the above wins. Its conclusions about the allowlist not taking effect were
resolved: the setting had never been saved.

## Earlier state — 2026-08-16 morning


| Capability | State | Evidence |
|---|---|---|
| Push a new branch | **Works** | `cse_01LjwLXgq9M2syg7FKctpCXU` |
| Push to an existing branch (= `main`) | **Works** | `cse_01QX2tqNBqDscFMrpvgLryB6`, `4a524da..84bc057` |
| Delete a branch | **Blocked**, HTTP 403 | same two runs |
| Force-push | Untested; assume blocked | — |
| Direct venue fetches | **Still blocked, 0/41** | `cse_01QX2tqNBqDscFMrpvgLryB6` |
| WebSearch | Works | every run |

**The only thing standing between here and publishing to `main` is the research
egress.** Every git capability the weekly job needs has been demonstrated.

Routine and remote are both back to normal: weekly prompt restored, cron
`0 13 * * 1` unchanged, next fire Mon 2026-08-17 13:07Z, `PUSH_TARGET` still
`routine-test/2026-08-17`. `git ls-remote --heads origin` shows only `main` at
`d5dfbb1` — every probe branch was cleaned up.

**Monday, as configured, will push to `routine-test/2026-08-17` and the site
will not change.** That is a safe end-to-end rehearsal. Flipping `PUSH_TARGET`
to `main` is now technically unblocked but should wait until the research is
trustworthy — see the gate below.

### The fix that worked

The owner added `culture-vulture` to the Claude GitHub App's repository
permissions with **read/write**. That was the whole fix; nothing in the repo,
the prompt, the branch names or the network config needed to change.

### Two traps, both of which cost time here

**1. The API `permissions` object is worthless as a check.** It reports

    { "admin": false, "maintain": false, "push": false, "triage": false, "pull": false }

*even when pushes work.* `GH_TOKEN` in the environment is the 14-character
literal string `proxy-injected`, so any `curl -H "Authorization: Bearer
$GH_TOKEN"` is an anonymous request against a public repo. The real credential
exists only inside the egress proxy, on git's path. **The only valid test of
write access is an actual `git push`.** This check reported failure moments
before a push succeeded, and would have talked us out of a fix that had already
landed.

**2. `git branch --show-current` returns empty.** Sessions are provisioned
**detached at `refs/heads/main`**, so the natural
`git push origin HEAD:$(git branch --show-current)` dies locally on
`fatal: invalid refspec 'HEAD:'` without ever touching the network — a false
negative that looks like nothing happened. Name the branch explicitly.

### Deletes are blocked — a standing consequence

`git push origin --delete <branch>` returns:

    error: RPC failed; HTTP 403
    send-pack: unexpected disconnect while reading sideband packet

The environment permits creating and updating refs but refuses to delete them.
This does not affect the weekly job, which only creates and updates. It does
mean **the routine cannot clean up after itself**, so any `routine-test/*`
branches accumulate until removed by hand from a credentialed local checkout.
Worth an explicit decision rather than discovering a pile of them later.

## The one open problem — research egress

**Setting the allowlist did not work.** On 2026-08-16 the owner set the
environment's Network access to Custom with the 41 venue hosts. A run
immediately afterwards (`cse_01QX2tqNBqDscFMrpvgLryB6`) found **all 41 still
blocked**, every one identically:

    curl: (56) CONNECT tunnel failed, response 403   → HTTP 000

Not one request reached an origin — no DNS, no TLS handshake. `WebFetch` fails
the same way with `{"error_type":"EGRESS_BLOCKED"}`, which matters because the
research prompt uses WebFetch, not curl. Controls confirm the proxy is on its
**old** policy rather than a broken new one: `pypi.org` → 200 (it is on
`no_proxy`), `example.com` → blocked.

**Unresolved, and where the next session should start.** Any of these fits:

- the setting was applied to a different environment — the routine is pinned to
  **`env_012gzvmeBx7V662M3KyXRCCo`**, and that is the one that must change;
- it did not persist;
- it only takes effect on newly-built environments, so the environment needs a
  rebuild before a run picks it up.

Confirm which before re-testing; a second identical attempt tells you nothing
new.

**The exact host list**, regenerated from `config/sources.yml` (41 hosts). Note
`sf.funcheap.com` — an earlier draft of this file said `*.funcheap.com`, which
is not what the config contains:

    augusthallsf.com          gamh.com                  ritzsanjose.com
    bandsintown.com           guildtheatre.com          sanjose.events
    bimbos365club.com         hammertheatre.com         sanjosetheaters.org
    bottomofthehill.com       ivyroom.com               sapcenter.com
    brickandmortarmusic.com   jambase.com               sf.funcheap.com
    cafedunord.com            livenation.com            sfjazz.org
    castrotheatre.com         mountainwinery.com        sfstation.com
    dnalounge.com             museumca.org              songkick.com
    dothebay.com              paramountoakland.org      sterngrove.org
    downtownsf.org            publicsf.com              thechapelsf.com
    filoli.org                redwoodcity.org           theestorkclubopakland.com
                              rickshawstop.com          thefoxoakland.com
                                                        thegreekberkeley.com
                                                        theindependentsf.com
                                                        thenewparkway.com
                                                        thewarfieldtheatre.com
                                                        visitoakland.com
                                                        yoshis.com

Keep "also include default list of common package managers" checked —
`validate.py` needs PyPI. Regenerate the list rather than trusting this copy if
`sources.yml` has changed:

    python3 - <<'PY'
    import re
    raw = open('config/sources.yml').read()
    hosts = {m.group(1).lower().removeprefix('www.')
             for m in re.finditer(r'https?://([^/\s"\')]+)', raw)}
    print('\n'.join(sorted(hosts)), len(hosts), sep='\n---- count: ')
    PY

**Setting it is not proof.** A run that actually fetches a tier-1 calendar is
the proof, and it must test WebFetch as well as curl.

## The gate before `PUSH_TARGET` becomes `main`

Fixing egress makes the research *sourced*, not *verified*. `validate.py`
checks schema, vocabulary and window — never facts. So "accurate and complete"
cannot be established by any automated gate in this project. Suggested order:

1. Fix the allowlist on `env_012gzvmeBx7V662M3KyXRCCo`; prove a tier-1 fetch
   works via both curl and WebFetch.
2. Run the weekly publish to `routine-test/<window>` and read the digest
   yourself.
3. Only then flip `PUSH_TARGET` to `main` — in `RUNBOOK-weekly.md` first, which
   is canonical, then paste into the routine.

## How to run a diagnostic against the real routine

Getting the environment right is the whole difficulty; an ad-hoc cloud session
does not reproduce it. Swap **only the prompt** on
`trig_01PbVtXqFUdYDFam4JGQEWUY` via the remote-trigger API (`update`), keeping
`environment_id`, `session_context.model`, `allowed_tools`, `sources` and
`mcp_connections` byte-identical — send the whole `job_config` back rather than
a partial, and save the weekly prompt first so it can be restored. Read results
with `list_runs` then `get_run_log`.

Four practical notes:

- Firing programmatically is **blocked by the permission classifier**; a human
  clicks **Run now** in the console.
- `persist_session: false` — the container is destroyed at the end, so the
  run's final message is the only record. Demand everything verbatim in it.
- **Restore the weekly prompt immediately.** A diagnostic left installed is what
  the next cron fires.
- Have the run leave probe branches in place and delete them yourself locally;
  the run cannot.

## Diagnostic record

Everything below is how the above was established. It is history, not
instructions.

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

- ~~Grant the routine write access.~~ **Done 2026-08-16** — App granted
  read/write on the repo; pushes verified working.
- **Fix the research egress on `env_012gzvmeBx7V662M3KyXRCCo`.** The only
  remaining blocker. See the open-problem section above.
- Run the weekly publish to a test branch and read the digest, before any flip
  to `main`.
- Phase 2 proper: break it on purpose, confirm it publishes nothing.
- Flip `PUSH_TARGET` to `main` in `RUNBOOK-weekly.md` (canonical), then paste
  into the routine. Technically unblocked; gated on the two items above.
- Decide how `routine-test/*` branches get cleaned up, since the routine cannot
  delete them.
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
