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
        title = Text(
            f"Ushtrimi {self.exercise_number} — Njësia {self.unit}",
            font_size=TITLE_SIZE,
            color=WHITE,
            weight=BOLD,
        )
        source = Text(
            self.textbook,
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
        header = Text(
            f"Pjesa {label})",
            font_size=PART_HEADER_SIZE,
            color=LABEL_COLOR,
            weight=BOLD,
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

        Args:
            title_text: Title for the summary (e.g. "Përmbledhje").
            rows: List of LaTeX strings for each row.
            font_size: Font size for rows.
        """
        title = Text(
            title_text,
            font_size=PART_HEADER_SIZE + 4,
            color=WHITE,
            weight=BOLD,
        )
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=T_TITLE_WRITE)

        row_group = VGroup(
            *[MathTex(r, font_size=font_size, color=ANSWER_COLOR) for r in rows]
        )
        row_group.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        row_group.next_to(title, DOWN, buff=0.6)

        box = make_answer_box(row_group)

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

        Args:
            text: Step title text.
            position: Absolute position (takes precedence).
            reference: Place below this mobject if position is None.
            buff: Spacing from reference.

        Returns the title mobject.
        """
        title = Text(
            text,
            font_size=STEP_TITLE_SIZE,
            color=STEP_TITLE_COLOR,
            weight=BOLD,
        )
        if position is not None:
            title.move_to(position)
        elif reference is not None:
            title.next_to(reference, DOWN, buff=buff, aligned_edge=LEFT)
        else:
            title.move_to(CALC_TOP)

        self.play(FadeIn(title), run_time=T_STEP_TITLE)
        return title

    def show_equation(self, tex, reference=None, buff=0.25, key=False,
                      color=None, font_size=None):
        """
        Show a single equation below a reference.

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
                elif ref is not None:
                    eq.next_to(ref, DOWN, buff=0.3)
            else:
                ref = results[-1]
                eq = MathTex(eq_spec["tex"], font_size=fs or CALC_SIZE)
                if color:
                    eq.set_color(color)
                eq.next_to(ref, DOWN, buff=buff)

            rt = T_KEY_EQUATION if is_key else T_ROUTINE_EQUATION
            self.play(Write(eq), run_time=rt)
            if is_key:
                self.wait(W_AFTER_KEY if i == len(equations) - 1 else W_AFTER_ROUTINE)
            else:
                self.wait(0.6)

            results.append(eq)

        return results

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
