"""Storyboard contract checks and stable sample provenance (no creative policy)."""

from __future__ import annotations

import hashlib
import json
import math
from typing import Any

from jsonschema import ValidationError


def sample_basis_digest(scene_plan: dict, script: dict, proposal_packet: dict) -> str:
    """Bind a sample to the approved story and production choices, not user notes."""
    basis = {
        "scene_plan": scene_plan,
        "script": script,
        "production_plan": proposal_packet["production_plan"],
        "selected_concept": proposal_packet["selected_concept"],
        "selected_direction": next(
            concept for concept in proposal_packet["concept_options"]
            if concept["id"] == proposal_packet["selected_concept"]["concept_id"]
        ),
    }
    return hashlib.sha256(
        json.dumps(basis, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    ).hexdigest()


def validate_scene_plan(data: dict[str, Any]) -> None:
    """Check relational constraints JSON Schema cannot express; preserve v1.0 reads."""
    scene_ids: set[str] = set()
    cursor = 0.0
    detailed = data["version"] == "1.1"
    references = data.get("metadata", {}).get("references", []) if detailed else []
    reference_ids = {ref["id"] for ref in references}
    if detailed and len(reference_ids) != len(references):
        raise ValidationError("Storyboard reference IDs must be unique")
    for scene in data["scenes"]:
        start, end = scene["start_seconds"], scene["end_seconds"]
        if not (math.isfinite(start) and math.isfinite(end)) or end <= start:
            raise ValidationError(f"Scene {scene['id']}: end must be after start")
        if scene["id"] in scene_ids:
            raise ValidationError(f"Duplicate scene ID: {scene['id']}")
        scene_ids.add(scene["id"])
        if not detailed:
            continue
        if not math.isclose(start, cursor, abs_tol=1e-6):
            raise ValidationError(f"Scene {scene['id']}: timeline gap or overlap")
        cursor = end
        spec = scene["creative_spec"]
        assets = scene["required_assets"]
        asset_ids = {asset["id"] for asset in assets}
        if len(asset_ids) != len(assets) or set(spec["asset_ids"]) != asset_ids:
            raise ValidationError(f"Scene {scene['id']}: asset IDs must match required_assets uniquely")
        if not set(spec["reference_ids"]) <= reference_ids:
            raise ValidationError(f"Scene {scene['id']}: unknown reference ID")
        covered = 0.0
        for beat in sorted(spec["motion_beats"], key=lambda item: item["start_seconds"]):
            a, b = beat["start_seconds"], beat["end_seconds"]
            if not (math.isfinite(a) and math.isfinite(b)) or b <= a or b > end - start + 1e-6:
                raise ValidationError(f"Scene {scene['id']}: motion beat outside scene or reversed")
            if a > covered + 1e-6:
                raise ValidationError(f"Scene {scene['id']}: motion beats must include holds without gaps")
            covered = max(covered, b)
        if not math.isclose(covered, end - start, abs_tol=1e-6):
            raise ValidationError(f"Scene {scene['id']}: motion beats must cover full scene")
    if detailed:
        total = data["metadata"]["total_duration_seconds"]
        if not math.isfinite(total) or not math.isclose(cursor, total, abs_tol=1e-6):
            raise ValidationError("Storyboard must cover total_duration_seconds exactly")
