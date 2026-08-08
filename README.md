# physical-ai-data-factory-sim

Maintained by: codex-daily-routine

A deterministic research harness for designing synthetic validation scenarios for
physical AI systems. It turns a small set of scene templates into perturbation-heavy
test plans that can be used to reason about sim-to-real coverage before expensive lab
or field experiments.

## How It Works

```text
SceneTemplate + perturbation grid
    -> generate_scenarios(seed)
    -> evaluate_scenario()
    -> coverage_report()
```

The package is intentionally small and reproducible:

- deterministic scenario generation from a seed
- no network access
- no external datasets
- explicit coverage metrics for lighting, occlusion, friction, latency and sensor noise

## Quickstart

```powershell
pip install -r requirements-dev.txt
pip install -e .
python -m pytest -q
python -m physical_ai_data_factory --scenes 12 --seed 7
python -m physical_ai_data_factory --scenes 40 --seed 11 --json
```

## Status

MVP: deterministic scenario generation, risk scoring, coverage aggregation, lab-readiness
reporting and tests. Next steps: add richer scene fixtures for optical-module handling,
mobile robot inspection and automated lab validation cells.

## License

MIT - see [LICENSE](LICENSE).
