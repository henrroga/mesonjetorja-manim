"""
Reel C — Ushtrimi 2, Njësia 6.2A
Matematika 12 (Botime Pegi)

Vektori c) -5j  →  |v| = 5;  α = -90°
Axis-aligned vector (downward). No right triangle needed.
Standalone vertical reel: hook diagram, solve magnitude + angle, boxed answer + CTA.
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

# ── Safe zone ────────────────────────────────
SAFE_TOP = 4.8
SAFE_BOTTOM = -3.3

# ── Font sizes ───────────────────────────────
HOOK_SIZE = 42
EQ_SIZE = 36
ANSWER_SIZE = 42
BODY_SIZE = 30
SMALL_SIZE = 26


class ReelC(Scene):
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
            r"\vec{v} = -5\vec{j}",
            font_size=HOOK_SIZE, color=WHITE,
        )
        vec_expr.move_to(UP * SAFE_TOP)

        # Question
        question = MathTex(
            r"\text{Gjej gjatësinë dhe këndin } \alpha",
            font_size=BODY_SIZE, color=LABEL_COLOR,
        )
        question.next_to(vec_expr, DOWN, buff=0.4)

        # ── Mini diagram ──
        axes = Axes(
            x_range=[-3, 3, 1], y_range=[-6, 2, 1],
            x_length=3.5, y_length=4.5,
            tips=True,
            axis_config={"color": DIVIDER_COLOR, "stroke_width": 1.5,
                         "include_numbers": False},
        )
        axes.move_to(UP * 0.0)

        ax_lbl_x = MathTex("x", font_size=22, color=DIVIDER_COLOR)
        ax_lbl_x.next_to(axes.x_axis.get_end(), DR, buff=0.1)
        ax_lbl_y = MathTex("y", font_size=22, color=DIVIDER_COLOR)
        ax_lbl_y.next_to(axes.y_axis.get_end(), UL, buff=0.1)

        origin = axes.c2p(0, 0)
        tip_pt = axes.c2p(0, -5)

        vec_arrow = Arrow(
            origin, tip_pt, buff=0,
            color=SHAPE_COLOR, stroke_width=3,
            max_tip_length_to_length_ratio=0.12,
        )

        # Value label alongside the arrow
        val_lbl = MathTex("-5", font_size=22, color=LABEL_COLOR)
        val_lbl.next_to(vec_arrow, RIGHT, buff=0.15)

        # Angle arc (clockwise from +x axis to -y, i.e. -90°)
        arc = Arc(
            radius=0.55, start_angle=0, angle=-PI / 2,
            arc_center=origin, color=HIGHLIGHT_COLOR, stroke_width=2,
        )
        alpha_lbl = MathTex(r"\alpha", font_size=22, color=HIGHLIGHT_COLOR)
        alpha_lbl.move_to(origin + 0.85 * np.array([np.cos(-PI / 4), np.sin(-PI / 4), 0]))

        # Animate hook
        self.play(Write(vec_expr), run_time=0.7)
        self.play(FadeIn(question, shift=UP * 0.2), run_time=0.5)
        self.wait(0.5)
        self.play(Create(axes), FadeIn(ax_lbl_x), FadeIn(ax_lbl_y), run_time=0.6)
        self.play(GrowArrow(vec_arrow), run_time=0.6)
        self.play(FadeIn(val_lbl), run_time=0.3)
        self.play(Create(arc), FadeIn(alpha_lbl), run_time=0.4)
        self.wait(2.5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # ────────────────────────────────────────────
    #  SOLVE (8–35s)
    # ────────────────────────────────────────────

    def solve(self):
        # ── Title ──
        title = MathTex(
            r"\text{Zgjidhje}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        title.move_to(UP * SAFE_TOP)
        self.play(FadeIn(title), run_time=0.3)

        # ── Magnitude ──
        mag_title = MathTex(
            r"\text{Gjatësia:}",
            font_size=SMALL_SIZE, color=STEP_TITLE_COLOR,
        )
        mag_title.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(mag_title, shift=UP * 0.15), run_time=0.4)

        eq1 = MathTex(
            r"|\vec{v}| = \sqrt{0^2 + (-5)^2}",
            font_size=EQ_SIZE, color=WHITE,
        )
        eq1.next_to(mag_title, DOWN, buff=0.4)
        self.play(Write(eq1), run_time=0.8)
        self.wait(0.8)

        eq2 = MathTex(
            r"= \sqrt{0 + 25} = \sqrt{25}",
            font_size=EQ_SIZE, color=WHITE,
        )
        eq2.next_to(eq1, DOWN, buff=0.35)
        self.play(Write(eq2), run_time=0.8)
        self.wait(0.8)

        eq3 = MathTex(
            r"|\vec{v}| = 5",
            font_size=EQ_SIZE, color=ANSWER_COLOR,
        )
        eq3.next_to(eq2, DOWN, buff=0.35)
        self.play(Write(eq3), run_time=0.7)
        self.wait(1.0)

        # ── Angle ──
        ang_title = MathTex(
            r"\text{Këndi } \alpha\text{:}",
            font_size=SMALL_SIZE, color=STEP_TITLE_COLOR,
        )
        ang_title.next_to(eq3, DOWN, buff=0.5)
        self.play(FadeIn(ang_title, shift=UP * 0.15), run_time=0.4)

        # Note about negative y
        sign_note = MathTex(
            r"\text{Meqë } y < 0\text{, këndi negativ:}",
            font_size=SMALL_SIZE, color=HIGHLIGHT_COLOR,
        )
        sign_note.next_to(ang_title, DOWN, buff=0.3)
        self.play(FadeIn(sign_note, shift=UP * 0.15), run_time=0.4)
        self.wait(0.6)

        cos_eq = MathTex(
            r"\alpha = -\cos^{-1}\!\Big(\frac{0}{5}\Big)",
            font_size=EQ_SIZE, color=WHITE,
        )
        cos_eq.next_to(sign_note, DOWN, buff=0.4)
        self.play(Write(cos_eq), run_time=0.8)
        self.wait(0.8)

        angle_res = MathTex(
            r"\alpha = -90^\circ",
            font_size=EQ_SIZE, color=ANSWER_COLOR,
        )
        angle_res.next_to(cos_eq, DOWN, buff=0.35)
        self.play(Write(angle_res), run_time=0.7)
        self.wait(1.0)

        # ── Boxed answer ──
        self.play(
            *[FadeOut(m) for m in [
                title, mag_title, eq1, eq2, ang_title, sign_note, cos_eq,
            ]],
            run_time=0.4,
        )

        # Reposition answers
        ans_mag = eq3
        ans_ang = angle_res
        target = VGroup(ans_mag.copy(), ans_ang.copy()).arrange(DOWN, buff=0.35)
        target.move_to(UP * 1.0)

        self.play(
            ans_mag.animate.move_to(target[0]),
            ans_ang.animate.move_to(target[1]),
            run_time=0.5,
        )

        box = make_answer_box(VGroup(ans_mag, ans_ang))
        self.play(Create(box), run_time=0.4)
        self.play(
            Flash(VGroup(ans_mag, ans_ang).get_center(), color=ANSWER_COLOR,
                  line_length=0.25, num_lines=12, run_time=0.6),
        )
        self.play(
            Circumscribe(VGroup(ans_mag, ans_ang, box),
                         color=HIGHLIGHT_COLOR, run_time=0.8),
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
