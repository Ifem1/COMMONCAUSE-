"""Direct Mode compatibility helpers."""
import os
import sys
import inspect
from pathlib import Path

import pytest
from gltest.direct import deploy_contract

if sys.platform == "win32":
    _unlink = os.unlink
    def _safe_unlink(path, *args, **kwargs):
        try:
            return _unlink(path, *args, **kwargs)
        except PermissionError:
            caller_files = [frame.filename.replace("\\", "/") for frame in inspect.stack()]
            if any(file.endswith("/gltest/direct/loader.py") for file in caller_files):
                return None
            raise
    os.unlink = _safe_unlink


@pytest.fixture
def direct_deploy(direct_vm):
    """Use the stable GenVM SDK matching the contract's pinned dependency.

    gltest otherwise picks the newest cached SDK bundle, which may be a
    prerelease even when the contract pins the stable Studionet runtime.
    """
    def _deploy(contract_path, *args, **kwargs):
        path = Path(contract_path)
        if not path.is_absolute():
            path = (Path.cwd() / path).resolve()
        return deploy_contract(path, direct_vm, *args, sdk_version="v0.2.16", **kwargs)

    return _deploy


@pytest.fixture(autouse=True)
def enable_direct_mode_pickling_checks(direct_vm):
    direct_vm.check_pickling = True
    yield
    # genlayer-test currently applies check_pickling to run_nondet but omits
    # run_nondet_unsafe, which COMMONCAUSE uses for validator consensus.
    # Check those captured closures explicitly so this suite still exercises
    # the serialization boundary for the production path.
    import cloudpickle

    for _, leader_fn, validator_fn in direct_vm._captured_validators:
        cloudpickle.dumps(leader_fn)
        cloudpickle.dumps(validator_fn)
