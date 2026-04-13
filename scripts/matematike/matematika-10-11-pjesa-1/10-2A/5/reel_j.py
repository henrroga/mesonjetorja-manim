"""
Reel J — Ushtrimi 5, Njësia 10.2A (Pjesa 10)
Ekuacioni: 0 = 4x² + 11x - 18  →  rirendisim: 4x² + 11x - 18 = 0
a=4, b=11, c=-18, D=409, x₁≈1,2  x₂≈-3,9

Standalone vertical reel: hook, rearrange, solve, answer + CTA.
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


class ReelJ(Scene):
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
        eq = MathTex(
            r"0 = 4x^2 + 11x - 18",
            font_size=48, color=WHITE,
        )
        eq.move_to(UP * 3.0)

        question = MathTex(
            r"\text{Zgjidhe ekuacionin!}",
            font_size=QUESTION_SIZE, color=LABEL_COLOR,
        )
        question.move_to(UP * 0.5)

        self.play(FadeIn(eq, shift=UP * 0.3), run_time=0.8)
        self.wait(1.5)
        self.play(FadeIn(question, shift=UP * 0.2), run_time=0.6)
        self.wait(3.0)

        # Hint: flip it around
        hint = MathTex(
            r"\text{Kujdes: ktheje në formë standarde!}",
            font_size=SMALL_SIZE, color=HIGHLIGHT_COLOR,
        )
        hint.move_to(DOWN * 1.5)
        self.play(FadeIn(hint, shift=UP * 0.2), run_time=0.5)
        self.wait(1.5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # ────────────────────────────────────────────
    #  SOLVE (8–35s)
    # ────────────────────────────────────────────

    def solve(self):
        title = MathTex(
            r"\text{Zgjidhje}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        title.move_to(UP * SAFE_TOP)
        self.play(FadeIn(title), run_time=0.3)

        # Show original equation
        eq_orig = MathTex(
            r"0 = 4x^2 + 11x - 18",
            font_size=EQ_SIZE, color=WHITE,
        )
        eq_orig.move_to(UP * 3.5)
        self.play(Write(eq_orig), run_time=0.6)
        self.wait(0.5)

        # Rearrange
        rearr_label = MathTex(
            r"\text{Shkruajmë në formën standarde:}",
            font_size=SMALL_SIZE, color=BODY_TEXT_COLOR,
        )
        rearr_label.move_to(UP * 2.5)
        self.play(FadeIn(rearr_label), run_time=0.4)

        eq_std = MathTex(
            r"4x^2 + 11x - 18 = 0",
            font_size=EQ_SIZE, color=SHAPE_COLOR,
        )
        eq_std.move_to(UP * 1.7)
        self.play(Write(eq_std), run_time=0.7)
        self.wait(1.0)

        # Identify a, b, c
        abc = MathTex(
            r"a = 4, \quad b = 11, \quad c = -18",
            font_size=EQ_SIZE, color=LABEL_COLOR,
        )
        abc.move_to(UP * 0.7)
        self.play(Write(abc), run_time=0.7)
        self.wait(0.8)

        # Discriminant
        d_title = MathTex(
            r"\text{Dallori:}",
            font_size=SMALL_SIZE, color=BODY_TEXT_COLOR,
        )
        d_title.move_to(DOWN * 0.1)
        self.play(FadeIn(d_title), run_time=0.3)

        d_calc = MathTex(
            r"D = 11^2 - 4 \cdot 4 \cdot (-18)",
            font_size=EQ_SIZE, color=WHITE,
        )
        d_calc.move_to(DOWN * 0.8)
        self.play(Write(d_calc), run_time=0.7)
        self.wait(0.5)

        d_result = MathTex(
            r"D = 121 + 288 = 409",
            font_size=EQ_SIZE, color=ANSWER_COLOR,
        )
        d_result.move_to(DOWN * 1.6)
        self.play(Write(d_result), run_time=0.7)
        self.wait(1.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

        # ── Calculate x ──
        x_title = MathTex(
            r"\text{Gjejmë zgjidhjet:}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        x_title.move_to(UP * SAFE_TOP)
        self.play(FadeIn(x_title), run_time=0.3)

        x_formula = MathTex(
            r"x = \frac{-b \pm \sqrt{D}}{2a}",
            font_size=EQ_SIZE, color=SHAPE_COLOR,
        )
        x_formula.move_to(UP * 3.2)
        self.play(Write(x_formula), run_time=0.6)
        self.wait(0.5)

        x_sub = MathTex(
            r"x = \frac{-11 \pm \sqrt{409}}{2 \cdot 4}",
            font_size=EQ_SIZE, color=WHITE,
        )
        x_sub.move_to(UP * 2.0)
        self.play(Write(x_sub), run_time=0.7)
        self.wait(0.5)

        x_simp = MathTex(
            r"x = \frac{-11 \pm \sqrt{409}}{8}",
            font_size=EQ_SIZE, color=WHITE,
        )
        x_simp.move_to(UP * 1.0)
        self.play(Write(x_simp), run_time=0.6)
        self.wait(0.5)

        sqrt_note = MathTex(
            r"\sqrt{409} \approx 20{,}22",
            font_size=SMALL_SIZE, color=BODY_TEXT_COLOR,
        )
        sqrt_note.move_to(UP * 0.2)
        self.play(FadeIn(sqrt_note), run_time=0.4)
        self.wait(0.5)

        # x1
        x1_eq = MathTex(
            r"x_1 = \frac{-11 + 20{,}22}{8} = \frac{9{,}22}{8} \approx 1{,}2",
            font_size=EQ_SIZE, color=ANSWER_COLOR,
        )
        x1_eq.move_to(DOWN * 0.8)
        self.play(Write(x1_eq), run_time=0.8)
        self.wait(0.8)

        # x2
        x2_eq = MathTex(
            r"x_2 = \frac{-11 - 20{,}22}{8} = \frac{-31{,}22}{8} \approx -3{,}9",
            font_size=EQ_SIZE, color=ANSWER_COLOR,
        )
        x2_eq.move_to(DOWN * 2.0)
        self.play(Write(x2_eq), run_time=0.8)
        self.wait(1.5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # ────────────────────────────────────────────
    #  ANSWER (35–42s)
    # ────────────────────────────────────────────

    def answer(self):
        ans1 = MathTex(
            r"x_1 \approx 1{,}2",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        ans1.move_to(UP * 1.5)

        ans2 = MathTex(
            r"x_2 \approx -3{,}9",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        ans2.move_to(UP * 0.2)

        self.play(Write(ans1), run_time=0.6)
        self.play(Write(ans2), run_time=0.6)
        self.wait(0.5)

        box = make_answer_box(VGroup(ans1, ans2))
        self.play(Create(box), run_time=0.4)
        self.play(
            Flash(VGroup(ans1, ans2).get_center(), color=ANSWER_COLOR,
                  line_length=0.25, num_lines=12, run_time=0.6),
        )
        self.play(
            Circumscribe(VGroup(ans1, ans2, box), color=HIGHLIGHT_COLOR, run_time=0.8),
        )
        self.wait(2.0)

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
