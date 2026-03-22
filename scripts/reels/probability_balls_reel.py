"""
Vertical Reel / TikTok — Probability with Colored Balls
========================================================

9:16 vertical format (1080×1920), under 60 seconds.
Fast-paced, hook-first, no voiceover.

Render:
    cd scripts && manim -pqh reels/probability_balls_reel.py ProbabilityBallsReel

Or for lower quality preview:
    cd scripts && manim -pql reels/probability_balls_reel.py ProbabilityBallsReel
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

# ──────────────────────────────────────────────────────────
#  SAFE ZONE CONSTANTS — Instagram / TikTok UI overlays
# ──────────────────────────────────────────────────────────
#
#  Frame: x ∈ [-4, 4], y ∈ [-7.11, 7.11]
#
#  Keep content away from ALL edges — platform UI overlaps
#  on bottom (captions), right (social buttons), top (status).
#  Use equal margins on left/right to keep content CENTERED.
#
SAFE_TOP = 4.8
SAFE_BOTTOM = -3.3
SAFE_LEFT = -3.0
SAFE_RIGHT = 3.0
SAFE_CENTER_X = 0.0   # Truly centered
SAFE_CENTER_Y = (SAFE_TOP + SAFE_BOTTOM) / 2  # ≈ 0.75

# ── Ball definitions ──
BALL_COLORS = {
    "red": RED, "white": WHITE, "black": "#555555",
    "purple": PURPLE, "blue": BLUE, "brown": "#8B4513",
    "green": GREEN, "yellow": YELLOW,
}
BALL_STROKE = {
    "red": RED_D, "white": GRAY, "black": WHITE,
    "purple": PURPLE_D, "blue": BLUE_D, "brown": "#5C2D0A",
    "green": GREEN_D, "yellow": YELLOW_D,
}


def make_ball(color_name, radius=0.22):
    return Circle(
        radius=radius,
        fill_opacity=1,
        fill_color=BALL_COLORS[color_name],
        stroke_color=BALL_STROKE[color_name],
        stroke_width=1.5,
    )


class ProbabilityBallsReel(Scene):
    """
    ~45 second vertical reel:
    1. HOOK (0-3s): "Sa mundësi ke?" + mystery bag
    2. REVEAL (3-12s): Balls appear in bag
    3. SOLVE Part A (12-25s): P(i kuq) = 15/22
    4. SOLVE Part B (25-38s): P(jo i kuq) = 7/22
    5. PUNCHLINE (38-50s): Comparison + CTA
    """

    def construct(self):
        self.camera.background_color = BG_COLOR
        MathTex.set_default(tex_template=ALBANIAN_TEX)
        Tex.set_default(tex_template=ALBANIAN_TEX)

        self.hook()
        self.reveal_balls()
        self.solve_red()
        self.solve_not_red()
        self.punchline()

    # ================================================================
    #  PHASE 1 — HOOK (first 3 seconds)
    # ================================================================

    def hook(self):
        # Big question mark — grabs attention immediately
        q_mark = MathTex(r"?", font_size=180, color=LABEL_COLOR)
        q_mark.move_to(UP * 3.5)

        hook_text = MathTex(
            r"\text{Sa mundësi ke të nxjerrësh}",
            font_size=40, color=WHITE,
        )
        hook_text2 = MathTex(
            r"\text{topin e kuq?}",
            font_size=48, color=RED,
        )
        hook_group = VGroup(hook_text, hook_text2).arrange(DOWN, buff=0.35)
        hook_group.move_to(UP * 0.5)

        # Mystery bag silhouette — positioned in safe zone
        bag = RoundedRectangle(
            corner_radius=0.4, width=4.0, height=3.0,
            fill_color="#2A2A2A", fill_opacity=0.6,
            stroke_color=DIVIDER_COLOR, stroke_width=2,
        )
        bag.move_to(DOWN * 2.5)

        # Fast dramatic entrance
        self.play(
            GrowFromCenter(q_mark),
            FadeIn(hook_group, shift=UP * 0.5),
            DrawBorderThenFill(bag),
            run_time=1.0,
        )
        self.play(
            q_mark.animate.scale(1.2),
            rate_func=there_and_back,
            run_time=0.6,
        )
        self.wait(0.8)

        # Store bag ref, fade hook text
        self.bag = bag
        self.play(
            FadeOut(q_mark),
            FadeOut(hook_group),
            run_time=0.4,
        )

    # ================================================================
    #  PHASE 2 — REVEAL BALLS (show what's in the bag)
    # ================================================================

    def reveal_balls(self):
        bag = self.bag

        # ── Build red balls: 5×3 grid ──
        r = 0.20
        gap = 0.50
        red_balls = VGroup()
        for row in range(3):
            for col in range(5):
                b = make_ball("red", radius=r)
                b.move_to(np.array([col * gap, -row * gap, 0]))
                red_balls.add(b)
        red_balls.move_to(ORIGIN)

        # ── Other 7 balls in a row ──
        other_names = ["white", "black", "purple", "blue", "brown", "green", "yellow"]
        other_balls = VGroup()
        for i, name in enumerate(other_names):
            b = make_ball(name, radius=r)
            b.move_to(np.array([i * gap, 0, 0]))
            other_balls.add(b)
        other_balls.move_to(ORIGIN)
        other_balls.next_to(red_balls, DOWN, buff=0.65)

        # Labels — proper Albanian
        red_label = MathTex(r"15", font_size=34, color=RED)
        red_label.next_to(red_balls, UP, buff=0.3)
        red_word = MathTex(r"\text{të kuqe}", font_size=24, color=RED)
        red_word.next_to(red_label, RIGHT, buff=0.15)

        other_label = MathTex(r"7", font_size=34, color=BODY_TEXT_COLOR)
        other_label.next_to(other_balls, DOWN, buff=0.3)
        other_word = MathTex(r"\text{të tjera}", font_size=24, color=BODY_TEXT_COLOR)
        other_word.next_to(other_label, RIGHT, buff=0.15)

        # Position everything centered in safe zone
        all_balls = VGroup(
            red_balls, red_label, red_word,
            other_balls, other_label, other_word,
        )
        all_balls.move_to(
            np.array([0, SAFE_CENTER_Y - 0.5, 0])
        )

        # Resize bag to fit
        bag.generate_target()
        bag.target.surround(all_balls, buff=0.55)

        # Reveal red balls with ShowIncreasingSubsets (counting effect)
        self.play(MoveToTarget(bag), run_time=0.5)
        self.play(
            ShowIncreasingSubsets(red_balls),
            run_time=1.5,
        )
        self.play(
            FadeIn(red_label, shift=DOWN * 0.2),
            FadeIn(red_word, shift=DOWN * 0.2),
            run_time=0.4,
        )

        # Reveal other balls
        self.play(
            LaggedStartMap(GrowFromCenter, other_balls, lag_ratio=0.12),
            run_time=1.0,
        )
        self.play(
            FadeIn(other_label, shift=UP * 0.2),
            FadeIn(other_word, shift=UP * 0.2),
            run_time=0.4,
        )

        # Total counter — below bag, within safe zone
        total_text = MathTex(
            r"\text{Totali} = 15 + 7 = 22",
            font_size=38, color=LABEL_COLOR,
        )
        total_text.next_to(bag, DOWN, buff=0.5)
        # Clamp into safe zone
        if total_text.get_bottom()[1] < SAFE_BOTTOM:
            total_text.set_y(SAFE_BOTTOM + 0.3)
        self.play(Write(total_text), run_time=0.8)
        self.play(
            Circumscribe(total_text, color=LABEL_COLOR, run_time=0.6),
        )
        self.wait(0.8)

        # Store references
        self.red_balls = red_balls
        self.other_balls = other_balls
        self.all_balls_group = VGroup(all_balls, bag, total_text)
        self.total_text = total_text
        self.red_label = red_label
        self.red_word = red_word
        self.other_label = other_label
        self.other_word = other_word

    # ================================================================
    #  PHASE 3 — SOLVE: P(i kuq) = 15/22
    # ================================================================

    def solve_red(self):
        # Shift balls to upper safe zone
        bag_target_y = SAFE_TOP - 2.0
        current_y = self.all_balls_group.get_center()[1]
        shift_amount = bag_target_y - current_y
        self.play(
            self.all_balls_group.animate.shift(UP * shift_amount),
            run_time=0.6,
        )

        # Dim non-red balls
        dim_anims = [b.animate.set_opacity(0.2) for b in self.other_balls]
        dim_anims.append(self.other_label.animate.set_opacity(0.2))
        dim_anims.append(self.other_word.animate.set_opacity(0.2))
        self.play(*dim_anims, run_time=0.4)

        # Pulse red balls
        self.play(
            LaggedStartMap(
                Indicate, self.red_balls,
                lag_ratio=0.02, color=ANSWER_COLOR,
                rate_func=there_and_back,
            ),
            run_time=0.8,
        )

        # Question — centered in safe zone
        calc_y = SAFE_CENTER_Y - 1.0
        q = MathTex(
            r"\text{Sa mundësi ka topi të jetë i kuq?}",
            font_size=32, color=STEP_TITLE_COLOR,
        )
        q.move_to(np.array([SAFE_CENTER_X, calc_y, 0]))
        self.play(FadeIn(q, shift=UP * 0.3), run_time=0.5)
        self.wait(0.6)

        # Formula
        formula = MathTex(
            r"P(\text{i kuq}) = \frac{\text{të kuqe}}{\text{totali}}",
            font_size=36, color=WHITE,
        )
        formula.next_to(q, DOWN, buff=0.5)
        formula.set_x(SAFE_CENTER_X)
        self.play(Write(formula), run_time=0.7)
        self.wait(0.5)

        # Substitute — answer
        answer = MathTex(
            r"P(\text{i kuq}) = \frac{15}{22}",
            font_size=44, color=ANSWER_COLOR,
        )
        answer.next_to(formula, DOWN, buff=0.55)
        answer.set_x(SAFE_CENTER_X)
        self.play(
            GrowFromPoint(answer, formula.get_center()),
            run_time=0.7,
        )

        # Highlight box
        box = SurroundingRectangle(
            answer, color=ANSWER_COLOR, buff=0.2, corner_radius=0.08,
        )
        self.play(Create(box), run_time=0.4)
        self.play(
            Flash(answer.get_center(), color=ANSWER_COLOR,
                  line_length=0.2, num_lines=10, run_time=0.5),
        )
        self.wait(1.0)

        # Fraction bar — narrower to stay in safe zone
        bar_width = 3.5
        bar_bg = RoundedRectangle(
            width=bar_width, height=0.35, corner_radius=0.1,
            fill_color=GRAY, fill_opacity=0.2,
            stroke_color=DIVIDER_COLOR, stroke_width=1,
        )
        bar_fill = RoundedRectangle(
            width=bar_width * (15 / 22), height=0.35, corner_radius=0.1,
            fill_color=RED, fill_opacity=0.8,
            stroke_width=0,
        )
        bar_group_anchor = answer.get_bottom() + DOWN * 0.6
        bar_bg.move_to(np.array([SAFE_CENTER_X, bar_group_anchor[1], 0]))
        bar_fill.move_to(bar_bg, aligned_edge=LEFT)

        pct = MathTex(r"\approx 68\%", font_size=28, color=RED)
        pct.next_to(bar_bg, DOWN, buff=0.2)

        self.play(FadeIn(bar_bg), run_time=0.3)
        bar_fill_target = bar_fill.copy()
        bar_fill.stretch(0, 0, about_edge=LEFT)
        self.play(
            bar_fill.animate.become(bar_fill_target),
            FadeIn(pct, shift=UP * 0.15),
            run_time=0.8,
        )
        self.wait(1.0)

        # Clean up for next part
        self.play(
            FadeOut(q), FadeOut(formula),
            FadeOut(answer), FadeOut(box),
            FadeOut(bar_bg), FadeOut(bar_fill), FadeOut(pct),
            run_time=0.4,
        )

        # Restore opacity
        restore_anims = [b.animate.set_opacity(1.0) for b in self.other_balls]
        restore_anims.append(self.other_label.animate.set_opacity(1.0))
        restore_anims.append(self.other_word.animate.set_opacity(1.0))
        self.play(*restore_anims, run_time=0.3)

    # ================================================================
    #  PHASE 4 — SOLVE: P(jo i kuq) = 7/22
    # ================================================================

    def solve_not_red(self):
        # Dim red balls this time
        dim_anims = [b.animate.set_opacity(0.2) for b in self.red_balls]
        dim_anims.append(self.red_label.animate.set_opacity(0.2))
        dim_anims.append(self.red_word.animate.set_opacity(0.2))
        self.play(*dim_anims, run_time=0.4)

        # Highlight others
        self.play(
            LaggedStartMap(
                Indicate, self.other_balls,
                lag_ratio=0.08, color=SHAPE_COLOR,
                rate_func=there_and_back,
            ),
            run_time=0.8,
        )

        # Question — in safe zone
        calc_y = SAFE_CENTER_Y - 1.0
        q = MathTex(
            r"\text{Po nëse NUK është i kuq?}",
            font_size=34, color=STEP_TITLE_COLOR,
        )
        q.move_to(np.array([SAFE_CENTER_X, calc_y, 0]))
        self.play(FadeIn(q, shift=UP * 0.3), run_time=0.5)
        self.wait(0.5)

        # Quick calc
        calc = MathTex(
            r"\text{Jo të kuqe} = 22 - 15 = 7",
            font_size=32, color=WHITE,
        )
        calc.next_to(q, DOWN, buff=0.45)
        calc.set_x(SAFE_CENTER_X)
        self.play(Write(calc), run_time=0.6)
        self.wait(0.4)

        # Answer
        answer = MathTex(
            r"P(\text{jo i kuq}) = \frac{7}{22}",
            font_size=44, color=SHAPE_COLOR,
        )
        answer.next_to(calc, DOWN, buff=0.55)
        answer.set_x(SAFE_CENTER_X)
        self.play(
            GrowFromPoint(answer, calc.get_center()),
            run_time=0.7,
        )

        box = SurroundingRectangle(
            answer, color=SHAPE_COLOR, buff=0.2, corner_radius=0.08,
        )
        self.play(Create(box), run_time=0.4)
        self.play(
            Flash(answer.get_center(), color=SHAPE_COLOR,
                  line_length=0.2, num_lines=10, run_time=0.5),
        )
        self.wait(1.0)

        # Fraction bar
        bar_width = 3.5
        bar_bg = RoundedRectangle(
            width=bar_width, height=0.35, corner_radius=0.1,
            fill_color=GRAY, fill_opacity=0.2,
            stroke_color=DIVIDER_COLOR, stroke_width=1,
        )
        bar_fill = RoundedRectangle(
            width=bar_width * (7 / 22), height=0.35, corner_radius=0.1,
            fill_color=SHAPE_COLOR, fill_opacity=0.8,
            stroke_width=0,
        )
        bar_group_anchor = answer.get_bottom() + DOWN * 0.6
        bar_bg.move_to(np.array([SAFE_CENTER_X, bar_group_anchor[1], 0]))
        bar_fill.move_to(bar_bg, aligned_edge=LEFT)

        pct = MathTex(r"\approx 32\%", font_size=28, color=SHAPE_COLOR)
        pct.next_to(bar_bg, DOWN, buff=0.2)

        self.play(FadeIn(bar_bg), run_time=0.3)
        bar_fill_target = bar_fill.copy()
        bar_fill.stretch(0, 0, about_edge=LEFT)
        self.play(
            bar_fill.animate.become(bar_fill_target),
            FadeIn(pct, shift=UP * 0.15),
            run_time=0.8,
        )
        self.wait(1.0)

        # Store for punchline
        self.not_red_group = VGroup(q, calc, answer, box, bar_bg, bar_fill, pct)

    # ================================================================
    #  PHASE 5 — PUNCHLINE (stacked comparison)
    # ================================================================

    def punchline(self):
        # Fade everything
        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=0.5,
        )

        # Title — within safe top
        title = MathTex(
            r"\text{Përfundimi:}",
            font_size=42, color=WHITE,
        )
        title.move_to(np.array([SAFE_CENTER_X, SAFE_TOP - 0.5, 0]))

        # ── Red probability card ──
        red_ans = MathTex(
            r"P(\text{i kuq}) = \frac{15}{22}",
            font_size=40, color=RED,
        )
        red_pct = MathTex(r"\approx 68\%", font_size=30, color=RED)
        red_bar_bg = RoundedRectangle(
            width=3.2, height=0.3, corner_radius=0.08,
            fill_color=GRAY, fill_opacity=0.2,
            stroke_color=DIVIDER_COLOR, stroke_width=1,
        )
        red_bar_fill = RoundedRectangle(
            width=3.2 * (15 / 22), height=0.3, corner_radius=0.08,
            fill_color=RED, fill_opacity=0.8, stroke_width=0,
        )
        red_bar = VGroup(red_bar_bg, red_bar_fill)
        red_bar_fill.move_to(red_bar_bg, aligned_edge=LEFT)
        red_card = VGroup(red_ans, red_pct, red_bar).arrange(DOWN, buff=0.3)

        # ── Not-red probability card ──
        nr_ans = MathTex(
            r"P(\text{jo i kuq}) = \frac{7}{22}",
            font_size=40, color=SHAPE_COLOR,
        )
        nr_pct = MathTex(r"\approx 32\%", font_size=30, color=SHAPE_COLOR)
        nr_bar_bg = RoundedRectangle(
            width=3.2, height=0.3, corner_radius=0.08,
            fill_color=GRAY, fill_opacity=0.2,
            stroke_color=DIVIDER_COLOR, stroke_width=1,
        )
        nr_bar_fill = RoundedRectangle(
            width=3.2 * (7 / 22), height=0.3, corner_radius=0.08,
            fill_color=SHAPE_COLOR, fill_opacity=0.8, stroke_width=0,
        )
        nr_bar = VGroup(nr_bar_bg, nr_bar_fill)
        nr_bar_fill.move_to(nr_bar_bg, aligned_edge=LEFT)
        nr_card = VGroup(nr_ans, nr_pct, nr_bar).arrange(DOWN, buff=0.3)

        # Stack cards vertically with good spacing
        comparison = VGroup(red_card, nr_card).arrange(DOWN, buff=1.2)
        comparison.move_to(np.array([SAFE_CENTER_X, SAFE_CENTER_Y - 0.3, 0]))

        # CTA — above the danger zone at bottom
        cta = MathTex(
            r"\text{@mesonjetorja}",
            font_size=34, color=STEP_TITLE_COLOR,
        )
        cta.move_to(np.array([SAFE_CENTER_X, SAFE_BOTTOM + 0.5, 0]))

        more = MathTex(
            r"\text{Më shumë ushtrime në faqen tonë!}",
            font_size=26, color=BODY_TEXT_COLOR,
        )
        more.next_to(cta, UP, buff=0.3)

        # Animate
        self.play(Write(title), run_time=0.6)
        self.play(
            FadeIn(red_card, shift=UP * 0.4),
            run_time=0.7,
        )
        self.wait(0.4)
        self.play(
            FadeIn(nr_card, shift=UP * 0.4),
            run_time=0.7,
        )
        self.wait(0.4)

        # Animate bars filling
        red_bar_fill_target = red_bar_fill.copy()
        red_bar_fill.stretch(0, 0, about_edge=LEFT)
        nr_bar_fill_target = nr_bar_fill.copy()
        nr_bar_fill.stretch(0, 0, about_edge=LEFT)
        self.play(
            red_bar_fill.animate.become(red_bar_fill_target),
            nr_bar_fill.animate.become(nr_bar_fill_target),
            run_time=1.0,
        )

        # CTA
        self.play(
            FadeIn(more, shift=UP * 0.3),
            FadeIn(cta, shift=UP * 0.3),
            run_time=0.6,
        )

        # Final celebrate pulse
        self.play(
            Circumscribe(
                comparison,
                color=LABEL_COLOR, run_time=1.0,
            ),
        )
        self.wait(2.0)
