from pathlib import Path
import py_compile

ROOT = Path(__file__).resolve().parents[1]

required = [
    "contracts/commoncause.py",
    "examples/protected_allocator.py",
    "README.md",
    "SUBMISSION.md",
    "DEPLOYMENT.md",
    "docs/ARCHITECTURE.md",
    "docs/THREAT_MODEL.md",
    "docs/LIVE_DEMO.md",
    "gltest.config.yaml",
]

for rel in required:
    path = ROOT / rel
    if not path.exists():
        raise SystemExit(f"missing required file: {rel}")

for rel in ("contracts/commoncause.py", "examples/protected_allocator.py"):
    py_compile.compile(str(ROOT / rel), doraise=True)

config = (ROOT / "gltest.config.yaml").read_text(encoding="utf-8")
if "https://studio.genlayer.com/api" not in config:
    raise SystemExit("Studionet RPC missing from gltest.config.yaml")

if (ROOT / "frontend").exists() or (ROOT / "package.json").exists():
    raise SystemExit("frontend scaffold unexpectedly present")

print("COMMONCAUSE preflight OK")
print("Target: Studionet chain ID 61999")
print("No frontend scaffold present")
