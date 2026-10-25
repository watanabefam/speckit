#!/usr/bin/env bash
# negative-control.sh — run a declared check against a mutant of this tree.
#
# A control that always fails (`exit 1`) proves only that a runner can see a non-zero status. This one
# goes through the same entry point as the check, on a copy of the tree that is broken in a way the
# check exists to notice, and it insists the failure arrives for the stated reason. That last part is
# the difference between "something went wrong" and "the check noticed" — the specificity half is what
# a bare `exit 1` cannot give, and what a broken copy would otherwise be mistaken for.
#
# Exit codes are the ones `bin/speckit-verify` reacts to, so they are a contract, not a preference:
#   1    the mutant was caught, by the expected message   -> the check is evidence
#   0    the check stayed green under the mutation        -> the engine reports `vacuous`
#   127  the control could not demonstrate anything       -> the engine reports `not-run`
#
# Usage:
#   scripts/negative-control.sh --mutate PATH --expect TEXT [--id ID] [--command CMD] [--tree DIR] [--keep]
#
#   --mutate   executable path (relative to the tree) that breaks the copy; non-zero = it changed nothing
#   --expect   the text the failing run must contain
#   --id       manifest check whose command to run (default: test)
#   --command  run this instead of the manifest's command (for tests, or a suite that is not make)
#   --tree     the tree to copy and mutate (default: this repository; the gate passes a fixture)
#   --keep     leave the mutated copy behind and print its path
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MUTATE=""
EXPECT=""
ID="test"
COMMAND=""
TREE="$ROOT"
KEEP=0

die() { printf 'negative-control: %s\n' "$*" >&2; exit 127; }
usage() { awk '/^# Usage:/{u=1} u && /^#/{sub(/^# ?/,""); print; next} u{exit}' "$0"; }

while [ $# -gt 0 ]; do
  case "$1" in
    --mutate) MUTATE="${2-}"; shift; shift ;;
    --expect) EXPECT="${2-}"; shift; shift ;;
    --id) ID="${2-}"; shift; shift ;;
    --command) COMMAND="${2-}"; shift; shift ;;
    --tree) TREE="${2-}"; shift; shift ;;
    --keep) KEEP=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) die "unknown option: $1 (try --help)" ;;
  esac
done

[ -n "$MUTATE" ] || die "--mutate is required"
[ -n "$EXPECT" ] || die "--expect is required"
[ -d "$TREE" ] || die "--tree is not a directory: $TREE"
[ -x "$TREE/$MUTATE" ] || die "mutator is missing or not executable: $TREE/$MUTATE"

# The command comes from the manifest by default, so the control and the check cannot drift apart: a
# control that runs a different command than the check is measuring something nobody declared.
if [ -z "$COMMAND" ]; then
  COMMAND="$(python3 - "$ROOT/.specify/verify.json" "$ID" <<'PY'
import json, sys
try:
    doc = json.load(open(sys.argv[1]))
except Exception:
    sys.exit(1)
for chk in doc.get("checks", []):
    if chk.get("id") == sys.argv[2]:
        print(chk.get("command") or "")
        sys.exit(0)
sys.exit(1)
PY
)" || die "no '$ID' check in .specify/verify.json — pass --command"
  [ -n "$COMMAND" ] || die "check '$ID' declares no command"
fi

WORK="$(mktemp -d "${TMPDIR:-/tmp}/negative-control.XXXXXX")" || die "could not create a temp directory"
LOG="$WORK.mutation.log"
cleanup() {
  rm -f "$LOG"
  if [ "$KEEP" = "1" ]; then
    printf 'negative-control: kept %s\n' "$WORK" >&2
  else
    rm -rf "$WORK"
  fi
}
trap cleanup EXIT INT TERM

# A copy, never the tree in place. A control that edits the tree it is judging leaves that tree broken
# if it is interrupted, and every later run then measures the mutant instead of the work.
copy_tree() {
  ( cd "$TREE" || exit 1
    for entry in .[!.]* *; do
      [ -e "$entry" ] || continue
      case "$entry" in
        .git|node_modules|.venv|__pycache__) continue ;;
      esac
      cp -R "$entry" "$WORK/" || exit 1
    done )
}
copy_tree || die "could not copy $TREE"
[ -n "$(ls -A "$WORK" 2>/dev/null)" ] || die "the copy is empty — refusing to run a check against nothing"

if ! ( cd "$WORK" && "./$MUTATE" ) >"$LOG" 2>&1; then
  printf 'negative-control: the mutator changed nothing (%s), so there is no mutant to run\n' "$MUTATE" >&2
  tail -5 "$LOG" >&2 || true
  exit 127
fi

set +e
OUT="$( cd "$WORK" && eval "$COMMAND" 2>&1 )"
RC=$?
set -e

if [ "$RC" -eq 0 ]; then
  printf 'negative-control: the suite passed on the mutant (%s) — the check does not notice this defect\n' \
    "$MUTATE" >&2
  exit 0
fi
case "$RC" in
  126|127) die "the suite could not run in the copy (exit $RC)" ;;
esac

if printf '%s\n' "$OUT" | grep -qF -- "$EXPECT"; then
  printf 'negative-control: caught by "%s" (suite exit %s)\n' "$EXPECT" "$RC"
  exit 1
fi

printf 'negative-control: the suite failed (exit %s) but not for the stated reason — no "%s" in its output\n' \
  "$RC" "$EXPECT" >&2
printf '%s\n' "$OUT" | tail -20 >&2
exit 127
