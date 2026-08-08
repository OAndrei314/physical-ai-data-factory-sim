"""CLI for physical-AI scenario generation."""
from __future__ import annotations

import argparse

from .simulator import coverage_report, generate_scenarios


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="physical-ai-data-factory")
    parser.add_argument("--scenes", type=int, default=12)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args(argv)

    scenarios = generate_scenarios(args.scenes, seed=args.seed)
    report = coverage_report(scenarios)
    print(f"scenarios={int(report['scenario_count'])}")
    print(f"mean_risk={report['mean_risk']}")
    print(f"high_risk_fraction={report['high_risk_fraction']}")
    print(f"template_coverage={report['template_coverage']}")
    return 0
