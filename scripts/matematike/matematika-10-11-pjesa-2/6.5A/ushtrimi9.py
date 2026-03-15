import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from manim import *
import numpy as np
from components import ExerciseScene
from style_guide import (
    make_divider, make_answer_box, fade_all,
    STEP_TITLE_COLOR, BODY_TEXT_COLOR, LABEL_COLOR,
    ANSWER_COLOR, SHAPE_COLOR, AUX_COLOR, HIGHLIGHT_COLOR,
    PART_HEADER_SIZE, STEP_TITLE_SIZE,
    BODY_SIZE, PROBLEM_MATH_SIZE, CALC_SIZE, ANSWER_SIZE,
    T_STEP_TITLE, T_BODY_FADE, T_KEY_EQUATION, T_ROUTINE_EQUATION,
    T_SHAPE_CREATE, T_DOT_FADE, T_LAYOUT_SHIFT, T_TRANSITION,
    W_AFTER_KEY, W_AFTER_ROUTINE, W_AFTER_ANSWER, W_PROBLEM,
    CALC_TOP, PX,
)


class Ushtrimi9(ExerciseScene):
    """
    Ushtrimi 9 — Njesia 6.5A
    Matematika 10-11: Pjesa II

    Sisteme ekuacionesh (rreth + drejtez).
    Visual storytelling: intersection dots appear only when algebra discovers them.
    _transfer_value flies results from equations to the graph.
    """

    exercise_number = 9
    unit = "6.5A"
    parts = ["a", "b", "c", "d", "e", "f"]

    # ── Right-panel alignment helpers (all centered at x = PX) ──

    def _title(self, text, ref=None, y_pos=None, buff=0.5):
        t = MathTex(
            r"\text{" + text + r"}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        if y_pos is not None:
            t.move_to(np.array([PX, y_pos, 0]))
        elif ref is not None:
            t.next_to(ref, DOWN, buff=buff)
            t.set_x(PX)
        self.play(FadeIn(t), run_time=T_STEP_TITLE)
        return t

    def _text(self, lines, ref, buff=0.25):
        parts = [MathTex(l, font_size=BODY_SIZE, color=BODY_TEXT_COLOR) for l in lines]
        g = VGroup(*parts).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        g.next_to(ref, DOWN, buff=buff)
        g.set_x(PX)
        self.play(FadeIn(g), run_time=T_BODY_FADE)
        return g

    def _eq(self, tex, ref, buff=0.25, color=None, fs=None, key=False):
        eq = MathTex(tex, font_size=fs or CALC_SIZE)
        if color:
            eq.set_color(color)
        eq.next_to(ref, DOWN, buff=buff)
        eq.set_x(PX)
        self.play(Write(eq), run_time=T_KEY_EQUATION if key else T_ROUTINE_EQUATION)
        self.wait(W_AFTER_KEY if key else 0.6)
        return eq

    def _transfer_value(self, source_eq, target_mob):
        """Animate a value 'flying' from the right panel to the figure."""
        ghost = source_eq.copy()
        self.play(
            ghost.animate.move_to(target_mob).scale(0.65).set_opacity(0),
            FadeIn(target_mob),
            run_time=0.8,
        )
        self.remove(ghost)

    # ================================================================
    #  GRAPH BUILDER — circle + line, NO dots yet (dots come from algebra)
    # ================================================================
    def _build_graph(self, radius, line_func, line_range,
                     axis_bound, axis_step=None,
                     circle_tex=None, line_tex=None):
        """
        Build axes with circle and line. Returns (axes, graph_group).
        Intersection dots are NOT added — they appear during algebra.
        """
        axes = self.create_axes(axis_bound, axis_bound, step=axis_step)
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")

        circle = self.plot_circle(axes, radius)
        line = axes.plot(line_func, x_range=line_range,
                         color=AUX_COLOR, stroke_width=2.5)

        graph_group = VGroup(axes, axes_labels, circle, line)

        # Optional equation labels on the graph
        if circle_tex:
            c_lbl = MathTex(circle_tex, font_size=18, color=SHAPE_COLOR)
            c_lbl.next_to(circle, UR, buff=0.08).shift(LEFT * 0.4 + DOWN * 0.2)
            graph_group.add(c_lbl)
        if line_tex:
            l_lbl = MathTex(line_tex, font_size=18, color=AUX_COLOR)
            l_lbl.next_to(line.point_from_proportion(0.85), UR, buff=0.12)
            graph_group.add(l_lbl)

        # Animate
        self.play(Create(axes), FadeIn(axes_labels), run_time=T_SHAPE_CREATE)
        self.play(Create(circle), Create(line), run_time=T_SHAPE_CREATE)
        if circle_tex:
            self.play(FadeIn(graph_group[-2] if line_tex else graph_group[-1]),
                      run_time=0.4)
        if line_tex:
            self.play(FadeIn(graph_group[-1]), run_time=0.4)
        self.wait(W_AFTER_ROUTINE)

        return axes, graph_group

    def _show_system(self, system_tex):
        """Show system of equations as problem statement."""
        prob_title = MathTex(
            r"\text{Sistemi:}",
            font_size=STEP_TITLE_SIZE + 2, color=STEP_TITLE_COLOR,
        )
        prob_eq = MathTex(system_tex, font_size=PROBLEM_MATH_SIZE + 4)
        self.show_problem(prob_title, prob_eq)

    # ================================================================
    #  PART A  —  x^2 + y^2 = 25,  y = x + 1
    #  FULL detailed walkthrough
    # ================================================================
    def part_a(self):
        self.show_part_header("a")

        # Problem statement
        self._show_system(
            r"\begin{cases} x^2 + y^2 = 25 \\ y = x + 1 \end{cases}"
        )

        # Build graph (no intersection dots yet)
        axes, graph_group = self._build_graph(
            radius=5,
            line_func=lambda x: x + 1,
            line_range=[-6, 5.5],
            axis_bound=7,
            circle_tex=r"x^2+y^2=25",
            line_tex=r"y=x+1",
        )

        # Shift left for split layout
        div = self.setup_split_layout(graph_group)
        self.wait(0.5)

        # ── Step 1: Substitution ──
        s1t = self._title("Hapi 1: Zevendesimi", y_pos=3.2)

        s1txt = self._text([
            r"\text{Zevendesojme } y = x + 1",
            r"\text{ne ekuacionin e rrethit:}",
        ], s1t)
        self.wait(1.5)

        # Flash the line on the graph when referencing it
        line_mob = graph_group[3]  # line is 4th element
        self.play(Indicate(line_mob, color=YELLOW, scale_factor=1.05), run_time=0.5)

        s1eq = self._eq(r"x^2 + (x+1)^2 = 25", s1txt, key=True)

        # ── Step 2: Expand & simplify ──
        s2t = self._title("Hapi 2: Thjeshtimi", ref=s1eq)

        s2eq1 = self._eq(r"x^2 + x^2 + 2x + 1 = 25", s2t)
        s2eq2 = self._eq(r"2x^2 + 2x - 24 = 0", s2eq1)
        s2eq3 = self._eq(r"x^2 + x - 12 = 0", s2eq2, color=LABEL_COLOR, key=True)
        self.wait(1.5)

        # ── Clear right panel for next steps ──
        calc1 = VGroup(s1t, s1txt, s1eq, s2t, s2eq1, s2eq2, s2eq3)
        self.play(FadeOut(calc1), run_time=T_TRANSITION)
        self.wait(0.5)

        # ── Step 3: Factor ──
        s3t = self._title("Hapi 3: Faktorizimi", y_pos=3.2)

        s3eq1 = self._eq(r"x^2 + x - 12 = 0", s3t)
        s3eq2 = self._eq(r"(x - 3)(x + 4) = 0", s3eq1, color=LABEL_COLOR, key=True)
        s3eq3 = self._eq(
            r"x_1 = 3 \qquad x_2 = -4",
            s3eq2, color=ANSWER_COLOR, fs=CALC_SIZE + 2, key=True,
        )
        self.wait(1.5)

        # ── Step 4: Find y values ──
        s4t = self._title("Hapi 4: Gjejme y", ref=s3eq3)

        s4eq1 = self._eq(r"y_1 = 3 + 1 = 4", s4t)

        # Flash the line equation on graph as reminder
        self.play(Indicate(line_mob, color=YELLOW, scale_factor=1.05), run_time=0.4)

        # FIRST INTERSECTION: transfer dot (3, 4) to graph
        dot1, lbl1 = self.mark_point(axes, 3, 4, "(3,\\,4)",
                                      color=LABEL_COLOR, direction=UR)
        pt1_group = VGroup(dot1, lbl1)
        # Shift to match graph position (graph was shifted left)
        self._transfer_value(s4eq1, pt1_group)
        self.play(Indicate(dot1, color=YELLOW, scale_factor=1.5), run_time=0.5)
        self.wait(1.0)

        s4eq2 = self._eq(r"y_2 = -4 + 1 = -3", s4eq1)

        # SECOND INTERSECTION: transfer dot (-4, -3) to graph
        dot2, lbl2 = self.mark_point(axes, -4, -3, "(-4,\\,-3)",
                                      color=HIGHLIGHT_COLOR, direction=DL)
        pt2_group = VGroup(dot2, lbl2)
        self._transfer_value(s4eq2, pt2_group)
        self.play(Indicate(dot2, color=YELLOW, scale_factor=1.5), run_time=0.5)
        self.wait(1.5)

        # ── Clear right panel for answer ──
        calc2 = VGroup(s3t, s3eq1, s3eq2, s3eq3, s4t, s4eq1, s4eq2)
        self.play(FadeOut(calc2), run_time=T_TRANSITION)
        self.wait(0.5)

        # ── Answer ──
        ans_title = self._title("Pergjigja:", y_pos=1.0)
        ans_eq = MathTex(
            r"(3,\,4) \quad \text{dhe} \quad (-4,\,-3)",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        ans_eq.next_to(ans_title, DOWN, buff=0.4)
        ans_eq.set_x(PX)
        box = make_answer_box(ans_eq)

        self.play(Write(ans_eq), run_time=T_KEY_EQUATION)
        self.play(Create(box), run_time=0.5)

        # Flash both dots on graph to reinforce visual connection
        self.play(
            Indicate(dot1, color=YELLOW, scale_factor=1.5),
            Indicate(dot2, color=YELLOW, scale_factor=1.5),
            run_time=0.6,
        )
        self.wait(W_AFTER_ANSWER)

    # ================================================================
    #  PART B  —  x^2 + y^2 = 25,  y = 2x - 5
    #  MODERATE detail
    # ================================================================
    def part_b(self):
        self.show_part_header("b")

        self._show_system(
            r"\begin{cases} x^2 + y^2 = 25 \\ y = 2x - 5 \end{cases}"
        )

        # Build graph (no dots)
        axes, graph_group = self._build_graph(
            radius=5,
            line_func=lambda x: 2 * x - 5,
            line_range=[-1, 6],
            axis_bound=7,
            circle_tex=r"x^2+y^2=25",
            line_tex=r"y=2x-5",
        )

        div = self.setup_split_layout(graph_group)
        self.wait(0.5)

        line_mob = graph_group[3]

        # ── Substitution + simplification ──
        s1t = self._title("Zevendesimi dhe thjeshtimi", y_pos=3.2)

        s1txt = self._text([
            r"\text{Zevendesojme } y = 2x - 5\text{:}",
        ], s1t)
        self.wait(1.0)

        self.play(Indicate(line_mob, color=YELLOW, scale_factor=1.05), run_time=0.4)

        s1eq1 = self._eq(r"x^2 + (2x-5)^2 = 25", s1txt, key=True)
        s1eq2 = self._eq(r"x^2 + 4x^2 - 20x + 25 = 25", s1eq1)
        s1eq3 = self._eq(r"5x^2 - 20x = 0", s1eq2, color=LABEL_COLOR)
        s1eq4 = self._eq(r"5x(x - 4) = 0", s1eq3)
        s1eq5 = self._eq(
            r"x_1 = 0 \qquad x_2 = 4",
            s1eq4, color=ANSWER_COLOR, fs=CALC_SIZE + 2, key=True,
        )
        self.wait(1.5)

        # ── Clear right panel ──
        calc1 = VGroup(s1t, s1txt, s1eq1, s1eq2, s1eq3, s1eq4, s1eq5)
        self.play(FadeOut(calc1), run_time=T_TRANSITION)
        self.wait(0.5)

        # ── Find y + transfer dots ──
        s2t = self._title("Gjejme y:", y_pos=3.2)

        s2eq1 = self._eq(r"y_1 = 2(0) - 5 = -5", s2t)

        # Transfer first dot
        dot1, lbl1 = self.mark_point(axes, 0, -5, "(0,\\,-5)",
                                      color=LABEL_COLOR, direction=DL)
        self._transfer_value(s2eq1, VGroup(dot1, lbl1))
        self.play(Indicate(dot1, color=YELLOW, scale_factor=1.5), run_time=0.5)
        self.wait(0.8)

        s2eq2 = self._eq(r"y_2 = 2(4) - 5 = 3", s2eq1)

        # Transfer second dot
        dot2, lbl2 = self.mark_point(axes, 4, 3, "(4,\\,3)",
                                      color=HIGHLIGHT_COLOR, direction=UR)
        self._transfer_value(s2eq2, VGroup(dot2, lbl2))
        self.play(Indicate(dot2, color=YELLOW, scale_factor=1.5), run_time=0.5)
        self.wait(1.5)

        # ── Clear + answer ──
        calc2 = VGroup(s2t, s2eq1, s2eq2)
        self.play(FadeOut(calc2), run_time=T_TRANSITION)
        self.wait(0.3)

        ans_title = self._title("Pergjigja:", y_pos=1.0)
        ans_eq = MathTex(
            r"(0,\,-5) \quad \text{dhe} \quad (4,\,3)",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        ans_eq.next_to(ans_title, DOWN, buff=0.4)
        ans_eq.set_x(PX)
        box = make_answer_box(ans_eq)

        self.play(Write(ans_eq), run_time=T_KEY_EQUATION)
        self.play(Create(box), run_time=0.5)
        self.play(
            Indicate(dot1, color=YELLOW, scale_factor=1.5),
            Indicate(dot2, color=YELLOW, scale_factor=1.5),
            run_time=0.6,
        )
        self.wait(W_AFTER_ANSWER)

    # ================================================================
    #  PART C  —  x^2 + y^2 = 100,  y = -(3/4)x
    #  MODERATE detail
    # ================================================================
    def part_c(self):
        self.show_part_header("c")

        self._show_system(
            r"\begin{cases} x^2 + y^2 = 100 \\ y = -\dfrac{3}{4}\,x \end{cases}"
        )

        axes, graph_group = self._build_graph(
            radius=10,
            line_func=lambda x: -0.75 * x,
            line_range=[-11, 11],
            axis_bound=12, axis_step=4,
            circle_tex=r"x^2+y^2=100",
            line_tex=r"y=-\tfrac{3}{4}x",
        )

        div = self.setup_split_layout(graph_group)
        self.wait(0.5)

        line_mob = graph_group[3]

        # ── Algebra ──
        s1t = self._title("Zevendesimi dhe thjeshtimi", y_pos=3.2)

        s1txt = self._text([
            r"\text{Zevendesojme } y = -\tfrac{3}{4}\,x\text{:}",
        ], s1t)
        self.wait(1.0)

        self.play(Indicate(line_mob, color=YELLOW, scale_factor=1.05), run_time=0.4)

        s1eq1 = self._eq(r"x^2 + \frac{9}{16}x^2 = 100", s1txt, key=True)
        s1eq2 = self._eq(r"\frac{25}{16}x^2 = 100", s1eq1)
        s1eq3 = self._eq(r"x^2 = 64", s1eq2, color=LABEL_COLOR)
        s1eq4 = self._eq(
            r"x = \pm 8",
            s1eq3, color=ANSWER_COLOR, fs=CALC_SIZE + 2, key=True,
        )
        self.wait(1.5)

        # ── Clear right panel ──
        calc1 = VGroup(s1t, s1txt, s1eq1, s1eq2, s1eq3, s1eq4)
        self.play(FadeOut(calc1), run_time=T_TRANSITION)
        self.wait(0.5)

        # ── Find y + transfer dots ──
        s2t = self._title("Gjejme y:", y_pos=3.2)

        s2eq1 = self._eq(r"y_1 = -\frac{3}{4}(8) = -6", s2t)

        dot1, lbl1 = self.mark_point(axes, 8, -6, "(8,\\,-6)",
                                      color=LABEL_COLOR, direction=DR)
        self._transfer_value(s2eq1, VGroup(dot1, lbl1))
        self.play(Indicate(dot1, color=YELLOW, scale_factor=1.5), run_time=0.5)
        self.wait(0.8)

        s2eq2 = self._eq(r"y_2 = -\frac{3}{4}(-8) = 6", s2eq1)

        dot2, lbl2 = self.mark_point(axes, -8, 6, "(-8,\\,6)",
                                      color=HIGHLIGHT_COLOR, direction=UL)
        self._transfer_value(s2eq2, VGroup(dot2, lbl2))
        self.play(Indicate(dot2, color=YELLOW, scale_factor=1.5), run_time=0.5)
        self.wait(1.5)

        # ── Clear + answer ──
        calc2 = VGroup(s2t, s2eq1, s2eq2)
        self.play(FadeOut(calc2), run_time=T_TRANSITION)
        self.wait(0.3)

        ans_title = self._title("Pergjigja:", y_pos=1.0)
        ans_eq = MathTex(
            r"(8,\,-6) \quad \text{dhe} \quad (-8,\,6)",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        ans_eq.next_to(ans_title, DOWN, buff=0.4)
        ans_eq.set_x(PX)
        box = make_answer_box(ans_eq)

        self.play(Write(ans_eq), run_time=T_KEY_EQUATION)
        self.play(Create(box), run_time=0.5)
        self.play(
            Indicate(dot1, color=YELLOW, scale_factor=1.5),
            Indicate(dot2, color=YELLOW, scale_factor=1.5),
            run_time=0.6,
        )
        self.wait(W_AFTER_ANSWER)

    # ================================================================
    #  PART D  —  x^2 + y^2 = 169,  y = 3x - 3
    #  CONDENSED: graph + key quadratic + answer + dots
    # ================================================================
    def part_d(self):
        self.show_part_header("d")

        self._show_system(
            r"\begin{cases} x^2 + y^2 = 169 \\ y = 3x - 3 \end{cases}"
        )

        axes, graph_group = self._build_graph(
            radius=13,
            line_func=lambda x: 3 * x - 3,
            line_range=[-4.5, 8.5],
            axis_bound=15, axis_step=5,
            circle_tex=r"x^2+y^2=169",
            line_tex=r"y=3x-3",
        )

        div = self.setup_split_layout(graph_group)
        self.wait(0.5)

        line_mob = graph_group[3]

        # ── Condensed algebra ──
        s1t = self._title("Zevendesimi:", y_pos=3.2)

        self.play(Indicate(line_mob, color=YELLOW, scale_factor=1.05), run_time=0.4)

        s1eq1 = self._eq(r"x^2 + (3x-3)^2 = 169", s1t, key=True)
        s1eq2 = self._eq(r"10x^2 - 18x - 160 = 0", s1eq1)
        s1eq3 = self._eq(r"5x^2 - 9x - 80 = 0", s1eq2, color=LABEL_COLOR, key=True)
        s1eq4 = self._eq(
            r"x_1 = 5 \qquad x_2 = -3{,}2",
            s1eq3, color=ANSWER_COLOR, fs=CALC_SIZE + 2, key=True,
        )
        self.wait(1.0)

        # Transfer first dot immediately
        dot1, lbl1 = self.mark_point(axes, 5, 12, "(5,\\,12)",
                                      color=LABEL_COLOR, direction=UR)
        self._transfer_value(s1eq4, VGroup(dot1, lbl1))
        self.wait(0.5)

        # ── Clear + find y ──
        calc1 = VGroup(s1t, s1eq1, s1eq2, s1eq3, s1eq4)
        self.play(FadeOut(calc1), run_time=T_TRANSITION)
        self.wait(0.3)

        s2t = self._title("Gjejme y:", y_pos=3.2)

        s2eq1 = self._eq(r"y_1 = 3(5) - 3 = 12", s2t)
        s2eq2 = self._eq(r"y_2 = 3(-3{,}2) - 3 = -12{,}6", s2eq1)

        # Transfer second dot
        dot2, lbl2 = self.mark_point(axes, -3.2, -12.6, "(-3{,}2;\\,-12{,}6)",
                                      color=HIGHLIGHT_COLOR, direction=DL,
                                      font_size=20)
        self._transfer_value(s2eq2, VGroup(dot2, lbl2))
        self.play(Indicate(dot2, color=YELLOW, scale_factor=1.5), run_time=0.5)
        self.wait(1.0)

        # ── Clear + answer ──
        calc2 = VGroup(s2t, s2eq1, s2eq2)
        self.play(FadeOut(calc2), run_time=T_TRANSITION)
        self.wait(0.3)

        ans_title = self._title("Pergjigja:", y_pos=1.0)
        ans_eq = MathTex(
            r"(5,\,12) \quad \text{dhe} \quad (-3{,}2;\;-12{,}6)",
            font_size=ANSWER_SIZE - 2, color=ANSWER_COLOR,
        )
        ans_eq.next_to(ans_title, DOWN, buff=0.4)
        ans_eq.set_x(PX)
        box = make_answer_box(ans_eq)

        self.play(Write(ans_eq), run_time=T_KEY_EQUATION)
        self.play(Create(box), run_time=0.5)
        self.play(
            Indicate(dot1, color=YELLOW, scale_factor=1.5),
            Indicate(dot2, color=YELLOW, scale_factor=1.5),
            run_time=0.6,
        )
        self.wait(W_AFTER_ANSWER)

    # ================================================================
    #  PART E  —  x^2 + y^2 = 36,  y = x - 2
    #  QUICK: graph + key quadratic + answer
    # ================================================================
    def part_e(self):
        self.show_part_header("e")

        self._show_system(
            r"\begin{cases} x^2 + y^2 = 36 \\ y = x - 2 \end{cases}"
        )

        axes, graph_group = self._build_graph(
            radius=6,
            line_func=lambda x: x - 2,
            line_range=[-5, 7],
            axis_bound=8, axis_step=2,
            circle_tex=r"x^2+y^2=36",
            line_tex=r"y=x-2",
        )

        div = self.setup_split_layout(graph_group)
        self.wait(0.5)

        line_mob = graph_group[3]

        # ── Quick algebra ──
        s1t = self._title("Zevendesimi:", y_pos=3.2)

        self.play(Indicate(line_mob, color=YELLOW, scale_factor=1.05), run_time=0.4)

        s1eq1 = self._eq(r"x^2 + (x-2)^2 = 36", s1t, key=True)
        s1eq2 = self._eq(r"2x^2 - 4x - 32 = 0", s1eq1)
        s1eq3 = self._eq(r"x^2 - 2x - 16 = 0", s1eq2, color=LABEL_COLOR)
        s1eq4 = self._eq(
            r"x = 1 \pm \sqrt{17}",
            s1eq3, color=ANSWER_COLOR, fs=CALC_SIZE + 2, key=True,
        )
        self.wait(1.0)

        # ── Clear + y values + dots ──
        calc1 = VGroup(s1t, s1eq1, s1eq2, s1eq3, s1eq4)
        self.play(FadeOut(calc1), run_time=T_TRANSITION)
        self.wait(0.3)

        x1 = 1 + np.sqrt(17)
        y1 = x1 - 2
        x2 = 1 - np.sqrt(17)
        y2 = x2 - 2

        s2t = self._title("Gjejme y:", y_pos=3.2)

        s2eq1 = self._eq(r"y_1 = 5{,}12 - 2 = 3{,}12", s2t)

        dot1, lbl1 = self.mark_point(axes, x1, y1, "(5{,}12;\\,3{,}12)",
                                      color=LABEL_COLOR, direction=UR,
                                      font_size=20)
        self._transfer_value(s2eq1, VGroup(dot1, lbl1))
        self.wait(0.5)

        s2eq2 = self._eq(r"y_2 = -3{,}12 - 2 = -5{,}12", s2eq1)

        dot2, lbl2 = self.mark_point(axes, x2, y2, "(-3{,}12;\\,-5{,}12)",
                                      color=HIGHLIGHT_COLOR, direction=DL,
                                      font_size=20)
        self._transfer_value(s2eq2, VGroup(dot2, lbl2))
        self.wait(1.0)

        # ── Clear + answer ──
        calc2 = VGroup(s2t, s2eq1, s2eq2)
        self.play(FadeOut(calc2), run_time=T_TRANSITION)
        self.wait(0.3)

        ans_title = self._title("Pergjigja:", y_pos=1.0)
        ans_eq = MathTex(
            r"(5{,}12;\;3{,}12) \quad \text{dhe} \quad (-3{,}12;\;-5{,}12)",
            font_size=ANSWER_SIZE - 4, color=ANSWER_COLOR,
        )
        ans_eq.next_to(ans_title, DOWN, buff=0.4)
        ans_eq.set_x(PX)
        box = make_answer_box(ans_eq)

        self.play(Write(ans_eq), run_time=T_KEY_EQUATION)
        self.play(Create(box), run_time=0.5)
        self.play(
            Indicate(dot1, color=YELLOW, scale_factor=1.5),
            Indicate(dot2, color=YELLOW, scale_factor=1.5),
            run_time=0.6,
        )
        self.wait(W_AFTER_ANSWER)

    # ================================================================
    #  PART F  —  x^2 + y^2 = 4,  y = 2x + 1
    #  QUICK: graph + key quadratic + answer
    # ================================================================
    def part_f(self):
        self.show_part_header("f")

        self._show_system(
            r"\begin{cases} x^2 + y^2 = 4 \\ y = 2x + 1 \end{cases}"
        )

        axes, graph_group = self._build_graph(
            radius=2,
            line_func=lambda x: 2 * x + 1,
            line_range=[-2.5, 1.8],
            axis_bound=4, axis_step=1,
            circle_tex=r"x^2+y^2=4",
            line_tex=r"y=2x+1",
        )

        div = self.setup_split_layout(graph_group)
        self.wait(0.5)

        line_mob = graph_group[3]

        # ── Quick algebra ──
        s1t = self._title("Zevendesimi:", y_pos=3.2)

        self.play(Indicate(line_mob, color=YELLOW, scale_factor=1.05), run_time=0.4)

        s1eq1 = self._eq(r"x^2 + (2x+1)^2 = 4", s1t, key=True)
        s1eq2 = self._eq(r"5x^2 + 4x - 3 = 0", s1eq1, color=LABEL_COLOR)
        s1eq3 = self._eq(
            r"x = \frac{-4 \pm \sqrt{76}}{10}",
            s1eq2, color=ANSWER_COLOR, fs=CALC_SIZE + 2, key=True,
        )
        self.wait(1.0)

        # ── Clear + y values + dots ──
        calc1 = VGroup(s1t, s1eq1, s1eq2, s1eq3)
        self.play(FadeOut(calc1), run_time=T_TRANSITION)
        self.wait(0.3)

        x1_val = (-4 + np.sqrt(76)) / 10
        y1_val = 2 * x1_val + 1
        x2_val = (-4 - np.sqrt(76)) / 10
        y2_val = 2 * x2_val + 1

        s2t = self._title("Gjejme y:", y_pos=3.2)

        s2eq1 = self._eq(r"y_1 = 2(0{,}47) + 1 = 1{,}94", s2t)

        dot1, lbl1 = self.mark_point(axes, x1_val, y1_val,
                                      "(0{,}47;\\,1{,}94)",
                                      color=LABEL_COLOR, direction=UR,
                                      font_size=20)
        self._transfer_value(s2eq1, VGroup(dot1, lbl1))
        self.wait(0.5)

        s2eq2 = self._eq(r"y_2 = 2(-1{,}27) + 1 = -1{,}54", s2eq1)

        dot2, lbl2 = self.mark_point(axes, x2_val, y2_val,
                                      "(-1{,}27;\\,-1{,}54)",
                                      color=HIGHLIGHT_COLOR, direction=DL,
                                      font_size=20)
        self._transfer_value(s2eq2, VGroup(dot2, lbl2))
        self.wait(1.0)

        # ── Clear + answer ──
        calc2 = VGroup(s2t, s2eq1, s2eq2)
        self.play(FadeOut(calc2), run_time=T_TRANSITION)
        self.wait(0.3)

        ans_title = self._title("Pergjigja:", y_pos=1.0)
        ans_eq = MathTex(
            r"(0{,}47;\;1{,}94) \quad \text{dhe} \quad (-1{,}27;\;-1{,}54)",
            font_size=ANSWER_SIZE - 4, color=ANSWER_COLOR,
        )
        ans_eq.next_to(ans_title, DOWN, buff=0.4)
        ans_eq.set_x(PX)
        box = make_answer_box(ans_eq)

        self.play(Write(ans_eq), run_time=T_KEY_EQUATION)
        self.play(Create(box), run_time=0.5)
        self.play(
            Indicate(dot1, color=YELLOW, scale_factor=1.5),
            Indicate(dot2, color=YELLOW, scale_factor=1.5),
            run_time=0.6,
        )
        self.wait(W_AFTER_ANSWER)

    # ================================================================
    #  FINAL SUMMARY
    # ================================================================
    def final_summary(self):
        self.show_summary_table(
            "Permbledhje e pergjigjeve",
            [
                r"\text{a)}\quad (3,\,4) \;\text{dhe}\; (-4,\,-3)",
                r"\text{b)}\quad (0,\,-5) \;\text{dhe}\; (4,\,3)",
                r"\text{c)}\quad (8,\,-6) \;\text{dhe}\; (-8,\,6)",
                r"\text{d)}\quad (5,\,12) \;\text{dhe}\; (-3{,}2;\,-12{,}6)",
                r"\text{e)}\quad (5{,}12;\,3{,}12) \;\text{dhe}\; (-3{,}12;\,-5{,}12)",
                r"\text{f)}\quad (0{,}47;\,1{,}94) \;\text{dhe}\; (-1{,}27;\,-1{,}54)",
            ],
        )
