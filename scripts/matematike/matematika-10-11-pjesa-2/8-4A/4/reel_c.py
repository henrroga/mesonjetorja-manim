"""
Reel C — Ushtrimi 4, Njësia 8.4A
"Sa është probabiliteti që Jetmira të vonohet?"

Standalone reel: re-states context, applies the total probability formula
P(V) = P(M)*P(V|M) + P(A)*P(V|A) = 0.04 + 0.12 = 0.16 = 16%.
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
        self.formula()
        self.answer()
        self.cta()

    # -----------------------------------------------
    #  HOOK (0-8s)
    # -----------------------------------------------

    def hook(self):
        line1 = MathTex(
            r"\text{Jetmira shkon në punë:}",
            font_size=HOOK_SIZE, color=WHITE,
        )
        line2 = MathTex(
            r"\text{Makinë (P=0{,}4), Autobus (P=0{,}6)}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        line3 = MathTex(
            r"\text{Vonohet 10\% me makinë, 20\% me autobus}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        hook_group = VGroup(line1, line2, line3).arrange(DOWN, buff=0.35)
        hook_group.move_to(UP * 3.0)

        ask = MathTex(
            r"\text{Sa mundësi ka të vonohet?}",
            font_size=QUESTION_SIZE, color=HIGHLIGHT_COLOR,
        )
        ask.next_to(hook_group, DOWN, buff=0.7)

        self.play(FadeIn(hook_group, shift=UP * 0.4), run_time=1.2)
        self.wait(2.5)
        self.play(FadeIn(ask, shift=UP * 0.3), run_time=0.8)
        self.wait(2.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # -----------------------------------------------
    #  FORMULA (8-35s)
    # -----------------------------------------------

    def formula(self):
        title = MathTex(
            r"\text{Formula e probabilitetit total:}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        title.move_to(UP * SAFE_TOP)
        self.play(FadeIn(title), run_time=0.5)

        # General formula
        gen = MathTex(
            r"P(V) = P(M) \cdot P(V|M) + P(A) \cdot P(V|A)",
            font_size=BODY_SIZE, color=WHITE,
        )
        gen.move_to(UP * 3.2)
        self.play(Write(gen), run_time=1.2)
        self.wait(2.0)

        # Identify values
        vals_title = MathTex(
            r"\text{Zëvendësojmë vlerat:}",
            font_size=SMALL_SIZE, color=STEP_TITLE_COLOR,
        )
        vals_title.move_to(UP * 2.0)
        self.play(FadeIn(vals_title), run_time=0.4)

        v1 = MathTex(r"P(M) = 0{,}4", font_size=BODY_SIZE, color=SHAPE_COLOR)
        v2 = MathTex(r"P(V|M) = 0{,}1", font_size=BODY_SIZE, color=LABEL_COLOR)
        v3 = MathTex(r"P(A) = 0{,}6", font_size=BODY_SIZE, color=AUX_COLOR)
        v4 = MathTex(r"P(V|A) = 0{,}2", font_size=BODY_SIZE, color=LABEL_COLOR)

        vals = VGroup(v1, v2, v3, v4).arrange(DOWN, buff=0.25)
        vals.next_to(vals_title, DOWN, buff=0.35)

        for v in [v1, v2, v3, v4]:
            self.play(FadeIn(v, shift=UP * 0.15), run_time=0.35)
        self.wait(1.5)

        # Clear and substitute
        self.play(
            FadeOut(vals), FadeOut(vals_title),
            run_time=0.3,
        )

        # Step-by-step substitution
        eq1 = MathTex(
            r"P(V) = 0{,}4 \times 0{,}1 + 0{,}6 \times 0{,}2",
            font_size=EQ_SIZE, color=WHITE,
        )
        eq1.move_to(UP * 1.5)
        self.play(Write(eq1), run_time=1.0)
        self.wait(1.5)

        # Multiply
        eq2 = MathTex(
            r"P(V) = 0{,}04 + 0{,}12",
            font_size=EQ_SIZE, color=WHITE,
        )
        eq2.next_to(eq1, DOWN, buff=0.5)
        self.play(Write(eq2), run_time=0.8)
        self.wait(1.0)

        # Result
        eq3 = MathTex(
            r"P(V) = 0{,}16",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        eq3.next_to(eq2, DOWN, buff=0.5)
        self.play(Write(eq3), run_time=0.8)
        self.wait(1.0)

        # Store for answer section
        self.eq_group = VGroup(title, gen, eq1, eq2, eq3)

    # -----------------------------------------------
    #  ANSWER (35-45s)
    # -----------------------------------------------

    def answer(self):
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

        ans_label = MathTex(
            r"\text{Probabiliteti i vonimit:}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        ans_label.move_to(UP * 2.0)

        answer = MathTex(
            r"P(V) = 0{,}16 = 16\%",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        answer.next_to(ans_label, DOWN, buff=0.6)
        box = make_answer_box(answer)

        interpret = MathTex(
            r"\text{Në çdo ditë pune, Jetmira ka}",
            font_size=SMALL_SIZE, color=BODY_TEXT_COLOR,
        )
        interpret2 = MathTex(
            r"\text{16\% mundësi të vonohet.}",
            font_size=SMALL_SIZE, color=BODY_TEXT_COLOR,
        )
        interp_group = VGroup(interpret, interpret2).arrange(DOWN, buff=0.2)
        interp_group.next_to(box, DOWN, buff=0.6)

        self.play(FadeIn(ans_label), run_time=0.5)
        self.play(Write(answer), run_time=0.9)
        self.play(Create(box), run_time=0.4)
        self.play(
            Flash(answer.get_center(), color=ANSWER_COLOR,
                  line_length=0.2, num_lines=10, run_time=0.5),
        )
        self.play(FadeIn(interp_group, shift=UP * 0.2), run_time=0.6)
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
