"""
Reel C — Ushtrimi 5, Njësia 8.4A
"Alarmet e rreme" — 8 atletë të pafajshëm dalin pozitiv!

Standalone reel: the SURPRISE reel. Shows WHY 8 false alarms exist.
400 clean athletes, test gives false positive 1/50 times => 8 false alarms.
8 out of 103 total positives (~8%) are innocent.
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
        self.setup_numbers()
        self.false_alarm_calc()
        self.cta()

    # -----------------------------------------------
    #  HOOK (0-8s)
    # -----------------------------------------------

    def hook(self):
        line1 = MathTex(
            r"\text{500 atletë testohen për doping.}",
            font_size=HOOK_SIZE, color=WHITE,
        )
        line2 = MathTex(
            r"\text{20\% përdorin barna.}",
            font_size=BODY_SIZE, color=AUX_COLOR,
        )
        line3 = MathTex(
            r"\text{Testi është 95\% i saktë --}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        hook_group = VGroup(line1, line2, line3).arrange(DOWN, buff=0.3)
        hook_group.move_to(UP * 3.0)

        ask = MathTex(
            r"\text{por a mund të gabojë?}",
            font_size=QUESTION_SIZE, color=HIGHLIGHT_COLOR,
        )
        ask.next_to(hook_group, DOWN, buff=0.6)

        self.play(FadeIn(hook_group, shift=UP * 0.4), run_time=1.2)
        self.wait(2.0)
        self.play(FadeIn(ask, shift=UP * 0.3), run_time=0.8)
        self.wait(2.5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # -----------------------------------------------
    #  SETUP — show the clean-athlete branch (8-22s)
    # -----------------------------------------------

    def setup_numbers(self):
        title = MathTex(
            r"\text{Atletët që NUK përdorin barna:}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        title.move_to(UP * SAFE_TOP)
        self.play(FadeIn(title), run_time=0.5)

        # Population split
        pop = MathTex(
            r"500 \text{ atletë}",
            font_size=EQ_SIZE, color=WHITE,
        )
        pop.move_to(UP * 3.5)
        self.play(GrowFromCenter(pop), run_time=0.5)

        # Split arrow
        split_l = MathTex(
            r"100 \text{ përdorin}",
            font_size=SMALL_SIZE, color=AUX_COLOR,
        )
        split_l.move_to(LEFT * 2.0 + UP * 2.3)
        split_r = MathTex(
            r"400 \text{ nuk përdorin}",
            font_size=BODY_SIZE, color=SHAPE_COLOR,
        )
        split_r.move_to(RIGHT * 1.5 + UP * 2.3)

        arrow_l = Arrow(
            pop.get_bottom() + DOWN * 0.1,
            split_l.get_top() + UP * 0.1,
            buff=0.1, color=AUX_COLOR, stroke_width=2, max_tip_length_to_length_ratio=0.15,
        )
        arrow_r = Arrow(
            pop.get_bottom() + DOWN * 0.1,
            split_r.get_top() + UP * 0.1,
            buff=0.1, color=SHAPE_COLOR, stroke_width=2.5, max_tip_length_to_length_ratio=0.15,
        )

        # Dim the left (user) branch, focus on right (clean)
        self.play(
            GrowArrow(arrow_l), GrowArrow(arrow_r),
            FadeIn(split_l), FadeIn(split_r),
            run_time=0.8,
        )
        self.play(
            split_l.animate.set_opacity(0.35),
            arrow_l.animate.set_opacity(0.35),
            run_time=0.4,
        )
        self.wait(1.0)

        # Highlight the 400 clean athletes
        self.play(
            Indicate(split_r, color=SHAPE_COLOR, scale_factor=1.1),
            run_time=0.6,
        )

        # Show the false positive rate
        rate_text = MathTex(
            r"\text{Testi jep pozitiv në } \frac{1}{50} \text{ rastesh}",
            font_size=BODY_SIZE, color=HIGHLIGHT_COLOR,
        )
        rate_text.move_to(UP * 0.9)
        self.play(FadeIn(rate_text, shift=UP * 0.2), run_time=0.8)
        self.wait(1.5)

        # The multiplication
        calc = MathTex(
            r"400 \times \frac{1}{50} = 8",
            font_size=EQ_SIZE, color=HIGHLIGHT_COLOR,
        )
        calc.next_to(rate_text, DOWN, buff=0.5)
        self.play(Write(calc), run_time=1.0)
        self.wait(1.0)

        alarm_label = MathTex(
            r"\text{8 alarme të rreme!}",
            font_size=QUESTION_SIZE, color=HIGHLIGHT_COLOR,
        )
        alarm_label.next_to(calc, DOWN, buff=0.5)
        self.play(FadeIn(alarm_label, shift=UP * 0.2), run_time=0.7)
        self.play(
            Indicate(alarm_label, color=HIGHLIGHT_COLOR, scale_factor=1.1),
            run_time=0.7,
        )
        self.wait(2.0)

    # -----------------------------------------------
    #  CONTEXT + ANSWER (22-35s)
    # -----------------------------------------------

    def false_alarm_calc(self):
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

        # Context: 8 out of 103 positives
        context_title = MathTex(
            r"\text{Nga 103 pozitivë gjithsej:}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        context_title.move_to(UP * 3.0)
        self.play(FadeIn(context_title), run_time=0.5)

        # Show both sources
        src1 = MathTex(
            r"95 \text{ janë përdorues të vërtetë}",
            font_size=BODY_SIZE, color=AUX_COLOR,
        )
        src1.next_to(context_title, DOWN, buff=0.5)

        src2 = MathTex(
            r"8 \text{ janë atletë të pafajshëm!}",
            font_size=BODY_SIZE, color=HIGHLIGHT_COLOR,
        )
        src2.next_to(src1, DOWN, buff=0.35)

        self.play(FadeIn(src1, shift=UP * 0.2), run_time=0.6)
        self.wait(0.8)
        self.play(FadeIn(src2, shift=UP * 0.2), run_time=0.6)
        self.wait(1.0)

        # Percentage
        pct = MathTex(
            r"\frac{8}{103} \approx 7{,}8\%",
            font_size=EQ_SIZE, color=HIGHLIGHT_COLOR,
        )
        pct.next_to(src2, DOWN, buff=0.6)
        self.play(Write(pct), run_time=0.8)
        self.wait(1.5)

        # Answer box
        answer = MathTex(
            r"8 \text{ alarme të rreme}",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        answer.next_to(pct, DOWN, buff=0.7)
        box = make_answer_box(answer)

        self.play(Write(answer), run_time=0.8)
        self.play(Create(box), run_time=0.4)
        self.play(
            Flash(answer.get_center(), color=ANSWER_COLOR,
                  line_length=0.2, num_lines=10, run_time=0.5),
        )
        self.wait(2.5)

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
