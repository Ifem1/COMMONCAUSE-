# Architecture

## Problem

Naive diversification counts commitments, providers or endpoints as distinct. Real failure domains are hierarchical and can be semantically hidden.

```text
Agent A -> Service X -> AWS us-east-1 -> AWS
Agent B -> Service Y -> AWS eu-west-1 -> AWS
Agent C -> Service Z -> Cloudflare
```

A deterministic exposure engine cannot derive those relationships from public prose by itself. A free-form LLM should not control economic limits either.

COMMONCAUSE therefore uses a hybrid architecture.

## Layer 1: deterministic risk vocabulary

The risk-book owner creates named factors with:

- category;
- description;
- parent factor;
- exposure cap in basis points of fixed book capacity.

A child can only point to an already-existing parent. This makes the hierarchy acyclic by construction.

The vocabulary is intentionally bounded. Consensus may select registered factors but cannot create new canonical factors.

## Layer 2: public-evidence semantic mapping

A commitment freezes:

- label;
- description;
- integer notional;
- 1–4 HTTPS evidence URLs;
- current factor catalogue hash.

Each validator independently fetches the public sources and runs the same semantic task.

Decision fields are:

```text
factor_ids
coverage
source_statuses
```

Free-form reasoning is discarded from the consensus boundary.

## Layer 3: deterministic hierarchy closure

If consensus returns direct factor `AWS us-east-1`, the contract traverses:

```text
AWS us-east-1 -> AWS
```

and stores the complete exposure closure. Duplicate ancestors are included only once.

The stored closure is the exact list later used for release, so exposure increments and decrements are symmetric.

## Layer 4: deterministic admission

For each factor in the closure:

```text
max_exposure = book_capacity * cap_bps / 10000
```

The commitment is admitted only if:

```text
total_active + notional <= book_capacity
```

and for every factor:

```text
factor.current_exposure + notional <= factor.max_exposure
```

There is no subjective risk score.

## Layer 5: composable receipts

Each commitment stores a `mapping_hash` binding:

- risk book ID;
- label hash;
- description hash;
- notional;
- factor-catalogue hash;
- consensus factor IDs;
- coverage class.

Another IC can pin that mapping using `is_admitted`.

The risk book also has a `state_hash` binding its revision, capacity and totals, factor status/cap/exposure/ancestry state, and active commitment mappings. Every successful book mutation advances the revision. This is an exposure-state pin; it does not hash every descriptive field of blocked or released commitment records. High-assurance consumers may pin both mapping and exposure-state hashes.

## Why a fixed capacity

A percentage of *current* portfolio value makes early allocations pathological: the first position is automatically 100% of the portfolio.

COMMONCAUSE instead sets the denominator once at risk-book creation. Cap percentages therefore express exposure relative to a declared portfolio capacity rather than a moving total.

## Why blocked commitments remain stored

A blocked commitment is useful evidence of the protocol decision. It records:

- mapping result;
- coverage state;
- blocking factor;
- catalogue hash;
- mapping hash.

It consumes no exposure and cannot later become active by silent mutation. After conditions change, the owner submits a fresh commitment that is analysed against the then-current factor catalogue.

This avoids retroactively changing the meaning of an old consensus receipt.
