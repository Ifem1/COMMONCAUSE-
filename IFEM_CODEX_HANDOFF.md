# Ifem → Codex handoff

Unzip the COMMONCAUSE ZIP locally yourself, open the extracted `commoncause` folder in Codex, and send Codex the instruction below.

---

Continue COMMONCAUSE from the repository already open in this Codex workspace.

Do not restart it, scaffold a replacement, rename the primitive, convert it into a full app, add a frontend, or replace the architecture with a simpler demo. Treat the existing repository as the near-final standalone GenLayer Intelligent Contract submission.

The intended future repository is `Ifem1/commoncause`. I will create that GitHub repository separately. Work only in the extracted local repository for now and prepare it so I can push it to `Ifem1/commoncause` afterwards.

COMMONCAUSE is a reusable common-cause exposure guard. GenLayer consensus maps a commitment and public evidence onto a frozen dependency-factor catalogue. Deterministic logic then rolls child factors into parents and enforces book capacity and factor exposure caps. Keep that trust boundary intact.

Network requirement is strict:

- GenLayer Studionet
- chain ID 61999
- RPC `https://studio.genlayer.com/api`
- use the `studionet` network definition

Do not change the target network.

Finish the repository in place:

1. Inspect every file and the current official GenLayer documentation before modifying runtime-specific syntax.
2. Install the current stable Studionet-compatible GenLayer CLI/test/linter tooling. Do not introduce release-candidate tooling intended for another Studio environment.
3. Run `python scripts/preflight.py`.
4. Run the complete Direct Mode test suite with pickling checks enabled where supported.
5. Fix every real contract, type, storage, event, web-access, nondeterministic-execution, timestamp, serialization or Direct Mode issue you find. Preserve the protocol semantics while fixing implementation issues.
6. Add or strengthen tests until the important invariants are directly proven, especially:
   - independent validator re-derivation of factor sets;
   - disagreement when a validator sees a materially different dependency mapping;
   - fail-closed ambiguous, unregistered and unavailable evidence;
   - ancestor roll-up and duplicate-ancestor deduplication;
   - child-safe but parent-unsafe common-cause rejection;
   - book-capacity rejection;
   - release symmetry and exposure conservation;
   - retirement and cap-update safety;
   - mapping-hash and state-hash behaviour;
   - malicious prompt-injection content treated as untrusted data.
7. Run the current GenVM linter and fix all genuine findings.
8. Verify there is no frontend and do not add one. This is an Intelligent Contracts submission, not a Project submission.
9. Review `examples/protected_allocator.py`. Keep it minimal. Its purpose is only to prove a second Intelligent Contract can consume COMMONCAUSE admission. Fix its interface/runtime syntax if current stable Studionet tooling requires changes.
10. Exercise COMMONCAUSE against Studionet 61999 as far as available GEN and credentials allow. Use `docs/LIVE_DEMO.md` as the intended reviewer lifecycle.
11. Deploy the main contract first. Record the final address, deploy transaction, explorer link and finalization evidence.
12. Create a real risk book with a parent factor and at least two different child factors. Use stable public evidence and prove:
    - commitment A admitted through child A;
    - commitment B mapped to child B but blocked because their shared parent cap would be exceeded;
    - an unregistered material dependency fails closed;
    - releasing A restores the parent headroom;
    - a fresh commitment can then be admitted if all caps permit.
13. If feasible on the current stable Studionet runtime, deploy and exercise `ProtectedAllocator` against the live COMMONCAUSE contract and prove exact mapping acceptance, wrong mapping rejection, blocked/released commitment rejection and action replay protection.
14. Measure representative fee paths using the current supported Studionet tooling. Include at least deployment, factor registration, a clear admitted commitment, a blocked commitment and release. Do not invent fee numbers.
15. Update `proof/README.md`, `DEPLOYMENT.md`, `README.md` and `SUBMISSION.md` with only facts actually proven by the final runs.
16. Perform a hostile final review as if you were a strict GenLayer reviewer. Specifically look for any place where the leader can control a substantive dependency decision without validators independently reproducing it, any path where ambiguity can activate exposure, any cap arithmetic issue, any hierarchy bypass, any hidden mutable trust assumption, and any claim in the documentation stronger than the code proves.
17. Run the full test suite and linter one final time after all edits.
18. Leave the repository clean and ready for me to push to `Ifem1/commoncause`.

Do not fabricate deployment evidence, test counts, transaction hashes, fees or successful Studionet behaviour. If a live step cannot be completed, document the exact blocker and leave that field clearly marked as pending rather than claiming success.

Do not add a frontend.
---
