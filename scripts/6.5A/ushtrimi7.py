import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from manim import *
import numpy as np
from style_guide import (
    apply_style, make_divider, make_answer_box, fade_all,
    STEP_TITLE_COLOR, BODY_TEXT_COLOR, LABEL_COLOR,
    ANSWER_COLOR, SHAPE_COLOR, AUX_COLOR, HIGHLIGHT_COLOR, DIVIDER_COLOR,
    TITLE_SIZE, SUBTITLE_SIZE, PART_HEADER_SIZE, STEP_TITLE_SIZE,
    BODY_SIZE, PROBLEM_MATH_SIZE, CALC_SIZE, ANSWER_SIZE,
    T_TITLE_WRITE, T_SUBTITLE_FADE, T_HEADER_WRITE, T_STEP_TITLE,
    T_BODY_FADE, T_KEY_EQUATION, T_ROUTINE_EQUATION, T_SHAPE_CREATE,
    T_DOT_FADE, T_LAYOUT_SHIFT, T_TRANSITION,
    W_AFTER_KEY, W_AFTER_ROUTINE, W_AFTER_ANSWER, W_PROBLEM,
    CALC_TOP,
)


class Ushtrimi7(Scene):
    """
    Ushtrimi 7 — Njësia 6.5A
    Matematika 10-11: Pjesa II

    Tangjente ndaj rrethit x² + y² = 100 në pika të dhëna.
    """

    def construct(self):
        apply_style(self)

        self.title_screen()

        self.intro_method()
        fade_all(self)
        self.wait(0.5)

        self.part_a()
        fade_all(self)
        self.wait(0.5)

        self.part_b()
        fade_all(self)
        self.wait(0.5)

        self.part_c()
        fade_all(self)
        self.wait(0.5)

        self.final_summary()
        self.wait(W_AFTER_ANSWER)

    # ================================================================
    #  TITLE
    # ================================================================
    def title_screen(self):
        title = Text(
            "Ushtrimi 7 — Njësia 6.5A",
            font_size=TITLE_SIZE, color=WHITE, weight=BOLD,
        )
        source = Text(
            "Matematika 10-11: Pjesa II",
            font_size=SUBTITLE_SIZE, color=BODY_TEXT_COLOR,
        )
        source.next_to(title, DOWN, buff=0.4)

        self.play(Write(title), run_time=T_TITLE_WRITE)
        self.play(FadeIn(source, shift=UP * 0.2), run_time=T_SUBTITLE_FADE)
        self.wait(W_AFTER_KEY)
        self.play(FadeOut(title), FadeOut(source))
        self.wait(0.5)

    # ================================================================
    #  INTRO — explain the tangent method
    # ================================================================
    def intro_method(self):
        prob_title = Text("Problemi:", font_size=STEP_TITLE_SIZE + 2, color=STEP_TITLE_COLOR, weight=BOLD)
        prob_txt = Text(
            "Një rreth ka ekuacionin x² + y² = 100.\nShkruani ekuacionin e tangjentes në pikat\n(6,8), (8,6), (10,0).",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR, line_spacing=1.4,
        )
        VGroup(prob_title, prob_txt).arrange(DOWN, buff=0.4).move_to(UP * 1)

        self.play(FadeIn(prob_title), run_time=T_STEP_TITLE)
        self.play(FadeIn(prob_txt), run_time=T_BODY_FADE)
        self.wait(W_PROBLEM)

        # Method explanation
        m_title = Text("Metoda:", font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR, weight=BOLD)
        m_title.next_to(prob_txt, DOWN, buff=0.5)

        m1 = MathTex(
            r"m_{\text{rreze}} = \frac{y_P - 0}{x_P - 0} = \frac{y_P}{x_P}",
            font_size=CALC_SIZE,
        )
        m1.next_to(m_title, DOWN, buff=0.3)

        m2 = MathTex(
            r"m_{\text{tang}} = -\frac{1}{m_{\text{rreze}}} = -\frac{x_P}{y_P}",
            font_size=CALC_SIZE, color=LABEL_COLOR,
        )
        m2.next_to(m1, DOWN, buff=0.25)

        m3_txt = Text(
            "sepse rrezja ⊥ tangjentes",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        m3_txt.next_to(m2, DOWN, buff=0.2)

        self.play(FadeIn(m_title), run_time=T_STEP_TITLE)
        self.play(Write(m1), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)
        self.play(Write(m2), run_time=T_KEY_EQUATION)
        self.play(FadeIn(m3_txt), run_time=T_BODY_FADE)
        self.wait(W_AFTER_KEY)

    # ================================================================
    #  PART A — tangent at (6, 8)
    # ================================================================
    def part_a(self):
        header = Text("Pjesa a) — Pika (6, 8)", font_size=PART_HEADER_SIZE, color=LABEL_COLOR, weight=BOLD)
        header.to_corner(UL, buff=0.4)
        self.play(Write(header), run_time=T_HEADER_WRITE)

        # Graph
        axes = self.make_axes()
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")

        circle = self.make_circle(axes)

        # Radius line from O to (6,8)
        radius = Line(axes.c2p(0, 0), axes.c2p(6, 8), color=HIGHLIGHT_COLOR, stroke_width=2.5)

        # Tangent point
        dot_p = Dot(axes.c2p(6, 8), color=LABEL_COLOR, radius=0.1)
        lbl_p = MathTex("(6,\\,8)", font_size=22, color=LABEL_COLOR).next_to(dot_p, UR, buff=0.12)

        # Tangent line: y = -3/4 x + 25/2
        tangent = axes.plot(
            lambda x: -0.75 * x + 12.5,
            x_range=[-1, 13],
            color=AUX_COLOR, stroke_width=2.5,
        )

        # Right angle mark at tangent point
        graph_group = VGroup(axes, axes_labels, circle, radius, dot_p, lbl_p, tangent)

        self.play(Create(axes), FadeIn(axes_labels), run_time=T_SHAPE_CREATE)
        self.play(Create(circle), run_time=T_SHAPE_CREATE * 0.8)
        self.play(Create(radius), FadeIn(dot_p), FadeIn(lbl_p), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)
        self.play(Create(tangent), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        # Shift left
        self.play(graph_group.animate.shift(LEFT * 3.2), run_time=T_LAYOUT_SHIFT)
        div = make_divider()
        self.play(FadeIn(div), run_time=0.2)

        # Step 1: slope of radius
        s1 = Text("Koef. këndor i rrezes:", font_size=BODY_SIZE, color=BODY_TEXT_COLOR)
        s1.move_to(CALC_TOP)

        eq1 = MathTex(r"m = \frac{8}{6} = \frac{4}{3}", font_size=CALC_SIZE)
        eq1.next_to(s1, DOWN, buff=0.25)

        # Step 2: slope of tangent
        s2 = Text("Koef. këndor i tangjentes:", font_size=BODY_SIZE, color=BODY_TEXT_COLOR)
        s2.next_to(eq1, DOWN, buff=0.35)

        eq2 = MathTex(r"m' = -\frac{1}{\frac{4}{3}} = -\frac{3}{4}", font_size=CALC_SIZE, color=LABEL_COLOR)
        eq2.next_to(s2, DOWN, buff=0.25)

        # Step 3: find c
        s3 = Text("Gjejmë c (y = m'x + c):", font_size=BODY_SIZE, color=BODY_TEXT_COLOR)
        s3.next_to(eq2, DOWN, buff=0.35)

        eq3 = MathTex(r"8 = -\frac{3}{4} \cdot 6 + c", font_size=CALC_SIZE)
        eq3.next_to(s3, DOWN, buff=0.2)

        eq4 = MathTex(r"c = 8 + \frac{18}{4} = \frac{50}{4} = \frac{25}{2}", font_size=CALC_SIZE)
        eq4.next_to(eq3, DOWN, buff=0.2)

        self.play(FadeIn(s1), run_time=T_STEP_TITLE)
        self.play(Write(eq1), run_time=T_ROUTINE_EQUATION)
        self.wait(0.6)
        self.play(FadeIn(s2), run_time=T_STEP_TITLE)
        self.play(Write(eq2), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)
        self.play(FadeIn(s3), run_time=T_STEP_TITLE)
        self.play(Write(eq3), run_time=T_ROUTINE_EQUATION)
        self.wait(0.5)
        self.play(Write(eq4), run_time=T_ROUTINE_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        # Answer
        ans = MathTex(r"y = -\frac{3}{4}x + \frac{25}{2}", font_size=ANSWER_SIZE, color=ANSWER_COLOR)
        ans.next_to(eq4, DOWN, buff=0.4)
        box = make_answer_box(ans)

        self.play(Write(ans), run_time=T_KEY_EQUATION)
        self.play(Create(box), run_time=0.5)
        self.wait(W_AFTER_ANSWER)

    # ================================================================
    #  PART B — tangent at (8, 6)
    # ================================================================
    def part_b(self):
        header = Text("Pjesa b) — Pika (8, 6)", font_size=PART_HEADER_SIZE, color=LABEL_COLOR, weight=BOLD)
        header.to_corner(UL, buff=0.4)
        self.play(Write(header), run_time=T_HEADER_WRITE)

        # Graph
        axes = self.make_axes()
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")
        circle = self.make_circle(axes)

        radius = Line(axes.c2p(0, 0), axes.c2p(8, 6), color=HIGHLIGHT_COLOR, stroke_width=2.5)
        dot_p = Dot(axes.c2p(8, 6), color=LABEL_COLOR, radius=0.1)
        lbl_p = MathTex("(8,\\,6)", font_size=22, color=LABEL_COLOR).next_to(dot_p, UR, buff=0.12)

        # y = -4/3 x + 50/3
        tangent = axes.plot(
            lambda x: -4 / 3 * x + 50 / 3,
            x_range=[-1, 13],
            color=AUX_COLOR, stroke_width=2.5,
        )

        graph_group = VGroup(axes, axes_labels, circle, radius, dot_p, lbl_p, tangent)

        self.play(Create(axes), FadeIn(axes_labels), run_time=T_SHAPE_CREATE)
        self.play(Create(circle), run_time=T_SHAPE_CREATE * 0.8)
        self.play(Create(radius), FadeIn(dot_p), FadeIn(lbl_p), run_time=T_KEY_EQUATION)
        self.play(Create(tangent), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        # Shift left
        self.play(graph_group.animate.shift(LEFT * 3.2), run_time=T_LAYOUT_SHIFT)
        div = make_divider()
        self.play(FadeIn(div), run_time=0.2)

        # Condensed algebra
        eq1 = MathTex(r"m = \frac{6}{8} = \frac{3}{4}", font_size=CALC_SIZE)
        eq1.move_to(CALC_TOP)

        eq2 = MathTex(r"m' = -\frac{4}{3}", font_size=CALC_SIZE, color=LABEL_COLOR)
        eq2.next_to(eq1, DOWN, buff=0.3)

        eq3 = MathTex(r"6 = -\frac{4}{3} \cdot 8 + c \;\Rightarrow\; c = \frac{50}{3}", font_size=CALC_SIZE)
        eq3.next_to(eq2, DOWN, buff=0.3)

        ans = MathTex(r"y = -\frac{4}{3}x + \frac{50}{3}", font_size=ANSWER_SIZE, color=ANSWER_COLOR)
        ans.next_to(eq3, DOWN, buff=0.5)
        box = make_answer_box(ans)

        self.play(Write(eq1), run_time=T_ROUTINE_EQUATION)
        self.wait(0.5)
        self.play(Write(eq2), run_time=T_ROUTINE_EQUATION)
        self.wait(0.5)
        self.play(Write(eq3), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)
        self.play(Write(ans), run_time=T_KEY_EQUATION)
        self.play(Create(box), run_time=0.5)
        self.wait(W_AFTER_ANSWER)

    # ================================================================
    #  PART C — tangent at (10, 0)
    # ================================================================
    def part_c(self):
        header = Text("Pjesa c) — Pika (10, 0)", font_size=PART_HEADER_SIZE, color=LABEL_COLOR, weight=BOLD)
        header.to_corner(UL, buff=0.4)
        self.play(Write(header), run_time=T_HEADER_WRITE)

        # Graph
        axes = self.make_axes()
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")
        circle = self.make_circle(axes)

        radius = Line(axes.c2p(0, 0), axes.c2p(10, 0), color=HIGHLIGHT_COLOR, stroke_width=2.5)
        dot_p = Dot(axes.c2p(10, 0), color=LABEL_COLOR, radius=0.1)
        lbl_p = MathTex("(10,\\,0)", font_size=22, color=LABEL_COLOR).next_to(dot_p, DR, buff=0.12)

        # Tangent is vertical: x = 10
        tangent = DashedLine(
            axes.c2p(10, -11), axes.c2p(10, 11),
            color=AUX_COLOR, stroke_width=2.5, dash_length=0.1,
        )
        tang_lbl = MathTex("x = 10", font_size=22, color=AUX_COLOR).next_to(tangent, RIGHT, buff=0.15).shift(UP * 2)

        graph_group = VGroup(axes, axes_labels, circle, radius, dot_p, lbl_p, tangent, tang_lbl)

        self.play(Create(axes), FadeIn(axes_labels), run_time=T_SHAPE_CREATE)
        self.play(Create(circle), run_time=T_SHAPE_CREATE * 0.8)
        self.play(Create(radius), FadeIn(dot_p), FadeIn(lbl_p), run_time=T_KEY_EQUATION)
        self.play(Create(tangent), FadeIn(tang_lbl), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        # Shift left
        self.play(graph_group.animate.shift(LEFT * 3.2), run_time=T_LAYOUT_SHIFT)
        div = make_divider()
        self.play(FadeIn(div), run_time=0.2)

        # Explanation
        txt1 = Text(
            "Rrezja shtrihet përgjatë boshtit Ox.",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        txt1.move_to(CALC_TOP)

        txt2 = Text(
            "Tangjentja është pingulja e boshtit\nOx në pikën (10, 0).",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR, line_spacing=1.4,
        )
        txt2.next_to(txt1, DOWN, buff=0.3)

        ans = MathTex(r"x = 10", font_size=ANSWER_SIZE, color=ANSWER_COLOR)
        ans.next_to(txt2, DOWN, buff=0.5)
        box = make_answer_box(ans)

        self.play(FadeIn(txt1), run_time=T_BODY_FADE)
        self.wait(W_AFTER_ROUTINE)
        self.play(FadeIn(txt2), run_time=T_BODY_FADE)
        self.wait(W_AFTER_ROUTINE)
        self.play(Write(ans), run_time=T_KEY_EQUATION)
        self.play(Create(box), run_time=0.5)
        self.wait(W_AFTER_ANSWER)

    # ================================================================
    #  FINAL SUMMARY
    # ================================================================
    def final_summary(self):
        title = Text(
            "Përmbledhje e përgjigjeve",
            font_size=PART_HEADER_SIZE + 4, color=WHITE, weight=BOLD,
        )
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=T_TITLE_WRITE)

        rows = VGroup(
            MathTex(r"\text{a)}\quad y = -\frac{3}{4}x + \frac{25}{2}", font_size=30),
            MathTex(r"\text{b)}\quad y = -\frac{4}{3}x + \frac{50}{3}", font_size=30),
            MathTex(r"\text{c)}\quad x = 10", font_size=30),
        )
        for row in rows:
            row.set_color(ANSWER_COLOR)

        rows.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        rows.next_to(title, DOWN, buff=0.6)

        box = make_answer_box(rows)

        self.play(
            LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3) for r in rows], lag_ratio=0.2),
            run_time=1.5,
        )
        self.play(Create(box), run_time=0.6)

    # ================================================================
    #  HELPERS
    # ================================================================
    def make_axes(self):
        return Axes(
            x_range=[-12, 14, 2],
            y_range=[-12, 14, 2],
            x_length=5.5, y_length=5.5,
            axis_config={
                "include_tip": True,
                "include_numbers": True,
                "font_size": 16,
                "color": DIVIDER_COLOR,
            },
        )

    def make_circle(self, axes):
        return axes.plot_parametric_curve(
            lambda t: np.array([10 * np.cos(t), 10 * np.sin(t), 0]),
            t_range=[0, 2 * PI],
            color=SHAPE_COLOR, stroke_width=3,
        )
