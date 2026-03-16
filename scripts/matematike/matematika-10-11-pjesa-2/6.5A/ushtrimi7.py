import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from manim import *
import numpy as np
from components import ExerciseScene
from style_guide import (
    make_answer_box, make_divider, fade_all,
    STEP_TITLE_COLOR, BODY_TEXT_COLOR, LABEL_COLOR,
    ANSWER_COLOR, SHAPE_COLOR, AUX_COLOR, HIGHLIGHT_COLOR, DIVIDER_COLOR,
    PART_HEADER_SIZE, STEP_TITLE_SIZE,
    BODY_SIZE, CALC_SIZE, ANSWER_SIZE,
    T_STEP_TITLE, T_BODY_FADE, T_KEY_EQUATION, T_ROUTINE_EQUATION,
    T_SHAPE_CREATE, T_LAYOUT_SHIFT, T_TRANSITION,
    W_AFTER_KEY, W_AFTER_ROUTINE, W_AFTER_ANSWER, W_PROBLEM,
    CALC_TOP, PX,
)


class Ushtrimi7(ExerciseScene):
    """
    Ushtrimi 7 — Njesia 6.5A
    Matematika 10-11: Pjesa II

    Gjeni ekuacionin e tangjentes ndaj rrethit x^2 + y^2 = 100
    ne pikat (6,8), (8,6), (10,0).

    Visual storytelling — no voiceover.
    Every computed value animates onto the figure.
    Perpendicularity of radius and tangent shown visually.
    """

    exercise_number = 7
    unit = "6.5A"
    parts = ["a", "b", "c"]

    # ── Graph builder ──

    def _build_graph(self, px, py, show_tangent=False, tangent_func=None,
                     tangent_range=None, vertical_tangent=False):
        """
        Build the circle x^2+y^2=100 on axes with the tangent point marked
        and radius drawn. Returns (axes, graph_group, radius_line, dot, dot_label).
        Tangent line is NOT drawn here — it will be animated later.
        """
        axes = Axes(
            x_range=[-13, 14, 2], y_range=[-13, 14, 2],
            x_length=5.5, y_length=5.5,
            axis_config={
                "include_tip": True, "include_numbers": True,
                "font_size": 16, "color": DIVIDER_COLOR,
            },
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")
        circle = self.plot_circle(axes, 10)

        # Origin dot
        origin_dot = Dot(axes.c2p(0, 0), color=WHITE, radius=0.05)

        # Tangent point
        dot_dir = UR
        if py == 0:
            dot_dir = DR
        dot_p = Dot(axes.c2p(px, py), color=LABEL_COLOR, radius=0.1)
        lbl_p = MathTex(
            f"({px},\\,{py})", font_size=22, color=LABEL_COLOR,
        )
        lbl_p.next_to(dot_p, dot_dir, buff=0.15)

        # Radius line from origin to tangent point
        radius_line = Line(
            axes.c2p(0, 0), axes.c2p(px, py),
            color=HIGHLIGHT_COLOR, stroke_width=2.5,
        )

        graph_group = VGroup(axes, axes_labels, circle, origin_dot,
                             radius_line, dot_p, lbl_p)

        # Animate: axes first, then circle, then radius + point
        self.play(Create(axes), FadeIn(axes_labels), run_time=T_SHAPE_CREATE)
        self.play(Create(circle), run_time=T_SHAPE_CREATE * 0.8)
        self.wait(0.5)
        self.play(FadeIn(origin_dot), run_time=0.3)
        self.play(FadeIn(dot_p), FadeIn(lbl_p), run_time=0.5)
        self.wait(0.5)
        self.play(Create(radius_line), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        return axes, graph_group, radius_line, dot_p, lbl_p

    def _draw_right_angle_at_tangent(self, axes, px, py, m_radius, graph_group):
        """
        Draw a small right-angle mark at the tangent point between
        the radius direction and the tangent direction.
        Returns the right-angle mark mobject.
        """
        # Tangent point in scene coordinates
        tp = axes.c2p(px, py)
        op = axes.c2p(0, 0)

        # Direction from tangent point TOWARD the origin (along radius, inward)
        rad_vec = np.array(op) - np.array(tp)
        rad_vec = rad_vec / np.linalg.norm(rad_vec)

        # Tangent direction: perpendicular to radius, pick one
        tang_vec = np.array([-rad_vec[1], rad_vec[0], 0])

        size = 0.2
        corner = np.array(tp) + size * rad_vec + size * tang_vec
        p1 = np.array(tp) + size * rad_vec
        p2 = np.array(tp) + size * tang_vec

        right_angle = VMobject(color=AUX_COLOR, stroke_width=2)
        right_angle.set_points_as_corners([p1, corner, p2])

        self.play(Create(right_angle), run_time=0.5)
        graph_group.add(right_angle)
        return right_angle

    def _draw_tangent_line(self, axes, tangent_func, tangent_range, graph_group):
        """Draw the tangent line on the graph and add to group."""
        tangent = axes.plot(
            tangent_func, x_range=tangent_range,
            color=AUX_COLOR, stroke_width=2.5,
        )
        self.play(Create(tangent), run_time=T_KEY_EQUATION)
        graph_group.add(tangent)
        return tangent

    def _draw_vertical_tangent(self, axes, x_val, graph_group):
        """Draw a vertical tangent line x = constant."""
        tangent = DashedLine(
            axes.c2p(x_val, -12), axes.c2p(x_val, 12),
            color=AUX_COLOR, stroke_width=2.5, dash_length=0.1,
        )
        self.play(Create(tangent), run_time=T_KEY_EQUATION)
        graph_group.add(tangent)
        return tangent

    # ================================================================
    #  PART A — tangent at (6, 8) — FULL DETAIL
    # ================================================================
    def part_a(self):
        header = self.show_part_header("a")

        # ── Problem statement ──
        prob_title = MathTex(
            r"\text{Gjeni tangjenten ndaj rrethit}",
            font_size=BODY_SIZE + 4, color=STEP_TITLE_COLOR,
        )
        prob_eq = MathTex(
            r"x^2 + y^2 = 100",
            font_size=CALC_SIZE + 4,
        )
        prob_point = MathTex(
            r"\text{ne piken } (6,\, 8)",
            font_size=CALC_SIZE, color=LABEL_COLOR,
        )
        self.show_problem(prob_title, prob_eq, prob_point)

        # ── Build graph: circle + radius + tangent point ──
        axes, graph_group, radius_line, dot_p, lbl_p = self._build_graph(6, 8)

        # ── Shift graph left, add divider ──
        self.play(graph_group.animate.shift(LEFT * 3.2), run_time=T_LAYOUT_SHIFT)
        div = make_divider()
        self.play(FadeIn(div), run_time=0.2)
        self.wait(0.5)

        # ────────────────────────────────────────
        # Step 1: Radius slope
        # ────────────────────────────────────────
        s1t = self.panel_title("Koeficienti kendor i rrezes", y_pos=3.2)

        # Flash the radius on the figure
        self.play(Indicate(radius_line, color=YELLOW, scale_factor=1.05), run_time=0.6)
        self.wait(0.5)

        s1txt = self.panel_text([
            r"\text{Rrezja lidh qendren } (0,0)",
            r"\text{me piken } (6,\, 8)\text{:}",
        ], s1t)
        self.wait(1.5)

        eq1a = self.panel_eq(
            r"m = \frac{y_2 - y_1}{x_2 - x_1}",
            s1txt, font_size=30,
        )

        eq1b = self.panel_eq(
            r"m = \frac{8 - 0}{6 - 0} = \frac{8}{6} = \frac{4}{3}",
            eq1a, font_size=30, key=True,
        )

        # Transfer: label the radius on graph with its slope
        m_lbl = MathTex(r"m = \tfrac{4}{3}", font_size=20, color=HIGHLIGHT_COLOR)
        # Place near midpoint of radius
        rad_mid = (np.array(axes.c2p(0, 0)) + np.array(axes.c2p(6, 8))) / 2

        m_lbl.move_to(rad_mid + np.array([0.35, -0.25, 0]))
        self.transfer_value(eq1b, m_lbl)
        self.wait(1.5)

        # ────────────────────────────────────────
        # Step 2: Perpendicularity + tangent slope
        # ────────────────────────────────────────
        # Clear step 1 content
        calc1 = VGroup(s1t, s1txt, eq1a, eq1b)
        self.play(FadeOut(calc1), run_time=0.5)

        s2t = self.panel_title("Koeficienti kendor i tangjentes", y_pos=3.2)

        s2txt = self.panel_text([
            r"\text{Rrezja eshte pingule me tangjenten:}",
        ], s2t)
        self.wait(1.5)

        # Show perpendicularity rule
        eq2a = self.panel_eq(
            r"m \times m' = -1",
            s2txt, font_size=34, color=STEP_TITLE_COLOR, key=True,
        )

        # Draw right angle mark at tangent point on figure
        ra_mark = self._draw_right_angle_at_tangent(axes, 6, 8, 4/3, graph_group)
        self.wait(1.5)

        # Calculate tangent slope step by step
        eq2b = self.panel_eq(
            r"m' = -\frac{1}{m} = -\frac{1}{\frac{4}{3}}",
            eq2a, font_size=30,
        )

        eq2c = self.panel_eq(
            r"m' = -1 \times \frac{3}{4} = -\frac{3}{4}",
            eq2b, font_size=30, color=LABEL_COLOR, key=True,
        )
        self.wait(1.5)

        # ────────────────────────────────────────
        # Step 3: Find c (y-intercept)
        # ────────────────────────────────────────
        # Clear step 2 content
        calc2 = VGroup(s2t, s2txt, eq2a, eq2b, eq2c)
        self.play(FadeOut(calc2), run_time=0.5)

        s3t = self.panel_title("Gjejme c (pikeprerjen me Oy)", y_pos=3.2)

        s3txt = self.panel_text([
            r"\text{Zevendesojme piken } (6,\, 8)",
            r"\text{ne } y = m'x + c\text{:}",
        ], s3t)
        self.wait(1.5)

        # Flash the tangent point on the figure
        self.play(Indicate(dot_p, color=YELLOW, scale_factor=1.5), run_time=0.5)
        self.wait(0.5)

        eq3a = self.panel_eq(
            r"8 = -\frac{3}{4} \cdot 6 + c",
            s3txt, font_size=30,
        )

        eq3b = self.panel_eq(
            r"8 = -\frac{18}{4} + c",
            eq3a, font_size=30,
        )

        eq3c = self.panel_eq(
            r"c = 8 + \frac{18}{4}",
            eq3b, font_size=30,
        )

        eq3d = self.panel_eq(
            r"c = \frac{32}{4} + \frac{18}{4} = \frac{50}{4} = \frac{25}{2}",
            eq3c, font_size=30, key=True,
        )
        self.wait(1.5)

        # ────────────────────────────────────────
        # Step 4: Final tangent equation + draw on graph
        # ────────────────────────────────────────
        # Clear step 3 content
        calc3 = VGroup(s3t, s3txt, eq3a, eq3b, eq3c, eq3d)
        self.play(FadeOut(calc3), run_time=0.5)

        s4t = self.panel_title("Ekuacioni i tangjentes", y_pos=3.0)
        self.wait(0.5)

        eq_final = self.panel_eq(
            r"y = -\frac{3}{4}x + \frac{25}{2}",
            s4t, font_size=ANSWER_SIZE, color=ANSWER_COLOR, key=True,
        )
        box = make_answer_box(eq_final)
        self.play(Create(box), run_time=0.5)
        self.wait(1.5)

        # Draw tangent line on the graph
        tangent = axes.plot(
            lambda x: -0.75 * x + 12.5,
            x_range=[-4, 12],
            color=AUX_COLOR, stroke_width=2.5,
        )
        self.play(Create(tangent), run_time=T_KEY_EQUATION)
        graph_group.add(tangent)
        self.wait(1)

        # Transfer tangent equation label to the graph
        tang_lbl = MathTex(
            r"y = -\tfrac{3}{4}x + \tfrac{25}{2}",
            font_size=18, color=AUX_COLOR,
        )
        tang_point = np.array(axes.c2p(1, 12.5 - 0.75))
        tang_lbl.move_to(tang_point + UP * 0.35 + LEFT * 0.3)
        self.transfer_value(eq_final, tang_lbl)
        graph_group.add(tang_lbl)
        self.wait(3)

        # Fade radius slope label
        self.play(FadeOut(m_lbl), run_time=0.3)
        self.wait(1)

    # ================================================================
    #  PART B — tangent at (8, 6) — MODERATE DETAIL
    # ================================================================
    def part_b(self):
        header = self.show_part_header("b")

        # ── Problem statement (brief) ──
        prob_title = MathTex(
            r"\text{Tangjentja ne piken}",
            font_size=BODY_SIZE + 4, color=STEP_TITLE_COLOR,
        )
        prob_point = MathTex(
            r"(8,\, 6)", font_size=CALC_SIZE + 4, color=LABEL_COLOR,
        )
        self.show_problem(prob_title, prob_point, wait_time=2.0)

        # ── Build graph ──
        axes, graph_group, radius_line, dot_p, lbl_p = self._build_graph(8, 6)

        # ── Shift graph left ──
        self.play(graph_group.animate.shift(LEFT * 3.2), run_time=T_LAYOUT_SHIFT)
        div = make_divider()
        self.play(FadeIn(div), run_time=0.2)
        self.wait(0.5)

        # ────────────────────────────────────────
        # Step 1: Radius slope
        # ────────────────────────────────────────
        s1t = self.panel_title("Koeficienti kendor i rrezes", y_pos=3.2)

        self.play(Indicate(radius_line, color=YELLOW, scale_factor=1.05), run_time=0.5)

        eq1 = self.panel_eq(
            r"m = \frac{6}{8} = \frac{3}{4}",
            s1t, font_size=32, key=True,
        )
        self.wait(1)

        # ────────────────────────────────────────
        # Step 2: Tangent slope (perpendicularity)
        # ────────────────────────────────────────
        s2t = self.panel_title("Rrezja } \\perp \\text{ tangjentes", ref=eq1, buff=0.4)

        # Show right angle mark on figure
        ra_mark = self._draw_right_angle_at_tangent(axes, 8, 6, 3/4, graph_group)
        self.wait(1)

        eq2a = self.panel_eq(
            r"m' = -\frac{1}{m} = -\frac{1}{\frac{3}{4}}",
            s2t, font_size=30,
        )

        eq2b = self.panel_eq(
            r"m' = -\frac{4}{3}",
            eq2a, font_size=32, color=LABEL_COLOR, key=True,
        )
        self.wait(1)

        # ────────────────────────────────────────
        # Step 3: Find c
        # ────────────────────────────────────────
        # Clear steps 1-2
        calc1 = VGroup(s1t, eq1, s2t, eq2a, eq2b)
        self.play(FadeOut(calc1), run_time=0.5)

        s3t = self.panel_title("Gjejme c", y_pos=3.2)

        s3txt = self.panel_text([
            r"\text{Zevendesojme piken } (8,\, 6)\text{:}",
        ], s3t)

        self.play(Indicate(dot_p, color=YELLOW, scale_factor=1.5), run_time=0.5)
        self.wait(0.5)

        eq3a = self.panel_eq(
            r"6 = -\frac{4}{3} \cdot 8 + c",
            s3txt, font_size=30,
        )

        eq3b = self.panel_eq(
            r"6 = -\frac{32}{3} + c",
            eq3a, font_size=30,
        )

        eq3c = self.panel_eq(
            r"c = 6 + \frac{32}{3} = \frac{18}{3} + \frac{32}{3} = \frac{50}{3}",
            eq3b, font_size=28, key=True,
        )
        self.wait(1)

        # ────────────────────────────────────────
        # Step 4: Final answer + draw tangent
        # ────────────────────────────────────────
        calc2 = VGroup(s3t, s3txt, eq3a, eq3b, eq3c)
        self.play(FadeOut(calc2), run_time=0.5)

        s4t = self.panel_title("Ekuacioni i tangjentes", y_pos=3.0)

        eq_final = self.panel_eq(
            r"y = -\frac{4}{3}x + \frac{50}{3}",
            s4t, font_size=ANSWER_SIZE, color=ANSWER_COLOR, key=True,
        )
        box = make_answer_box(eq_final)
        self.play(Create(box), run_time=0.5)
        self.wait(1.5)

        # Draw tangent on graph
        tangent = axes.plot(
            lambda x: -4/3 * x + 50/3,
            x_range=[-4, 12],
            color=AUX_COLOR, stroke_width=2.5,
        )
        self.play(Create(tangent), run_time=T_KEY_EQUATION)
        graph_group.add(tangent)
        self.wait(1)

        # Transfer label to graph
        tang_lbl = MathTex(
            r"y = -\tfrac{4}{3}x + \tfrac{50}{3}",
            font_size=18, color=AUX_COLOR,
        )
        tang_point = np.array(axes.c2p(2, 50/3 - 8/3))
        tang_lbl.move_to(tang_point + UP * 0.35 + LEFT * 0.5)
        self.transfer_value(eq_final, tang_lbl)
        graph_group.add(tang_lbl)
        self.wait(3)

    # ================================================================
    #  PART C — tangent at (10, 0) — SPECIAL CASE: vertical tangent
    # ================================================================
    def part_c(self):
        header = self.show_part_header("c")

        # ── Problem statement ──
        prob_title = MathTex(
            r"\text{Tangjentja ne piken}",
            font_size=BODY_SIZE + 4, color=STEP_TITLE_COLOR,
        )
        prob_point = MathTex(
            r"(10,\, 0)", font_size=CALC_SIZE + 4, color=LABEL_COLOR,
        )
        self.show_problem(prob_title, prob_point, wait_time=2.0)

        # ── Build graph ──
        axes, graph_group, radius_line, dot_p, lbl_p = self._build_graph(10, 0)

        # ── Shift graph left ──
        self.play(graph_group.animate.shift(LEFT * 3.2), run_time=T_LAYOUT_SHIFT)
        div = make_divider()
        self.play(FadeIn(div), run_time=0.2)
        self.wait(0.5)

        # ────────────────────────────────────────
        # Step 1: Observe the radius
        # ────────────────────────────────────────
        s1t = self.panel_title("Koeficienti kendor i rrezes", y_pos=3.2)

        self.play(Indicate(radius_line, color=YELLOW, scale_factor=1.05), run_time=0.6)
        self.wait(0.5)

        s1txt = self.panel_text([
            r"\text{Rrezja shkon nga } (0,0)",
            r"\text{ne } (10,\, 0)\text{, pergjate boshtit } Ox\text{.}",
        ], s1t)
        self.wait(2)

        eq1 = self.panel_eq(
            r"m = \frac{0 - 0}{10 - 0} = \frac{0}{10} = 0",
            s1txt, font_size=30, key=True,
        )

        s1note = self.panel_text([
            r"\text{Rrezja eshte horizontale } (m = 0)\text{.}",
        ], eq1, buff=0.3)
        self.wait(2)

        # ────────────────────────────────────────
        # Step 2: Perpendicular to horizontal = vertical
        # ────────────────────────────────────────
        calc1 = VGroup(s1t, s1txt, eq1, s1note)
        self.play(FadeOut(calc1), run_time=0.5)

        s2t = self.panel_title("Rrezja } \\perp \\text{ tangjentes", y_pos=3.2)

        s2txt = self.panel_text([
            r"\text{Nje drejtez pingule me nje}",
            r"\text{drejtez horizontale eshte}",
            r"\text{nje drejtez vertikale.}",
        ], s2t)
        self.wait(2.5)

        # Draw right angle mark at (10,0) — between horizontal radius and vertical tangent
        tp = np.array(axes.c2p(10, 0))
        sz = 0.2
        ra_p1 = tp + LEFT * sz
        ra_corner = tp + LEFT * sz + UP * sz
        ra_p2 = tp + UP * sz
        right_angle = VMobject(color=AUX_COLOR, stroke_width=2)
        right_angle.set_points_as_corners([ra_p1, ra_corner, ra_p2])
        self.play(Create(right_angle), run_time=0.5)
        graph_group.add(right_angle)
        self.wait(1.5)

        s2note = self.panel_text([
            r"\text{Tangjentja eshte vertikale.}",
            r"\text{Drejtezat vertikale kane formen:}",
        ], s2txt, buff=0.3)
        self.wait(1.5)

        eq2 = self.panel_eq(
            r"x = \text{konst.}",
            s2note, font_size=34, color=LABEL_COLOR,
        )
        self.wait(1)

        s2expl = self.panel_text([
            r"\text{Pika ka } x = 10\text{, pra:}",
        ], eq2, buff=0.3)
        self.wait(1)

        # ────────────────────────────────────────
        # Step 3: Final answer + draw tangent
        # ────────────────────────────────────────
        calc2 = VGroup(s2t, s2txt, s2note, eq2, s2expl)
        self.play(FadeOut(calc2), run_time=0.5)

        s3t = self.panel_title("Ekuacioni i tangjentes", y_pos=3.0)

        eq_final = self.panel_eq(
            r"x = 10",
            s3t, font_size=ANSWER_SIZE, color=ANSWER_COLOR, key=True,
        )
        box = make_answer_box(eq_final)
        self.play(Create(box), run_time=0.5)
        self.wait(1.5)

        # Draw vertical tangent line on graph
        tangent = DashedLine(
            axes.c2p(10, -11), axes.c2p(10, 11),
            color=AUX_COLOR, stroke_width=2.5, dash_length=0.1,
        )
        self.play(Create(tangent), run_time=T_KEY_EQUATION)
        graph_group.add(tangent)
        self.wait(1)

        # Transfer label to graph
        tang_lbl = MathTex(r"x = 10", font_size=20, color=AUX_COLOR)
        tang_lbl.next_to(tangent, RIGHT, buff=0.15).shift(UP * 1.5)
        self.transfer_value(eq_final, tang_lbl)
        graph_group.add(tang_lbl)
        self.wait(3)

    # ================================================================
    #  FINAL SUMMARY
    # ================================================================
    def final_summary(self):
        self.show_summary_table(
            "Permbledhje e pergjigjeve",
            [
                r"\text{a)}\quad y = -\frac{3}{4}x + \frac{25}{2}",
                r"\text{b)}\quad y = -\frac{4}{3}x + \frac{50}{3}",
                r"\text{c)}\quad x = 10",
            ],
            font_size=30,
        )
