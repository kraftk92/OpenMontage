# Inquiry next action validation brief

Historical planning fixture from the first unbranded lab validation. The status
and approval request below describe that planning checkpoint, not current project
state. This is not an intake template: new videos must follow the brand-asset and
visual-reference intake in `skills/meta/taste-direction.md` and demonstrate the
approved direction in their representative sample.

Status: draft for Kyle's approval. This is a planning document, not an active
production. No project, production checkpoint, artwork, or composition has been
created. Approving this brief authorizes planning through the approved storyboard
and its seven-second sample only; remaining assets and the final film require
sample approval. No paid services are authorized.

Create a 24-second visual explainer for a small service-business owner:
**Every new inquiry needs a clear next action.** The example is fictional and
makes no claims about revenue, conversion rates, or a real product's features.
The agent supplies references, script, diagrams, artwork, typography, and motion.
Kyle approves the treatment and factual accuracy rather than supplying assets.

## Two visual directions

| Direction | Visual treatment | Motion | Tradeoff |
|---|---|---|---|
| A — Editorial case file | Warm paper `#F1E8D6`, charcoal `#252722`, burnt-orange `#B94F2D`; Georgia headings with Arial labels. Inquiry as a purpose-drawn paper document, then an editorial diagram and a separate work record. | Measured document movement, restrained label reveals, long readable holds. | Tactile and approachable, but needs disciplined composition to avoid becoming repeated document cards. |
| B — Routing diagram | Off-white `#F4F3ED`, ink `#1D2927`, one green accent `#23785B`, muted lines `#AABBB5`; Arial headings/labels. Four different subjects: inquiry illustration, owner/action diagram, illustrative work record, closing type. | Clear cause and effect, one focal action at a time, an active line following the inquiry, then an explicit settled hold. | Less atmospheric; stronger evidence that motion itself explains the idea. |

**Recommend B.** It gives the first validation a meaningful transformation with
assets the agent can author locally. The diagram is the main subject only in
scene 2. It does not become a repeated visual scaffold for every scene.

Reference sources were read and their relevant visual examples inspected on
October 20, 2026. These are principles and composition references, not licensed
production assets or designs to reproduce:

- A1: [Stripe Press — Scaling People cover process](https://stripepress.substack.com/p/behind-the-cover-scaling-people-by).
  Cue: the three material/color cover tests. Natural paper and geometric marks
  make an operational subject feel physical. Borrow material restraint and
  hierarchy; do not copy the cover illustration or its arrangement.
- A2: [IBM flat illustration usage](https://www.ibm.com/design/language/illustration/flat-style/usage/).
  Cue: the editorial spread under “Examples in use.” A single strong illustration
  and separate text area suggest the case-file direction's editorial framing.
- B1: [IBM animation tips and techniques](https://www.ibm.com/design/language/animation/tips-and-techniques/).
  Cues: Focus, Rhythm, and Type/Presentation. Apply the documented transfer of
  attention, staggered cause and effect, and readable rest. Recheck the relevant
  animated examples during motion authoring; only still examples were visually
  inspected for this approval brief.
- B2: [IBM flat illustration usage](https://www.ibm.com/design/language/illustration/flat-style/usage/).
  Cue: the application example with a directional route. Use simple geometric
  forms and a clear path; avoid the reference's color treatment and artwork.

## Delivery and tool choices

- Pipeline: `animation` 2.1. Authoring: **atelier**, a fresh project-local React
  composition. Reuse engine knowledge and the approved design rules, not stock
  scene components. This costs more agent iteration than a templated assembly.
- Recommend **Remotion**: its installed React composition path has already
  rendered in this lab and can precisely control custom SVG and exact type.
  Tradeoff: bespoke scenes must be authored and inspected rather than assembled
  from ready-made cards.
- **HyperFrames**: a reasonable HTML/GSAP alternative for this motion, but the
  registry currently reports an npm-resolution timeout despite a cached CLI.
  A complete render is unverified here. Choosing it requires runtime verification
  before production; there is no silent runtime substitution.
- **FFmpeg**: available for encoding, probing, frame extraction, and local QA;
  simple concatenation alone cannot author the proposed vector transformation.
- Format: 1920×1080, 16:9, 30 fps, H.264 MP4, exactly 24 seconds. Sample: 7 seconds
  at the same resolution/fps. Use conservative render concurrency, initially 2.
- Font: Arial regular/bold, verified present under macOS Supplemental fonts.
  Resolve locally and check the actual rendered font before the sample. Direction
  A's Georgia files are also present. No font download is required for this plan.
- Audio: intentionally text-led and silent. No narration, music, or sound effects
  in this validation. This is the proposed scope, not a mid-run fallback.
- Media: original SVG/React illustration and a custom diagram. Scene 3 is an
  **illustrative workflow**, labelled as such; it is not a real software capture.
  No stock search, cloud generation, credentials, or operational-system access.
- Budget cap: **$0 external media/provider spend**. Agent usage and local compute
  are separate and unpriced. There is no supported estimate for total elapsed
  creative work or account usage yet.

Fresh preflight reported image providers **0/16**, video providers **0/26**, music
generation **0/5**, and TTS **0/10** in the current shell. FFmpeg and Remotion are
available. Registry warnings include:

> hyperframes: npm package `hyperframes` not resolvable: timeout (5s) -- offline or slow registry

That warning does not establish that HyperFrames is absent. The plan uses the
verified renderer. Other capability-readiness defects remain outside this patch.

## Proposed storyboard for direction B

Use a 96 px safe margin, 72 px main copy, 36 px diagram/record labels, and a 28 px
“Illustrative workflow” disclosure in scene 3. No subtitles repeat the main copy.
The companion [scene-plan draft](inquiry-next-action.scene-plan.json) is validated
against scene_plan v1.1; it is not an approved production checkpoint.

| Scene | Time | Exact copy | Composition and timing |
|---|---|---|---|
| 1 | 0–4s | “A new inquiry arrives.” | Single original inquiry illustration on the right, copy on the left. Enter in the first 0.8s, settle by 2s, hold to 4s. |
| 2 — sample | 4–11s | “Who owns the next step?” Labels: “Inquiry”, “Owner”, “Next action” | Full-width custom diagram. At scene time 0–0.5s establish inquiry; 0.5–2s reveal owner and link; 2–3.5s connect the next action; 3.5–5.2s accent the resolved route; 5.2–7s hold. No label is replaced by an icon that needs guessing. |
| 3 | 11–19s | “Make the next action visible.” “Illustrative workflow” “Owner” “Maya” “Next action” “Send availability” “Status” “Ready” | Distinct work-record composition. Establish by 1s; reveal the three rows sequentially by 5s; hold 5–8s. Fictional name and task, no real app chrome. |
| 4 | 19–24s | “Give every inquiry a next action.” | Quiet full-frame typography. Resolve in the first 1.2s and hold; one brief green underline, no diagram or document scaffolding. |

## Assets and sample boundary

The sample demonstrates scene 2, source timeline 4–11 seconds, rendered as a
standalone seven-second clip. Author only its inquiry symbol, owner/action
diagram, exact labels, local font handling, and motion. The diagram must show
cause and effect and a readable final state. Do not render all 24 seconds or
produce scene 3/4 assets before sample approval.

After approval, carry the sample's actual assets/settings into the remaining
production. Record asset IDs, project-local paths, source tool, scene linkage,
and provenance in the asset manifest. Build original artwork; do not turn
Mermaid source text into a successful “diagram” or use the stock scene catalog.

## Acceptance and approval

1. Kyle supplies no creative assets, script, reference pack, or animation design.
2. The approved storyboard specifies every copy string, reference, asset task,
   type treatment, action, and hold. All times and asset links validate.
3. The sample is 7.0 seconds ±1 frame, at 1920×1080/30 fps. ffprobe confirms the
   container, duration, dimensions, and expected silent audio architecture.
4. Inspect four real frames and play back the clip. Check exact copy, legibility
   at full frame and half-size viewing, visual coherence, factual accuracy, and
   meaningful transformation. Technical success alone is insufficient.
5. All required labels have a readable settled state; scene 2 ends with at least
   1.8 seconds of undisturbed reading time. No missing assets, placeholder art,
   unapproved provider/runtime changes, or unresolved blockers.
6. Persist the sample review with its planning digest and clip hash. Stop for
   explicit sample approval before batch assets. Changes to script, storyboard,
   selected treatment, or production plan require a new sample review/approval.
7. After that later approval, complete the remaining scenes, stop at the assets
   gate, and render the final film only after assets approval. The final must
   retain the approved treatment and pass visual playback and technical review.

**Decision requested:** approve direction B, Remotion atelier, the stated copy
and storyboard, silent audio plan, $0 external spend cap, and production only
through the seven-second sample. Direction A remains the concrete alternative.
Approval does not waive the sample, assets, or publication gates. Nothing is
published or connected to operational systems.
