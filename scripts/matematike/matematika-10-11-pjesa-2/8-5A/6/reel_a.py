"""
Reel A — Ushtrimi 6, Njësia 8.5A
"Diagrami pemë i frekuencave" — Frequency tree for medical test

Standalone reel: states the medical test problem, builds a frequency tree
showing how 800,000 people split into sick/healthy, then positive/negative.
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


class ReelA(Scene):
    def construct(self):
        apply_style(self)
        MathTex.set_default(tex_template=ALBANIAN_TEX)
        Tex.set_default(tex_template=ALBANIAN_TEX)

        self.hook()
        self.build_tree()
        self.bonus()
        self.cta()

    # -----------------------------------------------
    #  HOOK — state the problem (0-10s)
    # -----------------------------------------------

    def hook(self):
        line1 = MathTex(
            r"\text{800.000 njerëz testohen}",
            font_size=HOOK_SIZE, color=WHITE,
        )
        line2 = MathTex(
            r"\text{për një sëmundje.}",
            font_size=HOOK_SIZE, color=WHITE,
        )
        line3 = MathTex(
            r"\text{Sëmundja: 1 në 500}",
            font_size=BODY_SIZE, color=SHAPE_COLOR,
        )
        line4 = MathTex(
            r"\text{Testi: 98\% i saktë}",
            font_size=BODY_SIZE, color=LABEL_COLOR,
        )
        line5 = MathTex(
            r"\text{1\% alarm i rremë}",
            font_size=BODY_SIZE, color=AUX_COLOR,
        )

        hook_group = VGroup(line1, line2, line3, line4, line5).arrange(DOWN, buff=0.35)
        hook_group.move_to(UP * 2.5)

        ask = MathTex(
            r"\text{Si ndahen numrat?}",
            font_size=QUESTION_SIZE, color=HIGHLIGHT_COLOR,
        )
        ask.next_to(hook_group, DOWN, buff=0.7)

        self.play(FadeIn(hook_group, shift=UP * 0.4), run_time=1.2)
        self.wait(3.0)
        self.play(FadeIn(ask, shift=UP * 0.3), run_time=0.8)
        self.wait(2.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # -----------------------------------------------
    #  BUILD FREQUENCY TREE (10-35s)
    # -----------------------------------------------

    def build_tree(self):
        title = MathTex(
            r"\text{Diagrami pemë i frekuencave:}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        title.move_to(UP * SAFE_TOP)
        self.play(FadeIn(title), run_time=0.5)

        # ---- Level 0: Root ----
        root = MathTex(r"800.000", font_size=BODY_SIZE, color=WHITE)
        root.move_to(UP * 3.6)
        self.play(GrowFromCenter(root), run_time=0.5)

        # ---- Level 1: Sick / Healthy ----
        sick_label = MathTex(r"1.600", font_size=BODY_SIZE, color=SHAPE_COLOR)
        healthy_label = MathTex(r"798.400", font_size=BODY_SIZE, color=AUX_COLOR)
        sick_label.move_to(LEFT * 2.5 + UP * 1.4)
        healthy_label.move_to(RIGHT * 2.5 + UP * 1.4)

        sick_tag = MathTex(r"\text{të sëmurë}", font_size=TINY_SIZE, color=SHAPE_COLOR)
        sick_tag.next_to(sick_label, DOWN, buff=0.15)
        healthy_tag = MathTex(r"\text{të shëndetshëm}", font_size=TINY_SIZE, color=AUX_COLOR)
        healthy_tag.next_to(healthy_label, DOWN, buff=0.15)

        line_sick = Line(root.get_bottom(), sick_label.get_top(), buff=0.15,
                         color=SHAPE_COLOR, stroke_width=2.5)
        line_healthy = Line(root.get_bottom(), healthy_label.get_top(), buff=0.15,
                            color=AUX_COLOR, stroke_width=2.5)

        self.play(Create(line_sick), Create(line_healthy), run_time=0.7)
        self.play(
            GrowFromCenter(sick_label), GrowFromCenter(healthy_label),
            run_time=0.5,
        )
        self.play(FadeIn(sick_tag), FadeIn(healthy_tag), run_time=0.4)
        self.wait(1.0)

        # ---- Level 2: Sick branch → Pos / Neg ----
        sick_pos = MathTex(r"1.568", font_size=SMALL_SIZE, color=ANSWER_COLOR)
        sick_neg = MathTex(r"32", font_size=SMALL_SIZE, color=LABEL_COLOR)
        sick_pos.move_to(LEFT * 3.5 + DOWN * 0.8)
        sick_neg.move_to(LEFT * 1.5 + DOWN * 0.8)

        sp_tag = MathTex(r"+", font_size=SMALL_SIZE, color=ANSWER_COLOR)
        sp_tag.next_to(sick_pos, DOWN, buff=0.1)
        sn_tag = MathTex(r"-", font_size=SMALL_SIZE, color=LABEL_COLOR)
        sn_tag.next_to(sick_neg, DOWN, buff=0.1)

        line_sp = Line(sick_label.get_bottom() + DOWN * 0.3, sick_pos.get_top(), buff=0.15,
                       color=ANSWER_COLOR, stroke_width=2.5)
        line_sn = Line(sick_label.get_bottom() + DOWN * 0.3, sick_neg.get_top(), buff=0.15,
                       color=LABEL_COLOR, stroke_width=2.5)

        # Branch labels (percentages)
        p_sp = MathTex(r"98\%", font_size=TINY_SIZE, color=ANSWER_COLOR)
        p_sp.move_to(line_sp.get_center() + LEFT * 0.55)
        p_sn = MathTex(r"2\%", font_size=TINY_SIZE, color=LABEL_COLOR)
        p_sn.move_to(line_sn.get_center() + RIGHT * 0.45)

        self.play(Create(line_sp), Create(line_sn), run_time=0.6)
        self.play(
            GrowFromCenter(sick_pos), GrowFromCenter(sick_neg),
            FadeIn(sp_tag), FadeIn(sn_tag),
            run_time=0.5,
        )
        self.play(FadeIn(p_sp), FadeIn(p_sn), run_time=0.4)
        self.wait(0.8)

        # ---- Level 2: Healthy branch → Pos / Neg ----
        healthy_pos = MathTex(r"7.984", font_size=SMALL_SIZE, color=HIGHLIGHT_COLOR)
        healthy_neg = MathTex(r"790.416", font_size=SMALL_SIZE, color=ANSWER_COLOR)
        healthy_pos.move_to(RIGHT * 1.5 + DOWN * 0.8)
        healthy_neg.move_to(RIGHT * 3.5 + DOWN * 0.8)

        hp_tag = MathTex(r"+", font_size=SMALL_SIZE, color=HIGHLIGHT_COLOR)
        hp_tag.next_to(healthy_pos, DOWN, buff=0.1)
        hn_tag = MathTex(r"-", font_size=SMALL_SIZE, color=ANSWER_COLOR)
        hn_tag.next_to(healthy_neg, DOWN, buff=0.1)

        line_hp = Line(healthy_label.get_bottom() + DOWN * 0.3, healthy_pos.get_top(), buff=0.15,
                       color=HIGHLIGHT_COLOR, stroke_width=2.5)
        line_hn = Line(healthy_label.get_bottom() + DOWN * 0.3, healthy_neg.get_top(), buff=0.15,
                       color=ANSWER_COLOR, stroke_width=2.5)

        p_hp = MathTex(r"1\%", font_size=TINY_SIZE, color=HIGHLIGHT_COLOR)
        p_hp.move_to(line_hp.get_center() + LEFT * 0.45)
        p_hn = MathTex(r"99\%", font_size=TINY_SIZE, color=ANSWER_COLOR)
        p_hn.move_to(line_hn.get_center() + RIGHT * 0.55)

        self.play(Create(line_hp), Create(line_hn), run_time=0.6)
        self.play(
            GrowFromCenter(healthy_pos), GrowFromCenter(healthy_neg),
            FadeIn(hp_tag), FadeIn(hn_tag),
            run_time=0.5,
        )
        self.play(FadeIn(p_hp), FadeIn(p_hn), run_time=0.4)
        self.wait(1.5)

        # ---- Legend ----
        legend = VGroup(
            MathTex(r"\text{+ = pozitiv, -- = negativ}", font_size=TINY_SIZE, color=BODY_TEXT_COLOR),
        )
        legend.move_to(DOWN * 1.8)
        self.play(FadeIn(legend, shift=UP * 0.2), run_time=0.5)
        self.wait(2.0)

        # Store tree for later reference
        self.tree_group = VGroup(
            title, root, line_sick, line_healthy, sick_label, healthy_label,
            sick_tag, healthy_tag,
            line_sp, line_sn, sick_pos, sick_neg, sp_tag, sn_tag, p_sp, p_sn,
            line_hp, line_hn, healthy_pos, healthy_neg, hp_tag, hn_tag, p_hp, p_hn,
            legend,
        )

    # -----------------------------------------------
    #  BONUS — P(S|N) (35-42s)
    # -----------------------------------------------

    def bonus(self):
        # Shift tree up slightly to make room
        self.play(self.tree_group.animate.shift(UP * 0.6), run_time=0.5)

        bonus_title = MathTex(
            r"\text{Testi negativ = pothuajse i sigurt!}",
            font_size=SMALL_SIZE, color=STEP_TITLE_COLOR,
        )
        bonus_title.move_to(DOWN * 2.5)

        eq = MathTex(
            r"P(S|N) = \frac{32}{790.448} \approx 0{,}00004",
            font_size=SMALL_SIZE, color=ANSWER_COLOR,
        )
        eq.next_to(bonus_title, DOWN, buff=0.3)

        self.play(FadeIn(bonus_title, shift=UP * 0.2), run_time=0.5)
        self.play(Write(eq), run_time=1.0)

        box = make_answer_box(eq)
        self.play(Create(box), run_time=0.4)
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
