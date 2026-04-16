"""
Reel G — Ushtrimi 2, Njësia 6.2A
Matematika 12 (Botime Pegi)

Vektori g) -2i  →  |v| = 2;  α = 180° (përgjatë boshtit negativ Ox, y = 0 ≥ 0)
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))

from manim import *
import numpy as np
from style_guide import (
    apply_style, make_answer_box, BG_COLOR,
    STEP_TITLE_COLOR, BODY_TEXT_COLOR, LABEL_COLOR,
    ANSWER_COLOR, SHAPE_COLOR, HIGHLIGHT_COLOR, DIVIDER_COLOR,
    ALBANIAN_TEX,
)

# ── Vertical 9:16 config ────────────────────
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 8
config.frame_height = 8 * (1920 / 1080)

SAFE_TOP = 4.8
SAFE_BOTTOM = -3.3

HOOK_SIZE = 42
EQ_SIZE = 36
ANSWER_SIZE = 42
BODY_SIZE = 30
SMALL_SIZE = 26


class ReelG(Scene):
    def construct(self):
        apply_style(self)
        MathTex.set_default(tex_template=ALBANIAN_TEX)
        Tex.set_default(tex_template=ALBANIAN_TEX)
        self.hook()
        self.solve()
        self.cta()

    # ────────────────────────────────────────────
    #  HOOK (0–8s)
    # ────────────────────────────────────────────

    def hook(self):
        # Vector expression
        vec_expr = MathTex(
            r"\vec{v} = -2\vec{i}",
            font_size=48, color=WHITE,
        )
        vec_expr.move_to(UP * 4.2)

        question = MathTex(
            r"\text{Gjej gjatësinë dhe këndin } \alpha",
            font_size=HOOK_SIZE, color=LABEL_COLOR,
        )
        question.move_to(UP * 3.0)

        self.play(FadeIn(vec_expr, shift=UP * 0.3), run_time=0.8)
        self.wait(0.8)
        self.play(FadeIn(question, shift=UP * 0.2), run_time=0.6)
        self.wait(0.8)

        # Compact diagram: vector along negative x-axis
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=4.5,
            y_length=2.5,
            tips=True,
            axis_config={
                "color": DIVIDER_COLOR,
                "stroke_width": 1.5,
                "include_ticks": False,
            },
        )
        axes.move_to(DOWN * 0.3)

        ax_lbl_x = MathTex("x", font_size=22, color=DIVIDER_COLOR)
        ax_lbl_x.next_to(axes.x_axis.get_end(), DR, buff=0.1)
        ax_lbl_y = MathTex("y", font_size=22, color=DIVIDER_COLOR)
        ax_lbl_y.next_to(axes.y_axis.get_end(), UL, buff=0.1)

        origin = axes.c2p(0, 0)
        tip_pt = axes.c2p(-2, 0)

        vec_arrow = Arrow(
            origin, tip_pt, buff=0,
            color=SHAPE_COLOR, stroke_width=3,
            max_tip_length_to_length_ratio=0.15,
        )

        # Component label below the arrow (no dashed lines — vector IS on the axis)
        x_lbl = MathTex("-2", font_size=22, color=LABEL_COLOR)
        x_lbl.next_to(vec_arrow, DOWN, buff=0.15)

        # Angle arc: full semicircle from 0 to PI (180°)
        arc = Arc(
            radius=0.45,
            start_angle=0,
            angle=PI,
            arc_center=origin,
            color=HIGHLIGHT_COLOR,
            stroke_width=2,
        )
        arc_lbl = MathTex(r"\alpha", font_size=22, color=HIGHLIGHT_COLOR)
        arc_lbl.move_to(
            np.array(origin) + 0.7 * np.array([np.cos(PI / 2), np.sin(PI / 2), 0])
        )

        self.play(Create(axes), FadeIn(ax_lbl_x), FadeIn(ax_lbl_y), run_time=0.6)
        self.play(GrowArrow(vec_arrow), run_time=0.7)
        self.play(FadeIn(x_lbl), run_time=0.3)
        self.play(Create(arc), FadeIn(arc_lbl), run_time=0.5)
        self.wait(2.5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # ────────────────────────────────────────────
    #  SOLVE (8–40s)
    # ────────────────────────────────────────────

    def solve(self):
        title = MathTex(
            r"\text{Zgjidhje}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        title.move_to(UP * SAFE_TOP)
        self.play(FadeIn(title), run_time=0.3)

        # ── Magnitude ──
        mag_title = MathTex(
            r"\text{Gjatësia:}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        mag_title.move_to(UP * 3.8)
        self.play(FadeIn(mag_title, shift=UP * 0.15), run_time=0.4)

        eq1 = MathTex(
            r"|\vec{v}| = \sqrt{(-2)^2 + 0^2}",
            font_size=EQ_SIZE, color=WHITE,
        )
        eq1.move_to(UP * 2.8)
        self.play(Write(eq1), run_time=0.8)
        self.wait(0.8)

        eq2 = MathTex(
            r"= \sqrt{4 + 0} = \sqrt{4}",
            font_size=EQ_SIZE, color=WHITE,
        )
        eq2.move_to(UP * 1.8)
        self.play(Write(eq2), run_time=0.7)
        self.wait(0.6)

        eq3 = MathTex(
            r"|\vec{v}| = 2",
            font_size=EQ_SIZE, color=ANSWER_COLOR,
        )
        eq3.move_to(UP * 0.9)
        self.play(Write(eq3), run_time=0.7)
        self.wait(1.0)

        # ── Angle ──
        ang_title = MathTex(
            r"\text{Këndi } \alpha\text{:}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        ang_title.move_to(UP * 0.0)
        self.play(FadeIn(ang_title, shift=UP * 0.15), run_time=0.4)

        # y = 0 >= 0, so positive formula
        sign_note = MathTex(
            r"\text{Meqë } y = 0 \geq 0\text{:}",
            font_size=SMALL_SIZE, color=BODY_TEXT_COLOR,
        )
        sign_note.move_to(DOWN * 0.7)
        self.play(FadeIn(sign_note, shift=UP * 0.15), run_time=0.4)
        self.wait(0.4)

        cos_eq = MathTex(
            r"\alpha = \cos^{-1}\!\Big(\frac{-2}{2}\Big)",
            font_size=EQ_SIZE, color=WHITE,
        )
        cos_eq.move_to(DOWN * 1.6)
        self.play(Write(cos_eq), run_time=0.8)
        self.wait(0.6)

        cos_eq2 = MathTex(
            r"= \cos^{-1}(-1)",
            font_size=EQ_SIZE, color=WHITE,
        )
        cos_eq2.move_to(DOWN * 2.4)
        self.play(Write(cos_eq2), run_time=0.6)
        self.wait(0.6)

        angle_res = MathTex(
            r"\alpha = 180^\circ",
            font_size=EQ_SIZE, color=ANSWER_COLOR,
        )
        angle_res.move_to(DOWN * 3.2)
        self.play(Write(angle_res), run_time=0.7)
        self.wait(1.5)

        # ── Fade solve work, show final answers ──
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

        # Final answer display
        ans1 = MathTex(
            r"|\vec{v}| = 2",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        ans1.move_to(UP * 1.5)

        ans2 = MathTex(
            r"\alpha = 180^\circ",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        ans2.move_to(UP * 0.2)

        self.play(Write(ans1), run_time=0.6)
        self.play(Write(ans2), run_time=0.6)
        self.wait(0.5)

        box = make_answer_box(VGroup(ans1, ans2))
        self.play(Create(box), run_time=0.4)
        self.play(
            Flash(
                VGroup(ans1, ans2).get_center(), color=ANSWER_COLOR,
                line_length=0.25, num_lines=12, run_time=0.6,
            ),
        )
        self.play(
            Circumscribe(
                VGroup(ans1, ans2, box), color=HIGHLIGHT_COLOR, run_time=0.8,
            ),
        )
        self.wait(2.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # ────────────────────────────────────────────
    #  CTA
    # ────────────────────────────────────────────

    def cta(self):
        handle = MathTex(r"\text{mesonjetorja.com}", font_size=BODY_SIZE, color=WHITE)
        handle.move_to(UP * 0.5)
        tagline = MathTex(
            r"\text{Më shumë ushtrime në faqen tonë!}",
            font_size=SMALL_SIZE, color=BODY_TEXT_COLOR,
        )
        tagline.next_to(handle, DOWN, buff=0.4)
        self.play(GrowFromCenter(handle), FadeIn(tagline, shift=UP * 0.3), run_time=0.8)
        self.wait(1.5)
