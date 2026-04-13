"""
Reel A — Ushtrimi 5, Njësia 8.4A
"Diagrami pemë i frekuencave — testi i dopingut"

Standalone reel: 500 athletes, 20% use drugs.
Users: 95 positive / 5 negative.  Non-users: 8 positive / 392 negative.
Builds the full frequency tree.
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


class ReelA(Scene):
    def construct(self):
        apply_style(self)
        MathTex.set_default(tex_template=ALBANIAN_TEX)
        Tex.set_default(tex_template=ALBANIAN_TEX)

        self.hook()
        self.frequency_tree()
        self.cta()

    # -----------------------------------------------
    #  HOOK (0-10s)
    # -----------------------------------------------

    def hook(self):
        line1 = MathTex(
            r"\text{500 atletë testohen për doping.}",
            font_size=HOOK_SIZE, color=WHITE,
        )
        line2 = MathTex(
            r"\text{20\% përdorin barna.}",
            font_size=HOOK_SIZE, color=AUX_COLOR,
        )
        line3 = MathTex(
            r"\text{Testi nuk është perfekt...}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        hook_group = VGroup(line1, line2, line3).arrange(DOWN, buff=0.35)
        hook_group.move_to(UP * 2.5)

        ask = MathTex(
            r"\text{Si duket diagrami pemë?}",
            font_size=QUESTION_SIZE, color=HIGHLIGHT_COLOR,
        )
        ask.next_to(hook_group, DOWN, buff=0.7)

        self.play(FadeIn(hook_group, shift=UP * 0.4), run_time=1.2)
        self.wait(2.5)
        self.play(FadeIn(ask, shift=UP * 0.3), run_time=0.8)
        self.wait(2.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # -----------------------------------------------
    #  FREQUENCY TREE (10-42s)
    # -----------------------------------------------

    def frequency_tree(self):
        title = MathTex(
            r"\text{Diagrami i frekuencave:}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        title.move_to(UP * SAFE_TOP)
        self.play(FadeIn(title), run_time=0.5)

        # ---- Root: 500 ----
        root = MathTex(r"500", font_size=EQ_SIZE, color=WHITE)
        root.move_to(UP * 3.5)
        self.play(GrowFromCenter(root), run_time=0.5)

        # ---- Level 1 positions ----
        user_pos = LEFT * 2.5 + UP * 1.5
        clean_pos = RIGHT * 2.5 + UP * 1.5

        line_user = Line(root.get_bottom(), user_pos + UP * 0.35, buff=0.1,
                         color=AUX_COLOR, stroke_width=2.5)
        line_clean = Line(root.get_bottom(), clean_pos + UP * 0.35, buff=0.1,
                          color=SHAPE_COLOR, stroke_width=2.5)

        # Node labels
        user_node = MathTex(r"100", font_size=EQ_SIZE, color=AUX_COLOR)
        user_node.move_to(user_pos)
        user_sub = MathTex(r"\text{Përdorues}", font_size=SMALL_SIZE, color=AUX_COLOR)
        user_sub.next_to(user_node, DOWN, buff=0.15)

        clean_node = MathTex(r"400", font_size=EQ_SIZE, color=SHAPE_COLOR)
        clean_node.move_to(clean_pos)
        clean_sub = MathTex(r"\text{Jo-përdorues}", font_size=SMALL_SIZE, color=SHAPE_COLOR)
        clean_sub.next_to(clean_node, DOWN, buff=0.15)

        # Branch calculations
        calc_user = MathTex(r"500 \times 0{,}2", font_size=SMALL_SIZE, color=AUX_COLOR)
        calc_user.move_to(line_user.get_center() + LEFT * 0.15 + UP * 0.35)
        calc_clean = MathTex(r"500 \times 0{,}8", font_size=SMALL_SIZE, color=SHAPE_COLOR)
        calc_clean.move_to(line_clean.get_center() + RIGHT * 0.15 + UP * 0.35)

        self.play(Create(line_user), Create(line_clean), run_time=0.6)
        self.play(
            GrowFromCenter(user_node), FadeIn(user_sub),
            GrowFromCenter(clean_node), FadeIn(clean_sub),
            run_time=0.6,
        )
        self.play(FadeIn(calc_user), FadeIn(calc_clean), run_time=0.5)
        self.wait(1.5)

        # ---- Level 2 — user branches ----
        up_pos = LEFT * 3.5 + DOWN * 0.8    # user positive
        un_pos = LEFT * 1.5 + DOWN * 0.8    # user negative

        line_up = Line(user_node.get_bottom() + DOWN * 0.3, up_pos + UP * 0.35, buff=0.1,
                       color=LABEL_COLOR, stroke_width=2.5)
        line_un = Line(user_node.get_bottom() + DOWN * 0.3, un_pos + UP * 0.35, buff=0.1,
                       color=ANSWER_COLOR, stroke_width=2.5)

        up_node = MathTex(r"95", font_size=EQ_SIZE, color=LABEL_COLOR)
        up_node.move_to(up_pos)
        up_sub = MathTex(r"\text{Pozitiv}", font_size=SMALL_SIZE, color=LABEL_COLOR)
        up_sub.next_to(up_node, DOWN, buff=0.15)

        un_node = MathTex(r"5", font_size=EQ_SIZE, color=ANSWER_COLOR)
        un_node.move_to(un_pos)
        un_sub = MathTex(r"\text{Negativ}", font_size=SMALL_SIZE, color=ANSWER_COLOR)
        un_sub.next_to(un_node, DOWN, buff=0.15)

        self.play(Create(line_up), Create(line_un), run_time=0.6)
        self.play(
            GrowFromCenter(up_node), FadeIn(up_sub),
            GrowFromCenter(un_node), FadeIn(un_sub),
            run_time=0.5,
        )
        self.wait(1.0)

        # ---- Level 2 — clean branches ----
        cp_pos = RIGHT * 1.5 + DOWN * 0.8   # clean positive (false alarm!)
        cn_pos = RIGHT * 3.5 + DOWN * 0.8   # clean negative

        line_cp = Line(clean_node.get_bottom() + DOWN * 0.3, cp_pos + UP * 0.35, buff=0.1,
                       color=HIGHLIGHT_COLOR, stroke_width=2.5)
        line_cn = Line(clean_node.get_bottom() + DOWN * 0.3, cn_pos + UP * 0.35, buff=0.1,
                       color=ANSWER_COLOR, stroke_width=2.5)

        cp_node = MathTex(r"8", font_size=EQ_SIZE, color=HIGHLIGHT_COLOR)
        cp_node.move_to(cp_pos)
        cp_sub = MathTex(r"\text{Pozitiv}", font_size=SMALL_SIZE, color=HIGHLIGHT_COLOR)
        cp_sub.next_to(cp_node, DOWN, buff=0.15)

        cn_node = MathTex(r"392", font_size=EQ_SIZE, color=ANSWER_COLOR)
        cn_node.move_to(cn_pos)
        cn_sub = MathTex(r"\text{Negativ}", font_size=SMALL_SIZE, color=ANSWER_COLOR)
        cn_sub.next_to(cn_node, DOWN, buff=0.15)

        self.play(Create(line_cp), Create(line_cn), run_time=0.6)
        self.play(
            GrowFromCenter(cp_node), FadeIn(cp_sub),
            GrowFromCenter(cn_node), FadeIn(cn_sub),
            run_time=0.5,
        )
        self.wait(1.0)

        # Flash the false-alarm node
        self.play(
            Indicate(cp_node, color=HIGHLIGHT_COLOR, scale_factor=1.3),
            run_time=0.8,
        )

        # Legend
        legend = VGroup(
            MathTex(r"\text{Përdorues: 100 (20\%)}", font_size=SMALL_SIZE, color=AUX_COLOR),
            MathTex(r"\text{Jo-përdorues: 400 (80\%)}", font_size=SMALL_SIZE, color=SHAPE_COLOR),
        ).arrange(DOWN, buff=0.2)
        legend.move_to(DOWN * 2.6)

        self.play(FadeIn(legend, shift=UP * 0.2), run_time=0.6)
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
