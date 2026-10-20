# Representative Visual Sample Director

Use for the top-level `sample` stage in animation and animated-explainer.
It runs after approved script and storyboard, before batch assets, whether or
not the user supplied a reference video. This replaces their old conditional
proposal sample. The manifest and checkpoint approval gate are binding.

## Scope and authority

1. Write the sample `in_progress` checkpoint BEFORE producing anything. It
   requires all planning predecessors to be completed and approved.
2. Read the approved proposal, script, scene_plan v1.1, taste direction, and
   the selected tool's Layer 2/3 skills. Respect the approved runtime, authoring
   mode, providers, audio plan, and spend cap. No unilateral substitutions.
3. Select a representative 5–8 second sequence (or the full film if the approved
   film is shorter than 5 seconds) with a meaningful transformation
   and a readable hold. State which scene IDs it demonstrates and why. If the
   approved film cannot support that scope, revise the plan with the user first.
4. Acquire/create ONLY the assets needed for this sequence. Use actual intended
   art, type, diagrams, captures, and approved audio, not generic placeholders.
   An explicitly text-led brief needs neither TTS nor a music track.
5. In atelier mode hand-author only the sample's scene(s); reuse mechanics and
   design rules, not finished scene templates. The sample is a bounded exception
   to the usual assets-before-compose ordering. It does not authorize the full
   composition or a batch. Keep sources and outputs in the project workspace.

## Demonstrate the approved brand direction

Before authoring, read `proposal_packet.metadata.brand_intake`, the approved
production-plan taste/art direction, and `scene_plan.metadata.brand_direction`.
Resolve missing intake through `skills/meta/taste-direction.md` before building
the sample. Do not defer branding until the rest of the video is rendered.

Choose a sequence that proves both the motion treatment and the visual direction.
Use the intended brand assets and approved typography, hierarchy, palette,
composition, imagery/atmosphere, and motion. Record any approved adaptations or
provisional assets. A generic scene with a logo, gold rule, watermark, or branded
end card does not demonstrate a brand-led treatment.

During frame/playback review, compare the sample with the inspected references.
In `sample_review.review.notes`, record **brand direction evidence**: source and
approved trait -> actual frame/time and implementation -> pass or mismatch.
Cover the applicable visual rules and explain any intentionally omitted traits.
Check the core scene with logo/finishing overlays hidden conceptually: the
reference-derived design must still be evident. For intentionally unbranded work,
record that approved choice instead of inventing brand evidence.

A material mismatch is a blocker under `checks.visual_direction`, even when the
encode, copy, and motion pass. Revise the sample before batch assets or the full
composition; full-run authority never turns a failed direction check into a pass.
Present the clip with the reference comparisons so sample approval covers the
actual brand treatment.

If brand assets or visual direction arrive/change after sample approval, update
the canonical planning basis and render/review a revised representative sample
under the normal approval policy before continuing. Do not preserve a stale
basis by labeling material art-direction changes as supplemental finishing.

## Render and inspect

- Render through `video_compose` using the approved runtime and authoring mode.
  Its output is the 5–8 second sample, never the full film. Save sample-specific
  edit decisions and the partial asset manifest under `artifacts/sample/` so
  they cannot overwrite the later full-run artifacts.
- Probe the real output with ffprobe. Verify 5–8 seconds, target aspect ratio,
  intended resolution/fps, valid container, and the approved audio architecture.
- Extract and actually inspect at least four representative frames. Play back
  the sample to assess motion, timing, readable holds, and audio where applicable.
  If playback cannot be reviewed, record the blocker; do not claim a pass.
- Check exact copy, readability, visual direction/coherence, factual accuracy,
  and meaningful motion against each scene's `creative_spec.acceptance_criteria`.
  A successful encode or extracted frames alone do not establish visual quality.
- Fix blockers within the approved scope. After two unsuccessful review rounds,
  record a failed checkpoint and present concrete options; do not pass blockers
  with warnings or batch ahead to hide them.

## Persist and stop

Write a schema-valid `sample_review` to `artifacts/sample_review.json` with:

- `version: "1.0"`, project-relative `sample_path`, its `sample_sha256` file hash,
  measured `duration_seconds`,
  representative `scene_ids`, approved `render_runtime` and `composition_mode`;
- `basis_digest` from
  `lib.storyboard.sample_basis_digest(scene_plan, script, proposal_packet)` using
  the approved checkpoint payloads, not a separate draft on disk;
- `review.frames_inspected` with project-relative paths to the four real images,
  `playback_reviewed: true`, all five `checks: "pass"`, no unresolved blockers,
  and notes recording probe results and the visual/playback observations.

Checkpoint `sample` as `awaiting_human` with `{"sample_review": report}`. Present
the actual clip, scene IDs, review findings, and spend. END YOUR TURN and wait for
explicit sample approval. Only then write `completed, human_approved=True`.

Batch `assets` cannot even enter `in_progress` until this approved checkpoint
exists. The writer verifies that the clip/frame files still exist and the basis
digest matches the current approved script, storyboard, and production plan.
Changing that basis requires another sample and approval. There is no skip flag.
File existence and recorded checks are persistence safeguards; they are not
automated proof of aesthetics or truthful human approval.
