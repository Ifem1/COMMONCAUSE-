# COMMONCAUSE final build status

COMMONCAUSE remains a standalone GenLayer Intelligent Contract submission for **Studionet chain 61999** (`https://studio.genlayer.com/api`). The repository contains no frontend.

## Verified locally

- `python scripts/preflight.py` passes.
- The complete Direct Mode suite passes: **30 tests**, with Direct Mode closure-pickling checks enabled.
- `genvm-lint check` and SDK validation pass for `contracts/commoncause.py` and `examples/protected_allocator.py` using `genvm-linter` 0.11.0.
- Tool versions: GenLayer CLI 0.39.1, `genlayer-test` 0.29.2, `genvm-linter` 0.11.0, `genlayer-py` 0.16.3.
- The source handles the stable CLI's JSON-string-wrapped evidence-manifest argument form, discovered by a finalized live trial that rolled back before the fix.

## Verified on Studionet

The corrected COMMONCAUSE deployment and minimal `ProtectedAllocator` consumer were finalized. The risk-book lifecycle demonstrated an admitted child exposure, a different child blocked by the shared parent cap, an unregistered Azure dependency blocked fail-closed, release restoring parent headroom, and a fresh commitment admitted afterward. The consumer accepted an exact active mapping and rejected wrong, blocked, released, and replayed actions.

Addresses, transaction hashes, finalized outcomes, mapping/state hashes, and the superseded failed trial are recorded in [proof/README.md](proof/README.md). The official explorer detail page did not return transaction details during verification; successful CLI receipt waits supplied finalization evidence.

## Explicitly pending

- Per-path GEN fees: the stable Studionet tooling available here did not expose reliable per-transaction fee figures. No fee numbers are claimed.
- Explorer detail-page lookup: the configured explorer returned a service error, and the official transaction page failed to fetch details during this run.

The public submission repository is `Ifem1/COMMONCAUSE-`. No pending item is represented as completed evidence. See [DEPLOYMENT.md](DEPLOYMENT.md) and [proof/README.md](proof/README.md).
