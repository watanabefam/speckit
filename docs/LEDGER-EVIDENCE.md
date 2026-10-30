# Ledger evidence — why the verifier writes the line, and the worker does not

`progress.md` has always said "completion claims are not evidence". That rule was true and
unenforced: the `Task <n>: complete` line was still typed by the agent that did the work, so the
ledger recorded a **claim in a durable place**. Durable is not the same as true.

`bin/speckit-verify` closes that gap. It runs the task's own named verification, and only then
appends a line. It also hash-chains the line, so a hand-written entry is detectable rather than
merely frowned upon.

```bash
speckit-verify specs/006-vision-image-review --list          # what is runnable, what is not
speckit-verify specs/006-vision-image-review T3              # run T3's verifier, record it
speckit-verify specs/006-vision-image-review T4 --attest "Tim: read the diff, ran the deck by hand"
speckit-verify specs/006-vision-image-review --audit         # is the chain intact?
speckit-resume specs/006-vision-image-review --strict        # unattended loops: only verified counts
```

## The three evidence classes

A ledger line now says which kind of evidence backs it, and they are not interchangeable:

| Line | Who produced it | Counts in `--strict`? |
|---|---|---|
| `complete · verified · <cmd> · exit 0 · … · sig …` | `speckit-verify` ran the command | yes |
| `complete · attested · <who: what>` | a human looked, no automated oracle exists | no |
| `complete (<reason>)` | the agent, before this tool existed | no |
| `withdrawn` | resolved, not outstanding | n/a |

`--strict` is the mode for an unattended loop: nobody is going to read a human attestation before
the next iteration, so only a re-executed check counts as done.

## How the chain works

Each entry carries `prev <sig>` (the previous entry's signature) and `sig <sha256(prev|body)[:12]>`.
`--audit` recomputes the whole chain. Three things follow, and all three are exercised in
`scripts/self-gate.sh` (§1i2):

1. A line typed by hand does not chain — it is reported, and exit is 4.
2. Editing an older line breaks every link after it.
3. `speckit-resume --strict` recomputes the chain itself, so imitating the format is not enough.

A broken chain does not stop `speckit-resume` in its default mode. That is deliberate: stranding a
project because an old ledger predates the convention would be a worse defect than the claim it
flags. It warns, and `--strict` refuses.

## What the entry records, and why each field is there

```
Task 3: complete · verified · `node scripts/test/vision-review.test.mjs` · exit 0 ·
  at 2026-10-29T22:47:21Z · head dca01b4 · dirty 16 · prev 000000000000 · sig 5d4d23e497b9
```

- **the command** — so a later reader can re-run exactly what was run, not a paraphrase of it.
- **the exit code** — a failure is recorded as `failed · verified`, never as a completion.
- **`head` and `dirty`** — what the check ran against. A green check on a dirty tree is weaker
  evidence than a green check on a clean commit, and the ledger should not hide which it was.
- **`prev`/`sig`** — the chain.

## Tri-state exit codes

A check that did not run provides no signal, and reporting it as a pass converts a missing
capability into a green build — the same argument this kit already makes about skipped gate
sections. So `speckit-verify` distinguishes them:

| Exit | Meaning |
|---|---|
| 0 | verifier ran and passed; evidence appended |
| 1 | verifier ran and failed; failure appended |
| 2 | usage or setup error |
| 3 | **could not run** — the task names no runnable verifier; nothing appended |
| 4 | ledger chain is broken; refusing to append |

Exit 3 is the honest answer for the common case: most tasks in a real `tasks.md` do not name a
runnable verification. `--list` shows which do, so the gap is visible before a loop starts rather
than discovered mid-run.

## Where this came from

The design is not invented here; it is the written-up version of what several 2026 papers say:

- **Ratification by Re-execution** (Chauhan, 2026) — "a verifier that reads an implementer's
  claims and reasons about them produces an opinion. What a compliance record requires is primary
  execution evidence produced independently of those claims." Its protocol re-executes *before*
  reading the implementer's self-verification.
- **Agreement by Construction** (Kumar, 2026) — once a deterministic rule decides a case, an LLM
  judge's verdict on that case is not independent evidence of anything, and judges' reported
  agreement inflates.
- **When the Judge is Wrong** (Sudjianto & Lau, 2026) — judges need ground truth established
  outside the class of system being evaluated; otherwise the evaluation is circular.
- **Comparing Self-Verification, Multi-Agent Verification and External Retrieval** (Maharaj, 2026)
  — external verification detects more of a model's own errors than self-verification does.
- **FLAP-X** (Madariaga, 2026) — separate what can be held invariant from what cannot. Here: the
  command, its exit code and the chain are invariant; the agent's account of itself is not.

**Limits, stated plainly.** These are recent preprints, mostly with few or no citations; they agree
with each other and with practitioner experience, which is why the shape was adopted, but they are
evidence of direction, not of effect size. No study was found that measures agentic coding loops
with verifier-written ledgers specifically. The hash chain is tamper-**evident**, not tamper-proof:
anyone with write access can rewrite the whole ledger and recompute every signature. It detects the
common failure — an agent (or a person) adding a line by hand — not a determined forger.

And one limit of the tool itself: a task whose verifier is a weak check gets a strong-looking
ledger line. `speckit-verify` records *that a command passed*, not that the command was worth
running. Naming a good verifier is still a human judgement, made in `tasks.md`.
