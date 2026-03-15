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
