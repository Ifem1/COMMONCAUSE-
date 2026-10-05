# COMMONCAUSE submission notes

COMMONCAUSE is a reusable GenLayer Intelligent Contract that limits common-cause concentration across commitments that appear diversified but share an upstream failure dependency.

GenLayer consensus maps each commitment and its bounded public evidence onto a frozen dependency-factor catalogue. The leader and validators independently derive the substantive material factor set, evidence coverage, and source availability. `AMBIGUOUS`, `UNREGISTERED`, and `UNAVAILABLE` outcomes fail closed. Deterministic contract logic then expands child factors through their parent hierarchy, deduplicates ancestors, and enforces portfolio capacity and factor caps.

This division preserves the trust boundary: consensus handles semantic evidence mapping; deterministic execution handles roll-up, arithmetic, admission, release, and hashes. The LLM cannot set caps, choose notionals, or decide whether exposure is acceptable.

The repository is intentionally contract-only, with no frontend. It includes a minimal `ProtectedAllocator` consumer that accepts an active COMMONCAUSE commitment only when the supplied mapping hash matches, and rejects replayed action hashes.

## Target and verified evidence

The target is **GenLayer Studionet, chain ID 61999**, RPC `https://studio.genlayer.com/api`. Local verification passed with 30 Direct Mode tests and closure-pickling checks enabled; both deployable contracts passed the current GenVM linter and SDK validation.

The corrected COMMONCAUSE deployment and ProtectedAllocator consumer were finalized on Studionet. The live lifecycle proved admission through one child factor, rejection of a different child because their shared parent cap would be exceeded, fail-closed handling of an unregistered dependency, release restoring parent headroom, and successful admission of a fresh commitment afterward. The consumer accepted an exact active mapping and rejected wrong mapping, blocked and released commitments, and reused action hashes. Transaction-level evidence is in [proof/README.md](proof/README.md).

The official explorer page did not retrieve transaction details during verification. The proof records finalized CLI receipt waits and state reads instead. Reliable per-path fee figures were unavailable from the stable Studionet tooling used, so no fees are claimed.

The guarantee is intentionally narrow: for the registered catalogue and supplied public evidence, validators agree on material dependencies and deterministic contract logic enforces the declared common-cause limits. COMMONCAUSE does not prove global evidence completeness, source authority, or that every hidden dependency has been discovered.
