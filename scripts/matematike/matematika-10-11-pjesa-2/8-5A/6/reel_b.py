"""
Reel B — Ushtrimi 6, Njësia 8.5A
"Testi 98% i saktë, rezultati POZITIV — sa mundësi ke?"

Standalone reel: re-establishes the full medical test scenario,
walks through the numbers with a mini frequency tree,
then reveals the surprising 16.4% answer.
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
HOOK_SIZE = 36
QUESTION_SIZE = 42
EQ_SIZE = 36
ANSWER_SIZE = 44
BODY_SIZE = 30
SMALL_SIZE = 26
BIG_SIZE = 52


class ReelB(Scene):
    def construct(self):
        apply_style(self)
        MathTex.set_default(tex_template=ALBANIAN_TEX)
        Tex.set_default(tex_template=ALBANIAN_TEX)

        self.hook()
        self.show_context()
        self.show_the_numbers()
        self.reveal()
        self.cta()

    # ────────────────────────────────────────────
    #  HOOK — state the full problem (0–10s)
    # ────────────────────────────────────────────

    def hook(self):
        line1 = MathTex(
            r"\text{Një sëmundje prek 1 në 500.}",
            font_size=HOOK_SIZE, color=WHITE,
        )
        line2 = MathTex(
            r"\text{Testi ka saktësi 98\%.}",
            font_size=HOOK_SIZE, color=WHITE,
        )
        line3 = MathTex(
            r"\text{Rezultati yt: }",
            font_size=HOOK_SIZE, color=WHITE,
        )
        pos_word = MathTex(
            r"\text{POZITIV}",
            font_size=QUESTION_SIZE, color=HIGHLIGHT_COLOR,
        )
        line4 = MathTex(
            r"\text{Sa mundësi ke që je i sëmurë?}",
            font_size=BODY_SIZE, color=LABEL_COLOR,
        )

        hook_group = VGroup(line1, line2, line3, pos_word, line4).arrange(DOWN, buff=0.35)
        hook_group.move_to(UP * 1.5)

        self.play(FadeIn(VGroup(line1, line2), shift=UP * 0.3), run_time=1.0)
        self.wait(1.5)
        self.play(FadeIn(line3), run_time=0.4)
        self.play(GrowFromCenter(pos_word), run_time=0.6)
        self.wait(0.8)
        self.play(FadeIn(line4, shift=UP * 0.2), run_time=0.6)
        self.wait(2.5)  # let them read and think "~98%"

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # ────────────────────────────────────────────
    #  CONTEXT — explain with numbers (10–22s)
    # ────────────────────────────────────────────

    def show_context(self):
        title = MathTex(
            r"\text{Le të numërojmë:}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        title.move_to(UP * SAFE_TOP)
        self.play(FadeIn(title), run_time=0.4)

        # Population split
        pop = MathTex(r"800.000 \text{ të rritur}", font_size=BODY_SIZE, color=WHITE)
        pop.next_to(title, DOWN, buff=0.5)

        sick = MathTex(
            r"\text{Sëmurë: } 800.000 \times \frac{1}{500} = 1.600",
            font_size=SMALL_SIZE, color=SHAPE_COLOR,
        )
        sick.next_to(pop, DOWN, buff=0.4)

        healthy = MathTex(
            r"\text{Shëndetshëm: } 798.400",
            font_size=SMALL_SIZE, color=AUX_COLOR,
        )
        healthy.next_to(sick, DOWN, buff=0.25)

        self.play(FadeIn(pop), run_time=0.5)
        self.wait(0.8)
        self.play(FadeIn(sick, shift=LEFT * 0.2), run_time=0.6)
        self.wait(0.5)
        self.play(FadeIn(healthy, shift=LEFT * 0.2), run_time=0.6)
        self.wait(1.0)

        # Test results
        test_title = MathTex(
            r"\text{Kush del pozitiv?}",
            font_size=BODY_SIZE, color=HIGHLIGHT_COLOR,
        )
        test_title.next_to(healthy, DOWN, buff=0.5)

        true_pos = MathTex(
            r"\text{Sëmurë} \to \text{pozitiv: } 1.600 \times 0{,}98 = 1.568",
            font_size=SMALL_SIZE, color=SHAPE_COLOR,
        )
        true_pos.next_to(test_title, DOWN, buff=0.35)

        false_pos = MathTex(
            r"\text{Shëndetshëm} \to \text{pozitiv: } 798.400 \times 0{,}01 = 7.984",
            font_size=SMALL_SIZE, color=AUX_COLOR,
        )
        false_pos.next_to(true_pos, DOWN, buff=0.25)

        self.play(FadeIn(test_title), run_time=0.5)
        self.wait(0.5)
        self.play(FadeIn(true_pos, shift=LEFT * 0.2), run_time=0.6)
        self.wait(0.5)
        self.play(FadeIn(false_pos, shift=LEFT * 0.2), run_time=0.6)
        self.wait(1.5)

        self.context_mobs = VGroup(
            title, pop, sick, healthy, test_title, true_pos, false_pos,
        )

    # ────────────────────────────────────────────
    #  THE NUMBERS — total positive (22–32s)
    # ────────────────────────────────────────────

    def show_the_numbers(self):
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

        title = MathTex(
            r"\text{Pozitiv gjithsej:}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        title.move_to(UP * SAFE_TOP)
        self.play(FadeIn(title), run_time=0.4)

        # Two bars showing the composition
        bar_area_y = UP * 1.5

        # True positives (small bar)
        true_h = 1.0
        true_bar = Rectangle(
            width=2.0, height=true_h,
            fill_color=SHAPE_COLOR, fill_opacity=0.7,
            stroke_color=SHAPE_COLOR, stroke_width=2,
        )
        true_bar.move_to(bar_area_y)

        true_label = MathTex(
            r"1.568 \text{ vërtet të sëmurë}",
            font_size=SMALL_SIZE, color=SHAPE_COLOR,
        )
        true_label.next_to(true_bar, UP, buff=0.2)

        # False positives (big bar)
        false_h = 1.0 * (7984 / 1568)  # proportional height ≈ 5.09
        false_h = min(false_h, 3.5)  # cap for screen
        false_bar = Rectangle(
            width=2.0, height=false_h,
            fill_color=AUX_COLOR, fill_opacity=0.7,
            stroke_color=AUX_COLOR, stroke_width=2,
        )
        false_bar.next_to(true_bar, DOWN, buff=0.3)

        false_label = MathTex(
            r"7.984 \text{ alarme të rreme!}",
            font_size=SMALL_SIZE, color=AUX_COLOR,
        )
        false_label.next_to(false_bar, DOWN, buff=0.2)

        self.play(DrawBorderThenFill(true_bar), FadeIn(true_label), run_time=0.8)
        self.wait(0.5)
        self.play(DrawBorderThenFill(false_bar), FadeIn(false_label), run_time=0.8)
        self.wait(0.8)

        # Total
        total = MathTex(
            r"\text{Total pozitiv: } 1.568 + 7.984 = 9.552",
            font_size=BODY_SIZE, color=WHITE,
        )
        total.next_to(false_label, DOWN, buff=0.5)
        self.play(Write(total), run_time=0.8)
        self.wait(1.5)

        self.bar_mobs = VGroup(
            title, true_bar, true_label, false_bar, false_label, total,
        )

    # ────────────────────────────────────────────
    #  REVEAL — the answer (32–45s)
    # ────────────────────────────────────────────

    def reveal(self):
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

        q = MathTex(
            r"\text{Sa nga pozitivët janë vërtet të sëmurë?}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        q.move_to(UP * 3.5)
        self.play(FadeIn(q), run_time=0.5)

        formula = MathTex(
            r"P(S|P) = \frac{1.568}{9.552}",
            font_size=EQ_SIZE, color=WHITE,
        )
        formula.next_to(q, DOWN, buff=0.6)
        self.play(Write(formula), run_time=0.8)
        self.wait(1.0)

        answer = MathTex(
            r"\approx 0{,}164 = 16{,}4\%",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        answer.next_to(formula, DOWN, buff=0.5)
        box = make_answer_box(answer)

        self.play(Write(answer), run_time=0.8)
        self.play(Create(box), run_time=0.4)
        self.play(Circumscribe(VGroup(answer, box), color=HIGHLIGHT_COLOR, run_time=0.8))
        self.play(
            Flash(answer.get_center(), color=ANSWER_COLOR,
                  num_lines=12, line_length=0.3, run_time=0.5),
        )

        # The punchline
        punchline = MathTex(
            r"\text{Vetëm 16\% — JO 98\%!}",
            font_size=HOOK_SIZE, color=HIGHLIGHT_COLOR,
        )
        punchline.next_to(box, DOWN, buff=0.6)
        self.play(FadeIn(punchline, shift=UP * 0.2), run_time=0.6)

        why = MathTex(
            r"\text{Sëmundja: shumë e rrallë (1 në 500)}",
            font_size=SMALL_SIZE, color=BODY_TEXT_COLOR,
        )
        why.next_to(punchline, DOWN, buff=0.3)
        self.play(FadeIn(why), run_time=0.5)
        self.wait(3.0)

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
