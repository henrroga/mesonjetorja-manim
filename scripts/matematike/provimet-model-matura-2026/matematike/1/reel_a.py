"""
Reel A — Ushtrimi 1, Matematikë
Provimet Model Matura 2026

A = {x ∈ ℕ | 3 < x < 100}, B = {x ∈ ℕ | 3^x ∈ A}
Sa elemente ka B?  Përgjigja: C) 3

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

        # Set definitions
        set_a = MathTex(
            r"A = \{ x \in \mathbb{N} \mid 3 < x < 100 \}",
            font_size=EQ_SIZE, color=WHITE,
        )
        set_b = MathTex(
            r"B = \{ x \in \mathbb{N} \mid 3^x \in A \}",
            font_size=EQ_SIZE, color=WHITE,
        )
        question = MathTex(
            r"\text{Sa elemente ka } B \text{?}",
            font_size=QUESTION_SIZE, color=HIGHLIGHT_COLOR,
        )

        defs = VGroup(set_a, set_b, question).arrange(DOWN, buff=0.5)
        defs.move_to(UP * 1.5)

        self.play(Write(set_a), run_time=0.8)
        self.wait(0.6)
        self.play(Write(set_b), run_time=0.8)
        self.wait(0.6)
        self.play(FadeIn(question, shift=UP * 0.2), run_time=0.5)
        self.wait(0.5)

        # Options in 2x2 grid
        opt_a = MathTex(r"\text{A) } 1", font_size=BODY_SIZE, color=WHITE)
        opt_b = MathTex(r"\text{B) } 2", font_size=BODY_SIZE, color=WHITE)
        opt_c = MathTex(r"\text{C) } 3", font_size=BODY_SIZE, color=WHITE)
        opt_d = MathTex(r"\text{D) } 4", font_size=BODY_SIZE, color=WHITE)

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
    #  SOLVE (8–30s): Check each power of 3
    # ────────────────────────────────────────────

    def solve(self):
        # Restate condition compactly
        cond_title = MathTex(
            r"\text{Kushti: }",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        cond_title.move_to(UP * SAFE_TOP)

        cond = MathTex(
            r"3 < 3^x < 100",
            font_size=EQ_SIZE, color=WHITE,
        )
        cond.next_to(cond_title, DOWN, buff=0.4)

        self.play(FadeIn(cond_title), run_time=0.3)
        self.play(Write(cond), run_time=0.7)
        self.wait(1.0)

        # Check each x
        checks_data = [
            (1, 3,   False, r"3^1 = 3",   r"3 \not> 3",     r"\times"),
            (2, 9,   True,  r"3^2 = 9",   r"3 < 9 < 100",   r"\checkmark"),
            (3, 27,  True,  r"3^3 = 27",  r"3 < 27 < 100",  r"\checkmark"),
            (4, 81,  True,  r"3^4 = 81",  r"3 < 81 < 100",  r"\checkmark"),
            (5, 243, False, r"3^5 = 243", r"243 \not< 100",  r"\times"),
        ]

        check_rows = VGroup()
        for x_val, _, is_in, power_tex, reason_tex, mark in checks_data:
            color = ANSWER_COLOR if is_in else AUX_COLOR
            row = MathTex(
                r"x=" + str(x_val) + r": \;" + power_tex
                + r" \;\to\; " + reason_tex + r" \;" + mark,
                font_size=SMALL_SIZE, color=color,
            )
            check_rows.add(row)

        check_rows.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        check_rows.next_to(cond, DOWN, buff=0.6)
        check_rows.set_x(0)

        for row in check_rows:
            self.play(FadeIn(row, shift=RIGHT * 0.3), run_time=0.5)
            self.wait(0.6)

        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # ────────────────────────────────────────────
    #  ANSWER (30–40s): B = {2,3,4}, answer C
    # ────────────────────────────────────────────

    def answer(self):
        result_b = MathTex(
            r"B = \{ 2, \, 3, \, 4 \}",
            font_size=EQ_SIZE, color=ANSWER_COLOR,
        )
        result_b.move_to(UP * 2.0)

        card_b = MathTex(
            r"|B| = 3",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        card_b.next_to(result_b, DOWN, buff=0.5)

        self.play(Write(result_b), run_time=0.8)
        self.wait(0.8)
        self.play(Write(card_b), run_time=0.7)
        self.wait(0.6)

        # Answer box
        ans_group = VGroup(result_b, card_b)
        box = make_answer_box(ans_group)
        self.play(Create(box), run_time=0.4)

        # Correct option
        answer_c = MathTex(
            r"\text{Përgjigja: C)}",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        answer_c.next_to(box, DOWN, buff=0.6)
        self.play(GrowFromCenter(answer_c), run_time=0.7)

        self.play(
            Flash(answer_c.get_center(), color=ANSWER_COLOR,
                  line_length=0.25, num_lines=12, run_time=0.6),
        )
        self.play(
            Circumscribe(VGroup(ans_group, box), color=HIGHLIGHT_COLOR, run_time=0.8),
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
