"""
Reel D — Ushtrimi 5, Njësia 10.2A
Ekuacioni: 3x² + 3x - 2 = 0
a=3, b=3, c=-2, D=33, x=(-3±√33)/6, x₁≈0,5  x₂≈-1,5

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


class ReelD(Scene):
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
            r"3x^2 + 3x - 2 = 0",
            font_size=48, color=WHITE,
        )
        eq.move_to(UP * 3.0)

        question = MathTex(
            r"\text{Sa është } x \text{ ?}",
            font_size=QUESTION_SIZE, color=LABEL_COLOR,
        )
        question.move_to(UP * 0.5)

        self.play(FadeIn(eq, shift=UP * 0.3), run_time=0.8)
        self.wait(1.5)
        self.play(FadeIn(question, shift=UP * 0.2), run_time=0.6)
        self.wait(3.0)

        # Show quadratic formula
        formula = MathTex(
            r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}",
            font_size=EQ_SIZE, color=SHAPE_COLOR,
        )
        formula.move_to(DOWN * 1.5)
        self.play(Write(formula), run_time=0.8)
        self.wait(2.0)

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

        # Restate equation
        eq = MathTex(
            r"3x^2 + 3x - 2 = 0",
            font_size=EQ_SIZE, color=WHITE,
        )
        eq.move_to(UP * 3.5)
        self.play(Write(eq), run_time=0.6)
        self.wait(0.5)

        # Identify a, b, c
        abc = MathTex(
            r"a = 3, \quad b = 3, \quad c = -2",
            font_size=EQ_SIZE, color=LABEL_COLOR,
        )
        abc.move_to(UP * 2.5)
        self.play(Write(abc), run_time=0.7)
        self.wait(0.8)

        # Discriminant
        d_title = MathTex(
            r"\text{Diskriminanta:}",
            font_size=SMALL_SIZE, color=BODY_TEXT_COLOR,
        )
        d_title.move_to(UP * 1.6)
        self.play(FadeIn(d_title), run_time=0.3)

        d_calc = MathTex(
            r"D = 3^2 - 4 \cdot 3 \cdot (-2)",
            font_size=EQ_SIZE, color=WHITE,
        )
        d_calc.move_to(UP * 0.9)
        self.play(Write(d_calc), run_time=0.7)
        self.wait(0.5)

        d_result = MathTex(
            r"D = 9 + 24 = 33",
            font_size=EQ_SIZE, color=ANSWER_COLOR,
        )
        d_result.move_to(UP * 0.1)
        self.play(Write(d_result), run_time=0.7)
        self.wait(1.0)

        d_pos = MathTex(
            r"D > 0 \;\Rightarrow\; \text{dy zgjidhje reale}",
            font_size=SMALL_SIZE, color=STEP_TITLE_COLOR,
        )
        d_pos.move_to(DOWN * 0.7)
        self.play(FadeIn(d_pos, shift=UP * 0.2), run_time=0.5)
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
            r"x = \frac{-3 \pm \sqrt{33}}{2 \cdot 3}",
            font_size=EQ_SIZE, color=WHITE,
        )
        x_sub.move_to(UP * 2.0)
        self.play(Write(x_sub), run_time=0.7)
        self.wait(0.5)

        x_simp = MathTex(
            r"x = \frac{-3 \pm \sqrt{33}}{6}",
            font_size=EQ_SIZE, color=WHITE,
        )
        x_simp.move_to(UP * 1.0)
        self.play(Write(x_simp), run_time=0.6)
        self.wait(0.5)

        sqrt_note = MathTex(
            r"\sqrt{33} \approx 5{,}74",
            font_size=SMALL_SIZE, color=BODY_TEXT_COLOR,
        )
        sqrt_note.move_to(UP * 0.2)
        self.play(FadeIn(sqrt_note), run_time=0.4)
        self.wait(0.5)

        # x1
        x1_eq = MathTex(
            r"x_1 = \frac{-3 + 5{,}74}{6} = \frac{2{,}74}{6} \approx 0{,}5",
            font_size=EQ_SIZE, color=ANSWER_COLOR,
        )
        x1_eq.move_to(DOWN * 0.8)
        self.play(Write(x1_eq), run_time=0.8)
        self.wait(0.8)

        # x2
        x2_eq = MathTex(
            r"x_2 = \frac{-3 - 5{,}74}{6} = \frac{-8{,}74}{6} \approx -1{,}5",
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
            r"x_1 \approx 0{,}5",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        ans1.move_to(UP * 1.5)

        ans2 = MathTex(
            r"x_2 \approx -1{,}5",
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
