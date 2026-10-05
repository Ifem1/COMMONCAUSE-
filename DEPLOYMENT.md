# Studionet deployment

COMMONCAUSE targets **GenLayer Studionet, chain ID 61999**.

## Network identity

```text
Network alias: studionet
RPC: https://studio.genlayer.com/api
Chain ID: 61999
Explorer: https://explorer-studio.genlayer.com/
```

Do not change the repository to another Studio environment during finalisation.

## 1. Tooling check

Use current stable GenLayer tooling compatible with Studionet.
The verified stable tool versions in this workspace are GenLayer CLI 0.39.1, `genlayer-test` 0.29.2 and `genvm-linter` 0.11.0. Do not use the v0.40/Consensus v0.6 release-candidate stack for this target.

```bash
genlayer --version
genlayer network list
genlayer network set studionet
genlayer network info
```

Before signing anything, confirm `network info` resolves to the Studionet RPC and chain ID **61999**.

## 2. Run local checks first

```bash
python -m pip install -r requirements-dev.txt
python scripts/preflight.py
python -m pytest tests/ -q
```

The full Direct Mode suite runs with pickling checks enabled for the non-deterministic closures. Run the linter on both deployable contracts:

```bash
genvm-lint check contracts/commoncause.py
genvm-lint check examples/protected_allocator.py
```

## 3. Deploy COMMONCAUSE

```bash
genlayer network set studionet
genlayer deploy --contract contracts/commoncause.py
```

Wait for finalization and record:

- contract address;
- deploy transaction hash;
- explorer link;
- finalization status;
- deployed source/commit SHA.

Write those values into `proof/README.md`.

## 4. Exercise the live primitive

Use `docs/LIVE_DEMO.md` as the authoritative lifecycle.

At minimum, final live evidence should prove:

- factor hierarchy;
- one admitted commitment;
- one shared-parent cap rejection;
- one unregistered dependency fail-closed result;
- one release that restores headroom;
- stable mapping hashes and state hashes.

The public evidence pages used for the final demonstration should be stable and should plainly state the relevant infrastructure dependencies. Do not rely on screenshots when a public textual source is available.

## 5. Deploy the optional consumer

`examples/protected_allocator.py` is not the main submission. Deploy it only to prove reuse.

Deploy it with the COMMONCAUSE address and risk-book ID as constructor arguments using the current CLI syntax supported by the installed stable toolchain.

Then prove:

- correct admitted commitment + mapping hash succeeds;
- wrong mapping hash fails;
- blocked commitment fails;
- released commitment fails;
- duplicate `action_hash` fails.

## 6. Verified lifecycle and final repository updates

The live Studionet lifecycle has been completed for the current source. Actual addresses, transaction hashes, finalized receipt outcomes, factor exposure reads, mapping hashes and state hashes are recorded in [proof/README.md](proof/README.md). The explorer detail page did not return transaction details during verification, so finalization is supported by CLI receipt waits and contract state reads.

After any further source changes or redeployment:

- fill `proof/README.md` with the actual addresses and transaction hashes;
- add exact successful commands if the installed stable CLI syntax differs from this file;
- record the final direct-test count;
- record linter output;
- record at least one consensus transaction with multiple validators;
- update `SUBMISSION.md` only with claims that are actually proven.

Per-path GEN fees remain pending: the stable Studionet CLI and client available for this run did not expose reliable per-transaction fee measurements. Do not substitute rounded wallet-balance displays or fee tooling for a different network.

## No frontend

Do not add a Next.js, React, Vue or other frontend. COMMONCAUSE is intentionally a standalone reusable Intelligent Contract primitive.
