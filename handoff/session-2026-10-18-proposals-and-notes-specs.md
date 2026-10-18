Session name: Draft the build spec for the rot-detection checks

# Handoff: proposals as pull requests, and the public weekly note. Both specs written (18 October 2026)

Read `CLAUDE.md` first; it is binding. **`docs/` is the published web root.** The owner
is a non-technical product manager. Bring him product choices in plain words, decide the
mechanics yourself, and end on a recommendation.

## State

- Both designs were agreed with the owner in chat on 18 October, and both specs are on
  `main`:
  - [`specs/proposals-as-pull-requests.md`](../specs/proposals-as-pull-requests.md):
    **probe**. No plan, no audit.
  - [`specs/weekly-public-note.md`](../specs/weekly-public-note.md): **production**
    (owner, 18 October). It owes the pre-plan code-safety audit, a plan, the audit of
    the written code before merge, and a tier registry block.
  - The approved mockup is [`specs/mockups/weekly-note.html`](../specs/mockups/weekly-note.html).
- A builder check (a fresh reviewer reading the specs cold) ran on both, and its answers
  are folded in. None needed the owner.
- **The owner had not yet said yes to the written specs when this was written.** The
  last message asked him to read them. If he has not approved them, get his yes first.
  What he approved in chat is the design; the written specs add the calls listed under
  "Calls made by the session" in the note spec, and in the proposals spec the tag that
  records outcomes and the step order.
- The 12 October handoff (`session-2026-10-12-proposals-and-notes.md`) is superseded by
  this file. Do not re-read it.
- The owner acknowledged the 6 December calendar entry. Nothing is pending on Agent's Cal.

## Next action, in order

1. **Build the proposals spec** (probe), on a branch in a worktree. Follow its "Done
   when". The owner must tick one repository setting first, so give him a click-by-click
   HTML page for it. It is **not** ticked as of 18 October. The first exercise is the 12
   October week's groups. Re-fetch every address.
2. Turn Starline (did it reopen?) and the opera costume sale (keep or reverse the call)
   into plain questions for the owner.
3. **Note spec:** run `python3 ~/.claude/bin/tier-check.py --tier production <the files
   in its Files list>`, then `/nasa-code` over those files, and fill `## Pre-plan audit`.
   Then write the plan in **`specs/plans/`**, never `docs/`, with `superpowers:writing-plans`
   and `tiered-dispatch`. **Plan approval is a session boundary** (owner ruling, 6
   October). Stop there and hand off.
4. Put the 17 November trial review on Agent's Cal once the proposals build is live, and
   tell the owner.

## Constraints

- The Monday run fires at 03:04 UTC. A change to `prompts/weekly-run.md` reaches it only
  once the routine's stored prompt is updated (`trig_01U3f8NYCvzd7WEbYSNEbvNK`). The spec
  says to try the update through the routine API and read it back.
- No proposal is ever merged by an agent. Nothing may add a step that can stop a week
  from publishing.
- The DICE key and the act-now mailbox address are never written to any file. The
  repository is public.
- The main checkout has an untracked `specs/next-gen/`. It is not this work's; leave it.
