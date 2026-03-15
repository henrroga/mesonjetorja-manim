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

## Video Content Depth

Videos must go DEEPER than the text solution on the website. The text solution is a cheat sheet; the video is a lesson.

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
