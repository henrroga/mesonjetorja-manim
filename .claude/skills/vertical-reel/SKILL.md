---
name: vertical-reel
description: |
  Create vertical 9:16 Manim videos for Instagram Reels and TikTok. Handles safe zones,
  clarity-first pacing, and platform-aware layouts. One exercise produces MULTIPLE standalone reels.

  Trigger when: User asks for "reel", "TikTok", "vertical video", "Instagram video",
  "short-form", "9:16", or "vertical" in context of Manim video creation.
user-invokable: true
args:
  - name: exercise
    description: Which exercise or topic to create reels for (optional — will pick one if not specified)
    required: false
---

# Vertical Reel Production Guide — Instagram Reels & TikTok

Create 9:16 vertical Manim CE videos optimized for mobile-first social platforms.
Each reel is 30–50 seconds, **clarity-first**, and fully understandable on its own.

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

## 3. CORE PRINCIPLE: One Exercise = Multiple Standalone Reels

**NEVER cram an entire exercise into one reel.** Instead, split it into multiple reels,
each covering ONE clear concept or question. Each reel must be **fully understandable
on its own** — a viewer who sees only that one reel should:

1. Understand WHAT the problem is asking
2. Follow HOW it's being solved
3. See the ANSWER clearly

### How to Split an Exercise

Analyze the exercise and identify natural "reel boundaries":

| Exercise structure | Reel split |
|---|---|
| Parts a, b, c with different questions | One reel per part (or group related parts) |
| Setup + multiple probability questions | Reel 1: setup + first question. Reel 2+: each remaining question |
| Long algebra with multiple stages | One reel per stage (factoring, solving, checking) |
| Geometry with construction + calculation | Reel 1: construction. Reel 2: calculation |

**Example:** An exercise with "build a table, find P(0), P(3), P(6), P(prime)" becomes:
- `reel_a.py` — "What's the difference table for two dice?" (table + set of outcomes)
- `reel_b.py` — "P(0), P(3), P(6) for dice differences" (three quick probabilities)
- `reel_c.py` — "Is a dice difference prime?" (prime analysis + P(prime))

### Standalone Rule

Each reel must re-establish context. Don't assume the viewer saw a previous reel.
- Reel B can't start with "continuing from before..." — it must state the problem fresh
- Brief context recap (5–8 seconds) is NOT wasted time, it's essential
- Show the dice / table / setup again if needed — fast, but present

---

## 4. Reel Structure (30–50 seconds per reel)

Every reel follows this 4-phase structure:

### Phase 1 — HOOK + CONTEXT (0–10 seconds)

**The viewer must understand the problem AND want to solve it.** This is the MOST important phase.

#### Mini-Puzzle Hooks (USE WHEN POSSIBLE)

When the exercise has a natural "guess the answer" moment, **lead with it as a mini-puzzle**.
This makes viewers PAUSE and THINK before scrolling — they want to test themselves.

**Great hook patterns:**
- **Sequences:** Show the terms, ask "Cili numër vjen tjetër?" (What number comes next?)
- **Equations:** Show the equation, ask "Sa është x?"
- **Geometry:** Show the figure with a "?" on the unknown side/angle
- **Probability:** "Sa mundësi ke...?" with the full scenario visible
- **True/false:** "E vërtetë apo e gabuar?" with a bold claim

```python
def hook(self):
    # Show the sequence — viewer tries to spot the pattern
    seq = MathTex(
        r"15, \; 12, \; 9, \; 6, \; 3, \; \ldots",
        font_size=44, color=WHITE,
    )
    seq.move_to(UP * 3.0)

    question = MathTex(
        r"\text{Cili numër vjen tjetër?}",
        font_size=42, color=LABEL_COLOR,
    )
    question.next_to(seq, DOWN, buff=0.6)

    self.play(FadeIn(seq, shift=UP * 0.3), run_time=0.8)
    self.wait(1.0)
    self.play(FadeIn(question, shift=UP * 0.2), run_time=0.6)
    self.wait(3.0)  # LET THEM THINK
```

**After the hook pause (2–3 seconds), show the FULL solution** — not just the answer.
The hook gets them to stop scrolling; the solution keeps them watching.

**Not every exercise has a natural hook** — only use a mini-puzzle when it fits naturally.
When there's no natural puzzle, fall back to the clear problem statement approach below.

#### Clear Problem Statement (fallback)

When a mini-puzzle doesn't fit, state the problem clearly so the viewer immediately understands:

- **Show the ACTUAL question** — not a vague teaser, not truncated text
- Use **large text** (font_size 40–48) readable on a phone
- If the question needs 3 lines, use 3 lines — don't truncate
- **Give the question time to be READ** — if it takes 5 seconds to read, wait 5 seconds

#### Hook Rules (both types)

- The viewer must understand what's being asked within 5 seconds
- A visual element (shapes, numbers, table) helps but must NOT replace the text
- Students should think: "Oh, I know this from school — let me try!"
- After the hook, always explain the solution FULLY — never skip steps

**Bad hooks:**
- "Sa mundësi ke...?" with no context
- A giant "?" with no problem statement
- Jumping straight into a solution without showing the problem

### Phase 2 — SETUP / BUILD (10–20 seconds)

Show the visual foundation needed to solve the problem.
- Build a table, draw shapes, show objects
- `ShowIncreasingSubsets` for counting
- `LaggedStartMap(GrowFromCenter, ...)` for revealing groups
- **Label everything clearly** — the viewer needs to understand what they're looking at

### Phase 3 — SOLVE (20–35 seconds)

Walk through the solution. Keep it to 3–5 equations maximum per reel.
- Show the formula FIRST, then substitute values
- **Use color** to connect equation parts to visual elements
- **Brief "why" text is OK** — don't skip understanding to save 3 seconds
- Answer gets `SurroundingRectangle` + `Flash`

### Phase 4 — ANSWER + CTA (35–50 seconds)

Emphasize the answer, then CTA.
- Box the answer prominently
- Show "mesonjetorja.com" and "Më shumë ushtrime..."
- `Circumscribe` the final answer for emphasis

---

## 5. Timing & Pacing Rules

Reels are faster than YouTube videos, but **NEVER sacrifice comprehension for speed.**

| Action | Full video | Reel |
|--------|-----------|------|
| `Write(equation)` | 1.0–1.2s | 0.7–0.9s |
| Wait after question text | 3.0–4.0s | 2.0–3.0s (they MUST read it) |
| Wait after equation | 2.0–3.0s | 1.0–1.5s |
| Wait after answer | 3.5s | 1.5–2.0s |
| FadeOut transition | 0.7s | 0.3–0.4s |

**Total target: 30–50 seconds per reel.** Can go to 60s if needed for clarity.

### Pacing Principles
- **Clarity beats speed** — if the viewer doesn't understand, the reel is worthless
- **Give text time to be read** — Albanian words are long; respect reading speed
- **No dead air > 2s** — but "reading time" is NOT dead air
- **One concept per reel** — don't try to cover 5 parts of an exercise
- **Brief context recap is mandatory** — don't assume previous knowledge

---

## 6. Typography for Small Screens

Phone screens are small. Text must be LARGE and HIGH CONTRAST.

```python
# Reel font sizes (bigger than full video)
REEL_HOOK_SIZE = 44       # Hook question — must be readable at a glance
REEL_TITLE_SIZE = 40      # Phase titles
REEL_EQUATION_SIZE = 38   # Main equations
REEL_ANSWER_SIZE = 44     # Final answers — slightly bigger
REEL_BODY_SIZE = 32       # Explanatory text
REEL_SMALL_SIZE = 28      # Percentages, labels
REEL_TABLE_SIZE = 22      # Table cell values (tables have many cells)
```

Rules:
- **Never go below font_size 22** for tables, **26** for everything else
- **One line per MathTex** — no line wrapping
- **Maximum 7 words per text line** — break into multiple MathTex if needed
- **Use color for emphasis** — not bold (which we never use anyway)
- **Albanian text needs MORE space** — words like "ndryshesës" are long

---

## 7. Layout Patterns

### Pattern A: Question Top + Visual Middle + Calc Bottom (recommended)

```
┌─────────────┐
│  Question    │  ← Full question text, readable
│  (2-3 lines) │
│             │
│  [DIAGRAM]  │  ← Visual element: table, balls, shapes
│             │
│  Formula    │  ← Formula template
│  = Answer   │  ← Substituted answer (colored, boxed)
│             │
│  @handle    │  ← CTA
└─────────────┘
```

### Pattern B: Full-Screen Equation Chain

For pure algebra reels (no diagram needed):

```
┌─────────────┐
│  Problem    │  ← Full problem statement
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
│   Context   │  ← What we're comparing
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

## 8. Animation Selection for Reels

Reels need **clear, purposeful animations**. Every animation must serve comprehension.

### USE in reels:
- `GrowFromCenter` — dots, small objects appearing
- `ShowIncreasingSubsets` — counting (perfect for probability)
- `LaggedStartMap` — groups appearing with rhythm
- `Flash` — highlight answers
- `Circumscribe` — emphasize results
- `GrowFromPoint` — answer grows from equation
- `Indicate` with `there_and_back` — quick pulse
- `Write` — still good for equations; don't rush it

### AVOID in reels:
- `DrawBorderThenFill` for small objects — `GrowFromCenter` is faster
- `glow_trace` — too subtle for small screens
- `focus_on` — spotlight effect is too slow
- `Unwrite` / `Uncreate` — just `FadeOut`, it's faster
- `SpiralIn` — too dramatic for the pace

---

## 9. Color on Small Screens

High contrast is essential. The dark background (`#1C1C1C`) helps, but:
- **White text for neutral content** — not `GRAY_B` (too dim on phones)
- **Bright, saturated colors for key elements** — RED, BLUE, GREEN
- **ANSWER_COLOR (#83C167)** still works great for answers
- **Avoid DIVIDER_COLOR (#888888) for text** — too faint; OK for lines/borders only
- **One accent color per reel** — pick a consistent highlight color

---

## 10. Albanian Text in Reels

Same rules as full videos — ALWAYS use proper diacritics:
- ë (not e), ç (not c)
- `ALBANIAN_TEX` template is required
- **Give Albanian text enough space** — words are long, break lines generously

Common reel phrases:
```python
r"\text{Sa mundësi ke...?}"           # What's the probability...?
r"\text{A mund ta zgjidhësh?}"        # Can you solve it?
r"\text{Çfarë vlere ka } x \text{?}" # What is x?
r"\text{Përfundimi:}"                 # Conclusion:
r"\text{mesonjetorja.com}"             # CTA — always the website, never @handle
r"\text{Më shumë ushtrime në faqen tonë!}"  # More exercises on our page!
```

---

## 11. File Structure

Reel scripts live **inside the exercise folder**, next to the YouTube script.
Multiple reels per exercise — one file per reel:

```
scripts/
  matematike/
    matematika-10-11-pjesa-2/      # sourceSlug from DB
      8-3A/                         # unitSlug from DB
        3/                          # exerciseSlug from DB
          ushtrimi3.py              # YouTube video (ExerciseScene)
          reel_a.py                 # Reel A — e.g., "table + outcomes"
          reel_b.py                 # Reel B — e.g., "P(0), P(3), P(6)"
          reel_c.py                 # Reel C — e.g., "P(prime)"
          publish.txt               # Titles & captions for all videos
          Ushtrimi3.mp4             # YouTube output (gitignored)
          ReelA.mp4                 # Reel A output (gitignored)
          ReelB.mp4                 # Reel B output (gitignored)
          ReelC.mp4                 # Reel C output (gitignored)
```

Each reel is a **standalone Scene** (not subclassing ExerciseScene) because:
- No title screen needed
- No part headers needed
- No split layout (vertical doesn't have left/right panels)
- Custom timing constants

**Class naming:** `ReelA`, `ReelB`, `ReelC` — matches the output filename.

Import shared colors and `ALBANIAN_TEX` from `style_guide.py`.

---

## 12. Exercise Data & Solution Handling

The user provides exercise data as a JSON object with these fields:
- `exerciseSlug`, `unitSlug`, `sourceSlug` — used for folder structure
- `question` — the exercise problem (HTML)
- `solution` — the text solution from the website (HTML, may contain images)
- `unitContext` — the lesson/unit theory, examples, and tables (Markdown)
- `grade` — the student grade level (e.g., "Klasa 11")

**CRITICAL: The solution is a REFERENCE, not gospel truth.**
- Use it as a clue to understand the expected approach and final answers
- **Always double-check the math yourself** — verify every calculation
- **Expand beyond the solution** — the video must be MORE explanatory than the text
- **Use the unitContext** to connect the exercise to the broader lesson
- The unitContext shows the theory, notation, and worked examples the student has seen
- Reference the unit's approach/notation so the video feels like a natural extension

---

## 13. publish.txt — MANDATORY

Always generate a `publish.txt` in the exercise folder with ready-to-paste captions for each reel. See the `youtube-video` skill for the full template. Each reel section includes:
- Caption text with hook question + key answer + hashtags
- Reference: `Ushtrimi <N> | Kapitulli <unit> | <textbook> (Botime Pegi)`
- CTA: `Më shumë zgjidhje: mesonjetorja.com`
- Hashtags: `#matematike #<topic> #klasa<N> #mesonjetorja`

---

## 14. Render Commands

```bash
# Preview (fast, low quality — from project root)
./render.sh scripts/matematike/<sourceSlug>/<unitSlug>/<exerciseSlug>/reel_a.py ReelA l

# Final render with music (from project root)
./render.sh scripts/matematike/<sourceSlug>/<unitSlug>/<exerciseSlug>/reel_a.py ReelA
```

The vertical config is set in the script itself via `config.*` — no CLI flags needed.

---

## 15. Checklist Before Publishing

- [ ] Each reel is fully understandable WITHOUT seeing the other reels
- [ ] The question/problem is clearly stated and given enough reading time
- [ ] A student would think "I know this exercise!" within the first 8 seconds
- [ ] Total duration 30–50 seconds (up to 60s if clarity demands it)
- [ ] ALL content inside safe zone (no text at bottom/right edges)
- [ ] All Albanian text uses proper ë and ç
- [ ] Font sizes ≥ 26 everywhere (≥ 22 for table cells)
- [ ] No overlapping elements
- [ ] Answer is visually emphasized (box + flash)
- [ ] CTA (mesonjetorja.com) is visible but not in danger zone
- [ ] Plays well with sound off (it always does — no voiceover)
- [ ] Preview on actual phone screen before publishing
