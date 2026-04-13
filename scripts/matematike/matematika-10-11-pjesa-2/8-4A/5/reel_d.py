"""
Reel D — Ushtrimi 5, Njësia 8.4A
"Sa i saktë është testi i dopingut?"

Standalone reel: correct = true positive + true negative = 95 + 392 = 487.
P(correct) = 487/500 = 0.974 = 97.4%.
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


class ReelD(Scene):
    def construct(self):
        apply_style(self)
        MathTex.set_default(tex_template=ALBANIAN_TEX)
        Tex.set_default(tex_template=ALBANIAN_TEX)

        self.hook()
        self.explain()
        self.calculate()
        self.cta()

    # -----------------------------------------------
    #  HOOK (0-8s)
    # -----------------------------------------------

    def hook(self):
        line1 = MathTex(
            r"\text{500 atletë, test dopingu.}",
            font_size=HOOK_SIZE, color=WHITE,
        )
        line2 = MathTex(
            r"\text{Testi bën gabime...}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        hook_group = VGroup(line1, line2).arrange(DOWN, buff=0.35)
        hook_group.move_to(UP * 2.5)

        ask = MathTex(
            r"\text{Sa i saktë është testi në total?}",
            font_size=QUESTION_SIZE, color=HIGHLIGHT_COLOR,
        )
        ask.next_to(hook_group, DOWN, buff=0.7)

        self.play(FadeIn(hook_group, shift=UP * 0.4), run_time=1.2)
        self.wait(2.0)
        self.play(FadeIn(ask, shift=UP * 0.3), run_time=0.8)
        self.wait(2.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # -----------------------------------------------
    #  EXPLAIN (8-22s)
    # -----------------------------------------------

    def explain(self):
        title = MathTex(
            r"\text{Kur është testi i saktë?}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        title.move_to(UP * SAFE_TOP)
        self.play(FadeIn(title), run_time=0.5)

        # Two correct cases
        case1_label = MathTex(
            r"\text{Përdorues} + \text{Pozitiv}",
            font_size=BODY_SIZE, color=AUX_COLOR,
        )
        case1_val = MathTex(
            r"= 95 \text{ atletë}",
            font_size=EQ_SIZE, color=AUX_COLOR,
        )
        case1 = VGroup(case1_label, case1_val).arrange(DOWN, buff=0.2)
        case1.move_to(UP * 2.5)

        case2_label = MathTex(
            r"\text{Jo-përdorues} + \text{Negativ}",
            font_size=BODY_SIZE, color=SHAPE_COLOR,
        )
        case2_val = MathTex(
            r"= 392 \text{ atletë}",
            font_size=EQ_SIZE, color=SHAPE_COLOR,
        )
        case2 = VGroup(case2_label, case2_val).arrange(DOWN, buff=0.2)
        case2.next_to(case1, DOWN, buff=0.6)

        self.play(FadeIn(case1, shift=UP * 0.3), run_time=0.8)
        self.wait(1.5)
        self.play(FadeIn(case2, shift=UP * 0.3), run_time=0.8)
        self.wait(1.5)

        # Wrong cases (dimmed)
        wrong_label = MathTex(
            r"\text{Gabime: } 5 + 8 = 13 \text{ atletë}",
            font_size=SMALL_SIZE, color=BODY_TEXT_COLOR,
        )
        wrong_label.next_to(case2, DOWN, buff=0.5)
        self.play(FadeIn(wrong_label), run_time=0.5)
        self.wait(1.5)

    # -----------------------------------------------
    #  CALCULATE (22-42s)
    # -----------------------------------------------

    def calculate(self):
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

        title = MathTex(
            r"\text{Rezultate të sakta:}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        title.move_to(UP * SAFE_TOP)
        self.play(FadeIn(title), run_time=0.5)

        # Sum
        sum_eq = MathTex(
            r"95 + 392 = 487",
            font_size=EQ_SIZE, color=WHITE,
        )
        sum_eq.move_to(UP * 3.0)
        self.play(Write(sum_eq), run_time=1.0)
        self.wait(1.0)

        # Probability
        p_title = MathTex(
            r"\text{Probabiliteti:}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        p_title.next_to(sum_eq, DOWN, buff=0.6)
        self.play(FadeIn(p_title), run_time=0.4)

        p_eq1 = MathTex(
            r"P(\text{saktë}) = \frac{487}{500}",
            font_size=EQ_SIZE, color=LABEL_COLOR,
        )
        p_eq1.next_to(p_title, DOWN, buff=0.4)
        self.play(Write(p_eq1), run_time=1.0)
        self.wait(1.5)

        p_eq2 = MathTex(
            r"= 0{,}974 = 97{,}4\%",
            font_size=EQ_SIZE, color=LABEL_COLOR,
        )
        p_eq2.next_to(p_eq1, DOWN, buff=0.3)
        self.play(Write(p_eq2), run_time=0.8)
        self.wait(1.5)

        # Answer
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

        ans_label = MathTex(
            r"\text{Saktësia e testit:}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        ans_label.move_to(UP * 1.5)

        answer = MathTex(
            r"P = \frac{487}{500} = 0{,}974",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        answer.next_to(ans_label, DOWN, buff=0.5)

        pct = MathTex(
            r"97{,}4\% \text{ e rezultateve janë të sakta}",
            font_size=BODY_SIZE, color=ANSWER_COLOR,
        )
        pct.next_to(answer, DOWN, buff=0.4)

        box = make_answer_box(VGroup(answer, pct))

        self.play(FadeIn(ans_label), run_time=0.5)
        self.play(Write(answer), run_time=0.8)
        self.play(FadeIn(pct, shift=UP * 0.2), run_time=0.6)
        self.play(Create(box), run_time=0.4)
        self.play(
            Flash(answer.get_center(), color=ANSWER_COLOR,
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
