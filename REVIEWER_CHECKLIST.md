# Verified reviewer checklist

The items below are supported by the repository tests, documented local verification, and recorded Studionet lifecycle evidence. Explorer links and transaction hashes are recorded even where the explorer detail service was unavailable during verification.

## Category fit

- [x] The submission is a standalone Intelligent Contract primitive, not a full app.
- [x] No frontend exists in the repository.
- [x] COMMONCAUSE is useful to other builders without product-specific UI or workflow assumptions.

## GenLayer necessity

- [x] The semantic step cannot be replaced by simple exact string matching without losing the common-cause property.
- [x] GenLayer is used to map public natural-language evidence onto a frozen risk-factor vocabulary.
- [x] The LLM does not perform deterministic exposure arithmetic.

## Consensus quality

- [x] Validators independently re-fetch public evidence.
- [x] Validators independently re-derive the material factor set.
- [x] Agreement checks substantive factor IDs and coverage class, not merely valid JSON shape.
- [x] Different material factor sets produce disagreement.
- [x] Explanatory wording can differ without changing the substantive verdict.

## Fail-closed behaviour

- [x] Ambiguous mappings cannot activate commitments.
- [x] Unregistered material dependencies cannot activate commitments.
- [x] Unavailable evidence cannot activate commitments.
- [x] A clear result with no factor is not accepted.

## State design

- [x] Factor ancestry is acyclic.
- [x] Child exposure rolls up to every ancestor exactly once.
- [x] A shared parent can block two otherwise different children.
- [x] Admission cannot exceed total book capacity.
- [x] Release decrements exactly the stored admission closure.
- [x] Factor exposure cannot underflow.
- [x] A factor with live exposure cannot retire.
- [x] A parent with active children cannot retire.
- [x] A cap cannot be lowered below current exposure.

## Composability

- [x] Each commitment has a stable mapping hash.
- [x] The book has a current state hash.
- [x] Another IC can query admission by mapping hash.
- [x] The optional consumer demonstrates replay protection.

## Evidence

- [x] Full Direct Mode suite passes.
- [x] Pickling checks pass where supported.
- [x] GenVM linter passes.
- [x] Main contract deploys and finalises on Studionet 61999.
- [x] Live demo proves child-safe/shared-parent-unsafe rejection.
- [x] Live demo proves release restores parent headroom.
- [x] Live demo proves an unregistered dependency fails closed.
- [x] Explorer links and transaction hashes are recorded.
- [x] README and submission claims do not exceed the live proof.
