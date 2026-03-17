# Mësonjëtorja Manim — Video Production Guidelines

This project generates educational math/physics video solutions using Manim Community Edition.
Videos are published on mesonjetorja.com for Albanian students.

**CRITICAL: These videos have NO voiceover. The visuals must tell the complete story on their own. Every calculation result must be reflected on the figure. Every step must be visually obvious.**

## #1 Rule: Visual Storytelling — The Figure Is the Star

The figure/diagram is NOT a static decoration. It is the primary teaching tool. The right-side calculation panel supports the figure, not the other way around.

### Value Transfer Animations

Every time a value is computed on the right panel, **animate it onto the figure**:

```python
# After computing BH ≈ 15.73 on the right side:
bh_label = MathTex(r"15{,}73", font_size=22, color=LABEL_COLOR)
bh_label.move_to(...)  # position on the diagram

# Create a copy of the equation result and animate it flying to the figure
value_copy = eq_result.copy()
self.play(
    value_copy.animate.move_to(bh_label).scale(0.6),
    run_time=0.8,
)
self.play(FadeOut(value_copy), FadeIn(bh_label), run_time=0.3)
```

This creates a visual link between "we calculated this" and "here it is on the shape."

### Sub-Shape Focus (Highlight, Extract, Enlarge)

When working on a sub-part of a figure (e.g., right triangle ABH within triangle ABC):

1. **Shade/highlight the sub-shape** with a semi-transparent fill:
```python
sub_tri = Polygon(A, B, H, fill_color=SHAPE_COLOR, fill_opacity=0.15,
                  stroke_color=SHAPE_COLOR, stroke_width=2)
self.play(FadeIn(sub_tri), run_time=0.6)
```

2. **Dim everything else** — reduce opacity of non-relevant parts:
```python
self.play(
    tri.animate.set_stroke(opacity=0.3),
    other_labels.animate.set_opacity(0.3),
    run_time=0.5,
)
```

3. **For complex sub-shapes, extract and enlarge**: duplicate the sub-shape, scale it up, and work on the larger copy:
```python
# Create enlarged copy of the right triangle
big_sub = sub_tri_group.copy()
self.play(
    main_figure.animate.scale(0.5).shift(UP * 1.5 + LEFT * 1),
    big_sub.animate.scale(1.5).move_to(LEFT * 3),
    run_time=1.0,
)
```

### Progressive Figure Labeling

The figure should accumulate information as the solution progresses:
- Step 1 finds ∠C = 51° → show 51° arc on the figure
- Step 2 finds ∠A = 78° → show 78° arc on the figure
- Step 3 draws altitude → show it on the figure
- Step 4 finds BH ≈ 15.73 → animate the value onto the segment
- Step 5 finds BC ≈ 31.5 → animate the final answer onto the base

**The figure should visually grow richer as the student watches.**

### Color Linking Between Panel and Figure

When an equation references a specific element, **use the same color** on both:
- If the equation shows `BH` in yellow, the BH segment label on the figure should also be yellow
- If the answer `BC ≈ 31.5` is green, the BC label on the figure should be green
- Flash/highlight the relevant figure element when its equation appears

### Visual Cue Animations

Since there is no voiceover, use animations to direct attention:

- **Flash** a side/angle on the figure when it's referenced in a new equation
- **Indicate** (brief arrow or glow) which part of the figure we're about to work on
- **Circumscribe** a result to emphasize it
- Use `Indicate(mobject)` or brief color pulses to say "look here"

```python
# Before using angle B in a calculation, flash it on the figure
self.play(Indicate(ang_B_arc, color=YELLOW), run_time=0.5)
```

## Visual Toolkit — Manim CE Features to Use

Beyond basic Create/Write/FadeIn, use these built-in helpers from `ExerciseScene` for richer visuals:

### Equation Morphing (`morph_equation`)
When showing algebraic simplification steps, **MORPH** equations instead of FadeOut + new Write. Matching symbols stay in place while changed parts animate smoothly.

**CRITICAL: Use `{{double braces}}` around matchable parts** — this is how Manim knows what corresponds to what:
```python
# Create with double braces for matchable parts
eq1 = MathTex("{{x}}^2", "+", "{{y}}^2", "=", "{{49}}", font_size=32)
eq1.move_to(...); self.play(Write(eq1))

# Morph: "=" and "49" stay in place, "x^2 + y^2" morphs to "r^2"
eq2 = self.morph_equation(eq1, r"{{r}}^2 = {{49}}")

# Morph with color: "49" stays, "r^2 =" morphs to "r ="
eq3 = self.morph_equation(eq2, r"{{r}} = {{7}}", color=ANSWER_COLOR)
```

**Variable substitution with `key_map`:**
```python
# Map x→a and y→b when changing notation
eq2 = self.morph_equation(eq1, r"{{a}}^2 + {{b}}^2 = {{25}}",
                          key_map={"x": "a", "y": "b"})
```

**Use for:** simplification chains, rearranging formulas, substitution, factoring steps.

### Shape Morphing (`morph_shape`)
Transform one geometric figure into another while keeping matching parts stable:
```python
# Full triangle morphs into sub-triangle
new_tri = Polygon(A, B, H, color=SHAPE_COLOR)
self.morph_shape(full_triangle, new_tri)
```
**Use for:** triangle → sub-triangle, rearranging figures, before/after comparisons.

### Circumscribe + Flash (`highlight_result`)
For final answers and key results, use `highlight_result` instead of just a box:
```python
self.highlight_result(answer_eq)  # Circumscribe + particle Flash
```
**Use for:** final boxed answers, key intermediate findings, "aha" moments.

### Flash Points (`flash_point`)
When an intersection point or special location appears on a graph:
```python
self.flash_point(dot)  # particle burst at the dot's location
```
**Use for:** intersection points found algebraically, axis intercepts, vertices.

### Sequential Reveals (`reveal_sequence`)
When showing 3+ items (intercept dots, colored balls, summary rows), reveal them one by one with overlapping timing instead of all at once:
```python
self.reveal_sequence([dot1, dot2, dot3, dot4], lag_ratio=0.2)
```
**Use for:** multiple intercepts, lists of results, ball/object groups, summary tables.

### Path Tracing (`trace_path`)
Animate a dot traveling along a curve to show it satisfies an equation:
```python
dot = Dot(axes.c2p(5, 0), radius=0.08)
self.trace_path(dot, circle, run_time=3.0)
```
**Use for:** demonstrating circle equations, showing a point on a curve, geometric constructions.

### Introduction Animations — Stop Using Plain FadeIn for Everything

Choose the right introduction animation based on WHAT you're introducing:

| What | Animation | Why |
|------|-----------|-----|
| Circles, shapes, filled objects | `DrawBorderThenFill(shape)` | Outline first, then fill — satisfying |
| Dots, small objects, answer boxes | `GrowFromCenter(dot)` | Pops into existence — more alive than FadeIn |
| Results appearing at a location | `GrowFromPoint(result, origin_point)` | Grows FROM the calculation — visual link |
| Side labels, edge annotations | `GrowFromEdge(label, LEFT)` | Grows from the side it's attached to |
| Arrows, vectors | `GrowArrow(arrow)` | Grows from tail to tip — natural direction |
| Text, equations | `Write(eq)` | Standard for text — keep using this |
| Groups of items appearing | `reveal_sequence([...])` | LaggedStart — one by one with rhythm |

```python
# Instead of FadeIn(circle):
self.play(DrawBorderThenFill(circle), run_time=1.2)

# Instead of FadeIn(dot):
self.play(GrowFromCenter(dot), run_time=0.5)

# Answer box grows from the equation that produced it:
self.play(GrowFromPoint(answer_box, equation.get_center()), run_time=0.8)

# Side label grows from the edge of the triangle side:
self.play(GrowFromEdge(side_label, LEFT), run_time=0.5)
```

**Reserve `FadeIn` for:** text blocks, background elements, subtle UI. For anything the student should NOTICE appearing, use a growing animation.

### Removal Animations — Stop Using Plain FadeOut for Everything

| What | Animation | Why |
|------|-----------|-----|
| Geometric shapes | `Uncreate(shape)` | Reverse-draws the outline away — cleaner than fading |
| Equations, text | `Unwrite(eq)` | Erases like rubbing out — matches how Write introduced it |
| Groups, backgrounds | `FadeOut(group)` | Standard — fine for bulk cleanup |

```python
# Instead of FadeOut(triangle):
self.play(Uncreate(triangle), run_time=0.8)

# Instead of FadeOut(equation):
self.play(Unwrite(equation), run_time=0.6)
```

### Counting Animations

**`ShowIncreasingSubsets`** — Shows submobjects accumulating one by one, leaving all previous visible. Perfect for counting problems:
```python
# 22 balls appear one by one, each staying on screen
balls = VGroup(*[Circle(...) for _ in range(22)])
self.play(ShowIncreasingSubsets(balls), run_time=3.0)
```
**Use for:** counting objects (probability), building up a set of points, showing terms appearing in a sum.

### Dramatic Intros

**`SpiralIn`** — Submobjects fly in on spiral trajectories. Use sparingly for impact:
```python
# Final summary answers spiral in dramatically
self.play(SpiralIn(answer_group), run_time=1.5)
```
**Use for:** title screens, final summary tables, celebration moments. NOT for routine content.

### Glow Trace (`glow_trace`)
A neon glow traveling along a curve — says "THIS is the shape":
```python
self.glow_trace(circle, color=YELLOW)           # glow traces the full circle
self.glow_trace(Line(A, B), color=AUX_COLOR)    # glow runs along a side
```
**Use for:** introducing a circle/line/curve, emphasizing a specific edge, showing "this is the path". Especially powerful when first drawing a shape — draw it, then glow-trace it.

### Focus Spotlight (`focus_on`)
A spotlight shrinks onto a target — tells the viewer "NOW LOOK HERE":
```python
self.focus_on(dot_P)          # spotlight onto point P
self.focus_on(angle_arc)      # spotlight onto the angle
```
**Use for:** directing attention before a calculation step. Critical for no-voiceover videos — this is how you "point" at something.

### Celebration (`celebrate`)
Wave + Flash for the absolute final answer — more dramatic than `highlight_result`:
```python
self.celebrate(final_answer_box)  # wave + particle burst
```
**Use for:** the very last answer of the entire exercise, not intermediate results.

### Rate Functions for Polish
Add personality to animations with easing:
- `rate_functions.smooth` — default, good for most
- `rate_functions.rush_into` — fast start, slow end (snapping into place)
- `rate_functions.there_and_back` — temporary highlight that returns

### Dynamic Values & Updaters

These make videos feel alive instead of static. Use them to show PROCESSES, not just results.

#### Animated Counter (`animated_counter`)
A number that rolls from start to end using Manim's `ChangeDecimalToValue`. Students SEE the counting happen:
```python
# Count balls: 0 → 22, showing "Total: 22"
self.animated_counter(0, 22, prefix="Total: ", font_size=36,
                      position=RIGHT * 3, run_time=2.0)
```
**Use for:** counting objects, showing a computed value gradually, totals.

For standalone rolling numbers without the wrapper, use Manim directly:
```python
number = DecimalNumber(0, num_decimal_places=2, font_size=36, color=ANSWER_COLOR)
number.move_to(...)
self.add(number)
self.play(ChangeDecimalToValue(number, 15.73), run_time=1.5)
```

For function-driven values (e.g., tied to animation progress):
```python
self.play(ChangingDecimal(number, lambda a: 25 * np.cos(a * 51 * DEGREES)), run_time=2)
```

#### Fraction Bar (`fraction_bar`)
A visual bar that fills proportionally — shows what a fraction LOOKS like:
```python
# P(red) = 15/22 — bar fills to ~68%
self.fraction_bar(15, 22, position=DOWN * 2, color=RED)
```
**Use for:** probability fractions, percentages, ratio comparisons, proportions.

#### Linked Labels (`linked_label`)
A label that stays attached to a moving point — never gets "left behind":
```python
label = self.linked_label(dot, r"P(x,y)", direction=UR)
self.add(label)
# Now if dot moves, label follows automatically
```
**Use for:** labels on points that trace paths, dynamic geometry, parameter-dependent text.

#### Parameter Exploration (`animate_parameter`)
Animate a parameter changing with everything updating in real-time:
```python
r = ValueTracker(1)
circle = always_redraw(lambda: Circle(radius=r.get_value(), color=SHAPE_COLOR))
eq = always_redraw(lambda: MathTex(f"r = {r.get_value():.1f}").to_corner(UR))
self.add(circle, eq)
self.animate_parameter(r, 1, 10, [circle, eq], run_time=4)
```
**Use for:** showing how radius affects a circle, how slope changes a line, exploring what happens when a value changes. Powerful for building intuition.

### When to Use Each Feature

| Situation | Feature |
|-----------|---------|
| Final answer emphasis | `highlight_result()` |
| Algebra step → next step | `morph_equation()` (use `{{double braces}}`) |
| Geometry figure → sub-figure | `morph_shape()` |
| Multiple dots/items appearing | `reveal_sequence()` |
| Point on a curve | `trace_path()` |
| Intersection found | `flash_point()` |
| Counting objects | `animated_counter()` |
| Showing a proportion | `fraction_bar()` |
| Label follows moving point | `linked_label()` |
| "What if r changes?" | `animate_parameter()` |
| "This is the circle" | `glow_trace()` |
| "Look HERE now" | `focus_on()` |
| Final exercise answer | `celebrate()` |
| Shape intro (filled) | `DrawBorderThenFill` |
| Dot/small object intro | `GrowFromCenter` |
| Result appearing from source | `GrowFromPoint` |
| Arrow intro | `GrowArrow` |
| Counting objects 1 by 1 | `ShowIncreasingSubsets` |
| Dramatic summary intro | `SpiralIn` |
| Remove a shape cleanly | `Uncreate` |
| Erase an equation | `Unwrite` |

## Albanian Characters in LaTeX (ë, ç, etc.)

MathTex uses LaTeX which does NOT support UTF-8 characters like `ë` inside `\text{}`. The LaTeX diaeresis encoding `\"{e}` also renders incorrectly as `e"`.

**Rule: Use plain ASCII in all MathTex text.** Replace:
- `ë` → `e` (e.g., "këndor" → "kendor", "është" → "eshte")
- `ç` → `c`

Albanian students will understand the text perfectly without diacritics. `e"` is unacceptable.

## Shifted Axes: Never Double-Shift

When axes are shifted (e.g., `graph_group.animate.shift(LEFT * 3.2)`), all `axes.c2p()` and `axes.plot()` calls AUTOMATICALLY return coordinates in the shifted position.

**NEVER add manual shifts to objects created from already-shifted axes:**

```python
# WRONG — double-shifts the tangent line
tangent = axes.plot(lambda x: -0.75*x + 12.5, x_range=[-4, 12], ...)
tangent.shift(LEFT * 3.2)  # BUG: axes already shifted

# CORRECT — axes.plot() inherits the shift
tangent = axes.plot(lambda x: -0.75*x + 12.5, x_range=[-4, 12], ...)
# No manual shift needed

# WRONG — double-shifts a label position
pos = np.array(axes.c2p(6, 8)) + LEFT * 3.2  # BUG

# CORRECT
pos = np.array(axes.c2p(6, 8))  # already in shifted space
```

This applies to: `axes.plot()`, `axes.c2p()`, `Dot(axes.c2p(...))`, right-angle marks using `axes.c2p()`, tangent lines, labels, etc.

## CRITICAL: Zero Overlap Rule

**NOTHING may overlap ANYTHING on screen. This is the #2 quality rule.**

Before placing any visual element, mentally check if it will overlap with existing elements:

1. **Vertex labels vs side lengths** — A vertex label "B" and a side length "25" near the same corner WILL overlap. Use `buff=0.3+` and directional placement (`DL`, `DR`, `UR`, `UL`) to separate them. If a label would be close to a side-length number, move it further away or pick a different direction.

2. **Angle arcs vs construction lines** — An altitude/height drawn from vertex X bisects the angle at X. The dashed line goes through the middle of any angle arc at that vertex. **Always FadeOut the angle arc and label at vertex X before drawing an altitude from X.** When showing final angle arcs, **FadeOut the altitude first** if it passes through a vertex that will get an arc.

3. **Angle arcs vs triangle sides** — If the angle is small (< 40°), use a smaller arc radius (0.25-0.3). If the angle is large (> 120°), use a larger distance for the label. Always verify the arc + label don't cross a triangle side.

4. **Side length labels vs tick marks** — Place length labels with `perp_offset` of at least 0.35-0.4 to clear tick marks.

5. **Right angle marks vs labels** — The small square mark and nearby labels ("H", side lengths) must not overlap. Place the foot-point label (`"H"`) with `buff=0.2` in the direction AWAY from the right-angle mark.

6. **Step text vs previous step text** — **Always FadeOut previous calculation content before showing new content.** Never show two steps simultaneously unless they are intentionally designed to coexist and have been positioned to not overlap.

7. **Labels near the screen edge** — If a triangle vertex is near the left/right edge after shifting, its label may be clipped. Check that shifted coordinates + label offset stay within x ∈ [-6.5, 6.5], y ∈ [-3.5, 3.5].

8. **New labels on the figure vs existing labels** — When adding a computed value to the figure (e.g., BH ≈ 15.73), check it doesn't overlap with the vertex label, the side length label, or the angle label already there. If it would, fade or shift the conflicting element first.

## Right Panel Vertical Alignment

All content in the right calculation panel (step titles, body text, equations) MUST be center-aligned on the same vertical axis at `x = PX` (3.2).

**Use the built-in helpers** which enforce this automatically:
- `show_step_title()` — centers at PX
- `show_equation()` — centers at PX
- `show_equation_chain()` — centers at PX

If creating elements manually, ALWAYS call `.set_x(PX)` after vertical positioning:
```python
eq.next_to(ref, DOWN, buff=0.25)
eq.set_x(PX)  # REQUIRED — locks horizontal alignment
```

**Never** use `aligned_edge=LEFT` when positioning right-panel content relative to a previous element of different width — this causes horizontal drift and scattered appearance.

## Video Style Rules

1. **No bold fonts** — Never use `weight=BOLD`. Plain MathTex LaTeX font only.
2. **Use MathTex for everything** — Including Albanian text via `\text{}`. Never use `Text()` as it creates font inconsistency.
3. **Minimal colors** — Stick to the semantic color roles in `style_guide.py`. Don't rainbow things.
4. **Slow pacing** — 2-4 second waits after key equations, 1-2 seconds after routine steps. Better too slow than too fast.
5. **One thing at a time** — Show one equation, wait. Show the next, wait. Each equation gets its own moment.
6. **Clean transitions** — FadeOut everything before starting a new calculation section. Fresh screen for each phase.

## Video Content Depth — Grade-Aware Pacing

Videos must go DEEPER than the text solution on the website. The text solution is a cheat sheet; the video is a lesson.

**The audience is high school students and below.** The user will provide the grade and subject — adjust detail level accordingly. Lower grades need more hand-holding.

### Never Skip Algebra Steps

Every algebraic transformation must be shown as its own equation. Never combine multiple steps:

- **Bad:** `x²+(x+1)²-25=0 ⇒ 2x²+2x-24=0 ⇒ (x-3)(x+4)=0`
- **Good:** Show each step separately:
  1. `x² + (x+1)² = 25` — substitution
  2. `x² + x² + 2x + 1 = 25` — expand `(x+1)²`
  3. `2x² + 2x + 1 - 25 = 0` — move 25 to the left
  4. `2x² + 2x - 24 = 0` — simplify
  5. `x² + x - 12 = 0` — divide by 2
  6. Explain: "Two numbers that multiply to -12 and add to 1: that's 4 and -3"
  7. `(x+4)(x-3) = 0` — factor

### Add "Why" Text Before Non-Obvious Steps

Before every non-trivial operation, show a brief explanatory text line:

- Before expanding: `\text{Zhvillojmë katrorin e binomit:}`
- Before factoring: `\text{Gjejmë dy numra që shumëzojnë -12 dhe mbledhin 1}`
- Before quadratic formula: `\text{Përdorim formulën kuadratike me } a=5, b=4, c=-3`
- Before substitution: `\text{Zëvendësojmë } x \text{ në ekuacionin e dytë}`
- Before domain check: `\text{Kontrollojmë: argumenti i logaritmit duhet të jetë pozitiv}`

### Show Arithmetic Details

For high school level, show calculator-level computation:
- Discriminant: `\Delta = b^2-4ac = 4-4(5)(-3) = 4+60 = 64`
- Square root: `\sqrt{64} = 8`
- Don't just write `cos(51°) ≈ 0.6293` — show the substitution and multiplication

### General Content Principles

- **Explain "why"** before applying any rule or formula
- **Name the technique** so students recognize the pattern
- **Show intermediate steps** — don't skip anything
- **Add domain checks** for logs, roots, division — explain WHY we check, not just THAT we check
- **Connect to the bigger picture** — what type of problem is this?

## Geometry Diagram Quality Checklist

Before finishing any geometry diagram, verify ALL of these:

- [ ] Every vertex label is visible and not touching any line, arc, or other label
- [ ] Every side length label is outside the triangle with adequate spacing
- [ ] Every angle arc fits inside its angle and doesn't cross triangle sides
- [ ] Every angle label is readable and not covered by lines or other labels
- [ ] Tick marks (equal sides) don't overlap with side length numbers
- [ ] Construction lines (altitudes, medians) don't overlap with angle arcs at their endpoints
- [ ] Right-angle marks don't overlap with nearby labels
- [ ] After shifting the diagram left, all labels are still within screen bounds
- [ ] No two elements occupy the same visual space
- [ ] Every computed value is shown on the figure, not just on the right panel
- [ ] Sub-shapes being worked on are visually highlighted or extracted

## File Structure

- `scripts/style_guide.py` — Colors, sizes, timing, layout constants
- `scripts/components.py` — ExerciseScene base class with all reusable helpers
- `scripts/matematike/<book>/<unit>/ushtrimi<N>.py` — Individual exercise scripts

## Data Source

Get exercise data from mesonjetorja.com (deployed site), never from localhost or database directly.
