"""
Vertical Reel — Reflection + Translation (Exercise 8a)
======================================================

9:16 vertical (1080×1920), ~50 seconds.
Hook: "Can two transformations become one?"
Shows reflection across y=x-1 then translation by (-4,4).
Reveals: equivalent to reflection across y=-x+4.

Render:
    cd scripts && manim -qh reels/transformations_reel_a.py TransformationsReelA
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
config.frame_height = 8 * (1920 / 1080)  # ≈ 14.22

SAFE_TOP = 4.8
SAFE_BOTTOM = -3.3
SAFE_LEFT = -3.0
SAFE_RIGHT = 3.0
SAFE_CENTER_X = 0.0
SAFE_CENTER_Y = (SAFE_TOP + SAFE_BOTTOM) / 2  # ≈ 0.75

# Colors
ORIG_COLOR = SHAPE_COLOR
REFL_COLOR = AUX_COLOR
TRANS_COLOR = ANSWER_COLOR
LINE_COLOR = LABEL_COLOR
EQUIV_COLOR = HIGHLIGHT_COLOR


def reflect(px, py):
    """Reflect across y = x - 1: x' = y+1, y' = x-1."""
    return (py + 1, px - 1)


class TransformationsReelA(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        MathTex.set_default(tex_template=ALBANIAN_TEX)
        Tex.set_default(tex_template=ALBANIAN_TEX)

        self.hook()
        self.show_triangle_and_reflect()
        self.show_translation()
        self.reveal_equivalent()
        self.punchline()

    # ── HOOK (0-4s) ──
    def hook(self):
        q = MathTex(r"?", font_size=200, color=LABEL_COLOR)
        q.move_to(UP * 3.5)

        hook1 = MathTex(
            r"\text{2 shndërrime}",
            font_size=48, color=WHITE,
        )
        hook2 = MathTex(
            r"\text{= 1 shndërrim?}",
            font_size=48, color=ANSWER_COLOR,
        )
        hook_g = VGroup(hook1, hook2).arrange(DOWN, buff=0.35)
        hook_g.move_to(UP * 0.3)

        sub = MathTex(
            r"\text{Simetri + Zhvendosje}",
            font_size=30, color=BODY_TEXT_COLOR,
        )
        sub.next_to(hook_g, DOWN, buff=0.6)

        self.play(
            GrowFromCenter(q),
            FadeIn(hook_g, shift=UP * 0.5),
            FadeIn(sub, shift=UP * 0.3),
            run_time=0.8,
        )
        self.play(q.animate.scale(1.15), rate_func=there_and_back, run_time=0.5)
        self.wait(1.2)
        self.play(FadeOut(q), FadeOut(hook_g), FadeOut(sub), run_time=0.4)

    # ── SHOW TRIANGLE + REFLECT (4-18s) ──
    def show_triangle_and_reflect(self):
        # Axes
        axes = Axes(
            x_range=[-2, 7, 1], y_range=[-2, 7, 1],
            x_length=5.5, y_length=5.5,
            axis_config={
                "include_tip": True, "include_numbers": True,
                "font_size": 14, "color": DIVIDER_COLOR,
            },
        )
        axes.move_to(UP * 1.8)
        ax_labels = axes.get_axis_labels(
            x_label=MathTex("x", font_size=16),
            y_label=MathTex("y", font_size=16),
        )

        # Reflection line y = x - 1
        ref_line = axes.plot(lambda x: x - 1, x_range=[-1.5, 6.5],
                             color=LINE_COLOR, stroke_width=2)
        ref_lbl = MathTex(r"y = x - 1", font_size=20, color=LINE_COLOR)
        ref_lbl.next_to(axes.c2p(6, 5), UR, buff=0.1)

        # Original triangle
        A, B, C = (2, 2), (3, 2), (2, 4)
        tri_orig = Polygon(
            axes.c2p(*A), axes.c2p(*B), axes.c2p(*C),
            color=ORIG_COLOR, fill_color=ORIG_COLOR,
            fill_opacity=0.25, stroke_width=2.5,
        )
        labels_orig = VGroup(
            MathTex("A", font_size=18, color=ORIG_COLOR).next_to(axes.c2p(*A), DL, buff=0.1),
            MathTex("B", font_size=18, color=ORIG_COLOR).next_to(axes.c2p(*B), DR, buff=0.1),
            MathTex("C", font_size=18, color=ORIG_COLOR).next_to(axes.c2p(*C), UL, buff=0.1),
        )

        # Reflected triangle
        A1, B1, C1 = reflect(*A), reflect(*B), reflect(*C)
        tri_refl = Polygon(
            axes.c2p(*A1), axes.c2p(*B1), axes.c2p(*C1),
            color=REFL_COLOR, fill_color=REFL_COLOR,
            fill_opacity=0.25, stroke_width=2.5,
        )
        labels_refl = VGroup(
            MathTex("A_1", font_size=18, color=REFL_COLOR).next_to(axes.c2p(*A1), DR, buff=0.1),
            MathTex("B_1", font_size=18, color=REFL_COLOR).next_to(axes.c2p(*B1), UR, buff=0.1),
            MathTex("C_1", font_size=18, color=REFL_COLOR).next_to(axes.c2p(*C1), DR, buff=0.1),
        )

        # Perpendicular connectors
        perps = VGroup(*[
            DashedLine(axes.c2p(*o), axes.c2p(*r),
                       color=DIVIDER_COLOR, dash_length=0.05, stroke_width=1.5)
            for o, r in zip([A, B, C], [A1, B1, C1])
        ])

        # Step label
        step1 = MathTex(
            r"\text{Hapi 1: Simetri sipas } y = x - 1",
            font_size=28, color=STEP_TITLE_COLOR,
        )
        step1.move_to(DOWN * 2.0)

        # Rule
        rule = MathTex(
            r"x' = y + 1, \quad y' = x - 1",
            font_size=28, color=WHITE,
        )
        rule.next_to(step1, DOWN, buff=0.35)

        # Results
        results = VGroup(
            MathTex(r"A(2,2) \to A_1(3,1)", font_size=24, color=REFL_COLOR),
            MathTex(r"B(3,2) \to B_1(3,2)", font_size=24, color=REFL_COLOR),
            MathTex(r"C(2,4) \to C_1(5,1)", font_size=24, color=REFL_COLOR),
        ).arrange(DOWN, buff=0.15)
        results.next_to(rule, DOWN, buff=0.35)

        # Animate
        self.play(Create(axes), FadeIn(ax_labels), run_time=0.8)
        self.play(Create(ref_line), FadeIn(ref_lbl), run_time=0.6)
        self.play(DrawBorderThenFill(tri_orig), run_time=0.8)
        self.play(FadeIn(labels_orig), run_time=0.4)
        self.wait(0.5)

        self.play(FadeIn(step1), run_time=0.4)
        self.play(Write(rule), run_time=0.6)
        self.wait(0.5)

        # Reflect animation
        self.play(Create(perps), run_time=0.8)
        self.play(DrawBorderThenFill(tri_refl), FadeIn(labels_refl), run_time=0.8)
        self.play(
            LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in results],
                         lag_ratio=0.15),
            run_time=0.8,
        )
        self.wait(1.5)

        # Store and clean up calc text
        self.axes = axes
        self.ax_labels = ax_labels
        self.ref_line = ref_line
        self.ref_lbl = ref_lbl
        self.tri_orig = tri_orig
        self.labels_orig = labels_orig
        self.tri_refl = tri_refl
        self.labels_refl = labels_refl

        self.play(
            FadeOut(perps), FadeOut(step1), FadeOut(rule), FadeOut(results),
            run_time=0.4,
        )

    # ── SHOW TRANSLATION (18-30s) ──
    def show_translation(self):
        axes = self.axes

        A1, B1, C1 = (3, 1), (3, 2), (5, 1)
        A2, B2, C2 = (-1, 5), (-1, 6), (1, 5)

        tri_trans = Polygon(
            axes.c2p(*A2), axes.c2p(*B2), axes.c2p(*C2),
            color=TRANS_COLOR, fill_color=TRANS_COLOR,
            fill_opacity=0.25, stroke_width=2.5,
        )
        labels_trans = VGroup(
            MathTex("A_2", font_size=18, color=TRANS_COLOR).next_to(axes.c2p(*A2), DL, buff=0.1),
            MathTex("B_2", font_size=18, color=TRANS_COLOR).next_to(axes.c2p(*B2), UL, buff=0.1),
            MathTex("C_2", font_size=18, color=TRANS_COLOR).next_to(axes.c2p(*C2), DR, buff=0.1),
        )

        # Translation arrows
        arrows = VGroup(*[
            Arrow(axes.c2p(*f), axes.c2p(*t),
                  color=TRANS_COLOR, stroke_width=2, tip_length=0.12, buff=0)
            for f, t in zip([A1, B1, C1], [A2, B2, C2])
        ])

        step2 = MathTex(
            r"\text{Hapi 2: Zhvendosje me } \vec{a} = \begin{pmatrix} -4 \\ 4 \end{pmatrix}",
            font_size=26, color=STEP_TITLE_COLOR,
        )
        step2.move_to(DOWN * 2.0)

        results = VGroup(
            MathTex(r"A_1(3,1) \to A_2(-1,5)", font_size=24, color=TRANS_COLOR),
            MathTex(r"B_1(3,2) \to B_2(-1,6)", font_size=24, color=TRANS_COLOR),
            MathTex(r"C_1(5,1) \to C_2(1,5)", font_size=24, color=TRANS_COLOR),
        ).arrange(DOWN, buff=0.15)
        results.next_to(step2, DOWN, buff=0.35)

        self.play(FadeIn(step2), run_time=0.4)
        self.play(
            LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15),
            run_time=0.8,
        )
        self.play(DrawBorderThenFill(tri_trans), FadeIn(labels_trans), run_time=0.8)
        self.play(
            LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in results],
                         lag_ratio=0.15),
            run_time=0.8,
        )
        self.wait(1.5)

        # Dim middle triangle
        self.play(
            self.tri_refl.animate.set_opacity(0.1),
            self.labels_refl.animate.set_opacity(0.2),
            FadeOut(arrows), FadeOut(step2), FadeOut(results),
            run_time=0.4,
        )

        self.tri_trans = tri_trans
        self.labels_trans = labels_trans

    # ── REVEAL EQUIVALENT (30-45s) ──
    def reveal_equivalent(self):
        axes = self.axes

        # Fade graph elements
        graph = VGroup(
            self.axes, self.ax_labels, self.ref_line, self.ref_lbl,
            self.tri_orig, self.labels_orig, self.tri_refl, self.labels_refl,
            self.tri_trans, self.labels_trans,
        )
        self.play(FadeOut(graph), run_time=0.5)

        # New clean axes showing just original → final
        axes2 = Axes(
            x_range=[-3, 7, 1], y_range=[-2, 8, 1],
            x_length=5.5, y_length=5.5,
            axis_config={
                "include_tip": True, "include_numbers": True,
                "font_size": 14, "color": DIVIDER_COLOR,
            },
        )
        axes2.move_to(UP * 1.8)
        ax2_l = axes2.get_axis_labels(
            x_label=MathTex("x", font_size=16),
            y_label=MathTex("y", font_size=16),
        )

        A, B, C = (2, 2), (3, 2), (2, 4)
        A2, B2, C2 = (-1, 5), (-1, 6), (1, 5)

        tri_o = Polygon(
            axes2.c2p(*A), axes2.c2p(*B), axes2.c2p(*C),
            color=ORIG_COLOR, fill_color=ORIG_COLOR,
            fill_opacity=0.25, stroke_width=2.5,
        )
        lbl_o = VGroup(
            MathTex("A", font_size=18, color=ORIG_COLOR).next_to(axes2.c2p(*A), DL, buff=0.1),
            MathTex("B", font_size=18, color=ORIG_COLOR).next_to(axes2.c2p(*B), DR, buff=0.1),
            MathTex("C", font_size=18, color=ORIG_COLOR).next_to(axes2.c2p(*C), UL, buff=0.1),
        )

        tri_f = Polygon(
            axes2.c2p(*A2), axes2.c2p(*B2), axes2.c2p(*C2),
            color=TRANS_COLOR, fill_color=TRANS_COLOR,
            fill_opacity=0.25, stroke_width=2.5,
        )
        lbl_f = VGroup(
            MathTex("A_2", font_size=18, color=TRANS_COLOR).next_to(axes2.c2p(*A2), DL, buff=0.1),
            MathTex("B_2", font_size=18, color=TRANS_COLOR).next_to(axes2.c2p(*B2), UL, buff=0.1),
            MathTex("C_2", font_size=18, color=TRANS_COLOR).next_to(axes2.c2p(*C2), DR, buff=0.1),
        )

        # Equivalent line y = -x + 4
        eq_line = axes2.plot(lambda x: -x + 4, x_range=[-2, 6.5],
                             color=EQUIV_COLOR, stroke_width=2.5)
        eq_lbl = MathTex(r"y = -x + 4", font_size=22, color=EQUIV_COLOR)
        eq_lbl.next_to(axes2.c2p(-1, 5), UL, buff=0.15)

        # Connectors through the equivalent line
        eq_perps = VGroup(*[
            DashedLine(axes2.c2p(*o), axes2.c2p(*f),
                       color=EQUIV_COLOR, dash_length=0.05, stroke_width=1.5)
            for o, f in zip([A, B, C], [A2, B2, C2])
        ])

        title = MathTex(
            r"\text{Shndërrimi ekuivalent:}",
            font_size=30, color=STEP_TITLE_COLOR,
        )
        title.move_to(DOWN * 2.0)

        self.play(Create(axes2), FadeIn(ax2_l), run_time=0.6)
        self.play(
            DrawBorderThenFill(tri_o), FadeIn(lbl_o),
            DrawBorderThenFill(tri_f), FadeIn(lbl_f),
            run_time=0.8,
        )
        self.wait(0.5)

        self.play(FadeIn(title), run_time=0.4)
        self.play(Create(eq_line), FadeIn(eq_lbl), run_time=0.8)
        self.play(Create(eq_perps), run_time=0.8)
        self.wait(1.5)

        self.graph2 = VGroup(axes2, ax2_l, tri_o, lbl_o, tri_f, lbl_f,
                             eq_line, eq_lbl, eq_perps, title)

    # ── PUNCHLINE (45-55s) ──
    def punchline(self):
        self.play(FadeOut(self.graph2), run_time=0.4)

        ans_label = MathTex(
            r"\text{Përgjigja:}",
            font_size=36, color=WHITE,
        )
        ans_label.move_to(UP * 2.5)

        ans_line1 = MathTex(
            r"\text{Simetri } y\!=\!x\!-\!1 \text{ + Zhvendosje } \begin{pmatrix} -4 \\ 4 \end{pmatrix}",
            font_size=28, color=BODY_TEXT_COLOR,
        )
        equals = MathTex(r"=", font_size=50, color=WHITE)
        ans_line2 = MathTex(
            r"\text{Simetri sipas } y = -x + 4",
            font_size=38, color=ANSWER_COLOR,
        )

        ans_g = VGroup(ans_line1, equals, ans_line2).arrange(DOWN, buff=0.5)
        ans_g.move_to(UP * 0.2)

        box = SurroundingRectangle(
            ans_line2, color=ANSWER_COLOR, buff=0.25, corner_radius=0.1,
        )

        cta = MathTex(
            r"\text{@mesonjetorja}",
            font_size=32, color=STEP_TITLE_COLOR,
        )
        cta.move_to(DOWN * 2.5)

        self.play(Write(ans_label), run_time=0.5)
        self.play(FadeIn(ans_line1, shift=UP * 0.3), run_time=0.6)
        self.play(Write(equals), run_time=0.3)
        self.play(
            GrowFromPoint(ans_line2, equals.get_center()),
            run_time=0.7,
        )
        self.play(Create(box), run_time=0.4)
        self.play(
            Flash(ans_line2.get_center(), color=ANSWER_COLOR,
                  line_length=0.2, num_lines=10, run_time=0.5),
        )
        self.wait(0.5)
        self.play(FadeIn(cta, shift=UP * 0.3), run_time=0.4)
        self.play(
            Circumscribe(VGroup(ans_line2, box), color=ANSWER_COLOR, run_time=0.8),
        )
        self.wait(2.0)
