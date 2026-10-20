# Executable Storyboard Contract

Animation and animated-explainer use scene_plan version `1.1` for new planning
checkpoints. Older version `1.0` artifacts remain readable; they do not satisfy
the new sample gate. Other pipelines retain their current contract.

The agent owns reference discovery, exact copy, layout, type, motion, diagrams,
image prompts, capture choreography, and asset acquisition. Ask the user for
business facts, access, rights constraints, budget, and approval of concrete
work, not for the missing creative treatment or an entire asset pack. Collect
available brand assets and visual preferences up front per `taste-direction.md`;
when the user has no references, the agent finds and proposes them. Retain the
approved rules, asset paths/content hashes and reference observations in
`metadata.brand_direction`, and put applicable brand checks in each scene's
acceptance criteria. Record intentionally unbranded work explicitly.

## Per scene

Keep the canonical scene type vocabulary. Add `creative_spec` with:

- `primary_subject`: the subject and purpose of this scene;
- `on_screen_text`: exact strings, or `[]` when intentionally text-free;
- `reference_ids`: IDs from `metadata.references`, with a design observation for
  each cited reference (not permission to reproduce its artwork);
- `layout`: placement, scale, safe areas, and relationship between elements;
- `typography`: `font_family`, numeric `size_px`, numeric `weight`, hex `color`;
- `motion_beats`: scene-relative `start_seconds`, `end_seconds`, concrete `action`,
  and `easing`. Explicit holds cover the full scene. Concurrent actions may overlap;
- `asset_ids`: exactly the IDs in this scene's `required_assets`;
- `acceptance_criteria`: observable checks for copy, clarity, motion, and intent.

Each `required_assets` task includes the existing `type`, `description`, `source`,
plus `id`, `production_tool`, and `acceptance_criteria`. The tool path must be
feasible under preflight. Original SVG/React authoring is agent work; name its
render tool and explain the authoring path in the description. Do not call an
unconfigured generator feasible just because its adapter exists.

Put camera, separate overlays, and animation-mode notes in per-scene `metadata`.
Do not introduce unsupported root scene keys. Put total film duration and the
reference catalog under top-level `metadata.total_duration_seconds` and
`metadata.references` (`id`, `url`, `design_note`).

Validation rejects reversed timing, duplicate scene/reference IDs, gaps,
overlaps, unknown reference IDs, broken scene-to-asset links, and incomplete or
out-of-bounds motion timing. Planned silence/black holds are explicit scenes.
The schema validates completeness, not whether an artistic decision is good.

In atelier mode every scene needs its own primary subject and composition.
Reuse palette, typography, and engine knowledge; finished creative components
and stock scene templates remain off-limits. The sample gate validates the
hardest representative beat before the remaining assets are produced.
