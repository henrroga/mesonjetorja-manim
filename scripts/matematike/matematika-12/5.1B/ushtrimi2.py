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
    #  Full detailed walkthrough (first part teaches the technique)
    # ================================================================
    def part_a(self):
        self.show_part_header("a")
        self.show_problem(
            MathTex(r"\log_{10}(2x - 40) = 3", font_size=PROBLEM_MATH_SIZE + 4),
        )

        # Step 1: Recognize the type — this is a log = number equation
        s1 = self.show_step_title("Hapi 1: Njohim llojin e ekuacionit")

        s1_txt = Text(
            "Kemi logaritëm të barabartë me një numër.\nKëtë e zgjidhim duke e kthyer në\nformë eksponenciale.",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR, line_spacing=1.4,
        )
        s1_txt.next_to(s1, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(FadeIn(s1_txt), run_time=T_BODY_FADE)
        self.wait(W_AFTER_KEY)

        # Show the general rule prominently
        rule = MathTex(
            r"\log_b(a) = c \;\;\Longleftrightarrow\;\; a = b^c",
            font_size=CALC_SIZE + 4, color=LABEL_COLOR,
        )
        rule.next_to(s1_txt, DOWN, buff=0.35)
        self.play(Write(rule), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_KEY)

        # Step 2: Identify components
        s2_txt = Text(
            "Identifikojmë: b = 10, a = 2x−40, c = 3",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        s2_txt.next_to(rule, DOWN, buff=0.3)
        self.play(FadeIn(s2_txt), run_time=T_BODY_FADE)
        self.wait(W_AFTER_ROUTINE)

        # Apply
        eqs = self.show_equation_chain([
            {"tex": r"2x - 40 = 10^3", "key": True},
            {"tex": r"2x - 40 = 1000", "color": LABEL_COLOR},
        ], start_reference=s2_txt)

        # Transition
        self.play(FadeOut(VGroup(s1, s1_txt, rule, s2_txt, *eqs)), run_time=T_TRANSITION)
        self.wait(0.3)

        # Step 3: Solve the linear equation
        s3 = self.show_step_title("Hapi 2: Zgjidhim ekuacionin linear")

        s3_txt = Text(
            "Tani kemi ekuacion të thjeshtë linear.\nIzolojmë x:",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR, line_spacing=1.4,
        )
        s3_txt.next_to(s3, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(FadeIn(s3_txt), run_time=T_BODY_FADE)
        self.wait(W_AFTER_ROUTINE)

        eqs2 = self.show_equation_chain([
            r"2x = 1000 + 40",
            r"2x = 1040",
            {"tex": r"x = 520", "color": ANSWER_COLOR, "font_size": CALC_SIZE + 2, "key": True},
        ], start_reference=s3_txt)

        # Step 4: Verify domain
        s4 = self.show_step_title("Hapi 3: Verifikimi", reference=eqs2[-1], buff=0.4)

        s4_txt = Text(
            "Argumenti i logaritmit duhet > 0:\n2(520) − 40 = 1000 > 0  ✓",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR, line_spacing=1.4,
        )
        s4_txt.next_to(s4, DOWN, buff=0.2, aligned_edge=LEFT)
        self.play(FadeIn(s4_txt), run_time=T_BODY_FADE)
        self.wait(W_AFTER_ROUTINE)

        self.show_answer_below(r"x = 520", s4_txt)

    # ================================================================
    #  PART B — log₅(3x + 4) = 2
    #  Same technique, slightly faster (students saw it in part a)
    # ================================================================
    def part_b(self):
        self.show_part_header("b")
        self.show_problem(
            MathTex(r"\log_5(3x + 4) = 2", font_size=PROBLEM_MATH_SIZE + 4),
        )

        # Remind the technique briefly
        s1 = self.show_step_title("Hapi 1: Formë eksponenciale")

        s1_txt = Text(
            "Njëlloj si në pikën a), kthejmë\nlogaritmin në formë eksponenciale:",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR, line_spacing=1.4,
        )
        s1_txt.next_to(s1, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(FadeIn(s1_txt), run_time=T_BODY_FADE)
        self.wait(W_AFTER_ROUTINE)

        eqs = self.show_equation_chain([
            {"tex": r"3x + 4 = 5^2", "key": True},
            r"3x + 4 = 25",
        ], start_reference=s1_txt)

        # Step 2: Solve
        s2 = self.show_step_title("Hapi 2: Zgjidhim për x", reference=eqs[-1])

        eqs2 = self.show_equation_chain([
            r"3x = 25 - 4 = 21",
            {"tex": r"x = 7", "color": ANSWER_COLOR, "font_size": CALC_SIZE + 2, "key": True},
        ], start_reference=s2)

        # Quick verify
        s3_txt = Text(
            "Verifikim: 3(7)+4 = 25 > 0  ✓",
            font_size=BODY_SIZE - 2, color=BODY_TEXT_COLOR,
        )
        s3_txt.next_to(eqs2[-1], DOWN, buff=0.3)
        self.play(FadeIn(s3_txt), run_time=T_BODY_FADE)
        self.wait(W_AFTER_ROUTINE)

        self.show_answer_below(r"x = 7", s3_txt)

    # ================================================================
    #  PART C — log₃(x+2) − log₃x = log₃8
    #  New technique: log subtraction property
    # ================================================================
    def part_c(self):
        self.show_part_header("c")
        self.show_problem(
            MathTex(r"\log_3(x+2) - \log_3 x = \log_3 8", font_size=PROBLEM_MATH_SIZE + 4),
        )

        # Step 1: Explain the property
        s1 = self.show_step_title("Hapi 1: Vetia e zbritjes së logaritmeve")

        s1_txt = Text(
            "Kur kemi zbritje logaritmesh me bazë\ntë njëjtë, ato bashkohen si herës:",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR, line_spacing=1.4,
        )
        s1_txt.next_to(s1, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(FadeIn(s1_txt), run_time=T_BODY_FADE)
        self.wait(W_AFTER_ROUTINE)

        # Show general rule
        rule = MathTex(
            r"\log_b a - \log_b c = \log_b\!\left(\frac{a}{c}\right)",
            font_size=CALC_SIZE + 2, color=LABEL_COLOR,
        )
        rule.next_to(s1_txt, DOWN, buff=0.3)
        self.play(Write(rule), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_KEY)

        # Apply it
        eq1 = self.show_equation(
            r"\log_3\!\left(\frac{x+2}{x}\right) = \log_3 8",
            reference=rule, key=True,
        )

        # Step 2: Equal logs, equal arguments
        s2_txt = Text(
            "Kur bazat janë të njëjta,\nargumentet duhet të barabarta:",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR, line_spacing=1.4,
        )
        s2_txt.next_to(eq1, DOWN, buff=0.3)
        self.play(FadeIn(s2_txt), run_time=T_BODY_FADE)
        self.wait(W_AFTER_ROUTINE)

        # Transition
        self.play(FadeOut(VGroup(s1, s1_txt, rule, eq1, s2_txt)), run_time=T_TRANSITION)
        self.wait(0.3)

        # Step 3: Solve
        s3 = self.show_step_title("Hapi 2: Zgjidhim ekuacionin")

        eqs = self.show_equation_chain([
            {"tex": r"\frac{x+2}{x} = 8", "key": True},
            r"x + 2 = 8x",
            r"2 = 8x - x = 7x",
            {"tex": r"x = \frac{2}{7}", "color": ANSWER_COLOR, "font_size": CALC_SIZE + 2, "key": True},
        ], start_reference=s3)

        # Domain check
        s4 = self.show_step_title("Hapi 3: Verifikimi i kushteve", reference=eqs[-1], buff=0.4)

        s4_txt = Text(
            "Duhet x > 0 dhe x+2 > 0:\nx = 2/7 > 0  ✓  dhe  2/7+2 > 0  ✓",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR, line_spacing=1.4,
        )
        s4_txt.next_to(s4, DOWN, buff=0.2, aligned_edge=LEFT)
        self.play(FadeIn(s4_txt), run_time=T_BODY_FADE)
        self.wait(W_AFTER_ROUTINE)

        self.show_answer_below(r"x = \dfrac{2}{7}", s4_txt)

    # ================================================================
    #  PART D — log₃(x+2) + log₃x = 1
    #  New technique: log addition + quadratic + domain rejection
    # ================================================================
    def part_d(self):
        self.show_part_header("d")
        self.show_problem(
            MathTex(r"\log_3(x+2) + \log_3 x = 1", font_size=PROBLEM_MATH_SIZE + 4),
        )

        # Step 1: Log addition property
        s1 = self.show_step_title("Hapi 1: Vetia e mbledhjes së logaritmeve")

        s1_txt = Text(
            "Kur kemi mbledhje logaritmesh me bazë\ntë njëjtë, ato bashkohen si shumëzim:",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR, line_spacing=1.4,
        )
        s1_txt.next_to(s1, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(FadeIn(s1_txt), run_time=T_BODY_FADE)
        self.wait(W_AFTER_ROUTINE)

        rule = MathTex(
            r"\log_b a + \log_b c = \log_b(a \cdot c)",
            font_size=CALC_SIZE + 2, color=LABEL_COLOR,
        )
        rule.next_to(s1_txt, DOWN, buff=0.3)
        self.play(Write(rule), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_KEY)

        # Apply
        eqs = self.show_equation_chain([
            {"tex": r"\log_3[x(x+2)] = 1", "color": LABEL_COLOR, "key": True},
        ], start_reference=rule)

        # Convert to exponential
        s2_txt = Text(
            "Kthejmë në formë eksponenciale:",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        s2_txt.next_to(eqs[-1], DOWN, buff=0.3)
        self.play(FadeIn(s2_txt), run_time=T_BODY_FADE)
        self.wait(W_AFTER_ROUTINE)

        eqs2 = self.show_equation_chain([
            r"x(x+2) = 3^1 = 3",
            r"x^2 + 2x = 3",
            {"tex": r"x^2 + 2x - 3 = 0", "color": LABEL_COLOR, "key": True},
        ], start_reference=s2_txt)

        # Transition
        self.play(FadeOut(VGroup(s1, s1_txt, rule, *eqs, s2_txt, *eqs2)), run_time=T_TRANSITION)
        self.wait(0.3)

        # Step 2: Factor the quadratic
        s3 = self.show_step_title("Hapi 2: Faktorizimi i ekuacionit kuadratik")

        s3_txt = Text(
            "Kërkojmë dy numra që shumëzohen −3\ndhe mblidhen +2: ato janë +3 dhe −1.",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR, line_spacing=1.4,
        )
        s3_txt.next_to(s3, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(FadeIn(s3_txt), run_time=T_BODY_FADE)
        self.wait(W_AFTER_KEY)

        eqs3 = self.show_equation_chain([
            r"x^2 + 2x - 3 = 0",
            {"tex": r"(x + 3)(x - 1) = 0", "color": LABEL_COLOR, "key": True},
            {"tex": r"x_1 = -3 \qquad x_2 = 1", "font_size": CALC_SIZE + 2},
        ], start_reference=s3_txt)

        # Step 3: Domain rejection — THE key teaching moment
        s4 = self.show_step_title("Hapi 3: Argumentimi — kush zgjidhje pranohet?", reference=eqs3[-1], buff=0.5)

        s4_txt1 = Text(
            "Logaritmi ekziston vetëm kur argumenti\nështë pozitiv. Kontrollojmë:",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR, line_spacing=1.4,
        )
        s4_txt1.next_to(s4, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(FadeIn(s4_txt1), run_time=T_BODY_FADE)
        self.wait(W_AFTER_ROUTINE)

        # Show both checks
        check1 = MathTex(
            r"x = -3: \quad \log_3(-3+2) = \log_3(-1) \;\;\text{— nuk ekziston!}",
            font_size=BODY_SIZE + 2, color=AUX_COLOR,
        )
        check1.next_to(s4_txt1, DOWN, buff=0.3)

        check2 = MathTex(
            r"x = 1: \quad \log_3(1+2) + \log_3(1) = \log_3 3 + 0 = 1 \;\;\checkmark",
            font_size=BODY_SIZE + 2, color=ANSWER_COLOR,
        )
        check2.next_to(check1, DOWN, buff=0.25)

        self.play(Write(check1), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_KEY)
        self.play(Write(check2), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_KEY)

        self.show_answer_below(r"x = 1", check2)

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
