import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from manim import *
import numpy as np
from components import ExerciseScene
from style_guide import (
    STEP_TITLE_COLOR, BODY_TEXT_COLOR, LABEL_COLOR,
    ANSWER_COLOR, SHAPE_COLOR,
    STEP_TITLE_SIZE, BODY_SIZE, PROBLEM_MATH_SIZE, CALC_SIZE,
    T_STEP_TITLE, T_BODY_FADE, T_KEY_EQUATION,
    T_SHAPE_CREATE, T_TRANSITION,
    W_AFTER_KEY, W_AFTER_ROUTINE, W_PROBLEM,
    CALC_TOP,
)


class Ushtrimi2(ExerciseScene):
    """
    Ushtrimi 2 — Njësia 5.1B
    Matematika 12

    Zgjidhni ekuacionet logaritmike. Argumentoni përgjigjet.
    """

    exercise_number = 2
    unit = "5.1B"
    textbook = "Matematika 12"
    parts = ["a", "b", "c", "d"]

    # ================================================================
    #  PART A — log₁₀(2x - 40) = 3
    # ================================================================
    def part_a(self):
        self.show_part_header("a")
        self.show_problem(
            MathTex(r"\log_{10}(2x - 40) = 3", font_size=PROBLEM_MATH_SIZE + 4),
        )

        # Step 1: Apply log definition
        s1 = self.show_step_title("Hapi 1: Përkufizimi i logaritmit")

        s1_txt = Text(
            r"log_b(a) = c  ⇒  a = b^c",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        s1_txt.next_to(s1, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(FadeIn(s1_txt), run_time=T_BODY_FADE)
        self.wait(W_AFTER_ROUTINE)

        eqs = self.show_equation_chain([
            {"tex": r"2x - 40 = 10^3", "key": True},
            r"2x - 40 = 1000",
        ], start_reference=s1_txt)

        # Step 2: Solve for x
        s2 = self.show_step_title("Hapi 2: Zgjidhim për x", reference=eqs[-1])

        eqs2 = self.show_equation_chain([
            r"2x = 1040",
            {"tex": r"x = 520", "color": ANSWER_COLOR, "font_size": CALC_SIZE + 2, "key": True},
        ], start_reference=s2)

        self.show_answer_below(r"x = 520", eqs2[-1])

    # ================================================================
    #  PART B — log₅(3x + 4) = 2
    # ================================================================
    def part_b(self):
        self.show_part_header("b")
        self.show_problem(
            MathTex(r"\log_5(3x + 4) = 2", font_size=PROBLEM_MATH_SIZE + 4),
        )

        s1 = self.show_step_title("Hapi 1: Përkufizimi i logaritmit")

        eqs = self.show_equation_chain([
            {"tex": r"3x + 4 = 5^2", "key": True},
            r"3x + 4 = 25",
        ], start_reference=s1)

        s2 = self.show_step_title("Hapi 2: Zgjidhim për x", reference=eqs[-1])

        eqs2 = self.show_equation_chain([
            r"3x = 21",
            {"tex": r"x = 7", "color": ANSWER_COLOR, "font_size": CALC_SIZE + 2, "key": True},
        ], start_reference=s2)

        self.show_answer_below(r"x = 7", eqs2[-1])

    # ================================================================
    #  PART C — log₃(x+2) − log₃x = log₃8
    # ================================================================
    def part_c(self):
        self.show_part_header("c")
        self.show_problem(
            MathTex(r"\log_3(x+2) - \log_3 x = \log_3 8", font_size=PROBLEM_MATH_SIZE + 4),
        )

        # Step 1: Log subtraction property
        s1 = self.show_step_title("Hapi 1: Vetia e zbritjes")

        s1_txt = Text(
            "log_b(a) − log_b(c) = log_b(a/c)",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        s1_txt.next_to(s1, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(FadeIn(s1_txt), run_time=T_BODY_FADE)
        self.wait(W_AFTER_ROUTINE)

        eq1 = self.show_equation(
            r"\log_3\left(\frac{x+2}{x}\right) = \log_3 8",
            reference=s1_txt, key=True, color=LABEL_COLOR,
        )

        # Step 2: Equal logs → equal arguments
        s2 = self.show_step_title("Hapi 2: Barazojmë argumentet", reference=eq1)

        eqs = self.show_equation_chain([
            {"tex": r"\frac{x+2}{x} = 8", "key": True},
            r"x + 2 = 8x",
            r"2 = 7x",
            {"tex": r"x = \frac{2}{7}", "color": ANSWER_COLOR, "font_size": CALC_SIZE + 2, "key": True},
        ], start_reference=s2)

        self.show_answer_below(r"x = \dfrac{2}{7}", eqs[-1])

    # ================================================================
    #  PART D — log₃(x+2) + log₃x = 1
    # ================================================================
    def part_d(self):
        self.show_part_header("d")
        self.show_problem(
            MathTex(r"\log_3(x+2) + \log_3 x = 1", font_size=PROBLEM_MATH_SIZE + 4),
        )

        # Step 1: Log addition property
        s1 = self.show_step_title("Hapi 1: Vetia e mbledhjes")

        s1_txt = Text(
            "log_b(a) + log_b(c) = log_b(a·c)",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        s1_txt.next_to(s1, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(FadeIn(s1_txt), run_time=T_BODY_FADE)
        self.wait(W_AFTER_ROUTINE)

        eqs = self.show_equation_chain([
            {"tex": r"\log_3[x(x+2)] = 1", "color": LABEL_COLOR, "key": True},
            r"x^2 + 2x = 3^1",
            {"tex": r"x^2 + 2x - 3 = 0", "color": LABEL_COLOR},
        ], start_reference=s1_txt)

        # Clear and continue
        self.play(FadeOut(VGroup(s1, s1_txt, *eqs)), run_time=T_TRANSITION)
        self.wait(0.3)

        # Step 2: Factor
        s2 = self.show_step_title("Hapi 2: Faktorizimi")

        eqs2 = self.show_equation_chain([
            r"x^2 + 2x - 3 = 0",
            {"tex": r"(x + 3)(x - 1) = 0", "color": LABEL_COLOR, "key": True},
            {"tex": r"x_1 = -3 \qquad x_2 = 1", "font_size": CALC_SIZE + 2},
        ], start_reference=s2)

        # Step 3: Argument — reject x = -3
        s3 = self.show_step_title("Hapi 3: Argumentimi", reference=eqs2[-1], buff=0.5)

        s3_txt = Text(
            "Logaritmi nuk pranon vlera negative:\nx > 0, prandaj x = −3 eliminohet.",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR, line_spacing=1.4,
        )
        s3_txt.next_to(s3, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(FadeIn(s3_txt), run_time=T_BODY_FADE)
        self.wait(W_AFTER_KEY)

        self.show_answer_below(r"x = 1", s3_txt)

    # ================================================================
    #  FINAL SUMMARY
    # ================================================================
    def final_summary(self):
        self.show_summary_table(
            "Përmbledhje e përgjigjeve",
            [
                r"\text{a)}\quad x = 520",
                r"\text{b)}\quad x = 7",
                r"\text{c)}\quad x = \frac{2}{7}",
                r"\text{d)}\quad x = 1",
            ],
            font_size=30,
        )
