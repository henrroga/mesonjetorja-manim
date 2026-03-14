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


class Ushtrimi5(Scene):
    """
    Ushtrimi 5 — Njësia 5.1B
    Matematika 12

    a) Zgjidhni ekuacionin eksponencial.
    b) Gjeni pikën e prerjes së dy grafikëve eksponencialë.
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

        self.wait(W_AFTER_ANSWER)

    # ================================================================
    #  TITLE SCREEN
    # ================================================================
    def title_screen(self):
        title = Text(
            "Ushtrimi 5 — Njësia 5.1B",
            font_size=TITLE_SIZE, color=WHITE, weight=BOLD,
        )
        source = Text(
            "Matematika 12",
            font_size=SUBTITLE_SIZE, color=BODY_TEXT_COLOR,
        )
        source.next_to(title, DOWN, buff=0.4)

        self.play(Write(title), run_time=T_TITLE_WRITE)
        self.play(FadeIn(source, shift=UP * 0.2), run_time=T_SUBTITLE_FADE)
        self.wait(W_AFTER_KEY)
        self.play(FadeOut(title), FadeOut(source))
        self.wait(0.5)

    # ================================================================
    #  PART A — Solve 3^(2x+1) - 5·3^(x-1) + 2 = 0
    # ================================================================
    def part_a(self):
        header = Text("Pjesa a)", font_size=PART_HEADER_SIZE, color=LABEL_COLOR, weight=BOLD)
        header.to_corner(UL, buff=0.4)
        self.play(Write(header), run_time=T_HEADER_WRITE)

        # Problem statement
        prob_title = Text("Zgjidhni ekuacionin:", font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR, weight=BOLD)
        prob_eq = MathTex(
            r"3^{2x+1} - 5 \times 3^{x-1} + 2 = 0",
            font_size=PROBLEM_MATH_SIZE + 4,
        )
        prob_group = VGroup(prob_title, prob_eq).arrange(DOWN, buff=0.4).move_to(ORIGIN)

        self.play(FadeIn(prob_group, shift=UP * 0.3), run_time=T_SHAPE_CREATE)
        self.wait(W_PROBLEM)
        self.play(FadeOut(prob_group), run_time=T_TRANSITION)
        self.wait(0.3)

        # Step 1: Rewrite with substitution t = 3^x
        s1_title = Text(
            "Hapi 1: Rishkruajmë ekuacionin",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR, weight=BOLD,
        )
        s1_title.to_edge(UP, buff=0.5)

        s1_txt = Text(
            "Shëndërrojmë fuqitë duke përdorur\nveti të eksponentëve:",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR, line_spacing=1.4,
        )
        s1_txt.next_to(s1_title, DOWN, buff=0.3)

        s1_eq1 = MathTex(
            r"3 \cdot 3^{2x} - \frac{5}{3} \cdot 3^{x} + 2 = 0",
            font_size=CALC_SIZE,
        )
        s1_eq1.next_to(s1_txt, DOWN, buff=0.35)

        # Multiply by 1/3 approach — but textbook goes directly to quadratic:
        s1_eq2_txt = Text(
            "Shumëzojmë me 1/3 dhe thjeshtojmë:",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        s1_eq2_txt.next_to(s1_eq1, DOWN, buff=0.3)

        s1_eq2 = MathTex(
            r"(3^x)^2 - 5 \cdot (3^x) + 6 = 0",
            font_size=CALC_SIZE, color=LABEL_COLOR,
        )
        s1_eq2.next_to(s1_eq2_txt, DOWN, buff=0.25)

        self.play(FadeIn(s1_title), run_time=T_STEP_TITLE)
        self.play(FadeIn(s1_txt), run_time=T_BODY_FADE)
        self.wait(W_AFTER_ROUTINE)
        self.play(Write(s1_eq1), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_KEY)
        self.play(FadeIn(s1_eq2_txt), run_time=T_BODY_FADE)
        self.play(Write(s1_eq2), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_KEY)

        # Step 2: Substitution t = 3^x
        s2_title = Text(
            "Hapi 2: Zëvendësimi",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR, weight=BOLD,
        )
        s2_title.next_to(s1_eq2, DOWN, buff=0.4)

        s2_sub = MathTex(
            r"\text{Le } t = 3^x \text{, atëherë:}",
            font_size=CALC_SIZE,
        )
        s2_sub.next_to(s2_title, DOWN, buff=0.25)

        s2_eq = MathTex(r"t^2 - 5t + 6 = 0", font_size=CALC_SIZE + 2, color=LABEL_COLOR)
        s2_eq.next_to(s2_sub, DOWN, buff=0.25)

        self.play(FadeIn(s2_title), run_time=T_STEP_TITLE)
        self.play(Write(s2_sub), run_time=T_ROUTINE_EQUATION)
        self.play(Write(s2_eq), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_KEY)

        # Transition
        self.play(
            FadeOut(VGroup(s1_title, s1_txt, s1_eq1, s1_eq2_txt, s1_eq2, s2_title, s2_sub, s2_eq)),
            run_time=T_TRANSITION,
        )
        self.wait(0.3)

        # Step 3: Factor
        s3_title = Text(
            "Hapi 3: Faktorizimi",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR, weight=BOLD,
        )
        s3_title.to_edge(UP, buff=0.5)

        s3_eq1 = MathTex(r"t^2 - 5t + 6 = 0", font_size=CALC_SIZE)
        s3_eq1.next_to(s3_title, DOWN, buff=0.35)

        s3_eq2 = MathTex(r"(t - 2)(t - 3) = 0", font_size=CALC_SIZE, color=LABEL_COLOR)
        s3_eq2.next_to(s3_eq1, DOWN, buff=0.3)

        s3_eq3 = MathTex(r"t_1 = 2 \qquad t_2 = 3", font_size=CALC_SIZE + 2, color=ANSWER_COLOR)
        s3_eq3.next_to(s3_eq2, DOWN, buff=0.35)

        self.play(FadeIn(s3_title), run_time=T_STEP_TITLE)
        self.play(Write(s3_eq1), run_time=T_ROUTINE_EQUATION)
        self.wait(W_AFTER_ROUTINE)
        self.play(Write(s3_eq2), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)
        self.play(Write(s3_eq3), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_KEY)

        # Step 4: Back-substitute
        s4_title = Text(
            "Hapi 4: Kthehemi te 3^x",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR, weight=BOLD,
        )
        s4_title.next_to(s3_eq3, DOWN, buff=0.5)

        self.play(FadeIn(s4_title), run_time=T_STEP_TITLE)
        self.wait(0.5)

        # Transition
        self.play(
            FadeOut(VGroup(s3_title, s3_eq1, s3_eq2, s3_eq3, s4_title)),
            run_time=T_TRANSITION,
        )
        self.wait(0.3)

        # Case 1: 3^x = 2
        case1_title = Text("Rasti 1:", font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR, weight=BOLD)
        case1_title.to_edge(UP, buff=0.5).shift(LEFT * 3)

        c1_eq1 = MathTex(r"3^x = 2", font_size=CALC_SIZE + 2)
        c1_eq1.next_to(case1_title, DOWN, buff=0.3)

        c1_eq2 = MathTex(r"\log(3^x) = \log 2", font_size=CALC_SIZE)
        c1_eq2.next_to(c1_eq1, DOWN, buff=0.25)

        c1_eq3 = MathTex(r"x \cdot \log 3 = \log 2", font_size=CALC_SIZE)
        c1_eq3.next_to(c1_eq2, DOWN, buff=0.25)

        c1_eq4 = MathTex(r"x = \frac{\log 2}{\log 3} \approx 0{,}631", font_size=CALC_SIZE + 2, color=ANSWER_COLOR)
        c1_eq4.next_to(c1_eq3, DOWN, buff=0.3)

        # Case 2: 3^x = 3
        case2_title = Text("Rasti 2:", font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR, weight=BOLD)
        case2_title.to_edge(UP, buff=0.5).shift(RIGHT * 3)

        c2_eq1 = MathTex(r"3^x = 3", font_size=CALC_SIZE + 2)
        c2_eq1.next_to(case2_title, DOWN, buff=0.3)

        c2_eq2 = MathTex(r"3^x = 3^1", font_size=CALC_SIZE)
        c2_eq2.next_to(c2_eq1, DOWN, buff=0.25)

        c2_eq3 = MathTex(r"x = 1", font_size=CALC_SIZE + 2, color=ANSWER_COLOR)
        c2_eq3.next_to(c2_eq2, DOWN, buff=0.3)

        # Animate case 1
        self.play(FadeIn(case1_title), run_time=T_STEP_TITLE)
        self.play(Write(c1_eq1), run_time=T_ROUTINE_EQUATION)
        self.wait(0.6)
        self.play(Write(c1_eq2), run_time=T_ROUTINE_EQUATION)
        self.wait(0.6)
        self.play(Write(c1_eq3), run_time=T_ROUTINE_EQUATION)
        self.wait(0.6)
        self.play(Write(c1_eq4), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        # Animate case 2
        self.play(FadeIn(case2_title), run_time=T_STEP_TITLE)
        self.play(Write(c2_eq1), run_time=T_ROUTINE_EQUATION)
        self.wait(0.6)
        self.play(Write(c2_eq2), run_time=T_ROUTINE_EQUATION)
        self.wait(0.6)
        self.play(Write(c2_eq3), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_KEY)

        # Final answer box
        self.play(
            FadeOut(VGroup(
                case1_title, c1_eq1, c1_eq2, c1_eq3, c1_eq4,
                case2_title, c2_eq1, c2_eq2, c2_eq3,
            )),
            run_time=T_TRANSITION,
        )

        ans_title = Text("Përgjigja:", font_size=STEP_TITLE_SIZE + 2, color=STEP_TITLE_COLOR, weight=BOLD)
        ans1 = MathTex(r"x_1 = \frac{\log 2}{\log 3} \approx 0{,}631", font_size=ANSWER_SIZE, color=ANSWER_COLOR)
        ans2 = MathTex(r"x_2 = 1", font_size=ANSWER_SIZE, color=ANSWER_COLOR)

        ans_group = VGroup(ans_title, ans1, ans2).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        box = make_answer_box(VGroup(ans1, ans2))

        self.play(FadeIn(ans_group), run_time=T_SHAPE_CREATE)
        self.play(Create(box), run_time=0.5)
        self.wait(W_AFTER_ANSWER)

    # ================================================================
    #  PART B — Find intersection of y = 3^(2x-1) + 2 and y = 5·3^(x-1)
    # ================================================================
    def part_b(self):
        header = Text("Pjesa b)", font_size=PART_HEADER_SIZE, color=LABEL_COLOR, weight=BOLD)
        header.to_corner(UL, buff=0.4)
        self.play(Write(header), run_time=T_HEADER_WRITE)

        # Problem statement
        prob_title = Text(
            "Gjeni pikën e prerjes së grafikëve:",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR, weight=BOLD,
        )
        prob_eq1 = MathTex(r"y = 3^{2x-1} + 2", font_size=PROBLEM_MATH_SIZE, color=SHAPE_COLOR)
        prob_eq2 = MathTex(r"y = 5 \times 3^{x-1}", font_size=PROBLEM_MATH_SIZE, color=AUX_COLOR)

        prob_group = VGroup(prob_title, prob_eq1, prob_eq2).arrange(DOWN, buff=0.4).move_to(ORIGIN)

        self.play(FadeIn(prob_group, shift=UP * 0.3), run_time=T_SHAPE_CREATE)
        self.wait(W_PROBLEM)
        self.play(FadeOut(prob_group), run_time=T_TRANSITION)
        self.wait(0.3)

        # Graph first
        axes = Axes(
            x_range=[-2, 3, 1],
            y_range=[-1, 20, 5],
            x_length=6, y_length=5.5,
            axis_config={
                "include_tip": True,
                "include_numbers": True,
                "font_size": 18,
                "color": DIVIDER_COLOR,
            },
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")

        # y = 3^(2x-1) + 2
        func1 = axes.plot(
            lambda x: 3 ** (2 * x - 1) + 2,
            x_range=[-1.5, 1.65],
            color=SHAPE_COLOR, stroke_width=2.5,
        )
        func1_label = MathTex(r"y=3^{2x-1}+2", font_size=20, color=SHAPE_COLOR)
        func1_label.next_to(func1.point_from_proportion(0.85), UR, buff=0.1)

        # y = 5 · 3^(x-1)
        func2 = axes.plot(
            lambda x: 5 * 3 ** (x - 1),
            x_range=[-1.5, 2.2],
            color=AUX_COLOR, stroke_width=2.5,
        )
        func2_label = MathTex(r"y=5 \cdot 3^{x-1}", font_size=20, color=AUX_COLOR)
        func2_label.next_to(func2.point_from_proportion(0.8), RIGHT, buff=0.1)

        # Intersection points
        x1_val = 1.0
        y1_val = 5.0
        x2_val = np.log(2) / np.log(3)  # ≈ 0.631
        y2_val = 10 / 3  # ≈ 3.333

        dot1 = Dot(axes.c2p(x1_val, y1_val), color=LABEL_COLOR, radius=0.1)
        dot2 = Dot(axes.c2p(x2_val, y2_val), color=HIGHLIGHT_COLOR, radius=0.1)
        lbl1 = MathTex("(1,\\,5)", font_size=22, color=LABEL_COLOR).next_to(dot1, UR, buff=0.15)
        lbl2 = MathTex(
            r"\left(0{,}63;\;\tfrac{10}{3}\right)",
            font_size=22, color=HIGHLIGHT_COLOR,
        ).next_to(dot2, DL, buff=0.15)

        graph_group = VGroup(axes, axes_labels, func1, func1_label, func2, func2_label, dot1, dot2, lbl1, lbl2)

        self.play(Create(axes), FadeIn(axes_labels), run_time=T_SHAPE_CREATE)
        self.play(Create(func1), FadeIn(func1_label), run_time=T_SHAPE_CREATE)
        self.play(Create(func2), FadeIn(func2_label), run_time=T_SHAPE_CREATE)
        self.wait(W_AFTER_ROUTINE)
        self.play(FadeIn(dot1, scale=1.5), FadeIn(lbl1), run_time=T_DOT_FADE + 0.2)
        self.play(FadeIn(dot2, scale=1.5), FadeIn(lbl2), run_time=T_DOT_FADE + 0.2)
        self.wait(W_AFTER_KEY)

        # Shift graph left
        self.play(graph_group.animate.shift(LEFT * 3.2), run_time=T_LAYOUT_SHIFT)
        div = make_divider()
        self.play(FadeIn(div), run_time=0.2)

        # Algebra: set equal
        s1 = Text(
            "Barazojmë dy grafikët:",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        s1.move_to(CALC_TOP)

        eq1 = MathTex(
            r"3^{2x-1} + 2 = 5 \times 3^{x-1}",
            font_size=CALC_SIZE,
        )
        eq1.next_to(s1, DOWN, buff=0.3)

        eq2_txt = Text(
            "Ky është i njëjti ekuacion\nsi në pikën a)!",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR, line_spacing=1.4,
        )
        eq2_txt.next_to(eq1, DOWN, buff=0.35)

        eq3 = MathTex(
            r"x_1 = 1 \qquad x_2 = \frac{\log 2}{\log 3}",
            font_size=CALC_SIZE, color=LABEL_COLOR,
        )
        eq3.next_to(eq2_txt, DOWN, buff=0.3)

        self.play(FadeIn(s1), run_time=T_STEP_TITLE)
        self.play(Write(eq1), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)
        self.play(FadeIn(eq2_txt), run_time=T_BODY_FADE)
        self.wait(W_AFTER_ROUTINE)
        self.play(Write(eq3), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_KEY)

        # Transition
        self.play(FadeOut(VGroup(s1, eq1, eq2_txt, eq3)), run_time=T_TRANSITION)
        self.wait(0.3)

        # Find y values
        y_title = Text("Gjejmë y:", font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR, weight=BOLD)
        y_title.move_to(CALC_TOP)

        y1_txt = Text("Kur x = 1:", font_size=BODY_SIZE, color=BODY_TEXT_COLOR)
        y1_txt.next_to(y_title, DOWN, buff=0.3, aligned_edge=LEFT)

        y1_eq = MathTex(
            r"y = 5 \times 3^{1-1} = 5 \times 1 = 5",
            font_size=CALC_SIZE,
        )
        y1_eq.next_to(y1_txt, DOWN, buff=0.2)

        y2_txt = MathTex(
            r"\text{Kur } x = \tfrac{\log 2}{\log 3}\text{:}",
            font_size=BODY_SIZE + 2,
            color=BODY_TEXT_COLOR,
        )
        y2_txt.next_to(y1_eq, DOWN, buff=0.35, aligned_edge=LEFT)

        y2_eq = MathTex(
            r"y = 5 \times \frac{2}{3} = \frac{10}{3}",
            font_size=CALC_SIZE,
        )
        y2_eq.next_to(y2_txt, DOWN, buff=0.2)

        self.play(FadeIn(y_title), run_time=T_STEP_TITLE)
        self.play(FadeIn(y1_txt), run_time=T_BODY_FADE)
        self.play(Write(y1_eq), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)
        self.play(FadeIn(y2_txt), run_time=T_BODY_FADE)
        self.play(Write(y2_eq), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_KEY)

        # Final answer
        ans = VGroup(
            MathTex(r"(1,\;5)", font_size=ANSWER_SIZE, color=ANSWER_COLOR),
            MathTex(
                r"\left(\frac{\log 2}{\log 3},\;\frac{10}{3}\right)",
                font_size=ANSWER_SIZE, color=ANSWER_COLOR,
            ),
        ).arrange(RIGHT, buff=1.0)
        ans.next_to(y2_eq, DOWN, buff=0.5)
        box = make_answer_box(ans)

        self.play(Write(ans), run_time=T_KEY_EQUATION)
        self.play(Create(box), run_time=0.5)
        self.wait(W_AFTER_ANSWER)
