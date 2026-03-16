import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from manim import *
import numpy as np
from components import ExerciseScene
from style_guide import (
    make_answer_box, make_divider, fade_all,
    STEP_TITLE_COLOR, BODY_TEXT_COLOR, LABEL_COLOR,
    ANSWER_COLOR, SHAPE_COLOR, AUX_COLOR, HIGHLIGHT_COLOR,
    PART_HEADER_SIZE, STEP_TITLE_SIZE,
    BODY_SIZE, CALC_SIZE, ANSWER_SIZE,
    T_STEP_TITLE, T_BODY_FADE, T_KEY_EQUATION, T_ROUTINE_EQUATION,
    T_SHAPE_CREATE, T_LAYOUT_SHIFT, T_TRANSITION,
    W_AFTER_KEY, W_AFTER_ROUTINE, W_AFTER_ANSWER, W_PROBLEM,
    CALC_TOP, PX,
)


class Ushtrimi10(ExerciseScene):
    """
    Ushtrimi 10 -- Njesia 7.5A -- Matematika 10-11: Pjesa II

    Vector algebra: express combinations in terms of a and b,
    then analyse parallelism.

    Visual storytelling approach -- no voiceover.
    Uses vector arrow diagrams with color-coded components.
    """

    exercise_number = 10
    unit = "7.5A"
    parts = ["a", "b"]

    # ── Shared helpers (right-panel, centered at x = PX) ──

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

    def _ceq(self, tex, ref=None, pos=None, buff=0.3, color=None, fs=None, key=False):
        """Centered equation (full-screen, not right-panel)."""
        eq = MathTex(tex, font_size=fs or CALC_SIZE)
        if color:
            eq.set_color(color)
        if pos is not None:
            eq.move_to(pos)
        elif ref is not None:
            eq.next_to(ref, DOWN, buff=buff)
        self.play(Write(eq), run_time=T_KEY_EQUATION if key else T_ROUTINE_EQUATION)
        self.wait(W_AFTER_KEY if key else 0.6)
        return eq

    def _ctext(self, lines, ref, buff=0.25):
        """Centered text block (full-screen)."""
        parts = [MathTex(l, font_size=BODY_SIZE, color=BODY_TEXT_COLOR) for l in lines]
        g = VGroup(*parts).arrange(DOWN, buff=0.15)
        g.next_to(ref, DOWN, buff=buff)
        self.play(FadeIn(g), run_time=T_BODY_FADE)
        return g

    def _ctitle(self, text, ref=None, y_pos=None, buff=0.5):
        """Centered title (full-screen)."""
        t = MathTex(
            r"\text{" + text + r"}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        if y_pos is not None:
            t.move_to(np.array([0, y_pos, 0]))
        elif ref is not None:
            t.next_to(ref, DOWN, buff=buff)
        self.play(FadeIn(t), run_time=T_STEP_TITLE)
        return t

    # ── Vector arrow helper ──

    def _vec_arrow(self, start, end, color=SHAPE_COLOR, stroke_width=4,
                   tip_length=0.2):
        """Create a vector arrow from start to end."""
        return Arrow(
            start, end, color=color,
            stroke_width=stroke_width,
            tip_length=tip_length,
            buff=0,
            max_stroke_width_to_length_ratio=999,
            max_tip_length_to_length_ratio=0.5,
        )

    # ================================================================
    #  PART A — Express in terms of a and b
    # ================================================================

    def part_a(self):
        header = self.show_part_header("a")

        # ── Problem statement ──
        prob_title = MathTex(
            r"\text{Te dhena:}",
            font_size=STEP_TITLE_SIZE + 6, color=STEP_TITLE_COLOR,
        )
        prob_p = MathTex(
            r"\vec{p} = 3\vec{a} + 4\vec{b}",
            font_size=36,
        )
        prob_q = MathTex(
            r"\vec{q} = \vec{a} - 2\vec{b}",
            font_size=36,
        )
        prob_r = MathTex(
            r"\vec{r} = \vec{b} - \vec{a}",
            font_size=36,
        )
        prob_ask = MathTex(
            r"\text{Shprehni me } \vec{a} \text{ dhe } \vec{b}\text{:}",
            font_size=34, color=STEP_TITLE_COLOR,
        )
        self.show_problem(prob_title, prob_p, prob_q, prob_r, prob_ask,
                          wait_time=4.0)

        # ────────────────────────────────────────
        # Sub-part i)  p + 2q  (FULL DETAIL)
        # ────────────────────────────────────────
        self._part_a_i()
        fade_all(self)
        self.wait(0.5)

        # ────────────────────────────────────────
        # Sub-part ii)  q + 2r
        # ────────────────────────────────────────
        self._part_a_ii()
        fade_all(self)
        self.wait(0.5)

        # ────────────────────────────────────────
        # Sub-part iii)  q + r
        # ────────────────────────────────────────
        self._part_a_iii()
        fade_all(self)
        self.wait(0.5)

        # ────────────────────────────────────────
        # Sub-part iv)  3q - p
        # ────────────────────────────────────────
        self._part_a_iv()

    # ── Sub-part i: p + 2q (full detail) ──

    def _part_a_i(self):
        # Problem
        t0 = self._ctitle("i)  Gjeni:", y_pos=3.2)
        eq0 = self._ceq(
            r"\vec{p} + 2\vec{q} = \text{ ?}",
            t0, fs=36, buff=0.4,
        )
        self.wait(2)

        # Step 1: Substitute definitions
        t1 = self._ctitle("Zevendesojme vlerat e vektoreve:", ref=eq0, buff=0.5)
        self.wait(1.5)

        eq1 = self._ceq(
            r"\vec{p} + 2\vec{q} = "
            r"(3\vec{a} + 4\vec{b}) + 2(\vec{a} - 2\vec{b})",
            t1, fs=30,
        )
        self.wait(2)

        # Step 2: Distribute the 2
        t2 = self._ctitle("Shumezojme 2 me secilin term:", ref=eq1, buff=0.45)
        self.wait(1.5)

        eq2 = self._ceq(
            r"= 3\vec{a} + 4\vec{b} + 2\vec{a} - 4\vec{b}",
            t2, fs=32,
        )
        self.wait(2)

        # Clear and continue on fresh screen
        self.play(
            FadeOut(VGroup(t0, eq0, t1, eq1, t2)),
            eq2.animate.move_to(UP * 2.5),
            run_time=0.8,
        )
        self.wait(0.5)

        # Step 3: Group like terms
        t3 = self._ctitle("Mbledhim termat e ngjashme:", ref=eq2, buff=0.45)
        self.wait(1.5)

        # Show grouping with colors
        eq3 = MathTex(
            r"= (",
            r"3", r"+", r"2",
            r")", r"\vec{a}",
            r" + (",
            r"4", r"-", r"4",
            r")", r"\vec{b}",
            font_size=32,
        )
        # Color a-terms blue, b-terms orange
        for i in [1, 3, 5]:
            eq3[i].set_color(SHAPE_COLOR)
        for i in [7, 9, 11]:
            eq3[i].set_color(HIGHLIGHT_COLOR)
        eq3.next_to(t3, DOWN, buff=0.35)
        self.play(Write(eq3), run_time=T_KEY_EQUATION)
        self.wait(2.5)

        # Step 4: Simplify
        eq4 = MathTex(
            r"= ", r"5\vec{a}", r" + ", r"0 \cdot \vec{b}",
            font_size=34,
        )
        eq4[1].set_color(SHAPE_COLOR)
        eq4[3].set_color(HIGHLIGHT_COLOR)
        eq4.next_to(eq3, DOWN, buff=0.35)
        self.play(Write(eq4), run_time=T_ROUTINE_EQUATION)
        self.wait(2)

        # Highlight cancellation
        cancel_text = MathTex(
            r"\text{Vektoret } \vec{b} \text{ anulohen!}",
            font_size=BODY_SIZE, color=HIGHLIGHT_COLOR,
        )
        cancel_text.next_to(eq4, DOWN, buff=0.4)
        self.play(FadeIn(cancel_text), run_time=0.6)
        self.wait(2)

        # Final answer
        ans = MathTex(
            r"\vec{p} + 2\vec{q} = 5\vec{a}",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        ans.next_to(cancel_text, DOWN, buff=0.5)
        box = make_answer_box(ans)
        self.play(Write(ans), run_time=T_KEY_EQUATION)
        self.play(Create(box), run_time=0.5)
        self.wait(3)

        # ── Vector diagram ──
        self.play(
            FadeOut(VGroup(eq2, t3, eq3, eq4, cancel_text, ans, box)),
            run_time=0.7,
        )
        self.wait(0.3)

        self._show_vector_diagram_i()

    def _show_vector_diagram_i(self):
        """Show p + 2q = 5a visually with arrows."""
        title = MathTex(
            r"\vec{p} + 2\vec{q} = 5\vec{a}",
            font_size=34, color=ANSWER_COLOR,
        )
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.5)

        # Base vectors: a points right, b points up-right at 60 degrees
        origin = LEFT * 4.5 + DOWN * 1.5
        a_unit = np.array([1.0, 0, 0])
        b_unit = np.array([0.5, 0.866, 0])
        scale = 0.7

        # Show a and b base vectors
        a_end = origin + a_unit * scale
        b_end = origin + b_unit * scale
        arr_a = self._vec_arrow(origin, a_end, color=SHAPE_COLOR)
        arr_b = self._vec_arrow(origin, b_end, color=HIGHLIGHT_COLOR)
        lbl_a = MathTex(r"\vec{a}", font_size=24, color=SHAPE_COLOR)
        lbl_a.next_to(arr_a, DOWN, buff=0.12)
        lbl_b = MathTex(r"\vec{b}", font_size=24, color=HIGHLIGHT_COLOR)
        lbl_b.next_to(arr_b, UL, buff=0.12)

        self.play(
            GrowArrow(arr_a), GrowArrow(arr_b),
            FadeIn(lbl_a), FadeIn(lbl_b),
            run_time=0.8,
        )
        self.wait(1.5)

        # Show p = 3a + 4b as composed vector
        p_origin = LEFT * 1.5 + DOWN * 1.5
        p_3a = p_origin + 3 * a_unit * scale
        p_end = p_3a + 4 * b_unit * scale

        arr_p_a = self._vec_arrow(p_origin, p_3a, color=SHAPE_COLOR, stroke_width=3)
        lbl_pa = MathTex(r"3\vec{a}", font_size=22, color=SHAPE_COLOR)
        lbl_pa.next_to(arr_p_a, DOWN, buff=0.12)

        arr_p_b = self._vec_arrow(p_3a, p_end, color=HIGHLIGHT_COLOR, stroke_width=3)
        lbl_pb = MathTex(r"4\vec{b}", font_size=22, color=HIGHLIGHT_COLOR)
        lbl_pb.next_to(arr_p_b, LEFT, buff=0.12)

        p_label = MathTex(r"\vec{p}", font_size=26, color=WHITE)
        p_label.next_to(
            Line(p_origin, p_end).get_center(), RIGHT, buff=0.3,
        )

        self.play(
            GrowArrow(arr_p_a), FadeIn(lbl_pa),
            run_time=0.8,
        )
        self.play(
            GrowArrow(arr_p_b), FadeIn(lbl_pb),
            run_time=0.8,
        )
        # Resultant p
        arr_p = self._vec_arrow(p_origin, p_end, color=GRAY_B, stroke_width=2)
        self.play(GrowArrow(arr_p), FadeIn(p_label), run_time=0.6)
        self.wait(2)

        # Show 2q = 2a - 4b starting from tip of p
        q2_origin = p_end
        q2_2a = q2_origin + 2 * a_unit * scale
        q2_end = q2_2a - 4 * b_unit * scale

        arr_q_a = self._vec_arrow(q2_origin, q2_2a, color=SHAPE_COLOR, stroke_width=3)
        lbl_qa = MathTex(r"2\vec{a}", font_size=22, color=SHAPE_COLOR)
        lbl_qa.next_to(arr_q_a, UP, buff=0.12)

        arr_q_b = self._vec_arrow(q2_2a, q2_end, color=HIGHLIGHT_COLOR, stroke_width=3)
        lbl_qb = MathTex(r"-4\vec{b}", font_size=22, color=HIGHLIGHT_COLOR)
        lbl_qb.next_to(arr_q_b, RIGHT, buff=0.12)

        self.play(
            GrowArrow(arr_q_a), FadeIn(lbl_qa),
            run_time=0.8,
        )
        self.play(
            GrowArrow(arr_q_b), FadeIn(lbl_qb),
            run_time=0.8,
        )
        self.wait(2)

        # Result: p + 2q = 5a (from p_origin to q2_end)
        # This should be purely in the a direction
        result_arrow = self._vec_arrow(
            p_origin, q2_end,
            color=ANSWER_COLOR, stroke_width=5,
        )
        result_lbl = MathTex(r"5\vec{a}", font_size=28, color=ANSWER_COLOR)
        result_lbl.next_to(result_arrow, DOWN, buff=0.15)

        self.play(GrowArrow(result_arrow), run_time=1.0)
        self.play(FadeIn(result_lbl), run_time=0.5)
        self.play(Indicate(result_arrow, color=ANSWER_COLOR), run_time=0.6)
        self.wait(3)

    # ── Sub-part ii: q + 2r ──

    def _part_a_ii(self):
        t0 = self._ctitle("ii)  Gjeni:", y_pos=3.2)
        eq0 = self._ceq(
            r"\vec{q} + 2\vec{r} = \text{ ?}",
            t0, fs=36, buff=0.4,
        )
        self.wait(1.5)

        # Substitute
        t1 = self._ctitle("Zevendesojme:", ref=eq0, buff=0.45)

        eq1 = self._ceq(
            r"= (\vec{a} - 2\vec{b}) + 2(\vec{b} - \vec{a})",
            t1, fs=30,
        )
        self.wait(1.5)

        # Distribute
        t2 = self._ctitle("Shprehim:", ref=eq1, buff=0.4)

        eq2 = self._ceq(
            r"= \vec{a} - 2\vec{b} + 2\vec{b} - 2\vec{a}",
            t2, fs=32,
        )
        self.wait(2)

        # Collect like terms
        eq3 = MathTex(
            r"= (",
            r"1", r"-", r"2",
            r")", r"\vec{a}",
            r" + (",
            r"-2", r"+", r"2",
            r")", r"\vec{b}",
            font_size=32,
        )
        for i in [1, 3, 5]:
            eq3[i].set_color(SHAPE_COLOR)
        for i in [7, 9, 11]:
            eq3[i].set_color(HIGHLIGHT_COLOR)
        eq3.next_to(eq2, DOWN, buff=0.35)
        self.play(Write(eq3), run_time=T_KEY_EQUATION)
        self.wait(2)

        # Cancellation note
        cancel_text = MathTex(
            r"\text{Vektoret } \vec{b} \text{ anulohen!}",
            font_size=BODY_SIZE, color=HIGHLIGHT_COLOR,
        )
        cancel_text.next_to(eq3, DOWN, buff=0.35)
        self.play(FadeIn(cancel_text), run_time=0.6)
        self.wait(1.5)

        # Answer
        ans = MathTex(
            r"\vec{q} + 2\vec{r} = -\vec{a}",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        ans.next_to(cancel_text, DOWN, buff=0.45)
        box = make_answer_box(ans)
        self.play(Write(ans), run_time=T_KEY_EQUATION)
        self.play(Create(box), run_time=0.5)
        self.wait(3)

    # ── Sub-part iii: q + r ──

    def _part_a_iii(self):
        t0 = self._ctitle("iii)  Gjeni:", y_pos=3.2)
        eq0 = self._ceq(
            r"\vec{q} + \vec{r} = \text{ ?}",
            t0, fs=36, buff=0.4,
        )
        self.wait(1.5)

        # Substitute + distribute (combined since pattern is established)
        t1 = self._ctitle("Zevendesojme dhe shprehim:", ref=eq0, buff=0.45)

        eq1 = self._ceq(
            r"= (\vec{a} - 2\vec{b}) + (\vec{b} - \vec{a})",
            t1, fs=30,
        )
        self.wait(1.5)

        eq2 = self._ceq(
            r"= \vec{a} - 2\vec{b} + \vec{b} - \vec{a}",
            eq1, fs=32,
        )
        self.wait(1.5)

        # Collect like terms
        eq3 = MathTex(
            r"= (",
            r"1", r"-", r"1",
            r")", r"\vec{a}",
            r" + (",
            r"-2", r"+", r"1",
            r")", r"\vec{b}",
            font_size=32,
        )
        for i in [1, 3, 5]:
            eq3[i].set_color(SHAPE_COLOR)
        for i in [7, 9, 11]:
            eq3[i].set_color(HIGHLIGHT_COLOR)
        eq3.next_to(eq2, DOWN, buff=0.35)
        self.play(Write(eq3), run_time=T_KEY_EQUATION)
        self.wait(2)

        # Cancellation
        cancel_text = MathTex(
            r"\text{Vektoret } \vec{a} \text{ anulohen!}",
            font_size=BODY_SIZE, color=SHAPE_COLOR,
        )
        cancel_text.next_to(eq3, DOWN, buff=0.35)
        self.play(FadeIn(cancel_text), run_time=0.6)
        self.wait(1.5)

        # Answer
        ans = MathTex(
            r"\vec{q} + \vec{r} = -\vec{b}",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        ans.next_to(cancel_text, DOWN, buff=0.45)
        box = make_answer_box(ans)
        self.play(Write(ans), run_time=T_KEY_EQUATION)
        self.play(Create(box), run_time=0.5)
        self.wait(3)

    # ── Sub-part iv: 3q - p ──

    def _part_a_iv(self):
        t0 = self._ctitle("iv)  Gjeni:", y_pos=3.2)
        eq0 = self._ceq(
            r"3\vec{q} - \vec{p} = \text{ ?}",
            t0, fs=36, buff=0.4,
        )
        self.wait(1.5)

        # Substitute
        t1 = self._ctitle("Zevendesojme:", ref=eq0, buff=0.45)

        eq1 = self._ceq(
            r"= 3(\vec{a} - 2\vec{b}) - (3\vec{a} + 4\vec{b})",
            t1, fs=30,
        )
        self.wait(1.5)

        # Distribute
        t2 = self._ctitle("Shprehim:", ref=eq1, buff=0.4)

        eq2 = self._ceq(
            r"= 3\vec{a} - 6\vec{b} - 3\vec{a} - 4\vec{b}",
            t2, fs=32,
        )
        self.wait(2)

        # Collect like terms
        eq3 = MathTex(
            r"= (",
            r"3", r"-", r"3",
            r")", r"\vec{a}",
            r" + (",
            r"-6", r"-", r"4",
            r")", r"\vec{b}",
            font_size=32,
        )
        for i in [1, 3, 5]:
            eq3[i].set_color(SHAPE_COLOR)
        for i in [7, 9, 11]:
            eq3[i].set_color(HIGHLIGHT_COLOR)
        eq3.next_to(eq2, DOWN, buff=0.35)
        self.play(Write(eq3), run_time=T_KEY_EQUATION)
        self.wait(2)

        # Cancellation
        cancel_text = MathTex(
            r"\text{Vektoret } \vec{a} \text{ anulohen!}",
            font_size=BODY_SIZE, color=SHAPE_COLOR,
        )
        cancel_text.next_to(eq3, DOWN, buff=0.35)
        self.play(FadeIn(cancel_text), run_time=0.6)
        self.wait(1.5)

        # Answer
        ans = MathTex(
            r"3\vec{q} - \vec{p} = -10\vec{b}",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        ans.next_to(cancel_text, DOWN, buff=0.45)
        box = make_answer_box(ans)
        self.play(Write(ans), run_time=T_KEY_EQUATION)
        self.play(Create(box), run_time=0.5)
        self.wait(3)

    # ================================================================
    #  PART B — What can you say about these vectors?
    # ================================================================

    def part_b(self):
        header = self.show_part_header("b")

        # ── Problem statement ──
        prob_title = MathTex(
            r"\text{Cfare mund te thoni per vektoret?}",
            font_size=STEP_TITLE_SIZE + 4, color=STEP_TITLE_COLOR,
        )
        self.show_problem(prob_title, wait_time=3.0)

        # ────────────────────────────────────────
        # B.i) p+2q = 5a  and  q+2r = -a  -- both parallel to a
        # ────────────────────────────────────────
        self._part_b_i()
        fade_all(self)
        self.wait(0.5)

        # ────────────────────────────────────────
        # B.ii) q+r = -b  and  3q-p = -10b  -- both parallel to b
        # ────────────────────────────────────────
        self._part_b_ii()

    def _part_b_i(self):
        """Compare p+2q = 5a and q+2r = -a: both parallel to a."""
        title = MathTex(
            r"\text{Krahasojme:}",
            font_size=STEP_TITLE_SIZE + 2, color=STEP_TITLE_COLOR,
        )
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.5)

        # Show both results
        res1 = MathTex(
            r"\vec{p} + 2\vec{q} = ", r"5\vec{a}",
            font_size=34,
        )
        res1[1].set_color(SHAPE_COLOR)
        res2 = MathTex(
            r"\vec{q} + 2\vec{r} = ", r"-\vec{a}",
            font_size=34,
        )
        res2[1].set_color(SHAPE_COLOR)

        eqs = VGroup(res1, res2).arrange(DOWN, buff=0.4)
        eqs.next_to(title, DOWN, buff=0.6)

        self.play(Write(res1), run_time=T_ROUTINE_EQUATION)
        self.wait(1)
        self.play(Write(res2), run_time=T_ROUTINE_EQUATION)
        self.wait(2)

        # Explanation text
        exp1 = MathTex(
            r"\text{Te dy jane shumefisha te } \vec{a}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        exp1.next_to(eqs, DOWN, buff=0.5)
        self.play(FadeIn(exp1), run_time=T_BODY_FADE)
        self.wait(2)

        exp2 = MathTex(
            r"\Rightarrow \text{ Te dy jane paralele me } \vec{a}",
            font_size=BODY_SIZE + 2, color=ANSWER_COLOR,
        )
        exp2.next_to(exp1, DOWN, buff=0.35)
        self.play(FadeIn(exp2), run_time=T_BODY_FADE)
        self.wait(2.5)

        # Fade text, show vector diagram
        self.play(
            FadeOut(VGroup(title, eqs, exp1, exp2)),
            run_time=0.7,
        )

        # ── Visual: vector arrows showing parallel / opposite ──
        self._show_parallel_a_diagram()

    def _show_parallel_a_diagram(self):
        """Show 5a and -a as arrows: parallel, different lengths, opposite sense."""
        info = MathTex(
            r"\text{Paralele me } \vec{a}\text{:}",
            font_size=28, color=STEP_TITLE_COLOR,
        )
        info.to_edge(UP, buff=0.5)
        self.play(FadeIn(info), run_time=0.5)

        a_unit = np.array([1.0, 0, 0])
        scale = 0.55

        # Base vector a
        origin_a = LEFT * 5 + UP * 1.5
        arr_base = self._vec_arrow(
            origin_a, origin_a + a_unit * scale,
            color=SHAPE_COLOR, stroke_width=3,
        )
        lbl_base = MathTex(r"\vec{a}", font_size=24, color=SHAPE_COLOR)
        lbl_base.next_to(arr_base, UP, buff=0.12)
        self.play(GrowArrow(arr_base), FadeIn(lbl_base), run_time=0.6)
        self.wait(1)

        # 5a: long arrow pointing right
        origin_5a = LEFT * 5 + DOWN * 0.2
        end_5a = origin_5a + 5 * a_unit * scale
        arr_5a = self._vec_arrow(
            origin_5a, end_5a,
            color=ANSWER_COLOR, stroke_width=5,
        )
        lbl_5a = MathTex(
            r"\vec{p}+2\vec{q} = 5\vec{a}",
            font_size=24, color=ANSWER_COLOR,
        )
        lbl_5a.next_to(arr_5a, UP, buff=0.15)
        self.play(GrowArrow(arr_5a), FadeIn(lbl_5a), run_time=0.8)
        self.wait(1.5)

        # -a: short arrow pointing left (opposite direction)
        origin_neg = LEFT * 5 + DOWN * 1.8
        end_neg = origin_neg - a_unit * scale
        arr_neg = self._vec_arrow(
            origin_neg, end_neg,
            color=AUX_COLOR, stroke_width=5,
        )
        lbl_neg = MathTex(
            r"\vec{q}+2\vec{r} = -\vec{a}",
            font_size=24, color=AUX_COLOR,
        )
        lbl_neg.next_to(arr_neg, UP, buff=0.15)
        self.play(GrowArrow(arr_neg), FadeIn(lbl_neg), run_time=0.8)
        self.wait(2)

        # Annotations
        note1 = MathTex(
            r"5\vec{a} \text{ eshte 5 here me i gjate se } \vec{a}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        note1.move_to(DOWN * 2.8 + LEFT * 0.5)
        self.play(FadeIn(note1), run_time=0.6)
        self.wait(2)

        note2 = MathTex(
            r"-\vec{a} \text{ ka drejtim te kundert}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        note2.next_to(note1, DOWN, buff=0.3)
        self.play(FadeIn(note2), run_time=0.6)
        self.wait(3)

    def _part_b_ii(self):
        """Compare q+r = -b and 3q-p = -10b: both parallel to b."""
        title = MathTex(
            r"\text{Krahasojme:}",
            font_size=STEP_TITLE_SIZE + 2, color=STEP_TITLE_COLOR,
        )
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.5)

        # Show both results
        res1 = MathTex(
            r"\vec{q} + \vec{r} = ", r"-\vec{b}",
            font_size=34,
        )
        res1[1].set_color(HIGHLIGHT_COLOR)
        res2 = MathTex(
            r"3\vec{q} - \vec{p} = ", r"-10\vec{b}",
            font_size=34,
        )
        res2[1].set_color(HIGHLIGHT_COLOR)

        eqs = VGroup(res1, res2).arrange(DOWN, buff=0.4)
        eqs.next_to(title, DOWN, buff=0.6)

        self.play(Write(res1), run_time=T_ROUTINE_EQUATION)
        self.wait(1)
        self.play(Write(res2), run_time=T_ROUTINE_EQUATION)
        self.wait(2)

        # Explanation
        exp1 = MathTex(
            r"\text{Te dy jane shumefisha te } \vec{b}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        exp1.next_to(eqs, DOWN, buff=0.5)
        self.play(FadeIn(exp1), run_time=T_BODY_FADE)
        self.wait(2)

        exp2 = MathTex(
            r"\Rightarrow \text{ Te dy jane paralele me } \vec{b}",
            font_size=BODY_SIZE + 2, color=ANSWER_COLOR,
        )
        exp2.next_to(exp1, DOWN, buff=0.35)
        self.play(FadeIn(exp2), run_time=T_BODY_FADE)
        self.wait(2.5)

        # Fade text, show diagram
        self.play(
            FadeOut(VGroup(title, eqs, exp1, exp2)),
            run_time=0.7,
        )

        self._show_parallel_b_diagram()

    def _show_parallel_b_diagram(self):
        """Show -b and -10b as arrows: parallel, -10b is 10x longer."""
        info = MathTex(
            r"\text{Paralele me } \vec{b}\text{:}",
            font_size=28, color=STEP_TITLE_COLOR,
        )
        info.to_edge(UP, buff=0.5)
        self.play(FadeIn(info), run_time=0.5)

        b_unit = np.array([0.5, 0.866, 0])
        scale = 0.6

        # Base vector b
        origin_b = LEFT * 5 + UP * 1.0
        arr_base = self._vec_arrow(
            origin_b, origin_b + b_unit * scale,
            color=HIGHLIGHT_COLOR, stroke_width=3,
        )
        lbl_base = MathTex(r"\vec{b}", font_size=24, color=HIGHLIGHT_COLOR)
        lbl_base.next_to(arr_base, RIGHT, buff=0.12)
        self.play(GrowArrow(arr_base), FadeIn(lbl_base), run_time=0.6)
        self.wait(1)

        # -b: short arrow in opposite direction
        origin_neg = LEFT * 2 + UP * 1.5
        end_neg = origin_neg - b_unit * scale
        arr_negb = self._vec_arrow(
            origin_neg, end_neg,
            color=ANSWER_COLOR, stroke_width=5,
        )
        lbl_negb = MathTex(
            r"\vec{q}+\vec{r} = -\vec{b}",
            font_size=24, color=ANSWER_COLOR,
        )
        lbl_negb.next_to(arr_negb, RIGHT, buff=0.15)
        self.play(GrowArrow(arr_negb), FadeIn(lbl_negb), run_time=0.8)
        self.wait(1.5)

        # -10b: very long arrow in opposite direction (scaled down for screen)
        # Show it at a reduced visual scale to fit, but indicate it is 10x
        origin_10 = RIGHT * 2 + UP * 2.5
        end_10 = origin_10 - b_unit * scale * 5  # visual = 5x (screen limit)
        arr_10b = self._vec_arrow(
            origin_10, end_10,
            color=AUX_COLOR, stroke_width=5,
        )
        lbl_10b = MathTex(
            r"3\vec{q}-\vec{p} = -10\vec{b}",
            font_size=24, color=AUX_COLOR,
        )
        lbl_10b.next_to(arr_10b, RIGHT, buff=0.15)
        self.play(GrowArrow(arr_10b), FadeIn(lbl_10b), run_time=0.8)
        self.wait(2)

        # Annotations
        note1 = MathTex(
            r"-10\vec{b} \text{ eshte 10 here me i gjate se } \vec{b}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        note1.move_to(DOWN * 2.5)
        self.play(FadeIn(note1), run_time=0.6)
        self.wait(2)

        note2 = MathTex(
            r"\text{Te dy kane drejtim te kundert me } \vec{b}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        note2.next_to(note1, DOWN, buff=0.3)
        self.play(FadeIn(note2), run_time=0.6)
        self.wait(3)

    # ================================================================
    #  FINAL SUMMARY
    # ================================================================

    def final_summary(self):
        self.show_summary_table(
            "Permbledhje",
            [
                r"\text{i)} \quad \vec{p} + 2\vec{q} = 5\vec{a}",
                r"\text{ii)} \quad \vec{q} + 2\vec{r} = -\vec{a}",
                r"\text{iii)} \quad \vec{q} + \vec{r} = -\vec{b}",
                r"\text{iv)} \quad 3\vec{q} - \vec{p} = -10\vec{b}",
                r"",
                r"\text{i), ii) paralele me } \vec{a}",
                r"\text{iii), iv) paralele me } \vec{b}",
            ],
            font_size=30,
        )
