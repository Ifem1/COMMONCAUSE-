# Threat model

## Protected properties

COMMONCAUSE is designed to protect these properties:

1. a commitment cannot consume portfolio capacity without an agreed dependency mapping;
2. a child dependency cannot bypass exposure at its registered ancestors;
3. ambiguous, incomplete or unavailable evidence cannot produce an active commitment;
4. a validator must re-derive the material factor set rather than validate output shape only;
5. the LLM cannot choose caps or override deterministic arithmetic;
6. active exposure cannot disappear through factor retirement;
7. release cannot underflow stored exposure;
8. consumers can bind to the exact mapping hash.

## Threat: malicious commitment text or web page

Commitment text and web content may contain prompt injection.

Mitigation:

- prompt treats all supplied content as untrusted data;
- the task is bounded to selecting registered factor IDs;
- outputs are canonicalised;
- validators independently re-fetch and re-derive;
- economic admission occurs outside nondeterministic execution.

## Threat: leader omits a dependency

A leader could propose fewer factors than the evidence supports.

Mitigation:

- validator independently runs the same mapping task;
- factor-set equality is part of the validator decision;
- disagreement rejects the leader result.

## Threat: missing factor catalogue entry

An evidence page may clearly reveal a dependency absent from the owner's catalogue.

Mitigation:

- prompt requires `UNREGISTERED` rather than guessing a factor;
- `UNREGISTERED` fails closed;
- owner must register the factor and submit a fresh commitment.

## Threat: source temporarily unavailable

Mitigation:

- source availability is a consensus decision field;
- any unavailable required source forces `UNAVAILABLE`;
- `UNAVAILABLE` cannot activate exposure.

## Threat: aliasing of the same provider

COMMONCAUSE does not globally resolve corporate/entity aliases. The risk-book owner is responsible for constructing a coherent factor catalogue. If `AWS` and `Amazon Web Services` are mistakenly registered as independent roots, the semantic layer cannot safely repair the policy model.

This is an explicit trust boundary, not hidden AI authority.

## Threat: cap manipulation after admission

The owner controls the risk policy and can change caps.

Mitigations:

- a new cap cannot be set below current exposure;
- book revision and state hash change;
- consumers that require immutable policy can pin the state hash or use a wrapper with stricter governance.

COMMONCAUSE does not claim the owner is untrusted. It is a reusable risk engine under an owner-defined policy.

## Threat: hidden real-world dependency

No finite public-evidence protocol can prove absence of undisclosed dependencies.

COMMONCAUSE therefore does not claim global completeness. Its guarantee is scoped to the frozen registered vocabulary and supplied public evidence.

## Threat: stale admitted mapping

A commitment stays active until the owner releases it. COMMONCAUSE does not continuously monitor webpages for later dependency changes.

A higher-level application may require periodic re-admission or compose COMMONCAUSE with a separate drift-monitoring primitive. Continuous monitoring is deliberately outside this contract's scope.

## Threat: consumer replay

COMMONCAUSE itself only exposes read-only admission receipts. The example `ProtectedAllocator` demonstrates one consumer pattern that records a unique action hash and rejects reuse.
