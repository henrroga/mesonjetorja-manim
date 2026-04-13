"""
Reel C — Ushtrimi 5, Njësia 8.4A
"Sa prej pozitivëve janë alarme të rreme?"

Standalone reel: the surprise — 8 out of 103 positives are clean athletes!
Shows 8/103 ~ 7.8% false positive rate among positives.
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

# -- Vertical 9:16 config --
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 8
config.frame_height = 8 * (1920 / 1080)

# -- Safe zone --
SAFE_TOP = 4.8
SAFE_BOTTOM = -3.3

# -- Font sizes --
HOOK_SIZE = 38
QUESTION_SIZE = 42
EQ_SIZE = 38
ANSWER_SIZE = 42
BODY_SIZE = 32
SMALL_SIZE = 28


class ReelC(Scene):
    def construct(self):
        apply_style(self)
        MathTex.set_default(tex_template=ALBANIAN_TEX)
        Tex.set_default(tex_template=ALBANIAN_TEX)

        self.hook()
        self.breakdown()
        self.surprise()
        self.cta()

    # -----------------------------------------------
    #  HOOK (0-8s)
    # -----------------------------------------------

    def hook(self):
        line1 = MathTex(
            r"\text{Testi i dopingut doli pozitiv}",
            font_size=HOOK_SIZE, color=WHITE,
        )
        line2 = MathTex(
            r"\text{për 103 atletë.}",
            font_size=HOOK_SIZE, color=WHITE,
        )
        hook_group = VGroup(line1, line2).arrange(DOWN, buff=0.3)
        hook_group.move_to(UP * 2.5)

        ask = MathTex(
            r"\text{Sa prej tyre janë TË PASTËR?}",
            font_size=QUESTION_SIZE, color=HIGHLIGHT_COLOR,
        )
        ask.next_to(hook_group, DOWN, buff=0.7)

        self.play(FadeIn(hook_group, shift=UP * 0.4), run_time=1.2)
        self.wait(2.0)
        self.play(FadeIn(ask, shift=UP * 0.3), run_time=0.8)
        self.wait(2.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # -----------------------------------------------
    #  BREAKDOWN (8-30s)
    # -----------------------------------------------

    def breakdown(self):
        title = MathTex(
            r"\text{Nga ku vijnë 103 pozitivët?}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        title.move_to(UP * SAFE_TOP)
        self.play(FadeIn(title), run_time=0.5)

        # Two sources
        src1_label = MathTex(
            r"\text{Përdorues barnash:}",
            font_size=BODY_SIZE, color=AUX_COLOR,
        )
        src1_val = MathTex(
            r"95 \text{ pozitivë}",
            font_size=EQ_SIZE, color=AUX_COLOR,
        )
        src1 = VGroup(src1_label, src1_val).arrange(DOWN, buff=0.2)
        src1.move_to(UP * 2.5)

        src2_label = MathTex(
            r"\text{Atletë të pastër:}",
            font_size=BODY_SIZE, color=HIGHLIGHT_COLOR,
        )
        src2_val = MathTex(
            r"8 \text{ pozitivë (alarme të rreme!)}",
            font_size=EQ_SIZE, color=HIGHLIGHT_COLOR,
        )
        src2 = VGroup(src2_label, src2_val).arrange(DOWN, buff=0.2)
        src2.next_to(src1, DOWN, buff=0.6)

        self.play(FadeIn(src1, shift=UP * 0.3), run_time=0.8)
        self.wait(1.5)
        self.play(FadeIn(src2, shift=UP * 0.3), run_time=0.8)
        self.wait(1.0)

        # Flash the false alarm
        self.play(
            Indicate(src2_val, color=HIGHLIGHT_COLOR, scale_factor=1.1),
            run_time=0.8,
        )
        self.wait(1.5)

        # Total
        total_eq = MathTex(
            r"\text{Gjithsej pozitivë:} \quad 95 + 8 = 103",
            font_size=BODY_SIZE, color=WHITE,
        )
        total_eq.next_to(src2, DOWN, buff=0.6)
        self.play(Write(total_eq), run_time=0.8)
        self.wait(1.5)

        # False positive count
        fp_title = MathTex(
            r"\text{Alarme të rreme:}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        fp_title.next_to(total_eq, DOWN, buff=0.6)

        fp_eq = MathTex(
            r"8 \text{ atletë të pastër me test pozitiv}",
            font_size=EQ_SIZE, color=HIGHLIGHT_COLOR,
        )
        fp_eq.next_to(fp_title, DOWN, buff=0.3)

        self.play(FadeIn(fp_title), run_time=0.5)
        self.play(Write(fp_eq), run_time=0.8)
        self.wait(2.0)

    # -----------------------------------------------
    #  SURPRISE — percentage (30-45s)
    # -----------------------------------------------

    def surprise(self):
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

        q = MathTex(
            r"\text{Nga 103 pozitivë, sa janë të rremë?}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        q.move_to(UP * 3.0)
        self.play(FadeIn(q), run_time=0.5)

        frac_eq = MathTex(
            r"\frac{8}{103} \approx 0{,}078 = 7{,}8\%",
            font_size=EQ_SIZE, color=HIGHLIGHT_COLOR,
        )
        frac_eq.next_to(q, DOWN, buff=0.7)
        self.play(Write(frac_eq), run_time=1.2)
        self.wait(1.5)

        # Big reveal
        reveal = MathTex(
            r"\text{7{,}8\% e pozitivëve janë}",
            font_size=BODY_SIZE, color=WHITE,
        )
        reveal2 = MathTex(
            r"\text{alarme të rreme!}",
            font_size=QUESTION_SIZE, color=HIGHLIGHT_COLOR,
        )
        reveal_group = VGroup(reveal, reveal2).arrange(DOWN, buff=0.3)
        reveal_group.next_to(frac_eq, DOWN, buff=0.8)

        self.play(FadeIn(reveal_group, shift=UP * 0.3), run_time=0.8)
        self.wait(1.0)

        # Answer box
        ans = MathTex(
            r"8 \text{ alarme të rreme}",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        ans.next_to(reveal_group, DOWN, buff=0.7)
        box = make_answer_box(ans)

        self.play(Write(ans), run_time=0.8)
        self.play(Create(box), run_time=0.4)
        self.play(
            Flash(ans.get_center(), color=ANSWER_COLOR,
                  line_length=0.2, num_lines=10, run_time=0.5),
        )
        self.wait(3.0)

    # -----------------------------------------------
    #  CTA
    # -----------------------------------------------

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
