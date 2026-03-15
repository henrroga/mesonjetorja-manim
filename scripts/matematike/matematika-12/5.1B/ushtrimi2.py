import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from manim import *
import numpy as np
from components import ExerciseScene
from style_guide import (
    make_answer_box, fade_all,
    STEP_TITLE_COLOR, BODY_TEXT_COLOR, LABEL_COLOR,
    ANSWER_COLOR, SHAPE_COLOR, AUX_COLOR, HIGHLIGHT_COLOR,
    STEP_TITLE_SIZE, BODY_SIZE, PROBLEM_MATH_SIZE, CALC_SIZE, ANSWER_SIZE,
    T_STEP_TITLE, T_BODY_FADE, T_KEY_EQUATION, T_ROUTINE_EQUATION,
    T_SHAPE_CREATE, T_TRANSITION,
    W_AFTER_KEY, W_AFTER_ROUTINE, W_AFTER_ANSWER, W_PROBLEM,
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
        self.wait(2)

        # --- Screen 1: Recognize the type + general rule ---
        s1 = self.show_step_title("Hapi 1: Njohim llojin e ekuacionit")

        s1_line1 = MathTex(
            r"\text{Kemi logarit\"{e}m t\"{e} barabart\"{e} me nj\"{e} num\"{e}r.}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        s1_line2 = MathTex(
            r"\text{K\"{e}t\"{e} e zgjidhim duke e kthyer n\"{e}}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        s1_line3 = MathTex(
            r"\text{form\"{e} eksponenciale.}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        s1_txt = VGroup(s1_line1, s1_line2, s1_line3).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        s1_txt.next_to(s1, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(FadeIn(s1_txt), run_time=T_BODY_FADE)
        self.wait(3)

        rule = MathTex(
            r"\log_b(a) = c \;\;\Longleftrightarrow\;\; a = b^c",
            font_size=CALC_SIZE + 4, color=LABEL_COLOR,
        )
        rule.next_to(s1_txt, DOWN, buff=0.35)
        self.play(Write(rule), run_time=T_KEY_EQUATION)
        self.wait(3)

        # Identify components
        s2_txt = MathTex(
            r"\text{Identifikojm\"{e}:} \quad b = 10,\; a = 2x-40,\; c = 3",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        s2_txt.next_to(rule, DOWN, buff=0.3)
        self.play(FadeIn(s2_txt), run_time=T_BODY_FADE)
        self.wait(2)

        # Apply
        eqs = self.show_equation_chain([
            {"tex": r"2x - 40 = 10^3", "key": True},
            {"tex": r"2x - 40 = 1000", "color": LABEL_COLOR},
        ], start_reference=s2_txt)
        self.wait(2)

        # Clear screen
        self.play(FadeOut(VGroup(s1, s1_txt, rule, s2_txt, *eqs)), run_time=T_TRANSITION)
        self.wait(0.5)

        # --- Screen 2: Solve the linear equation ---
        s3 = self.show_step_title("Hapi 2: Zgjidhim ekuacionin linear")

        s3_line1 = MathTex(
            r"\text{Tani kemi ekuacion t\"{e} thjesht\"{e} linear.}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        s3_line2 = MathTex(
            r"\text{Izolojm\"{e} } x\text{:}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        s3_txt = VGroup(s3_line1, s3_line2).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        s3_txt.next_to(s3, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(FadeIn(s3_txt), run_time=T_BODY_FADE)
        self.wait(2)

        eqs2 = self.show_equation_chain([
            r"2x = 1000 + 40",
            r"2x = 1040",
            {"tex": r"x = 520", "color": ANSWER_COLOR, "font_size": CALC_SIZE + 2, "key": True},
        ], start_reference=s3_txt)
        self.wait(3)

        # Clear screen
        self.play(FadeOut(VGroup(s3, s3_txt, *eqs2)), run_time=T_TRANSITION)
        self.wait(0.5)

        # --- Screen 3: Verify domain ---
        s4 = self.show_step_title("Hapi 3: Verifikimi")

        s4_line1 = MathTex(
            r"\text{Argumenti i logaritmit duhet} > 0\text{:}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        s4_line2 = MathTex(
            r"2(520) - 40 = 1000 > 0 \;\;\checkmark",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        s4_txt = VGroup(s4_line1, s4_line2).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        s4_txt.next_to(s4, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(FadeIn(s4_txt), run_time=T_BODY_FADE)
        self.wait(3)

        self.show_answer_below(r"x = 520", s4_txt)

    # ================================================================
    #  PART B — log₅(3x + 4) = 2
    # ================================================================
    def part_b(self):
        self.show_part_header("b")
        self.show_problem(
            MathTex(r"\log_5(3x + 4) = 2", font_size=PROBLEM_MATH_SIZE + 4),
        )
        self.wait(2)

        # --- Screen 1: Convert to exponential form ---
        s1 = self.show_step_title("Hapi 1: Form\u00eb eksponenciale")

        s1_line1 = MathTex(
            r"\text{Nj\"{e}lloj si n\"{e} pik\"{e}n a), kthejm\"{e}}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        s1_line2 = MathTex(
            r"\text{logaritmin n\"{e} form\"{e} eksponenciale:}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        s1_txt = VGroup(s1_line1, s1_line2).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        s1_txt.next_to(s1, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(FadeIn(s1_txt), run_time=T_BODY_FADE)
        self.wait(2)

        eqs = self.show_equation_chain([
            {"tex": r"3x + 4 = 5^2", "key": True},
            r"3x + 4 = 25",
        ], start_reference=s1_txt)
        self.wait(2)

        # Clear screen
        self.play(FadeOut(VGroup(s1, s1_txt, *eqs)), run_time=T_TRANSITION)
        self.wait(0.5)

        # --- Screen 2: Solve for x ---
        s2 = self.show_step_title("Hapi 2: Zgjidhim p\u00ebr x")

        eqs2 = self.show_equation_chain([
            r"3x = 25 - 4 = 21",
            {"tex": r"x = 7", "color": ANSWER_COLOR, "font_size": CALC_SIZE + 2, "key": True},
        ], start_reference=s2)
        self.wait(3)

        # Clear screen
        self.play(FadeOut(VGroup(s2, *eqs2)), run_time=T_TRANSITION)
        self.wait(0.5)

        # --- Screen 3: Verification + answer ---
        s3 = self.show_step_title("Hapi 3: Verifikimi")

        s3_txt = MathTex(
            r"3(7)+4 = 25 > 0 \;\;\checkmark",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        s3_txt.next_to(s3, DOWN, buff=0.3)
        self.play(FadeIn(s3_txt), run_time=T_BODY_FADE)
        self.wait(3)

        self.show_answer_below(r"x = 7", s3_txt)

    # ================================================================
    #  PART C — log₃(x+2) − log₃x = log₃8
    # ================================================================
    def part_c(self):
        self.show_part_header("c")
        self.show_problem(
            MathTex(r"\log_3(x+2) - \log_3 x = \log_3 8", font_size=PROBLEM_MATH_SIZE + 4),
        )
        self.wait(2)

        # --- Screen 1: Log subtraction property ---
        s1 = self.show_step_title("Hapi 1: Vetia e zbritjes s\u00eb logaritmeve")

        s1_line1 = MathTex(
            r"\text{Kur kemi zbritje logaritmesh me baz\"{e}}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        s1_line2 = MathTex(
            r"\text{t\"{e} nj\"{e}jt\"{e}, ato bashkohen si her\"{e}s:}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        s1_txt = VGroup(s1_line1, s1_line2).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        s1_txt.next_to(s1, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(FadeIn(s1_txt), run_time=T_BODY_FADE)
        self.wait(2)

        rule = MathTex(
            r"\log_b a - \log_b c = \log_b\!\left(\frac{a}{c}\right)",
            font_size=CALC_SIZE + 2, color=LABEL_COLOR,
        )
        rule.next_to(s1_txt, DOWN, buff=0.3)
        self.play(Write(rule), run_time=T_KEY_EQUATION)
        self.wait(3)

        # Apply it
        eq1 = self.show_equation(
            r"\log_3\!\left(\frac{x+2}{x}\right) = \log_3 8",
            reference=rule, key=True,
        )
        self.wait(2)

        # Equal logs, equal arguments
        s2_txt = MathTex(
            r"\text{Kur bazat jan\"{e} t\"{e} nj\"{e}jta, argumentet duhet t\"{e} barabarta.}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        s2_txt.next_to(eq1, DOWN, buff=0.3)
        self.play(FadeIn(s2_txt), run_time=T_BODY_FADE)
        self.wait(3)

        # Clear screen
        self.play(FadeOut(VGroup(s1, s1_txt, rule, eq1, s2_txt)), run_time=T_TRANSITION)
        self.wait(0.5)

        # --- Screen 2: Solve the equation ---
        s3 = self.show_step_title("Hapi 2: Zgjidhim ekuacionin")

        eqs = self.show_equation_chain([
            {"tex": r"\frac{x+2}{x} = 8", "key": True},
            r"x + 2 = 8x",
            r"2 = 8x - x = 7x",
            {"tex": r"x = \frac{2}{7}", "color": ANSWER_COLOR, "font_size": CALC_SIZE + 2, "key": True},
        ], start_reference=s3)
        self.wait(3)

        # Clear screen
        self.play(FadeOut(VGroup(s3, *eqs)), run_time=T_TRANSITION)
        self.wait(0.5)

        # --- Screen 3: Domain check + answer ---
        s4 = self.show_step_title("Hapi 3: Verifikimi i kushteve")

        s4_line1 = MathTex(
            r"\text{Duhet } x > 0 \text{ dhe } x+2 > 0\text{:}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        s4_line2 = MathTex(
            r"x = \tfrac{2}{7} > 0 \;\;\checkmark \quad \text{dhe} \quad \tfrac{2}{7}+2 > 0 \;\;\checkmark",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        s4_txt = VGroup(s4_line1, s4_line2).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        s4_txt.next_to(s4, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(FadeIn(s4_txt), run_time=T_BODY_FADE)
        self.wait(3)

        self.show_answer_below(r"x = \dfrac{2}{7}", s4_txt)

    # ================================================================
    #  PART D — log₃(x+2) + log₃x = 1
    # ================================================================
    def part_d(self):
        self.show_part_header("d")
        self.show_problem(
            MathTex(r"\log_3(x+2) + \log_3 x = 1", font_size=PROBLEM_MATH_SIZE + 4),
        )
        self.wait(2)

        # --- Screen 1: Log addition property ---
        s1 = self.show_step_title("Hapi 1: Vetia e mbledhjes s\u00eb logaritmeve")

        s1_line1 = MathTex(
            r"\text{Kur kemi mbledhje logaritmesh me baz\"{e}}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        s1_line2 = MathTex(
            r"\text{t\"{e} nj\"{e}jt\"{e}, ato bashkohen si shum\"{e}zim:}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        s1_txt = VGroup(s1_line1, s1_line2).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        s1_txt.next_to(s1, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(FadeIn(s1_txt), run_time=T_BODY_FADE)
        self.wait(2)

        rule = MathTex(
            r"\log_b a + \log_b c = \log_b(a \cdot c)",
            font_size=CALC_SIZE + 2, color=LABEL_COLOR,
        )
        rule.next_to(s1_txt, DOWN, buff=0.3)
        self.play(Write(rule), run_time=T_KEY_EQUATION)
        self.wait(3)

        # Apply
        eq_combined = self.show_equation(
            r"\log_3[x(x+2)] = 1",
            reference=rule, key=True, color=LABEL_COLOR,
        )
        self.wait(2)

        # Convert to exponential
        s2_txt = MathTex(
            r"\text{Kthejm\"{e} n\"{e} form\"{e} eksponenciale:}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        s2_txt.next_to(eq_combined, DOWN, buff=0.3)
        self.play(FadeIn(s2_txt), run_time=T_BODY_FADE)
        self.wait(2)

        eqs2 = self.show_equation_chain([
            r"x(x+2) = 3^1 = 3",
            r"x^2 + 2x = 3",
            {"tex": r"x^2 + 2x - 3 = 0", "color": LABEL_COLOR, "key": True},
        ], start_reference=s2_txt)
        self.wait(2)

        # Clear screen
        self.play(FadeOut(VGroup(s1, s1_txt, rule, eq_combined, s2_txt, *eqs2)), run_time=T_TRANSITION)
        self.wait(0.5)

        # --- Screen 2: Factor the quadratic ---
        s3 = self.show_step_title("Hapi 2: Faktorizimi i ekuacionit kuadratik")

        s3_line1 = MathTex(
            r"\text{K\"{e}rkojm\"{e} dy numra q\"{e} shum\"{e}zohen } {-3}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        s3_line2 = MathTex(
            r"\text{dhe mblidhen } {+2}\text{: ato jan\"{e} } {+3} \text{ dhe } {-1}\text{.}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        s3_txt = VGroup(s3_line1, s3_line2).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        s3_txt.next_to(s3, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(FadeIn(s3_txt), run_time=T_BODY_FADE)
        self.wait(3)

        eqs3 = self.show_equation_chain([
            r"x^2 + 2x - 3 = 0",
            {"tex": r"(x + 3)(x - 1) = 0", "color": LABEL_COLOR, "key": True},
            {"tex": r"x_1 = -3 \qquad x_2 = 1", "font_size": CALC_SIZE + 2},
        ], start_reference=s3_txt)
        self.wait(3)

        # Clear screen
        self.play(FadeOut(VGroup(s3, s3_txt, *eqs3)), run_time=T_TRANSITION)
        self.wait(0.5)

        # --- Screen 3: Domain rejection ---
        s4 = self.show_step_title("Hapi 3: Argumentimi")

        s4_line1 = MathTex(
            r"\text{Logaritmi ekziston vet\"{e}m kur argumenti}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        s4_line2 = MathTex(
            r"\text{\"{e}sht\"{e} pozitiv. Kontrollojm\"{e}:}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        s4_txt = VGroup(s4_line1, s4_line2).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        s4_txt.next_to(s4, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(FadeIn(s4_txt), run_time=T_BODY_FADE)
        self.wait(2)

        # Show both checks
        check1 = MathTex(
            r"x = -3: \quad \log_3(-3+2) = \log_3(-1)",
            font_size=BODY_SIZE + 2, color=AUX_COLOR,
        )
        check1_note = MathTex(
            r"\text{nuk ekziston!}",
            font_size=BODY_SIZE + 2, color=AUX_COLOR,
        )
        check1_note.next_to(check1, RIGHT, buff=0.2)
        check1_group = VGroup(check1, check1_note)
        check1_group.next_to(s4_txt, DOWN, buff=0.3)

        self.play(Write(check1_group), run_time=T_KEY_EQUATION)
        self.wait(3)

        check2 = MathTex(
            r"x = 1: \quad \log_3(1+2) + \log_3(1) = \log_3 3 + 0 = 1 \;\;\checkmark",
            font_size=BODY_SIZE + 2, color=ANSWER_COLOR,
        )
        check2.next_to(check1_group, DOWN, buff=0.25)

        self.play(Write(check2), run_time=T_KEY_EQUATION)
        self.wait(3)

        self.show_answer_below(r"x = 1", check2)

    # ================================================================
    #  FINAL SUMMARY
    # ================================================================
    def final_summary(self):
        self.show_summary_table(
            "P\u00ebrmbledhje e p\u00ebrgjigjeve",
            [
                r"\text{a)}\quad x = 520",
                r"\text{b)}\quad x = 7",
                r"\text{c)}\quad x = \frac{2}{7}",
                r"\text{d)}\quad x = 1",
            ],
            font_size=30,
        )
