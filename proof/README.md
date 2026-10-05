# Verified Studionet 61999 evidence

Evidence below comes from GenLayer CLI reads and `genlayer receipt` waits against the configured `studionet` network. The corrected deployment and listed lifecycle transactions reached `FINALIZED`; state reads were made from the final contract address.

## Toolchain and local verification

```text
Network alias: studionet
Chain ID: 61999
RPC: https://studio.genlayer.com/api
GenLayer CLI: 0.39.1 (stable)
genlayer-test: 0.29.2
genvm-linter: 0.11.0
Direct Mode: 30 passed; pickling checks enabled
Preflight: passed
GenVM lint + SDK validation: passed for both contracts
```

The Direct Mode fixture pins the stable GenVM SDK selected by the contract dependency. The current `gltest` Direct Mode patch does not apply its `check_pickling` flag to `run_nondet_unsafe`; the test fixture explicitly cloudpickles both captured closures after each test.

## COMMONCAUSE deployment

The first deployment was finalized, but a live CLI submission exposed that the stable CLI preserves JSON string quoting for string ABI arguments. The first manifest proposal rolled back with `EXPECTED: evidence manifest must contain 1..4 URLs`. The parser was updated to accept both the documented raw JSON array string and the CLI’s quoted-string form, retested, and redeployed. The first deployment is superseded; the corrected deployment below is the one used for the lifecycle proof.

```text
Corrected contract address: 0x3b2Bb3373B1c2d709aceF5744bEA8aae1EdFB012
Deploy transaction: 0xc25ffde08c63bbe303728dc695eea5b17586acc19b980bd01afc6759c71f75f8
Finalized: YES
Consensus: 5 of 5 validators agreed
Deployment workspace Git metadata: unavailable at deployment time
Source file SHA-256: f1fafc01909788cbc4d29e9986cb76f11b8c8ae7166d5a420b064ee6c4c86f57
```

The deployment workspace was an extracted copy without `.git`, so no deployment-time Git commit SHA is asserted. The deployed contract source is pinned by the SHA-256 above; the repository's current `contracts/commoncause.py` is retained with that same source checksum.

Explorer links:

- [Studionet explorer transaction](https://explorer-studio.genlayer.com/tx/0xc25ffde08c63bbe303728dc695eea5b17586acc19b980bd01afc6759c71f75f8)
- Configured CLI explorer base: https://genlayer-explorer.vercel.app (returned Vercel `503 DEPLOYMENT_PAUSED` during this run)

The official `explorer-studio.genlayer.com` page loaded but returned “Failed to fetch transaction” for this transaction at verification time. The finalization evidence is therefore the successful CLI receipt wait and the matching final-state reads, rather than an explorer detail panel.

## Risk book and factors

```text
Risk book ID: 1
Capacity: 1000 risk_units
Initial factor catalogue hash: 52fd995c63d311726b976c478f77ad64bc758a6a100af90622bd80d13a320011
Final state hash: 238193dd2466a2480cf64969bfa243e2ce1e441d02941a8b523f859d3feb2109
Final total active: 260
Final active commitments: 1
Final blocked commitments: 2
Final released commitments: 1
```

| Factor | ID | Parent | Cap | Final exposure | Final headroom |
|---|---:|---:|---:|---:|---:|
| AWS | 1 | — | 5000 bps / 500 | 260 | 240 |
| AWS us-east-1 | 2 | 1 | 3000 bps / 300 | 0 | 300 |
| AWS eu-west-1 | 3 | 1 | 3000 bps / 300 | 260 | 40 |

Public evidence used for the AWS region classifications: [AWS Regions](https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions.html). The unregistered Azure scenario used [Microsoft Learn: List of Azure regions](https://learn.microsoft.com/en-us/azure/reliability/regions-list).

## Finalized live lifecycle transactions

| Scenario | Commitment | Transaction | Final result |
|---|---:|---|---|
| Create risk book | 1 | `0x142546846116de5dd929734dc651ade05bf45f819ba714cac1aaecb6ff8173bd` | Finalized |
| Register AWS parent | — | `0x5f44e9329fc38fdd454f8e1ca1ce7cda78bb2797efc2d25650b494f10ab726fa` | Finalized |
| Register us-east-1 child | — | `0xfc7fe5f06e87ea361599c891886536ddd0db69d306c3a6681ecd54437b4c9fbe` | Finalized |
| Register eu-west-1 child | — | `0xc8bd41e9f79b78112813078acd11083c88496262ea1618a4669a9808ed47aa3a` | Finalized |
| Commitment A admitted, 250 units on factor 2 | 1 | `0x79cc4e09d6ea1b7a5fe531170ccc8fdbd43db60d40c2ae4886e9625b3b75bba1` | `ACTIVE`, `CLEAR` |
| Commitment B, 260 units on distinct factor 3 | 2 | `0x81713e2bf9eb5c0e1aa4dfce29631393350b2490105fa68df3dd82c0260f4cd1` | `BLOCKED`, `FACTOR_CAP`, blocker factor 1 |
| Azure dependency absent from catalogue | 3 | `0x9cf1752a613e2829be4f2311119e34752ddd4fd55dc227d840fcdc4f22d2362d` | `BLOCKED`, `UNREGISTERED` |
| Release commitment A | 1 | `0x828e371d2e95c9eb6711bca85b0307778fccad770a247f86a233206643a0a11c` | `RELEASED`; parent and child A exposure returned to zero |
| Fresh eu-west-1 commitment admitted | 4 | `0x60b4bc44bfdb39718afcc2853878acda01e805bec084e7745545d86437cd40aa` | `ACTIVE`, `CLEAR`; 260 units at child B and parent |

Mapping hashes:

```text
Commitment 1 (A, active then released): b385dfca1d99a261d4c255ba407cf33cb27231a94ad4379cb9a5c37c802ea60b
Commitment 2 (B, blocked at shared parent): ab56b00d42d831dd5229ec163f902945d1d6312424d6c92176db19ee97e83a14
Commitment 3 (Azure, UNREGISTERED): ec3379f71197fd9edd97d5c4c066081c9cb9e6ba48614ee76671f378f472314d
Commitment 4 (fresh B, admitted after release): 207eef0f4d85f94a8b3e576c39d44d2f1931dfdb76fe91f3ca650d3aba440755
```

Observed state hashes:

```text
After A admission: 41fc21b27756441d631872d5579411cedb57a1a80c3e81ba8014a49441c4cbd4
After B blocked at parent: 1e19d25dab8fe7e70eacb12b03ace3afb21c673259801fc266bf44a60fa75e5e
After Azure blocked UNREGISTERED: 4cf39d536c44149191cda0b914771cdae6600e02f254f599fb8cae847e19f234
Final after release and fresh B admission: 238193dd2466a2480cf64969bfa243e2ce1e441d02941a8b523f859d3feb2109
```

## ProtectedAllocator consumer

```text
Address: 0x5E85a1E1ecE5aaD189fa2C7bBd23E8b6656166dF
Deploy transaction: 0xce5315fc26477f3c67909f08b1eb95eddcfe802429e2f1db7fb062cf85c0c792
Finalized: YES
```

| Check | Transaction | Finalized execution |
|---|---|---|
| Exact admitted mapping accepted | `0xaa4964792aca9936937e8233c1bfbdfad690039af65c51684c9259e21cfb48d9` | Success; allocation 1 recorded for commitment 4 |
| Wrong mapping rejected | `0x0126fd3dcb39c7cdcf99c9f145f1368e6c7fde55c5843737224fcdeb14699e65` | Rollback: CommonCause commitment is not admitted |
| Blocked commitment rejected | `0x6f9e1d339384f8f7c92c6f82a6236ac908c5ebf12eb136b863c7159ceeca5315` | Rollback: CommonCause commitment is not admitted |
| Released commitment rejected | `0xb408c24560861922bbf9f237fa8953213b083730a4732a41e72035ef431083f7` | Rollback: CommonCause commitment is not admitted |
| Reused action hash rejected | `0x542ebbe840bb0f38106ee6f4519f7f90cf451fd8f3e95e95ed7856e0d6f66d58` | Rollback: action already consumed |
| Uppercase reused action hash rejected | `0xb4d0d2c1831e3aa07db9baf28fe51ac53b2ce687511f16e78265dc1ef5ace6fd` | Rollback after lowercase normalization |

## Fee measurement status

Fee values are pending. The stable Studionet CLI 0.39.1 and installed `genlayer-py` 0.16.3 did not expose fee-estimation commands or per-transaction paid-fee fields for this stable network. The v0.6 fee-profile tooling documented for Studio-dev belongs to the v0.40 / v0.19 release-candidate stack on chain 61997, which is outside this task’s strict Studionet 61999 target. The wallet balance read as `1009.809 GEN` both before and after the run at three-decimal display precision; that rounded account balance cannot attribute fees to individual paths and is not reported as a fee measurement.

The deployment, factor-registration, admitted, blocked and release transactions above are real finalized paths; no per-path fee amount is claimed.

## Superseded first-deployment trial

```text
Address: 0x7f9E9A92fd48858a36cFCD80815A24FCF67ae64f
Deploy tx: 0x54cf8fb705780407922f5db82cbe9c00793665490883d2a3d3ef928f4ae95fe7 (FINALIZED)
Manifest proposal tx: 0x7dfffe290285fd12ead42a89cb8827910b268cce7a0cbacac292b325614236ce (FINALIZED rollback)
Reason: CLI JSON string argument was not unwrapped; corrected and redeployed at the address above.
```

No evidence from that superseded instance is counted in the successful live lifecycle.
