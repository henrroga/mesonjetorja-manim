"""
Reel B — Ushtrimi 5, Njësia 8.4A
"Sa atletë gjithsej dalin pozitiv?"

Standalone reel: re-establishes the doping-test context,
shows compact tree with the two positive branches highlighted,
calculates 95 + 8 = 103 total positives.
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
        self.compact_tree()
        self.calculate()
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
            r"\text{100 përdorin barna, 400 jo.}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        hook_group = VGroup(line1, line2).arrange(DOWN, buff=0.35)
        hook_group.move_to(UP * 2.5)

        ask = MathTex(
            r"\text{Sa atletë gjithsej dalin pozitiv?}",
            font_size=QUESTION_SIZE, color=HIGHLIGHT_COLOR,
        )
        ask.next_to(hook_group, DOWN, buff=0.7)

        self.play(FadeIn(hook_group, shift=UP * 0.4), run_time=1.2)
        self.wait(2.0)
        self.play(FadeIn(ask, shift=UP * 0.3), run_time=0.8)
        self.wait(2.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # -----------------------------------------------
    #  COMPACT TREE (8-28s)
    # -----------------------------------------------

    def compact_tree(self):
        title = MathTex(
            r"\text{Nga diagrami pemë:}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        title.move_to(UP * SAFE_TOP)
        self.play(FadeIn(title), run_time=0.5)

        # Root
        root = MathTex(r"500", font_size=EQ_SIZE, color=WHITE)
        root.move_to(UP * 3.5)
        self.play(GrowFromCenter(root), run_time=0.4)

        # Level 1
        user_pos = LEFT * 2.5 + UP * 1.5
        clean_pos = RIGHT * 2.5 + UP * 1.5

        line_user = Line(root.get_bottom(), user_pos + UP * 0.35, buff=0.1,
                         color=AUX_COLOR, stroke_width=2.5)
        line_clean = Line(root.get_bottom(), clean_pos + UP * 0.35, buff=0.1,
                          color=SHAPE_COLOR, stroke_width=2.5)

        user_node = MathTex(r"100", font_size=EQ_SIZE, color=AUX_COLOR)
        user_node.move_to(user_pos)
        clean_node = MathTex(r"400", font_size=EQ_SIZE, color=SHAPE_COLOR)
        clean_node.move_to(clean_pos)

        self.play(
            Create(line_user), Create(line_clean),
            GrowFromCenter(user_node), GrowFromCenter(clean_node),
            run_time=0.7,
        )
        self.wait(0.5)

        # Level 2 — all four endpoints
        up_pos = LEFT * 3.5 + DOWN * 0.5
        un_pos = LEFT * 1.5 + DOWN * 0.5
        cp_pos = RIGHT * 1.5 + DOWN * 0.5
        cn_pos = RIGHT * 3.5 + DOWN * 0.5

        line_up = Line(user_node.get_bottom(), up_pos + UP * 0.35, buff=0.1,
                       color=LABEL_COLOR, stroke_width=2.5)
        line_un = Line(user_node.get_bottom(), un_pos + UP * 0.35, buff=0.1,
                       color=BODY_TEXT_COLOR, stroke_width=1.5)
        line_cp = Line(clean_node.get_bottom(), cp_pos + UP * 0.35, buff=0.1,
                       color=HIGHLIGHT_COLOR, stroke_width=2.5)
        line_cn = Line(clean_node.get_bottom(), cn_pos + UP * 0.35, buff=0.1,
                       color=BODY_TEXT_COLOR, stroke_width=1.5)

        up_node = MathTex(r"95", font_size=EQ_SIZE, color=LABEL_COLOR)
        up_node.move_to(up_pos)
        up_sub = MathTex(r"\text{Poz.}", font_size=SMALL_SIZE, color=LABEL_COLOR)
        up_sub.next_to(up_node, DOWN, buff=0.12)

        un_node = MathTex(r"5", font_size=BODY_SIZE, color=BODY_TEXT_COLOR)
        un_node.move_to(un_pos)
        un_sub = MathTex(r"\text{Neg.}", font_size=SMALL_SIZE, color=BODY_TEXT_COLOR)
        un_sub.next_to(un_node, DOWN, buff=0.12)

        cp_node = MathTex(r"8", font_size=EQ_SIZE, color=HIGHLIGHT_COLOR)
        cp_node.move_to(cp_pos)
        cp_sub = MathTex(r"\text{Poz.}", font_size=SMALL_SIZE, color=HIGHLIGHT_COLOR)
        cp_sub.next_to(cp_node, DOWN, buff=0.12)

        cn_node = MathTex(r"392", font_size=BODY_SIZE, color=BODY_TEXT_COLOR)
        cn_node.move_to(cn_pos)
        cn_sub = MathTex(r"\text{Neg.}", font_size=SMALL_SIZE, color=BODY_TEXT_COLOR)
        cn_sub.next_to(cn_node, DOWN, buff=0.12)

        self.play(
            Create(line_up), Create(line_un),
            Create(line_cp), Create(line_cn),
            run_time=0.6,
        )
        self.play(
            GrowFromCenter(up_node), FadeIn(up_sub),
            GrowFromCenter(un_node), FadeIn(un_sub),
            GrowFromCenter(cp_node), FadeIn(cp_sub),
            GrowFromCenter(cn_node), FadeIn(cn_sub),
            run_time=0.6,
        )
        self.wait(1.5)

        # Highlight the two positive endpoints
        self.play(
            Indicate(up_node, color=LABEL_COLOR, scale_factor=1.3),
            Indicate(cp_node, color=HIGHLIGHT_COLOR, scale_factor=1.3),
            run_time=0.8,
        )
        self.wait(1.0)

        # Store references
        self.up_node = up_node
        self.cp_node = cp_node

    # -----------------------------------------------
    #  CALCULATE (28-42s)
    # -----------------------------------------------

    def calculate(self):
        # Sum equation
        sum_title = MathTex(
            r"\text{Pozitivë gjithsej:}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        sum_title.move_to(DOWN * 2.0)

        sum_eq = MathTex(
            r"95 + 8 = 103",
            font_size=EQ_SIZE, color=LABEL_COLOR,
        )
        sum_eq.next_to(sum_title, DOWN, buff=0.4)

        self.play(FadeIn(sum_title), run_time=0.5)
        self.play(Write(sum_eq), run_time=1.0)
        self.wait(1.5)

        # Answer screen
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
