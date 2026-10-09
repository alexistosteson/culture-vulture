#!/usr/bin/env bash
#
# rot-checks-walk.sh — the owner's behavioural check for the rot-check build
# (specs/rot-checks-build.md §8). The page that goes with it is
# handoff/rot-checks-walk.html.
#
#     bash handoff/rot-checks-walk.sh 1     a misspelled venue is refused
#     bash handoff/rot-checks-walk.sh 2     a thin venue is refused, then let through
#     bash handoff/rot-checks-walk.sh 3     both kinds of warning appear and nothing stops
#     bash handoff/rot-checks-walk.sh 4     the live week passes
#
# Steps 1-3 damage a THROWAWAY COPY of the site and run the real gate
# (scripts/verify.sh) on that copy. Nothing in this folder is changed and nothing
# is published. The copy is pinned to the commit at which the build's last step
# went live, so the walk shows the same week whenever it is run. Step 4 runs the
# gate on this folder as it is today.
#
# The gate's lines are shown as the gate printed them. The verdict at the foot is
# worked out from the gate's exit code and from the text it printed — and every
# damaging change prints how many places it changed, because a change that
# matched nothing looks exactly like a check that found nothing.

set -uo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PIN=ac372e5          # main when step 7, the last step, went live
WEEK=2026-10-05      # the newest week at that commit
step="${1:-}"

case "$step" in 1|2|3|4) ;; *)
  echo "Say which step: bash handoff/rot-checks-walk.sh 1   (or 2, 3, 4)"; exit 64 ;;
esac

TMP="${TMPDIR:-/tmp}"; TMP="${TMP%/}"
WORK="$(mktemp -d "$TMP/rot-checks-walk.XXXXXX")"
COPY="$WORK/site"
LOG="$WORK/step$step.log"
line="────────────────────────────────────────────────────────────────"

say()  { printf '%s\n' "$*"; }
head1() { say "$line"; say "$1"; say "$line"; }

# Run the gate in a folder; leave its output in $LOG and its exit code in $rc.
gate() {
  say "Running the gate — about 20 seconds …"
  bash "$1/scripts/verify.sh" >"$LOG" 2>&1; rc=$?
}

# The gate's own lines that matter to a reader, exactly as printed. Warnings are
# taken from the gate's closing list only; it prints each one twice.
show() {
  say
  say "What the gate said (its own lines, copied exactly):"
  grep -E '^  FAIL |^ +BLOCK |^ +ok +|^passed |^  WARN |^VERIFICATION ' "$LOG" | sed 's/^/    /'
  say
}

verdict() {   # verdict <ok|bad> <what was expected>
  if [ "$1" = ok ]; then say "MATCHES WHAT THIS STEP SHOULD SHOW: YES — $2"
  else say "MATCHES WHAT THIS STEP SHOULD SHOW: NO — expected: $2"
       say "Copy everything above into your note for this step."; fi
}

make_copy() {
  if ! git clone -q "$ROOT" "$COPY" 2>"$WORK/clone.err" \
     || ! git -C "$COPY" checkout -q "$PIN" 2>>"$WORK/clone.err"; then
    say "COULD NOT MAKE THE THROWAWAY COPY — nothing was checked."
    sed 's/^/    /' "$WORK/clone.err"; exit 2
  fi
}

# A damaging change that matched nothing must stop the walk, not pass it.
need_changes() {   # need_changes <count> <what>
  if [ "$1" -lt 1 ]; then
    say "THE CHANGE MATCHED NOTHING ($2) — nothing was tested. Tell Claude."; exit 2
  fi
}

finish() {
  say
  say "Full output of the gate: $LOG"
  [ "$step" != 4 ] && say "The real site and this folder were not touched."
  rm -rf "$COPY"
}

case "$step" in

1)
  head1 "STEP 1 — a misspelled venue should be refused"
  make_copy
  n=$(python3 - "$COPY/data/$WEEK.json" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1]); t = p.read_text()
old, new = '"venue": "The Fillmore"', '"venue": "Fillmore"'
p.write_text(t.replace(old, new)); print(t.count(old))
PY
)
  need_changes "$n" "no listing at The Fillmore"
  say "Changed in the throwaway copy: $n listings at “The Fillmore” now say “Fillmore”."
  # Rebuild the copy's page data first, so the only thing wrong is the spelling
  # and not also "the page data is out of date".
  (cd "$COPY" && python3 scripts/build.py >/dev/null 2>&1)
  gate "$COPY"; show
  if [ $rc -eq 1 ] && grep -q 'BLOCK.*“Fillmore”.*“The Fillmore”' "$LOG"; then
    say "RESULT: the week was REFUSED."
    verdict ok "refused, and the message names both spellings."
  else
    say "RESULT: exit code $rc."
    verdict bad "refused (exit 1) with a BLOCK line naming “Fillmore” and “The Fillmore”."
  fi
  finish ;;

2)
  head1 "STEP 2 — a thin venue should be refused until the digest explains it"
  make_copy
  n=$(python3 - "$COPY/digests/$WEEK.md" "$WORK/removed.txt" <<'PY'
import sys, re, pathlib
p = pathlib.Path(sys.argv[1]); t = p.read_text()
m = re.search(r"^- \*\*The Regency Ballroom\*\* — reached.*?(?=^- |^## |\Z)", t, re.S | re.M)
if not m:
    print(0); sys.exit()
pathlib.Path(sys.argv[2]).write_text(m.group(0))
p.write_text(t[:m.start()] + t[m.end():]); print(1)
PY
)
  need_changes "$n" "no Regency Ballroom line under Thin this week"
  say "The Regency Ballroom has 1 listing this week after 2, 2, 4 and 5 — a thin venue."
  say "The digest explains it in one line under “Thin this week”."
  say
  say "FIRST HALF. Changed in the throwaway copy: that one line is deleted."
  gate "$COPY"; show
  rc_a=$rc
  grep -q 'BLOCK.*Regency Ballroom' "$LOG" && blocked=yes || blocked=no
  cp "$LOG" "$WORK/step2-first-half.log"
  [ $rc_a -eq 1 ] && say "RESULT: the week was REFUSED." || say "RESULT: exit code $rc_a."
  say
  say "SECOND HALF. The same line is put back:"
  sed 's/^/    /' "$WORK/removed.txt"
  (cd "$COPY" && git checkout -q -- "digests/$WEEK.md")
  gate "$COPY"; show
  grep -q 'ok .*Regency Ballroom.*accounted for' "$LOG" && answered=yes || answered=no
  [ $rc -eq 0 ] && say "RESULT: the week was LET THROUGH." || say "RESULT: exit code $rc."
  if [ $rc_a -eq 1 ] && [ $blocked = yes ] && [ $rc -eq 0 ] && [ $answered = yes ]; then
    verdict ok "refused without the line, let through with it."
  else
    verdict bad "refused (exit 1, a BLOCK line naming the Regency) without the line; let through (exit 0, the Regency “accounted for”) with it."
  fi
  say "First half's full output: $WORK/step2-first-half.log"
  finish ;;

3)
  head1 "STEP 3 — both kinds of warning should appear, and nothing should stop"
  make_copy
  n=$(python3 - "$COPY/config/sources.yml" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1]); t = p.read_text()
old, new = "{ name: Oakland Arena,", "{ name: Oakland Arena (walk),"
p.write_text(t.replace(old, new)); print(t.count(old))
PY
)
  need_changes "$n" "no Oakland Arena entry in the venue list"
  say "Kind one — a watched venue gone quiet — is already there for real."
  say "Kind two — a relied-on venue nobody wrote down — needs staging."
  say "Changed in the throwaway copy: Oakland Arena's entry in the venue list is"
  say "renamed, so the list no longer covers it ($n entry changed)."
  gate "$COPY"; show
  grep -q 'WARN .*has produced no listing' "$LOG" && quiet=yes || quiet=no
  grep -q 'WARN .*Oakland Arena.*is not in sources.yml' "$LOG" && undeclared=yes || undeclared=no
  if [ $rc -eq 0 ] && [ $quiet = yes ] && [ $undeclared = yes ]; then
    say "RESULT: the week was LET THROUGH, with warnings."
    verdict ok "both kinds of warning printed and the week still passed."
  else
    say "RESULT: exit code $rc (quiet-venue warning: $quiet, unwritten-venue warning: $undeclared)."
    verdict bad "exit 0, a warning that a venue “has produced no listing”, and a warning that Oakland Arena “is not in sources.yml”."
  fi
  finish ;;

4)
  head1 "STEP 4 — the live week, untouched, should pass"
  say "Nothing is changed. This runs the gate on the site as it is today."
  gate "$ROOT"; show
  if [ $rc -eq 0 ] && grep -q '^VERIFICATION PASSED' "$LOG"; then
    say "RESULT: the live week PASSED."
    verdict ok "passed. Warnings may be listed; they do not stop a week."
  else
    say "RESULT: exit code $rc."
    verdict bad "VERIFICATION PASSED (exit 0)."
  fi
  finish ;;

esac
