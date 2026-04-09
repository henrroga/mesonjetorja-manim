"""
Reel E — Ushtrimi 9, Njësia 9.1A
Vargu: 1/2, -1/4, -1, -7/4, -5/2, ...  →  aₙ = 5/4 − (3/4)n

Standalone vertical reel: hook, solve, answer + CTA.
Uses fractions throughout — careful LaTeX formatting.
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
HOOK_SIZE = 36
QUESTION_SIZE = 40
EQ_SIZE = 34
ANSWER_SIZE = 40
BODY_SIZE = 30
SMALL_SIZE = 26


class ReelE(Scene):
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
            r"\frac{1}{2}, \; -\frac{1}{4}, \; -1, \; -\frac{7}{4}, \; -\frac{5}{2}, \; \ldots",
            font_size=44, color=WHITE,
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

        answer_tease = MathTex(r"-\frac{13}{4}", font_size=56, color=ANSWER_COLOR)
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

        # Show difference calculation
        diff_title = MathTex(
            r"\text{Gjejmë diferencën:}",
            font_size=SMALL_SIZE, color=BODY_TEXT_COLOR,
        )
        diff_title.move_to(UP * 3.5)
        self.play(FadeIn(diff_title), run_time=0.4)

        diff_calc = MathTex(
            r"d = -\frac{1}{4} - \frac{1}{2} = -\frac{1}{4} - \frac{2}{4} = -\frac{3}{4}",
            font_size=EQ_SIZE, color=WHITE,
        )
        diff_calc.next_to(diff_title, DOWN, buff=0.4)
        self.play(Write(diff_calc), run_time=1.0)
        self.wait(1.2)

        # d and a₁
        d_eq = MathTex(
            r"d = -\frac{3}{4}",
            font_size=EQ_SIZE, color=LABEL_COLOR,
        )
        d_eq.next_to(diff_calc, DOWN, buff=0.5)
        self.play(Write(d_eq), run_time=0.6)
        self.wait(0.6)

        a1_eq = MathTex(
            r"a_1 = \frac{1}{2}",
            font_size=EQ_SIZE, color=LABEL_COLOR,
        )
        a1_eq.next_to(d_eq, DOWN, buff=0.4)
        self.play(Write(a1_eq), run_time=0.6)
        self.wait(0.8)

        # Substitute
        sub_title = MathTex(
            r"\text{Zëvendësojmë në formulë:}",
            font_size=SMALL_SIZE, color=BODY_TEXT_COLOR,
        )
        sub_title.next_to(a1_eq, DOWN, buff=0.5)
        self.play(FadeIn(sub_title), run_time=0.4)

        step1 = MathTex(
            r"a_n = \frac{1}{2} + (n-1) \cdot \left(-\frac{3}{4}\right)",
            font_size=EQ_SIZE, color=WHITE,
        )
        step1.next_to(sub_title, DOWN, buff=0.4)
        self.play(Write(step1), run_time=0.9)
        self.wait(1.0)

        # Expand
        step2 = MathTex(
            r"a_n = \frac{1}{2} - \frac{3}{4}n + \frac{3}{4}",
            font_size=EQ_SIZE, color=WHITE,
        )
        step2.next_to(step1, DOWN, buff=0.4)
        self.play(Write(step2), run_time=0.8)
        self.wait(0.8)

        # Simplify: 1/2 + 3/4 = 2/4 + 3/4 = 5/4
        step3 = MathTex(
            r"a_n = \frac{2}{4} + \frac{3}{4} - \frac{3}{4}n",
            font_size=EQ_SIZE, color=WHITE,
        )
        step3.next_to(step2, DOWN, buff=0.4)
        self.play(Write(step3), run_time=0.8)
        self.wait(0.8)

        # Final
        step4 = MathTex(
            r"a_n = \frac{5}{4} - \frac{3}{4}n",
            font_size=EQ_SIZE, color=ANSWER_COLOR,
        )
        step4.next_to(step3, DOWN, buff=0.4)
        self.play(Write(step4), run_time=0.7)
        self.wait(1.5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # ────────────────────────────────────────────
    #  ANSWER (25–35s)
    # ────────────────────────────────────────────

    def answer(self):
        ans = MathTex(
            r"a_n = \frac{5}{4} - \frac{3}{4}n",
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
            r"a_1 = \frac{5}{4} - \frac{3}{4} = \frac{2}{4} = \frac{1}{2} \;\checkmark",
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
