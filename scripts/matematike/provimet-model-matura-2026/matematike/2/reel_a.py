"""
Reel A — Ushtrimi 2, Matematikë
Provimet Model Matura 2026

Nëse 5% e numrit n është 22, vlera e n është:
A) 1000  B) 440  C) 400  D) 40
Përgjigja: B) 440

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
    #  HOOK (0–8s): Show the problem + options
    # ────────────────────────────────────────────

    def hook(self):
        # Matura badge
        badge = MathTex(
            r"\text{Matura 2026}",
            font_size=SMALL_SIZE, color=HIGHLIGHT_COLOR,
        )
        badge.move_to(UP * SAFE_TOP)
        self.play(FadeIn(badge, shift=DOWN * 0.2), run_time=0.4)

        # Question text
        question = MathTex(
            r"\text{Nëse 5\% e numrit } n",
            font_size=EQ_SIZE, color=WHITE,
        )
        question2 = MathTex(
            r"\text{është 22, vlera e } n \text{ është:}",
            font_size=EQ_SIZE, color=HIGHLIGHT_COLOR,
        )

        q_group = VGroup(question, question2).arrange(DOWN, buff=0.4)
        q_group.move_to(UP * 1.8)

        self.play(Write(question), run_time=0.8)
        self.wait(0.5)
        self.play(FadeIn(question2, shift=UP * 0.2), run_time=0.5)
        self.wait(0.5)

        # Options in 2x2 grid
        opt_a = MathTex(r"\text{A) } 1000", font_size=BODY_SIZE, color=WHITE)
        opt_b = MathTex(r"\text{B) } 440", font_size=BODY_SIZE, color=WHITE)
        opt_c = MathTex(r"\text{C) } 400", font_size=BODY_SIZE, color=WHITE)
        opt_d = MathTex(r"\text{D) } 40", font_size=BODY_SIZE, color=WHITE)

        row1 = VGroup(opt_a, opt_b).arrange(RIGHT, buff=1.5)
        row2 = VGroup(opt_c, opt_d).arrange(RIGHT, buff=1.5)
        opts = VGroup(row1, row2).arrange(DOWN, buff=0.4)
        opts.next_to(q_group, DOWN, buff=0.7)

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
    #  SOLVE (8–25s): Step-by-step calculation
    # ────────────────────────────────────────────

    def solve(self):
        # Step 1: Convert percentage
        step1 = MathTex(
            r"\text{Shprehim 5\% si numër dhjetor:}",
            font_size=SMALL_SIZE, color=STEP_TITLE_COLOR,
        )
        step1.move_to(UP * SAFE_TOP)

        pct_eq = MathTex(
            r"5\% = \frac{5}{100} = 0{,}05",
            font_size=EQ_SIZE, color=WHITE,
        )
        pct_eq.next_to(step1, DOWN, buff=0.5)

        self.play(FadeIn(step1), run_time=0.3)
        self.play(Write(pct_eq), run_time=0.8)
        self.wait(1.2)

        # Step 2: Set up equation
        step2 = MathTex(
            r"\text{Ndërtojmë ekuacionin:}",
            font_size=SMALL_SIZE, color=STEP_TITLE_COLOR,
        )
        step2.next_to(pct_eq, DOWN, buff=0.5)

        equation = MathTex(
            r"0{,}05 \cdot n = 22",
            font_size=EQ_SIZE, color=WHITE,
        )
        equation.next_to(step2, DOWN, buff=0.4)

        self.play(FadeIn(step2), run_time=0.3)
        self.play(Write(equation), run_time=0.7)
        self.wait(1.0)

        # Step 3: Isolate n
        step3 = MathTex(
            r"\text{Izolojmë } n \text{:}",
            font_size=SMALL_SIZE, color=STEP_TITLE_COLOR,
        )
        step3.next_to(equation, DOWN, buff=0.5)

        isolate = MathTex(
            r"n = \frac{22}{0{,}05}",
            font_size=EQ_SIZE, color=WHITE,
        )
        isolate.next_to(step3, DOWN, buff=0.4)

        self.play(FadeIn(step3), run_time=0.3)
        self.play(Write(isolate), run_time=0.7)
        self.wait(1.0)

        # Step 4: Compute
        step4 = MathTex(
            r"\text{Llogarisim:}",
            font_size=SMALL_SIZE, color=STEP_TITLE_COLOR,
        )
        step4.next_to(isolate, DOWN, buff=0.5)

        compute = MathTex(
            r"n = \frac{2200}{5} = 440",
            font_size=EQ_SIZE, color=ANSWER_COLOR,
        )
        compute.next_to(step4, DOWN, buff=0.4)

        self.play(FadeIn(step4), run_time=0.3)
        self.play(Write(compute), run_time=0.8)
        self.wait(1.5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # ────────────────────────────────────────────
    #  ANSWER (25–35s): Show final answer B) 440
    # ────────────────────────────────────────────

    def answer(self):
        result = MathTex(
            r"n = 440",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        result.move_to(UP * 2.0)

        self.play(Write(result), run_time=0.8)
        self.wait(0.8)

        # Answer box
        box = make_answer_box(result)
        self.play(Create(box), run_time=0.4)

        # Correct option
        answer_b = MathTex(
            r"\text{Përgjigja: B) 440}",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        answer_b.next_to(box, DOWN, buff=0.6)
        self.play(GrowFromCenter(answer_b), run_time=0.7)

        self.play(
            Flash(answer_b.get_center(), color=ANSWER_COLOR,
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
