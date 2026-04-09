"""
Reel C — Ushtrimi 9, Njësia 9.1A
Vargu: 5, 1, -3, -7, -11, ...  →  aₙ = 9 − 4n

Standalone vertical reel: hook, solve, answer + CTA.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))

from manim import *
import numpy as np
from style_guide import (
    apply_style, make_answer_box, BG_COLOR,
    STEP_TITLE_COLOR, BODY_TEXT_COLOR, LABEL_COLOR,
    ANSWER_COLOR, SHAPE_COLOR, AUX_COLOR, HIGHLIGHT_COLOR, DIVIDER_COLOR,
    ALBANIAN_TEX,
)

# ── Vertical 9:16 config ────────────────────
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 8
config.frame_height = 8 * (1920 / 1080)

# ── Safe zone ────────────────────────────────
SAFE_TOP = 4.8
SAFE_BOTTOM = -3.3

# ── Font sizes ───────────────────────────────
HOOK_SIZE = 38
QUESTION_SIZE = 42
EQ_SIZE = 36
ANSWER_SIZE = 42
BODY_SIZE = 30
SMALL_SIZE = 26


class ReelC(Scene):
    def construct(self):
        apply_style(self)
        MathTex.set_default(tex_template=ALBANIAN_TEX)
        Tex.set_default(tex_template=ALBANIAN_TEX)

        self.hook()
        self.solve()
        self.answer()
        self.cta()

    # ────────────────────────────────────────────
    #  HOOK (0–8s)
    # ────────────────────────────────────────────

    def hook(self):
        seq = MathTex(
            r"5, \; 1, \; {-3}, \; {-7}, \; {-11}, \; \ldots",
            font_size=48, color=WHITE,
        )
        seq.move_to(UP * 3.0)

        question = MathTex(
            r"\text{Cili numër vjen tjetër?}",
            font_size=QUESTION_SIZE, color=LABEL_COLOR,
        )
        question.move_to(UP * 0.5)

        self.play(FadeIn(seq, shift=UP * 0.3), run_time=0.8)
        self.wait(1.5)
        self.play(FadeIn(question, shift=UP * 0.2), run_time=0.6)
        self.wait(3.0)

        answer_tease = MathTex(r"-15", font_size=56, color=ANSWER_COLOR)
        answer_tease.move_to(DOWN * 1.5)
        self.play(GrowFromCenter(answer_tease), run_time=0.5)
        self.wait(0.8)

        real_q = MathTex(
            r"\text{Po kufiza e } n\text{-të?}",
            font_size=BODY_SIZE, color=HIGHLIGHT_COLOR,
        )
        real_q.move_to(DOWN * 3.0)
        self.play(FadeIn(real_q, shift=UP * 0.2), run_time=0.5)
        self.wait(1.5)

        # Formula reminder
        formula = MathTex(
            r"a_n = a_1 + (n-1) \cdot d",
            font_size=EQ_SIZE, color=SHAPE_COLOR,
        )
        formula.next_to(question, DOWN, buff=0.8)
        self.play(Write(formula), run_time=0.8)
        self.wait(2.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # ────────────────────────────────────────────
    #  SOLVE (8–25s)
    # ────────────────────────────────────────────

    def solve(self):
        title = MathTex(
            r"\text{Zgjidhje}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        title.move_to(UP * SAFE_TOP)
        self.play(FadeIn(title), run_time=0.3)

        # Show sequence with difference arrows
        terms = MathTex(
            r"5, \quad 1, \quad {-3}, \quad {-7}, \quad {-11}",
            font_size=EQ_SIZE, color=WHITE,
        )
        terms.move_to(UP * 3.2)
        self.play(Write(terms), run_time=0.7)
        self.wait(0.5)

        # Difference arrows
        arrow_group = VGroup()
        positions = [(-2.0, 3.2), (-0.7, 3.2), (0.65, 3.2), (2.05, 3.2)]
        for i, (x, y) in enumerate(positions):
            arr = CurvedArrow(
                np.array([x - 0.45, y + 0.3, 0]),
                np.array([x + 0.45, y + 0.3, 0]),
                angle=-TAU / 4,
                color=AUX_COLOR,
                stroke_width=2,
                tip_length=0.15,
            )
            lab = MathTex(r"-4", font_size=22, color=AUX_COLOR)
            lab.next_to(arr, UP, buff=0.05)
            arrow_group.add(VGroup(arr, lab))

        self.play(
            LaggedStart(*[FadeIn(a, shift=DOWN * 0.1) for a in arrow_group], lag_ratio=0.15),
            run_time=0.8,
        )
        self.wait(1.0)

        # d = -4
        d_eq = MathTex(r"d = -4", font_size=EQ_SIZE, color=LABEL_COLOR)
        d_eq.move_to(UP * 1.2)
        self.play(Write(d_eq), run_time=0.6)
        self.wait(0.8)

        # a₁ = 5
        a1_eq = MathTex(r"a_1 = 5", font_size=EQ_SIZE, color=LABEL_COLOR)
        a1_eq.next_to(d_eq, DOWN, buff=0.4)
        self.play(Write(a1_eq), run_time=0.6)
        self.wait(0.8)

        # Substitute
        sub_title = MathTex(
            r"\text{Zëvendësojmë në formulë:}",
            font_size=SMALL_SIZE, color=BODY_TEXT_COLOR,
        )
        sub_title.next_to(a1_eq, DOWN, buff=0.6)
        self.play(FadeIn(sub_title), run_time=0.4)

        step1 = MathTex(
            r"a_n = 5 + (n-1) \cdot (-4)",
            font_size=EQ_SIZE, color=WHITE,
        )
        step1.next_to(sub_title, DOWN, buff=0.4)
        self.play(Write(step1), run_time=0.8)
        self.wait(1.0)

        # Expand
        step2 = MathTex(
            r"a_n = 5 - 4n + 4",
            font_size=EQ_SIZE, color=WHITE,
        )
        step2.next_to(step1, DOWN, buff=0.4)
        self.play(Write(step2), run_time=0.7)
        self.wait(0.8)

        # Simplify
        step3 = MathTex(
            r"a_n = 9 - 4n",
            font_size=EQ_SIZE, color=ANSWER_COLOR,
        )
        step3.next_to(step2, DOWN, buff=0.4)
        self.play(Write(step3), run_time=0.7)
        self.wait(1.5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # ────────────────────────────────────────────
    #  ANSWER (25–35s)
    # ────────────────────────────────────────────

    def answer(self):
        ans = MathTex(
            r"a_n = 9 - 4n",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        ans.move_to(UP * 1.5)

        self.play(Write(ans), run_time=0.8)
        self.wait(0.6)

        box = make_answer_box(ans)
        self.play(Create(box), run_time=0.4)
        self.play(
            Flash(ans.get_center(), color=ANSWER_COLOR,
                  line_length=0.25, num_lines=12, run_time=0.6),
        )
        self.play(
            Circumscribe(VGroup(ans, box), color=HIGHLIGHT_COLOR, run_time=0.8),
        )
        self.wait(2.0)

        # Quick verification
        verify = MathTex(
            r"a_1 = 9 - 4(1) = 5 \;\checkmark",
            font_size=SMALL_SIZE, color=BODY_TEXT_COLOR,
        )
        verify.next_to(box, DOWN, buff=0.6)
        self.play(FadeIn(verify, shift=UP * 0.2), run_time=0.5)
        self.wait(1.5)

    # ────────────────────────────────────────────
    #  CTA
    # ────────────────────────────────────────────

    def cta(self):
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

        handle = MathTex(r"\text{mesonjetorja.com}", font_size=BODY_SIZE, color=WHITE)
        handle.move_to(UP * 0.5)
        tagline = MathTex(
            r"\text{Më shumë ushtrime në faqen tonë!}",
            font_size=SMALL_SIZE, color=BODY_TEXT_COLOR,
        )
        tagline.next_to(handle, DOWN, buff=0.4)

        self.play(GrowFromCenter(handle), FadeIn(tagline, shift=UP * 0.3), run_time=0.8)
        self.wait(1.5)
