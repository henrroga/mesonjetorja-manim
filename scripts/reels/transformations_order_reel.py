"""
Vertical Reel — Order Matters! (Exercise 8: a vs b)
====================================================

9:16 vertical (1080×1920), ~50 seconds.
Hook: "Does the order of transformations matter?"
Shows the SAME two operations in different order give DIFFERENT results.
Standalone "aha moment" reel.

Render:
    cd scripts && manim -qh reels/transformations_order_reel.py TransformationsOrderReel
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from manim import *
import numpy as np
from style_guide import (
    BG_COLOR, ALBANIAN_TEX,
    STEP_TITLE_COLOR, BODY_TEXT_COLOR, LABEL_COLOR,
    ANSWER_COLOR, SHAPE_COLOR, AUX_COLOR, HIGHLIGHT_COLOR, DIVIDER_COLOR,
)

# ── Vertical frame config ──
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 8
config.frame_height = 8 * (1920 / 1080)

SAFE_TOP = 4.8
SAFE_BOTTOM = -3.3
SAFE_CENTER_X = 0.0
SAFE_CENTER_Y = (SAFE_TOP + SAFE_BOTTOM) / 2

ORIG_COLOR = SHAPE_COLOR
RESULT_A_COLOR = ANSWER_COLOR
RESULT_B_COLOR = AUX_COLOR
LINE_COLOR = LABEL_COLOR
EQUIV_A_COLOR = ANSWER_COLOR
EQUIV_B_COLOR = AUX_COLOR


def reflect(px, py):
    return (py + 1, px - 1)


def translate(px, py):
    return (px - 4, py + 4)


class TransformationsOrderReel(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        MathTex.set_default(tex_template=ALBANIAN_TEX)
        Tex.set_default(tex_template=ALBANIAN_TEX)

        self.hook()
        self.show_order_a()
        self.show_order_b()
        self.comparison()
        self.punchline()

    # ── HOOK (0-4s) ──
    def hook(self):
        hook1 = MathTex(
            r"\text{A ka rëndësi}",
            font_size=50, color=WHITE,
        )
        hook2 = MathTex(
            r"\text{RADHA?}",
            font_size=72, color=HIGHLIGHT_COLOR,
        )
        hook_g = VGroup(hook1, hook2).arrange(DOWN, buff=0.35)
        hook_g.move_to(UP * 1.5)

        sub1 = MathTex(
            r"\text{Simetri + Zhvendosje}",
            font_size=30, color=ANSWER_COLOR,
        )
        vs = MathTex(r"\text{vs}", font_size=36, color=WHITE)
        sub2 = MathTex(
            r"\text{Zhvendosje + Simetri}",
            font_size=30, color=AUX_COLOR,
        )
        sub_g = VGroup(sub1, vs, sub2).arrange(DOWN, buff=0.25)
        sub_g.next_to(hook_g, DOWN, buff=0.8)

        self.play(
            FadeIn(hook_g, shift=UP * 0.5),
            run_time=0.7,
        )
        self.play(
            hook2.animate.scale(1.1),
            rate_func=there_and_back, run_time=0.5,
        )
        self.play(
            LaggedStart(
                FadeIn(sub1, shift=RIGHT * 0.3),
                FadeIn(vs),
                FadeIn(sub2, shift=LEFT * 0.3),
                lag_ratio=0.2,
            ),
            run_time=0.8,
        )
        self.wait(1.0)
        self.play(FadeOut(hook_g), FadeOut(sub_g), run_time=0.4)

    # ── ORDER A: Reflect then Translate (4-18s) ──
    def show_order_a(self):
        title = MathTex(
            r"\text{Radha A: Simetri pastaj Zhvendosje}",
            font_size=26, color=RESULT_A_COLOR,
        )
        title.move_to(UP * SAFE_TOP - UP * 0.3)

        axes = Axes(
            x_range=[-3, 7, 1], y_range=[-2, 7, 1],
            x_length=5.0, y_length=4.5,
            axis_config={
                "include_tip": True, "include_numbers": True,
                "font_size": 12, "color": DIVIDER_COLOR,
            },
        )
        axes.move_to(UP * 1.5)
        ax_l = axes.get_axis_labels(
            x_label=MathTex("x", font_size=14),
            y_label=MathTex("y", font_size=14),
        )

        A, B, C = (2, 2), (3, 2), (2, 4)
        # Reflect first, then translate
        A1, B1, C1 = reflect(*A), reflect(*B), reflect(*C)
        A2 = translate(*A1)
        B2 = translate(*B1)
        C2 = translate(*C1)

        tri_o = Polygon(
            axes.c2p(*A), axes.c2p(*B), axes.c2p(*C),
            color=ORIG_COLOR, fill_color=ORIG_COLOR,
            fill_opacity=0.2, stroke_width=2,
        )
        tri_f = Polygon(
            axes.c2p(*A2), axes.c2p(*B2), axes.c2p(*C2),
            color=RESULT_A_COLOR, fill_color=RESULT_A_COLOR,
            fill_opacity=0.25, stroke_width=2.5,
        )
        lbl_o = MathTex("ABC", font_size=18, color=ORIG_COLOR)
        lbl_o.move_to(tri_o.get_center() + DR * 0.3)
        lbl_f = MathTex("A_2B_2C_2", font_size=16, color=RESULT_A_COLOR)
        lbl_f.move_to(tri_f.get_center() + UL * 0.3)

        # Ref line
        ref_line = axes.plot(lambda x: x - 1, x_range=[-1, 6],
                             color=LINE_COLOR, stroke_width=1.5)

        # Result text
        res = MathTex(
            r"A_2(-1,5),\; B_2(-1,6),\; C_2(1,5)",
            font_size=22, color=RESULT_A_COLOR,
        )
        res.move_to(DOWN * 1.5)

        equiv = MathTex(
            r"\text{= Simetri sipas } y = -x + 4",
            font_size=28, color=RESULT_A_COLOR,
        )
        equiv.next_to(res, DOWN, buff=0.4)
        eq_box = SurroundingRectangle(equiv, color=RESULT_A_COLOR,
                                       buff=0.15, corner_radius=0.08)

        self.play(FadeIn(title), run_time=0.4)
        self.play(Create(axes), FadeIn(ax_l), run_time=0.6)
        self.play(Create(ref_line), run_time=0.4)
        self.play(DrawBorderThenFill(tri_o), FadeIn(lbl_o), run_time=0.6)
        self.wait(0.3)

        # Animate: ghost copy morphs to final position
        tri_ghost = tri_o.copy()
        self.play(Transform(tri_ghost, tri_f), run_time=1.0)
        self.remove(tri_ghost)
        self.add(tri_f)
        self.play(FadeIn(lbl_f), run_time=0.3)

        self.play(Write(res), run_time=0.6)
        self.play(Write(equiv), Create(eq_box), run_time=0.7)
        self.wait(1.5)

        self.order_a_group = VGroup(
            title, axes, ax_l, ref_line, tri_o, lbl_o,
            tri_f, lbl_f, res, equiv, eq_box,
        )
        self.play(FadeOut(self.order_a_group), run_time=0.4)

    # ── ORDER B: Translate then Reflect (18-32s) ──
    def show_order_b(self):
        title = MathTex(
            r"\text{Radha B: Zhvendosje pastaj Simetri}",
            font_size=26, color=RESULT_B_COLOR,
        )
        title.move_to(UP * SAFE_TOP - UP * 0.3)

        axes = Axes(
            x_range=[-4, 11, 1], y_range=[-5, 10, 1],
            x_length=5.0, y_length=5.0,
            axis_config={
                "include_tip": True, "include_numbers": True,
                "font_size": 10, "color": DIVIDER_COLOR,
            },
        )
        axes.move_to(UP * 1.5)
        ax_l = axes.get_axis_labels(
            x_label=MathTex("x", font_size=14),
            y_label=MathTex("y", font_size=14),
        )

        A, B, C = (2, 2), (3, 2), (2, 4)
        # Translate first, then reflect
        A1p = translate(*A)
        B1p = translate(*B)
        C1p = translate(*C)
        A2p = reflect(*A1p)
        B2p = reflect(*B1p)
        C2p = reflect(*C1p)

        tri_o = Polygon(
            axes.c2p(*A), axes.c2p(*B), axes.c2p(*C),
            color=ORIG_COLOR, fill_color=ORIG_COLOR,
            fill_opacity=0.2, stroke_width=2,
        )
        tri_f = Polygon(
            axes.c2p(*A2p), axes.c2p(*B2p), axes.c2p(*C2p),
            color=RESULT_B_COLOR, fill_color=RESULT_B_COLOR,
            fill_opacity=0.25, stroke_width=2.5,
        )
        lbl_o = MathTex("ABC", font_size=16, color=ORIG_COLOR)
        lbl_o.move_to(tri_o.get_center() + DR * 0.2)
        lbl_f = MathTex("A'_2B'_2C'_2", font_size=14, color=RESULT_B_COLOR)
        lbl_f.move_to(tri_f.get_center() + DL * 0.3)

        ref_line = axes.plot(lambda x: x - 1, x_range=[-3, 10],
                             color=LINE_COLOR, stroke_width=1.5)

        res = MathTex(
            r"A'_2(7,-3),\; B'_2(7,-2),\; C'_2(9,-3)",
            font_size=22, color=RESULT_B_COLOR,
        )
        res.move_to(DOWN * 1.5)

        equiv = MathTex(
            r"\text{= Simetri sipas } y = -x + 5",
            font_size=28, color=RESULT_B_COLOR,
        )
        equiv.next_to(res, DOWN, buff=0.4)
        eq_box = SurroundingRectangle(equiv, color=RESULT_B_COLOR,
                                       buff=0.15, corner_radius=0.08)

        self.play(FadeIn(title), run_time=0.4)
        self.play(Create(axes), FadeIn(ax_l), run_time=0.6)
        self.play(Create(ref_line), run_time=0.4)
        self.play(DrawBorderThenFill(tri_o), FadeIn(lbl_o), run_time=0.6)
        self.wait(0.3)

        tri_ghost = tri_o.copy()
        self.play(Transform(tri_ghost, tri_f), run_time=1.0)
        self.remove(tri_ghost)
        self.add(tri_f)
        self.play(FadeIn(lbl_f), run_time=0.3)

        self.play(Write(res), run_time=0.6)
        self.play(Write(equiv), Create(eq_box), run_time=0.7)
        self.wait(1.5)

        self.order_b_group = VGroup(
            title, axes, ax_l, ref_line, tri_o, lbl_o,
            tri_f, lbl_f, res, equiv, eq_box,
        )
        self.play(FadeOut(self.order_b_group), run_time=0.4)

    # ── COMPARISON (32-45s) ──
    def comparison(self):
        title = MathTex(
            r"\text{Krahasimi:}",
            font_size=40, color=WHITE,
        )
        title.move_to(UP * 4.0)

        # Card A
        card_a_title = MathTex(
            r"\text{Simetri pastaj Zhvendosje}",
            font_size=26, color=RESULT_A_COLOR,
        )
        card_a_res = MathTex(
            r"y = -x + 4",
            font_size=40, color=RESULT_A_COLOR,
        )
        card_a = VGroup(card_a_title, card_a_res).arrange(DOWN, buff=0.3)
        box_a = SurroundingRectangle(card_a, color=RESULT_A_COLOR,
                                      buff=0.3, corner_radius=0.1)
        group_a = VGroup(card_a, box_a)

        # VS
        vs = MathTex(r"\neq", font_size=60, color=HIGHLIGHT_COLOR)

        # Card B
        card_b_title = MathTex(
            r"\text{Zhvendosje pastaj Simetri}",
            font_size=26, color=RESULT_B_COLOR,
        )
        card_b_res = MathTex(
            r"y = -x + 5",
            font_size=40, color=RESULT_B_COLOR,
        )
        card_b = VGroup(card_b_title, card_b_res).arrange(DOWN, buff=0.3)
        box_b = SurroundingRectangle(card_b, color=RESULT_B_COLOR,
                                      buff=0.3, corner_radius=0.1)
        group_b = VGroup(card_b, box_b)

        comparison = VGroup(group_a, vs, group_b).arrange(DOWN, buff=0.6)
        comparison.move_to(UP * 0.5)

        self.play(Write(title), run_time=0.5)
        self.play(FadeIn(group_a, shift=LEFT * 0.5), run_time=0.7)
        self.wait(0.5)
        self.play(Write(vs), run_time=0.4)
        self.play(FadeIn(group_b, shift=RIGHT * 0.5), run_time=0.7)
        self.wait(0.5)

        # Dramatic pulse on the ≠
        self.play(
            vs.animate.scale(1.4),
            rate_func=there_and_back, run_time=0.6,
        )
        self.play(
            Flash(vs.get_center(), color=HIGHLIGHT_COLOR,
                  line_length=0.3, num_lines=12, run_time=0.5),
        )
        self.wait(1.5)

        self.comparison_group = VGroup(title, comparison)

    # ── PUNCHLINE (45-55s) ──
    def punchline(self):
        self.play(FadeOut(self.comparison_group), run_time=0.4)

        msg1 = MathTex(
            r"\text{RADHA KA RËNDËSI!}",
            font_size=44, color=HIGHLIGHT_COLOR,
        )
        msg1.move_to(UP * 2.0)

        msg2 = MathTex(
            r"\text{Shndërrimet gjeometrike}",
            font_size=30, color=WHITE,
        )
        msg3 = MathTex(
            r"\text{nuk janë të këmbyeshme.}",
            font_size=30, color=WHITE,
        )
        msg_g = VGroup(msg2, msg3).arrange(DOWN, buff=0.2)
        msg_g.move_to(UP * 0.3)

        box = SurroundingRectangle(msg1, color=HIGHLIGHT_COLOR,
                                    buff=0.25, corner_radius=0.1)

        cta = MathTex(
            r"\text{@mesonjetorja}",
            font_size=32, color=STEP_TITLE_COLOR,
        )
        cta.move_to(DOWN * 2.0)

        self.play(
            GrowFromCenter(msg1), run_time=0.6,
        )
        self.play(Create(box), run_time=0.4)
        self.play(
            msg1.animate.scale(1.1),
            rate_func=there_and_back, run_time=0.5,
        )
        self.play(FadeIn(msg_g, shift=UP * 0.3), run_time=0.6)
        self.wait(0.5)
        self.play(FadeIn(cta, shift=UP * 0.2), run_time=0.4)
        self.play(
            Circumscribe(VGroup(msg1, box), color=HIGHLIGHT_COLOR, run_time=0.8),
        )
        self.wait(2.5)
