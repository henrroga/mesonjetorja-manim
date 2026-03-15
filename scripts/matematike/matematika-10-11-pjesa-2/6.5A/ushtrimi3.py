import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from manim import *
import numpy as np
from components import ExerciseScene
from style_guide import (
    make_answer_box, make_divider, fade_all,
    STEP_TITLE_COLOR, BODY_TEXT_COLOR, LABEL_COLOR,
    ANSWER_COLOR, SHAPE_COLOR, HIGHLIGHT_COLOR, DIVIDER_COLOR,
    PART_HEADER_SIZE, STEP_TITLE_SIZE,
    BODY_SIZE, PROBLEM_MATH_SIZE, CALC_SIZE, ANSWER_SIZE,
    T_STEP_TITLE, T_BODY_FADE, T_KEY_EQUATION, T_ROUTINE_EQUATION,
    T_SHAPE_CREATE, T_LAYOUT_SHIFT, T_TRANSITION,
    W_AFTER_KEY, W_AFTER_ROUTINE, W_AFTER_ANSWER, W_PROBLEM,
    CALC_TOP, PX,
)


class Ushtrimi3(ExerciseScene):
    """
    Ushtrimi 3 -- Njesia 6.5A -- Matematika 10-11: Pjesa II

    Skiconi grafiket e rratheve dhe emertoni pikeprerjet me boshtet.
    Six circle equations centered at origin.

    Visual storytelling: no voiceover, every value transfers to the graph.
    Grade 10-11 pacing with progressive acceleration.
    """

    exercise_number = 3
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
        """Animate a value flying from the right panel to the figure."""
        ghost = source_eq.copy()
        self.play(
            ghost.animate.move_to(target_mob).scale(0.65).set_opacity(0),
            FadeIn(target_mob),
            run_time=0.8,
        )
        self.remove(ghost)

    # ── Graph builder: axes + circle on the left panel ──

    def _build_graph(self, r_val, axis_bound=None, step=None):
        """Create axes + circle centered at origin, positioned left."""
        bound = axis_bound or int(r_val + 2)
        s = step or max(1, bound // 4)
        axes = self.create_axes(bound, bound, step=s, x_length=5.5, y_length=5.5)
        axes.move_to(LEFT * 3.2)
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")
        circle = self.plot_circle(axes, r_val)
        return axes, axes_labels, circle

    # ================================================================
    #  PART A -- x^2 + y^2 = 49, r = 7
    #  FULL detail: explain circle form, radius, each intercept set
    # ================================================================
    def part_a(self):
        self.show_part_header("a")

        # --- Problem statement ---
        prob = MathTex(r"x^2 + y^2 = 49", font_size=PROBLEM_MATH_SIZE + 4)
        self.play(FadeIn(prob, shift=UP * 0.3), run_time=T_SHAPE_CREATE)
        self.wait(W_PROBLEM)
        self.play(FadeOut(prob), run_time=T_TRANSITION)
        self.wait(0.3)

        # --- Identify the circle form ---
        s1t = self._title("Njohim ekuacionin", y_pos=3.2)

        s1txt = self._text([
            r"\text{Forma e pergjithshme e rrethit}",
            r"\text{me qender ne origjine:}",
        ], s1t)
        self.wait(1.5)

        s1eq1 = self._eq(r"x^2 + y^2 = r^2", s1txt, key=True)

        s1txt2 = self._text([
            r"\text{Krahasojme me ekuacionin tone:}",
        ], s1eq1, buff=0.3)
        self.wait(1)

        s1eq2 = self._eq(r"x^2 + y^2 = 49", s1txt2)

        s1txt3 = self._text([
            r"\text{Pra:}",
        ], s1eq2, buff=0.2)

        s1eq3 = self._eq(r"r^2 = 49", s1txt3, buff=0.15)
        s1eq4 = self._eq(r"r = \sqrt{49} = 7", s1eq3, color=ANSWER_COLOR, key=True)

        # Clean right panel
        calc1 = VGroup(s1t, s1txt, s1eq1, s1txt2, s1eq2, s1txt3, s1eq3, s1eq4)
        self.play(FadeOut(calc1), run_time=T_TRANSITION)
        self.wait(0.3)

        # --- Find x-intercepts ---
        s2t = self._title("Pikeprerjet me boshtin x", y_pos=3.2)

        s2txt = self._text([
            r"\text{Per te gjetur pikeprerjet me}",
            r"\text{boshtin } x\text{, vendosim } y = 0\text{:}",
        ], s2t)
        self.wait(2)

        s2eq1 = self._eq(r"x^2 + 0^2 = 49", s2txt)
        s2eq2 = self._eq(r"x^2 = 49", s2eq1)
        s2eq3 = self._eq(r"x = \pm 7", s2eq2, color=LABEL_COLOR, key=True)

        s2pts = self._eq(
            r"(-7,\,0) \quad \text{dhe} \quad (7,\,0)",
            s2eq3, color=LABEL_COLOR, fs=28, buff=0.3,
        )
        self.wait(1.5)

        # --- Find y-intercepts ---
        # Clear x-intercept work
        calc2a = VGroup(s2t, s2txt, s2eq1, s2eq2, s2eq3, s2pts)
        self.play(FadeOut(calc2a), run_time=T_TRANSITION)
        self.wait(0.3)

        s3t = self._title("Pikeprerjet me boshtin y", y_pos=3.2)

        s3txt = self._text([
            r"\text{Per te gjetur pikeprerjet me}",
            r"\text{boshtin } y\text{, vendosim } x = 0\text{:}",
        ], s3t)
        self.wait(2)

        s3eq1 = self._eq(r"0^2 + y^2 = 49", s3txt)
        s3eq2 = self._eq(r"y^2 = 49", s3eq1)
        s3eq3 = self._eq(r"y = \pm 7", s3eq2, color=HIGHLIGHT_COLOR, key=True)

        s3pts = self._eq(
            r"(0,\,-7) \quad \text{dhe} \quad (0,\,7)",
            s3eq3, color=HIGHLIGHT_COLOR, fs=28, buff=0.3,
        )
        self.wait(1.5)

        # Clean panel
        calc2b = VGroup(s3t, s3txt, s3eq1, s3eq2, s3eq3, s3pts)
        self.play(FadeOut(calc2b), run_time=T_TRANSITION)
        self.wait(0.3)

        # --- Graph with intercepts ---
        axes, axes_labels, circle = self._build_graph(7, axis_bound=9, step=2)

        self.play(Create(axes), FadeIn(axes_labels), run_time=T_SHAPE_CREATE)
        self.play(Create(circle), run_time=T_SHAPE_CREATE)
        self.wait(1)

        # Equation label on graph
        eq_label = MathTex(r"x^2 + y^2 = 49", font_size=24, color=SHAPE_COLOR)
        eq_label.next_to(axes, UR, buff=0.2)
        eq_label.shift(DOWN * 0.5)
        self.play(FadeIn(eq_label), run_time=0.5)

        # Divider
        div = make_divider()
        self.play(FadeIn(div), run_time=0.2)

        # Right panel: show intercept results and transfer to graph
        res_t = self._title("Pikeprerjet", y_pos=3.0)

        res_x = self._eq(
            r"x\text{-boshti: } (-7,\,0),\; (7,\,0)",
            res_t, color=LABEL_COLOR, fs=28, buff=0.4,
        )

        # Mark x-intercepts on graph
        d1, l1 = self.mark_point(axes, -7, 0, r"(-7,0)", color=LABEL_COLOR,
                                  direction=DL, font_size=20)
        d2, l2 = self.mark_point(axes, 7, 0, r"(7,0)", color=LABEL_COLOR,
                                  direction=DR, font_size=20)
        self._transfer_value(res_x, VGroup(d1, l1))
        self._transfer_value(res_x, VGroup(d2, l2))
        self.wait(1)

        res_y = self._eq(
            r"y\text{-boshti: } (0,\,-7),\; (0,\,7)",
            res_x, color=HIGHLIGHT_COLOR, fs=28, buff=0.3,
        )

        # Mark y-intercepts on graph
        d3, l3 = self.mark_point(axes, 0, -7, r"(0,-7)", color=HIGHLIGHT_COLOR,
                                  direction=DL, font_size=20)
        d4, l4 = self.mark_point(axes, 0, 7, r"(0,7)", color=HIGHLIGHT_COLOR,
                                  direction=UL, font_size=20)
        self._transfer_value(res_y, VGroup(d3, l3))
        self._transfer_value(res_y, VGroup(d4, l4))
        self.wait(1)

        # Radius label
        r_label = self._eq(r"r = 7", res_y, color=ANSWER_COLOR, fs=30, key=True)

        # Radius dashed line on graph
        r_line = DashedLine(
            axes.c2p(0, 0), axes.c2p(7, 0),
            color=ANSWER_COLOR, dash_length=0.08, stroke_width=2,
        )
        r_mid = MathTex("7", font_size=20, color=ANSWER_COLOR)
        r_mid.next_to(r_line, UP, buff=0.12)
        self._transfer_value(r_label, VGroup(r_line, r_mid))

        self.wait(W_AFTER_ANSWER)

    # ================================================================
    #  PART B -- x^2 + y^2 = 64, r = 8
    #  FULL detail (same structure as a, slightly less verbose)
    # ================================================================
    def part_b(self):
        self.show_part_header("b")

        # --- Problem statement ---
        prob = MathTex(r"x^2 + y^2 = 64", font_size=PROBLEM_MATH_SIZE + 4)
        self.play(FadeIn(prob, shift=UP * 0.3), run_time=T_SHAPE_CREATE)
        self.wait(W_PROBLEM)
        self.play(FadeOut(prob), run_time=T_TRANSITION)
        self.wait(0.3)

        # --- Identify circle and radius ---
        s1t = self._title("Njohim rrrethin", y_pos=3.2)

        s1txt = self._text([
            r"\text{Forma } x^2 + y^2 = r^2",
            r"\text{me qender ne origjine.}",
        ], s1t)
        self.wait(1.5)

        s1eq1 = self._eq(r"r^2 = 64", s1txt)
        s1eq2 = self._eq(r"r = \sqrt{64} = 8", s1eq1, color=ANSWER_COLOR, key=True)
        self.wait(1)

        # Clean
        calc1 = VGroup(s1t, s1txt, s1eq1, s1eq2)
        self.play(FadeOut(calc1), run_time=T_TRANSITION)
        self.wait(0.3)

        # --- x-intercepts ---
        s2t = self._title("Pikeprerjet me boshtin x", y_pos=3.2)

        s2txt = self._text([
            r"\text{Vendosim } y = 0\text{:}",
        ], s2t)
        self.wait(1.5)

        s2eq1 = self._eq(r"x^2 + 0^2 = 64", s2txt)
        s2eq2 = self._eq(r"x^2 = 64 \implies x = \pm 8", s2eq1, color=LABEL_COLOR, key=True)

        s2pts = self._eq(
            r"(-8,\,0) \quad \text{dhe} \quad (8,\,0)",
            s2eq2, color=LABEL_COLOR, fs=28,
        )
        self.wait(1.5)

        # --- y-intercepts ---
        calc2a = VGroup(s2t, s2txt, s2eq1, s2eq2, s2pts)
        self.play(FadeOut(calc2a), run_time=T_TRANSITION)
        self.wait(0.3)

        s3t = self._title("Pikeprerjet me boshtin y", y_pos=3.2)

        s3txt = self._text([
            r"\text{Vendosim } x = 0\text{:}",
        ], s3t)
        self.wait(1.5)

        s3eq1 = self._eq(r"0^2 + y^2 = 64", s3txt)
        s3eq2 = self._eq(r"y^2 = 64 \implies y = \pm 8", s3eq1, color=HIGHLIGHT_COLOR, key=True)

        s3pts = self._eq(
            r"(0,\,-8) \quad \text{dhe} \quad (0,\,8)",
            s3eq2, color=HIGHLIGHT_COLOR, fs=28,
        )
        self.wait(1.5)

        calc2b = VGroup(s3t, s3txt, s3eq1, s3eq2, s3pts)
        self.play(FadeOut(calc2b), run_time=T_TRANSITION)
        self.wait(0.3)

        # --- Graph ---
        axes, axes_labels, circle = self._build_graph(8, axis_bound=10, step=2)

        self.play(Create(axes), FadeIn(axes_labels), run_time=T_SHAPE_CREATE)
        self.play(Create(circle), run_time=T_SHAPE_CREATE)
        self.wait(1)

        eq_label = MathTex(r"x^2 + y^2 = 64", font_size=24, color=SHAPE_COLOR)
        eq_label.next_to(axes, UR, buff=0.2).shift(DOWN * 0.5)
        self.play(FadeIn(eq_label), run_time=0.5)

        div = make_divider()
        self.play(FadeIn(div), run_time=0.2)

        res_t = self._title("Pikeprerjet", y_pos=3.0)

        res_x = self._eq(
            r"x\text{-boshti: } (-8,\,0),\; (8,\,0)",
            res_t, color=LABEL_COLOR, fs=28, buff=0.4,
        )

        d1, l1 = self.mark_point(axes, -8, 0, r"(-8,0)", color=LABEL_COLOR,
                                  direction=DL, font_size=20)
        d2, l2 = self.mark_point(axes, 8, 0, r"(8,0)", color=LABEL_COLOR,
                                  direction=DR, font_size=20)
        self._transfer_value(res_x, VGroup(d1, l1))
        self._transfer_value(res_x, VGroup(d2, l2))
        self.wait(1)

        res_y = self._eq(
            r"y\text{-boshti: } (0,\,-8),\; (0,\,8)",
            res_x, color=HIGHLIGHT_COLOR, fs=28, buff=0.3,
        )

        d3, l3 = self.mark_point(axes, 0, -8, r"(0,-8)", color=HIGHLIGHT_COLOR,
                                  direction=DL, font_size=20)
        d4, l4 = self.mark_point(axes, 0, 8, r"(0,8)", color=HIGHLIGHT_COLOR,
                                  direction=UL, font_size=20)
        self._transfer_value(res_y, VGroup(d3, l3))
        self._transfer_value(res_y, VGroup(d4, l4))
        self.wait(1)

        r_label = self._eq(r"r = 8", res_y, color=ANSWER_COLOR, fs=30, key=True)

        r_line = DashedLine(
            axes.c2p(0, 0), axes.c2p(8, 0),
            color=ANSWER_COLOR, dash_length=0.08, stroke_width=2,
        )
        r_mid = MathTex("8", font_size=20, color=ANSWER_COLOR)
        r_mid.next_to(r_line, UP, buff=0.12)
        self._transfer_value(r_label, VGroup(r_line, r_mid))

        self.wait(W_AFTER_ANSWER)

    # ================================================================
    #  PART C -- x^2 + y^2 = 2, r = sqrt(2)
    #  MODERATE: explain surd simplification
    # ================================================================
    def part_c(self):
        self.show_part_header("c")

        # --- Problem ---
        prob = MathTex(r"x^2 + y^2 = 2", font_size=PROBLEM_MATH_SIZE + 4)
        self.play(FadeIn(prob, shift=UP * 0.3), run_time=T_SHAPE_CREATE)
        self.wait(W_PROBLEM)
        self.play(FadeOut(prob), run_time=T_TRANSITION)
        self.wait(0.3)

        # --- Radius ---
        s1t = self._title("Gjejme rrezen", y_pos=3.2)

        s1txt = self._text([
            r"\text{Forma } x^2 + y^2 = r^2\text{:}",
        ], s1t)
        self.wait(1)

        s1eq1 = self._eq(r"r^2 = 2", s1txt)

        s1txt2 = self._text([
            r"\text{Meqe 2 nuk eshte katror}",
            r"\text{i plote, rrezja eshte irracionale:}",
        ], s1eq1, buff=0.3)
        self.wait(2)

        s1eq2 = self._eq(r"r = \sqrt{2} \approx 1{,}41", s1eq1, color=ANSWER_COLOR,
                          key=True, buff=0.25)
        # Reposition after text (text was added after eq1 but we want eq2 below text)
        # Actually let's fix the flow: eq2 below s1txt2
        # We already created it below s1eq1; let's just continue

        self.wait(1)

        # Clean
        calc1 = VGroup(s1t, s1txt, s1eq1, s1txt2, s1eq2)
        self.play(FadeOut(calc1), run_time=T_TRANSITION)
        self.wait(0.3)

        # --- Intercepts (combined for moderate pace) ---
        s2t = self._title("Pikeprerjet me boshtet", y_pos=3.2)

        s2txt = self._text([
            r"\text{Vendosim } y = 0\text{:}",
        ], s2t)
        self.wait(1)

        s2eq1 = self._eq(r"x^2 = 2 \implies x = \pm\sqrt{2}", s2txt, color=LABEL_COLOR)

        s2pts = self._eq(
            r"(-\sqrt{2},\,0) \quad \text{dhe} \quad (\sqrt{2},\,0)",
            s2eq1, color=LABEL_COLOR, fs=28,
        )
        self.wait(1.5)

        s2txt2 = self._text([
            r"\text{Vendosim } x = 0\text{:}",
        ], s2pts, buff=0.3)
        self.wait(1)

        s2eq2 = self._eq(r"y^2 = 2 \implies y = \pm\sqrt{2}", s2txt2, color=HIGHLIGHT_COLOR)

        s2pts2 = self._eq(
            r"(0,\,-\sqrt{2}) \quad \text{dhe} \quad (0,\,\sqrt{2})",
            s2eq2, color=HIGHLIGHT_COLOR, fs=28,
        )
        self.wait(1.5)

        calc2 = VGroup(s2t, s2txt, s2eq1, s2pts, s2txt2, s2eq2, s2pts2)
        self.play(FadeOut(calc2), run_time=T_TRANSITION)
        self.wait(0.3)

        # --- Graph ---
        sqrt2 = np.sqrt(2)
        axes, axes_labels, circle = self._build_graph(sqrt2, axis_bound=3, step=1)

        self.play(Create(axes), FadeIn(axes_labels), run_time=T_SHAPE_CREATE)
        self.play(Create(circle), run_time=T_SHAPE_CREATE)
        self.wait(1)

        eq_label = MathTex(r"x^2 + y^2 = 2", font_size=24, color=SHAPE_COLOR)
        eq_label.next_to(axes, UR, buff=0.2).shift(DOWN * 0.5)
        self.play(FadeIn(eq_label), run_time=0.5)

        div = make_divider()
        self.play(FadeIn(div), run_time=0.2)

        res_t = self._title("Pikeprerjet", y_pos=3.0)

        res_x = self._eq(
            r"(\pm\sqrt{2},\,0)",
            res_t, color=LABEL_COLOR, fs=28, buff=0.4,
        )

        d1, l1 = self.mark_point(axes, -sqrt2, 0, r"(-\!\sqrt{2},0)",
                                  color=LABEL_COLOR, direction=DL, font_size=18)
        d2, l2 = self.mark_point(axes, sqrt2, 0, r"(\sqrt{2},0)",
                                  color=LABEL_COLOR, direction=DR, font_size=18)
        self._transfer_value(res_x, VGroup(d1, l1))
        self._transfer_value(res_x, VGroup(d2, l2))
        self.wait(1)

        res_y = self._eq(
            r"(0,\,\pm\sqrt{2})",
            res_x, color=HIGHLIGHT_COLOR, fs=28, buff=0.3,
        )

        d3, l3 = self.mark_point(axes, 0, -sqrt2, r"(0,-\!\sqrt{2})",
                                  color=HIGHLIGHT_COLOR, direction=DL, font_size=18)
        d4, l4 = self.mark_point(axes, 0, sqrt2, r"(0,\sqrt{2})",
                                  color=HIGHLIGHT_COLOR, direction=UL, font_size=18)
        self._transfer_value(res_y, VGroup(d3, l3))
        self._transfer_value(res_y, VGroup(d4, l4))
        self.wait(1)

        r_label = self._eq(r"r = \sqrt{2}", res_y, color=ANSWER_COLOR, fs=30, key=True)

        r_line = DashedLine(
            axes.c2p(0, 0), axes.c2p(sqrt2, 0),
            color=ANSWER_COLOR, dash_length=0.08, stroke_width=2,
        )
        r_mid = MathTex(r"\sqrt{2}", font_size=18, color=ANSWER_COLOR)
        r_mid.next_to(r_line, UP, buff=0.12)
        self._transfer_value(r_label, VGroup(r_line, r_mid))

        self.wait(W_AFTER_ANSWER)

    # ================================================================
    #  PART D -- x^2 + y^2 = 20, r = 2*sqrt(5)
    #  MODERATE: explain surd simplification sqrt(20) = 2*sqrt(5)
    # ================================================================
    def part_d(self):
        self.show_part_header("d")

        # --- Problem ---
        prob = MathTex(r"x^2 + y^2 = 20", font_size=PROBLEM_MATH_SIZE + 4)
        self.play(FadeIn(prob, shift=UP * 0.3), run_time=T_SHAPE_CREATE)
        self.wait(W_PROBLEM)
        self.play(FadeOut(prob), run_time=T_TRANSITION)
        self.wait(0.3)

        # --- Radius with surd simplification ---
        s1t = self._title("Gjejme rrezen", y_pos=3.2)

        s1txt = self._text([
            r"\text{Forma } x^2 + y^2 = r^2\text{:}",
        ], s1t)
        self.wait(1)

        s1eq1 = self._eq(r"r^2 = 20", s1txt)
        s1eq2 = self._eq(r"r = \sqrt{20}", s1eq1)

        s1txt2 = self._text([
            r"\text{Thjeshtojme rrenjen katrore:}",
        ], s1eq2, buff=0.3)
        self.wait(2)

        s1eq3 = self._eq(r"\sqrt{20} = \sqrt{4 \times 5}", s1txt2)
        s1eq4 = self._eq(r"= \sqrt{4} \cdot \sqrt{5} = 2\sqrt{5}", s1eq3)

        s1res = self._eq(
            r"r = 2\sqrt{5} \approx 4{,}47",
            s1eq4, color=ANSWER_COLOR, key=True,
        )
        self.wait(1)

        calc1 = VGroup(s1t, s1txt, s1eq1, s1eq2, s1txt2, s1eq3, s1eq4, s1res)
        self.play(FadeOut(calc1), run_time=T_TRANSITION)
        self.wait(0.3)

        # --- Intercepts (combined) ---
        s2t = self._title("Pikeprerjet me boshtet", y_pos=3.2)

        s2txt = self._text([
            r"\text{Vendosim } y = 0\text{:}",
        ], s2t)
        self.wait(1)

        s2eq1 = self._eq(r"x^2 = 20 \implies x = \pm 2\sqrt{5}", s2txt, color=LABEL_COLOR)

        s2pts = self._eq(
            r"(-2\sqrt{5},\,0),\; (2\sqrt{5},\,0)",
            s2eq1, color=LABEL_COLOR, fs=26,
        )
        self.wait(1.5)

        s2txt2 = self._text([
            r"\text{Vendosim } x = 0\text{:}",
        ], s2pts, buff=0.3)
        self.wait(1)

        s2eq2 = self._eq(r"y^2 = 20 \implies y = \pm 2\sqrt{5}", s2txt2,
                          color=HIGHLIGHT_COLOR)

        s2pts2 = self._eq(
            r"(0,\,-2\sqrt{5}),\; (0,\,2\sqrt{5})",
            s2eq2, color=HIGHLIGHT_COLOR, fs=26,
        )
        self.wait(1.5)

        calc2 = VGroup(s2t, s2txt, s2eq1, s2pts, s2txt2, s2eq2, s2pts2)
        self.play(FadeOut(calc2), run_time=T_TRANSITION)
        self.wait(0.3)

        # --- Graph ---
        r_val = 2 * np.sqrt(5)
        axes, axes_labels, circle = self._build_graph(r_val, axis_bound=6, step=2)

        self.play(Create(axes), FadeIn(axes_labels), run_time=T_SHAPE_CREATE)
        self.play(Create(circle), run_time=T_SHAPE_CREATE)
        self.wait(1)

        eq_label = MathTex(r"x^2 + y^2 = 20", font_size=24, color=SHAPE_COLOR)
        eq_label.next_to(axes, UR, buff=0.2).shift(DOWN * 0.5)
        self.play(FadeIn(eq_label), run_time=0.5)

        div = make_divider()
        self.play(FadeIn(div), run_time=0.2)

        res_t = self._title("Pikeprerjet", y_pos=3.0)

        res_x = self._eq(
            r"(\pm 2\sqrt{5},\,0)",
            res_t, color=LABEL_COLOR, fs=28, buff=0.4,
        )

        d1, l1 = self.mark_point(axes, -r_val, 0, r"(-2\!\sqrt{5},0)",
                                  color=LABEL_COLOR, direction=DL, font_size=18)
        d2, l2 = self.mark_point(axes, r_val, 0, r"(2\!\sqrt{5},0)",
                                  color=LABEL_COLOR, direction=DR, font_size=18)
        self._transfer_value(res_x, VGroup(d1, l1))
        self._transfer_value(res_x, VGroup(d2, l2))
        self.wait(1)

        res_y = self._eq(
            r"(0,\,\pm 2\sqrt{5})",
            res_x, color=HIGHLIGHT_COLOR, fs=28, buff=0.3,
        )

        d3, l3 = self.mark_point(axes, 0, -r_val, r"(0,-2\!\sqrt{5})",
                                  color=HIGHLIGHT_COLOR, direction=DL, font_size=18)
        d4, l4 = self.mark_point(axes, 0, r_val, r"(0,2\!\sqrt{5})",
                                  color=HIGHLIGHT_COLOR, direction=UL, font_size=18)
        self._transfer_value(res_y, VGroup(d3, l3))
        self._transfer_value(res_y, VGroup(d4, l4))
        self.wait(1)

        r_label = self._eq(r"r = 2\sqrt{5}", res_y, color=ANSWER_COLOR, fs=30, key=True)

        r_line = DashedLine(
            axes.c2p(0, 0), axes.c2p(r_val, 0),
            color=ANSWER_COLOR, dash_length=0.08, stroke_width=2,
        )
        r_mid = MathTex(r"2\sqrt{5}", font_size=18, color=ANSWER_COLOR)
        r_mid.next_to(r_line, UP, buff=0.12)
        self._transfer_value(r_label, VGroup(r_line, r_mid))

        self.wait(W_AFTER_ANSWER)

    # ================================================================
    #  PART E -- y^2 = 4 - x^2 --> x^2 + y^2 = 4, r = 2
    #  EXTRA: show the algebra of rewriting to standard form
    # ================================================================
    def part_e(self):
        self.show_part_header("e")

        # --- Problem statement ---
        prob = MathTex(r"y^2 = 4 - x^2", font_size=PROBLEM_MATH_SIZE + 4)
        self.play(FadeIn(prob, shift=UP * 0.3), run_time=T_SHAPE_CREATE)
        self.wait(W_PROBLEM)
        self.play(FadeOut(prob), run_time=T_TRANSITION)
        self.wait(0.3)

        # --- Rewrite to standard form ---
        s1t = self._title("Rishkruajme ne formen standarde", y_pos=3.2)

        s1txt = self._text([
            r"\text{Ekuacioni i dhene:}",
        ], s1t)
        self.wait(1)

        s1eq1 = self._eq(r"y^2 = 4 - x^2", s1txt)

        s1txt2 = self._text([
            r"\text{Shtojme } x^2 \text{ ne te dyja anet:}",
        ], s1eq1, buff=0.3)
        self.wait(2)

        s1eq2 = self._eq(r"x^2 + y^2 = 4", s1txt2, key=True)

        # Flash to emphasize this is a circle
        self.play(Indicate(s1eq2, color=SHAPE_COLOR, scale_factor=1.15), run_time=0.6)

        s1txt3 = self._text([
            r"\text{Kjo eshte forma } x^2 + y^2 = r^2",
            r"\text{me qender ne origjine!}",
        ], s1eq2, buff=0.3)
        self.wait(2.5)

        # Clean
        calc1 = VGroup(s1t, s1txt, s1eq1, s1txt2, s1eq2, s1txt3)
        self.play(FadeOut(calc1), run_time=T_TRANSITION)
        self.wait(0.3)

        # --- Radius ---
        s2t = self._title("Gjejme rrezen", y_pos=3.2)

        s2eq1 = self._eq(r"r^2 = 4", s2t, buff=0.4)
        s2eq2 = self._eq(r"r = \sqrt{4} = 2", s2eq1, color=ANSWER_COLOR, key=True)
        self.wait(1)

        # --- Intercepts ---
        s2txt = self._text([
            r"\text{Vendosim } y = 0\text{:}",
        ], s2eq2, buff=0.4)
        self.wait(1)

        s2eq3 = self._eq(r"x^2 = 4 \implies x = \pm 2", s2txt, color=LABEL_COLOR)

        s2txt2 = self._text([
            r"\text{Vendosim } x = 0\text{:}",
        ], s2eq3, buff=0.3)
        self.wait(1)

        s2eq4 = self._eq(r"y^2 = 4 \implies y = \pm 2", s2txt2, color=HIGHLIGHT_COLOR)
        self.wait(1.5)

        calc2 = VGroup(s2t, s2eq1, s2eq2, s2txt, s2eq3, s2txt2, s2eq4)
        self.play(FadeOut(calc2), run_time=T_TRANSITION)
        self.wait(0.3)

        # --- Graph ---
        axes, axes_labels, circle = self._build_graph(2, axis_bound=4, step=1)

        self.play(Create(axes), FadeIn(axes_labels), run_time=T_SHAPE_CREATE)
        self.play(Create(circle), run_time=T_SHAPE_CREATE)
        self.wait(1)

        eq_label = MathTex(r"x^2 + y^2 = 4", font_size=24, color=SHAPE_COLOR)
        eq_label.next_to(axes, UR, buff=0.2).shift(DOWN * 0.5)
        orig_label = MathTex(r"(y^2 = 4 - x^2)", font_size=18, color=BODY_TEXT_COLOR)
        orig_label.next_to(eq_label, DOWN, buff=0.1)
        self.play(FadeIn(eq_label), FadeIn(orig_label), run_time=0.5)

        div = make_divider()
        self.play(FadeIn(div), run_time=0.2)

        res_t = self._title("Pikeprerjet", y_pos=3.0)

        res_x = self._eq(
            r"x\text{-boshti: } (-2,\,0),\; (2,\,0)",
            res_t, color=LABEL_COLOR, fs=28, buff=0.4,
        )

        d1, l1 = self.mark_point(axes, -2, 0, r"(-2,0)", color=LABEL_COLOR,
                                  direction=DL, font_size=20)
        d2, l2 = self.mark_point(axes, 2, 0, r"(2,0)", color=LABEL_COLOR,
                                  direction=DR, font_size=20)
        self._transfer_value(res_x, VGroup(d1, l1))
        self._transfer_value(res_x, VGroup(d2, l2))
        self.wait(1)

        res_y = self._eq(
            r"y\text{-boshti: } (0,\,-2),\; (0,\,2)",
            res_x, color=HIGHLIGHT_COLOR, fs=28, buff=0.3,
        )

        d3, l3 = self.mark_point(axes, 0, -2, r"(0,-2)", color=HIGHLIGHT_COLOR,
                                  direction=DL, font_size=20)
        d4, l4 = self.mark_point(axes, 0, 2, r"(0,2)", color=HIGHLIGHT_COLOR,
                                  direction=UL, font_size=20)
        self._transfer_value(res_y, VGroup(d3, l3))
        self._transfer_value(res_y, VGroup(d4, l4))
        self.wait(1)

        r_label = self._eq(r"r = 2", res_y, color=ANSWER_COLOR, fs=30, key=True)

        r_line = DashedLine(
            axes.c2p(0, 0), axes.c2p(2, 0),
            color=ANSWER_COLOR, dash_length=0.08, stroke_width=2,
        )
        r_mid = MathTex("2", font_size=20, color=ANSWER_COLOR)
        r_mid.next_to(r_line, UP, buff=0.12)
        self._transfer_value(r_label, VGroup(r_line, r_mid))

        self.wait(W_AFTER_ANSWER)

    # ================================================================
    #  PART F -- y^2 = 16 - x^2 --> x^2 + y^2 = 16, r = 4
    #  EXTRA: show the algebra of rewriting (same pattern as e)
    # ================================================================
    def part_f(self):
        self.show_part_header("f")

        # --- Problem statement ---
        prob = MathTex(r"y^2 = 16 - x^2", font_size=PROBLEM_MATH_SIZE + 4)
        self.play(FadeIn(prob, shift=UP * 0.3), run_time=T_SHAPE_CREATE)
        self.wait(W_PROBLEM)
        self.play(FadeOut(prob), run_time=T_TRANSITION)
        self.wait(0.3)

        # --- Rewrite to standard form ---
        s1t = self._title("Rishkruajme ne formen standarde", y_pos=3.2)

        s1txt = self._text([
            r"\text{Ekuacioni i dhene:}",
        ], s1t)
        self.wait(1)

        s1eq1 = self._eq(r"y^2 = 16 - x^2", s1txt)

        s1txt2 = self._text([
            r"\text{Shtojme } x^2 \text{ ne te dyja anet:}",
        ], s1eq1, buff=0.3)
        self.wait(2)

        s1eq2 = self._eq(r"x^2 + y^2 = 16", s1txt2, key=True)

        self.play(Indicate(s1eq2, color=SHAPE_COLOR, scale_factor=1.15), run_time=0.6)

        s1txt3 = self._text([
            r"\text{Rreth me qender ne origjine!}",
        ], s1eq2, buff=0.3)
        self.wait(2)

        calc1 = VGroup(s1t, s1txt, s1eq1, s1txt2, s1eq2, s1txt3)
        self.play(FadeOut(calc1), run_time=T_TRANSITION)
        self.wait(0.3)

        # --- Radius ---
        s2t = self._title("Gjejme rrezen", y_pos=3.2)

        s2eq1 = self._eq(r"r^2 = 16", s2t, buff=0.4)
        s2eq2 = self._eq(r"r = \sqrt{16} = 4", s2eq1, color=ANSWER_COLOR, key=True)
        self.wait(1)

        # --- Intercepts ---
        s2txt = self._text([
            r"\text{Vendosim } y = 0\text{:}",
        ], s2eq2, buff=0.4)
        self.wait(1)

        s2eq3 = self._eq(r"x^2 = 16 \implies x = \pm 4", s2txt, color=LABEL_COLOR)

        s2txt2 = self._text([
            r"\text{Vendosim } x = 0\text{:}",
        ], s2eq3, buff=0.3)
        self.wait(1)

        s2eq4 = self._eq(r"y^2 = 16 \implies y = \pm 4", s2txt2, color=HIGHLIGHT_COLOR)
        self.wait(1.5)

        calc2 = VGroup(s2t, s2eq1, s2eq2, s2txt, s2eq3, s2txt2, s2eq4)
        self.play(FadeOut(calc2), run_time=T_TRANSITION)
        self.wait(0.3)

        # --- Graph ---
        axes, axes_labels, circle = self._build_graph(4, axis_bound=6, step=2)

        self.play(Create(axes), FadeIn(axes_labels), run_time=T_SHAPE_CREATE)
        self.play(Create(circle), run_time=T_SHAPE_CREATE)
        self.wait(1)

        eq_label = MathTex(r"x^2 + y^2 = 16", font_size=24, color=SHAPE_COLOR)
        eq_label.next_to(axes, UR, buff=0.2).shift(DOWN * 0.5)
        orig_label = MathTex(r"(y^2 = 16 - x^2)", font_size=18, color=BODY_TEXT_COLOR)
        orig_label.next_to(eq_label, DOWN, buff=0.1)
        self.play(FadeIn(eq_label), FadeIn(orig_label), run_time=0.5)

        div = make_divider()
        self.play(FadeIn(div), run_time=0.2)

        res_t = self._title("Pikeprerjet", y_pos=3.0)

        res_x = self._eq(
            r"x\text{-boshti: } (-4,\,0),\; (4,\,0)",
            res_t, color=LABEL_COLOR, fs=28, buff=0.4,
        )

        d1, l1 = self.mark_point(axes, -4, 0, r"(-4,0)", color=LABEL_COLOR,
                                  direction=DL, font_size=20)
        d2, l2 = self.mark_point(axes, 4, 0, r"(4,0)", color=LABEL_COLOR,
                                  direction=DR, font_size=20)
        self._transfer_value(res_x, VGroup(d1, l1))
        self._transfer_value(res_x, VGroup(d2, l2))
        self.wait(1)

        res_y = self._eq(
            r"y\text{-boshti: } (0,\,-4),\; (0,\,4)",
            res_x, color=HIGHLIGHT_COLOR, fs=28, buff=0.3,
        )

        d3, l3 = self.mark_point(axes, 0, -4, r"(0,-4)", color=HIGHLIGHT_COLOR,
                                  direction=DL, font_size=20)
        d4, l4 = self.mark_point(axes, 0, 4, r"(0,4)", color=HIGHLIGHT_COLOR,
                                  direction=UL, font_size=20)
        self._transfer_value(res_y, VGroup(d3, l3))
        self._transfer_value(res_y, VGroup(d4, l4))
        self.wait(1)

        r_label = self._eq(r"r = 4", res_y, color=ANSWER_COLOR, fs=30, key=True)

        r_line = DashedLine(
            axes.c2p(0, 0), axes.c2p(4, 0),
            color=ANSWER_COLOR, dash_length=0.08, stroke_width=2,
        )
        r_mid = MathTex("4", font_size=20, color=ANSWER_COLOR)
        r_mid.next_to(r_line, UP, buff=0.12)
        self._transfer_value(r_label, VGroup(r_line, r_mid))

        self.wait(W_AFTER_ANSWER)

    # ================================================================
    #  FINAL SUMMARY
    # ================================================================
    def final_summary(self):
        self.show_summary_table(
            "Permbledhje",
            [
                r"\text{a)}\; x^2+y^2=49 \quad r=7 \quad (\pm7,0),\;(0,\pm7)",
                r"\text{b)}\; x^2+y^2=64 \quad r=8 \quad (\pm8,0),\;(0,\pm8)",
                r"\text{c)}\; x^2+y^2=2 \quad r=\sqrt{2} \quad (\pm\sqrt{2},0),\;(0,\pm\sqrt{2})",
                r"\text{d)}\; x^2+y^2=20 \quad r=2\sqrt{5} \quad (\pm 2\sqrt{5},0),\;(0,\pm 2\sqrt{5})",
                r"\text{e)}\; x^2+y^2=4 \quad r=2 \quad (\pm2,0),\;(0,\pm2)",
                r"\text{f)}\; x^2+y^2=16 \quad r=4 \quad (\pm4,0),\;(0,\pm4)",
            ],
            font_size=26,
        )
