from matrix.config import DEPARTMENTS, proposed_departments


def test_nine_departments_and_evolution_is_last():
    assert len(DEPARTMENTS) == 9
    assert DEPARTMENTS[-1] == "evolution"
    assert "evaluation" not in DEPARTMENTS


def test_routing():
    assert proposed_departments("launch a service") == ["concept", "design", "marketing", "sales"]
    assert proposed_departments("Build an app") == ["concept", "design", "development", "qa_qc"]
    assert proposed_departments("Train and improve the Brain") == ["evolution"]
