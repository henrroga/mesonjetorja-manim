"""
Reel B — Ushtrimi 3, Njësia 8.3A
"Sa është P(0), P(3), dhe P(6) kur ndryshesa e dy zareve?"

Standalone reel: re-establishes context (two dice, difference),
then calculates three probabilities with clear visuals.
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
HOOK_SIZE = 38
QUESTION_SIZE = 42
EQ_SIZE = 38
ANSWER_SIZE = 42
BODY_SIZE = 32
SMALL_SIZE = 28
TABLE_SIZE = 20

# ── Difference table ─────────────────────────
DIFF = [[abs(i - j) for j in range(1, 7)] for i in range(1, 7)]


class ReelB(Scene):
    def construct(self):
        apply_style(self)
        MathTex.set_default(tex_template=ALBANIAN_TEX)
        Tex.set_default(tex_template=ALBANIAN_TEX)

        self.hook()
        self.context_table()
        self.prob_zero()
        self.prob_three()
        self.prob_six()
        self.cta()

    # ────────────────────────────────────────────
    #  HOOK (0–8s)
    # ────────────────────────────────────────────

    def hook(self):
        line1 = MathTex(
            r"\text{Hidhen dy zare të rregullta.}",
            font_size=HOOK_SIZE, color=WHITE,
        )
        line2 = MathTex(
            r"\text{Ndryshesa e pikëve: } |i - j|",
            font_size=HOOK_SIZE, color=WHITE,
        )
        line3 = MathTex(
            r"\text{Gjeni } P(0),\; P(3),\; P(6)",
            font_size=QUESTION_SIZE, color=LABEL_COLOR,
        )
        q = VGroup(line1, line2, line3).arrange(DOWN, buff=0.4)
        q.move_to(UP * 2.0)

        self.play(FadeIn(q, shift=UP * 0.4), run_time=1.2)
        self.wait(3.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # ────────────────────────────────────────────
    #  QUICK CONTEXT TABLE (8–14s)
    # ────────────────────────────────────────────

    def context_table(self):
        """Show a compact version of the difference table as a reminder."""
        title = MathTex(
            r"\text{Tabela e ndryshesave (36 rezultate)}",
            font_size=SMALL_SIZE, color=STEP_TITLE_COLOR,
        )
        title.move_to(UP * SAFE_TOP)

        cell_w, cell_h = 0.62, 0.46
        cells = VGroup()
        self.val_cells = {}

        # Corner
        corner = MathTex(r"|i{-}j|", font_size=16, color=DIVIDER_COLOR)
        corner.move_to(ORIGIN)
        cells.add(corner)

        # Headers
        for c in range(6):
            h = MathTex(str(c + 1), font_size=TABLE_SIZE, color=SHAPE_COLOR)
            h.move_to(RIGHT * (c + 1) * cell_w)
            cells.add(h)
        for r in range(6):
            h = MathTex(str(r + 1), font_size=TABLE_SIZE, color=AUX_COLOR)
            h.move_to(DOWN * (r + 1) * cell_h)
            cells.add(h)

        # Values
        for r in range(6):
            for c in range(6):
                val = DIFF[r][c]
                txt = MathTex(str(val), font_size=TABLE_SIZE, color=WHITE)
                txt.move_to(RIGHT * (c + 1) * cell_w + DOWN * (r + 1) * cell_h)
                cells.add(txt)
                self.val_cells[(r, c)] = txt

        cells.move_to(UP * 1.5)
        self.table = cells

        self.play(FadeIn(title), run_time=0.3)
        self.play(FadeIn(cells), run_time=0.8)
        self.wait(1.5)

        self.table_title = title

    # ────────────────────────────────────────────
    #  P(0) — highlight diagonal (14–22s)
    # ────────────────────────────────────────────

    def prob_zero(self):
        # Highlight zeros on the diagonal
        zero_cells = [self.val_cells[(i, i)] for i in range(6)]
        rects = VGroup(*[
            SurroundingRectangle(c, color=LABEL_COLOR, buff=0.04, stroke_width=2)
            for c in zero_cells
        ])
        self.play(LaggedStartMap(Create, rects, lag_ratio=0.1), run_time=0.6)

        # Count label
        count = MathTex(
            r"0 \text{ paraqitet } 6 \text{ herë}",
            font_size=BODY_SIZE, color=LABEL_COLOR,
        )
        count.next_to(self.table, DOWN, buff=0.4)
        self.play(FadeIn(count, shift=UP * 0.2), run_time=0.5)

        # Probability
        prob = MathTex(
            r"P(0) = \dfrac{6}{36} = \dfrac{1}{6}",
            font_size=EQ_SIZE, color=ANSWER_COLOR,
        )
        prob.next_to(count, DOWN, buff=0.4)
        box = make_answer_box(prob)

        self.play(Write(prob), run_time=0.8)
        self.play(Create(box), run_time=0.3)
        self.wait(1.5)

        # Clean up highlights
        self.play(
            FadeOut(rects), FadeOut(count), FadeOut(prob), FadeOut(box),
            run_time=0.4,
        )

    # ────────────────────────────────────────────
    #  P(3) — highlight 3s (22–30s)
    # ────────────────────────────────────────────

    def prob_three(self):
        # Find all cells with value 3
        three_cells = [
            self.val_cells[(r, c)]
            for r in range(6) for c in range(6)
            if DIFF[r][c] == 3
        ]
        rects = VGroup(*[
            SurroundingRectangle(c, color=SHAPE_COLOR, buff=0.04, stroke_width=2)
            for c in three_cells
        ])
        self.play(LaggedStartMap(Create, rects, lag_ratio=0.08), run_time=0.5)

        count = MathTex(
            r"3 \text{ paraqitet } 6 \text{ herë}",
            font_size=BODY_SIZE, color=SHAPE_COLOR,
        )
        count.next_to(self.table, DOWN, buff=0.4)
        self.play(FadeIn(count, shift=UP * 0.2), run_time=0.5)

        prob = MathTex(
            r"P(3) = \dfrac{6}{36} = \dfrac{1}{6}",
            font_size=EQ_SIZE, color=ANSWER_COLOR,
        )
        prob.next_to(count, DOWN, buff=0.4)
        box = make_answer_box(prob)

        self.play(Write(prob), run_time=0.8)
        self.play(Create(box), run_time=0.3)
        self.wait(1.5)

        self.play(
            FadeOut(rects), FadeOut(count), FadeOut(prob), FadeOut(box),
            run_time=0.4,
        )

    # ────────────────────────────────────────────
    #  P(6) = 0 — nothing to highlight (30–40s)
    # ────────────────────────────────────────────

    def prob_six(self):
        # Dim the whole table briefly
        self.play(self.table.animate.set_opacity(0.3), run_time=0.4)

        explain1 = MathTex(
            r"\text{A ka ndryshesë 6?}",
            font_size=BODY_SIZE, color=AUX_COLOR,
        )
        explain1.next_to(self.table, DOWN, buff=0.4)
        self.play(FadeIn(explain1), run_time=0.5)
        self.wait(1.0)

        explain2 = MathTex(
            r"\text{Ndryshesa max: } |1 - 6| = 5",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        explain2.next_to(explain1, DOWN, buff=0.3)
        self.play(FadeIn(explain2), run_time=0.5)
        self.wait(1.0)

        explain3 = MathTex(
            r"\text{Nuk ka asnjë çift me ndryshesë 6!}",
            font_size=BODY_SIZE, color=AUX_COLOR,
        )
        explain3.next_to(explain2, DOWN, buff=0.3)
        self.play(FadeIn(explain3), run_time=0.5)
        self.wait(0.8)

        prob = MathTex(
            r"P(6) = 0",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        prob.next_to(explain3, DOWN, buff=0.5)
        box = make_answer_box(prob)

        self.play(Write(prob), run_time=0.7)
        self.play(Create(box), run_time=0.3)
        self.play(
            Flash(prob.get_center(), color=AUX_COLOR,
                  line_length=0.15, num_lines=8, run_time=0.5),
        )
        self.wait(1.5)

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
