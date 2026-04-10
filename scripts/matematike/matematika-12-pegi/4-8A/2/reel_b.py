"""
Reel B -- Ushtrimi 2, Njesia 4.8A
y = -x,  y = 0,  x = -1,  x = -2   ->  integral_{-2}^{-1} (-x) dx = 3/2 = 1,5

Standalone vertical reel: hook graph, solve, answer + CTA.
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
EQ_SIZE = 36
ANSWER_SIZE = 42
BODY_SIZE = 30
SMALL_SIZE = 26


class ReelB(Scene):
    def construct(self):
        apply_style(self)
        MathTex.set_default(tex_template=ALBANIAN_TEX)
        Tex.set_default(tex_template=ALBANIAN_TEX)

        self.hook()
        self.solve()
        self.answer()
        self.cta()

    # ------------------------------------------------
    #  HOOK (0-8s)
    # ------------------------------------------------

    def hook(self):
        axes = Axes(
            x_range=[-3, 1, 1], y_range=[0, 3, 1],
            x_length=5, y_length=3,
            axis_config={"include_numbers": True, "font_size": 20, "color": DIVIDER_COLOR},
        )
        axes.move_to(UP * 2.0)

        # Plot y = -x (positive in the region x < 0)
        graph = axes.plot(lambda x: -x, x_range=[-2.8, 0], color=SHAPE_COLOR, stroke_width=3)

        # Shaded area between x=-2 and x=-1
        area = axes.get_area(graph, x_range=[-2, -1], color=SHAPE_COLOR, opacity=0.35)

        # Boundary dashed lines
        x1_line = DashedLine(
            axes.c2p(-2, 0), axes.c2p(-2, 2),
            color=LABEL_COLOR, stroke_width=2, dash_length=0.08,
        )
        x2_line = DashedLine(
            axes.c2p(-1, 0), axes.c2p(-1, 1),
            color=LABEL_COLOR, stroke_width=2, dash_length=0.08,
        )

        func_label = MathTex(r"y = -x", font_size=SMALL_SIZE, color=SHAPE_COLOR)
        func_label.next_to(axes.c2p(-2.6, 2.6), LEFT, buff=0.15)

        x1_label = MathTex(r"x\!=\!-2", font_size=20, color=LABEL_COLOR)
        x1_label.next_to(axes.c2p(-2, 0), DOWN, buff=0.25)
        x2_label = MathTex(r"x\!=\!-1", font_size=20, color=LABEL_COLOR)
        x2_label.next_to(axes.c2p(-1, 0), DOWN, buff=0.25)

        question = MathTex(
            r"\text{Sa është syprina?}",
            font_size=QUESTION_SIZE, color=LABEL_COLOR,
        )
        question.move_to(DOWN * 0.8)

        self.play(Create(axes), run_time=0.6)
        self.play(Create(graph), run_time=0.5)
        self.play(
            FadeIn(x1_line), FadeIn(x2_line),
            FadeIn(x1_label), FadeIn(x2_label),
            run_time=0.4,
        )
        self.play(DrawBorderThenFill(area), run_time=0.6)
        self.play(FadeIn(func_label), run_time=0.3)
        self.wait(0.5)
        self.play(FadeIn(question, shift=UP * 0.2), run_time=0.6)
        self.wait(3.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # ------------------------------------------------
    #  SOLVE (8-25s)
    # ------------------------------------------------

    def solve(self):
        title = MathTex(
            r"\text{Zgjidhje}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        title.move_to(UP * SAFE_TOP)
        self.play(FadeIn(title), run_time=0.3)

        # Show the integral
        integral = MathTex(
            r"S = \int_{-2}^{-1} (-x) \, dx",
            font_size=EQ_SIZE, color=WHITE,
        )
        integral.move_to(UP * 3.0)
        self.play(Write(integral), run_time=0.8)
        self.wait(1.0)

        # Antiderivative
        why1 = MathTex(
            r"\text{Gjejmë antiderivatën:}",
            font_size=SMALL_SIZE, color=BODY_TEXT_COLOR,
        )
        why1.next_to(integral, DOWN, buff=0.5)
        self.play(FadeIn(why1), run_time=0.4)

        step1 = MathTex(
            r"= \left[ -\frac{x^2}{2} \right]_{-2}^{-1}",
            font_size=EQ_SIZE, color=WHITE,
        )
        step1.next_to(why1, DOWN, buff=0.4)
        self.play(Write(step1), run_time=0.8)
        self.wait(1.0)

        # Substitute
        why2 = MathTex(
            r"\text{Zëvendësojmë kufijtë:}",
            font_size=SMALL_SIZE, color=BODY_TEXT_COLOR,
        )
        why2.next_to(step1, DOWN, buff=0.5)
        self.play(FadeIn(why2), run_time=0.4)

        step2 = MathTex(
            r"= -\frac{(-1)^2}{2} + \frac{(-2)^2}{2}",
            font_size=EQ_SIZE, color=WHITE,
        )
        step2.next_to(why2, DOWN, buff=0.4)
        self.play(Write(step2), run_time=0.8)
        self.wait(0.8)

        # Simplify
        step3 = MathTex(
            r"= -\frac{1}{2} + \frac{4}{2} = \frac{3}{2}",
            font_size=EQ_SIZE, color=ANSWER_COLOR,
        )
        step3.next_to(step2, DOWN, buff=0.4)
        self.play(Write(step3), run_time=0.8)
        self.wait(1.5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # ------------------------------------------------
    #  ANSWER (25-35s)
    # ------------------------------------------------

    def answer(self):
        ans = MathTex(
            r"S = \dfrac{3}{2} = 1{,}5",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        ans.move_to(UP * 1.5)

        self.play(Write(ans), run_time=0.8)
        self.wait(0.6)

        box = make_answer_box(ans)
        self.play(Create(box), run_time=0.4)
        self.play(
            Flash(ans.get_center(), color=ANSWER_COLOR,
                  line_length=0.25, num_lines=12, run_time=0.6),
        )
        self.play(
            Circumscribe(VGroup(ans, box), color=HIGHLIGHT_COLOR, run_time=0.8),
        )
        self.wait(2.0)

    # ------------------------------------------------
    #  CTA
    # ------------------------------------------------

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
