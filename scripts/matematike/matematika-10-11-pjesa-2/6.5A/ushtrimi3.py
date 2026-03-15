import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from manim import *
import numpy as np
from components import ExerciseScene
from style_guide import (
    STEP_TITLE_COLOR, BODY_TEXT_COLOR, LABEL_COLOR,
    ANSWER_COLOR, SHAPE_COLOR,
    BODY_SIZE, PROBLEM_MATH_SIZE, CALC_SIZE, STEP_TITLE_SIZE,
    T_SHAPE_CREATE, T_KEY_EQUATION, T_ROUTINE_EQUATION,
    T_STEP_TITLE, T_BODY_FADE, T_TRANSITION,
    W_AFTER_KEY, W_AFTER_ROUTINE, W_PROBLEM,
)


class Ushtrimi3(ExerciseScene):
    """
    Ushtrimi 3 — Njësia 6.5A
    Matematika 10-11: Pjesa II

    Skiconi grafikët e rrathëve dhe emërtoni pikëprerjet me boshtet.
    """

    exercise_number = 3
    unit = "6.5A"
    parts = ["a", "b", "c", "d", "e", "f"]

    # ================================================================
    #  PART A — x² + y² = 49,  r = 7
    #  Full detailed walkthrough
    # ================================================================
    def part_a(self):
        self.show_part_header("a")

        # --- Screen 1: Problem statement ---
        prob = MathTex(r"x^2 + y^2 = 49", font_size=PROBLEM_MATH_SIZE + 4)
        prob.move_to(ORIGIN)
        self.play(FadeIn(prob, shift=UP * 0.3), run_time=T_SHAPE_CREATE)
        self.wait(W_PROBLEM)
        self.play(FadeOut(prob), run_time=T_TRANSITION)
        self.wait(0.3)

        # --- Screen 2: Identify as circle ---
        exp_title = MathTex(
            r"\text{Njohim ekuacionin:}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        exp_line1 = MathTex(
            r"\text{Kjo \"{e}sht\"{e} forma e rrethit me}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        exp_line2 = MathTex(
            r"\text{qend\"{e}r n\"{e} origjin\"{e} (0, 0).}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        exp_eq = MathTex(r"x^2 + y^2 = r^2", font_size=CALC_SIZE)
        exp_r = MathTex(r"r^2 = 49 \implies r = 7", font_size=CALC_SIZE, color=ANSWER_COLOR)

        exp_group = VGroup(exp_title, exp_line1, exp_line2, exp_eq, exp_r).arrange(
            DOWN, buff=0.35
        ).move_to(ORIGIN)

        self.play(FadeIn(exp_group, shift=UP * 0.2), run_time=T_SHAPE_CREATE)
        self.wait(3.0)
        self.play(FadeOut(exp_group), run_time=T_TRANSITION)
        self.wait(0.3)

        # --- Screen 3: Find axis intercepts ---
        int_title = MathTex(
            r"\text{Pik\"{e}prerjet me boshtet:}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )

        int_x_title = MathTex(
            r"\text{Me boshtin } x \; (y = 0)\text{:}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        int_x_eq = MathTex(r"x^2 = 49 \implies x = \pm 7", font_size=CALC_SIZE)
        int_x_pts = MathTex(
            r"(-7,\,0) \quad \text{dhe} \quad (7,\,0)",
            font_size=CALC_SIZE, color=LABEL_COLOR,
        )

        int_y_title = MathTex(
            r"\text{Me boshtin } y \; (x = 0)\text{:}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        int_y_eq = MathTex(r"y^2 = 49 \implies y = \pm 7", font_size=CALC_SIZE)
        int_y_pts = MathTex(
            r"(0,\,-7) \quad \text{dhe} \quad (0,\,7)",
            font_size=CALC_SIZE, color=LABEL_COLOR,
        )

        x_block = VGroup(int_x_title, int_x_eq, int_x_pts).arrange(
            DOWN, buff=0.2, aligned_edge=LEFT
        )
        y_block = VGroup(int_y_title, int_y_eq, int_y_pts).arrange(
            DOWN, buff=0.2, aligned_edge=LEFT
        )
        int_group = VGroup(int_title, x_block, y_block).arrange(
            DOWN, buff=0.4
        ).move_to(ORIGIN)

        self.play(FadeIn(int_title), run_time=T_STEP_TITLE)
        self.wait(0.5)
        self.play(FadeIn(int_x_title), run_time=T_BODY_FADE)
        self.play(Write(int_x_eq), run_time=T_ROUTINE_EQUATION)
        self.play(Write(int_x_pts), run_time=T_ROUTINE_EQUATION)
        self.wait(2.0)
        self.play(FadeIn(int_y_title), run_time=T_BODY_FADE)
        self.play(Write(int_y_eq), run_time=T_ROUTINE_EQUATION)
        self.play(Write(int_y_pts), run_time=T_ROUTINE_EQUATION)
        self.wait(3.0)
        self.play(FadeOut(int_group), run_time=T_TRANSITION)
        self.wait(0.3)

        # --- Screen 4: Graph ---
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
        self.show_part_header("b")

        # --- Screen 1: Problem + radius ---
        prob = MathTex(r"x^2 + y^2 = 64", font_size=PROBLEM_MATH_SIZE + 4)
        r_eq = MathTex(r"r^2 = 64 \implies r = 8", font_size=CALC_SIZE, color=ANSWER_COLOR)
        grp = VGroup(prob, r_eq).arrange(DOWN, buff=0.4).move_to(ORIGIN)

        self.play(FadeIn(prob), run_time=T_SHAPE_CREATE)
        self.wait(2.0)
        self.play(Write(r_eq), run_time=T_KEY_EQUATION)
        self.wait(2.5)
        self.play(FadeOut(grp), run_time=T_TRANSITION)
        self.wait(0.3)

        # --- Screen 2: Intercepts ---
        int_title = MathTex(
            r"\text{Pik\"{e}prerjet me boshtet:}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        int_x = MathTex(
            r"x = \pm 8 \;\Rightarrow\; (-8,\,0),\; (8,\,0)",
            font_size=CALC_SIZE, color=LABEL_COLOR,
        )
        int_y = MathTex(
            r"y = \pm 8 \;\Rightarrow\; (0,\,-8),\; (0,\,8)",
            font_size=CALC_SIZE, color=LABEL_COLOR,
        )
        int_grp = VGroup(int_title, int_x, int_y).arrange(DOWN, buff=0.4).move_to(ORIGIN)

        self.play(FadeIn(int_grp, shift=UP * 0.2), run_time=T_SHAPE_CREATE)
        self.wait(3.0)
        self.play(FadeOut(int_grp), run_time=T_TRANSITION)
        self.wait(0.3)

        # --- Screen 3: Graph ---
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
        self.show_part_header("c")

        # --- Screen 1: Problem + radius ---
        prob = MathTex(r"x^2 + y^2 = 2", font_size=PROBLEM_MATH_SIZE + 4)
        r_eq = MathTex(
            r"r^2 = 2 \implies r = \sqrt{2}",
            font_size=CALC_SIZE, color=ANSWER_COLOR,
        )
        grp = VGroup(prob, r_eq).arrange(DOWN, buff=0.4).move_to(ORIGIN)

        self.play(FadeIn(prob), run_time=T_SHAPE_CREATE)
        self.wait(2.0)
        self.play(Write(r_eq), run_time=T_KEY_EQUATION)
        self.wait(2.5)
        self.play(FadeOut(grp), run_time=T_TRANSITION)
        self.wait(0.3)

        # --- Screen 2: Intercepts ---
        int_title = MathTex(
            r"\text{Pik\"{e}prerjet me boshtet:}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        int_x = MathTex(
            r"x = \pm\sqrt{2} \;\Rightarrow\; (-\sqrt{2},\,0),\; (\sqrt{2},\,0)",
            font_size=CALC_SIZE, color=LABEL_COLOR,
        )
        int_y = MathTex(
            r"y = \pm\sqrt{2} \;\Rightarrow\; (0,\,-\sqrt{2}),\; (0,\,\sqrt{2})",
            font_size=CALC_SIZE, color=LABEL_COLOR,
        )
        int_grp = VGroup(int_title, int_x, int_y).arrange(DOWN, buff=0.4).move_to(ORIGIN)

        self.play(FadeIn(int_grp, shift=UP * 0.2), run_time=T_SHAPE_CREATE)
        self.wait(3.0)
        self.play(FadeOut(int_grp), run_time=T_TRANSITION)
        self.wait(0.3)

        # --- Screen 3: Graph ---
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
        self.show_part_header("d")

        # --- Screen 1: Problem + radius ---
        prob = MathTex(r"x^2 + y^2 = 20", font_size=PROBLEM_MATH_SIZE + 4)
        r_eq = MathTex(
            r"r^2 = 20 \implies r = 2\sqrt{5}",
            font_size=CALC_SIZE, color=ANSWER_COLOR,
        )
        grp = VGroup(prob, r_eq).arrange(DOWN, buff=0.4).move_to(ORIGIN)

        self.play(FadeIn(prob), run_time=T_SHAPE_CREATE)
        self.wait(2.0)
        self.play(Write(r_eq), run_time=T_KEY_EQUATION)
        self.wait(2.5)
        self.play(FadeOut(grp), run_time=T_TRANSITION)
        self.wait(0.3)

        # --- Screen 2: Intercepts ---
        int_title = MathTex(
            r"\text{Pik\"{e}prerjet me boshtet:}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        int_x = MathTex(
            r"x = \pm 2\sqrt{5} \;\Rightarrow\; (-2\sqrt{5},\,0),\; (2\sqrt{5},\,0)",
            font_size=CALC_SIZE, color=LABEL_COLOR,
        )
        int_y = MathTex(
            r"y = \pm 2\sqrt{5} \;\Rightarrow\; (0,\,-2\sqrt{5}),\; (0,\,2\sqrt{5})",
            font_size=CALC_SIZE, color=LABEL_COLOR,
        )
        int_grp = VGroup(int_title, int_x, int_y).arrange(DOWN, buff=0.4).move_to(ORIGIN)

        self.play(FadeIn(int_grp, shift=UP * 0.2), run_time=T_SHAPE_CREATE)
        self.wait(3.0)
        self.play(FadeOut(int_grp), run_time=T_TRANSITION)
        self.wait(0.3)

        # --- Screen 3: Graph ---
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
        self.show_part_header("e")

        # --- Screen 1: Show original form ---
        prob = MathTex(r"y^2 = 4 - x^2", font_size=PROBLEM_MATH_SIZE + 4)
        prob.move_to(ORIGIN)
        self.play(FadeIn(prob), run_time=T_SHAPE_CREATE)
        self.wait(2.5)
        self.play(FadeOut(prob), run_time=T_TRANSITION)
        self.wait(0.3)

        # --- Screen 2: Rewrite + radius ---
        rewrite_title = MathTex(
            r"\text{Rishkruajm\"{e} n\"{e} form\"{e}n standarde:}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        rewrite_eq = MathTex(
            r"x^2 + y^2 = 4",
            font_size=CALC_SIZE, color=WHITE,
        )
        r_eq = MathTex(r"r = 2", font_size=CALC_SIZE, color=ANSWER_COLOR)
        rw_grp = VGroup(rewrite_title, rewrite_eq, r_eq).arrange(
            DOWN, buff=0.4
        ).move_to(ORIGIN)

        self.play(FadeIn(rewrite_title), run_time=T_STEP_TITLE)
        self.wait(0.5)
        self.play(Write(rewrite_eq), run_time=T_KEY_EQUATION)
        self.wait(2.0)
        self.play(Write(r_eq), run_time=T_ROUTINE_EQUATION)
        self.wait(3.0)
        self.play(FadeOut(rw_grp), run_time=T_TRANSITION)
        self.wait(0.3)

        # --- Screen 3: Intercepts ---
        int_title = MathTex(
            r"\text{Pik\"{e}prerjet me boshtet:}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        int_x = MathTex(
            r"x = \pm 2 \;\Rightarrow\; (-2,\,0),\; (2,\,0)",
            font_size=CALC_SIZE, color=LABEL_COLOR,
        )
        int_y = MathTex(
            r"y = \pm 2 \;\Rightarrow\; (0,\,-2),\; (0,\,2)",
            font_size=CALC_SIZE, color=LABEL_COLOR,
        )
        int_grp = VGroup(int_title, int_x, int_y).arrange(DOWN, buff=0.4).move_to(ORIGIN)

        self.play(FadeIn(int_grp, shift=UP * 0.2), run_time=T_SHAPE_CREATE)
        self.wait(3.0)
        self.play(FadeOut(int_grp), run_time=T_TRANSITION)
        self.wait(0.3)

        # --- Screen 4: Graph ---
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
        self.show_part_header("f")

        # --- Screen 1: Show original form ---
        prob = MathTex(r"y^2 = 16 - x^2", font_size=PROBLEM_MATH_SIZE + 4)
        prob.move_to(ORIGIN)
        self.play(FadeIn(prob), run_time=T_SHAPE_CREATE)
        self.wait(2.5)
        self.play(FadeOut(prob), run_time=T_TRANSITION)
        self.wait(0.3)

        # --- Screen 2: Rewrite + radius ---
        rewrite_title = MathTex(
            r"\text{Rishkruajm\"{e} n\"{e} form\"{e}n standarde:}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        rewrite_eq = MathTex(
            r"x^2 + y^2 = 16",
            font_size=CALC_SIZE, color=WHITE,
        )
        r_eq = MathTex(r"r = 4", font_size=CALC_SIZE, color=ANSWER_COLOR)
        rw_grp = VGroup(rewrite_title, rewrite_eq, r_eq).arrange(
            DOWN, buff=0.4
        ).move_to(ORIGIN)

        self.play(FadeIn(rewrite_title), run_time=T_STEP_TITLE)
        self.wait(0.5)
        self.play(Write(rewrite_eq), run_time=T_KEY_EQUATION)
        self.wait(2.0)
        self.play(Write(r_eq), run_time=T_ROUTINE_EQUATION)
        self.wait(3.0)
        self.play(FadeOut(rw_grp), run_time=T_TRANSITION)
        self.wait(0.3)

        # --- Screen 3: Intercepts ---
        int_title = MathTex(
            r"\text{Pik\"{e}prerjet me boshtet:}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        int_x = MathTex(
            r"x = \pm 4 \;\Rightarrow\; (-4,\,0),\; (4,\,0)",
            font_size=CALC_SIZE, color=LABEL_COLOR,
        )
        int_y = MathTex(
            r"y = \pm 4 \;\Rightarrow\; (0,\,-4),\; (0,\,4)",
            font_size=CALC_SIZE, color=LABEL_COLOR,
        )
        int_grp = VGroup(int_title, int_x, int_y).arrange(DOWN, buff=0.4).move_to(ORIGIN)

        self.play(FadeIn(int_grp, shift=UP * 0.2), run_time=T_SHAPE_CREATE)
        self.wait(3.0)
        self.play(FadeOut(int_grp), run_time=T_TRANSITION)
        self.wait(0.3)

        # --- Screen 4: Graph ---
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
        self.show_summary_table(
            "Përmbledhje",
            [
                r"\text{a)}\; x^2+y^2=49 \quad r=7 \quad (\pm7,0),\;(0,\pm7)",
                r"\text{b)}\; x^2+y^2=64 \quad r=8 \quad (\pm8,0),\;(0,\pm8)",
                r"\text{c)}\; x^2+y^2=2 \quad r=\sqrt{2} \quad (\pm\sqrt{2},0),\;(0,\pm\sqrt{2})",
                r"\text{d)}\; x^2+y^2=20 \quad r=2\sqrt{5} \quad (\pm2\sqrt{5},0),\;(0,\pm2\sqrt{5})",
                r"\text{e)}\; x^2+y^2=4 \quad r=2 \quad (\pm2,0),\;(0,\pm2)",
                r"\text{f)}\; x^2+y^2=16 \quad r=4 \quad (\pm4,0),\;(0,\pm4)",
            ],
            font_size=26,
        )
