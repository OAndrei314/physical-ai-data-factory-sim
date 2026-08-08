from physical_ai_data_factory import coverage_report, generate_scenarios


def test_generation_is_deterministic():
    assert generate_scenarios(5, seed=42) == generate_scenarios(5, seed=42)


def test_coverage_report_detects_high_risk_scenarios():
    scenarios = generate_scenarios(30, seed=3)
    report = coverage_report(scenarios)

    assert report["scenario_count"] == 30.0
    assert 0.0 < report["mean_risk"] < 1.0
    assert report["template_coverage"] == 1.0
    assert report["high_risk_fraction"] >= 0.0
