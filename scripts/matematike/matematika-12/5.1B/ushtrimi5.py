import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from manim import *
import numpy as np
from components import ExerciseScene
from style_guide import (
    make_answer_box, fade_all,
    STEP_TITLE_COLOR, BODY_TEXT_COLOR, LABEL_COLOR,
    ANSWER_COLOR, SHAPE_COLOR, AUX_COLOR, HIGHLIGHT_COLOR, DIVIDER_COLOR,
    STEP_TITLE_SIZE, BODY_SIZE, PROBLEM_MATH_SIZE, CALC_SIZE, ANSWER_SIZE,
    T_STEP_TITLE, T_BODY_FADE, T_KEY_EQUATION, T_ROUTINE_EQUATION,
    T_SHAPE_CREATE, T_DOT_FADE, T_LAYOUT_SHIFT, T_TRANSITION,
    W_AFTER_KEY, W_AFTER_ROUTINE, W_AFTER_ANSWER, W_PROBLEM,
    CALC_TOP,
)


class Ushtrimi5(ExerciseScene):
    """
    Ushtrimi 5 — Njësia 5.1B
    Matematika 12

    a) Zgjidhni ekuacionin eksponencial.
    b) Gjeni pikën e prerjes së dy grafikëve eksponencialë.
    """

    exercise_number = 5
    unit = "5.1B"
    textbook = "Matematika 12"
    parts = ["a", "b"]

    # ================================================================
    #  PART A — Solve 3^(2x+1) - 5·3^(x-1) + 2 = 0
    # ================================================================
    def part_a(self):
        self.show_part_header("a")

        # Problem statement
        prob_title = Text("Zgjidhni ekuacionin:", font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR, weight=BOLD)
        prob_eq = MathTex(r"3^{2x+1} - 5 \times 3^{x-1} + 2 = 0", font_size=PROBLEM_MATH_SIZE + 4)
        self.show_problem(prob_title, prob_eq)

        # Step 1: Rewrite with substitution t = 3^x
        s1_title = self.show_step_title("Hapi 1: Rishkruajmë ekuacionin", position=UP * 3)

        s1_txt = Text(
            "Shëndërrojmë fuqitë duke përdorur\nveti të eksponentëve:",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR, line_spacing=1.4,
        )
        s1_txt.next_to(s1_title, DOWN, buff=0.3)
        self.play(FadeIn(s1_txt), run_time=T_BODY_FADE)
        self.wait(W_AFTER_ROUTINE)

        s1_eq1 = self.show_equation(
            r"3 \cdot 3^{2x} - \frac{5}{3} \cdot 3^{x} + 2 = 0",
            reference=s1_txt, buff=0.35, key=True,
        )

        s1_eq2_txt = Text("Shumëzojmë me 1/3 dhe thjeshtojmë:", font_size=BODY_SIZE, color=BODY_TEXT_COLOR)
        s1_eq2_txt.next_to(s1_eq1, DOWN, buff=0.3)
        self.play(FadeIn(s1_eq2_txt), run_time=T_BODY_FADE)

        s1_eq2 = self.show_equation(
            r"(3^x)^2 - 5 \cdot (3^x) + 6 = 0",
            reference=s1_eq2_txt, color=LABEL_COLOR, key=True,
        )

        # Step 2: Substitution t = 3^x
        s2_title = self.show_step_title("Hapi 2: Zëvendësimi", reference=s1_eq2)

        s2_sub = self.show_equation(r"\text{Le } t = 3^x \text{, atëherë:}", reference=s2_title)
        s2_eq = self.show_equation(r"t^2 - 5t + 6 = 0", reference=s2_sub, color=LABEL_COLOR, key=True)

        # Transition
        self.play(
            FadeOut(VGroup(s1_title, s1_txt, s1_eq1, s1_eq2_txt, s1_eq2, s2_title, s2_sub, s2_eq)),
            run_time=T_TRANSITION,
        )
        self.wait(0.3)

        # Step 3: Factor
        s3_title = self.show_step_title("Hapi 3: Faktorizimi", position=UP * 3)

        eqs3 = self.show_equation_chain([
            r"t^2 - 5t + 6 = 0",
            {"tex": r"(t - 2)(t - 3) = 0", "color": LABEL_COLOR, "key": True},
            {"tex": r"t_1 = 2 \qquad t_2 = 3", "color": ANSWER_COLOR, "font_size": CALC_SIZE + 2, "key": True},
        ], start_reference=s3_title)

        # Step 4: Back-substitute
        s4_title = self.show_step_title("Hapi 4: Kthehemi te 3^x", reference=eqs3[-1], buff=0.5)

        # Transition
        self.play(FadeOut(VGroup(s3_title, *eqs3, s4_title)), run_time=T_TRANSITION)
        self.wait(0.3)

        # Case 1: 3^x = 2
        case1_title = Text("Rasti 1:", font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR, weight=BOLD)
        case1_title.to_edge(UP, buff=0.5).shift(LEFT * 3)

        c1_eqs = [
            MathTex(r"3^x = 2", font_size=CALC_SIZE + 2),
            MathTex(r"\log(3^x) = \log 2", font_size=CALC_SIZE),
            MathTex(r"x \cdot \log 3 = \log 2", font_size=CALC_SIZE),
            MathTex(r"x = \frac{\log 2}{\log 3} \approx 0{,}631", font_size=CALC_SIZE + 2, color=ANSWER_COLOR),
        ]
        for i, eq in enumerate(c1_eqs):
            if i == 0:
                eq.next_to(case1_title, DOWN, buff=0.3)
            else:
                eq.next_to(c1_eqs[i - 1], DOWN, buff=0.25)

        # Case 2: 3^x = 3
        case2_title = Text("Rasti 2:", font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR, weight=BOLD)
        case2_title.to_edge(UP, buff=0.5).shift(RIGHT * 3)

        c2_eqs = [
            MathTex(r"3^x = 3", font_size=CALC_SIZE + 2),
            MathTex(r"3^x = 3^1", font_size=CALC_SIZE),
            MathTex(r"x = 1", font_size=CALC_SIZE + 2, color=ANSWER_COLOR),
        ]
        for i, eq in enumerate(c2_eqs):
            if i == 0:
                eq.next_to(case2_title, DOWN, buff=0.3)
            else:
                eq.next_to(c2_eqs[i - 1], DOWN, buff=0.25)

        # Animate case 1
        self.play(FadeIn(case1_title), run_time=T_STEP_TITLE)
        for eq in c1_eqs:
            rt = T_KEY_EQUATION if eq == c1_eqs[-1] else T_ROUTINE_EQUATION
            self.play(Write(eq), run_time=rt)
            self.wait(0.6)
        self.wait(W_AFTER_ROUTINE)

        # Animate case 2
        self.play(FadeIn(case2_title), run_time=T_STEP_TITLE)
        for eq in c2_eqs:
            rt = T_KEY_EQUATION if eq == c2_eqs[-1] else T_ROUTINE_EQUATION
            self.play(Write(eq), run_time=rt)
            self.wait(0.6)
        self.wait(W_AFTER_KEY)

        # Final answer box
        self.play(
            FadeOut(VGroup(case1_title, *c1_eqs, case2_title, *c2_eqs)),
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
        self.show_part_header("b")

        # Problem statement
        prob_title = Text(
            "Gjeni pikën e prerjes së grafikëve:",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR, weight=BOLD,
        )
        prob_eq1 = MathTex(r"y = 3^{2x-1} + 2", font_size=PROBLEM_MATH_SIZE, color=SHAPE_COLOR)
        prob_eq2 = MathTex(r"y = 5 \times 3^{x-1}", font_size=PROBLEM_MATH_SIZE, color=AUX_COLOR)
        self.show_problem(prob_title, prob_eq1, prob_eq2)

        # Graph
        axes = Axes(
            x_range=[-2, 3, 1], y_range=[-1, 20, 5],
            x_length=6, y_length=5.5,
            axis_config={"include_tip": True, "include_numbers": True,
                         "font_size": 18, "color": DIVIDER_COLOR},
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")

        func1 = axes.plot(lambda x: 3 ** (2 * x - 1) + 2, x_range=[-1.5, 1.65],
                          color=SHAPE_COLOR, stroke_width=2.5)
        func1_label = MathTex(r"y=3^{2x-1}+2", font_size=20, color=SHAPE_COLOR)
        func1_label.next_to(func1.point_from_proportion(0.85), UR, buff=0.1)

        func2 = axes.plot(lambda x: 5 * 3 ** (x - 1), x_range=[-1.5, 2.2],
                          color=AUX_COLOR, stroke_width=2.5)
        func2_label = MathTex(r"y=5 \cdot 3^{x-1}", font_size=20, color=AUX_COLOR)
        func2_label.next_to(func2.point_from_proportion(0.8), RIGHT, buff=0.1)

        # Intersection points
        x1_val, y1_val = 1.0, 5.0
        x2_val = np.log(2) / np.log(3)
        y2_val = 10 / 3

        dot1, lbl1 = self.mark_point(axes, x1_val, y1_val, "(1,\\,5)",
                                      color=LABEL_COLOR, direction=UR)
        dot2, lbl2 = self.mark_point(axes, x2_val, y2_val,
                                      r"\left(0{,}63;\;\tfrac{10}{3}\right)",
                                      color=HIGHLIGHT_COLOR, direction=DL)

        graph_group = VGroup(axes, axes_labels, func1, func1_label,
                             func2, func2_label, dot1, dot2, lbl1, lbl2)

        self.play(Create(axes), FadeIn(axes_labels), run_time=T_SHAPE_CREATE)
        self.play(Create(func1), FadeIn(func1_label), run_time=T_SHAPE_CREATE)
        self.play(Create(func2), FadeIn(func2_label), run_time=T_SHAPE_CREATE)
        self.wait(W_AFTER_ROUTINE)
        self.play(FadeIn(dot1, scale=1.5), FadeIn(lbl1), run_time=T_DOT_FADE + 0.2)
        self.play(FadeIn(dot2, scale=1.5), FadeIn(lbl2), run_time=T_DOT_FADE + 0.2)
        self.wait(W_AFTER_KEY)

        # Split layout
        div = self.setup_split_layout(graph_group)

        # Algebra: set equal
        s1 = Text("Barazojmë dy grafikët:", font_size=BODY_SIZE, color=BODY_TEXT_COLOR)
        s1.move_to(CALC_TOP)
        self.play(FadeIn(s1), run_time=T_STEP_TITLE)

        eq1 = self.show_equation(r"3^{2x-1} + 2 = 5 \times 3^{x-1}", reference=s1, buff=0.3, key=True)

        eq2_txt = Text(
            "Ky është i njëjti ekuacion\nsi në pikën a)!",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR, line_spacing=1.4,
        )
        eq2_txt.next_to(eq1, DOWN, buff=0.35)
        self.play(FadeIn(eq2_txt), run_time=T_BODY_FADE)
        self.wait(W_AFTER_ROUTINE)

        eq3 = self.show_equation(
            r"x_1 = 1 \qquad x_2 = \frac{\log 2}{\log 3}",
            reference=eq2_txt, color=LABEL_COLOR, key=True,
        )

        # Transition
        self.play(FadeOut(VGroup(s1, eq1, eq2_txt, eq3)), run_time=T_TRANSITION)
        self.wait(0.3)

        # Find y values
        y_title = self.show_step_title("Gjejmë y:")

        y1_txt = Text("Kur x = 1:", font_size=BODY_SIZE, color=BODY_TEXT_COLOR)
        y1_txt.next_to(y_title, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(FadeIn(y1_txt), run_time=T_BODY_FADE)

        y1_eq = self.show_equation(r"y = 5 \times 3^{1-1} = 5 \times 1 = 5", reference=y1_txt, key=True)

        y2_txt = MathTex(
            r"\text{Kur } x = \tfrac{\log 2}{\log 3}\text{:}",
            font_size=BODY_SIZE + 2, color=BODY_TEXT_COLOR,
        )
        y2_txt.next_to(y1_eq, DOWN, buff=0.35, aligned_edge=LEFT)
        self.play(FadeIn(y2_txt), run_time=T_BODY_FADE)

        y2_eq = self.show_equation(r"y = 5 \times \frac{2}{3} = \frac{10}{3}", reference=y2_txt, key=True)

        # Final answer
        ans = VGroup(
            MathTex(r"(1,\;5)", font_size=ANSWER_SIZE, color=ANSWER_COLOR),
            MathTex(r"\left(\frac{\log 2}{\log 3},\;\frac{10}{3}\right)",
                    font_size=ANSWER_SIZE, color=ANSWER_COLOR),
        ).arrange(RIGHT, buff=1.0)
        ans.next_to(y2_eq, DOWN, buff=0.5)
        box = make_answer_box(ans)

        self.play(Write(ans), run_time=T_KEY_EQUATION)
        self.play(Create(box), run_time=0.5)
        self.wait(W_AFTER_ANSWER)
