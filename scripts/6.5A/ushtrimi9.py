import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

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


class Ushtrimi9(Scene):
    """
    Ushtrimi 9 — Njësia 6.5A
    Matematika 10-11: Pjesa II

    Sisteme ekuacionesh (rreth + drejtëz).
    """

    def construct(self):
        apply_style(self)

        # ====== TITLE ======
        self.title_screen()

        # ====== PARTS a–f ======
        self.part_a()
        fade_all(self)
        self.wait(0.5)

        self.part_b()
        fade_all(self)
        self.wait(0.5)

        self.part_c()
        fade_all(self)
        self.wait(0.5)

        self.part_d()
        fade_all(self)
        self.wait(0.5)

        self.part_e()
        fade_all(self)
        self.wait(0.5)

        self.part_f()
        fade_all(self)
        self.wait(0.5)

        # ====== FINAL SUMMARY ======
        self.final_summary()
        self.wait(W_AFTER_ANSWER)

    # ================================================================
    #  TITLE SCREEN
    # ================================================================
    def title_screen(self):
        title = Text(
            "Ushtrimi 9 — Njësia 6.5A",
            font_size=TITLE_SIZE,
            color=WHITE,
            weight=BOLD,
        )
        source = Text(
            "Matematika 10-11: Pjesa II",
            font_size=SUBTITLE_SIZE,
            color=BODY_TEXT_COLOR,
        )
        source.next_to(title, DOWN, buff=0.4)

        self.play(Write(title), run_time=T_TITLE_WRITE)
        self.play(FadeIn(source, shift=UP * 0.2), run_time=T_SUBTITLE_FADE)
        self.wait(W_AFTER_KEY)
        self.play(FadeOut(title), FadeOut(source))
        self.wait(0.5)

    # ================================================================
    #  PART A  —  x² + y² = 25,  y = x + 1
    #  Full detailed walkthrough
    # ================================================================
    def part_a(self):
        # — Header —
        header = Text("Pjesa a)", font_size=PART_HEADER_SIZE, color=LABEL_COLOR, weight=BOLD)
        header.to_corner(UL, buff=0.4)
        self.play(Write(header), run_time=T_HEADER_WRITE)

        # — Problem Statement —
        prob_title = Text("Sistemi:", font_size=STEP_TITLE_SIZE + 2, color=STEP_TITLE_COLOR, weight=BOLD)
        prob_eq = MathTex(
            r"\begin{cases} x^2 + y^2 = 25 \\ y = x + 1 \end{cases}",
            font_size=PROBLEM_MATH_SIZE + 4,
        )
        prob_group = VGroup(prob_title, prob_eq).arrange(DOWN, buff=0.5).move_to(ORIGIN)

        self.play(FadeIn(prob_group, shift=UP * 0.3), run_time=T_SHAPE_CREATE)
        self.wait(W_PROBLEM)
        self.play(FadeOut(prob_group), run_time=T_TRANSITION)
        self.wait(0.3)

        # — Graph (centered first, then shifted left) —
        axes = self.create_axes(7, 7)
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")

        circle = axes.plot_parametric_curve(
            lambda t: np.array([5 * np.cos(t), 5 * np.sin(t), 0]),
            t_range=[0, 2 * PI],
            color=SHAPE_COLOR,
            stroke_width=3,
        )
        circle_label = MathTex(r"x^2+y^2=25", font_size=20, color=SHAPE_COLOR)
        circle_label.next_to(circle, UR, buff=0.1).shift(LEFT * 0.5)

        line = axes.plot(lambda x: x + 1, x_range=[-6, 5.5], color=AUX_COLOR, stroke_width=2.5)
        line_label = MathTex(r"y=x+1", font_size=20, color=AUX_COLOR)
        line_label.next_to(line.point_from_proportion(0.85), UR, buff=0.15)

        # Intersection points
        dot1 = Dot(axes.c2p(3, 4), color=LABEL_COLOR, radius=0.1)
        dot2 = Dot(axes.c2p(-4, -3), color=HIGHLIGHT_COLOR, radius=0.1)
        lbl1 = MathTex("(3,\\,4)", font_size=22, color=LABEL_COLOR).next_to(dot1, UR, buff=0.15)
        lbl2 = MathTex("(-4,\\,-3)", font_size=22, color=HIGHLIGHT_COLOR).next_to(dot2, DL, buff=0.15)

        graph_group = VGroup(axes, axes_labels, circle, circle_label, line, line_label, dot1, dot2, lbl1, lbl2)

        # Animate graph construction
        self.play(Create(axes), FadeIn(axes_labels), run_time=T_SHAPE_CREATE)
        self.play(Create(circle), FadeIn(circle_label), run_time=T_SHAPE_CREATE)
        self.play(Create(line), FadeIn(line_label), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)
        self.play(FadeIn(dot1, scale=1.5), FadeIn(lbl1), run_time=T_DOT_FADE + 0.2)
        self.play(FadeIn(dot2, scale=1.5), FadeIn(lbl2), run_time=T_DOT_FADE + 0.2)
        self.wait(W_AFTER_KEY)

        # Shift graph to the left
        self.play(graph_group.animate.shift(LEFT * 3.2), run_time=T_LAYOUT_SHIFT)
        self.wait(0.3)

        # — Divider —
        div = make_divider()
        self.play(FadeIn(div), run_time=0.3)

        # — Step 1: Substitution —
        s1_title = Text("Hapi 1: Zëvendësimi", font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR, weight=BOLD)
        s1_title.move_to(CALC_TOP)

        s1_txt = Text(
            "Zëvendësojmë y = x + 1\nnë ekuacionin e rrethit:",
            font_size=BODY_SIZE,
            color=BODY_TEXT_COLOR,
            line_spacing=1.4,
        )
        s1_txt.next_to(s1_title, DOWN, buff=0.25, aligned_edge=LEFT)

        s1_eq1 = MathTex(r"x^2 + (x+1)^2 = 25", font_size=CALC_SIZE)
        s1_eq1.next_to(s1_txt, DOWN, buff=0.3)

        self.play(FadeIn(s1_title), run_time=T_STEP_TITLE)
        self.play(FadeIn(s1_txt), run_time=T_BODY_FADE)
        self.wait(W_AFTER_ROUTINE)
        self.play(Write(s1_eq1), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        # — Step 2: Expand & Simplify —
        s2_title = Text("Hapi 2: Thjeshtimi", font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR, weight=BOLD)
        s2_title.next_to(s1_eq1, DOWN, buff=0.4, aligned_edge=LEFT)

        s2_eq1 = MathTex(r"x^2 + x^2 + 2x + 1 = 25", font_size=CALC_SIZE)
        s2_eq1.next_to(s2_title, DOWN, buff=0.2)

        s2_eq2 = MathTex(r"2x^2 + 2x - 24 = 0", font_size=CALC_SIZE)
        s2_eq2.next_to(s2_eq1, DOWN, buff=0.2)

        s2_eq3 = MathTex(r"x^2 + x - 12 = 0", font_size=CALC_SIZE, color=LABEL_COLOR)
        s2_eq3.next_to(s2_eq2, DOWN, buff=0.2)

        self.play(FadeIn(s2_title), run_time=T_STEP_TITLE)
        self.play(Write(s2_eq1), run_time=T_ROUTINE_EQUATION)
        self.wait(0.8)
        self.play(Write(s2_eq2), run_time=T_ROUTINE_EQUATION)
        self.wait(0.8)
        self.play(Write(s2_eq3), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_KEY)

        # — Transition: clear top steps —
        top_items = VGroup(s1_title, s1_txt, s1_eq1, s2_title, s2_eq1, s2_eq2, s2_eq3)
        self.play(FadeOut(top_items), run_time=T_TRANSITION)
        self.wait(0.3)

        # — Step 3: Factor —
        s3_title = Text("Hapi 3: Faktorizimi", font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR, weight=BOLD)
        s3_title.move_to(CALC_TOP)

        s3_eq1 = MathTex(r"x^2 + x - 12 = 0", font_size=CALC_SIZE)
        s3_eq1.next_to(s3_title, DOWN, buff=0.3)

        s3_eq2 = MathTex(r"(x - 3)(x + 4) = 0", font_size=CALC_SIZE, color=LABEL_COLOR)
        s3_eq2.next_to(s3_eq1, DOWN, buff=0.25)

        s3_eq3 = MathTex(r"x_1 = 3 \qquad x_2 = -4", font_size=CALC_SIZE + 2, color=ANSWER_COLOR)
        s3_eq3.next_to(s3_eq2, DOWN, buff=0.35)

        self.play(FadeIn(s3_title), run_time=T_STEP_TITLE)
        self.play(Write(s3_eq1), run_time=T_ROUTINE_EQUATION)
        self.wait(W_AFTER_ROUTINE)
        self.play(Write(s3_eq2), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)
        self.play(Write(s3_eq3), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_KEY)

        # — Step 4: Find y —
        s4_title = Text("Hapi 4: Gjejmë y", font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR, weight=BOLD)
        s4_title.next_to(s3_eq3, DOWN, buff=0.5, aligned_edge=LEFT)

        s4_eq1 = MathTex(r"y_1 = 3 + 1 = 4", font_size=CALC_SIZE)
        s4_eq1.next_to(s4_title, DOWN, buff=0.25)

        s4_eq2 = MathTex(r"y_2 = -4 + 1 = -3", font_size=CALC_SIZE)
        s4_eq2.next_to(s4_eq1, DOWN, buff=0.2)

        self.play(FadeIn(s4_title), run_time=T_STEP_TITLE)
        self.play(Write(s4_eq1), run_time=T_ROUTINE_EQUATION)
        self.wait(0.8)
        self.play(Write(s4_eq2), run_time=T_ROUTINE_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        # — Answer box —
        ans = MathTex(
            r"(3,\,4) \quad \text{dhe} \quad (-4,\,-3)",
            font_size=ANSWER_SIZE,
            color=ANSWER_COLOR,
        )
        ans.next_to(s4_eq2, DOWN, buff=0.5)
        box = make_answer_box(ans)

        self.play(Write(ans), run_time=T_KEY_EQUATION)
        self.play(Create(box), run_time=0.5)
        self.wait(W_AFTER_ANSWER)

    # ================================================================
    #  PART B  —  x² + y² = 25,  y = 2x − 5
    # ================================================================
    def part_b(self):
        header = Text("Pjesa b)", font_size=PART_HEADER_SIZE, color=LABEL_COLOR, weight=BOLD)
        header.to_corner(UL, buff=0.4)
        self.play(Write(header), run_time=T_HEADER_WRITE)

        # Problem
        prob = MathTex(
            r"\begin{cases} x^2 + y^2 = 25 \\ y = 2x - 5 \end{cases}",
            font_size=PROBLEM_MATH_SIZE + 4,
        )
        prob.move_to(ORIGIN)
        self.play(FadeIn(prob, shift=UP * 0.3), run_time=T_SHAPE_CREATE)
        self.wait(W_PROBLEM - 1)
        self.play(FadeOut(prob), run_time=T_TRANSITION)
        self.wait(0.3)

        # Graph
        axes = self.create_axes(7, 7)
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")

        circle = axes.plot_parametric_curve(
            lambda t: np.array([5 * np.cos(t), 5 * np.sin(t), 0]),
            t_range=[0, 2 * PI], color=SHAPE_COLOR, stroke_width=3,
        )
        line = axes.plot(lambda x: 2 * x - 5, x_range=[-1, 6], color=AUX_COLOR, stroke_width=2.5)

        dot1 = Dot(axes.c2p(0, -5), color=LABEL_COLOR, radius=0.1)
        dot2 = Dot(axes.c2p(4, 3), color=HIGHLIGHT_COLOR, radius=0.1)
        lbl1 = MathTex("(0,\\,-5)", font_size=22, color=LABEL_COLOR).next_to(dot1, DL, buff=0.15)
        lbl2 = MathTex("(4,\\,3)", font_size=22, color=HIGHLIGHT_COLOR).next_to(dot2, UR, buff=0.15)

        graph_group = VGroup(axes, axes_labels, circle, line, dot1, dot2, lbl1, lbl2)

        self.play(Create(axes), FadeIn(axes_labels), run_time=T_SHAPE_CREATE)
        self.play(Create(circle), run_time=T_SHAPE_CREATE * 0.8)
        self.play(Create(line), run_time=T_KEY_EQUATION * 0.8)
        self.play(FadeIn(dot1, scale=1.5), FadeIn(lbl1), FadeIn(dot2, scale=1.5), FadeIn(lbl2), run_time=0.6)
        self.wait(W_AFTER_ROUTINE)

        # Shift left
        self.play(graph_group.animate.shift(LEFT * 3.2), run_time=T_LAYOUT_SHIFT)
        div = make_divider()
        self.play(FadeIn(div), run_time=0.2)

        # Algebra
        s1 = Text("Zëvendësojmë y = 2x − 5:", font_size=BODY_SIZE, color=BODY_TEXT_COLOR)
        s1.move_to(CALC_TOP)

        eq1 = MathTex(r"x^2 + (2x-5)^2 = 25", font_size=CALC_SIZE)
        eq1.next_to(s1, DOWN, buff=0.3)

        eq2 = MathTex(r"x^2 + 4x^2 - 20x + 25 = 25", font_size=CALC_SIZE)
        eq2.next_to(eq1, DOWN, buff=0.2)

        eq3 = MathTex(r"5x^2 - 20x = 0", font_size=CALC_SIZE, color=LABEL_COLOR)
        eq3.next_to(eq2, DOWN, buff=0.2)

        eq4 = MathTex(r"5x(x - 4) = 0", font_size=CALC_SIZE)
        eq4.next_to(eq3, DOWN, buff=0.2)

        eq5 = MathTex(r"x_1 = 0 \qquad x_2 = 4", font_size=CALC_SIZE + 2, color=ANSWER_COLOR)
        eq5.next_to(eq4, DOWN, buff=0.3)

        self.play(FadeIn(s1), run_time=T_STEP_TITLE)
        self.play(Write(eq1), run_time=T_KEY_EQUATION)
        self.wait(0.8)
        self.play(Write(eq2), run_time=T_ROUTINE_EQUATION)
        self.wait(0.6)
        self.play(Write(eq3), run_time=T_ROUTINE_EQUATION)
        self.wait(0.6)
        self.play(Write(eq4), run_time=T_ROUTINE_EQUATION)
        self.wait(0.8)
        self.play(Write(eq5), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        # Transition
        self.play(FadeOut(VGroup(s1, eq1, eq2, eq3, eq4, eq5)), run_time=T_TRANSITION)

        # Find y
        y_title = Text("Gjejmë y:", font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR, weight=BOLD)
        y_title.move_to(CALC_TOP)

        y_eq1 = MathTex(r"y_1 = 2(0) - 5 = -5", font_size=CALC_SIZE)
        y_eq1.next_to(y_title, DOWN, buff=0.3)

        y_eq2 = MathTex(r"y_2 = 2(4) - 5 = 3", font_size=CALC_SIZE)
        y_eq2.next_to(y_eq1, DOWN, buff=0.2)

        ans = MathTex(
            r"(0,\,-5) \quad \text{dhe} \quad (4,\,3)",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        ans.next_to(y_eq2, DOWN, buff=0.5)
        box = make_answer_box(ans)

        self.play(FadeIn(y_title), run_time=T_STEP_TITLE)
        self.play(Write(y_eq1), run_time=T_ROUTINE_EQUATION)
        self.wait(0.6)
        self.play(Write(y_eq2), run_time=T_ROUTINE_EQUATION)
        self.wait(W_AFTER_ROUTINE)
        self.play(Write(ans), run_time=T_KEY_EQUATION)
        self.play(Create(box), run_time=0.5)
        self.wait(W_AFTER_ANSWER)

    # ================================================================
    #  PART C  —  x² + y² = 100,  y = −3/4 x
    # ================================================================
    def part_c(self):
        header = Text("Pjesa c)", font_size=PART_HEADER_SIZE, color=LABEL_COLOR, weight=BOLD)
        header.to_corner(UL, buff=0.4)
        self.play(Write(header), run_time=T_HEADER_WRITE)

        # Problem
        prob = MathTex(
            r"\begin{cases} x^2 + y^2 = 100 \\ y = -\dfrac{3}{4}\,x \end{cases}",
            font_size=PROBLEM_MATH_SIZE + 4,
        )
        prob.move_to(ORIGIN)
        self.play(FadeIn(prob, shift=UP * 0.3), run_time=T_SHAPE_CREATE)
        self.wait(W_PROBLEM - 1)
        self.play(FadeOut(prob), run_time=T_TRANSITION)
        self.wait(0.3)

        # Graph
        axes = self.create_axes(12, 12, step=4)
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")

        circle = axes.plot_parametric_curve(
            lambda t: np.array([10 * np.cos(t), 10 * np.sin(t), 0]),
            t_range=[0, 2 * PI], color=SHAPE_COLOR, stroke_width=3,
        )
        line = axes.plot(lambda x: -0.75 * x, x_range=[-11, 11], color=AUX_COLOR, stroke_width=2.5)

        dot1 = Dot(axes.c2p(8, -6), color=LABEL_COLOR, radius=0.1)
        dot2 = Dot(axes.c2p(-8, 6), color=HIGHLIGHT_COLOR, radius=0.1)
        lbl1 = MathTex("(8,\\,-6)", font_size=22, color=LABEL_COLOR).next_to(dot1, DR, buff=0.15)
        lbl2 = MathTex("(-8,\\,6)", font_size=22, color=HIGHLIGHT_COLOR).next_to(dot2, UL, buff=0.15)

        graph_group = VGroup(axes, axes_labels, circle, line, dot1, dot2, lbl1, lbl2)

        self.play(Create(axes), FadeIn(axes_labels), run_time=T_SHAPE_CREATE)
        self.play(Create(circle), run_time=T_SHAPE_CREATE * 0.8)
        self.play(Create(line), run_time=T_KEY_EQUATION * 0.8)
        self.play(FadeIn(dot1, scale=1.5), FadeIn(lbl1), FadeIn(dot2, scale=1.5), FadeIn(lbl2), run_time=0.6)
        self.wait(W_AFTER_ROUTINE)

        # Shift left
        self.play(graph_group.animate.shift(LEFT * 3.2), run_time=T_LAYOUT_SHIFT)
        div = make_divider()
        self.play(FadeIn(div), run_time=0.2)

        # Algebra (condensed)
        s1 = Text("Zëvendësojmë y = −3/4 x:", font_size=BODY_SIZE, color=BODY_TEXT_COLOR)
        s1.move_to(CALC_TOP)

        eq1 = MathTex(r"x^2 + \frac{9}{16}x^2 = 100", font_size=CALC_SIZE)
        eq1.next_to(s1, DOWN, buff=0.3)

        eq2 = MathTex(r"\frac{25}{16}x^2 = 100", font_size=CALC_SIZE)
        eq2.next_to(eq1, DOWN, buff=0.25)

        eq3 = MathTex(r"x^2 = 64", font_size=CALC_SIZE, color=LABEL_COLOR)
        eq3.next_to(eq2, DOWN, buff=0.25)

        eq4 = MathTex(r"x = \pm 8", font_size=CALC_SIZE + 2, color=ANSWER_COLOR)
        eq4.next_to(eq3, DOWN, buff=0.3)

        self.play(FadeIn(s1), run_time=T_STEP_TITLE)
        self.play(Write(eq1), run_time=T_KEY_EQUATION)
        self.wait(0.8)
        self.play(Write(eq2), run_time=T_ROUTINE_EQUATION)
        self.wait(0.6)
        self.play(Write(eq3), run_time=T_ROUTINE_EQUATION)
        self.wait(0.6)
        self.play(Write(eq4), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        # Find y & answer
        y_txt = MathTex(
            r"y_1 = -\frac{3}{4}(8) = -6 \qquad y_2 = -\frac{3}{4}(-8) = 6",
            font_size=CALC_SIZE - 2,
        )
        y_txt.next_to(eq4, DOWN, buff=0.4)

        ans = MathTex(
            r"(8,\,-6) \quad \text{dhe} \quad (-8,\,6)",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        ans.next_to(y_txt, DOWN, buff=0.4)
        box = make_answer_box(ans)

        self.play(Write(y_txt), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)
        self.play(Write(ans), run_time=T_KEY_EQUATION)
        self.play(Create(box), run_time=0.5)
        self.wait(W_AFTER_ANSWER)

    # ================================================================
    #  PART D  —  x² + y² = 169,  y = 3x − 3
    #  Quick format
    # ================================================================
    def part_d(self):
        header = Text("Pjesa d)", font_size=PART_HEADER_SIZE, color=LABEL_COLOR, weight=BOLD)
        header.to_corner(UL, buff=0.4)
        self.play(Write(header), run_time=T_HEADER_WRITE)

        # Problem
        prob = MathTex(
            r"\begin{cases} x^2 + y^2 = 169 \\ y = 3x - 3 \end{cases}",
            font_size=PROBLEM_MATH_SIZE + 4,
        )
        prob.move_to(ORIGIN)
        self.play(FadeIn(prob, shift=UP * 0.3), run_time=T_SHAPE_CREATE)
        self.wait(W_PROBLEM - 1)
        self.play(FadeOut(prob), run_time=T_TRANSITION)
        self.wait(0.3)

        # Graph
        axes = self.create_axes(15, 15, step=5)
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")

        circle = axes.plot_parametric_curve(
            lambda t: np.array([13 * np.cos(t), 13 * np.sin(t), 0]),
            t_range=[0, 2 * PI], color=SHAPE_COLOR, stroke_width=3,
        )
        line = axes.plot(lambda x: 3 * x - 3, x_range=[-4.5, 8.5], color=AUX_COLOR, stroke_width=2.5)

        dot1 = Dot(axes.c2p(5, 12), color=LABEL_COLOR, radius=0.1)
        dot2 = Dot(axes.c2p(-3.2, -12.6), color=HIGHLIGHT_COLOR, radius=0.1)
        lbl1 = MathTex("(5,\\,12)", font_size=22, color=LABEL_COLOR).next_to(dot1, UR, buff=0.15)
        lbl2 = MathTex("(-3{,}2;\\,-12{,}6)", font_size=22, color=HIGHLIGHT_COLOR).next_to(dot2, DL, buff=0.15)

        graph_group = VGroup(axes, axes_labels, circle, line, dot1, dot2, lbl1, lbl2)

        self.play(Create(axes), FadeIn(axes_labels), run_time=T_SHAPE_CREATE)
        self.play(Create(circle), Create(line), run_time=T_SHAPE_CREATE)
        self.play(FadeIn(dot1, scale=1.5), FadeIn(lbl1), FadeIn(dot2, scale=1.5), FadeIn(lbl2), run_time=0.6)
        self.wait(W_AFTER_ROUTINE)

        # Shift left
        self.play(graph_group.animate.shift(LEFT * 3.2), run_time=T_LAYOUT_SHIFT)
        div = make_divider()
        self.play(FadeIn(div), run_time=0.2)

        # Quick algebra
        eq1 = MathTex(r"x^2 + (3x-3)^2 = 169", font_size=CALC_SIZE)
        eq1.move_to(CALC_TOP)

        eq2 = MathTex(r"10x^2 - 18x - 160 = 0", font_size=CALC_SIZE)
        eq2.next_to(eq1, DOWN, buff=0.25)

        eq3 = MathTex(r"5x^2 - 9x - 80 = 0", font_size=CALC_SIZE, color=LABEL_COLOR)
        eq3.next_to(eq2, DOWN, buff=0.25)

        eq4 = MathTex(r"x_1 = 5 \qquad x_2 = -3{,}2", font_size=CALC_SIZE + 2, color=ANSWER_COLOR)
        eq4.next_to(eq3, DOWN, buff=0.35)

        self.play(Write(eq1), run_time=T_KEY_EQUATION)
        self.wait(0.6)
        self.play(Write(eq2), run_time=T_ROUTINE_EQUATION)
        self.wait(0.5)
        self.play(Write(eq3), run_time=T_ROUTINE_EQUATION)
        self.wait(0.5)
        self.play(Write(eq4), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        # Answer
        ans = MathTex(
            r"(5,\,12) \quad \text{dhe} \quad (-3{,}2;\;-12{,}6)",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        ans.next_to(eq4, DOWN, buff=0.5)
        box = make_answer_box(ans)

        self.play(Write(ans), run_time=T_KEY_EQUATION)
        self.play(Create(box), run_time=0.5)
        self.wait(W_AFTER_ANSWER)

    # ================================================================
    #  PART E  —  x² + y² = 36,  y = x − 2
    #  Quick format
    # ================================================================
    def part_e(self):
        header = Text("Pjesa e)", font_size=PART_HEADER_SIZE, color=LABEL_COLOR, weight=BOLD)
        header.to_corner(UL, buff=0.4)
        self.play(Write(header), run_time=T_HEADER_WRITE)

        # Problem
        prob = MathTex(
            r"\begin{cases} x^2 + y^2 = 36 \\ y = x - 2 \end{cases}",
            font_size=PROBLEM_MATH_SIZE + 4,
        )
        prob.move_to(ORIGIN)
        self.play(FadeIn(prob, shift=UP * 0.3), run_time=T_SHAPE_CREATE)
        self.wait(W_PROBLEM - 1)
        self.play(FadeOut(prob), run_time=T_TRANSITION)
        self.wait(0.3)

        # Graph
        axes = self.create_axes(8, 8, step=2)
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")

        circle = axes.plot_parametric_curve(
            lambda t: np.array([6 * np.cos(t), 6 * np.sin(t), 0]),
            t_range=[0, 2 * PI], color=SHAPE_COLOR, stroke_width=3,
        )
        line = axes.plot(lambda x: x - 2, x_range=[-5, 7], color=AUX_COLOR, stroke_width=2.5)

        # x1 ≈ 5.125, y1 ≈ 3.125;  x2 ≈ −3.125, y2 ≈ −5.125
        x1, y1 = 5.125, 3.125
        x2, y2 = -3.125, -5.125
        dot1 = Dot(axes.c2p(x1, y1), color=LABEL_COLOR, radius=0.1)
        dot2 = Dot(axes.c2p(x2, y2), color=HIGHLIGHT_COLOR, radius=0.1)
        lbl1 = MathTex("(5{,}1;\\,3{,}1)", font_size=22, color=LABEL_COLOR).next_to(dot1, UR, buff=0.15)
        lbl2 = MathTex("(-3{,}1;\\,-5{,}1)", font_size=22, color=HIGHLIGHT_COLOR).next_to(dot2, DL, buff=0.15)

        graph_group = VGroup(axes, axes_labels, circle, line, dot1, dot2, lbl1, lbl2)

        self.play(Create(axes), FadeIn(axes_labels), run_time=T_SHAPE_CREATE)
        self.play(Create(circle), Create(line), run_time=T_SHAPE_CREATE)
        self.play(FadeIn(dot1, scale=1.5), FadeIn(lbl1), FadeIn(dot2, scale=1.5), FadeIn(lbl2), run_time=0.6)
        self.wait(W_AFTER_ROUTINE)

        # Shift left
        self.play(graph_group.animate.shift(LEFT * 3.2), run_time=T_LAYOUT_SHIFT)
        div = make_divider()
        self.play(FadeIn(div), run_time=0.2)

        # Quick algebra
        eq1 = MathTex(r"x^2 + (x-2)^2 = 36", font_size=CALC_SIZE)
        eq1.move_to(CALC_TOP)

        eq2 = MathTex(r"2x^2 - 4x - 32 = 0", font_size=CALC_SIZE)
        eq2.next_to(eq1, DOWN, buff=0.25)

        eq3 = MathTex(r"x^2 - 2x - 16 = 0", font_size=CALC_SIZE, color=LABEL_COLOR)
        eq3.next_to(eq2, DOWN, buff=0.25)

        eq4 = MathTex(
            r"x = \frac{2 \pm \sqrt{68}}{2} = 1 \pm \sqrt{17}",
            font_size=CALC_SIZE,
        )
        eq4.next_to(eq3, DOWN, buff=0.3)

        eq5 = MathTex(r"x_1 \approx 5{,}12 \qquad x_2 \approx -3{,}12", font_size=CALC_SIZE, color=ANSWER_COLOR)
        eq5.next_to(eq4, DOWN, buff=0.3)

        self.play(Write(eq1), run_time=T_KEY_EQUATION)
        self.wait(0.5)
        self.play(Write(eq2), run_time=T_ROUTINE_EQUATION)
        self.wait(0.4)
        self.play(Write(eq3), run_time=T_ROUTINE_EQUATION)
        self.wait(0.4)
        self.play(Write(eq4), run_time=T_KEY_EQUATION)
        self.wait(0.6)
        self.play(Write(eq5), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        # Answer
        ans = MathTex(
            r"(5{,}12;\;3{,}12) \quad \text{dhe} \quad (-3{,}12;\;-5{,}12)",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        ans.next_to(eq5, DOWN, buff=0.4)
        box = make_answer_box(ans)

        self.play(Write(ans), run_time=T_KEY_EQUATION)
        self.play(Create(box), run_time=0.5)
        self.wait(W_AFTER_ANSWER)

    # ================================================================
    #  PART F  —  x² + y² = 4,  y = 2x + 1
    #  Quick format
    # ================================================================
    def part_f(self):
        header = Text("Pjesa f)", font_size=PART_HEADER_SIZE, color=LABEL_COLOR, weight=BOLD)
        header.to_corner(UL, buff=0.4)
        self.play(Write(header), run_time=T_HEADER_WRITE)

        # Problem
        prob = MathTex(
            r"\begin{cases} x^2 + y^2 = 4 \\ y = 2x + 1 \end{cases}",
            font_size=PROBLEM_MATH_SIZE + 4,
        )
        prob.move_to(ORIGIN)
        self.play(FadeIn(prob, shift=UP * 0.3), run_time=T_SHAPE_CREATE)
        self.wait(W_PROBLEM - 1)
        self.play(FadeOut(prob), run_time=T_TRANSITION)
        self.wait(0.3)

        # Graph
        axes = self.create_axes(4, 4, step=1)
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")

        circle = axes.plot_parametric_curve(
            lambda t: np.array([2 * np.cos(t), 2 * np.sin(t), 0]),
            t_range=[0, 2 * PI], color=SHAPE_COLOR, stroke_width=3,
        )
        line = axes.plot(lambda x: 2 * x + 1, x_range=[-2.5, 1.8], color=AUX_COLOR, stroke_width=2.5)

        # x1 ≈ 0.47, y1 ≈ 1.94;  x2 ≈ −1.27, y2 ≈ −1.54
        x1, y1 = 0.47, 1.94
        x2, y2 = -1.27, -1.54
        dot1 = Dot(axes.c2p(x1, y1), color=LABEL_COLOR, radius=0.1)
        dot2 = Dot(axes.c2p(x2, y2), color=HIGHLIGHT_COLOR, radius=0.1)
        lbl1 = MathTex("(0{,}47;\\,1{,}94)", font_size=22, color=LABEL_COLOR).next_to(dot1, UR, buff=0.15)
        lbl2 = MathTex("(-1{,}27;\\,-1{,}54)", font_size=22, color=HIGHLIGHT_COLOR).next_to(dot2, DL, buff=0.15)

        graph_group = VGroup(axes, axes_labels, circle, line, dot1, dot2, lbl1, lbl2)

        self.play(Create(axes), FadeIn(axes_labels), run_time=T_SHAPE_CREATE)
        self.play(Create(circle), Create(line), run_time=T_SHAPE_CREATE)
        self.play(FadeIn(dot1, scale=1.5), FadeIn(lbl1), FadeIn(dot2, scale=1.5), FadeIn(lbl2), run_time=0.6)
        self.wait(W_AFTER_ROUTINE)

        # Shift left
        self.play(graph_group.animate.shift(LEFT * 3.2), run_time=T_LAYOUT_SHIFT)
        div = make_divider()
        self.play(FadeIn(div), run_time=0.2)

        # Quick algebra
        eq1 = MathTex(r"x^2 + (2x+1)^2 = 4", font_size=CALC_SIZE)
        eq1.move_to(CALC_TOP)

        eq2 = MathTex(r"5x^2 + 4x - 3 = 0", font_size=CALC_SIZE, color=LABEL_COLOR)
        eq2.next_to(eq1, DOWN, buff=0.25)

        eq3 = MathTex(
            r"x = \frac{-4 \pm \sqrt{76}}{10}",
            font_size=CALC_SIZE,
        )
        eq3.next_to(eq2, DOWN, buff=0.3)

        eq4 = MathTex(r"x_1 \approx 0{,}47 \qquad x_2 \approx -1{,}27", font_size=CALC_SIZE, color=ANSWER_COLOR)
        eq4.next_to(eq3, DOWN, buff=0.3)

        self.play(Write(eq1), run_time=T_KEY_EQUATION)
        self.wait(0.5)
        self.play(Write(eq2), run_time=T_ROUTINE_EQUATION)
        self.wait(0.5)
        self.play(Write(eq3), run_time=T_KEY_EQUATION)
        self.wait(0.6)
        self.play(Write(eq4), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        # Answer
        ans = MathTex(
            r"(0{,}47;\;1{,}94) \quad \text{dhe} \quad (-1{,}27;\;-1{,}54)",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        ans.next_to(eq4, DOWN, buff=0.4)
        box = make_answer_box(ans)

        self.play(Write(ans), run_time=T_KEY_EQUATION)
        self.play(Create(box), run_time=0.5)
        self.wait(W_AFTER_ANSWER)

    # ================================================================
    #  FINAL SUMMARY
    # ================================================================
    def final_summary(self):
        title = Text(
            "Përmbledhje e përgjigjeve",
            font_size=PART_HEADER_SIZE + 4,
            color=WHITE,
            weight=BOLD,
        )
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=T_TITLE_WRITE)

        answers = VGroup(
            MathTex(r"\text{a)}\quad (3,\,4) \;\text{dhe}\; (-4,\,-3)", font_size=28),
            MathTex(r"\text{b)}\quad (0,\,-5) \;\text{dhe}\; (4,\,3)", font_size=28),
            MathTex(r"\text{c)}\quad (8,\,-6) \;\text{dhe}\; (-8,\,6)", font_size=28),
            MathTex(r"\text{d)}\quad (5,\,12) \;\text{dhe}\; (-3{,}2;\,-12{,}6)", font_size=28),
            MathTex(r"\text{e)}\quad (5{,}12;\,3{,}12) \;\text{dhe}\; (-3{,}12;\,-5{,}12)", font_size=28),
            MathTex(r"\text{f)}\quad (0{,}47;\,1{,}94) \;\text{dhe}\; (-1{,}27;\,-1{,}54)", font_size=28),
        )
        for ans in answers:
            ans.set_color(ANSWER_COLOR)

        answers.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        answers.next_to(title, DOWN, buff=0.6)

        box = make_answer_box(answers)

        self.play(
            LaggedStart(*[FadeIn(a, shift=RIGHT * 0.3) for a in answers], lag_ratio=0.15),
            run_time=2.0,
        )
        self.play(Create(box), run_time=0.6)

    # ================================================================
    #  HELPERS
    # ================================================================
    def create_axes(self, x_bound, y_bound, step=None):
        """Create Axes scaled for the given bounds."""
        s = step or max(1, x_bound // 4)
        return Axes(
            x_range=[-x_bound, x_bound, s],
            y_range=[-y_bound, y_bound, s],
            x_length=5.5,
            y_length=5.5,
            axis_config={
                "include_tip": True,
                "include_numbers": True,
                "font_size": 18,
                "color": DIVIDER_COLOR,
            },
        )
