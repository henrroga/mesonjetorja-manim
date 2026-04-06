"""
Reel B — Ushtrimi 6, Njësia 8.5A
"Vetëm 16,4%!" — The base rate fallacy surprise

Standalone reel: hooks with "98% accurate test, you're positive — how likely
are you sick?" then reveals the shocking 16.4% answer with visual explanation.
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
TINY_SIZE = 24
BIG_SIZE = 56


class ReelB(Scene):
    def construct(self):
        apply_style(self)
        MathTex.set_default(tex_template=ALBANIAN_TEX)
        Tex.set_default(tex_template=ALBANIAN_TEX)

        self.hook()
        self.reveal()
        self.explain()
        self.answer_and_cta()

    # -----------------------------------------------
    #  HOOK — build tension (0-8s)
    # -----------------------------------------------

    def hook(self):
        line1 = MathTex(
            r"\text{Testi ka saktësi 98\%.}",
            font_size=HOOK_SIZE, color=WHITE,
        )
        line2 = MathTex(
            r"\text{Rezultati yt:}",
            font_size=HOOK_SIZE, color=WHITE,
        )
        pos_label = MathTex(
            r"\text{POZITIV}",
            font_size=BIG_SIZE, color=HIGHLIGHT_COLOR,
        )
        line3 = MathTex(
            r"\text{Sa mundësi ke që je}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        line4 = MathTex(
            r"\text{vërtet i sëmurë?}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )

        hook_group = VGroup(line1, line2, pos_label, line3, line4).arrange(DOWN, buff=0.4)
        hook_group.move_to(UP * 1.5)

        self.play(FadeIn(VGroup(line1, line2), shift=UP * 0.3), run_time=0.8)
        self.wait(0.5)
        self.play(GrowFromCenter(pos_label), run_time=0.6)
        self.wait(0.8)
        self.play(FadeIn(VGroup(line3, line4), shift=UP * 0.2), run_time=0.6)

        # Let viewer think "~98%"
        self.wait(3.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # -----------------------------------------------
    #  REVEAL — the shocking answer (8-25s)
    # -----------------------------------------------

    def reveal(self):
        # Most people think...
        think = MathTex(
            r"\text{Shumica mendojnë } \approx 98\% \text{...}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        think.move_to(UP * 3.0)
        self.play(FadeIn(think, shift=UP * 0.2), run_time=0.6)
        self.wait(1.5)
        self.play(FadeOut(think), run_time=0.3)

        # The real answer
        intro = MathTex(
            r"\text{Përgjigja e vërtetë:}",
            font_size=HOOK_SIZE, color=STEP_TITLE_COLOR,
        )
        intro.move_to(UP * 3.0)

        answer = MathTex(
            r"16{,}4\%",
            font_size=BIG_SIZE * 1.3, color=ANSWER_COLOR,
        )
        answer.move_to(UP * 1.2)

        self.play(Write(intro), run_time=0.6)
        self.wait(0.5)
        self.play(GrowFromCenter(answer), run_time=0.8)

        # Circumscribe + Flash
        self.play(Circumscribe(answer, color=ANSWER_COLOR, run_time=1.0))
        self.play(
            Flash(answer.get_center(), color=ANSWER_COLOR,
                  num_lines=12, line_length=0.4, run_time=0.6),
        )
        self.wait(2.0)

        self.play(FadeOut(intro), FadeOut(answer), run_time=0.4)

    # -----------------------------------------------
    #  EXPLAIN — visual bars (25-42s)
    # -----------------------------------------------

    def explain(self):
        # Context line
        context = MathTex(
            r"\text{Sëmundja: vetëm 1 në 500.}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        context.move_to(UP * SAFE_TOP)
        self.play(FadeIn(context), run_time=0.5)

        sub = MathTex(
            r"\text{Nga 800.000 të testuar:}",
            font_size=SMALL_SIZE, color=BODY_TEXT_COLOR,
        )
        sub.next_to(context, DOWN, buff=0.3)
        self.play(FadeIn(sub), run_time=0.4)

        # --- Two bars side by side ---
        bar_width_true = 0.8   # narrow — few truly sick
        bar_width_false = 3.5  # wide — many false positives
        bar_height = 4.0

        # True positives bar (small, blue)
        true_bar = Rectangle(
            width=bar_width_true, height=bar_height * (1568 / 7984),
            fill_color=SHAPE_COLOR, fill_opacity=0.7,
            stroke_color=SHAPE_COLOR, stroke_width=2,
        )
        true_bar.move_to(LEFT * 2.0 + DOWN * 0.5)

        true_num = MathTex(r"1.568", font_size=SMALL_SIZE, color=SHAPE_COLOR)
        true_num.next_to(true_bar, UP, buff=0.2)

        true_desc = MathTex(
            r"\text{vërtet}", font_size=TINY_SIZE, color=SHAPE_COLOR,
        )
        true_desc2 = MathTex(
            r"\text{të sëmurë}", font_size=TINY_SIZE, color=SHAPE_COLOR,
        )
        true_desc_group = VGroup(true_desc, true_desc2).arrange(DOWN, buff=0.1)
        true_desc_group.next_to(true_bar, DOWN, buff=0.2)

        # False positives bar (big, red/orange)
        false_bar = Rectangle(
            width=bar_width_false, height=bar_height * (7984 / 7984),
            fill_color=AUX_COLOR, fill_opacity=0.7,
            stroke_color=AUX_COLOR, stroke_width=2,
        )
        false_bar.move_to(RIGHT * 1.8 + DOWN * 0.5)
        # Align bottoms
        false_bar.align_to(true_bar, DOWN)

        false_num = MathTex(r"7.984", font_size=SMALL_SIZE, color=AUX_COLOR)
        false_num.next_to(false_bar, UP, buff=0.2)

        false_desc = MathTex(
            r"\text{alarme}", font_size=TINY_SIZE, color=AUX_COLOR,
        )
        false_desc2 = MathTex(
            r"\text{të rreme}", font_size=TINY_SIZE, color=AUX_COLOR,
        )
        false_desc_group = VGroup(false_desc, false_desc2).arrange(DOWN, buff=0.1)
        false_desc_group.next_to(false_bar, DOWN, buff=0.2)

        # Animate bars
        self.play(
            DrawBorderThenFill(true_bar),
            run_time=0.8,
        )
        self.play(
            GrowFromCenter(true_num),
            FadeIn(true_desc_group),
            run_time=0.5,
        )
        self.wait(0.5)

        self.play(
            DrawBorderThenFill(false_bar),
            run_time=0.8,
        )
        self.play(
            GrowFromCenter(false_num),
            FadeIn(false_desc_group),
            run_time=0.5,
        )
        self.wait(1.0)

        # Explanation text
        explain_text = MathTex(
            r"\text{Shumica e pozitivëve}",
            font_size=SMALL_SIZE, color=HIGHLIGHT_COLOR,
        )
        explain_text2 = MathTex(
            r"\text{janë alarme të rreme!}",
            font_size=SMALL_SIZE, color=HIGHLIGHT_COLOR,
        )
        explain_group = VGroup(explain_text, explain_text2).arrange(DOWN, buff=0.15)
        explain_group.move_to(DOWN * 3.0)

        self.play(FadeIn(explain_group, shift=UP * 0.2), run_time=0.6)
        self.wait(3.0)

        # Store for cleanup
        self.explain_mobs = VGroup(
            context, sub,
            true_bar, true_num, true_desc_group,
            false_bar, false_num, false_desc_group,
            explain_group,
        )

    # -----------------------------------------------
    #  ANSWER + CTA (42-50s)
    # -----------------------------------------------

    def answer_and_cta(self):
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

        # Final answer
        eq = MathTex(
            r"P(S|P) = \frac{1.568}{9.552} \approx 0{,}164",
            font_size=EQ_SIZE, color=WHITE,
        )
        eq.move_to(UP * 2.0)

        percent = MathTex(
            r"= 16{,}4\%",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        percent.next_to(eq, DOWN, buff=0.4)

        answer_group = VGroup(eq, percent)
        box = make_answer_box(answer_group)

        self.play(Write(eq), run_time=1.0)
        self.play(Write(percent), run_time=0.6)
        self.play(Create(box), run_time=0.4)
        self.play(
            Flash(answer_group.get_center(), color=ANSWER_COLOR,
                  num_lines=14, line_length=0.5, run_time=0.6),
        )
        self.wait(2.5)

        # CTA
        self.play(FadeOut(VGroup(eq, percent, box)), run_time=0.4)

        handle = MathTex(r"\text{mesonjetorja.com}", font_size=BODY_SIZE, color=WHITE)
        handle.move_to(UP * 0.5)
        tagline = MathTex(
            r"\text{Më shumë ushtrime në faqen tonë!}",
            font_size=SMALL_SIZE, color=BODY_TEXT_COLOR,
        )
        tagline.next_to(handle, DOWN, buff=0.4)

        self.play(GrowFromCenter(handle), FadeIn(tagline, shift=UP * 0.3), run_time=0.8)
        self.wait(1.5)
