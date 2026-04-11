"""
Reel A — Ushtrimi 3, Matematikë
Provimet Model Matura 2026

log x / log 0,1 = 2  (x > 0)
Gjej x.  Përgjigja: C) 0,01

Standalone vertical reel — hook, solve, answer.
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
EQ_SIZE = 38
ANSWER_SIZE = 44
BODY_SIZE = 32
SMALL_SIZE = 28


class ReelA(Scene):
    def construct(self):
        apply_style(self)
        MathTex.set_default(tex_template=ALBANIAN_TEX)
        Tex.set_default(tex_template=ALBANIAN_TEX)

        self.hook()
        self.solve()
        self.answer()
        self.cta()

    # ────────────────────────────────────────────
    #  HOOK (0–8s): Show equation + "Sa është x?"
    # ────────────────────────────────────────────

    def hook(self):
        # Matura badge
        badge = MathTex(
            r"\text{Matura 2026}",
            font_size=SMALL_SIZE, color=HIGHLIGHT_COLOR,
        )
        badge.move_to(UP * SAFE_TOP)
        self.play(FadeIn(badge, shift=DOWN * 0.2), run_time=0.4)

        # Main equation — the puzzle
        equation = MathTex(
            r"\frac{\log x}{\log 0{,}1} = 2",
            font_size=HOOK_SIZE, color=WHITE,
        )

        question = MathTex(
            r"\text{Sa është } x \text{?}",
            font_size=QUESTION_SIZE, color=HIGHLIGHT_COLOR,
        )

        hook_group = VGroup(equation, question).arrange(DOWN, buff=0.7)
        hook_group.move_to(ORIGIN)

        self.play(Write(equation), run_time=1.0)
        self.wait(1.0)
        self.play(FadeIn(question, shift=UP * 0.2), run_time=0.5)

        # Options in 2x2 grid
        opt_a = MathTex(r"\text{A) } 100", font_size=BODY_SIZE, color=WHITE)
        opt_b = MathTex(r"\text{B) } 0{,}1", font_size=BODY_SIZE, color=WHITE)
        opt_c = MathTex(r"\text{C) } 0{,}01", font_size=BODY_SIZE, color=WHITE)
        opt_d = MathTex(r"\text{D) } {-2}", font_size=BODY_SIZE, color=WHITE)

        row1 = VGroup(opt_a, opt_b).arrange(RIGHT, buff=1.5)
        row2 = VGroup(opt_c, opt_d).arrange(RIGHT, buff=1.5)
        opts = VGroup(row1, row2).arrange(DOWN, buff=0.4)
        opts.next_to(question, DOWN, buff=0.7)

        self.play(
            LaggedStart(
                FadeIn(opt_a, shift=UP * 0.2),
                FadeIn(opt_b, shift=UP * 0.2),
                FadeIn(opt_c, shift=UP * 0.2),
                FadeIn(opt_d, shift=UP * 0.2),
                lag_ratio=0.12,
            ),
            run_time=0.8,
        )
        self.wait(2.5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # ────────────────────────────────────────────
    #  SOLVE (8–28s): Step-by-step
    # ────────────────────────────────────────────

    def solve(self):
        # Step 1: Simplify log 0,1
        step1_title = MathTex(
            r"\text{Thjeshtojmë } \log 0{,}1 \text{:}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        step1_title.move_to(UP * SAFE_TOP)

        eq1 = MathTex(
            r"\log 0{,}1 = \log 10^{-1} = -1",
            font_size=EQ_SIZE, color=LABEL_COLOR,
        )
        eq1.next_to(step1_title, DOWN, buff=0.5)

        self.play(FadeIn(step1_title), run_time=0.3)
        self.play(Write(eq1), run_time=0.8)
        self.wait(1.5)

        # Step 2: Substitute
        step2_title = MathTex(
            r"\text{Zëvendësojmë:}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        step2_title.next_to(eq1, DOWN, buff=0.6)

        eq2 = MathTex(
            r"\frac{\log x}{-1} = 2",
            font_size=EQ_SIZE, color=WHITE,
        )
        eq2.next_to(step2_title, DOWN, buff=0.4)

        self.play(FadeIn(step2_title), run_time=0.3)
        self.play(Write(eq2), run_time=0.7)
        self.wait(1.0)

        # Step 3: Solve for log x
        eq3 = MathTex(
            r"\log x = -2",
            font_size=EQ_SIZE, color=LABEL_COLOR,
        )
        eq3.next_to(eq2, DOWN, buff=0.5)

        self.play(Write(eq3), run_time=0.7)
        self.wait(1.2)

        # Step 4: Definition of logarithm
        step4_title = MathTex(
            r"\text{Përkufizimi:}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        step4_title.next_to(eq3, DOWN, buff=0.6)

        eq4 = MathTex(
            r"x = 10^{-2} = 0{,}01",
            font_size=EQ_SIZE, color=ANSWER_COLOR,
        )
        eq4.next_to(step4_title, DOWN, buff=0.4)

        self.play(FadeIn(step4_title), run_time=0.3)
        self.play(Write(eq4), run_time=0.8)
        self.wait(1.5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # ────────────────────────────────────────────
    #  ANSWER (28–38s): Boxed answer + flash
    # ────────────────────────────────────────────

    def answer(self):
        result = MathTex(
            r"x = 0{,}01",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        result.move_to(UP * 1.5)

        self.play(Write(result), run_time=0.8)
        self.wait(0.6)

        box = make_answer_box(result)
        self.play(Create(box), run_time=0.4)

        # Correct option
        answer_c = MathTex(
            r"\text{Përgjigja: C) } 0{,}01",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        answer_c.next_to(box, DOWN, buff=0.6)
        self.play(GrowFromCenter(answer_c), run_time=0.7)

        self.play(
            Flash(answer_c.get_center(), color=ANSWER_COLOR,
                  line_length=0.25, num_lines=12, run_time=0.6),
        )
        self.play(
            Circumscribe(VGroup(result, box), color=HIGHLIGHT_COLOR, run_time=0.8),
        )
        self.wait(2.5)

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
