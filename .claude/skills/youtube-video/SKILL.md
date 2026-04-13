---
name: youtube-video
description: |
  Create full-length YouTube exercise videos using Manim CE. Handles persistent visuals,
  step-by-step calculations, table highlighting, end screens, and grade-aware pacing.

  Trigger when: User asks for "YouTube video", "full video", "exercise video", "ushtrimi",
  or provides exercise JSON data without specifying "reel".
user-invokable: true
args:
  - name: exercise
    description: Which exercise to create a video for (optional)
    required: false
---

# YouTube Video Production Guide

Create full-length 16:9 Manim CE exercise videos for mesonjetorja.com.
These are 1–3 minute detailed walkthroughs published on YouTube.

---

## 1. When to Use ExerciseScene vs Plain Scene

**Use `ExerciseScene`** (from `components.py`) when:
- Each part of the exercise is self-contained (no shared visual state)
- Parts don't need a persistent figure/table across them
- Standard geometry or algebra exercises with independent sub-questions

**Use a plain `Scene`** when:
- A key visual (table, graph, diagram) must persist across multiple parts
- Parts reference the same figure and highlight different elements on it
- The visual IS the exercise (probability tables, coordinate planes, etc.)

`ExerciseScene` calls `fade_all()` between every part — this DESTROYS all mobjects.
If you need anything to survive across parts, you MUST use a plain `Scene`.

```python
# WRONG — table gets destroyed between parts
class Ushtrimi3(ExerciseScene):
    parts = ["a", "b", "c"]
    def part_a(self):
        self.table = MathTable(...)  # built here
    def part_b(self):
        self.table.highlight(...)    # ERROR: table was destroyed by fade_all

# CORRECT — plain Scene with manual flow control
class Ushtrimi3(Scene):
    def construct(self):
        self.title_screen()
        self.part_a()   # builds table
        self.part_b()   # table persists, shifts left
        self.part_c()   # table still there, highlight cells
        self.final_summary()
        self.end_screen()
```

---

## 2. Persistent Visual Pattern

When the exercise has a key visual element (table, graph, triangle), follow this pattern:

### Phase 1: Build (centered)
Build the visual centered on screen with full labels.

### Phase 2: Shift & Shrink (left side)
When calculations begin, shift the visual to the left and scale it down:
```python
self.play(
    self.table.animate.scale(0.8).move_to(LEFT * 3.5 + DOWN * 0.2),
    run_time=1.0,
)
```
Remove auxiliary labels (axis labels, totals) that won't fit at the smaller size.

### Phase 3: Reference (highlight per step)
For each calculation step, highlight the relevant parts of the visual:
```python
# Highlight cells matching value
entries = [self.table.get_entries((r+2, c+2)) for r,c in matching_cells]
rects = VGroup(*[SurroundingRectangle(e, color=color, ...) for e in entries])
self.play(
    *[e.animate.set_color(color) for e in entries],
    LaggedStartMap(Create, rects, lag_ratio=0.05),
    run_time=0.7,
)
```
After each step, **reset the highlights** before the next step:
```python
self.play(
    FadeOut(rects),
    *[e.animate.set_color(WHITE) for e in entries],
    run_time=0.3,
)
```

### Phase 4: Farewell
Only remove the visual when ALL calculations that reference it are done.

---

## 3. Albanian Mathematical Terminology

**ALWAYS use Albanian textbook terms, not Latin/foreign loanwords.** Match the exact terminology from the exercise's solution text — that is authoritative.

| Correct (Albanian) | WRONG (avoid) | Context |
|---|---|---|
| **Dallori** | "Diskriminanta" | Discriminant D = b² - 4ac (quadratic) |
| **Integrali** | "antiderivatë" | Integral in calculus |
| **Syprina** | "Sipërfaqja" (generic) | Area under curve |
| **Kufiza e n-të** | "Termi i n-të" | nth term of sequence |
| **Diferenca e përbashkët** | "Raporti" | Common difference (arithmetic seq) |
| **Herësi** | — | Quotient |
| **Njehsojmë** | — | "We calculate" (general solve verb) |
| **Zgjidhje** | — | Solution |
| **Ekuacion kuadratik** | "Ekuacion kuadratik" ✓ | Quadratic equation |
| **Përkufizimi** | "Definicioni" | Definition |
| **Provë** | — | Verification/check |

**Why:** Students learn specific Albanian terms. Foreign loanwords like "diskriminanta" or "antiderivatë" aren't used in Albanian schools — students won't recognize them.

**How to apply:** When the user provides an exercise JSON, look at the `solution` field — that has the authoritative terminology. Match it.

## 4. Integral / Area Specifics

### Terminology
- Use **"integrali"** — never "antiderivatë" or "antiderivata"
- "Njehsojmë integralin:" not "Gjejmë antiderivatën:"

### Always show units on area results
Area answers MUST include **"njësi katrore"** (square units):
```python
# WRONG — 3 what?
r"S = 3"

# CORRECT
r"S = 3 \text{ njësi katrore}"
# or shorter:
r"S = 3 \text{ nj}^2"
```

### Graph boundary labels vs axis ticks
When drawing vertical boundary lines (x=1, x=2) on a graph, do NOT place labels that overlap with existing axis tick numbers. Options:
1. **Let axis numbers speak for themselves** — don't add redundant "x=1" labels at the same position
2. If boundary labels are needed, **offset them** above/below the axis, not on top of the tick number
3. Use dashed lines for boundaries WITHOUT text labels when the axis already shows the number

```python
# WRONG — "x=1" label overlaps with axis tick "1"
bound_label = MathTex("x=1").next_to(axes.c2p(1, 0), DOWN)  # sits on top of "1"

# CORRECT — dashed line only, axis tick already shows "1"
bound_line = DashedLine(axes.c2p(1, 0), axes.c2p(1, y_max), color=DIVIDER_COLOR)
# No redundant text label needed
```

---

## 4. Tables — Use MathTable, Never Manual Grids

**NEVER** position table cells manually with coordinate math. It causes misalignment.

**ALWAYS** use Manim's `MathTable`:
```python
from manim import MathTable

table = MathTable(
    table_data,                    # 2D list of strings
    row_labels=row_labels,         # list of MathTex
    col_labels=col_labels,         # list of MathTex
    top_left_entry=corner_label,   # MathTex for top-left cell
    include_outer_lines=True,
    v_buff=0.25,
    h_buff=0.4,
    element_to_mobject_config={"font_size": 22},
    line_config={"stroke_width": 1, "color": DIVIDER_COLOR, "stroke_opacity": 0.5},
)
table.scale(0.85)
```

**Accessing cells:** `table.get_entries((row, col))` — 1-indexed, row 1 and col 1 are the label rows. So data cell (r, c) is at `(r+2, c+2)`.

---

## 4. Calculation Panel (Right Side)

When the visual is on the left, calculations go on the right at `x = PX` (3.2):

```python
PX = 3.2

question.move_to(RIGHT * PX + UP * 2.5)
equation.next_to(prev, DOWN, buff=0.35).set_x(PX)
answer.next_to(prev, DOWN, buff=0.4).set_x(PX)
```

**Always** call `.set_x(PX)` after `.next_to()` to lock horizontal alignment.

### Cleanup Pattern
After each sub-question, clean up the right panel but keep the left visual:
```python
self.play(
    FadeOut(question), FadeOut(why), FadeOut(count), FadeOut(answer), FadeOut(box),
    FadeOut(header),
    run_time=0.5,
)
# Reset table highlights too
self._reset_cells(target_val, rects)
```

---

## 5. Screen Space — Use the Full Screen, Never Cram

### Center intro screens
Formula intros, problem statements, or any standalone content should be **centered on screen** using `VGroup(...).arrange(DOWN).move_to(ORIGIN)`. Never pin them to the top edge leaving dead space below.

### Two-phase layout for repetitive parts
When an exercise has many similar sub-questions (e.g., 5 sequences), each part should use two phases:

1. **Visual phase** — Show the sequence/diagram with annotations (arrows, labels) centered on screen
2. **Calculation phase** — Fade out the visual, move key info (a₁, d) up, then chain the calculation steps using the freed space

```python
# Phase 1: show sequence + arrows
self.play(Write(terms), ...)
self.play(Create(arrows), ...)
self.play(Write(params), ...)  # a₁ = 15, d = -3
self.wait(...)

# Phase 2: fade visual, reclaim space for calculation
self.play(FadeOut(terms), FadeOut(arrows), run_time=0.4)
self.play(params.animate.move_to(header.get_bottom() + DOWN * 0.5), run_time=0.4)

# Now chain substitution → expand → simplify → answer in the freed space
```

This prevents tall content (fractions, long equations) from pushing the answer box off screen.

### Arrows go BELOW, not above
When adding curved arrows between sequence terms, place them **below** the terms (positive angle). Labels go below the arrows. This avoids overlapping with headers above.

```python
# WRONG — arrows above terms, crash into header
y_base = terms.get_top()[1] + 0.15
arrow = CurvedArrow(start, end, angle=-TAU/4)

# CORRECT — arrows below terms
y_base = terms.get_bottom()[1] - 0.15
arrow = CurvedArrow(start, end, angle=TAU/4)  # positive = curves down
d_label.next_to(arrow, DOWN, buff=0.05)
```

### CurvedArrow: use Create(), never GrowArrow()
`GrowArrow()` crashes on `CurvedArrow` in Manim CE 0.20.1. Always use `Create()`.

---

## 6. End Screen — MANDATORY

Every YouTube video MUST end with:
```python
def end_screen(self):
    domain = MathTex(r"\text{mesonjetorja.com}", font_size=TITLE_SIZE, color=WHITE)
    domain.move_to(UP * 0.5)
    tagline = MathTex(
        r"\text{Më shumë ushtrime në faqen tonë!}",
        font_size=SUBTITLE_SIZE, color=BODY_TEXT_COLOR,
    )
    tagline.next_to(domain, DOWN, buff=0.5)
    self.play(GrowFromCenter(domain), FadeIn(tagline, shift=UP * 0.3), run_time=1.0)
    self.wait(8.0)  # 8 seconds for YouTube end screen overlay
```

**Never use `@mesonjetorja`** — always `mesonjetorja.com`.

---

## 6. Exercise Data & Solution Handling

Same as reel skill — the user provides JSON with:
- `exerciseSlug`, `unitSlug`, `sourceSlug` — folder structure
- `question` — the exercise problem (HTML)
- `solution` — REFERENCE only, always double-check the math
- `unitContext` — lesson theory, use it to connect the exercise to the broader topic
- `grade` — adjust pacing and detail level

---

## 7. File Structure

```
scripts/
  matematike/
    <sourceSlug>/
      <unitSlug>/
        <exerciseSlug>/
          ushtrimi<N>.py       # YouTube video
          reel_a.py            # Reel A (standalone)
          reel_b.py            # Reel B (standalone)
          publish.txt          # Titles & captions for all videos
          Ushtrimi<N>.mp4      # YouTube output (gitignored)
          ReelA.mp4            # Reel output (gitignored)
```

---

## 8. publish.txt — MANDATORY

Every exercise folder MUST include a `publish.txt` with ready-to-paste titles and captions for all videos. This makes posting fast and consistent.

### YouTube Title Format
```
Ushtrimi <N> | Kapitulli <unit> | <textbook name> (Botime Pegi)
```

### YouTube Description Template
```
Në këtë video zgjidhim ushtrimin <N> nga kapitulli <unit> ku <brief problem description in Albanian>.

Zgjidhjet e librit: https://mesonjetorja.com/zgjidhje/<sourceSlug>

Lini komentet tuaja më poshtë dhe bëni Subscribe për më shumë.

Website: https://mesonjetorja.com/
Instagram: https://www.instagram.com/mesonjetorja
TikTok: https://www.tiktok.com/@mesonjetorja

#matematike #<topic> #<topic> #klasa<N>
```

### Reel Caption Template
```
<Hook question or problem summary in Albanian> 🎲

<Key result or answer>

Ushtrimi <N> | Kapitulli <unit> | <textbook short name> (Botime Pegi)

Më shumë zgjidhje: mesonjetorja.com

#matematike #<topic> #<topic> #klasa<N> #mesonjetorja
```

### File Structure
```
═══════════════════════════════════════════════════════
 YOUTUBE VIDEO
═══════════════════════════════════════════════════════

Title:
...

Description:
...

═══════════════════════════════════════════════════════
 REEL A — <topic>
═══════════════════════════════════════════════════════

Caption (Instagram / TikTok):
...
```

One section per video. Include the key answers in reel captions so viewers can verify.

---

## 9. Render Commands

```bash
# Preview (low quality)
./render.sh scripts/matematike/<sourceSlug>/<unitSlug>/<exerciseSlug>/ushtrimi<N>.py Ushtrimi<N> l

# Final render (1080p with music)
./render.sh scripts/matematike/<sourceSlug>/<unitSlug>/<exerciseSlug>/ushtrimi<N>.py Ushtrimi<N>
```

---

## 9. Checklist

- [ ] Key visual persists across all parts that reference it
- [ ] No mobject is animated after being destroyed (no ghost highlights)
- [ ] Tables use `MathTable`, not manual coordinate positioning
- [ ] Right-panel content is aligned at `x = PX`
- [ ] Each step highlights relevant cells/parts on the persistent visual
- [ ] Highlights are reset between steps
- [ ] All Albanian text uses proper ë and ç
- [ ] End screen shows `mesonjetorja.com` with 8s hold
- [ ] No overlapping elements anywhere — arrows below terms, labels clear of headers
- [ ] Intro/formula screens are centered on screen (not pinned to top with dead space)
- [ ] Repetitive parts use two-phase layout (visual → fade → calculation)
- [ ] Fractions/tall content doesn't push answer box off screen
- [ ] CurvedArrow uses Create() not GrowArrow()
- [ ] Video ends cleanly (no abrupt cut)
