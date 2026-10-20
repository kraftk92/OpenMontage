"""Offline persistence regressions; no providers, media generation, or pytest needed.

Evidence files here are sentinel bytes for checkpoint tests, not rendered-video
fixtures. Actual probe/playback quality remains a production acceptance check.
Run: .venv/bin/python -m unittest tests.lib.test_storyboard_sample_contract -v
"""

from __future__ import annotations

import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from jsonschema import ValidationError

from lib.checkpoint import (
    CheckpointValidationError, _stage_requires_approval, get_next_stage,
    get_pipeline_stages, init_project, read_checkpoint, write_checkpoint,
)
from lib.pipeline_loader import list_pipelines, load_pipeline
from lib.storyboard import sample_basis_digest
from schemas.artifacts import load_schema, validate_artifact


def storyboard() -> dict:
    return {
        "version": "1.1",
        "metadata": {
            "total_duration_seconds": 7,
            "references": [{"id": "r1", "url": "https://example.org/reference", "design_note": "Test reference only"}],
        },
        "scenes": [{
            "id": "s1", "type": "animation", "description": "An inquiry gets an owner.",
            "start_seconds": 0, "end_seconds": 7,
            "metadata": {"camera": "N/A", "overlays": []},
            "required_assets": [{
                "id": "a1", "type": "animation", "description": "Custom routing diagram",
                "source": "generate", "production_tool": "video_compose",
                "acceptance_criteria": ["Owner appears after inquiry"],
            }],
            "creative_spec": {
                "primary_subject": "Routing diagram", "on_screen_text": ["Who owns the next step?"],
                "reference_ids": ["r1"], "layout": "Left-to-right diagram with readable hold",
                "typography": {"font_family": "Arial", "size_px": 64, "weight": 600, "color": "#123456"},
                "motion_beats": [
                    {"start_seconds": 0, "end_seconds": 4, "action": "Assign inquiry", "easing": "ease-out"},
                    {"start_seconds": 4, "end_seconds": 7, "action": "Hold", "easing": "none"},
                ],
                "asset_ids": ["a1"], "acceptance_criteria": ["Owner is clear without narration"],
            },
        }],
    }


def planning_artifacts(pipeline: str) -> dict:
    research = {
        "version": "1.0", "topic": "Fixture", "research_date": "2026-10-20",
        "landscape": {
            "existing_content": [{"title": f"Fixture {i}", "source": "test", "angle": "test", "what_it_covers": "fixture"} for i in range(3)],
            "saturated_angles": [], "underserved_gaps": ["fixture"],
        },
        "data_points": [{"claim": "Fixture, not a researched fact", "source_url": "https://example.org", "credibility": "primary_source"} for _ in range(3)],
        "audience_insights": {"common_questions": ["A?", "B?", "C?"], "misconceptions": [], "knowledge_level": "fixture"},
        "angles_discovered": [{"name": f"Fixture {i}", "hook": "Test", "type": "evergreen", "why_now": "Fixture"} for i in range(3)],
        "sources": [{"url": "https://example.org", "title": "Fixture", "used_for": "test"} for _ in range(5)],
    }
    proposal = {
        "version": "1.0",
        "concept_options": [{
            "id": f"c{i}", "title": f"Direction {i}", "hook": "Next step?",
            "narrative_structure": "problem_solution", "visual_approach": "Fixture",
            "target_duration_seconds": 7, "why_this_works": "Fixture",
        } for i in range(2)],
        "selected_concept": {"concept_id": "c0", "rationale": "Test"},
        "production_plan": {"pipeline": pipeline, "render_runtime": "remotion", "composition_mode": "atelier", "stages": []},
        "cost_estimate": {"total_estimated_usd": 0, "line_items": [], "budget_verdict": "within_budget"},
        "approval": {"status": "approved"},
    }
    script = {"version": "1.0", "title": "Fixture", "total_duration_seconds": 7, "sections": [{"id": "s1", "text": "Who owns the next step?", "start_seconds": 0, "end_seconds": 7}]}
    return {"research": {"research_brief": research}, "proposal": {"proposal_packet": proposal}, "script": {"script": script}, "scene_plan": {"scene_plan": storyboard()}}


class StoryboardTests(unittest.TestCase):
    def test_complete_plan_and_legacy_plan_validate(self):
        validate_artifact("scene_plan", storyboard())
        validate_artifact("scene_plan", {"version": "1.0", "scenes": [{"id": "old", "type": "animation", "description": "Legacy", "start_seconds": 0, "end_seconds": 1}]})

    def test_structural_and_relational_failures(self):
        cases = []
        def broken(change):
            plan = storyboard()
            change(plan)
            cases.append(plan)
        broken(lambda p: p["scenes"][0].pop("creative_spec"))
        broken(lambda p: p["scenes"][0]["creative_spec"].pop("typography"))
        broken(lambda p: p["scenes"][0].update(end_seconds=0))
        broken(lambda p: p["scenes"][0].update(start_seconds=1))
        broken(lambda p: p["scenes"].append(copy.deepcopy(p["scenes"][0])))
        broken(lambda p: p["metadata"].update(total_duration_seconds=8))
        broken(lambda p: p["scenes"][0]["creative_spec"].update(asset_ids=["missing"]))
        broken(lambda p: p["scenes"][0]["creative_spec"].update(reference_ids=["missing"]))
        broken(lambda p: p["scenes"][0]["required_assets"][0].pop("production_tool"))
        broken(lambda p: p["scenes"][0]["creative_spec"]["motion_beats"][1].update(start_seconds=5))
        broken(lambda p: p["scenes"][0]["creative_spec"]["motion_beats"][1].update(end_seconds=8))
        broken(lambda p: p["scenes"][0]["creative_spec"]["motion_beats"][1].update(end_seconds=3))
        broken(lambda p: p["metadata"]["references"].append(copy.deepcopy(p["metadata"]["references"][0])))
        for i, plan in enumerate(cases):
            with self.subTest(case=i), self.assertRaises(ValidationError):
                validate_artifact("scene_plan", plan)

    def test_legacy_reversed_timing_rejected(self):
        with self.assertRaises(ValidationError):
            validate_artifact("scene_plan", {"version": "1.0", "scenes": [{"id": "old", "type": "animation", "description": "Bad", "start_seconds": 5, "end_seconds": 1}]})

    def test_approval_brief_has_complete_24_second_storyboard(self):
        path = Path(__file__).resolve().parents[2] / "docs/validation/inquiry-next-action.scene-plan.json"
        plan = json.loads(path.read_text())
        validate_artifact("scene_plan", plan)
        self.assertEqual(plan["metadata"]["total_duration_seconds"], 24)
        sample = next(scene for scene in plan["scenes"] if scene["id"] == "routing")
        self.assertEqual(sample["end_seconds"] - sample["start_seconds"], 7)

    def test_every_manifest_and_schema_loads(self):
        from jsonschema import Draft202012Validator
        from schemas.artifacts import list_schemas
        for name in list_schemas():
            Draft202012Validator.check_schema(load_schema(name))
        for name in list_pipelines():
            manifest = load_pipeline(name)
            self.assertEqual(get_pipeline_stages(name), [s["name"] for s in manifest["stages"]])
            for stage in manifest["stages"]:
                self.assertEqual(_stage_requires_approval(name, stage["name"]), stage.get("human_approval_default", False))
                if "skill" in stage:
                    self.assertTrue((Path(__file__).resolve().parents[2] / "skills" / (stage["skill"] + ".md")).is_file())


class SampleGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.pipeline = "animation"
        self.project = init_project("run", title="Fixture", pipeline_type=self.pipeline, pipeline_dir=self.root)
        self.planning = planning_artifacts(self.pipeline)
        for stage, artifacts in self.planning.items():
            self.write(stage, "completed", artifacts, human_approved=True)
        self.report = self.make_report()

    def write(self, stage, status, artifacts=None, **kwargs):
        return write_checkpoint(self.root, "run", stage, status, artifacts or {}, pipeline_type=self.pipeline, **kwargs)

    def make_report(self):
        for filename in ["sample.mp4", *[f"frame{i}.png" for i in range(4)]]:
            (self.project / filename).write_bytes(b"checkpoint-test sentinel, not media")
        return {
            "version": "1.0", "sample_path": "sample.mp4",
            "sample_sha256": hashlib.sha256((self.project / "sample.mp4").read_bytes()).hexdigest(),
            "duration_seconds": 7, "scene_ids": ["s1"],
            "basis_digest": sample_basis_digest(self.planning["scene_plan"]["scene_plan"], self.planning["script"]["script"], self.planning["proposal"]["proposal_packet"]),
            "render_runtime": "remotion", "composition_mode": "atelier",
            "review": {"frames_inspected": [f"frame{i}.png" for i in range(4)], "playback_reviewed": True, "checks": {name: "pass" for name in ["exact_copy", "readability", "visual_direction", "factual_accuracy", "meaningful_motion"]}, "unresolved_blockers": []},
        }

    def approve_sample(self):
        self.write("sample", "completed", {"sample_review": self.report}, human_approved=True)

    def test_gate_precedes_batches_in_both_manifests(self):
        for name in ("animation", "animated-explainer"):
            stages = get_pipeline_stages(name)
            self.assertEqual(stages[stages.index("scene_plan") + 1], "sample")
            self.assertEqual(stages[stages.index("sample") + 1], "assets")
            self.assertTrue(_stage_requires_approval(name, "sample"))
        self.assertEqual(get_next_stage(self.root, "run", self.pipeline), "sample")

    def test_missing_sample_blocks_entry_and_completion(self):
        for status in ["in_progress", "awaiting_human", "completed"]:
            with self.subTest(status=status), self.assertRaises(CheckpointValidationError):
                self.write("assets", status, {"asset_manifest": {"version": "1.0", "assets": []}}, human_approved=True)

    def test_awaiting_sample_does_not_authorize_batches(self):
        self.write("sample", "awaiting_human", {"sample_review": self.report})
        with self.assertRaises(CheckpointValidationError):
            self.write("assets", "in_progress")

    def test_sample_cannot_complete_without_explicit_approval(self):
        with self.assertRaisesRegex(CheckpointValidationError, "GATE VIOLATION"):
            self.write("sample", "completed", {"sample_review": self.report})

    def test_sample_requires_artifact_and_playback_review(self):
        with self.assertRaises(CheckpointValidationError):
            self.write("sample", "awaiting_human")
        self.report["review"]["playback_reviewed"] = False
        with self.assertRaises(CheckpointValidationError):
            self.write("sample", "awaiting_human", {"sample_review": self.report})

    def test_approved_sample_allows_batch_entry_and_is_archived(self):
        self.write("sample", "awaiting_human", {"sample_review": self.report})
        self.approve_sample()
        self.write("assets", "in_progress")
        self.assertTrue(list((self.project / "history").glob("checkpoint_sample_*.json")))
        self.assertTrue(read_checkpoint(self.root, "run", "sample")["human_approved"])

    def test_changed_script_invalidates_prior_approval(self):
        self.approve_sample()
        self.planning["script"]["script"]["sections"][0]["text"] = "Changed copy."
        self.write("script", "completed", self.planning["script"], human_approved=True)
        with self.assertRaisesRegex(CheckpointValidationError, "STALE SAMPLE"):
            self.write("assets", "in_progress")

    def test_changed_storyboard_or_production_plan_invalidates_sample(self):
        self.approve_sample()
        self.planning["scene_plan"]["scene_plan"]["scenes"][0]["creative_spec"]["layout"] = "Different treatment"
        self.write("scene_plan", "completed", self.planning["scene_plan"], human_approved=True)
        with self.assertRaisesRegex(CheckpointValidationError, "STALE SAMPLE"):
            self.write("assets", "in_progress")
        self.planning["scene_plan"]["scene_plan"] = storyboard()
        self.write("scene_plan", "completed", self.planning["scene_plan"], human_approved=True)
        self.planning["proposal"]["proposal_packet"]["production_plan"]["render_runtime"] = "hyperframes"
        self.write("proposal", "completed", self.planning["proposal"], human_approved=True)
        with self.assertRaisesRegex(CheckpointValidationError, "STALE SAMPLE"):
            self.write("assets", "in_progress")

    def test_missing_or_modified_evidence_invalidates_sample(self):
        self.approve_sample()
        (self.project / "frame0.png").unlink()
        with self.assertRaises(CheckpointValidationError):
            self.write("assets", "in_progress")
        (self.project / "frame0.png").write_bytes(b"fixture")
        (self.project / "sample.mp4").write_bytes(b"replaced clip")
        with self.assertRaisesRegex(CheckpointValidationError, "Sample clip changed"):
            self.write("assets", "in_progress")

    def test_sample_rejects_bad_duration_unknown_scene_runtime_or_blocker(self):
        for field, value in [("duration_seconds", 4), ("duration_seconds", 9), ("scene_ids", ["unknown"]), ("render_runtime", "hyperframes")]:
            report = copy.deepcopy(self.report)
            report[field] = value
            with self.subTest(field=field, value=value), self.assertRaises(CheckpointValidationError):
                self.write("sample", "awaiting_human", {"sample_review": report})
        self.report["review"]["unresolved_blockers"] = ["Unreadable copy"]
        with self.assertRaises(CheckpointValidationError):
            self.write("sample", "awaiting_human", {"sample_review": self.report})

    def test_new_storyboard_write_rejects_legacy_contract(self):
        self.planning["scene_plan"]["scene_plan"]["version"] = "1.0"
        with self.assertRaisesRegex(CheckpointValidationError, "Storyboard version"):
            self.write("scene_plan", "awaiting_human", self.planning["scene_plan"])

    def test_selected_visual_direction_change_invalidates_sample(self):
        self.approve_sample()
        self.planning["proposal"]["proposal_packet"]["concept_options"][0]["visual_approach"] = "Different visual world"
        self.write("proposal", "completed", self.planning["proposal"], human_approved=True)
        with self.assertRaisesRegex(CheckpointValidationError, "STALE SAMPLE"):
            self.write("assets", "in_progress")

    def test_proposal_rejects_unknown_selected_concept(self):
        proposal = self.planning["proposal"]["proposal_packet"]
        proposal["selected_concept"]["concept_id"] = "missing"
        with self.assertRaises(ValidationError):
            validate_artifact("proposal_packet", proposal)

    def test_evidence_outside_project_cannot_satisfy_gate(self):
        self.report["sample_path"] = "../outside.mp4"
        (self.root / "outside.mp4").write_bytes(b"fixture")
        with self.assertRaises(CheckpointValidationError):
            self.write("sample", "awaiting_human", {"sample_review": self.report})

    def test_sample_entry_requires_storyboard_approval(self):
        self.write("scene_plan", "awaiting_human", self.planning["scene_plan"])
        with self.assertRaises(CheckpointValidationError):
            self.write("sample", "in_progress")

    def test_failed_heartbeat_remains_available_for_diagnostics(self):
        self.write("assets", "failed")

    def test_short_approved_film_can_be_sampled_in_full(self):
        self.planning["script"]["script"]["total_duration_seconds"] = 3
        self.planning["script"]["script"]["sections"][0]["end_seconds"] = 3
        self.write("script", "completed", self.planning["script"], human_approved=True)
        plan = self.planning["scene_plan"]["scene_plan"]
        plan["metadata"]["total_duration_seconds"] = 3
        plan["scenes"][0]["end_seconds"] = 3
        plan["scenes"][0]["creative_spec"]["motion_beats"] = [{"start_seconds": 0, "end_seconds": 3, "action": "Short sequence", "easing": "none"}]
        self.write("scene_plan", "completed", self.planning["scene_plan"], human_approved=True)
        self.report = self.make_report()
        self.report["duration_seconds"] = 3
        self.approve_sample()
        self.write("assets", "in_progress")

    def test_storyboard_duration_must_match_approved_script(self):
        self.planning["script"]["script"]["total_duration_seconds"] = 8
        self.planning["script"]["script"]["sections"][0]["end_seconds"] = 8
        self.write("script", "completed", self.planning["script"], human_approved=True)
        with self.assertRaisesRegex(CheckpointValidationError, "approved script"):
            self.write("scene_plan", "awaiting_human", self.planning["scene_plan"])


if __name__ == "__main__":
    unittest.main()
