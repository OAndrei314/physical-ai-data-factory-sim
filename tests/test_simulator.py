from physical_ai_data_factory import coverage_report, generate_scenarios, validation_readiness_report


def test_generation_is_deterministic():
    assert generate_scenarios(5, seed=42) == generate_scenarios(5, seed=42)


def test_coverage_report_detects_high_risk_scenarios():
    scenarios = generate_scenarios(30, seed=3)
    report = coverage_report(scenarios)

    assert report["scenario_count"] == 30.0
    assert 0.0 < report["mean_risk"] < 1.0
    assert report["template_coverage"] == 1.0
    assert report["high_risk_fraction"] >= 0.0


def test_validation_readiness_report_prioritizes_risky_lab_cases():
    scenarios = generate_scenarios(40, seed=11)
    report = validation_readiness_report(scenarios)

    assert report["decision"] in {"ready_for_lab", "expand_simulation"}
    assert 0.0 <= report["stress_coverage"] <= 1.0
    assert len(report["priority_scenarios"]) <= 5
    assert report["priority_scenarios"][0]["risk_score"] >= report["priority_scenarios"][-1]["risk_score"]
