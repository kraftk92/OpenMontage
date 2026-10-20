# Taste Direction - Meta Skill

## When to Use

Use this before committing to visual identity, mood boards, proposal packets, custom playbooks, atelier composition, image reference batches, or brand-heavy videos.

This skill defines OpenMontage's video taste profile contract. Do not treat it as a frontend style recipe. The output is a compact video taste profile that travels through proposal, scene planning, asset prompts, edit, compose, and review.

## Output Contract

Write a `taste_profile` when the proposal or playbook needs a stronger creative contract:

```json
{
  "design_read": "Premium expert explainer: calm authority, high trust, low ornament.",
  "visual_variance": 4,
  "motion_intensity": 3,
  "information_density": 5,
  "palette_discipline": "Neutral base, one accent, no decorative gradients.",
  "layout_variation": "Alternate editorial split frames with data-forward full-frame scenes.",
  "reference_strategy": "One reference still per scene family before asset generation.",
  "anti_patterns": ["generic AI-purple gradient backgrounds"],
  "quality_gates": ["Every scene should carry the design read without explanatory labels."]
}
```

`visual_variance`, `motion_intensity`, and `information_density` are 1-10 integer dials:

| Dial | Low | Mid | High |
|------|-----|-----|------|
| `visual_variance` | Tight system, repeated grammar | Pattern with purposeful scene families | Each beat may use a distinct visual mode |
| `motion_intensity` | Calm holds, small transitions | Clear motion accents and reveals | Fast kinetic language, frequent directional changes |
| `information_density` | One idea per frame | Main idea plus support detail | Dense dashboards, diagrams, or layered callouts |

## Process

### 0. Collect brand assets and visual references up front

Do this before concept development or storyboard lock, not at final composition.
Inspect resources already in the workspace and the conversation first. Ask once
for the missing essentials, keeping the request compact:

- Brand source: website or brand guide, usable logo variants, fonts and any
  existing imagery/product captures. Identify required assets and usage constraints.
- Two or three visual references, with what the user likes about each: type,
  atmosphere, framing, illustration, motion, or pacing. Include dislikes when known.
- Intended audience and the single message the video should leave them with.

Do not ask again for supplied information or require a complete asset pack. When
the user has no references, find and inspect options, explain their relevant
traits, and recommend a direction. When only a website is supplied, inspect its
rendered appearance and representative sections; text extraction and a logo
download are insufficient. Record unavailable assets and obtain approval through
the proposal for any provisional fonts, assets, or intentionally unbranded look.
Do not silently substitute generic styling for missing brand inputs.

Record sources, local asset paths, reference frame/time cues, observations,
missing items, and user preferences in `proposal_packet.metadata.brand_intake`.
Translate them into a concrete **brand direction** in the existing
`production_plan.taste_profile` and `production_plan.art_direction`: typography
and hierarchy, palette and contrast, layout, imagery/material/atmosphere, and
motion/pacing. State what is carried over, adapted for video, or deliberately
omitted and why. Brand rules constrain the visual options; a logo is not the
entire direction. Carry the essential rules inline in the production plan, not
only as a path to a mutable document.

In `scene_plan.metadata.brand_direction`, retain the approved rules, referenced
asset paths/content hashes, and reference observations. This keeps the actual
brand direction inside the storyboard/sample basis. Unbranded work records that
choice explicitly. Each scene's acceptance criteria should name the applicable
rules, and the representative sample must visibly demonstrate them.

### 1. Make a Design Read

Before choosing a playbook or palette, state what the video needs to feel like and why. Tie it to the audience, promise, platform, and subject matter.

Good reads are specific:

- "Investor-facing AI launch: precise, restrained, and credible; avoid hype visuals."
- "Youth science short: bright, curious, and kinetic; make invisible physics feel tactile."
- "Security incident explainer: tense and surgical; high contrast, low ornament, readable evidence."

Weak reads are only adjectives:

- "modern and clean"
- "cinematic"
- "professional"

### 2. Set the Three Dials

Pick `visual_variance`, `motion_intensity`, and `information_density` before writing concepts. These numbers should explain later choices:

- High motion plus low information means short kinetic beats, not dense diagrams.
- Low motion plus high information means stable frames, chart builds, and long readable holds.
- High variance means scene families need stronger anchors: recurring type, palette, framing, or sound motif.

### 3. Choose a Style Path

Use the dials to pick one of three paths:

| Path | Use When | Artifact |
|------|----------|----------|
| Existing playbook | A preset honestly matches the read | `production_plan.playbook` |
| Custom playbook | The subject has its own visual world | generated `styles/<name>.yaml` with `taste_profile` |
| Atelier art direction | Hero work needs a one-off language | `production_plan.art_direction` plus `taste_profile` |

Do not let preset availability override the design read. If the content calls for a custom visual world, write the custom playbook or art direction.

### 4. Plan References

If the work uses AI image/video, mood boards, brand assets, or atelier composition, create a reference strategy:

- Use one reference still per scene family or major beat.
- Do not compress the whole direction into one mood board image.
- For brand/product work, complete the intake above before visual concepts;
  inspect a brand kit and references before sample assets or batch generation.
- For screen demos, inspect the real UI and write a redesign/audit note before styling overlays.

### 5. Carry the Profile Downstream

At proposal stage:

- Add `production_plan.taste_profile`.
- Log style/playbook selection in `decision_log`.
- Explain how the dials affect runtime, composition mode, and asset generation.

At scene planning:

- Vary layouts according to `visual_variance`.
- Keep on-screen text and callouts within `information_density`.
- Set transition families and camera movement from `motion_intensity`.

At assets:

- Include palette, texture, framing, and reference strategy in image/video prompts.
- Generate reference stills before full batches when the profile depends on visual nuance.

At edit/compose:

- Match hold times and cut rhythm to the motion dial.
- Avoid adding decorative overlays that violate the design read.

## Anti-Default Checklist

Flag these before moving forward:

- Generic AI-purple gradients or default corporate-blue visuals with no subject reason.
- Same transition on every cut when `visual_variance` is 4 or higher.
- Kinetic motion that makes narration harder to follow.
- Dense callouts when `information_density` is 4 or lower.
- Text-only slides unless the design read intentionally calls for typographic storytelling.
- Mood boards that look attractive but do not map to concrete scene families.
- Brand/product videos that never show or inspect the real brand/product surface.

## Review Hooks

Reviewer should check:

- Does `taste_profile.design_read` explain a real creative choice?
- Do scene plans and edits respect the three dials?
- Are anti-patterns actually avoided?
- Is the reference strategy present when AI images/video or atelier work depends on visual nuance?
- Could this video belong to any topic after replacing the title? If yes, the taste direction is too generic.
- With the logo, watermark, and end card hidden, do the sample's type, layout,
  imagery/atmosphere, and motion still reflect the approved brand direction?
  Record concrete reference-to-frame evidence; a cosmetic overlay does not pass.
