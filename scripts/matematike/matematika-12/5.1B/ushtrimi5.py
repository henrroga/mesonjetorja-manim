import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from manim import *
import numpy as np
from components import ExerciseScene
from style_guide import (
    make_answer_box, make_divider, fade_all,
    STEP_TITLE_COLOR, BODY_TEXT_COLOR, LABEL_COLOR,
    ANSWER_COLOR, SHAPE_COLOR, AUX_COLOR, HIGHLIGHT_COLOR, DIVIDER_COLOR,
    PART_HEADER_SIZE, STEP_TITLE_SIZE,
    BODY_SIZE, PROBLEM_MATH_SIZE, CALC_SIZE, ANSWER_SIZE,
    T_STEP_TITLE, T_BODY_FADE, T_KEY_EQUATION, T_ROUTINE_EQUATION,
    T_SHAPE_CREATE, T_DOT_FADE, T_LAYOUT_SHIFT, T_TRANSITION,
    W_AFTER_KEY, W_AFTER_ROUTINE, W_AFTER_ANSWER, W_PROBLEM,
    CALC_TOP, PX,
)


class Ushtrimi5(ExerciseScene):
    """
    Ushtrimi 5 — Njesia 5.1B — Matematika 12

    a) Zgjidhni: 3^(2x-1) - 5*3^(x-1) + 2 = 0
    b) Gjeni pikat e prerjes se y=3^(2x-1)+2 dhe y=5*3^(x-1)

    Visual storytelling — no voiceover.
    """

    exercise_number = 5
    unit = "5.1B"
    textbook = "Matematika 12"
    parts = ["a", "b"]

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
        else:
            t.move_to(np.array([PX, 3.2, 0]))
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

    def _centered_title(self, text, y_pos=3.0):
        """Title centered on screen (for full-screen algebra, no split layout)."""
        t = MathTex(
            r"\text{" + text + r"}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        t.move_to(np.array([0, y_pos, 0]))
        self.play(FadeIn(t), run_time=T_STEP_TITLE)
        return t

    def _centered_text(self, lines, ref, buff=0.25):
        """Body text centered on screen."""
        parts = [MathTex(l, font_size=BODY_SIZE, color=BODY_TEXT_COLOR) for l in lines]
        g = VGroup(*parts).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        g.next_to(ref, DOWN, buff=buff)
        g.set_x(0)
        self.play(FadeIn(g), run_time=T_BODY_FADE)
        return g

    def _centered_eq(self, tex, ref, buff=0.25, color=None, fs=None, key=False):
        """Equation centered on screen."""
        eq = MathTex(tex, font_size=fs or CALC_SIZE)
        if color:
            eq.set_color(color)
        eq.next_to(ref, DOWN, buff=buff)
        eq.set_x(0)
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
    #  PART A — Solve 3^(2x-1) - 5*3^(x-1) + 2 = 0
    #  Full-screen algebra, no graph needed.
    # ================================================================
    def part_a(self):
        self.show_part_header("a")

        # ── Problem statement ──
        prob_title = MathTex(
            r"\text{Zgjidhni ekuacionin:}",
            font_size=STEP_TITLE_SIZE + 4, color=WHITE,
        )
        prob_eq = MathTex(
            r"3^{2x-1} - 5 \cdot 3^{x-1} + 2 = 0",
            font_size=PROBLEM_MATH_SIZE + 4,
        )
        self.show_problem(prob_title, prob_eq, wait_time=4.0)

        # ────────────────────────────────────────────
        # Step 1: Rewrite 3^(2x-1) using exponent rules
        # ────────────────────────────────────────────
        s1t = self._centered_title("Hapi 1: Rishkruajme fuqite", y_pos=3.2)

        s1txt = self._centered_text([
            r"\text{Perdorim vetine e eksponenteve:}",
            r"a^{m+n} = a^m \cdot a^n",
        ], s1t)
        self.wait(2.0)

        # Show rewriting 3^(2x-1) step by step
        s1eq1 = self._centered_eq(
            r"3^{2x-1} = 3^{-1} \cdot 3^{2x} = \frac{1}{3} \cdot (3^x)^2",
            s1txt, buff=0.35, key=True, fs=34,
        )

        # Show rewriting 5*3^(x-1) step by step
        s1eq2 = self._centered_eq(
            r"5 \cdot 3^{x-1} = 5 \cdot 3^{-1} \cdot 3^x = \frac{5}{3} \cdot 3^x",
            s1eq1, buff=0.3, key=True, fs=34,
        )
        self.wait(1.5)

        # Clean screen
        self.play(
            FadeOut(VGroup(s1t, s1txt, s1eq1, s1eq2)),
            run_time=T_TRANSITION,
        )
        self.wait(0.5)

        # ────────────────────────────────────────────
        # Step 2: Substitute into the equation
        # ────────────────────────────────────────────
        s2t = self._centered_title("Hapi 2: Zevendesojme ne ekuacion", y_pos=3.2)

        s2txt = self._centered_text([
            r"\text{Ekuacioni behet:}",
        ], s2t)
        self.wait(1.5)

        s2eq1 = self._centered_eq(
            r"\frac{1}{3}(3^x)^2 - \frac{5}{3} \cdot 3^x + 2 = 0",
            s2txt, buff=0.35, key=True, fs=34,
        )

        s2txt2 = self._centered_text([
            r"\text{Shumezojme te dyja anet me 3}",
            r"\text{per te hequr thyesat:}",
        ], s2eq1, buff=0.3)
        self.wait(2.0)

        s2eq2 = self._centered_eq(
            r"(3^x)^2 - 5 \cdot 3^x + 6 = 0",
            s2txt2, buff=0.3, color=LABEL_COLOR, key=True, fs=36,
        )
        self.wait(1.5)

        # Clean screen
        self.play(
            FadeOut(VGroup(s2t, s2txt, s2eq1, s2txt2, s2eq2)),
            run_time=T_TRANSITION,
        )
        self.wait(0.5)

        # ────────────────────────────────────────────
        # Step 3: Substitution t = 3^x
        # ────────────────────────────────────────────
        s3t = self._centered_title("Hapi 3: Zevendesimi", y_pos=3.2)

        s3txt = self._centered_text([
            r"\text{Kjo eshte nje teknike standarde:}",
            r"\text{zevendesojme } t = 3^x",
        ], s3t)
        self.wait(2.5)

        s3eq1 = self._centered_eq(
            r"\text{Le } t = 3^x, \quad t > 0",
            s3txt, buff=0.35, color=HIGHLIGHT_COLOR, fs=34, key=True,
        )

        s3eq2 = self._centered_eq(
            r"t^2 - 5t + 6 = 0",
            s3eq1, buff=0.35, color=LABEL_COLOR, fs=38, key=True,
        )
        self.wait(1.5)

        # Clean screen
        self.play(
            FadeOut(VGroup(s3t, s3txt, s3eq1, s3eq2)),
            run_time=T_TRANSITION,
        )
        self.wait(0.5)

        # ────────────────────────────────────────────
        # Step 4: Factor the quadratic
        # ────────────────────────────────────────────
        s4t = self._centered_title("Hapi 4: Faktorizimi", y_pos=3.2)

        s4eq0 = self._centered_eq(
            r"t^2 - 5t + 6 = 0",
            s4t, buff=0.35, fs=34,
        )

        s4txt = self._centered_text([
            r"\text{Gjejme dy numra qe shumezojne 6}",
            r"\text{dhe mbledhin 5: keta jane 2 dhe 3}",
        ], s4eq0, buff=0.3)
        self.wait(3.0)

        s4eq1 = self._centered_eq(
            r"(t - 2)(t - 3) = 0",
            s4txt, buff=0.3, color=LABEL_COLOR, fs=36, key=True,
        )

        s4eq2 = self._centered_eq(
            r"t_1 = 2 \qquad t_2 = 3",
            s4eq1, buff=0.35, color=ANSWER_COLOR, fs=36, key=True,
        )
        self.wait(1.5)

        # Clean screen
        self.play(
            FadeOut(VGroup(s4t, s4eq0, s4txt, s4eq1, s4eq2)),
            run_time=T_TRANSITION,
        )
        self.wait(0.5)

        # ────────────────────────────────────────────
        # Step 5: Back-substitute — two cases side by side
        # ────────────────────────────────────────────
        s5t = self._centered_title("Hapi 5: Kthehemi te x", y_pos=3.2)

        s5txt = self._centered_text([
            r"\text{Zevendesojme mbrapa } t = 3^x \text{:}",
        ], s5t)
        self.wait(2.0)

        # Fade before showing side-by-side cases
        self.play(FadeOut(VGroup(s5t, s5txt)), run_time=T_TRANSITION)
        self.wait(0.3)

        # ── Case 1: 3^x = 2 (left side) ──
        case1_title = MathTex(
            r"\text{Rasti 1:}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        case1_title.move_to(np.array([-3, 3.0, 0]))

        c1_eqs = [
            MathTex(r"3^x = 2", font_size=CALC_SIZE + 2),
            MathTex(
                r"\text{Marrim logaritmin e te dyja aneve:}",
                font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
            ),
            MathTex(r"\log(3^x) = \log 2", font_size=CALC_SIZE),
            MathTex(
                r"\text{Vetia: } \log(a^n) = n \cdot \log a",
                font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
            ),
            MathTex(r"x \cdot \log 3 = \log 2", font_size=CALC_SIZE),
            MathTex(
                r"x = \frac{\log 2}{\log 3} \approx 0{,}631",
                font_size=CALC_SIZE + 2, color=ANSWER_COLOR,
            ),
        ]
        for i, eq in enumerate(c1_eqs):
            if i == 0:
                eq.next_to(case1_title, DOWN, buff=0.3)
            else:
                eq.next_to(c1_eqs[i - 1], DOWN, buff=0.22)
            eq.set_x(-3)

        # ── Case 2: 3^x = 3 (right side) ──
        case2_title = MathTex(
            r"\text{Rasti 2:}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        case2_title.move_to(np.array([3, 3.0, 0]))

        c2_eqs = [
            MathTex(r"3^x = 3", font_size=CALC_SIZE + 2),
            MathTex(
                r"\text{Bazat jane te njejta:}",
                font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
            ),
            MathTex(r"3^x = 3^1", font_size=CALC_SIZE),
            MathTex(
                r"\text{Ekspomentet jane te barabarta:}",
                font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
            ),
            MathTex(r"x = 1", font_size=CALC_SIZE + 2, color=ANSWER_COLOR),
        ]
        for i, eq in enumerate(c2_eqs):
            if i == 0:
                eq.next_to(case2_title, DOWN, buff=0.3)
            else:
                eq.next_to(c2_eqs[i - 1], DOWN, buff=0.22)
            eq.set_x(3)

        # Animate case 1
        self.play(FadeIn(case1_title), run_time=T_STEP_TITLE)
        for eq in c1_eqs:
            is_key = (eq == c1_eqs[-1])
            rt = T_KEY_EQUATION if is_key else T_ROUTINE_EQUATION
            self.play(Write(eq), run_time=rt)
            self.wait(1.5 if not is_key else W_AFTER_KEY)

        # Animate case 2
        self.play(FadeIn(case2_title), run_time=T_STEP_TITLE)
        for eq in c2_eqs:
            is_key = (eq == c2_eqs[-1])
            rt = T_KEY_EQUATION if is_key else T_ROUTINE_EQUATION
            self.play(Write(eq), run_time=rt)
            self.wait(1.5 if not is_key else W_AFTER_KEY)

        self.wait(2.0)

        # Clean screen
        self.play(
            FadeOut(VGroup(case1_title, *c1_eqs, case2_title, *c2_eqs)),
            run_time=T_TRANSITION,
        )
        self.wait(0.5)

        # ── Final answer ──
        ans_title = MathTex(
            r"\text{Pergjigja:}",
            font_size=STEP_TITLE_SIZE + 4, color=WHITE,
        )
        ans1 = MathTex(
            r"x_1 = \frac{\log 2}{\log 3} \approx 0{,}631",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        ans2 = MathTex(
            r"x_2 = 1",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        ans_group = VGroup(ans_title, ans1, ans2).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        box = make_answer_box(VGroup(ans1, ans2))

        self.play(FadeIn(ans_group), run_time=T_SHAPE_CREATE)
        self.play(Create(box), run_time=0.5)
        self.wait(W_AFTER_ANSWER)

    # ================================================================
    #  PART B — Intersection of y=3^(2x-1)+2 and y=5*3^(x-1)
    #  Split layout: graph left, calculations right.
    # ================================================================
    def part_b(self):
        self.show_part_header("b")

        # ── Problem statement ──
        prob_title = MathTex(
            r"\text{Gjeni pikat e prerjes se grafikeve:}",
            font_size=STEP_TITLE_SIZE + 2, color=WHITE,
        )
        prob_eq1 = MathTex(
            r"y = 3^{2x-1} + 2",
            font_size=PROBLEM_MATH_SIZE, color=SHAPE_COLOR,
        )
        prob_eq2 = MathTex(
            r"y = 5 \cdot 3^{x-1}",
            font_size=PROBLEM_MATH_SIZE, color=AUX_COLOR,
        )
        self.show_problem(prob_title, prob_eq1, prob_eq2, wait_time=4.0)

        # ── Build graph ──
        axes = Axes(
            x_range=[-2, 3, 1],
            y_range=[-1, 20, 5],
            x_length=5.5,
            y_length=5.5,
            axis_config={
                "include_tip": True,
                "include_numbers": True,
                "font_size": 18,
                "color": DIVIDER_COLOR,
            },
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")

        # Curve 1: y = 3^(2x-1) + 2
        func1 = axes.plot(
            lambda x: 3 ** (2 * x - 1) + 2,
            x_range=[-1.5, 1.65],
            color=SHAPE_COLOR,
            stroke_width=2.5,
        )
        func1_label = MathTex(
            r"y=3^{2x-1}+2", font_size=18, color=SHAPE_COLOR,
        )
        func1_label.next_to(func1.point_from_proportion(0.85), UR, buff=0.1)

        # Curve 2: y = 5*3^(x-1)
        func2 = axes.plot(
            lambda x: 5 * 3 ** (x - 1),
            x_range=[-1.5, 2.2],
            color=AUX_COLOR,
            stroke_width=2.5,
        )
        func2_label = MathTex(
            r"y=5 \cdot 3^{x-1}", font_size=18, color=AUX_COLOR,
        )
        func2_label.next_to(func2.point_from_proportion(0.78), RIGHT, buff=0.1)

        graph_group = VGroup(axes, axes_labels, func1, func1_label, func2, func2_label)

        # Animate graph creation
        self.play(Create(axes), FadeIn(axes_labels), run_time=T_SHAPE_CREATE)
        self.play(Create(func1), FadeIn(func1_label), run_time=T_SHAPE_CREATE)
        self.wait(1.0)
        self.play(Create(func2), FadeIn(func2_label), run_time=T_SHAPE_CREATE)
        self.wait(2.0)

        # ── Shift graph left, add divider ──
        div = self.setup_split_layout(graph_group)
        self.wait(0.5)

        # Flash curves to draw attention
        self.play(Indicate(func1, color=SHAPE_COLOR), run_time=0.5)
        self.play(Indicate(func2, color=AUX_COLOR), run_time=0.5)

        # ────────────────────────────────────────────
        # Step 1: Set equal — same equation as part a
        # ────────────────────────────────────────────
        s1t = self._title("Hapi 1: Barazojme grafiket", y_pos=3.0)

        s1txt = self._text([
            r"\text{Pikat e prerjes plotesojne:}",
        ], s1t)
        self.wait(1.5)

        s1eq1 = self._eq(
            r"3^{2x-1} + 2 = 5 \cdot 3^{x-1}",
            s1txt, buff=0.3, key=True, fs=30,
        )

        s1txt2 = self._text([
            r"\text{Risistemojme:}",
        ], s1eq1, buff=0.25)
        self.wait(1.0)

        s1eq2 = self._eq(
            r"3^{2x-1} - 5 \cdot 3^{x-1} + 2 = 0",
            s1txt2, buff=0.25, color=LABEL_COLOR, fs=28, key=True,
        )

        s1txt3 = self._text([
            r"\text{Ky eshte ekuacioni}",
            r"\text{i njejte si ne piken a)!}",
        ], s1eq2, buff=0.3)
        self.wait(3.0)

        # Clean right panel
        self.play(
            FadeOut(VGroup(s1t, s1txt, s1eq1, s1txt2, s1eq2, s1txt3)),
            run_time=T_TRANSITION,
        )
        self.wait(0.5)

        # ────────────────────────────────────────────
        # Step 2: Solutions from part a
        # ────────────────────────────────────────────
        s2t = self._title("Hapi 2: Zgjidhjet nga pika a)", y_pos=3.0)

        s2txt = self._text([
            r"\text{Kemi gjetur:}",
        ], s2t)
        self.wait(1.0)

        s2eq1 = self._eq(
            r"x_1 = 1",
            s2txt, buff=0.3, color=ANSWER_COLOR, fs=34, key=True,
        )

        s2eq2 = self._eq(
            r"x_2 = \frac{\log 2}{\log 3} \approx 0{,}631",
            s2eq1, buff=0.3, color=ANSWER_COLOR, fs=30, key=True,
        )
        self.wait(1.5)

        # Clean right panel
        self.play(
            FadeOut(VGroup(s2t, s2txt, s2eq1, s2eq2)),
            run_time=T_TRANSITION,
        )
        self.wait(0.5)

        # ────────────────────────────────────────────
        # Step 3: Find y-values
        # ────────────────────────────────────────────
        s3t = self._title("Hapi 3: Gjejme vlerat e y", y_pos=3.0)

        # y for x = 1
        s3txt1 = self._text([
            r"\text{Kur } x = 1\text{:}",
        ], s3t)
        self.wait(1.0)

        s3eq1 = self._eq(
            r"y = 5 \cdot 3^{1-1}",
            s3txt1, buff=0.25, fs=30,
        )
        s3eq2 = self._eq(
            r"y = 5 \cdot 3^0 = 5 \cdot 1",
            s3eq1, buff=0.2, fs=30,
        )
        s3eq3 = self._eq(
            r"y = 5",
            s3eq2, buff=0.2, color=ANSWER_COLOR, fs=34, key=True,
        )

        # Transfer intersection point (1, 5) to graph
        x1_val, y1_val = 1.0, 5.0
        dot1 = Dot(axes.c2p(x1_val, y1_val), color=LABEL_COLOR, radius=0.1)
        lbl1 = MathTex("(1,\\;5)", font_size=22, color=LABEL_COLOR)
        lbl1.next_to(dot1, UR, buff=0.15)
        self._transfer_value(s3eq3, VGroup(dot1, lbl1))
        self.wait(1.5)

        # Clean y1 work before y2
        self.play(
            FadeOut(VGroup(s3txt1, s3eq1, s3eq2, s3eq3)),
            run_time=T_TRANSITION,
        )
        self.wait(0.3)

        # y for x = log2/log3
        s3txt2 = self._text([
            r"\text{Kur } x = \tfrac{\log 2}{\log 3}\text{:}",
        ], s3t, buff=0.3)
        self.wait(1.0)

        s3eq4_txt = self._text([
            r"\text{Fillimisht: } 3^x = 2\text{, pra:}",
        ], s3txt2, buff=0.25)
        self.wait(1.5)

        s3eq4 = self._eq(
            r"y = 5 \cdot 3^{x-1} = 5 \cdot \frac{3^x}{3}",
            s3eq4_txt, buff=0.25, fs=30,
        )
        s3eq5 = self._eq(
            r"y = 5 \cdot \frac{2}{3} = \frac{10}{3}",
            s3eq4, buff=0.2, fs=30,
        )
        s3eq6 = self._eq(
            r"y = \frac{10}{3} \approx 3{,}33",
            s3eq5, buff=0.2, color=ANSWER_COLOR, fs=34, key=True,
        )

        # Transfer intersection point (0.631, 10/3) to graph
        x2_val = np.log(2) / np.log(3)
        y2_val = 10 / 3
        dot2 = Dot(axes.c2p(x2_val, y2_val), color=HIGHLIGHT_COLOR, radius=0.1)
        lbl2 = MathTex(
            r"\left(0{,}63;\;\tfrac{10}{3}\right)",
            font_size=20, color=HIGHLIGHT_COLOR,
        )
        lbl2.next_to(dot2, DL, buff=0.15)
        self._transfer_value(s3eq6, VGroup(dot2, lbl2))
        self.wait(2.0)

        # Clean right panel
        self.play(
            FadeOut(VGroup(s3t, s3txt2, s3eq4_txt, s3eq4, s3eq5, s3eq6)),
            run_time=T_TRANSITION,
        )
        self.wait(0.5)

        # ────────────────────────────────────────────
        # Final answer
        # ────────────────────────────────────────────
        ans_label = MathTex(
            r"\text{Pikat e prerjes:}",
            font_size=STEP_TITLE_SIZE + 2, color=WHITE,
        )
        ans_label.move_to(np.array([PX, 2.5, 0]))
        self.play(FadeIn(ans_label), run_time=T_STEP_TITLE)
        self.wait(1.0)

        ans_p1 = MathTex(
            r"(1,\;5)",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        ans_p1.next_to(ans_label, DOWN, buff=0.5)
        ans_p1.set_x(PX)

        ans_p2 = MathTex(
            r"\left(\frac{\log 2}{\log 3},\;\frac{10}{3}\right)",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        ans_p2.next_to(ans_p1, DOWN, buff=0.4)
        ans_p2.set_x(PX)

        box = make_answer_box(VGroup(ans_p1, ans_p2))

        self.play(Write(ans_p1), run_time=T_KEY_EQUATION)
        self.wait(0.5)
        self.play(Write(ans_p2), run_time=T_KEY_EQUATION)
        self.play(Create(box), run_time=0.5)

        # Highlight intersection dots on graph
        self.play(
            Indicate(dot1, color=YELLOW, scale_factor=1.5),
            Indicate(dot2, color=YELLOW, scale_factor=1.5),
            run_time=0.8,
        )
        self.wait(W_AFTER_ANSWER)
