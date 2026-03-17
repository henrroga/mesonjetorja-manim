"""
Mësonjëtorja Manim — Reusable Exercise Components
===================================================

Shared building blocks for exercise video scripts.
Import and subclass ExerciseScene for consistent exercise videos.

Usage:
    from components import ExerciseScene
"""

from manim import *
import numpy as np
from style_guide import (
    apply_style, make_divider, make_answer_box, fade_all,
    BG_COLOR, STEP_TITLE_COLOR, BODY_TEXT_COLOR, LABEL_COLOR,
    ANSWER_COLOR, SHAPE_COLOR, AUX_COLOR, HIGHLIGHT_COLOR, DIVIDER_COLOR,
    TITLE_SIZE, SUBTITLE_SIZE, PART_HEADER_SIZE, STEP_TITLE_SIZE,
    BODY_SIZE, PROBLEM_MATH_SIZE, CALC_SIZE, ANSWER_SIZE,
    DIAGRAM_LABEL_SIZE, DIAGRAM_VALUE_SIZE,
    T_TITLE_WRITE, T_SUBTITLE_FADE, T_HEADER_WRITE, T_STEP_TITLE,
    T_BODY_FADE, T_KEY_EQUATION, T_ROUTINE_EQUATION, T_SHAPE_CREATE,
    T_DOT_FADE, T_LAYOUT_SHIFT, T_TRANSITION,
    W_AFTER_KEY, W_AFTER_ROUTINE, W_AFTER_ANSWER, W_PROBLEM,
    DIAGRAM_CENTER, CALC_CENTER, CALC_TOP, DIVIDER_X,
    ALBANIAN_TEX,
)


# ──────────────────────────────────────────────
#  EXERCISE SCENE BASE CLASS
# ──────────────────────────────────────────────

class ExerciseScene(Scene):
    """
    Base class for all exercise video scenes.

    Subclass this and set the class attributes, then define part methods.

    Example:
        class Ushtrimi1(ExerciseScene):
            exercise_number = 1
            unit = "6.5A"
            textbook = "Matematika 10-11: Pjesa II"
            parts = ["a", "b", "c"]

            def part_a(self): ...
            def part_b(self): ...
            def part_c(self): ...
    """

    exercise_number: int = 0
    unit: str = ""
    textbook: str = "Matematika 10-11: Pjesa II"
    parts: list = []

    def construct(self):
        apply_style(self)
        # Enable Albanian characters (ë, ç) in all MathTex globally
        MathTex.set_default(tex_template=ALBANIAN_TEX)
        Tex.set_default(tex_template=ALBANIAN_TEX)
        self.title_screen()

        for part_name in self.parts:
            method = getattr(self, f"part_{part_name}")
            method()
            fade_all(self)
            self.wait(0.5)

        if hasattr(self, "final_summary"):
            self.final_summary()
            self.wait(W_AFTER_ANSWER)

    # ──────────────────────────────────────────
    #  TITLE SCREEN
    # ──────────────────────────────────────────

    def title_screen(self):
        """Standard animated title screen."""
        title = MathTex(
            r"\text{Ushtrimi " + str(self.exercise_number) + r" — Njësia " + self.unit + r"}",
            font_size=TITLE_SIZE,
            color=WHITE,
        )
        source = MathTex(
            r"\text{" + self.textbook + r"}",
            font_size=SUBTITLE_SIZE,
            color=BODY_TEXT_COLOR,
        )
        source.next_to(title, DOWN, buff=0.4)

        self.play(Write(title), run_time=T_TITLE_WRITE)
        self.play(FadeIn(source, shift=UP * 0.2), run_time=T_SUBTITLE_FADE)
        self.wait(W_AFTER_KEY)
        self.play(FadeOut(title), FadeOut(source))
        self.wait(0.5)

    # ──────────────────────────────────────────
    #  PART HEADER
    # ──────────────────────────────────────────

    def show_part_header(self, label):
        """
        Show a part header in the top-left corner (e.g. "Pjesa a)").

        Returns the header mobject for later reference.
        """
        header = MathTex(
            r"\text{Pjesa " + label + r")}",
            font_size=PART_HEADER_SIZE,
            color=LABEL_COLOR,
        )
        header.to_corner(UL, buff=0.4)
        self.play(Write(header), run_time=T_HEADER_WRITE)
        return header

    # ──────────────────────────────────────────
    #  PROBLEM STATEMENT
    # ──────────────────────────────────────────

    def show_problem(self, *content, wait_time=None):
        """
        Display a centered problem statement, wait, then fade it out.

        Args:
            *content: Mobjects to arrange vertically (titles, equations, etc.)
            wait_time: How long to display (default: W_PROBLEM)
        """
        wt = wait_time if wait_time is not None else W_PROBLEM
        group = VGroup(*content).arrange(DOWN, buff=0.4).move_to(ORIGIN)

        self.play(FadeIn(group, shift=UP * 0.3), run_time=T_SHAPE_CREATE)
        self.wait(wt)
        self.play(FadeOut(group), run_time=T_TRANSITION)
        self.wait(0.3)

    # ──────────────────────────────────────────
    #  ANSWER BOX
    # ──────────────────────────────────────────

    def show_answer(self, answer_tex, position=None, font_size=None):
        """
        Display a final answer with a surrounding box.

        Args:
            answer_tex: LaTeX string for the answer.
            position: Where to place (defaults to ORIGIN).
            font_size: Font size (defaults to ANSWER_SIZE).

        Returns:
            Tuple of (answer_mobject, box_mobject).
        """
        fs = font_size or ANSWER_SIZE
        ans = MathTex(answer_tex, font_size=fs, color=ANSWER_COLOR)
        if position is not None:
            ans.move_to(position)
        box = make_answer_box(ans)

        self.play(Write(ans), run_time=T_KEY_EQUATION)
        self.play(Create(box), run_time=0.5)
        self.wait(W_AFTER_ANSWER)
        return ans, box

    def show_answer_below(self, answer_tex, reference, buff=0.5, font_size=None):
        """
        Display a final answer below a reference mobject.

        Args:
            answer_tex: LaTeX string for the answer.
            reference: Mobject to place the answer below.
            buff: Vertical spacing.
            font_size: Font size (defaults to ANSWER_SIZE).

        Returns:
            Tuple of (answer_mobject, box_mobject).
        """
        fs = font_size or ANSWER_SIZE
        ans = MathTex(answer_tex, font_size=fs, color=ANSWER_COLOR)
        ans.next_to(reference, DOWN, buff=buff)
        box = make_answer_box(ans)

        self.play(Write(ans), run_time=T_KEY_EQUATION)
        self.play(Create(box), run_time=0.5)
        self.wait(W_AFTER_ANSWER)
        return ans, box

    # ──────────────────────────────────────────
    #  SUMMARY TABLE
    # ──────────────────────────────────────────

    def show_summary_table(self, title_text, rows, font_size=28):
        """
        Display a final summary with all answers in a boxed list.

        The box is centered on screen with generous spacing to avoid
        overlaps between rows and between the title and box.

        Args:
            title_text: Title for the summary (e.g. "Përmbledhje").
            rows: List of LaTeX strings for each row.
            font_size: Font size for rows.
        """
        title = MathTex(
            r"\text{" + title_text + r"}",
            font_size=PART_HEADER_SIZE + 4,
            color=WHITE,
        )
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=T_TITLE_WRITE)

        row_group = VGroup(
            *[MathTex(r, font_size=font_size, color=ANSWER_COLOR) for r in rows]
        )
        row_group.arrange(DOWN, buff=0.45, aligned_edge=LEFT)

        box = make_answer_box(row_group)

        # Center the box+rows on screen, below the title with generous gap
        content = VGroup(row_group, box)
        content.move_to(ORIGIN).shift(DOWN * 0.3)

        # Ensure it doesn't overlap with title
        if content.get_top()[1] > title.get_bottom()[1] - 0.4:
            content.next_to(title, DOWN, buff=0.5)

        self.play(
            LaggedStart(
                *[FadeIn(r, shift=RIGHT * 0.3) for r in row_group],
                lag_ratio=0.15,
            ),
            run_time=2.0,
        )
        self.play(Create(box), run_time=0.6)

    # ──────────────────────────────────────────
    #  GRAPH HELPERS
    # ──────────────────────────────────────────

    def create_axes(self, x_bound, y_bound, step=None, x_length=5.5, y_length=5.5):
        """
        Create standard Axes for graphing.

        Args:
            x_bound: Symmetric range for x-axis (creates [-x_bound, x_bound]).
            y_bound: Symmetric range for y-axis.
            step: Tick spacing (auto-calculated if None).
            x_length: Visual width.
            y_length: Visual height.
        """
        s = step or max(1, x_bound // 4)
        return Axes(
            x_range=[-x_bound, x_bound, s],
            y_range=[-y_bound, y_bound, s],
            x_length=x_length,
            y_length=y_length,
            axis_config={
                "include_tip": True,
                "include_numbers": True,
                "font_size": 18,
                "color": DIVIDER_COLOR,
            },
        )

    def plot_circle(self, axes, radius, color=None, stroke_width=3):
        """
        Plot a circle centered at origin on the given axes.

        Returns the parametric curve mobject.
        """
        c = color or SHAPE_COLOR
        return axes.plot_parametric_curve(
            lambda t: np.array([radius * np.cos(t), radius * np.sin(t), 0]),
            t_range=[0, 2 * PI],
            color=c,
            stroke_width=stroke_width,
        )

    def mark_point(self, axes, x, y, label_tex, color=None,
                   direction=UR, font_size=22, radius=0.1):
        """
        Create a dot and label at a point on axes.

        Returns (dot, label) tuple.
        """
        c = color or LABEL_COLOR
        dot = Dot(axes.c2p(x, y), color=c, radius=radius)
        lbl = MathTex(label_tex, font_size=font_size, color=c)
        lbl.next_to(dot, direction, buff=0.15)
        return dot, lbl

    def mark_points(self, axes, points, labels, colors=None, directions=None,
                    font_size=22, radius=0.1):
        """
        Mark multiple points on axes.

        Args:
            axes: The Axes object.
            points: List of (x, y) tuples.
            labels: List of LaTeX label strings.
            colors: List of colors (defaults to alternating LABEL_COLOR/HIGHLIGHT_COLOR).
            directions: List of label directions (defaults to UR).

        Returns list of (dot, label) tuples.
        """
        default_colors = [LABEL_COLOR, HIGHLIGHT_COLOR]
        result = []
        for i, ((x, y), lbl_tex) in enumerate(zip(points, labels)):
            c = colors[i] if colors else default_colors[i % len(default_colors)]
            d = directions[i] if directions else UR
            dot, lbl = self.mark_point(axes, x, y, lbl_tex, color=c,
                                       direction=d, font_size=font_size, radius=radius)
            result.append((dot, lbl))
        return result

    # ──────────────────────────────────────────
    #  SPLIT LAYOUT (Graph left, Calc right)
    # ──────────────────────────────────────────

    def setup_split_layout(self, graph_group):
        """
        Shift a graph group to the left and add a divider.

        Args:
            graph_group: VGroup of all graph elements.

        Returns the divider mobject.
        """
        self.play(graph_group.animate.shift(LEFT * 3.2), run_time=T_LAYOUT_SHIFT)
        div = make_divider()
        self.play(FadeIn(div), run_time=0.2)
        return div

    # ──────────────────────────────────────────
    #  STEP-BY-STEP CALCULATIONS
    # ──────────────────────────────────────────

    def show_step_title(self, text, position=None, reference=None, buff=0.4):
        """
        Show a step title (e.g. "Hapi 1: Zëvendësimi").

        All titles are center-aligned at x = CALC_CENTER to maintain
        a consistent vertical axis in the right panel.

        Args:
            text: Step title text.
            position: Absolute position (takes precedence).
            reference: Place below this mobject if position is None.
            buff: Spacing from reference.

        Returns the title mobject.
        """
        title = MathTex(
            r"\text{" + text + r"}",
            font_size=STEP_TITLE_SIZE,
            color=STEP_TITLE_COLOR,
        )
        if position is not None:
            title.move_to(position)
            title.set_x(CALC_CENTER[0])
        elif reference is not None:
            title.next_to(reference, DOWN, buff=buff)
            title.set_x(CALC_CENTER[0])
        else:
            title.move_to(CALC_TOP)

        self.play(FadeIn(title), run_time=T_STEP_TITLE)
        return title

    def show_equation(self, tex, reference=None, buff=0.25, key=False,
                      color=None, font_size=None):
        """
        Show a single equation below a reference.

        Equations are center-aligned at x = CALC_CENTER to maintain
        a consistent vertical axis in the right panel.

        Args:
            tex: LaTeX string.
            reference: Mobject to position below.
            buff: Vertical spacing.
            key: If True, use longer animation time and wait.
            color: Equation color.
            font_size: Font size (defaults to CALC_SIZE).

        Returns the equation mobject.
        """
        fs = font_size or CALC_SIZE
        eq = MathTex(tex, font_size=fs)
        if color:
            eq.set_color(color)
        if reference is not None:
            eq.next_to(reference, DOWN, buff=buff)
            eq.set_x(CALC_CENTER[0])

        rt = T_KEY_EQUATION if key else T_ROUTINE_EQUATION
        self.play(Write(eq), run_time=rt)
        if key:
            self.wait(W_AFTER_KEY)
        else:
            self.wait(0.6)
        return eq

    def show_equation_chain(self, equations, start_position=None, start_reference=None,
                            buff=0.25, key_indices=None):
        """
        Show a chain of equations sequentially.

        All equations are center-aligned at x = CALC_CENTER to maintain
        a consistent vertical axis in the right panel.

        Args:
            equations: List of dicts with keys:
                - "tex": LaTeX string (required)
                - "color": Color (optional)
                - "font_size": Size (optional)
                - "key": Whether this is a key equation (optional)
            start_position: Where to place the first equation.
            start_reference: Mobject to start below.
            buff: Spacing between equations.
            key_indices: Set of indices that are key equations.

        Returns list of equation mobjects.
        """
        key_set = set(key_indices or [])
        results = []

        for i, eq_spec in enumerate(equations):
            if isinstance(eq_spec, str):
                eq_spec = {"tex": eq_spec}

            is_key = eq_spec.get("key", i in key_set)
            color = eq_spec.get("color")
            fs = eq_spec.get("font_size")

            if i == 0:
                ref = start_reference
                eq = MathTex(eq_spec["tex"], font_size=fs or CALC_SIZE)
                if color:
                    eq.set_color(color)
                if start_position is not None:
                    eq.move_to(start_position)
                    eq.set_x(CALC_CENTER[0])
                elif ref is not None:
                    eq.next_to(ref, DOWN, buff=0.3)
                    eq.set_x(CALC_CENTER[0])
            else:
                ref = results[-1]
                eq = MathTex(eq_spec["tex"], font_size=fs or CALC_SIZE)
                if color:
                    eq.set_color(color)
                eq.next_to(ref, DOWN, buff=buff)
                eq.set_x(CALC_CENTER[0])

            rt = T_KEY_EQUATION if is_key else T_ROUTINE_EQUATION
            self.play(Write(eq), run_time=rt)
            if is_key:
                self.wait(W_AFTER_KEY if i == len(equations) - 1 else W_AFTER_ROUTINE)
            else:
                self.wait(0.6)

            results.append(eq)

        return results

    # ──────────────────────────────────────────
    #  ALIGNED PANEL HELPERS (right-panel at PX)
    # ──────────────────────────────────────────

    def panel_title(self, text, ref=None, y_pos=None, buff=0.5):
        """Show a step title centered at x=PX in the right panel."""
        t = MathTex(
            r"\text{" + text + r"}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        if y_pos is not None:
            t.move_to(np.array([CALC_CENTER[0], y_pos, 0]))
        elif ref is not None:
            t.next_to(ref, DOWN, buff=buff)
            t.set_x(CALC_CENTER[0])
        self.play(FadeIn(t), run_time=T_STEP_TITLE)
        return t

    def panel_text(self, lines, ref, buff=0.25):
        """Show multi-line body text centered at x=PX in the right panel."""
        parts = [MathTex(l, font_size=BODY_SIZE, color=BODY_TEXT_COLOR) for l in lines]
        g = VGroup(*parts).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        g.next_to(ref, DOWN, buff=buff)
        g.set_x(CALC_CENTER[0])
        self.play(FadeIn(g), run_time=T_BODY_FADE)
        return g

    def panel_eq(self, tex, ref, buff=0.25, color=None, font_size=None, key=False):
        """Show an equation centered at x=PX in the right panel."""
        fs = font_size or CALC_SIZE
        eq = MathTex(tex, font_size=fs)
        if color:
            eq.set_color(color)
        eq.next_to(ref, DOWN, buff=buff)
        eq.set_x(CALC_CENTER[0])
        rt = T_KEY_EQUATION if key else T_ROUTINE_EQUATION
        self.play(Write(eq), run_time=rt)
        self.wait(W_AFTER_KEY if key else 0.6)
        return eq

    def transfer_value(self, source_eq, target_mob):
        """Animate a value flying from the right panel to the figure."""
        ghost = source_eq.copy()
        self.play(
            ghost.animate.move_to(target_mob).scale(0.65).set_opacity(0),
            FadeIn(target_mob),
            run_time=0.8,
        )
        self.remove(ghost)

    # ──────────────────────────────────────────
    #  CENTERED HELPERS (full-screen, no split)
    # ──────────────────────────────────────────

    def centered_title(self, text, ref=None, y_pos=None, buff=0.5):
        """Show a step title centered on screen (for full-screen algebra)."""
        t = MathTex(
            r"\text{" + text + r"}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        if y_pos is not None:
            t.move_to(np.array([0, y_pos, 0]))
        elif ref is not None:
            t.next_to(ref, DOWN, buff=buff)
            t.set_x(0)
        self.play(FadeIn(t), run_time=T_STEP_TITLE)
        return t

    def centered_text(self, lines, ref, buff=0.25):
        """Show multi-line body text centered on screen."""
        parts = [MathTex(l, font_size=BODY_SIZE, color=BODY_TEXT_COLOR) for l in lines]
        g = VGroup(*parts).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        g.next_to(ref, DOWN, buff=buff)
        g.set_x(0)
        self.play(FadeIn(g), run_time=T_BODY_FADE)
        return g

    def centered_eq(self, tex, ref, buff=0.25, color=None, font_size=None, key=False):
        """Show an equation centered on screen."""
        fs = font_size or CALC_SIZE
        eq = MathTex(tex, font_size=fs)
        if color:
            eq.set_color(color)
        eq.next_to(ref, DOWN, buff=buff)
        eq.set_x(0)
        rt = T_KEY_EQUATION if key else T_ROUTINE_EQUATION
        self.play(Write(eq), run_time=rt)
        self.wait(W_AFTER_KEY if key else 0.6)
        return eq

    # ──────────────────────────────────────────
    #  VISUAL TOOLKIT — Enhanced Animations
    # ──────────────────────────────────────────

    def highlight_result(self, mobject, color=None):
        """
        Emphasize a result with Circumscribe + Flash.

        Use on final answers, key intermediate results, or boxed equations.
        More visually impactful than just a SurroundingRectangle.
        """
        c = color or ANSWER_COLOR
        self.play(Circumscribe(mobject, color=c, run_time=0.8))
        self.play(
            Flash(mobject.get_center(), color=c,
                  line_length=0.15, num_lines=8, run_time=0.4),
        )

    def morph_equation(self, old_eq, new_tex, font_size=None, color=None,
                       position=None, key_map=None,
                       transform_mismatches=False):
        """
        Morph one equation into another using TransformMatchingTex.

        Matching symbols stay in place; changed parts animate smoothly.
        Perfect for algebraic simplification steps.

        IMPORTANT: For best results, use {{double braces}} around the
        parts you want to match independently. Example:
            old: MathTex("{{x}}^2", "+", "{{y}}^2", "=", "{{25}}")
            new: MathTex("{{r}}^2", "=", "{{25}}")
        The "=" and "25" will stay in place; "x^2 +" and "y^2" will
        morph into "r^2".

        Args:
            old_eq: The current equation mobject on screen.
            new_tex: LaTeX string for the new equation (use {{}} for parts).
            font_size: Font size (defaults to old_eq's size or CALC_SIZE).
            color: Color for the new equation.
            position: Where to place the new eq (defaults to old_eq's pos).
            key_map: Dict mapping old keys to new keys for variable
                     substitution. E.g., {"x": "a", "y": "b"}.
            transform_mismatches: If True, unmatched parts Transform
                     instead of fading. Set True for cleaner morphs.

        Returns the new equation mobject.
        """
        fs = font_size or CALC_SIZE
        new_eq = MathTex(new_tex, font_size=fs)
        if color:
            new_eq.set_color(color)
        if position is not None:
            new_eq.move_to(position)
        else:
            new_eq.move_to(old_eq)
        self.play(
            TransformMatchingTex(
                old_eq, new_eq,
                key_map=key_map or {},
                transform_mismatches=transform_mismatches,
            ),
            run_time=T_KEY_EQUATION,
        )
        self.wait(0.6)
        return new_eq

    def morph_shape(self, old_mob, new_mob, run_time=None,
                    fade_transform_mismatches=True):
        """
        Morph one geometric shape/group into another by matching shapes.

        Matching submobjects (by normalized shape hash) stay in place;
        others fade-transform. Perfect for geometry transformations.

        Use for:
        - Full triangle → sub-triangle (matching sides stay)
        - Circle with labels → same circle with different labels
        - Rearranging a figure while keeping common parts stable

        Args:
            old_mob: The current shape/group on screen.
            new_mob: The target shape/group.
            run_time: Duration (defaults to T_KEY_EQUATION).
            fade_transform_mismatches: If True, unmatched parts
                     FadeTransform (smoother). Default: True.

        Returns the new mobject.
        """
        rt = run_time or T_KEY_EQUATION
        self.play(
            TransformMatchingShapes(
                old_mob, new_mob,
                fade_transform_mismatches=fade_transform_mismatches,
            ),
            run_time=rt,
        )
        self.wait(0.6)
        return new_mob

    def reveal_sequence(self, mobjects, lag_ratio=0.15, direction=RIGHT,
                        run_time=1.5):
        """
        Reveal multiple mobjects sequentially with LaggedStart.

        Use when showing 3+ items: intercept points, colored balls,
        equation terms, summary rows. Creates visual rhythm.
        """
        self.play(
            LaggedStart(
                *[FadeIn(m, shift=direction * 0.3) for m in mobjects],
                lag_ratio=lag_ratio,
            ),
            run_time=run_time,
        )

    def trace_path(self, dot, path, run_time=2.0, color=None):
        """
        Animate a dot moving along a path (circle, line, curve).

        Use to demonstrate that a point satisfies an equation,
        or to visually trace a geometric construction.
        """
        if color:
            dot.set_color(color)
        self.play(
            MoveAlongPath(dot, path),
            run_time=run_time,
            rate_func=rate_functions.smooth,
        )

    def flash_point(self, point, color=None, radius=0.3):
        """
        Flash a point on the figure to draw attention.

        Use when an intersection point is found, or when marking
        a special location on a graph.
        """
        c = color or LABEL_COLOR
        if hasattr(point, 'get_center'):
            pos = point.get_center()
        else:
            pos = np.array(point)
        self.play(
            Flash(pos, color=c, line_length=0.12,
                  num_lines=8, flash_radius=radius, run_time=0.5),
        )

    def glow_trace(self, path_mobject, color=None, time_width=0.3,
                   stroke_width=8, run_time=1.5):
        """
        Send a glowing sliver of light traveling along a curve.

        Use for: "this is the circle", tracing a triangle side,
        showing a line segment, scanning an edge. Creates a neon
        glow that travels along the path.

        Args:
            path_mobject: A VMobject (Circle, Line, Polygon side, Arc, etc.)
            color: Glow color (defaults to LABEL_COLOR / yellow).
            time_width: How wide the glow sliver is (0.1=thin, 0.5=wide).
            stroke_width: Thickness of the glow.
            run_time: Duration.
        """
        c = color or LABEL_COLOR
        glow = path_mobject.copy().set_stroke(color=c, width=stroke_width)
        self.play(
            ShowPassingFlash(glow, time_width=time_width, run_time=run_time),
        )

    def focus_on(self, target, color=None, opacity=0.2, run_time=1.0):
        """
        Shrink a spotlight onto a target — "now look HERE".

        Use for: directing attention to a specific part of the figure
        before starting a calculation on it. Essential for no-voiceover
        videos where you need to tell the viewer WHERE to look.

        Args:
            target: A Mobject or point to focus on.
            color: Spotlight color (defaults to dim gray).
            opacity: How opaque the spotlight circle is.
            run_time: Duration.
        """
        c = color or GRAY
        self.play(FocusOn(target, color=c, opacity=opacity, run_time=run_time))

    def celebrate(self, mobject, run_time=1.5):
        """
        Wave + Flash celebration on a final result.

        Use for: the absolute final answer of the entire exercise,
        major milestones. More dramatic than highlight_result.
        """
        self.play(ApplyWave(mobject, amplitude=0.15, run_time=run_time * 0.6))
        self.play(
            Flash(mobject.get_center(), color=ANSWER_COLOR,
                  line_length=0.3, num_lines=12, run_time=run_time * 0.4),
        )

    # ──────────────────────────────────────────
    #  DYNAMIC / UPDATER HELPERS
    # ──────────────────────────────────────────

    def animated_counter(self, start, end, prefix="", suffix="",
                         font_size=None, color=None, position=None,
                         run_time=1.5, num_decimal_places=0):
        """
        Animate a number rolling from start to end using ChangeDecimalToValue.

        Uses Manim's built-in ChangeDecimalToValue for smooth interpolation.

        Use for: counting balls, showing a computed value appearing
        gradually, progress indicators, totals.

        Args:
            start: Starting value.
            end: Final value.
            prefix: Text before the number (e.g., "Total: ").
            suffix: Text after the number (e.g., " cm").
            font_size: Size (defaults to CALC_SIZE).
            color: Color (defaults to ANSWER_COLOR).
            position: Where to place (defaults to ORIGIN).
            run_time: Duration of the animation.
            num_decimal_places: Decimal precision (0 for integers).

        Returns the group containing prefix + number + suffix.
        """
        fs = font_size or CALC_SIZE
        c = color or ANSWER_COLOR

        number = DecimalNumber(
            start,
            num_decimal_places=num_decimal_places,
            font_size=fs,
            color=c,
        )

        # Build group with optional prefix/suffix
        group = VGroup()

        if prefix:
            pre_label = MathTex(
                r"\text{" + prefix + r"}",
                font_size=fs, color=c,
            )
            group.add(pre_label)

        group.add(number)

        if suffix:
            suf_label = MathTex(
                r"\text{" + suffix + r"}",
                font_size=fs, color=c,
            )
            group.add(suf_label)

        group.arrange(RIGHT, buff=0.15)
        if position is not None:
            group.move_to(position)

        self.add(group)
        self.play(
            ChangeDecimalToValue(number, end),
            run_time=run_time,
        )

        return group

    def fraction_bar(self, numerator, denominator, width=4.0, height=0.4,
                     color=None, bg_color=None, position=None,
                     run_time=1.0):
        """
        Show a visual fraction bar that fills proportionally.

        Use for: probability (P = 15/22 fills 68%), percentages,
        progress visualization, ratio comparisons.

        Args:
            numerator: The favorable count.
            denominator: The total count.
            width: Bar width in scene units.
            height: Bar height.
            color: Fill color (defaults to ANSWER_COLOR).
            bg_color: Background bar color (defaults to dim gray).
            position: Where to place.
            run_time: Fill animation duration.

        Returns (bar_group, fill_rect) for later reference.
        """
        c = color or ANSWER_COLOR
        bg = bg_color or DIVIDER_COLOR

        ratio = numerator / denominator
        fill_width = width * ratio

        # Background bar (full width)
        bg_rect = Rectangle(
            width=width, height=height,
            fill_color=bg, fill_opacity=0.3,
            stroke_color=bg, stroke_width=1,
        )

        # Fill bar (starts at zero width, animates to ratio)
        fill_rect = Rectangle(
            width=0.001, height=height,
            fill_color=c, fill_opacity=0.7,
            stroke_width=0,
        )
        fill_rect.align_to(bg_rect, LEFT)

        bar_group = VGroup(bg_rect, fill_rect)
        if position is not None:
            bar_group.move_to(position)

        # Label: "15/22"
        label = MathTex(
            f"\\frac{{{numerator}}}{{{denominator}}}",
            font_size=24, color=c,
        )
        label.next_to(bar_group, RIGHT, buff=0.2)

        self.play(FadeIn(bg_rect), run_time=0.3)
        self.play(
            fill_rect.animate.stretch_to_fit_width(fill_width).align_to(bg_rect, LEFT),
            FadeIn(label),
            run_time=run_time,
        )

        bar_group.add(label)
        return bar_group, fill_rect

    def linked_label(self, target, tex, font_size=None, color=None,
                     direction=UP, buff=0.2):
        """
        Create a label that always stays attached to a moving mobject.

        Use for: labels on points that move along paths, dynamic
        geometry where vertices shift, parameter-dependent labels.

        Args:
            target: The mobject to track.
            tex: LaTeX string for the label.
            font_size: Size (defaults to DIAGRAM_VALUE_SIZE).
            color: Color (defaults to LABEL_COLOR).
            direction: Where relative to target (UP, DOWN, UR, etc.).
            buff: Distance from target.

        Returns the label mobject (with updater attached).
        """
        fs = font_size or DIAGRAM_VALUE_SIZE
        c = color or LABEL_COLOR

        label = MathTex(tex, font_size=fs, color=c)
        label.next_to(target, direction, buff=buff)
        label.add_updater(
            lambda m: m.next_to(target, direction, buff=buff)
        )
        return label

    def animate_parameter(self, tracker, start, end, mobjects_to_update,
                          run_time=3.0, rate_func=None):
        """
        Animate a ValueTracker change with dependent mobjects updating.

        Use for: showing how changing radius affects a circle,
        how slope changes a line, parameter exploration.

        Args:
            tracker: A ValueTracker controlling the parameter.
            start: Starting value.
            end: Ending value.
            mobjects_to_update: List of mobjects with updaters attached.
            run_time: Animation duration.
            rate_func: Easing function.

        Example:
            r_tracker = ValueTracker(1)
            circle = always_redraw(
                lambda: Circle(radius=r_tracker.get_value(), color=SHAPE_COLOR)
            )
            self.add(circle)
            self.animate_parameter(r_tracker, 1, 5, [circle], run_time=3)
        """
        rf = rate_func or rate_functions.smooth
        tracker.set_value(start)
        self.play(
            tracker.animate.set_value(end),
            run_time=run_time,
            rate_func=rf,
        )

    # ──────────────────────────────────────────
    #  GEOMETRY HELPERS
    # ──────────────────────────────────────────

    # ──────────────────────────────────────────
    #  CIRCLE GRAPH WITH INTERCEPTS
    # ──────────────────────────────────────────

    def show_circle_graph(
        self, r_val, r_sq, eq_str, r_str,
        intercepts_x, intercepts_y,
        x_labels, y_labels,
        axis_bound=None,
    ):
        """
        Draw a circle on axes with labeled axis intercepts.

        Used for exercises about circle equations and their graphs.

        Args:
            r_val: Numeric radius value.
            r_sq: Radius squared (for display).
            eq_str: LaTeX for circle equation.
            r_str: LaTeX for radius display.
            intercepts_x: List of (x, y) tuples for x-axis intercepts.
            intercepts_y: List of (x, y) tuples for y-axis intercepts.
            x_labels: List of LaTeX strings for x-intercept labels.
            y_labels: List of LaTeX strings for y-intercept labels.
            axis_bound: Axis range (auto-calculated if None).
        """
        bound = axis_bound or int(r_val + 2)
        step = max(1, bound // 4)

        axes = self.create_axes(bound, bound, step=step, x_length=6, y_length=6)
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")

        circle = self.plot_circle(axes, r_val)

        # Equation and radius labels
        eq_label = MathTex(eq_str, font_size=24, color=SHAPE_COLOR)
        eq_label.to_corner(UR, buff=0.5)
        r_label = MathTex(r_str, font_size=24, color=ANSWER_COLOR)
        r_label.next_to(eq_label, DOWN, buff=0.2)

        # Radius line from origin to (r, 0)
        r_line = DashedLine(
            axes.c2p(0, 0), axes.c2p(r_val, 0),
            color=ANSWER_COLOR, dash_length=0.08, stroke_width=2,
        )
        r_mid_label = MathTex(r_str, font_size=20, color=ANSWER_COLOR)
        r_mid_label.next_to(r_line, UP, buff=0.15)

        # Intercept dots and labels
        dots_and_labels = VGroup()

        for i, (pt, lbl_str) in enumerate(zip(intercepts_x, x_labels)):
            dot = Dot(axes.c2p(pt[0], pt[1]), color=LABEL_COLOR, radius=0.08)
            lbl = MathTex(lbl_str, font_size=20, color=LABEL_COLOR)
            lbl.next_to(dot, DL if i == 0 else DR, buff=0.12)
            dots_and_labels.add(dot, lbl)

        for i, (pt, lbl_str) in enumerate(zip(intercepts_y, y_labels)):
            dot = Dot(axes.c2p(pt[0], pt[1]), color=HIGHLIGHT_COLOR, radius=0.08)
            lbl = MathTex(lbl_str, font_size=20, color=HIGHLIGHT_COLOR)
            lbl.next_to(dot, DL if i == 0 else UL, buff=0.12)
            dots_and_labels.add(dot, lbl)

        # Animate
        self.play(Create(axes), FadeIn(axes_labels), run_time=T_SHAPE_CREATE)
        self.play(Create(circle), run_time=T_SHAPE_CREATE)
        self.play(FadeIn(eq_label), FadeIn(r_label), run_time=T_BODY_FADE)
        self.play(Create(r_line), FadeIn(r_mid_label), run_time=T_ROUTINE_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        self.play(
            LaggedStart(
                *[FadeIn(obj, scale=1.3) for obj in dots_and_labels],
                lag_ratio=0.1,
            ),
            run_time=1.5,
        )
        self.wait(W_AFTER_ANSWER)

    # ──────────────────────────────────────────
    #  GEOMETRY HELPERS
    # ──────────────────────────────────────────

    # ──────────────────────────────────────────
    #  ASYMMETRIC / CUSTOM AXES
    # ──────────────────────────────────────────

    def create_axes_custom(self, x_range, y_range, x_length=6, y_length=5.5,
                           include_numbers=True, font_size=18):
        """
        Create Axes with independent x/y ranges.

        Unlike create_axes() which assumes symmetric ranges, this supports
        any [min, max, step] for each axis. Useful for exponential, log,
        and trig graphs where the domain/range aren't symmetric.

        Args:
            x_range: [x_min, x_max, x_step]
            y_range: [y_min, y_max, y_step]
            x_length: Visual width.
            y_length: Visual height.
            include_numbers: Show tick numbers.
            font_size: Number font size.
        """
        return Axes(
            x_range=x_range,
            y_range=y_range,
            x_length=x_length,
            y_length=y_length,
            axis_config={
                "include_tip": True,
                "include_numbers": include_numbers,
                "font_size": font_size,
                "color": DIVIDER_COLOR,
            },
        )

    # ──────────────────────────────────────────
    #  FUNCTION GRAPHING
    # ──────────────────────────────────────────

    def plot_function(self, axes, func, x_range, color=None,
                      stroke_width=2.5, label_tex=None, label_direction=UR):
        """
        Plot a function on axes with an optional label.

        Args:
            axes: Axes object.
            func: Callable f(x) -> y.
            x_range: [x_min, x_max] for the plot domain.
            color: Curve color (defaults to SHAPE_COLOR).
            stroke_width: Line width.
            label_tex: LaTeX label (e.g. r"y = x^2"). None to skip.
            label_direction: Where to place label relative to curve end.

        Returns:
            (curve, label) tuple. label is None if label_tex is None.
        """
        c = color or SHAPE_COLOR
        curve = axes.plot(func, x_range=x_range, color=c, stroke_width=stroke_width)
        lbl = None
        if label_tex:
            lbl = MathTex(label_tex, font_size=20, color=c)
            lbl.next_to(curve.point_from_proportion(0.85), label_direction, buff=0.1)
        return curve, lbl

    def show_function_graph(self, functions, x_range_axes, y_range_axes,
                            points=None, point_labels=None,
                            show_roots=False, animate_construction=True):
        """
        Full animated function graph with curves, points, and labels.

        Useful for: quadratic, exponential, logarithmic, trigonometric exercises.

        Args:
            functions: List of dicts, each with:
                - "func": callable f(x) -> y
                - "x_range": [x_min, x_max] for plot domain
                - "label": LaTeX label string (optional)
                - "color": color (optional, cycles through SHAPE/AUX/HIGHLIGHT)
            x_range_axes: [x_min, x_max, step] for axes
            y_range_axes: [y_min, y_max, step] for axes
            points: List of (x, y) tuples to mark (optional)
            point_labels: List of LaTeX labels for points (optional)
            show_roots: If True, mark x-intercepts of first function.
            animate_construction: If True, animate each element.

        Returns:
            (axes, graph_group) — graph_group contains all elements.
        """
        default_colors = [SHAPE_COLOR, AUX_COLOR, HIGHLIGHT_COLOR, LABEL_COLOR]

        axes = self.create_axes_custom(x_range_axes, y_range_axes)
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")

        all_elements = [axes, axes_labels]
        curves = []

        if animate_construction:
            self.play(Create(axes), FadeIn(axes_labels), run_time=T_SHAPE_CREATE)

        for i, f_spec in enumerate(functions):
            c = f_spec.get("color", default_colors[i % len(default_colors)])
            curve, lbl = self.plot_function(
                axes, f_spec["func"], f_spec["x_range"],
                color=c, label_tex=f_spec.get("label"),
            )
            curves.append(curve)
            all_elements.append(curve)
            if lbl:
                all_elements.append(lbl)

            if animate_construction:
                anims = [Create(curve)]
                if lbl:
                    anims.append(FadeIn(lbl))
                self.play(*anims, run_time=T_SHAPE_CREATE)

        # Mark specific points
        if points:
            labels = point_labels or [f"({x},\\,{y})" for x, y in points]
            for j, ((px, py), lbl_tex) in enumerate(zip(points, labels)):
                dot, lbl = self.mark_point(
                    axes, px, py, lbl_tex,
                    color=default_colors[j % len(default_colors)],
                )
                all_elements.extend([dot, lbl])
                if animate_construction:
                    self.play(FadeIn(dot, scale=1.5), FadeIn(lbl), run_time=T_DOT_FADE + 0.2)

        # Mark roots of first function
        if show_roots and curves:
            root_dots = self._find_and_mark_roots(axes, functions[0]["func"],
                                                   functions[0]["x_range"])
            all_elements.extend(root_dots)
            if animate_construction and root_dots:
                self.play(
                    *[FadeIn(d, scale=1.3) for d in root_dots],
                    run_time=T_DOT_FADE + 0.3,
                )

        graph_group = VGroup(*all_elements)
        return axes, graph_group

    def _find_and_mark_roots(self, axes, func, x_range, tol=0.01, n_samples=500):
        """Find approximate roots of func in x_range and mark them on axes."""
        x_min, x_max = x_range[0], x_range[1]
        xs = np.linspace(x_min, x_max, n_samples)
        ys = np.array([func(x) for x in xs])

        roots = []
        for i in range(len(ys) - 1):
            if ys[i] * ys[i + 1] <= 0:
                # Linear interpolation for root
                if abs(ys[i + 1] - ys[i]) > 1e-12:
                    root_x = xs[i] - ys[i] * (xs[i + 1] - xs[i]) / (ys[i + 1] - ys[i])
                else:
                    root_x = (xs[i] + xs[i + 1]) / 2
                roots.append(root_x)

        elements = []
        for rx in roots:
            dot = Dot(axes.c2p(rx, 0), color=LABEL_COLOR, radius=0.08)
            # Format root label nicely
            if abs(rx - round(rx)) < tol:
                lbl_str = f"({int(round(rx))},\\,0)"
            else:
                lbl_str = f"({rx:.2f},\\,0)"
            lbl = MathTex(lbl_str, font_size=20, color=LABEL_COLOR)
            lbl.next_to(dot, DOWN, buff=0.15)
            elements.extend([dot, lbl])

        return elements

    # ──────────────────────────────────────────
    #  PARABOLA FEATURES
    # ──────────────────────────────────────────

    def show_parabola_features(self, axes, a, b, c, show_vertex=True,
                                show_axis=True, show_roots=True,
                                show_y_intercept=True, color=None):
        """
        Plot y = ax² + bx + c with key features labeled.

        Useful for quadratic function exercises.

        Args:
            axes: Axes object.
            a, b, c: Coefficients of ax² + bx + c.
            show_vertex: Mark and label the vertex.
            show_axis: Show axis of symmetry (dashed vertical line).
            show_roots: Mark x-intercepts if they exist.
            show_y_intercept: Mark the y-intercept.
            color: Parabola color.

        Returns:
            VGroup of all created elements (curve + features).
        """
        clr = color or SHAPE_COLOR
        discriminant = b**2 - 4 * a * c
        vertex_x = -b / (2 * a)
        vertex_y = a * vertex_x**2 + b * vertex_x + c

        # Determine plot range to show the parabola nicely
        x_spread = max(3, abs(vertex_x) + 3)
        x_min = vertex_x - x_spread
        x_max = vertex_x + x_spread

        func = lambda x: a * x**2 + b * x + c
        curve = axes.plot(func, x_range=[x_min, x_max], color=clr, stroke_width=2.5)

        elements = [curve]

        # Vertex
        if show_vertex:
            dot_v = Dot(axes.c2p(vertex_x, vertex_y), color=ANSWER_COLOR, radius=0.1)
            vx_str = f"{vertex_x:.1f}" if vertex_x != int(vertex_x) else str(int(vertex_x))
            vy_str = f"{vertex_y:.1f}" if vertex_y != int(vertex_y) else str(int(vertex_y))
            lbl_v = MathTex(f"({vx_str},\\,{vy_str})", font_size=20, color=ANSWER_COLOR)
            direction = DOWN if a > 0 else UP
            lbl_v.next_to(dot_v, direction, buff=0.15)
            elements.extend([dot_v, lbl_v])

        # Axis of symmetry
        if show_axis:
            y_min = min(vertex_y, 0) - 1
            y_max = max(vertex_y, 0) + 1
            axis_line = DashedLine(
                axes.c2p(vertex_x, y_min), axes.c2p(vertex_x, y_max),
                color=DIVIDER_COLOR, dash_length=0.08, stroke_width=1.5,
            )
            axis_lbl = MathTex(
                f"x = {vx_str}", font_size=18, color=DIVIDER_COLOR,
            )
            axis_lbl.next_to(axis_line, UP, buff=0.1)
            elements.extend([axis_line, axis_lbl])

        # Roots
        if show_roots and discriminant >= 0:
            sqrt_d = np.sqrt(discriminant)
            x1 = (-b - sqrt_d) / (2 * a)
            x2 = (-b + sqrt_d) / (2 * a)
            for rx in sorted(set([x1, x2])):
                dot_r = Dot(axes.c2p(rx, 0), color=LABEL_COLOR, radius=0.08)
                rx_str = f"{rx:.2f}" if abs(rx - round(rx)) > 0.01 else str(int(round(rx)))
                lbl_r = MathTex(f"({rx_str},\\,0)", font_size=20, color=LABEL_COLOR)
                lbl_r.next_to(dot_r, DOWN, buff=0.15)
                elements.extend([dot_r, lbl_r])

        # Y-intercept
        if show_y_intercept:
            dot_y = Dot(axes.c2p(0, c), color=HIGHLIGHT_COLOR, radius=0.08)
            c_str = f"{c:.1f}" if c != int(c) else str(int(c))
            lbl_y = MathTex(f"(0,\\,{c_str})", font_size=20, color=HIGHLIGHT_COLOR)
            lbl_y.next_to(dot_y, RIGHT, buff=0.15)
            elements.extend([dot_y, lbl_y])

        return VGroup(*elements)

    # ──────────────────────────────────────────
    #  VALUE TABLE
    # ──────────────────────────────────────────

    def show_value_table(self, x_values, y_values, x_label="x", y_label="y",
                         position=None, font_size=24, highlight_indices=None):
        """
        Display a table of x/y values.

        Common in exercises that ask "fill in the table, then plot".

        Args:
            x_values: List of x values (strings or numbers).
            y_values: List of y values (strings or numbers).
            x_label: Header for x row.
            y_label: Header for y row.
            position: Where to place the table (default: ORIGIN).
            font_size: Font size for values.
            highlight_indices: Set of column indices to highlight.

        Returns:
            The table VGroup.
        """
        highlights = set(highlight_indices or [])

        # Build rows
        header_x = MathTex(x_label, font_size=font_size, color=STEP_TITLE_COLOR)
        header_y = MathTex(y_label, font_size=font_size, color=STEP_TITLE_COLOR)

        x_entries = []
        y_entries = []
        for i, (xv, yv) in enumerate(zip(x_values, y_values)):
            x_str = str(xv) if isinstance(xv, (int, float)) else xv
            y_str = str(yv) if isinstance(yv, (int, float)) else yv
            x_color = LABEL_COLOR if i in highlights else WHITE
            y_color = ANSWER_COLOR if i in highlights else WHITE
            x_entries.append(MathTex(x_str, font_size=font_size, color=x_color))
            y_entries.append(MathTex(y_str, font_size=font_size, color=y_color))

        # Arrange as grid
        col_buff = 0.6
        row_buff = 0.4

        x_row = VGroup(header_x, *x_entries).arrange(RIGHT, buff=col_buff)
        y_row = VGroup(header_y, *y_entries).arrange(RIGHT, buff=col_buff)

        # Align columns
        for xe, ye in zip(x_row, y_row):
            ye.align_to(xe, LEFT)

        table = VGroup(x_row, y_row).arrange(DOWN, buff=row_buff, aligned_edge=LEFT)

        # Add horizontal line between header row and values
        h_line = Line(
            x_row.get_left() + DOWN * row_buff / 2 + LEFT * 0.2,
            x_row.get_right() + DOWN * row_buff / 2 + RIGHT * 0.2,
            color=DIVIDER_COLOR, stroke_width=1.5,
        )
        # Add vertical line after headers
        v_line = Line(
            x_row[0].get_right() + RIGHT * col_buff / 2 + UP * 0.3,
            y_row[0].get_right() + RIGHT * col_buff / 2 + DOWN * 0.3,
            color=DIVIDER_COLOR, stroke_width=1.5,
        )

        full_table = VGroup(table, h_line, v_line)
        if position is not None:
            full_table.move_to(position)

        self.play(FadeIn(full_table), run_time=T_SHAPE_CREATE)
        self.wait(W_AFTER_ROUTINE)
        return full_table

    # ──────────────────────────────────────────
    #  NUMBER LINE WITH SOLUTION SETS
    # ──────────────────────────────────────────

    def show_number_line(self, x_range, tick_step=1, length=10,
                         marked_values=None, position=None):
        """
        Create a number line for inequality solutions.

        Args:
            x_range: [min, max] for the number line.
            tick_step: Spacing between ticks.
            length: Visual length.
            marked_values: List of values to specially label.
            position: Where to place (default: ORIGIN).

        Returns:
            The NumberLine mobject.
        """
        nl = NumberLine(
            x_range=[x_range[0], x_range[1], tick_step],
            length=length,
            include_numbers=True,
            font_size=20,
            color=DIVIDER_COLOR,
            include_tip=True,
        )
        if position is not None:
            nl.move_to(position)

        if marked_values:
            for val in marked_values:
                dot = Dot(nl.n2p(val), color=LABEL_COLOR, radius=0.1)
                nl.add(dot)

        return nl

    def show_interval_on_line(self, number_line, start, end,
                               start_open=False, end_open=False,
                               color=None):
        """
        Highlight an interval on a number line (for inequality solutions).

        Args:
            number_line: NumberLine mobject.
            start: Left endpoint (use None for -infinity).
            end: Right endpoint (use None for +infinity).
            start_open: Open circle at start? (strict inequality)
            end_open: Open circle at end?
            color: Interval color (defaults to ANSWER_COLOR).

        Returns:
            VGroup of (line_segment, start_marker, end_marker).
        """
        c = color or ANSWER_COLOR

        # Determine visual endpoints
        nl_min = number_line.x_range[0]
        nl_max = number_line.x_range[1]
        p_start = number_line.n2p(start if start is not None else nl_min)
        p_end = number_line.n2p(end if end is not None else nl_max)

        # Thick colored line for the interval
        interval_line = Line(p_start, p_end, color=c, stroke_width=6, stroke_opacity=0.7)

        elements = [interval_line]

        # Start marker
        if start is not None:
            if start_open:
                marker = Circle(radius=0.1, color=c, stroke_width=3).move_to(p_start)
            else:
                marker = Dot(p_start, color=c, radius=0.1)
            elements.append(marker)

        # End marker
        if end is not None:
            if end_open:
                marker = Circle(radius=0.1, color=c, stroke_width=3).move_to(p_end)
            else:
                marker = Dot(p_end, color=c, radius=0.1)
            elements.append(marker)

        # Arrows for infinity
        if start is None:
            arrow = Arrow(p_start + LEFT * 0.3, p_start, color=c, stroke_width=4,
                          max_tip_length_to_length_ratio=0.2)
            elements.append(arrow)
        if end is None:
            arrow = Arrow(p_end + RIGHT * 0.3, p_end, color=c, stroke_width=4,
                          max_tip_length_to_length_ratio=0.2)
            elements.append(arrow)

        group = VGroup(*elements)
        self.play(Create(interval_line), run_time=T_KEY_EQUATION)
        if len(elements) > 1:
            self.play(
                *[FadeIn(e) for e in elements[1:]],
                run_time=T_DOT_FADE,
            )
        self.wait(W_AFTER_ROUTINE)
        return group

    # ──────────────────────────────────────────
    #  TRIANGLE BUILDER
    # ──────────────────────────────────────────

    def build_triangle(self, vertices, labels, side_lengths=None,
                       angles=None, equal_sides=None, position=None):
        """
        Construct and animate a labeled triangle.

        Handles the boilerplate of creating, labeling, and marking triangles
        for geometry exercises (law of sines/cosines, Pythagorean, etc.)

        Args:
            vertices: Dict mapping label -> np.array position.
                      e.g. {"A": np.array([0, 2, 0]), "B": ..., "C": ...}
            labels: Dict mapping label -> direction for label placement.
                    e.g. {"A": UP, "B": DL, "C": DR}
            side_lengths: Dict mapping "AB" -> display string (optional).
                         e.g. {"AB": "25", "AC": "25"}
            angles: Dict mapping vertex label -> (degrees_str, color) (optional).
                    e.g. {"B": ("51°", GREEN)}
            equal_sides: List of side pairs to mark with tick marks (optional).
                         e.g. [("A", "B"), ("A", "C")]
            position: Shift the whole triangle (optional).

        Returns:
            Dict with keys: "triangle", "labels", "sides", "angles", "ticks", "group"
        """
        # Sort vertices to build polygon
        vertex_names = list(vertices.keys())
        pts = [vertices[n] for n in vertex_names]

        if position is not None:
            pts = [p + position for p in pts]
            vertices = {n: p + position for n, p in vertices.items()}

        tri = Polygon(*pts, color=SHAPE_COLOR, stroke_width=3)

        # Vertex labels
        vlabels = {}
        for name, direction in labels.items():
            lbl = MathTex(name, font_size=36, color=WHITE)
            lbl.next_to(vertices[name], direction, buff=0.15)
            vlabels[name] = lbl

        result = {
            "triangle": tri,
            "labels": vlabels,
            "sides": {},
            "angles": {},
            "ticks": [],
            "group": VGroup(tri, *vlabels.values()),
        }

        # Animate triangle creation
        self.play(Create(tri), run_time=T_SHAPE_CREATE)
        self.play(*[FadeIn(l) for l in vlabels.values()], run_time=0.6)
        self.wait(1)

        # Side lengths
        if side_lengths:
            for side_key, length_str in side_lengths.items():
                p1 = vertices[side_key[0]]
                p2 = vertices[side_key[1]]
                mid = self.midpoint(p1, p2)
                # Determine offset direction
                offset = self.perp_offset(p1, p2, 0.35)
                s_lbl = MathTex(length_str, font_size=28, color=LABEL_COLOR)
                s_lbl.move_to(mid + offset)
                result["sides"][side_key] = s_lbl
                result["group"].add(s_lbl)

        # Equal side tick marks
        if equal_sides:
            for p1_name, p2_name in equal_sides:
                tick = self.tick_mark(vertices[p1_name], vertices[p2_name], size=0.12)
                result["ticks"].append(tick)
                result["group"].add(tick)

        # Animate sides and ticks
        side_anims = [FadeIn(s) for s in result["sides"].values()]
        tick_anims = [Create(t) for t in result["ticks"]]
        if side_anims or tick_anims:
            self.play(*side_anims, *tick_anims, run_time=0.8)

        # Angles
        if angles:
            for vertex_name, (angle_str, angle_color) in angles.items():
                v = vertices[vertex_name]
                # Find the two other vertices
                others = [n for n in vertex_names if n != vertex_name]
                p1 = vertices[others[0]]
                p2 = vertices[others[1]]
                arc = self.angle_arc(v, p1, p2, radius=0.45, color=angle_color)
                lbl = MathTex(angle_str, font_size=24, color=angle_color)
                lbl.move_to(self.angle_label_pos(v, p1, p2, 0.75))
                result["angles"][vertex_name] = (arc, lbl)
                result["group"].add(arc, lbl)
                self.play(Create(arc), FadeIn(lbl), run_time=0.8)

        return result

    # ──────────────────────────────────────────
    #  CALCULUS HELPERS
    # ──────────────────────────────────────────

    def show_tangent_to_curve(self, axes, func, x0, dx=0.5, tangent_length=3,
                               func_color=None, tangent_color=None,
                               label_point=True):
        """
        Draw a tangent line to a curve at x = x0.

        For derivative visualization exercises.

        Args:
            axes: Axes object.
            func: Callable f(x) -> y.
            x0: x-coordinate of the tangent point.
            dx: Step for numerical derivative.
            tangent_length: How far the tangent line extends each side.
            func_color: Curve color.
            tangent_color: Tangent line color.
            label_point: Whether to label the tangent point.

        Returns:
            VGroup of (tangent_line, tangent_point_dot, slope_label).
        """
        fc = func_color or SHAPE_COLOR
        tc = tangent_color or AUX_COLOR

        y0 = func(x0)
        # Numerical derivative
        slope = (func(x0 + dx) - func(x0 - dx)) / (2 * dx)

        # Tangent line: y - y0 = slope * (x - x0)
        tangent_func = lambda x: slope * (x - x0) + y0
        x_left = x0 - tangent_length
        x_right = x0 + tangent_length

        tangent_line = axes.plot(
            tangent_func, x_range=[x_left, x_right],
            color=tc, stroke_width=2.5,
        )

        dot = Dot(axes.c2p(x0, y0), color=tc, radius=0.1)

        elements = [tangent_line, dot]

        if label_point:
            x_str = f"{x0:.1f}" if x0 != int(x0) else str(int(x0))
            y_str = f"{y0:.1f}" if abs(y0 - round(y0)) > 0.01 else str(int(round(y0)))
            pt_lbl = MathTex(f"({x_str},\\,{y_str})", font_size=20, color=tc)
            pt_lbl.next_to(dot, UR, buff=0.15)
            elements.append(pt_lbl)

        # Slope label
        slope_str = f"{slope:.2f}" if abs(slope - round(slope)) > 0.01 else str(int(round(slope)))
        slope_lbl = MathTex(f"m = {slope_str}", font_size=20, color=tc)
        slope_lbl.next_to(tangent_line.point_from_proportion(0.9), UR, buff=0.1)
        elements.append(slope_lbl)

        group = VGroup(*elements)

        self.play(FadeIn(dot, scale=1.5), run_time=T_DOT_FADE)
        self.play(Create(tangent_line), run_time=T_KEY_EQUATION)
        if label_point:
            self.play(FadeIn(elements[2]), FadeIn(slope_lbl), run_time=T_BODY_FADE)
        else:
            self.play(FadeIn(slope_lbl), run_time=T_BODY_FADE)
        self.wait(W_AFTER_ROUTINE)

        return group

    def show_area_under_curve(self, axes, func, x_start, x_end,
                               color=None, opacity=0.3, n_rects=0):
        """
        Shade the area under a curve between x_start and x_end.

        For integral visualization exercises.

        Args:
            axes: Axes object.
            func: Callable f(x) -> y.
            x_start: Left bound.
            x_end: Right bound.
            color: Fill color (defaults to SHAPE_COLOR).
            opacity: Fill opacity.
            n_rects: If > 0, show Riemann rectangles instead of smooth fill.

        Returns:
            The shaded area mobject.
        """
        c = color or SHAPE_COLOR

        if n_rects > 0:
            # Riemann sum rectangles
            area = axes.get_riemann_rectangles(
                axes.plot(func, x_range=[x_start, x_end]),
                x_range=[x_start, x_end],
                dx=(x_end - x_start) / n_rects,
                color=[c, HIGHLIGHT_COLOR],
                fill_opacity=opacity,
                stroke_width=1,
            )
        else:
            area = axes.get_area(
                axes.plot(func, x_range=[x_start, x_end]),
                x_range=[x_start, x_end],
                color=c,
                opacity=opacity,
            )

        self.play(FadeIn(area), run_time=T_SHAPE_CREATE)
        self.wait(W_AFTER_ROUTINE)
        return area

    # ──────────────────────────────────────────
    #  CONIC SECTION HELPERS
    # ──────────────────────────────────────────

    def plot_ellipse(self, axes, a, b, center=(0, 0), color=None, stroke_width=3):
        """
        Plot an ellipse on axes.

        Equation: (x-h)²/a² + (y-k)²/b² = 1

        Args:
            axes: Axes object.
            a: Semi-major axis (horizontal).
            b: Semi-minor axis (vertical).
            center: (h, k) center point.
            color: Ellipse color.
            stroke_width: Line width.

        Returns:
            The parametric curve mobject.
        """
        c = color or SHAPE_COLOR
        h, k = center
        return axes.plot_parametric_curve(
            lambda t: np.array([h + a * np.cos(t), k + b * np.sin(t), 0]),
            t_range=[0, 2 * PI],
            color=c,
            stroke_width=stroke_width,
        )

    def plot_hyperbola(self, axes, a, b, center=(0, 0), color=None,
                        stroke_width=3, t_range=None):
        """
        Plot a hyperbola on axes.

        Equation: (x-h)²/a² - (y-k)²/b² = 1

        Args:
            axes: Axes object.
            a, b: Semi-axes.
            center: (h, k) center point.
            color: Curve color.
            stroke_width: Line width.
            t_range: Parameter range (default [-2, 2]).

        Returns:
            VGroup of left and right branches.
        """
        c = color or SHAPE_COLOR
        h, k = center
        t_r = t_range or [-2, 2]

        # Right branch: x = h + a*cosh(t), y = k + b*sinh(t)
        right = axes.plot_parametric_curve(
            lambda t: np.array([h + a * np.cosh(t), k + b * np.sinh(t), 0]),
            t_range=t_r, color=c, stroke_width=stroke_width,
        )
        # Left branch: x = h - a*cosh(t), y = k + b*sinh(t)
        left = axes.plot_parametric_curve(
            lambda t: np.array([h - a * np.cosh(t), k + b * np.sinh(t), 0]),
            t_range=t_r, color=c, stroke_width=stroke_width,
        )
        return VGroup(left, right)

    # ──────────────────────────────────────────
    #  GEOMETRY HELPERS
    # ──────────────────────────────────────────

    @staticmethod
    def midpoint(p1, p2):
        """Calculate the midpoint of two points."""
        return (np.array(p1) + np.array(p2)) / 2

    @staticmethod
    def perp_offset(p1, p2, dist):
        """Get a perpendicular offset vector from the line p1->p2."""
        d = np.array(p2) - np.array(p1)
        d = d / np.linalg.norm(d)
        perp = np.array([-d[1], d[0], 0])
        return perp * dist

    @staticmethod
    def tick_mark(p1, p2, size=0.1, color=None):
        """Draw an equal-length tick mark at the midpoint of a segment."""
        c = color or LABEL_COLOR
        mid = (np.array(p1) + np.array(p2)) / 2
        d = np.array(p2) - np.array(p1)
        d = d / np.linalg.norm(d)
        perp = np.array([-d[1], d[0], 0])
        return Line(
            mid - perp * size,
            mid + perp * size,
            color=c,
            stroke_width=2.5,
        )

    @staticmethod
    def angle_arc(vertex, p1, p2, radius=0.4, color=None):
        """Draw an arc indicating an angle at vertex between rays to p1 and p2."""
        c = color or LABEL_COLOR
        v = np.array(vertex)
        d1 = np.array(p1) - v
        d2 = np.array(p2) - v
        a1 = np.arctan2(d1[1], d1[0])
        a2 = np.arctan2(d2[1], d2[0])
        diff = (a2 - a1) % (2 * np.pi)
        if diff > np.pi:
            start = a2
            angle = 2 * np.pi - diff
        else:
            start = a1
            angle = diff
        return Arc(
            radius=radius,
            start_angle=start,
            angle=angle,
            arc_center=v,
            color=c,
            stroke_width=2.5,
        )

    @staticmethod
    def angle_label_pos(vertex, p1, p2, distance=0.55):
        """Calculate position for an angle label along the bisector."""
        v = np.array(vertex)
        d1 = (np.array(p1) - v)
        d1 = d1 / np.linalg.norm(d1)
        d2 = (np.array(p2) - v)
        d2 = d2 / np.linalg.norm(d2)
        bisector = d1 + d2
        norm = np.linalg.norm(bisector)
        if norm < 1e-6:
            bisector = np.array([-d1[1], d1[0], 0])
        else:
            bisector = bisector / norm
        return v + bisector * distance

    @staticmethod
    def right_angle_mark(vertex, p_horiz, p_vert, size=0.2, color=None):
        """Draw a right angle indicator at vertex."""
        c = color or AUX_COLOR
        v = np.array(vertex)
        dh = np.array(p_horiz) - v
        dh = dh / np.linalg.norm(dh) * size
        dv = np.array(p_vert) - v
        dv = dv / np.linalg.norm(dv) * size
        return VGroup(
            Line(v + dh, v + dh + dv, color=c, stroke_width=2.5),
            Line(v + dv, v + dh + dv, color=c, stroke_width=2.5),
        )

    # ══════════════════════════════════════════
    #  CROSS-SUBJECT COMPONENTS
    #  (Physics, Chemistry, Math)
    # ══════════════════════════════════════════

    # ──────────────────────────────────────────
    #  VECTOR ARROWS
    # ──────────────────────────────────────────

    def draw_vector(self, start, end, color=None, label_tex=None,
                    label_direction=None, stroke_width=4,
                    max_tip_length=0.25):
        """
        Draw a vector arrow with an optional label.

        Useful for: forces, velocities, displacements, electric fields.

        Args:
            start: Start point (np.array or list).
            end: End point.
            color: Arrow color (defaults to SHAPE_COLOR).
            label_tex: LaTeX label (e.g. r"\\vec{F}"). None to skip.
            label_direction: Where to place label (auto if None).
            stroke_width: Arrow thickness.
            max_tip_length: Arrow head size.

        Returns:
            (arrow, label) tuple. label is None if label_tex is None.
        """
        c = color or SHAPE_COLOR
        arrow = Arrow(
            start=np.array(start), end=np.array(end),
            color=c, stroke_width=stroke_width,
            max_tip_length_to_length_ratio=max_tip_length,
            buff=0,
        )
        lbl = None
        if label_tex:
            mid = (np.array(start) + np.array(end)) / 2
            if label_direction is None:
                # Auto: perpendicular to arrow direction
                d = np.array(end) - np.array(start)
                perp = np.array([-d[1], d[0], 0])
                norm = np.linalg.norm(perp)
                label_direction = perp / norm * 0.4 if norm > 1e-6 else UP * 0.4
            lbl = MathTex(label_tex, font_size=24, color=c)
            lbl.next_to(mid, label_direction, buff=0.1)
        return arrow, lbl

    def show_vector(self, start, end, color=None, label_tex=None,
                    label_direction=None):
        """Draw and animate a vector arrow with label."""
        arrow, lbl = self.draw_vector(start, end, color=color,
                                       label_tex=label_tex,
                                       label_direction=label_direction)
        anims = [GrowArrow(arrow)]
        if lbl:
            anims.append(FadeIn(lbl))
        self.play(*anims, run_time=T_KEY_EQUATION)
        self.wait(0.5)
        return arrow, lbl

    # ──────────────────────────────────────────
    #  FREE BODY DIAGRAM
    # ──────────────────────────────────────────

    def show_free_body_diagram(self, forces, body_position=ORIGIN,
                                body_radius=0.3, body_label=None):
        """
        Draw a free body diagram: a body with force vectors.

        Args:
            forces: List of dicts, each with:
                - "direction": np.array unit direction (e.g. UP, DOWN, RIGHT)
                - "magnitude": visual length of arrow
                - "label": LaTeX label (e.g. r"\\vec{F}_g")
                - "color": arrow color (optional)
            body_position: Center of the body dot.
            body_radius: Size of the body circle.
            body_label: Label for the body (e.g. "m").

        Returns:
            VGroup of all elements.
        """
        bp = np.array(body_position)

        # Body
        body = Circle(radius=body_radius, color=WHITE, fill_color=DIVIDER_COLOR,
                       fill_opacity=0.3, stroke_width=2)
        body.move_to(bp)

        elements = [body]

        if body_label:
            b_lbl = MathTex(body_label, font_size=24, color=WHITE)
            b_lbl.move_to(bp)
            elements.append(b_lbl)

        self.play(Create(body), run_time=0.6)
        if body_label:
            self.play(FadeIn(b_lbl), run_time=0.3)

        # Force arrows
        default_colors = [AUX_COLOR, SHAPE_COLOR, ANSWER_COLOR, HIGHLIGHT_COLOR, LABEL_COLOR]
        for i, f in enumerate(forces):
            direction = np.array(f["direction"])
            direction = direction / np.linalg.norm(direction)
            mag = f.get("magnitude", 1.5)
            c = f.get("color", default_colors[i % len(default_colors)])

            start = bp + direction * body_radius
            end = start + direction * mag

            arrow, lbl = self.draw_vector(start, end, color=c,
                                           label_tex=f.get("label"))
            elements.append(arrow)
            if lbl:
                elements.append(lbl)

            anims = [GrowArrow(arrow)]
            if lbl:
                anims.append(FadeIn(lbl))
            self.play(*anims, run_time=0.6)

        self.wait(W_AFTER_ROUTINE)
        return VGroup(*elements)

    # ──────────────────────────────────────────
    #  BAR CHART
    # ──────────────────────────────────────────

    def show_bar_chart(self, values, labels, title_text=None,
                       colors=None, position=None, bar_width=0.6,
                       max_height=3.5, show_values=True, value_format=None):
        """
        Display a labeled bar chart.

        Useful for: energy comparisons (KE/PE), stoichiometry (moles/mass),
        statistics, any quantity comparison.

        Args:
            values: List of numeric values.
            labels: List of LaTeX strings for each bar.
            title_text: Chart title (optional).
            colors: List of bar colors (cycles defaults if None).
            position: Where to place the chart.
            bar_width: Width of each bar.
            max_height: Maximum bar height in scene units.
            show_values: Display numeric value on top of each bar.
            value_format: Format string for values (e.g. "{:.1f}").

        Returns:
            VGroup of all chart elements.
        """
        default_colors = [SHAPE_COLOR, AUX_COLOR, ANSWER_COLOR,
                          HIGHLIGHT_COLOR, LABEL_COLOR]

        max_val = max(abs(v) for v in values) if values else 1
        scale = max_height / max_val if max_val > 0 else 1

        bars = VGroup()
        bar_labels = VGroup()
        val_labels = VGroup()

        for i, (val, label_tex) in enumerate(zip(values, labels)):
            c = (colors[i] if colors else
                 default_colors[i % len(default_colors)])

            height = abs(val) * scale
            bar = Rectangle(
                width=bar_width, height=max(height, 0.05),
                fill_color=c, fill_opacity=0.7,
                stroke_color=c, stroke_width=2,
            )

            bars.add(bar)

            lbl = MathTex(label_tex, font_size=22, color=c)
            bar_labels.add(lbl)

            if show_values:
                fmt = value_format or "{}"
                v_lbl = MathTex(fmt.format(val), font_size=20, color=c)
                val_labels.add(v_lbl)

        # Arrange bars side by side
        bars.arrange(RIGHT, buff=0.4, aligned_edge=DOWN)

        # Position labels below bars
        for bar, lbl in zip(bars, bar_labels):
            lbl.next_to(bar, DOWN, buff=0.2)

        # Position values above bars
        if show_values:
            for bar, v_lbl in zip(bars, val_labels):
                v_lbl.next_to(bar, UP, buff=0.1)

        # Baseline
        baseline = Line(
            bars.get_left() + LEFT * 0.3 + DOWN * 0.01,
            bars.get_right() + RIGHT * 0.3 + DOWN * 0.01,
            color=DIVIDER_COLOR, stroke_width=2,
        )

        all_elements = VGroup(bars, bar_labels, baseline)
        if show_values:
            all_elements.add(val_labels)

        if position is not None:
            all_elements.move_to(position)

        # Title
        if title_text:
            title = MathTex(r"\text{" + title_text + r"}",
                           font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR)
            title.next_to(all_elements, UP, buff=0.4)
            all_elements.add(title)

        # Animate
        self.play(FadeIn(baseline), run_time=0.3)
        self.play(
            LaggedStart(
                *[GrowFromEdge(bar, DOWN) for bar in bars],
                lag_ratio=0.15,
            ),
            run_time=1.2,
        )
        self.play(
            *[FadeIn(l) for l in bar_labels],
            run_time=0.5,
        )
        if show_values:
            self.play(*[FadeIn(v) for v in val_labels], run_time=0.5)
        if title_text:
            self.play(Write(title), run_time=0.6)

        self.wait(W_AFTER_ROUTINE)
        return all_elements

    # ──────────────────────────────────────────
    #  LABELED DIAGRAM
    # ──────────────────────────────────────────

    def add_label(self, target, label_tex, direction=RIGHT, color=None,
                  font_size=22, line=False):
        """
        Add a label to any mobject, optionally with a connecting line.

        Useful for labeling parts of any diagram (physics, chemistry, biology).

        Args:
            target: The mobject to label.
            label_tex: LaTeX string for the label.
            direction: Where to place (UP, DOWN, LEFT, RIGHT, etc.)
            color: Label color.
            font_size: Label font size.
            line: If True, draw a thin line from label to target.

        Returns:
            (label, line_or_None) tuple.
        """
        c = color or BODY_TEXT_COLOR
        lbl = MathTex(label_tex, font_size=font_size, color=c)
        lbl.next_to(target, direction, buff=0.3)

        connector = None
        if line:
            connector = Line(
                target.get_center(), lbl.get_center(),
                color=DIVIDER_COLOR, stroke_width=1, stroke_opacity=0.5,
            )
            self.play(Create(connector), FadeIn(lbl), run_time=T_BODY_FADE)
        else:
            self.play(FadeIn(lbl), run_time=T_BODY_FADE)

        return lbl, connector

    def add_brace_label(self, mobject, label_tex, direction=DOWN, color=None,
                        font_size=22):
        """
        Add a brace with label to a mobject (for showing lengths, ranges, etc.).

        Args:
            mobject: Mobject to brace.
            label_tex: LaTeX label.
            direction: Brace direction.
            color: Brace and label color.
            font_size: Label font size.

        Returns:
            (brace, label) tuple.
        """
        c = color or BODY_TEXT_COLOR
        brace = Brace(mobject, direction, color=c)
        lbl = MathTex(label_tex, font_size=font_size, color=c)
        brace.put_at_tip(lbl)

        self.play(GrowFromCenter(brace), FadeIn(lbl), run_time=T_BODY_FADE)
        return brace, lbl

    # ──────────────────────────────────────────
    #  BEFORE / AFTER LAYOUT
    # ──────────────────────────────────────────

    def show_before_after(self, before_group, after_group,
                          before_title="Para", after_title="Pas",
                          arrow_label=None):
        """
        Show a before/after comparison with an arrow between them.

        Useful for: collisions, reactions, transformations, state changes.

        Args:
            before_group: VGroup for the "before" state.
            after_group: VGroup for the "after" state.
            before_title: Title above left side.
            after_title: Title above right side.
            arrow_label: Label on the arrow (e.g. "react", "collision").

        Returns:
            VGroup of entire layout.
        """
        # Position
        before_group.move_to(LEFT * 3.5)
        after_group.move_to(RIGHT * 3.5)

        # Titles
        b_title = MathTex(r"\text{" + before_title + r"}",
                          font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR)
        b_title.next_to(before_group, UP, buff=0.4)

        a_title = MathTex(r"\text{" + after_title + r"}",
                          font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR)
        a_title.next_to(after_group, UP, buff=0.4)

        # Arrow
        arrow = Arrow(LEFT * 1.2, RIGHT * 1.2, color=DIVIDER_COLOR,
                       stroke_width=3)
        arrow.move_to(ORIGIN)

        elements = [before_group, after_group, b_title, a_title, arrow]

        if arrow_label:
            a_lbl = MathTex(arrow_label, font_size=20, color=BODY_TEXT_COLOR)
            a_lbl.next_to(arrow, UP, buff=0.1)
            elements.append(a_lbl)

        # Animate
        self.play(Write(b_title), FadeIn(before_group), run_time=T_SHAPE_CREATE)
        self.wait(W_AFTER_ROUTINE)
        self.play(GrowArrow(arrow), run_time=0.6)
        if arrow_label:
            self.play(FadeIn(a_lbl), run_time=0.3)
        self.play(Write(a_title), FadeIn(after_group), run_time=T_SHAPE_CREATE)
        self.wait(W_AFTER_KEY)

        return VGroup(*elements)

    # ──────────────────────────────────────────
    #  UNIT CONVERSION CHAIN
    # ──────────────────────────────────────────

    def show_conversion_chain(self, steps, position=None):
        """
        Show a step-by-step unit conversion.

        Useful for: physics (m/s to km/h), chemistry (moles to grams), etc.

        Args:
            steps: List of LaTeX strings for each step.
                   e.g. [r"72\\,\\text{km/h}", r"\\times \\frac{1000}{3600}",
                         r"= 20\\,\\text{m/s}"]
            position: Where to place (default: ORIGIN).

        Returns:
            VGroup of all step elements.
        """
        elements = []
        for i, step_tex in enumerate(steps):
            eq = MathTex(step_tex, font_size=CALC_SIZE)
            if i == 0:
                if position is not None:
                    eq.move_to(position)
            else:
                eq.next_to(elements[-1], RIGHT, buff=0.15)
            elements.append(eq)

        # Check if it fits, if not stack vertically
        group = VGroup(*elements)
        if group.get_width() > 12:
            # Re-arrange vertically
            group.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
            if position is not None:
                group.move_to(position)

        # Color the last step as the answer
        if len(elements) > 1:
            elements[-1].set_color(ANSWER_COLOR)

        self.play(
            LaggedStart(*[Write(e) for e in elements], lag_ratio=0.3),
            run_time=T_KEY_EQUATION * len(elements) * 0.5,
        )
        self.wait(W_AFTER_KEY)
        return group

    # ══════════════════════════════════════════
    #  PHYSICS COMPONENTS
    # ══════════════════════════════════════════

    # ──────────────────────────────────────────
    #  KINEMATICS GRAPHS
    # ──────────────────────────────────────────

    def show_kinematics_graph(self, graph_type, segments, t_max,
                               y_label=None, y_max=None,
                               show_area=False, show_slope=False):
        """
        Display a piecewise-linear kinematics graph (x-t, v-t, or a-t).

        Args:
            graph_type: "position", "velocity", or "acceleration".
            segments: List of (t_end, value) tuples defining
                      piecewise-constant or linear segments.
                      For "velocity": [(2, 10), (5, 10), (7, 0)] means
                      v=10 from t=0..2, v=10 from t=2..5, v=0 from t=5..7.
            t_max: Maximum time.
            y_label: Custom y-axis label (auto if None).
            y_max: Custom y-axis max (auto if None).
            show_area: Shade area under curve (useful for v-t → displacement).
            show_slope: Draw slope annotation (useful for x-t → velocity).

        Returns:
            (axes, graph_group) tuple.
        """
        type_labels = {
            "position": "x\\,(\\text{m})",
            "velocity": "v\\,(\\text{m/s})",
            "acceleration": "a\\,(\\text{m/s}^2)",
        }
        y_lbl = y_label or type_labels.get(graph_type, "y")

        # Determine y range
        all_vals = [v for _, v in segments]
        y_min_val = min(0, min(all_vals)) - 1
        y_max_val = y_max or (max(all_vals) + 2)
        y_step = max(1, int((y_max_val - y_min_val) / 5))

        axes = self.create_axes_custom(
            [0, t_max, max(1, t_max // 6)],
            [y_min_val, y_max_val, y_step],
            x_length=7, y_length=4.5,
        )
        axes_labels = VGroup(
            MathTex("t\\,(\\text{s})", font_size=20).next_to(axes.x_axis, RIGHT, buff=0.1),
            MathTex(y_lbl, font_size=20).next_to(axes.y_axis, UP, buff=0.1),
        )

        # Build piecewise line
        points = [axes.c2p(0, segments[0][1] if segments else 0)]
        t_prev = 0
        for t_end, val in segments:
            points.append(axes.c2p(t_end, val))
            t_prev = t_end

        graph_line = VMobject(color=SHAPE_COLOR, stroke_width=3)
        graph_line.set_points_as_corners(points)

        elements = [axes, axes_labels, graph_line]

        self.play(Create(axes), FadeIn(axes_labels), run_time=T_SHAPE_CREATE)
        self.play(Create(graph_line), run_time=T_SHAPE_CREATE)

        # Key value dots
        t_prev = 0
        for t_end, val in segments:
            dot = Dot(axes.c2p(t_end, val), color=LABEL_COLOR, radius=0.06)
            elements.append(dot)
            t_prev = t_end
        self.play(*[FadeIn(e) for e in elements[3:]], run_time=0.5)

        # Shade area
        if show_area:
            # Build polygon for area under curve
            area_points = [axes.c2p(0, 0)]
            area_points.extend(points)
            area_points.append(axes.c2p(t_prev, 0))

            area = Polygon(*area_points, fill_color=SHAPE_COLOR,
                           fill_opacity=0.2, stroke_width=0)
            elements.append(area)
            self.play(FadeIn(area), run_time=T_BODY_FADE)

        self.wait(W_AFTER_KEY)
        return axes, VGroup(*elements)

    # ──────────────────────────────────────────
    #  PROJECTILE MOTION
    # ──────────────────────────────────────────

    def show_projectile_path(self, v0, angle_deg, g=9.81,
                              show_components=False, show_max_height=True,
                              show_range=True):
        """
        Animate a projectile motion parabola.

        Args:
            v0: Initial speed (m/s).
            angle_deg: Launch angle in degrees.
            g: Gravitational acceleration.
            show_components: Show v_x and v_y components at start.
            show_max_height: Mark maximum height.
            show_range: Mark horizontal range.

        Returns:
            (axes, graph_group) tuple.
        """
        angle_rad = angle_deg * DEGREES
        v0x = v0 * np.cos(angle_rad)
        v0y = v0 * np.sin(angle_rad)

        t_flight = 2 * v0y / g
        x_range_val = v0x * t_flight
        y_max_val = v0y**2 / (2 * g)

        # Scale for visualization
        x_bound = x_range_val * 1.2
        y_bound = y_max_val * 1.4

        axes = self.create_axes_custom(
            [0, x_bound, x_bound / 5],
            [0, y_bound, y_bound / 4],
            x_length=8, y_length=4.5,
        )
        x_lbl = MathTex("x\\,(\\text{m})", font_size=20).next_to(axes.x_axis, RIGHT, buff=0.1)
        y_lbl = MathTex("y\\,(\\text{m})", font_size=20).next_to(axes.y_axis, UP, buff=0.1)

        # Parametric path
        path = axes.plot_parametric_curve(
            lambda t: np.array([v0x * t, v0y * t - 0.5 * g * t**2, 0]),
            t_range=[0, t_flight],
            color=SHAPE_COLOR, stroke_width=3,
        )

        elements = [axes, x_lbl, y_lbl, path]

        self.play(Create(axes), FadeIn(x_lbl), FadeIn(y_lbl), run_time=T_SHAPE_CREATE)
        self.play(Create(path), run_time=T_SHAPE_CREATE * 1.5)

        # Velocity components at launch
        if show_components:
            origin = axes.c2p(0, 0)
            vx_end = axes.c2p(v0x * 0.15, 0)
            vy_end = axes.c2p(0, v0y * 0.15)
            v_end = axes.c2p(v0x * 0.15, v0y * 0.15)

            vx_arr, vx_lbl = self.draw_vector(origin, vx_end, color=AUX_COLOR,
                                               label_tex=r"v_x")
            vy_arr, vy_lbl = self.draw_vector(origin, vy_end, color=HIGHLIGHT_COLOR,
                                               label_tex=r"v_y")
            v_arr, v_lbl = self.draw_vector(origin, v_end, color=ANSWER_COLOR,
                                             label_tex=r"v_0")
            for arr, lbl in [(vx_arr, vx_lbl), (vy_arr, vy_lbl), (v_arr, v_lbl)]:
                self.play(GrowArrow(arr), FadeIn(lbl), run_time=0.5)
                elements.extend([arr, lbl])

        # Max height
        if show_max_height:
            t_apex = v0y / g
            h_max = v0y * t_apex - 0.5 * g * t_apex**2
            x_apex = v0x * t_apex
            dot_h = Dot(axes.c2p(x_apex, h_max), color=ANSWER_COLOR, radius=0.08)
            lbl_h = MathTex(f"h_{{max}} = {h_max:.1f}", font_size=20, color=ANSWER_COLOR)
            lbl_h.next_to(dot_h, UR, buff=0.1)
            # Dashed line down
            dash_h = DashedLine(axes.c2p(x_apex, 0), axes.c2p(x_apex, h_max),
                                color=DIVIDER_COLOR, dash_length=0.08, stroke_width=1.5)
            elements.extend([dot_h, lbl_h, dash_h])
            self.play(FadeIn(dot_h), FadeIn(lbl_h), Create(dash_h), run_time=0.6)

        # Range
        if show_range:
            dot_r = Dot(axes.c2p(x_range_val, 0), color=LABEL_COLOR, radius=0.08)
            lbl_r = MathTex(f"R = {x_range_val:.1f}", font_size=20, color=LABEL_COLOR)
            lbl_r.next_to(dot_r, DOWN, buff=0.15)
            elements.extend([dot_r, lbl_r])
            self.play(FadeIn(dot_r), FadeIn(lbl_r), run_time=0.5)

        self.wait(W_AFTER_KEY)
        return axes, VGroup(*elements)

    # ──────────────────────────────────────────
    #  ENERGY BAR CHART
    # ──────────────────────────────────────────

    def show_energy_bars(self, states, position=None):
        """
        Show energy bar charts for multiple states (before/after).

        Common in conservation of energy problems.

        Args:
            states: List of dicts, each with:
                - "title": State label (e.g. "Fillimi", "Fundi")
                - "KE": kinetic energy value
                - "PE": potential energy value
                - "TE": total energy (optional, auto-calculated)
            position: Where to place.

        Returns:
            VGroup of all charts.
        """
        charts = VGroup()
        n = len(states)
        spacing = 10.0 / n

        for i, state in enumerate(states):
            ke = state.get("KE", 0)
            pe = state.get("PE", 0)
            te = state.get("TE", ke + pe)

            chart = self.show_bar_chart(
                values=[ke, pe, te],
                labels=[r"E_k", r"E_p", r"E_{tot}"],
                title_text=state.get("title"),
                colors=[AUX_COLOR, SHAPE_COLOR, ANSWER_COLOR],
                position=LEFT * (spacing * (n - 1) / 2) + RIGHT * (spacing * i),
                bar_width=0.45,
                max_height=2.5,
                value_format="{:.0f}",
            )
            charts.add(chart)

        return charts

    # ══════════════════════════════════════════
    #  CHEMISTRY COMPONENTS
    # ══════════════════════════════════════════

    # ──────────────────────────────────────────
    #  CHEMICAL EQUATION
    # ──────────────────────────────────────────

    def show_chemical_equation(self, reactants, products, coefficients=None,
                                position=None, balanced=True):
        """
        Display a chemical equation with optional coefficient highlighting.

        Args:
            reactants: List of formula strings (e.g. ["H_2", "O_2"]).
            products: List of formula strings (e.g. ["H_2O"]).
            coefficients: Dict mapping formula -> coefficient string.
                          e.g. {"H_2": "2", "H_2O": "2"}
            position: Where to place.
            balanced: If True, show checkmark; if False, show X.

        Returns:
            The equation VGroup.
        """
        parts = []
        coeffs = coefficients or {}

        # Build reactant side
        for i, r in enumerate(reactants):
            coeff = coeffs.get(r, "")
            if coeff:
                c_tex = MathTex(coeff, font_size=CALC_SIZE, color=ANSWER_COLOR)
                parts.append(c_tex)
            parts.append(MathTex(r"\\text{" + r + "}", font_size=CALC_SIZE))
            if i < len(reactants) - 1:
                parts.append(MathTex("+", font_size=CALC_SIZE, color=DIVIDER_COLOR))

        # Arrow
        parts.append(MathTex(r"\\rightarrow", font_size=CALC_SIZE, color=BODY_TEXT_COLOR))

        # Build product side
        for i, p in enumerate(products):
            coeff = coeffs.get(p, "")
            if coeff:
                c_tex = MathTex(coeff, font_size=CALC_SIZE, color=ANSWER_COLOR)
                parts.append(c_tex)
            parts.append(MathTex(r"\\text{" + p + "}", font_size=CALC_SIZE))
            if i < len(products) - 1:
                parts.append(MathTex("+", font_size=CALC_SIZE, color=DIVIDER_COLOR))

        group = VGroup(*parts).arrange(RIGHT, buff=0.15)
        if position is not None:
            group.move_to(position)

        self.play(
            LaggedStart(*[FadeIn(p) for p in parts], lag_ratio=0.1),
            run_time=T_SHAPE_CREATE,
        )
        self.wait(W_AFTER_ROUTINE)

        return group

    # ──────────────────────────────────────────
    #  REACTION ENERGY DIAGRAM
    # ──────────────────────────────────────────

    def show_reaction_energy_diagram(self, e_reactants, e_products, e_activation,
                                      labels=None, position=None):
        """
        Show a reaction energy (enthalpy) diagram.

        Displays: reactant energy level → activation energy peak → product level.

        Args:
            e_reactants: Energy level of reactants.
            e_products: Energy level of products.
            e_activation: Activation energy (height above reactants).
            labels: Dict with optional keys:
                    "reactants", "products", "activation", "delta_h"
            position: Where to place.

        Returns:
            VGroup of all elements.
        """
        lbls = labels or {}

        # Scale
        e_max = max(e_reactants + e_activation, e_products) * 1.3
        e_min = min(e_reactants, e_products) * 0.8 if min(e_reactants, e_products) > 0 else -1

        axes = self.create_axes_custom(
            [0, 10, 2], [e_min, e_max, (e_max - e_min) / 5],
            x_length=8, y_length=5, include_numbers=False,
        )

        # Axis labels
        x_lbl = Text("Rruga e reaksionit", font_size=18, color=BODY_TEXT_COLOR)
        x_lbl.next_to(axes.x_axis, DOWN, buff=0.3)
        y_lbl = Text("Energjia", font_size=18, color=BODY_TEXT_COLOR)
        y_lbl.next_to(axes.y_axis, UP, buff=0.2)

        # Reactant level (flat line)
        r_line = Line(axes.c2p(0.5, e_reactants), axes.c2p(3, e_reactants),
                       color=SHAPE_COLOR, stroke_width=3)
        r_lbl = MathTex(
            lbls.get("reactants", r"\text{Reaktantët}"),
            font_size=20, color=SHAPE_COLOR,
        )
        r_lbl.next_to(r_line, LEFT, buff=0.15)

        # Product level
        p_line = Line(axes.c2p(7, e_products), axes.c2p(9.5, e_products),
                       color=ANSWER_COLOR, stroke_width=3)
        p_lbl = MathTex(
            lbls.get("products", r"\text{Produktet}"),
            font_size=20, color=ANSWER_COLOR,
        )
        p_lbl.next_to(p_line, RIGHT, buff=0.15)

        # Activation energy curve (smooth bump)
        peak_e = e_reactants + e_activation
        curve_points = []
        for t in np.linspace(0, 1, 50):
            x = 3 + 4 * t
            # Gaussian-ish bump
            y = e_reactants + (peak_e - e_reactants) * np.exp(-((t - 0.35)**2) / 0.04)
            if t > 0.5:
                # Transition down to products
                blend = (t - 0.5) / 0.5
                y = peak_e * np.exp(-((t - 0.35)**2) / 0.04) + e_products * blend
                y = e_products + (peak_e - e_products) * np.exp(-((t - 0.35)**2) / 0.04)
            curve_points.append(axes.c2p(x, y))

        # Simpler approach: use a smooth curve through key points
        key_pts = [
            axes.c2p(3, e_reactants),
            axes.c2p(4, e_reactants + e_activation * 0.5),
            axes.c2p(5, e_reactants + e_activation),
            axes.c2p(6, e_products + (e_reactants + e_activation - e_products) * 0.5),
            axes.c2p(7, e_products),
        ]
        curve = VMobject(color=AUX_COLOR, stroke_width=2.5)
        curve.set_points_smoothly(key_pts)

        # Activation energy arrow
        ea_arrow = DoubleArrow(
            axes.c2p(4.2, e_reactants), axes.c2p(4.2, e_reactants + e_activation),
            color=HIGHLIGHT_COLOR, stroke_width=2, buff=0,
            max_tip_length_to_length_ratio=0.1,
        )
        ea_lbl = MathTex(
            lbls.get("activation", r"E_a"),
            font_size=22, color=HIGHLIGHT_COLOR,
        )
        ea_lbl.next_to(ea_arrow, LEFT, buff=0.1)

        # Delta H arrow
        dh_arrow = DoubleArrow(
            axes.c2p(8.5, e_reactants), axes.c2p(8.5, e_products),
            color=LABEL_COLOR, stroke_width=2, buff=0,
            max_tip_length_to_length_ratio=0.1,
        )
        dh_lbl = MathTex(
            lbls.get("delta_h", r"\Delta H"),
            font_size=22, color=LABEL_COLOR,
        )
        dh_lbl.next_to(dh_arrow, RIGHT, buff=0.1)

        elements = VGroup(axes, x_lbl, y_lbl, r_line, r_lbl,
                          p_line, p_lbl, curve, ea_arrow, ea_lbl,
                          dh_arrow, dh_lbl)
        if position is not None:
            elements.move_to(position)

        # Animate
        self.play(Create(axes), FadeIn(x_lbl), FadeIn(y_lbl), run_time=T_SHAPE_CREATE)
        self.play(Create(r_line), FadeIn(r_lbl), run_time=0.8)
        self.play(Create(curve), run_time=T_SHAPE_CREATE)
        self.play(Create(p_line), FadeIn(p_lbl), run_time=0.8)
        self.play(GrowArrow(ea_arrow), FadeIn(ea_lbl), run_time=0.6)
        self.play(GrowArrow(dh_arrow), FadeIn(dh_lbl), run_time=0.6)
        self.wait(W_AFTER_KEY)

        return elements

    # ──────────────────────────────────────────
    #  ELECTRON CONFIGURATION
    # ──────────────────────────────────────────

    def show_electron_config(self, element_symbol, config_str, orbital_diagram=None,
                              position=None):
        """
        Display an electron configuration with optional orbital box diagram.

        Args:
            element_symbol: Element symbol (e.g. "Na").
            config_str: Configuration string LaTeX
                        (e.g. r"1s^2\\,2s^2\\,2p^6\\,3s^1").
            orbital_diagram: List of (orbital_name, n_electrons, max_electrons)
                            tuples for box diagram. None to skip.
                            e.g. [("1s", 2, 2), ("2s", 2, 2), ("2p", 6, 6), ("3s", 1, 2)]
            position: Where to place.

        Returns:
            VGroup of all elements.
        """
        # Element symbol
        elem = MathTex(
            r"\text{" + element_symbol + r"}: ",
            font_size=CALC_SIZE + 4, color=SHAPE_COLOR,
        )
        config = MathTex(config_str, font_size=CALC_SIZE, color=WHITE)

        top_line = VGroup(elem, config).arrange(RIGHT, buff=0.2)
        if position is not None:
            top_line.move_to(position + UP * 1.5)
        else:
            top_line.move_to(UP * 1.5)

        self.play(Write(elem), run_time=0.5)
        self.play(Write(config), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        elements = [top_line]

        # Orbital box diagram
        if orbital_diagram:
            boxes_group = VGroup()
            for orbital_name, n_e, max_e in orbital_diagram:
                # Label
                o_lbl = MathTex(orbital_name, font_size=18, color=BODY_TEXT_COLOR)

                # Boxes (one per electron pair slot)
                n_slots = max_e // 2 if max_e > 1 else 1
                slot_boxes = VGroup()
                for s in range(n_slots):
                    box = Square(side_length=0.35, color=DIVIDER_COLOR, stroke_width=1.5)
                    # Arrows inside
                    arrows_in = VGroup()
                    e_in_slot = min(2, n_e - s * 2)
                    if e_in_slot >= 1:
                        up_arrow = MathTex(r"\uparrow", font_size=16, color=ANSWER_COLOR)
                        up_arrow.move_to(box.get_center() + LEFT * 0.06)
                        arrows_in.add(up_arrow)
                    if e_in_slot >= 2:
                        down_arrow = MathTex(r"\downarrow", font_size=16, color=AUX_COLOR)
                        down_arrow.move_to(box.get_center() + RIGHT * 0.06)
                        arrows_in.add(down_arrow)
                    slot_boxes.add(VGroup(box, arrows_in))

                slot_boxes.arrange(RIGHT, buff=0.05)
                o_lbl.next_to(slot_boxes, DOWN, buff=0.1)
                orbital_group = VGroup(slot_boxes, o_lbl)
                boxes_group.add(orbital_group)

            boxes_group.arrange(RIGHT, buff=0.3)
            boxes_group.next_to(top_line, DOWN, buff=0.6)

            self.play(FadeIn(boxes_group), run_time=T_SHAPE_CREATE)
            self.wait(W_AFTER_KEY)
            elements.append(boxes_group)

        return VGroup(*elements)

    # ══════════════════════════════════════════
    #  CIRCUIT DIAGRAM COMPONENTS
    # ══════════════════════════════════════════

    @staticmethod
    def _resistor_zigzag(start, end, n_peaks=4, amplitude=0.15, color=None):
        """Create a zigzag resistor symbol between two points."""
        c = color or SHAPE_COLOR
        s = np.array(start)
        e = np.array(end)
        direction = e - s
        length = np.linalg.norm(direction)
        unit = direction / length
        perp = np.array([-unit[1], unit[0], 0])

        lead = length * 0.2
        zig_length = length - 2 * lead
        seg = zig_length / (2 * n_peaks)

        points = [s, s + unit * lead]
        for i in range(n_peaks):
            base = s + unit * (lead + 2 * i * seg)
            points.append(base + unit * (seg * 0.5) + perp * amplitude)
            points.append(base + unit * (seg * 1.5) - perp * amplitude)
        points.append(s + unit * (lead + zig_length))
        points.append(e)

        zigzag = VMobject(color=c, stroke_width=2.5)
        zigzag.set_points_as_corners(points)
        return zigzag

    @staticmethod
    def _battery_symbol(position, direction=RIGHT, size=0.4, color=None):
        """Create a battery symbol (long/short line pair)."""
        c = color or WHITE
        pos = np.array(position)
        d = np.array(direction)
        d = d / np.linalg.norm(d)
        perp = np.array([-d[1], d[0], 0])

        long_half = size * 0.5
        short_half = size * 0.3
        gap = size * 0.12

        long_line = Line(
            pos - perp * long_half + d * gap,
            pos + perp * long_half + d * gap,
            color=c, stroke_width=3,
        )
        short_line = Line(
            pos - perp * short_half - d * gap,
            pos + perp * short_half - d * gap,
            color=c, stroke_width=5,
        )
        plus = MathTex("+", font_size=16, color=c)
        plus.next_to(long_line, d, buff=0.08)

        return VGroup(long_line, short_line, plus)

    def draw_resistor(self, start, end, label_tex=None, color=None,
                       label_direction=None):
        """
        Draw a resistor between two points with optional label.

        Returns (resistor, label) tuple.
        """
        c = color or SHAPE_COLOR
        resistor = self._resistor_zigzag(start, end, color=c)

        lbl = None
        if label_tex:
            mid = (np.array(start) + np.array(end)) / 2
            if label_direction is None:
                d = np.array(end) - np.array(start)
                perp = np.array([-d[1], d[0], 0])
                norm = np.linalg.norm(perp)
                label_direction = perp / norm * 0.35 if norm > 1e-6 else UP * 0.35
            lbl = MathTex(label_tex, font_size=22, color=c)
            lbl.next_to(mid, label_direction, buff=0.05)

        return resistor, lbl

    def draw_wire(self, *points, color=None):
        """Draw a wire through a series of points."""
        c = color or WHITE
        wire = VMobject(color=c, stroke_width=2)
        wire.set_points_as_corners([np.array(p) for p in points])
        return wire

    def draw_battery(self, position, direction=RIGHT, label_tex=None,
                      size=0.4, color=None):
        """
        Draw a battery at a position.

        Returns (battery, label) tuple.
        """
        battery = self._battery_symbol(position, direction, size, color)

        lbl = None
        if label_tex:
            d = np.array(direction)
            d = d / np.linalg.norm(d)
            perp = np.array([-d[1], d[0], 0])
            lbl = MathTex(label_tex, font_size=22, color=color or WHITE)
            lbl.next_to(battery, perp * -1, buff=0.2)

        return battery, lbl

    def draw_node(self, position, color=None, radius=0.06):
        """Draw a junction node dot."""
        return Dot(np.array(position), color=color or WHITE, radius=radius)
