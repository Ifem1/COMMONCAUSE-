from pathlib import Path

SRC = (Path(__file__).parents[1] / "contracts" / "commoncause.py").read_text(encoding="utf-8")


def test_contract_logic_is_network_agnostic():
    assert "studio.genlayer.com" not in SRC
    assert "chain_id" not in SRC


def test_consensus_rederives_material_decision():
    assert "run_nondet_unsafe" in SRC
    assert "derive_once()" in SRC
    assert 'leader["factor_ids"] == own["factor_ids"]' in SRC
    assert 'leader["source_statuses"] == own["source_statuses"]' in SRC


def test_model_cannot_decide_cap_or_admission():
    prompt = SRC[SRC.index("COMMONCAUSE / CLASSIFY MATERIAL DEPENDENCIES"):SRC.index("class CommonCause")]
    assert "Do not decide admission, diversification, caps, exposure" in prompt
    assert "_admission_check_explicit" in SRC


def test_exposure_rolls_to_ancestors():
    assert "_factor_closure" in SRC
    assert "parent_factor_id" in SRC


def test_fail_closed_coverage_states_exist():
    for marker in ("COVERAGE_AMBIGUOUS", "COVERAGE_UNREGISTERED", "COVERAGE_UNAVAILABLE"):
        assert marker in SRC
