# Live reviewer demo — Studionet 61999

The purpose of this demo is to prove the mechanism, not merely deploy the source.

## Preparation

Choose stable public pages that clearly support two commitments with different child dependencies sharing one parent provider. Also choose one page exposing a material dependency not yet present in the catalogue.

Record the exact evidence URLs before deployment.

## Phase A — create the risk book

Create a book such as:

```text
name: Agent Infrastructure
unit: risk_units
capacity: 1000
```

Register:

```text
AWS                    PROVIDER      cap 5000 bps
AWS us-east-1          REGION        cap 3000 bps parent=AWS
AWS eu-west-1          REGION        cap 3000 bps parent=AWS
Cloudflare             NETWORK       cap 4000 bps
```

Verify `get_riskbook` and `get_factor`.

## Phase B — admit commitment A

Use public evidence establishing a dependency on `AWS us-east-1`.

Submit notional 250.

Expected:

```text
status = ACTIVE
AWS us-east-1 exposure = 250
AWS exposure = 250
book total_active = 250
```

Record the commitment mapping hash.

## Phase C — prove common-cause rejection

Use different public evidence establishing a dependency on `AWS eu-west-1`.

Submit notional 260.

Regional cap:

```text
260 <= 300
```

but parent provider exposure would be:

```text
250 + 260 = 510 > 500
```

Expected:

```text
status = BLOCKED
reason_code = FACTOR_CAP
blocking_factor_id = AWS
```

This is the core COMMONCAUSE proof.

## Phase D — prove fail-closed missing vocabulary

Use evidence that clearly names another material provider which has not been registered.

Expected consensus result:

```text
coverage = UNREGISTERED
status = BLOCKED
```

Do not add the missing factor until after this transaction finalises and is recorded.

## Phase E — release restores headroom

Release commitment A.

Expected:

```text
AWS us-east-1 exposure = 0
AWS exposure = 0
book total_active = 0
```

Submit a fresh commitment equivalent to B.

Expected: it may now be admitted if every applicable factor cap is respected.

## Phase F — consumer proof

Deploy `ProtectedAllocator` against the live COMMONCAUSE address and risk-book ID.

Prove:

1. active commitment + exact mapping hash succeeds;
2. wrong mapping hash fails;
3. blocked commitment fails;
4. released commitment fails;
5. repeated action hash fails.

## Phase G — consensus adversarial evidence

Use Direct Mode or a controlled validator environment to show a validator independently deriving a different factor set rejects the leader result.

This is critical reviewer evidence because schema validation alone would be insufficient.

## Capture

Add to `proof/README.md`:

- COMMONCAUSE address;
- deploy tx;
- optional consumer address;
- every lifecycle tx hash;
- finalised transaction statuses;
- direct-test count;
- linter result;
- factor IDs used in the demo;
- mapping hashes;
- before/after state hashes;
- exact evidence URLs.
