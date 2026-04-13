"""
Reel B — Ushtrimi 5, Njësia 8.4A
"Sa pozitivë gjithsej?" (Total positive = 95 + 8 = 103)

Standalone reel: re-establishes the full doping-test context with numbers,
shows both sources of positives, calculates the total.
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


class ReelB(Scene):
    def construct(self):
        apply_style(self)
        MathTex.set_default(tex_template=ALBANIAN_TEX)
        Tex.set_default(tex_template=ALBANIAN_TEX)

        self.hook()
        self.setup_numbers()
        self.calculate()
        self.cta()

    # -----------------------------------------------
    #  HOOK (0-5s)
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
        hook_group = VGroup(line1, line2).arrange(DOWN, buff=0.35)
        hook_group.move_to(UP * 3.0)

        ask = MathTex(
            r"\text{Sa atletë dalin pozitiv gjithsej?}",
            font_size=QUESTION_SIZE, color=HIGHLIGHT_COLOR,
        )
        ask.next_to(hook_group, DOWN, buff=0.7)

        self.play(FadeIn(hook_group, shift=UP * 0.4), run_time=1.0)
        self.wait(1.5)
        self.play(FadeIn(ask, shift=UP * 0.3), run_time=0.8)
        self.wait(2.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # -----------------------------------------------
    #  SETUP NUMBERS (5-18s)
    # -----------------------------------------------

    def setup_numbers(self):
        title = MathTex(
            r"\text{Nga diagrami pemë:}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        title.move_to(UP * SAFE_TOP)
        self.play(FadeIn(title), run_time=0.5)

        # --- Population split ---
        pop_line = MathTex(
            r"500 \text{ atletë}",
            font_size=EQ_SIZE, color=WHITE,
        )
        pop_line.move_to(UP * 3.5)
        self.play(GrowFromCenter(pop_line), run_time=0.5)

        # Left branch: users
        user_label = MathTex(
            r"100 \text{ përdorin barna}",
            font_size=BODY_SIZE, color=AUX_COLOR,
        )
        user_label.move_to(LEFT * 1.8 + UP * 2.2)
        arrow_l = Arrow(
            pop_line.get_bottom() + DOWN * 0.1,
            user_label.get_top() + UP * 0.1,
            buff=0.1, color=AUX_COLOR, stroke_width=2.5, max_tip_length_to_length_ratio=0.15,
        )

        # Right branch: non-users
        clean_label = MathTex(
            r"400 \text{ nuk përdorin}",
            font_size=BODY_SIZE, color=SHAPE_COLOR,
        )
        clean_label.move_to(RIGHT * 1.8 + UP * 2.2)
        arrow_r = Arrow(
            pop_line.get_bottom() + DOWN * 0.1,
            clean_label.get_top() + UP * 0.1,
            buff=0.1, color=SHAPE_COLOR, stroke_width=2.5, max_tip_length_to_length_ratio=0.15,
        )

        self.play(
            GrowArrow(arrow_l), GrowArrow(arrow_r),
            FadeIn(user_label), FadeIn(clean_label),
            run_time=0.8,
        )
        self.wait(1.0)

        # --- User positives ---
        user_pos_text = MathTex(
            r"19/20 \;\rightarrow\; 95 \text{ pozitivë}",
            font_size=BODY_SIZE, color=LABEL_COLOR,
        )
        user_pos_text.next_to(user_label, DOWN, buff=0.5)

        self.play(FadeIn(user_pos_text, shift=UP * 0.2), run_time=0.7)
        self.wait(1.0)

        # --- Clean false positives ---
        clean_pos_text = MathTex(
            r"1/50 \;\rightarrow\; 8 \text{ pozitivë}",
            font_size=BODY_SIZE, color=HIGHLIGHT_COLOR,
        )
        clean_pos_text.next_to(clean_label, DOWN, buff=0.5)

        alarm_note = MathTex(
            r"\text{(alarme të rreme!)}",
            font_size=SMALL_SIZE, color=HIGHLIGHT_COLOR,
        )
        alarm_note.next_to(clean_pos_text, DOWN, buff=0.15)

        self.play(FadeIn(clean_pos_text, shift=UP * 0.2), run_time=0.7)
        self.play(FadeIn(alarm_note), run_time=0.4)
        self.wait(1.5)

        # Flash the false alarm number
        self.play(
            Indicate(clean_pos_text, color=HIGHLIGHT_COLOR, scale_factor=1.1),
            run_time=0.6,
        )
        self.wait(1.0)

        # Store for transition
        self.setup_mobs = VGroup(
            title, pop_line, arrow_l, arrow_r,
            user_label, clean_label,
            user_pos_text, clean_pos_text, alarm_note,
        )

    # -----------------------------------------------
    #  CALCULATE (18-35s)
    # -----------------------------------------------

    def calculate(self):
        # Sum title
        sum_title = MathTex(
            r"\text{Pozitivë gjithsej:}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        sum_title.move_to(DOWN * 0.8)

        sum_eq = MathTex(
            r"95 + 8 = 103",
            font_size=EQ_SIZE, color=LABEL_COLOR,
        )
        sum_eq.next_to(sum_title, DOWN, buff=0.4)

        self.play(FadeIn(sum_title), run_time=0.5)
        self.play(Write(sum_eq), run_time=1.0)
        self.wait(1.5)

        # Clear and show answer
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

        ans_label = MathTex(
            r"\text{Analiza pozitive gjithsej:}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        ans_label.move_to(UP * 1.5)

        answer = MathTex(
            r"103 \text{ atletë}",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        answer.next_to(ans_label, DOWN, buff=0.6)
        box = make_answer_box(answer)

        self.play(FadeIn(ans_label), run_time=0.5)
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
