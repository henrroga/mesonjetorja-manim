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


class Ushtrimi3(Scene):
    """
    Ushtrimi 3 — Njësia 6.5A
    Matematika 10-11: Pjesa II

    Skiconi grafikët e rrathëve dhe emërtoni pikëprerjet me boshtet.
    """

    def construct(self):
        apply_style(self)

        self.title_screen()

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

        self.final_summary()
        self.wait(W_AFTER_ANSWER)

    # ================================================================
    #  TITLE SCREEN
    # ================================================================
    def title_screen(self):
        title = Text(
            "Ushtrimi 3 — Njësia 6.5A",
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
    #  PART A — x² + y² = 49,  r = 7
    #  Full detailed walkthrough
    # ================================================================
    def part_a(self):
        header = Text("Pjesa a)", font_size=PART_HEADER_SIZE, color=LABEL_COLOR, weight=BOLD)
        header.to_corner(UL, buff=0.4)
        self.play(Write(header), run_time=T_HEADER_WRITE)

        # Problem statement
        prob = MathTex(r"x^2 + y^2 = 49", font_size=PROBLEM_MATH_SIZE + 4)
        prob.move_to(ORIGIN)
        self.play(FadeIn(prob, shift=UP * 0.3), run_time=T_SHAPE_CREATE)
        self.wait(W_PROBLEM - 1)
        self.play(FadeOut(prob), run_time=T_TRANSITION)
        self.wait(0.3)

        # Explanation: identify as circle
        exp_title = Text("Njohim ekuacionin:", font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR, weight=BOLD)
        exp_txt = Text(
            "Kjo është forma e rrethit me\nqendër në origjinë (0, 0).",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR, line_spacing=1.4,
        )
        exp_eq = MathTex(r"x^2 + y^2 = r^2", font_size=CALC_SIZE)
        exp_r = MathTex(r"r^2 = 49 \implies r = 7", font_size=CALC_SIZE, color=ANSWER_COLOR)

        exp_group = VGroup(exp_title, exp_txt, exp_eq, exp_r).arrange(DOWN, buff=0.35).move_to(ORIGIN)

        self.play(FadeIn(exp_group, shift=UP * 0.2), run_time=T_SHAPE_CREATE)
        self.wait(W_AFTER_KEY)
        self.play(FadeOut(exp_group), run_time=T_TRANSITION)
        self.wait(0.3)

        # Find axis intercepts (centered)
        int_title = Text("Pikëprerjet me boshtet:", font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR, weight=BOLD)

        int_x_title = Text("Me boshtin x (y = 0):", font_size=BODY_SIZE, color=BODY_TEXT_COLOR)
        int_x_eq = MathTex(r"x^2 = 49 \implies x = \pm 7", font_size=CALC_SIZE)
        int_x_pts = MathTex(r"(-7,\,0) \quad \text{dhe} \quad (7,\,0)", font_size=CALC_SIZE, color=LABEL_COLOR)

        int_y_title = Text("Me boshtin y (x = 0):", font_size=BODY_SIZE, color=BODY_TEXT_COLOR)
        int_y_eq = MathTex(r"y^2 = 49 \implies y = \pm 7", font_size=CALC_SIZE)
        int_y_pts = MathTex(r"(0,\,-7) \quad \text{dhe} \quad (0,\,7)", font_size=CALC_SIZE, color=LABEL_COLOR)

        int_group = VGroup(
            int_title,
            VGroup(int_x_title, int_x_eq, int_x_pts).arrange(DOWN, buff=0.2, aligned_edge=LEFT),
            VGroup(int_y_title, int_y_eq, int_y_pts).arrange(DOWN, buff=0.2, aligned_edge=LEFT),
        ).arrange(DOWN, buff=0.4).move_to(ORIGIN)

        self.play(FadeIn(int_title), run_time=T_STEP_TITLE)
        self.play(FadeIn(int_x_title), run_time=T_BODY_FADE)
        self.play(Write(int_x_eq), run_time=T_ROUTINE_EQUATION)
        self.play(Write(int_x_pts), run_time=T_ROUTINE_EQUATION)
        self.wait(W_AFTER_ROUTINE)
        self.play(FadeIn(int_y_title), run_time=T_BODY_FADE)
        self.play(Write(int_y_eq), run_time=T_ROUTINE_EQUATION)
        self.play(Write(int_y_pts), run_time=T_ROUTINE_EQUATION)
        self.wait(W_AFTER_KEY)
        self.play(FadeOut(int_group), run_time=T_TRANSITION)
        self.wait(0.3)

        # Graph
        self.show_circle_graph(
            r_val=7, r_sq=49,
            eq_str=r"x^2 + y^2 = 49",
            r_str=r"r = 7",
            intercepts_x=[(-7, 0), (7, 0)],
            intercepts_y=[(0, -7), (0, 7)],
            x_labels=[r"(-7,0)", r"(7,0)"],
            y_labels=[r"(0,-7)", r"(0,7)"],
        )

    # ================================================================
    #  PART B — x² + y² = 64,  r = 8
    # ================================================================
    def part_b(self):
        header = Text("Pjesa b)", font_size=PART_HEADER_SIZE, color=LABEL_COLOR, weight=BOLD)
        header.to_corner(UL, buff=0.4)
        self.play(Write(header), run_time=T_HEADER_WRITE)

        # Problem + quick identify
        prob = MathTex(r"x^2 + y^2 = 64", font_size=PROBLEM_MATH_SIZE + 4)
        r_eq = MathTex(r"r^2 = 64 \implies r = 8", font_size=CALC_SIZE, color=ANSWER_COLOR)
        VGroup(prob, r_eq).arrange(DOWN, buff=0.4).move_to(ORIGIN)

        self.play(FadeIn(prob), run_time=T_SHAPE_CREATE)
        self.wait(0.8)
        self.play(Write(r_eq), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)
        self.play(FadeOut(prob), FadeOut(r_eq), run_time=T_TRANSITION)
        self.wait(0.3)

        self.show_circle_graph(
            r_val=8, r_sq=64,
            eq_str=r"x^2 + y^2 = 64",
            r_str=r"r = 8",
            intercepts_x=[(-8, 0), (8, 0)],
            intercepts_y=[(0, -8), (0, 8)],
            x_labels=[r"(-8,0)", r"(8,0)"],
            y_labels=[r"(0,-8)", r"(0,8)"],
        )

    # ================================================================
    #  PART C — x² + y² = 2,  r = √2
    # ================================================================
    def part_c(self):
        header = Text("Pjesa c)", font_size=PART_HEADER_SIZE, color=LABEL_COLOR, weight=BOLD)
        header.to_corner(UL, buff=0.4)
        self.play(Write(header), run_time=T_HEADER_WRITE)

        prob = MathTex(r"x^2 + y^2 = 2", font_size=PROBLEM_MATH_SIZE + 4)
        r_eq = MathTex(r"r^2 = 2 \implies r = \sqrt{2}", font_size=CALC_SIZE, color=ANSWER_COLOR)
        VGroup(prob, r_eq).arrange(DOWN, buff=0.4).move_to(ORIGIN)

        self.play(FadeIn(prob), run_time=T_SHAPE_CREATE)
        self.wait(0.8)
        self.play(Write(r_eq), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)
        self.play(FadeOut(prob), FadeOut(r_eq), run_time=T_TRANSITION)
        self.wait(0.3)

        sqrt2 = np.sqrt(2)
        self.show_circle_graph(
            r_val=sqrt2, r_sq=2,
            eq_str=r"x^2 + y^2 = 2",
            r_str=r"r = \sqrt{2}",
            intercepts_x=[(-sqrt2, 0), (sqrt2, 0)],
            intercepts_y=[(0, -sqrt2), (0, sqrt2)],
            x_labels=[r"(-\sqrt{2},0)", r"(\sqrt{2},0)"],
            y_labels=[r"(0,-\sqrt{2})", r"(0,\sqrt{2})"],
            axis_bound=3,
        )

    # ================================================================
    #  PART D — x² + y² = 20,  r = 2√5
    # ================================================================
    def part_d(self):
        header = Text("Pjesa d)", font_size=PART_HEADER_SIZE, color=LABEL_COLOR, weight=BOLD)
        header.to_corner(UL, buff=0.4)
        self.play(Write(header), run_time=T_HEADER_WRITE)

        prob = MathTex(r"x^2 + y^2 = 20", font_size=PROBLEM_MATH_SIZE + 4)
        r_eq = MathTex(r"r^2 = 20 \implies r = 2\sqrt{5}", font_size=CALC_SIZE, color=ANSWER_COLOR)
        VGroup(prob, r_eq).arrange(DOWN, buff=0.4).move_to(ORIGIN)

        self.play(FadeIn(prob), run_time=T_SHAPE_CREATE)
        self.wait(0.8)
        self.play(Write(r_eq), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)
        self.play(FadeOut(prob), FadeOut(r_eq), run_time=T_TRANSITION)
        self.wait(0.3)

        r = 2 * np.sqrt(5)
        self.show_circle_graph(
            r_val=r, r_sq=20,
            eq_str=r"x^2 + y^2 = 20",
            r_str=r"r = 2\sqrt{5}",
            intercepts_x=[(-r, 0), (r, 0)],
            intercepts_y=[(0, -r), (0, r)],
            x_labels=[r"(-2\sqrt{5},0)", r"(2\sqrt{5},0)"],
            y_labels=[r"(0,-2\sqrt{5})", r"(0,2\sqrt{5})"],
            axis_bound=6,
        )

    # ================================================================
    #  PART E — y² = 4 − x²  →  x² + y² = 4,  r = 2
    # ================================================================
    def part_e(self):
        header = Text("Pjesa e)", font_size=PART_HEADER_SIZE, color=LABEL_COLOR, weight=BOLD)
        header.to_corner(UL, buff=0.4)
        self.play(Write(header), run_time=T_HEADER_WRITE)

        # Show original form, then rewrite
        prob = MathTex(r"y^2 = 4 - x^2", font_size=PROBLEM_MATH_SIZE + 4)
        rewrite = MathTex(r"\Rightarrow\; x^2 + y^2 = 4", font_size=CALC_SIZE, color=STEP_TITLE_COLOR)
        r_eq = MathTex(r"r = 2", font_size=CALC_SIZE, color=ANSWER_COLOR)
        VGroup(prob, rewrite, r_eq).arrange(DOWN, buff=0.4).move_to(ORIGIN)

        self.play(FadeIn(prob), run_time=T_SHAPE_CREATE)
        self.wait(0.8)
        self.play(Write(rewrite), run_time=T_KEY_EQUATION)
        self.wait(0.6)
        self.play(Write(r_eq), run_time=T_ROUTINE_EQUATION)
        self.wait(W_AFTER_ROUTINE)
        self.play(FadeOut(prob), FadeOut(rewrite), FadeOut(r_eq), run_time=T_TRANSITION)
        self.wait(0.3)

        self.show_circle_graph(
            r_val=2, r_sq=4,
            eq_str=r"x^2 + y^2 = 4",
            r_str=r"r = 2",
            intercepts_x=[(-2, 0), (2, 0)],
            intercepts_y=[(0, -2), (0, 2)],
            x_labels=[r"(-2,0)", r"(2,0)"],
            y_labels=[r"(0,-2)", r"(0,2)"],
            axis_bound=4,
        )

    # ================================================================
    #  PART F — y² = 16 − x²  →  x² + y² = 16,  r = 4
    # ================================================================
    def part_f(self):
        header = Text("Pjesa f)", font_size=PART_HEADER_SIZE, color=LABEL_COLOR, weight=BOLD)
        header.to_corner(UL, buff=0.4)
        self.play(Write(header), run_time=T_HEADER_WRITE)

        prob = MathTex(r"y^2 = 16 - x^2", font_size=PROBLEM_MATH_SIZE + 4)
        rewrite = MathTex(r"\Rightarrow\; x^2 + y^2 = 16", font_size=CALC_SIZE, color=STEP_TITLE_COLOR)
        r_eq = MathTex(r"r = 4", font_size=CALC_SIZE, color=ANSWER_COLOR)
        VGroup(prob, rewrite, r_eq).arrange(DOWN, buff=0.4).move_to(ORIGIN)

        self.play(FadeIn(prob), run_time=T_SHAPE_CREATE)
        self.wait(0.8)
        self.play(Write(rewrite), run_time=T_KEY_EQUATION)
        self.wait(0.6)
        self.play(Write(r_eq), run_time=T_ROUTINE_EQUATION)
        self.wait(W_AFTER_ROUTINE)
        self.play(FadeOut(prob), FadeOut(rewrite), FadeOut(r_eq), run_time=T_TRANSITION)
        self.wait(0.3)

        self.show_circle_graph(
            r_val=4, r_sq=16,
            eq_str=r"x^2 + y^2 = 16",
            r_str=r"r = 4",
            intercepts_x=[(-4, 0), (4, 0)],
            intercepts_y=[(0, -4), (0, 4)],
            x_labels=[r"(-4,0)", r"(4,0)"],
            y_labels=[r"(0,-4)", r"(0,4)"],
            axis_bound=6,
        )

    # ================================================================
    #  FINAL SUMMARY
    # ================================================================
    def final_summary(self):
        title = Text(
            "Përmbledhje",
            font_size=PART_HEADER_SIZE + 4, color=WHITE, weight=BOLD,
        )
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=T_TITLE_WRITE)

        rows = VGroup(
            MathTex(r"\text{a)}\; x^2+y^2=49 \quad r=7 \quad (\pm7,0),\;(0,\pm7)", font_size=26),
            MathTex(r"\text{b)}\; x^2+y^2=64 \quad r=8 \quad (\pm8,0),\;(0,\pm8)", font_size=26),
            MathTex(r"\text{c)}\; x^2+y^2=2 \quad r=\sqrt{2} \quad (\pm\sqrt{2},0),\;(0,\pm\sqrt{2})", font_size=26),
            MathTex(r"\text{d)}\; x^2+y^2=20 \quad r=2\sqrt{5} \quad (\pm2\sqrt{5},0),\;(0,\pm2\sqrt{5})", font_size=26),
            MathTex(r"\text{e)}\; x^2+y^2=4 \quad r=2 \quad (\pm2,0),\;(0,\pm2)", font_size=26),
            MathTex(r"\text{f)}\; x^2+y^2=16 \quad r=4 \quad (\pm4,0),\;(0,\pm4)", font_size=26),
        )
        for row in rows:
            row.set_color(ANSWER_COLOR)

        rows.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        rows.next_to(title, DOWN, buff=0.6)

        box = make_answer_box(rows)

        self.play(
            LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3) for r in rows], lag_ratio=0.15),
            run_time=2.0,
        )
        self.play(Create(box), run_time=0.6)

    # ================================================================
    #  REUSABLE: Show circle graph with labeled intercepts
    # ================================================================
    def show_circle_graph(
        self, r_val, r_sq, eq_str, r_str,
        intercepts_x, intercepts_y,
        x_labels, y_labels,
        axis_bound=None,
    ):
        """Draw a circle on axes with labeled axis intercepts."""
        bound = axis_bound or int(r_val + 2)
        step = max(1, bound // 4)

        axes = Axes(
            x_range=[-bound, bound, step],
            y_range=[-bound, bound, step],
            x_length=6, y_length=6,
            axis_config={
                "include_tip": True,
                "include_numbers": True,
                "font_size": 18,
                "color": DIVIDER_COLOR,
            },
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")

        # Circle
        circle = axes.plot_parametric_curve(
            lambda t: np.array([r_val * np.cos(t), r_val * np.sin(t), 0]),
            t_range=[0, 2 * PI],
            color=SHAPE_COLOR, stroke_width=3,
        )

        # Equation label
        eq_label = MathTex(eq_str, font_size=24, color=SHAPE_COLOR)
        eq_label.to_corner(UR, buff=0.5)

        # Radius label
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

        # X-axis intercepts
        for i, (pt, lbl_str) in enumerate(zip(intercepts_x, x_labels)):
            dot = Dot(axes.c2p(pt[0], pt[1]), color=LABEL_COLOR, radius=0.08)
            lbl = MathTex(lbl_str, font_size=20, color=LABEL_COLOR)
            if i == 0:  # left point
                lbl.next_to(dot, DL, buff=0.12)
            else:  # right point
                lbl.next_to(dot, DR, buff=0.12)
            dots_and_labels.add(dot, lbl)

        # Y-axis intercepts
        for i, (pt, lbl_str) in enumerate(zip(intercepts_y, y_labels)):
            dot = Dot(axes.c2p(pt[0], pt[1]), color=HIGHLIGHT_COLOR, radius=0.08)
            lbl = MathTex(lbl_str, font_size=20, color=HIGHLIGHT_COLOR)
            if i == 0:  # bottom point
                lbl.next_to(dot, DL, buff=0.12)
            else:  # top point
                lbl.next_to(dot, UL, buff=0.12)
            dots_and_labels.add(dot, lbl)

        # Animate
        self.play(Create(axes), FadeIn(axes_labels), run_time=T_SHAPE_CREATE)
        self.play(Create(circle), run_time=T_SHAPE_CREATE)
        self.play(FadeIn(eq_label), FadeIn(r_label), run_time=T_BODY_FADE)
        self.play(Create(r_line), FadeIn(r_mid_label), run_time=T_ROUTINE_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        # Show intercept points
        self.play(
            LaggedStart(
                *[FadeIn(obj, scale=1.3) for obj in dots_and_labels],
                lag_ratio=0.1,
            ),
            run_time=1.5,
        )
        self.wait(W_AFTER_ANSWER)
