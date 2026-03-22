---
name: vertical-reel
description: |
  Create vertical 9:16 Manim videos for Instagram Reels and TikTok. Handles safe zones,
  fast pacing, hook-first structure, and platform-aware layouts.

  Trigger when: User asks for "reel", "TikTok", "vertical video", "Instagram video",
  "short-form", "9:16", or "vertical" in context of Manim video creation.
user-invokable: true
args:
  - name: exercise
    description: Which exercise or topic to create a reel for (optional — will pick one if not specified)
    required: false
---

# Vertical Reel Production Guide — Instagram Reels & TikTok

Create 9:16 vertical Manim CE videos optimized for mobile-first social platforms.
These are short (30–60s), fast-paced, hook-first educational clips.

---

## 1. Frame Configuration

```python
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 8
config.frame_height = 8 * (1920 / 1080)  # ≈ 14.22
```

Frame coordinate space: `x ∈ [-4, 4]`, `y ∈ [-7.11, 7.11]`

---

## 2. CRITICAL: Platform Safe Zones

Instagram and TikTok overlay UI elements on top of the video. Content behind these overlays
is invisible or distracting. **All meaningful content MUST stay inside the safe zone.**

```
┌─────────────────────────┐
│  STATUS BAR / HEADER    │  ← y > 5.4  — AVOID (12% top)
│─────────────────────────│
│                         │
│                    [♥]  │  ← x > 2.8  — AVOID (right 12%)
│                    [💬] │     Like, comment, share,
│   ┌─────────────┐ [➤]  │     bookmark buttons
│   │             │ [🔖] │
│   │  SAFE ZONE  │       │  ← CONTENT GOES HERE
│   │             │       │
│   └─────────────┘       │
│                         │
│─────────────────────────│
│  CAPTION / MUSIC / CTA  │  ← y < -3.6  — AVOID (25% bottom)
└─────────────────────────┘
```

### Safe Zone Constants

```python
SAFE_TOP = 4.8        # Below status bar / back button
SAFE_BOTTOM = -3.3    # Above caption / music bar / CTA
SAFE_LEFT = -3.0      # Away from left edge
SAFE_RIGHT = 3.0      # Away from right edge (social buttons)
SAFE_CENTER_X = 0.0   # Truly centered on frame
SAFE_CENTER_Y = 0.75  # Vertical center of safe zone
```

**Key insight:** Keep content CENTERED with equal margins on all sides. The safe zone
has generous padding from every edge — bottom has the most because of captions/music UI.

### What Goes Where

| Zone | What to put there |
|------|-------------------|
| `y ∈ [3.0, 4.8]` | Title / hook text — visible above "following" tabs |
| `y ∈ [-1.0, 3.0]` | Main content — calculations, diagrams, animations |
| `y ∈ [-3.3, -1.0]` | Secondary content — fraction bars, percentage labels |
| `y < -3.3` | **NOTHING** — captions cover this |
| `|x| > 3.0` | **NOTHING** — too close to edges / social buttons |

### CTA Placement

The @handle / "follow for more" text goes at the UPPER edge of the bottom danger zone,
not inside it. Place at `y ≈ SAFE_BOTTOM + 0.5` so it's visible but doesn't compete
with the main content.

---

## 3. Video Structure (30–60 seconds)

Every reel follows this 5-phase structure:

### Phase 1 — HOOK (0–3 seconds) 🎯

**The most important phase.** Users decide to scroll or stay in under 2 seconds.

Rules:
- **Start with a QUESTION** — not a title, not "let me show you"
- Use **large text** (font_size 40–52) that's readable on a phone
- Include a **visual mystery** — a shape, a "?", something incomplete
- **No slow fades** — use `GrowFromCenter`, simultaneous animations
- Everything appears in ONE `self.play()` call, `run_time=1.0`

```python
def hook(self):
    q_mark = MathTex(r"?", font_size=180, color=LABEL_COLOR)
    q_mark.move_to(UP * 3.5)  # Centered in safe zone

    hook_text = MathTex(
        r"\text{Sa mundësi ke të nxjerrësh}",
        font_size=40, color=WHITE,
    )
    hook_text2 = MathTex(
        r"\text{topin e kuq?}",
        font_size=48, color=RED,  # Key word in COLOR
    )
    hook_group = VGroup(hook_text, hook_text2).arrange(DOWN, buff=0.35)
    hook_group.move_to(UP * 0.5)

    # Everything appears at once — FAST
    self.play(
        GrowFromCenter(q_mark),
        FadeIn(hook_group, shift=UP * 0.5),
        run_time=1.0,
    )
    self.play(q_mark.animate.scale(1.2), rate_func=there_and_back, run_time=0.6)
    self.wait(0.8)
```

Good hooks:
- "Sa mundësi ke...?" (What's the probability...?)
- "A mund ta zgjidhësh këtë?" (Can you solve this?)
- "Çfarë vlere ka x?" (What is x?)
- Show the problem visually FIRST, then solve it

### Phase 2 — SETUP (3–12 seconds)

Show the problem data visually. Use counting animations, colored objects, diagrams.
- `ShowIncreasingSubsets` for counting
- `LaggedStartMap(GrowFromCenter, ...)` for revealing groups
- Keep labels SHORT — single numbers, not full sentences

### Phase 3 — SOLVE Part 1 (12–25 seconds)

The main calculation. Keep it to 3–4 equations maximum.
- One question text → one formula → one substitution → one answer
- **Skip "why" text** — reels are too fast for explanations
- **Use color** to connect equation parts to visual elements
- Answer gets `SurroundingRectangle` + `Flash`

### Phase 4 — SOLVE Part 2 (25–38 seconds) [optional]

A second quick result that contrasts with Part 1.
- Even faster — 2–3 equations
- Reuse the same visual setup (just dim/highlight differently)

### Phase 5 — PUNCHLINE (38–55 seconds)

Visual comparison, summary, or "wow" moment.
- Side-by-side or stacked comparison
- Animated fraction bars filling simultaneously
- CTA: "@mesonjetorja" and "Më shumë ushtrime..."
- `Circumscribe` the final comparison for emphasis

---

## 4. Timing & Pacing Rules

Reels are 2–3x faster than full exercise videos.

| Action | Full video | Reel |
|--------|-----------|------|
| `Write(equation)` | 1.0–1.2s | 0.6–0.8s |
| Wait after equation | 2.0–3.0s | 0.4–0.6s |
| Wait after answer | 3.5s | 1.0s |
| FadeOut transition | 0.7s | 0.3–0.4s |
| Phase transition | Clean fade | Instant or 0.4s |

**Total target: 30–50 seconds.** Never exceed 60 seconds.

### Pacing Principles
- **No dead air** — if nothing moves for > 1.5s, the viewer scrolls
- **Overlap animations** — use `AnimationGroup` and simultaneous `self.play()` calls
- **Cut the "why"** — full videos explain; reels show the result
- **One concept per reel** — don't try to cover 5 parts of an exercise

---

## 5. Typography for Small Screens

Phone screens are small. Text must be LARGE and HIGH CONTRAST.

```python
# Reel font sizes (bigger than full video)
REEL_HOOK_SIZE = 48       # Hook question — must be readable at a glance
REEL_TITLE_SIZE = 42      # Phase titles
REEL_EQUATION_SIZE = 40   # Main equations
REEL_ANSWER_SIZE = 44     # Final answers — slightly bigger
REEL_BODY_SIZE = 32       # Explanatory text (use sparingly)
REEL_SMALL_SIZE = 28      # Percentages, labels
```

Rules:
- **Never go below font_size 26** — unreadable on phones
- **One line per MathTex** — no line wrapping
- **Maximum 6 words per text line** — break into multiple MathTex if needed
- **Use color for emphasis** — not bold (which we never use anyway)

---

## 6. Layout Patterns

### Pattern A: Visual Top + Calc Bottom (recommended)

```
┌─────────────┐
│  [DIAGRAM]  │  ← Visual element: balls, triangle, graph
│  [LABELS]   │
│             │
│  Question?  │  ← One-line question
│  Formula    │  ← Formula template
│  = Answer   │  ← Substituted answer (colored, boxed)
│  ████░░░ %  │  ← Fraction bar
│             │
│  @handle    │  ← CTA
└─────────────┘
```

### Pattern B: Full-Screen Equation Chain

For pure algebra reels (no diagram needed):

```
┌─────────────┐
│  Problem?   │  ← Hook question with the equation
│             │
│  Step 1     │
│  Step 2     │  ← Each step morphs from previous
│  Step 3     │
│  = ANSWER   │  ← Big, colored, boxed
│             │
│  @handle    │
└─────────────┘
```

### Pattern C: Before/After or Comparison

```
┌─────────────┐
│   Title     │
│             │
│  Result A   │
│  ████████░  │  ← Bar A
│             │
│  Result B   │
│  ███░░░░░░  │  ← Bar B (visual contrast!)
│             │
│  @handle    │
└─────────────┘
```

---

## 7. Animation Selection for Reels

Reels need **punchy, fast animations**. Skip subtle ones.

### USE in reels:
- `GrowFromCenter` — dots, small objects appearing
- `ShowIncreasingSubsets` — counting (perfect for probability)
- `LaggedStartMap` — groups appearing with rhythm
- `Flash` — highlight answers
- `Circumscribe` — emphasize results
- `GrowFromPoint` — answer grows from equation
- `Indicate` with `there_and_back` — quick pulse

### AVOID in reels:
- `Write` for long equations — too slow; use `FadeIn(shift=UP)` instead
- `DrawBorderThenFill` for small objects — `GrowFromCenter` is faster
- `glow_trace` — too subtle for small screens
- `focus_on` — spotlight effect is too slow
- `Unwrite` / `Uncreate` — just `FadeOut`, it's faster
- `SpiralIn` — too dramatic for the pace

---

## 8. Color on Small Screens

High contrast is essential. The dark background (`#1C1C1C`) helps, but:
- **White text for neutral content** — not `GRAY_B` (too dim on phones)
- **Bright, saturated colors for key elements** — RED, BLUE, GREEN
- **ANSWER_COLOR (#83C167)** still works great for answers
- **Avoid DIVIDER_COLOR (#888888) for text** — too faint; OK for lines/borders only
- **One accent color per phase** — don't rainbow; pick red for Part A, blue for Part B

---

## 9. Albanian Text in Reels

Same rules as full videos — ALWAYS use proper diacritics:
- ë (not e), ç (not c)
- `ALBANIAN_TEX` template is required
- Keep text SHORT — Albanian words are long; break lines if needed

Common reel phrases:
```python
r"\text{Sa mundësi ke...?}"           # What's the probability...?
r"\text{A mund ta zgjidhësh?}"        # Can you solve it?
r"\text{Çfarë vlere ka } x \text{?}" # What is x?
r"\text{Përfundimi:}"                 # Conclusion:
r"\text{@mesonjetorja}"               # CTA handle
r"\text{Më shumë ushtrime në faqen tonë!}"  # More exercises on our page!
```

---

## 10. File Structure

Place reel scripts in `scripts/reels/`:
```
scripts/
  reels/
    probability_balls_reel.py
    quadratic_equation_reel.py
    triangle_angles_reel.py
    ...
```

Each reel is a **standalone Scene** (not subclassing ExerciseScene) because:
- No title screen needed (waste of seconds)
- No part headers needed
- No split layout (vertical doesn't have left/right panels)
- Custom timing constants

Import shared colors and `ALBANIAN_TEX` from `style_guide.py`.

---

## 11. Render Commands

```bash
# Preview (fast, low quality)
cd scripts && manim -pql reels/my_reel.py MyReelScene

# Final render (1080x1920, high quality)
cd scripts && manim -pqh reels/my_reel.py MyReelScene
```

The vertical config is set in the script itself via `config.*` — no CLI flags needed.

---

## 12. Checklist Before Publishing

- [ ] Total duration ≤ 60 seconds (ideally 30–50s)
- [ ] Hook grabs attention in first 2 seconds
- [ ] ALL content inside safe zone (no text at bottom/right edges)
- [ ] All Albanian text uses proper ë and ç
- [ ] Font sizes ≥ 26 everywhere
- [ ] No overlapping elements
- [ ] Answer is visually emphasized (box + flash)
- [ ] CTA (@mesonjetorja) is visible but not in danger zone
- [ ] No dead air > 1.5 seconds
- [ ] Plays well with sound off (it always does — no voiceover)
- [ ] Preview on actual phone screen before publishing
