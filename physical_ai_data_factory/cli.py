"""CLI for physical-AI scenario generation."""
from __future__ import annotations

import argparse
import json

from .simulator import coverage_report, generate_scenarios, validation_readiness_report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="physical-ai-data-factory")
    parser.add_argument("--scenes", type=int, default=12)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--json", action="store_true", help="emit the validation-readiness report as JSON")
    args = parser.parse_args(argv)

    scenarios = generate_scenarios(args.scenes, seed=args.seed)
    readiness = validation_readiness_report(scenarios)
    if args.json:
        print(json.dumps(readiness, indent=2, sort_keys=True))
        return 0
    report = coverage_report(scenarios)
    print(f"decision={readiness['decision']}")
    print(f"scenarios={int(report['scenario_count'])}")
    print(f"mean_risk={report['mean_risk']}")
    print(f"high_risk_fraction={report['high_risk_fraction']}")
    print(f"template_coverage={report['template_coverage']}")
    print(f"stress_coverage={readiness['stress_coverage']}")
    return 0
