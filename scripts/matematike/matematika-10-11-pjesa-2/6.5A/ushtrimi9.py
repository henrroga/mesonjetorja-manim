import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from manim import *
import numpy as np
from components import ExerciseScene
from style_guide import (
    make_divider, make_answer_box,
    STEP_TITLE_COLOR, BODY_TEXT_COLOR, LABEL_COLOR,
    ANSWER_COLOR, SHAPE_COLOR, AUX_COLOR, HIGHLIGHT_COLOR,
    PART_HEADER_SIZE, STEP_TITLE_SIZE,
    BODY_SIZE, PROBLEM_MATH_SIZE, CALC_SIZE, ANSWER_SIZE,
    T_STEP_TITLE, T_BODY_FADE, T_KEY_EQUATION, T_ROUTINE_EQUATION,
    T_SHAPE_CREATE, T_DOT_FADE, T_LAYOUT_SHIFT, T_TRANSITION,
    W_AFTER_KEY, W_AFTER_ROUTINE, W_AFTER_ANSWER, W_PROBLEM,
    CALC_TOP,
)


class Ushtrimi9(ExerciseScene):
    """
    Ushtrimi 9 — Njësia 6.5A
    Matematika 10-11: Pjesa II

    Sisteme ekuacionesh (rreth + drejtëz).
    """

    exercise_number = 9
    unit = "6.5A"
    parts = ["a", "b", "c", "d", "e", "f"]

    # ================================================================
    #  HELPER: Build circle-line graph with intersection dots
    # ================================================================
    def _build_circle_line_graph(self, radius, line_func, line_range,
                                  points, labels, axis_bound, axis_step=None):
        """
        Build a graph with circle + line and intersection points.

        Returns (graph_group, axes) for further manipulation.
        """
        axes = self.create_axes(axis_bound, axis_bound, step=axis_step)
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")

        circle = self.plot_circle(axes, radius)
        line = axes.plot(line_func, x_range=line_range,
                         color=AUX_COLOR, stroke_width=2.5)

        dots_and_labels = VGroup()
        colors = [LABEL_COLOR, HIGHLIGHT_COLOR]
        for i, ((x, y), lbl_tex) in enumerate(zip(points, labels)):
            dot, lbl = self.mark_point(axes, x, y, lbl_tex,
                                       color=colors[i % 2],
                                       direction=UR if i == 0 else DL)
            dots_and_labels.add(dot, lbl)

        graph_group = VGroup(axes, axes_labels, circle, line, dots_and_labels)

        # Animate
        self.play(Create(axes), FadeIn(axes_labels), run_time=T_SHAPE_CREATE)
        self.play(Create(circle), Create(line), run_time=T_SHAPE_CREATE)
        self.play(
            *[FadeIn(obj, scale=1.5) for obj in dots_and_labels],
            run_time=0.6,
        )
        self.wait(W_AFTER_ROUTINE)

        return graph_group

    def _show_system_problem(self, system_tex):
        """Show a system of equations problem statement."""
        prob = MathTex(system_tex, font_size=PROBLEM_MATH_SIZE + 4)
        prob.move_to(ORIGIN)
        self.play(FadeIn(prob, shift=UP * 0.3), run_time=T_SHAPE_CREATE)
        self.wait(W_PROBLEM - 1)
        self.play(FadeOut(prob), run_time=T_TRANSITION)
        self.wait(0.3)

    # ================================================================
    #  PART A  —  x² + y² = 25,  y = x + 1
    #  Full detailed walkthrough
    # ================================================================
    def part_a(self):
        self.show_part_header("a")

        # Problem Statement
        prob_title = Text("Sistemi:", font_size=STEP_TITLE_SIZE + 2, color=STEP_TITLE_COLOR, weight=BOLD)
        prob_eq = MathTex(
            r"\begin{cases} x^2 + y^2 = 25 \\ y = x + 1 \end{cases}",
            font_size=PROBLEM_MATH_SIZE + 4,
        )
        self.show_problem(prob_title, prob_eq)

        # Graph (centered first, then shifted left)
        axes = self.create_axes(7, 7)
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")

        circle = self.plot_circle(axes, 5)
        circle_label = MathTex(r"x^2+y^2=25", font_size=20, color=SHAPE_COLOR)
        circle_label.next_to(circle, UR, buff=0.1).shift(LEFT * 0.5)

        line = axes.plot(lambda x: x + 1, x_range=[-6, 5.5], color=AUX_COLOR, stroke_width=2.5)
        line_label = MathTex(r"y=x+1", font_size=20, color=AUX_COLOR)
        line_label.next_to(line.point_from_proportion(0.85), UR, buff=0.15)

        dot1, lbl1 = self.mark_point(axes, 3, 4, "(3,\\,4)", color=LABEL_COLOR, direction=UR)
        dot2, lbl2 = self.mark_point(axes, -4, -3, "(-4,\\,-3)", color=HIGHLIGHT_COLOR, direction=DL)

        graph_group = VGroup(axes, axes_labels, circle, circle_label, line, line_label, dot1, dot2, lbl1, lbl2)

        # Animate graph construction
        self.play(Create(axes), FadeIn(axes_labels), run_time=T_SHAPE_CREATE)
        self.play(Create(circle), FadeIn(circle_label), run_time=T_SHAPE_CREATE)
        self.play(Create(line), FadeIn(line_label), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)
        self.play(FadeIn(dot1, scale=1.5), FadeIn(lbl1), run_time=T_DOT_FADE + 0.2)
        self.play(FadeIn(dot2, scale=1.5), FadeIn(lbl2), run_time=T_DOT_FADE + 0.2)
        self.wait(W_AFTER_KEY)

        # Split layout
        div = self.setup_split_layout(graph_group)
        self.wait(0.3)

        # Step 1: Substitution
        s1_title = self.show_step_title("Hapi 1: Zëvendësimi")

        s1_txt = Text(
            "Zëvendësojmë y = x + 1\nnë ekuacionin e rrethit:",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR, line_spacing=1.4,
        )
        s1_txt.next_to(s1_title, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(FadeIn(s1_txt), run_time=T_BODY_FADE)
        self.wait(W_AFTER_ROUTINE)

        s1_eq1 = self.show_equation(r"x^2 + (x+1)^2 = 25", reference=s1_txt, buff=0.3, key=True)

        # Step 2: Expand & Simplify
        s2_title = self.show_step_title("Hapi 2: Thjeshtimi", reference=s1_eq1)

        eqs = self.show_equation_chain([
            r"x^2 + x^2 + 2x + 1 = 25",
            r"2x^2 + 2x - 24 = 0",
            {"tex": r"x^2 + x - 12 = 0", "color": LABEL_COLOR, "key": True},
        ], start_reference=s2_title)

        # Transition: clear top steps
        top_items = VGroup(s1_title, s1_txt, s1_eq1, s2_title, *eqs)
        self.play(FadeOut(top_items), run_time=T_TRANSITION)
        self.wait(0.3)

        # Step 3: Factor
        s3_title = self.show_step_title("Hapi 3: Faktorizimi")

        eqs3 = self.show_equation_chain([
            r"x^2 + x - 12 = 0",
            {"tex": r"(x - 3)(x + 4) = 0", "color": LABEL_COLOR, "key": True},
            {"tex": r"x_1 = 3 \qquad x_2 = -4", "color": ANSWER_COLOR, "font_size": CALC_SIZE + 2, "key": True},
        ], start_reference=s3_title)

        # Step 4: Find y
        s4_title = self.show_step_title("Hapi 4: Gjejmë y", reference=eqs3[-1], buff=0.5)

        y_eqs = self.show_equation_chain([
            r"y_1 = 3 + 1 = 4",
            r"y_2 = -4 + 1 = -3",
        ], start_reference=s4_title)
        self.wait(W_AFTER_ROUTINE)

        # Answer box
        self.show_answer_below(
            r"(3,\,4) \quad \text{dhe} \quad (-4,\,-3)",
            y_eqs[-1],
        )

    # ================================================================
    #  PART B  —  x² + y² = 25,  y = 2x − 5
    # ================================================================
    def part_b(self):
        self.show_part_header("b")
        self._show_system_problem(r"\begin{cases} x^2 + y^2 = 25 \\ y = 2x - 5 \end{cases}")

        # Graph
        graph_group = self._build_circle_line_graph(
            radius=5, line_func=lambda x: 2 * x - 5, line_range=[-1, 6],
            points=[(0, -5), (4, 3)],
            labels=["(0,\\,-5)", "(4,\\,3)"],
            axis_bound=7,
        )

        div = self.setup_split_layout(graph_group)

        # Algebra
        s1 = Text("Zëvendësojmë y = 2x − 5:", font_size=BODY_SIZE, color=BODY_TEXT_COLOR)
        s1.move_to(CALC_TOP)
        self.play(FadeIn(s1), run_time=T_STEP_TITLE)

        eqs = self.show_equation_chain([
            {"tex": r"x^2 + (2x-5)^2 = 25", "key": True},
            r"x^2 + 4x^2 - 20x + 25 = 25",
            {"tex": r"5x^2 - 20x = 0", "color": LABEL_COLOR},
            r"5x(x - 4) = 0",
            {"tex": r"x_1 = 0 \qquad x_2 = 4", "color": ANSWER_COLOR, "font_size": CALC_SIZE + 2, "key": True},
        ], start_reference=s1)

        # Transition
        self.play(FadeOut(VGroup(s1, *eqs)), run_time=T_TRANSITION)

        # Find y
        y_title = self.show_step_title("Gjejmë y:")
        y_eqs = self.show_equation_chain([
            r"y_1 = 2(0) - 5 = -5",
            r"y_2 = 2(4) - 5 = 3",
        ], start_reference=y_title)
        self.wait(W_AFTER_ROUTINE)

        self.show_answer_below(
            r"(0,\,-5) \quad \text{dhe} \quad (4,\,3)",
            y_eqs[-1],
        )

    # ================================================================
    #  PART C  —  x² + y² = 100,  y = −3/4 x
    # ================================================================
    def part_c(self):
        self.show_part_header("c")
        self._show_system_problem(r"\begin{cases} x^2 + y^2 = 100 \\ y = -\dfrac{3}{4}\,x \end{cases}")

        graph_group = self._build_circle_line_graph(
            radius=10, line_func=lambda x: -0.75 * x, line_range=[-11, 11],
            points=[(8, -6), (-8, 6)],
            labels=["(8,\\,-6)", "(-8,\\,6)"],
            axis_bound=12, axis_step=4,
        )

        div = self.setup_split_layout(graph_group)

        # Algebra (condensed)
        s1 = Text("Zëvendësojmë y = −3/4 x:", font_size=BODY_SIZE, color=BODY_TEXT_COLOR)
        s1.move_to(CALC_TOP)
        self.play(FadeIn(s1), run_time=T_STEP_TITLE)

        eqs = self.show_equation_chain([
            {"tex": r"x^2 + \frac{9}{16}x^2 = 100", "key": True},
            r"\frac{25}{16}x^2 = 100",
            {"tex": r"x^2 = 64", "color": LABEL_COLOR},
            {"tex": r"x = \pm 8", "color": ANSWER_COLOR, "font_size": CALC_SIZE + 2, "key": True},
        ], start_reference=s1)

        # Find y & answer
        y_txt = MathTex(
            r"y_1 = -\frac{3}{4}(8) = -6 \qquad y_2 = -\frac{3}{4}(-8) = 6",
            font_size=CALC_SIZE - 2,
        )
        y_txt.next_to(eqs[-1], DOWN, buff=0.4)
        self.play(Write(y_txt), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        self.show_answer_below(
            r"(8,\,-6) \quad \text{dhe} \quad (-8,\,6)",
            y_txt,
            buff=0.4,
        )

    # ================================================================
    #  PART D  —  x² + y² = 169,  y = 3x − 3
    # ================================================================
    def part_d(self):
        self.show_part_header("d")
        self._show_system_problem(r"\begin{cases} x^2 + y^2 = 169 \\ y = 3x - 3 \end{cases}")

        graph_group = self._build_circle_line_graph(
            radius=13, line_func=lambda x: 3 * x - 3, line_range=[-4.5, 8.5],
            points=[(5, 12), (-3.2, -12.6)],
            labels=["(5,\\,12)", "(-3{,}2;\\,-12{,}6)"],
            axis_bound=15, axis_step=5,
        )

        div = self.setup_split_layout(graph_group)

        # Quick algebra
        eqs = self.show_equation_chain([
            {"tex": r"x^2 + (3x-3)^2 = 169", "key": True},
            r"10x^2 - 18x - 160 = 0",
            {"tex": r"5x^2 - 9x - 80 = 0", "color": LABEL_COLOR},
            {"tex": r"x_1 = 5 \qquad x_2 = -3{,}2", "color": ANSWER_COLOR, "font_size": CALC_SIZE + 2, "key": True},
        ], start_position=CALC_TOP)

        self.show_answer_below(
            r"(5,\,12) \quad \text{dhe} \quad (-3{,}2;\;-12{,}6)",
            eqs[-1],
        )

    # ================================================================
    #  PART E  —  x² + y² = 36,  y = x − 2
    # ================================================================
    def part_e(self):
        self.show_part_header("e")
        self._show_system_problem(r"\begin{cases} x^2 + y^2 = 36 \\ y = x - 2 \end{cases}")

        x1, y1 = 5.125, 3.125
        x2, y2 = -3.125, -5.125

        graph_group = self._build_circle_line_graph(
            radius=6, line_func=lambda x: x - 2, line_range=[-5, 7],
            points=[(x1, y1), (x2, y2)],
            labels=["(5{,}1;\\,3{,}1)", "(-3{,}1;\\,-5{,}1)"],
            axis_bound=8, axis_step=2,
        )

        div = self.setup_split_layout(graph_group)

        eqs = self.show_equation_chain([
            {"tex": r"x^2 + (x-2)^2 = 36", "key": True},
            r"2x^2 - 4x - 32 = 0",
            {"tex": r"x^2 - 2x - 16 = 0", "color": LABEL_COLOR},
            r"x = \frac{2 \pm \sqrt{68}}{2} = 1 \pm \sqrt{17}",
            {"tex": r"x_1 \approx 5{,}12 \qquad x_2 \approx -3{,}12", "color": ANSWER_COLOR, "key": True},
        ], start_position=CALC_TOP)

        self.show_answer_below(
            r"(5{,}12;\;3{,}12) \quad \text{dhe} \quad (-3{,}12;\;-5{,}12)",
            eqs[-1],
            buff=0.4,
        )

    # ================================================================
    #  PART F  —  x² + y² = 4,  y = 2x + 1
    # ================================================================
    def part_f(self):
        self.show_part_header("f")
        self._show_system_problem(r"\begin{cases} x^2 + y^2 = 4 \\ y = 2x + 1 \end{cases}")

        x1, y1 = 0.47, 1.94
        x2, y2 = -1.27, -1.54

        graph_group = self._build_circle_line_graph(
            radius=2, line_func=lambda x: 2 * x + 1, line_range=[-2.5, 1.8],
            points=[(x1, y1), (x2, y2)],
            labels=["(0{,}47;\\,1{,}94)", "(-1{,}27;\\,-1{,}54)"],
            axis_bound=4, axis_step=1,
        )

        div = self.setup_split_layout(graph_group)

        eqs = self.show_equation_chain([
            {"tex": r"x^2 + (2x+1)^2 = 4", "key": True},
            {"tex": r"5x^2 + 4x - 3 = 0", "color": LABEL_COLOR},
            r"x = \frac{-4 \pm \sqrt{76}}{10}",
            {"tex": r"x_1 \approx 0{,}47 \qquad x_2 \approx -1{,}27", "color": ANSWER_COLOR, "key": True},
        ], start_position=CALC_TOP)

        self.show_answer_below(
            r"(0{,}47;\;1{,}94) \quad \text{dhe} \quad (-1{,}27;\;-1{,}54)",
            eqs[-1],
            buff=0.4,
        )

    # ================================================================
    #  FINAL SUMMARY
    # ================================================================
    def final_summary(self):
        self.show_summary_table(
            "Përmbledhje e përgjigjeve",
            [
                r"\text{a)}\quad (3,\,4) \;\text{dhe}\; (-4,\,-3)",
                r"\text{b)}\quad (0,\,-5) \;\text{dhe}\; (4,\,3)",
                r"\text{c)}\quad (8,\,-6) \;\text{dhe}\; (-8,\,6)",
                r"\text{d)}\quad (5,\,12) \;\text{dhe}\; (-3{,}2;\,-12{,}6)",
                r"\text{e)}\quad (5{,}12;\,3{,}12) \;\text{dhe}\; (-3{,}12;\,-5{,}12)",
                r"\text{f)}\quad (0{,}47;\,1{,}94) \;\text{dhe}\; (-1{,}27;\,-1{,}54)",
            ],
        )
