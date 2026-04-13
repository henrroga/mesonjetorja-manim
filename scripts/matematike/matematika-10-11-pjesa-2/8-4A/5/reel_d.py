"""
Reel D — Ushtrimi 5, Njësia 8.4A
"P(rezultat i saktë)" — Sa i saktë është testi?

Standalone reel: shows all 4 outcomes from the tree, identifies which
are correct (95 + 392 = 487), calculates P = 487/500 = 97.4%.
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
TINY_SIZE = 26


class ReelD(Scene):
    def construct(self):
        apply_style(self)
        MathTex.set_default(tex_template=ALBANIAN_TEX)
        Tex.set_default(tex_template=ALBANIAN_TEX)

        self.hook()
        self.show_outcomes()
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
            r"\text{20\% përdorin barna, 80\% jo.}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        hook_group = VGroup(line1, line2).arrange(DOWN, buff=0.35)
        hook_group.move_to(UP * 3.0)

        ask = MathTex(
            r"\text{Sa i saktë është testi në total?}",
            font_size=QUESTION_SIZE, color=HIGHLIGHT_COLOR,
        )
        ask.next_to(hook_group, DOWN, buff=0.7)

        self.play(FadeIn(hook_group, shift=UP * 0.4), run_time=1.0)
        self.wait(1.5)
        self.play(FadeIn(ask, shift=UP * 0.3), run_time=0.8)
        self.wait(2.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # -----------------------------------------------
    #  SHOW ALL 4 OUTCOMES (5-20s)
    # -----------------------------------------------

    def show_outcomes(self):
        title = MathTex(
            r"\text{4 rezultatet e mundshme:}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        title.move_to(UP * SAFE_TOP)
        self.play(FadeIn(title), run_time=0.5)

        # --- Population context ---
        pop_row = MathTex(
            r"500 \text{ atletë: } 100 \text{ përdorues} + 400 \text{ jo}",
            font_size=SMALL_SIZE, color=BODY_TEXT_COLOR,
        )
        pop_row.move_to(UP * 3.6)
        self.play(FadeIn(pop_row), run_time=0.5)
        self.wait(0.8)

        # --- 4 outcome rows ---
        # Correct outcomes get green check, wrong get red X
        row1_txt = MathTex(
            r"\text{Përdorues + Pozitiv:}",
            font_size=BODY_SIZE, color=AUX_COLOR,
        )
        row1_val = MathTex(
            r"95", font_size=EQ_SIZE, color=AUX_COLOR,
        )
        row1_check = MathTex(
            r"\checkmark", font_size=EQ_SIZE, color=ANSWER_COLOR,
        )

        row2_txt = MathTex(
            r"\text{Përdorues + Negativ:}",
            font_size=BODY_SIZE, color=AUX_COLOR,
        )
        row2_val = MathTex(
            r"5", font_size=EQ_SIZE, color=AUX_COLOR,
        )
        row2_x = MathTex(
            r"\times", font_size=EQ_SIZE, color=HIGHLIGHT_COLOR,
        )

        row3_txt = MathTex(
            r"\text{Jo-përdorues + Pozitiv:}",
            font_size=BODY_SIZE, color=SHAPE_COLOR,
        )
        row3_val = MathTex(
            r"8", font_size=EQ_SIZE, color=SHAPE_COLOR,
        )
        row3_x = MathTex(
            r"\times", font_size=EQ_SIZE, color=HIGHLIGHT_COLOR,
        )
        row3_note = MathTex(
            r"\text{(alarme të rreme)}", font_size=TINY_SIZE, color=HIGHLIGHT_COLOR,
        )

        row4_txt = MathTex(
            r"\text{Jo-përdorues + Negativ:}",
            font_size=BODY_SIZE, color=SHAPE_COLOR,
        )
        row4_val = MathTex(
            r"392", font_size=EQ_SIZE, color=SHAPE_COLOR,
        )
        row4_check = MathTex(
            r"\checkmark", font_size=EQ_SIZE, color=ANSWER_COLOR,
        )

        # Arrange as a table-like layout
        rows = []
        for txt, val, mark in [
            (row1_txt, row1_val, row1_check),
            (row2_txt, row2_val, row2_x),
            (row3_txt, row3_val, row3_x),
            (row4_txt, row4_val, row4_check),
        ]:
            row = VGroup(txt, val, mark).arrange(RIGHT, buff=0.3)
            rows.append(row)

        # Add the note next to row3
        row3_note.next_to(rows[2], DOWN, buff=0.1)
        rows[2] = VGroup(rows[2], row3_note)

        outcome_group = VGroup(*rows).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        outcome_group.move_to(UP * 1.2)

        # Reveal one by one
        for i, row in enumerate(rows):
            self.play(FadeIn(row, shift=UP * 0.2), run_time=0.6)
            if i == 2:
                # Extra pause on the false alarm row
                self.play(
                    Indicate(rows[2], color=HIGHLIGHT_COLOR, scale_factor=1.05),
                    run_time=0.5,
                )
            self.wait(0.8)

        self.wait(1.0)

        # Store for use in calculate
        self.outcome_group = outcome_group
        self.pop_row = pop_row

    # -----------------------------------------------
    #  CALCULATE (20-35s)
    # -----------------------------------------------

    def calculate(self):
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

        title = MathTex(
            r"\text{Rezultate të sakta:}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        title.move_to(UP * SAFE_TOP)
        self.play(FadeIn(title), run_time=0.5)

        # Correct = true positive + true negative
        correct_label = MathTex(
            r"\text{Të sakta} = 95 + 392",
            font_size=EQ_SIZE, color=ANSWER_COLOR,
        )
        correct_label.move_to(UP * 3.0)
        self.play(Write(correct_label), run_time=0.8)
        self.wait(0.8)

        correct_val = MathTex(
            r"= 487 \text{ atletë}",
            font_size=EQ_SIZE, color=ANSWER_COLOR,
        )
        correct_val.next_to(correct_label, DOWN, buff=0.35)
        self.play(Write(correct_val), run_time=0.7)
        self.wait(1.0)

        # Probability
        p_title = MathTex(
            r"\text{Probabiliteti:}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        p_title.next_to(correct_val, DOWN, buff=0.6)
        self.play(FadeIn(p_title), run_time=0.4)

        p_eq1 = MathTex(
            r"P(\text{saktë}) = \frac{487}{500}",
            font_size=EQ_SIZE, color=LABEL_COLOR,
        )
        p_eq1.next_to(p_title, DOWN, buff=0.4)
        self.play(Write(p_eq1), run_time=1.0)
        self.wait(1.0)

        p_eq2 = MathTex(
            r"= 0{,}974 = 97{,}4\%",
            font_size=EQ_SIZE, color=LABEL_COLOR,
        )
        p_eq2.next_to(p_eq1, DOWN, buff=0.3)
        self.play(Write(p_eq2), run_time=0.8)
        self.wait(1.5)

        # Answer screen
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

        ans_label = MathTex(
            r"\text{Saktësia e testit:}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        ans_label.move_to(UP * 1.5)

        answer = MathTex(
            r"97{,}4\% \text{ e rezultateve}",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        answer.next_to(ans_label, DOWN, buff=0.4)

        answer2 = MathTex(
            r"\text{janë të sakta}",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        answer2.next_to(answer, DOWN, buff=0.25)

        ans_group = VGroup(answer, answer2)
        box = make_answer_box(ans_group)

        self.play(FadeIn(ans_label), run_time=0.5)
        self.play(Write(answer), run_time=0.8)
        self.play(FadeIn(answer2, shift=UP * 0.2), run_time=0.5)
        self.play(Create(box), run_time=0.4)
        self.play(
            Flash(ans_group.get_center(), color=ANSWER_COLOR,
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
