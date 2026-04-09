"""
Reel A — Ushtrimi 21.16, Kapitulli 21
Fizika 10-11: Pjesa e Dytë (Botime Pegi)

Transformatori: 230V → 6V, Np = 6000
Ns ≈ 157, Is ≈ 1,53 A

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
    #  HOOK (0–8s): State the problem
    # ────────────────────────────────────────────

    def hook(self):
        # Topic badge
        badge = MathTex(
            r"\text{Transformatori}",
            font_size=SMALL_SIZE, color=HIGHLIGHT_COLOR,
        )
        badge.move_to(UP * SAFE_TOP)
        self.play(FadeIn(badge, shift=DOWN * 0.2), run_time=0.4)

        # The hook question
        line1 = MathTex(
            r"\text{Një radio punon me } 6 \text{ V.}",
            font_size=BODY_SIZE, color=WHITE,
        )
        line2 = MathTex(
            r"\text{Rrjeti jep } 230 \text{ V.}",
            font_size=BODY_SIZE, color=WHITE,
        )
        question = MathTex(
            r"\text{Sa mbështjella duhet dytësori?}",
            font_size=QUESTION_SIZE, color=LABEL_COLOR,
        )

        hook_group = VGroup(line1, line2, question).arrange(DOWN, buff=0.5)
        hook_group.move_to(UP * 1.5)

        self.play(Write(line1), run_time=0.7)
        self.wait(0.5)
        self.play(Write(line2), run_time=0.7)
        self.wait(0.5)
        self.play(FadeIn(question, shift=UP * 0.2), run_time=0.5)
        self.wait(2.5)

        # Show given data compactly
        data = MathTex(
            r"V_p = 230 \text{ V}, \quad V_s = 6{,}0 \text{ V}, \quad N_p = 6000",
            font_size=SMALL_SIZE, color=BODY_TEXT_COLOR,
        )
        data.next_to(hook_group, DOWN, buff=0.7)
        self.play(FadeIn(data, shift=UP * 0.2), run_time=0.5)
        self.wait(1.5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # ────────────────────────────────────────────
    #  SOLVE (8–25s): Both parts
    # ────────────────────────────────────────────

    def solve(self):
        # ── Part a: Ns ──
        part_a_hdr = MathTex(
            r"\text{a) Mbështjellat e dytësorit:}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        part_a_hdr.move_to(UP * SAFE_TOP)
        self.play(FadeIn(part_a_hdr), run_time=0.3)

        formula_a = MathTex(
            r"N_s = N_p \times \frac{V_s}{V_p}",
            font_size=EQ_SIZE, color=WHITE,
        )
        formula_a.move_to(UP * 2.5)
        self.play(Write(formula_a), run_time=0.8)
        self.wait(0.8)

        sub_a = MathTex(
            r"N_s = 6000 \times \frac{6{,}0}{230}",
            font_size=EQ_SIZE, color=WHITE,
        )
        sub_a.next_to(formula_a, DOWN, buff=0.5)
        self.play(Write(sub_a), run_time=0.8)
        self.wait(0.8)

        result_a = MathTex(
            r"N_s \approx 157 \text{ mbështjella}",
            font_size=EQ_SIZE, color=ANSWER_COLOR,
        )
        result_a.next_to(sub_a, DOWN, buff=0.5)
        self.play(Write(result_a), run_time=0.7)

        box_a = make_answer_box(result_a)
        self.play(Create(box_a), run_time=0.3)
        self.wait(1.5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

        # ── Part b: Is ──
        part_b_hdr = MathTex(
            r"\text{b) Rryma në dytësor } (I_p = 0{,}040 \text{ A}) \text{:}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        part_b_hdr.move_to(UP * SAFE_TOP)
        self.play(FadeIn(part_b_hdr), run_time=0.3)

        formula_b = MathTex(
            r"I_s = \frac{V_p \cdot I_p}{V_s}",
            font_size=EQ_SIZE, color=WHITE,
        )
        formula_b.move_to(UP * 2.5)
        self.play(Write(formula_b), run_time=0.8)
        self.wait(0.8)

        sub_b = MathTex(
            r"I_s = \frac{230 \times 0{,}040}{6{,}0}",
            font_size=EQ_SIZE, color=WHITE,
        )
        sub_b.next_to(formula_b, DOWN, buff=0.5)
        self.play(Write(sub_b), run_time=0.8)
        self.wait(0.6)

        compute_b = MathTex(
            r"I_s = \frac{9{,}2}{6{,}0}",
            font_size=EQ_SIZE, color=WHITE,
        )
        compute_b.next_to(sub_b, DOWN, buff=0.5)
        self.play(Write(compute_b), run_time=0.6)
        self.wait(0.6)

        result_b = MathTex(
            r"I_s \approx 1{,}53 \text{ A}",
            font_size=EQ_SIZE, color=ANSWER_COLOR,
        )
        result_b.next_to(compute_b, DOWN, buff=0.5)
        self.play(Write(result_b), run_time=0.7)

        box_b = make_answer_box(result_b)
        self.play(Create(box_b), run_time=0.3)
        self.wait(1.5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # ────────────────────────────────────────────
    #  ANSWER (25–35s): Summary + assumption
    # ────────────────────────────────────────────

    def answer(self):
        ans_a = MathTex(
            r"N_s \approx 157 \text{ mbështjella}",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        ans_b = MathTex(
            r"I_s \approx 1{,}53 \text{ A}",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )

        answers = VGroup(ans_a, ans_b).arrange(DOWN, buff=0.5)
        answers.move_to(UP * 2.0)

        self.play(Write(ans_a), run_time=0.7)
        self.wait(0.5)
        self.play(Write(ans_b), run_time=0.7)
        self.wait(0.5)

        box = make_answer_box(answers)
        self.play(Create(box), run_time=0.4)
        self.play(
            Flash(answers.get_center(), color=ANSWER_COLOR,
                  line_length=0.25, num_lines=12, run_time=0.6),
        )
        self.wait(1.0)

        # Assumption note
        assumption = MathTex(
            r"\text{Supozimi: transformator ideal}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        assumption.next_to(box, DOWN, buff=0.6)
        self.play(FadeIn(assumption, shift=UP * 0.2), run_time=0.5)
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
