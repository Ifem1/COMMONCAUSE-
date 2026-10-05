# Strict reviewer checklist

Before submission, a reviewer should be able to answer **yes** to every item below.

## Category fit

- [ ] The submission is a standalone Intelligent Contract primitive, not a full app.
- [ ] No frontend exists in the repository.
- [ ] COMMONCAUSE is useful to other builders without product-specific UI or workflow assumptions.

## GenLayer necessity

- [ ] The semantic step cannot be replaced by simple exact string matching without losing the common-cause property.
- [ ] GenLayer is used to map public natural-language evidence onto a frozen risk-factor vocabulary.
- [ ] The LLM does not perform deterministic exposure arithmetic.

## Consensus quality

- [ ] Validators independently re-fetch public evidence.
- [ ] Validators independently re-derive the material factor set.
- [ ] Agreement checks substantive factor IDs and coverage class, not merely valid JSON shape.
- [ ] Different material factor sets produce disagreement.
- [ ] Explanatory wording can differ without changing the substantive verdict.

## Fail-closed behaviour

- [ ] Ambiguous mappings cannot activate commitments.
- [ ] Unregistered material dependencies cannot activate commitments.
- [ ] Unavailable evidence cannot activate commitments.
- [ ] A clear result with no factor is not accepted.

## State design

- [ ] Factor ancestry is acyclic.
- [ ] Child exposure rolls up to every ancestor exactly once.
- [ ] A shared parent can block two otherwise different children.
- [ ] Admission cannot exceed total book capacity.
- [ ] Release decrements exactly the stored admission closure.
- [ ] Factor exposure cannot underflow.
- [ ] A factor with live exposure cannot retire.
- [ ] A parent with active children cannot retire.
- [ ] A cap cannot be lowered below current exposure.

## Composability

- [ ] Each commitment has a stable mapping hash.
- [ ] The book has a current state hash.
- [ ] Another IC can query admission by mapping hash.
- [ ] The optional consumer demonstrates replay protection.

## Evidence

- [ ] Full Direct Mode suite passes.
- [ ] Pickling checks pass where supported.
- [ ] GenVM linter passes.
- [ ] Main contract deploys and finalises on Studionet 61999.
- [ ] Live demo proves child-safe/shared-parent-unsafe rejection.
- [ ] Live demo proves release restores parent headroom.
- [ ] Live demo proves an unregistered dependency fails closed.
- [ ] Explorer links and transaction hashes are recorded.
- [ ] README and submission claims do not exceed the live proof.
