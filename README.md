# COMMONCAUSE

**Consensus-backed common-cause exposure guard for autonomous portfolios.**

COMMONCAUSE prevents a portfolio from looking diversified while several commitments secretly depend on the same upstream provider, infrastructure, model provider, data source, custodian, network, region or logistics system.

Three commitments can have different names, different endpoints and different operators while still sharing one failure root. COMMONCAUSE uses GenLayer consensus only for the semantic step that ordinary deterministic contracts cannot safely perform: mapping a public commitment and its evidence onto the registered factor-catalogue snapshot for that evaluation. Exposure arithmetic, hierarchy roll-up, caps, admission, release and replay-safe consumer checks remain deterministic.

This repository is intentionally **contract-only**. It has no frontend and should be submitted under **Intelligent Contracts**, not Projects.

## Target network

- Network: **Studionet**
- Chain ID: **61999**
- RPC: `https://studio.genlayer.com/api`
- Explorer: `https://explorer-studio.genlayer.com/`

The contract itself is network-agnostic. Repository deployment instructions deliberately target Studionet 61999.

## The primitive

Suppose a treasury thinks it diversified across two workloads:

```text
Workload A -> AWS us-east-1
Workload B -> AWS eu-west-1
```

The regional dependencies are different, but both roll up to the same provider:

```text
AWS
├── us-east-1
└── eu-west-1
```

If the risk book allows at most 50% exposure to AWS, the second commitment must be blocked when the combined exposure would exceed that provider-level cap even if each region remains below its own regional cap.

COMMONCAUSE makes that check composable and stateful.

## Protocol split

### GenLayer consensus decides only

> Which already-registered dependency factors are materially implicated by this commitment and its public evidence?

The leader and validators independently:

1. fetch the same bounded HTTPS evidence manifest;
2. inspect the same immutable factor catalogue;
3. derive the material registered factor IDs;
4. classify evidence coverage as `CLEAR`, `AMBIGUOUS`, `UNREGISTERED` or `UNAVAILABLE`;
5. compare the actual factor set and source-availability vector.

A validator does **not** merely schema-check the leader output.

### Deterministic contract logic decides

- factor hierarchy and parent roll-up;
- total portfolio capacity;
- factor-specific exposure caps;
- commitment admission or blocking;
- exposure increments and decrements;
- factor retirement safety;
- cap-update safety;
- mapping hashes;
- book state hashes;
- consumer eligibility.

The LLM never chooses a cap, adjusts a notional, accepts risk, invents a compromise or decides whether a cap is exceeded.

## Factor hierarchy

A risk book can define up to 24 factors. A factor may have one already-existing parent, which makes ancestry acyclic by construction.

Example:

```text
AWS                          cap 50%
└── AWS us-east-1            cap 30%

Cloudflare                   cap 40%
```

A commitment mapped directly to `AWS us-east-1` consumes exposure against both:

```text
AWS us-east-1 +200
AWS           +200
```

This is the key common-cause mechanism: apparently separate children still accumulate at their shared root.

## Fixed-capacity denominator

Each risk book has a fixed capacity and a caller-defined unit label.

Example:

```text
capacity = 1,000 risk_units
AWS cap = 5,000 bps = 500 units
us-east-1 cap = 3,000 bps = 300 units
```

A new 260-unit commitment mapped to `AWS eu-west-1` may be locally safe at the regional factor but still be blocked because AWS total exposure would cross 500 units.

Using a fixed book capacity avoids a moving denominator that could make an early commitment impossible merely because the portfolio is initially small.

## Evidence coverage is fail-closed

Consensus returns one of four coverage states:

- `CLEAR` — all material dependencies evidenced by the supplied public material map clearly to registered factors;
- `AMBIGUOUS` — mapping cannot be established safely;
- `UNREGISTERED` — evidence indicates a material dependency that the risk book has not represented;
- `UNAVAILABLE` — at least one required public source could not be retrieved by the execution.

Only `CLEAR` can reach deterministic admission.

A `CLEAR` answer with zero factors is converted to ambiguity. The contract therefore cannot silently accept a non-zero commitment as having no material dependency.

## Why factors are registered before commitments

COMMONCAUSE deliberately does not let an LLM invent canonical providers or entities during admission. The risk-book owner defines the factor vocabulary first. Consensus maps evidence to that frozen vocabulary.

This keeps authority deterministic and makes the trust boundary explicit:

- **owner:** defines what failure roots matter and their caps;
- **GenLayer:** decides whether public evidence maps a commitment onto those roots;
- **contract:** enforces portfolio exposure mechanically.

If evidence reveals an important dependency that is missing from the catalogue, the correct outcome is `UNREGISTERED`, not an invented factor.

## Consumer interface

Other Intelligent Contracts can consume the primitive through:

```python
is_admitted(commitment_id, expected_mapping_hash)
```

For stricter consumers that need to pin the current exposure-state snapshot:

```python
is_admitted_for_state(
    commitment_id,
    expected_mapping_hash,
    expected_book_hash,
)
```

The state hash commits to the book revision, capacity, active total, factor status/caps/exposures/ancestry, and active commitment mappings. A successful book mutation advances the revision and changes the hash. It is an exposure-state pin; it does not hash every descriptive field of blocked or released commitment records.

`examples/protected_allocator.py` is a deliberately tiny consumer contract. It refuses an allocation unless COMMONCAUSE confirms the commitment is active and the exact mapping hash matches. It also prevents action-hash replay.

The consumer is included to demonstrate reuse. COMMONCAUSE itself remains the submission primitive.

## Main API

### Writes

```text
create_riskbook(name, purpose, unit_label, capacity)
register_factor(riskbook_id, name, category, description, cap_bps, parent_factor_id)
update_factor_cap(factor_id, new_cap_bps)
retire_factor(factor_id)
propose_commitment(riskbook_id, label, description, notional, evidence_manifest)
cancel_blocked_commitment(commitment_id)
release_commitment(commitment_id, reason)
```

`evidence_manifest` is a JSON array containing 1–4 HTTPS URLs.

### Views

```text
get_riskbook(riskbook_id)
get_factor(factor_id)
get_commitment(commitment_id)
factor_exposure(factor_id)
would_exceed(riskbook_id, notional, factor_ids_json)
is_admitted(commitment_id, expected_mapping_hash)
is_admitted_for_state(commitment_id, expected_mapping_hash, expected_book_hash)
current_state_hash(riskbook_id)
```

`would_exceed` is fully deterministic. It is useful after a dependency mapping already exists and a caller wants to inspect cap headroom without another LLM call.

## Security properties

### 1. Independent validator re-derivation

The leader and validator both perform the actual public-source fetch and semantic mapping. Agreement requires the same:

- sorted material factor IDs;
- evidence coverage class;
- source availability vector.

Free-form explanation is not part of the consensus decision.

### 2. Prompt injection boundary

Risk-book purpose, commitment text, factor descriptions and web pages are explicitly labelled untrusted data. They cannot alter the task instructions.

### 3. Public HTTPS evidence only

The manifest rejects non-HTTPS, local-host and whitespace-containing URLs and bounds URL count and length.

This does not prove a source is authoritative. COMMONCAUSE is a portfolio dependency mapper, not a source-authority oracle. Deployers must choose appropriate public evidence.

### 4. Parent exposure cannot be bypassed

A direct child mapping is expanded deterministically to all ancestors before accounting. Duplicate ancestors are deduplicated.

### 5. Exposure is conserved

Admission increments the book total and every factor in the closure. Release decrements the same stored closure. Underflow checks fail closed.

### 6. Retired factors cannot silently disappear

A factor cannot retire while it has active exposure or active child factors.

### 7. Cap changes cannot create an immediate violation

A factor cap cannot be lowered below its current active exposure.

### 8. Consumer pins

Every evaluated commitment stores:

- evidence manifest hash;
- factor-catalogue hash;
- consensus-derived direct factors;
- coverage class;
- mapping hash.

A consumer can pin the mapping hash, and optionally the complete risk-book state hash.

## What COMMONCAUSE does not claim

COMMONCAUSE does **not** prove that:

- the public evidence is globally complete;
- a provider is truthful;
- every hidden dependency has been discovered;
- two businesses are legally the same entity;
- a commitment will succeed;
- a factor cap is economically optimal.

It proves a narrower and reusable property:

> Given a frozen risk catalogue, public evidence and deterministic caps, GenLayer validators agreed on the material registered dependencies of this commitment, and the contract admitted it only if the resulting common-cause exposure stayed inside the declared limits.

## Direct Mode tests

Install development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Run the complete Direct Mode suite with closure-pickling checks enabled:

```bash
python -m pytest tests/ -q
```

Verified locally with 30 passing tests using `genlayer-test` 0.29.2 and the stable GenVM SDK matching the contract dependency. Full GenVM linter validation passes for both contracts with `genvm-linter` 0.11.0. The installed stable GenLayer CLI is 0.39.1. See [proof/README.md](proof/README.md) for finalised Studionet lifecycle evidence and the fee/explorer limitations.

Important scenarios include:

- factor hierarchy creation;
- owner-only mutation;
- parent roll-up;
- shared-parent cap rejection;
- child cap rejection;
- unregistered-dependency fail-closed path;
- ambiguous mapping fail-closed path;
- release accounting;
- retirement protection;
- unsafe cap reduction rejection;
- deterministic `would_exceed`;
- mapping-hash pinning;
- state-hash mutation;
- malicious/different validator mapping disagreement;
- equivalent decision with different explanatory reason acceptance;
- portfolio-cap enforcement;
- source-level checks that the LLM never controls admission arithmetic.

## Repository structure

```text
contracts/commoncause.py          reusable Intelligent Contract
examples/protected_allocator.py   minimal IC consumer
examples/demo_manifest.json       example public-evidence manifest shape
tests/                            Direct Mode + source-level tests
docs/ARCHITECTURE.md              design and invariants
docs/THREAT_MODEL.md              trust boundary and attack analysis
docs/LIVE_DEMO.md                 Studionet 61999 reviewer runbook
proof/README.md                    where final deployment evidence goes
DEPLOYMENT.md                     exact Studionet deployment workflow
SUBMISSION.md                     reviewer-facing submission copy
IFEM_CODEX_HANDOFF.md             final agent handoff
scripts/preflight.py              repository sanity checks
```

## Licence

MIT.
