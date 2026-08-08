"""Scenario generation and coverage scoring for physical-AI validation."""
from __future__ import annotations

import random
from dataclasses import dataclass
from statistics import mean


@dataclass(frozen=True)
class SceneTemplate:
    name: str
    nominal_distance_m: float
    object_count: int
    safety_margin_mm: float


@dataclass(frozen=True)
class Scenario:
    template: str
    lighting_lux: int
    occlusion_pct: float
    friction_scale: float
    sensor_noise_pct: float
    control_latency_ms: int
    risk_score: float


DEFAULT_TEMPLATES = (
    SceneTemplate("optical-module-handling", 0.42, 3, 12.0),
    SceneTemplate("rack-service-inspection", 1.8, 9, 35.0),
    SceneTemplate("lab-cart-navigation", 3.2, 14, 55.0),
)


def generate_scenarios(
    count: int,
    seed: int = 0,
    templates: tuple[SceneTemplate, ...] = DEFAULT_TEMPLATES,
) -> list[Scenario]:
    """Generate deterministic perturbation scenarios."""
    if count <= 0:
        return []
    rng = random.Random(seed)
    scenarios: list[Scenario] = []
    for index in range(count):
        template = templates[index % len(templates)]
        lighting_lux = rng.choice((80, 150, 300, 650, 1200))
        occlusion_pct = rng.choice((0.0, 0.05, 0.15, 0.3, 0.45))
        friction_scale = rng.choice((0.65, 0.8, 1.0, 1.2))
        sensor_noise_pct = rng.choice((0.5, 1.0, 2.5, 5.0, 8.0))
        control_latency_ms = rng.choice((5, 15, 35, 70, 120))
        scenarios.append(
            Scenario(
                template=template.name,
                lighting_lux=lighting_lux,
                occlusion_pct=occlusion_pct,
                friction_scale=friction_scale,
                sensor_noise_pct=sensor_noise_pct,
                control_latency_ms=control_latency_ms,
                risk_score=_risk_score(template, lighting_lux, occlusion_pct, friction_scale, sensor_noise_pct, control_latency_ms),
            )
        )
    return scenarios


def coverage_report(scenarios: list[Scenario]) -> dict[str, float]:
    if not scenarios:
        return {"scenario_count": 0.0, "mean_risk": 0.0, "high_risk_fraction": 0.0, "template_coverage": 0.0}
    templates = {scenario.template for scenario in scenarios}
    high_risk = [scenario for scenario in scenarios if scenario.risk_score >= 0.65]
    return {
        "scenario_count": float(len(scenarios)),
        "mean_risk": round(mean(scenario.risk_score for scenario in scenarios), 3),
        "high_risk_fraction": round(len(high_risk) / len(scenarios), 3),
        "template_coverage": round(len(templates) / len(DEFAULT_TEMPLATES), 3),
    }


def _risk_score(
    template: SceneTemplate,
    lighting_lux: int,
    occlusion_pct: float,
    friction_scale: float,
    sensor_noise_pct: float,
    control_latency_ms: int,
) -> float:
    low_light = max(0.0, (300 - lighting_lux) / 300)
    friction_penalty = abs(1.0 - friction_scale)
    latency_penalty = min(1.0, control_latency_ms / 120)
    margin_penalty = max(0.0, (30.0 - template.safety_margin_mm) / 30.0)
    score = (
        0.24 * low_light
        + 0.25 * occlusion_pct / 0.45
        + 0.16 * friction_penalty / 0.35
        + 0.15 * sensor_noise_pct / 8.0
        + 0.12 * latency_penalty
        + 0.08 * margin_penalty
    )
    return round(min(1.0, score), 3)
