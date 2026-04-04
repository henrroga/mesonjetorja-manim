"""
Reel C — Ushtrimi 3, Njësia 8.3A
"Sa mundësi ka që ndryshesa e dy zareve të jetë numër i thjeshtë?"

Standalone reel: re-establishes context (two dice, difference),
identifies which differences are prime, counts them, finds P(prime) = 4/9.
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
ANSWER_SIZE = 44
BODY_SIZE = 32
SMALL_SIZE = 28
TABLE_SIZE = 20

# ── Difference table ─────────────────────────
DIFF = [[abs(i - j) for j in range(1, 7)] for i in range(1, 7)]
PRIMES = {2, 3, 5}


class ReelC(Scene):
    def construct(self):
        apply_style(self)
        MathTex.set_default(tex_template=ALBANIAN_TEX)
        Tex.set_default(tex_template=ALBANIAN_TEX)

        self.hook()
        self.identify_primes()
        self.count_and_solve()
        self.cta()

    # ────────────────────────────────────────────
    #  HOOK (0–10s)
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
            r"\text{Sa mundësi ka që ndryshesa}",
            font_size=HOOK_SIZE, color=WHITE,
        )
        line4 = MathTex(
            r"\text{të jetë numër i thjeshtë?}",
            font_size=QUESTION_SIZE, color=HIGHLIGHT_COLOR,
        )
        q = VGroup(line1, line2, line3, line4).arrange(DOWN, buff=0.35)
        q.move_to(UP * 1.5)

        self.play(FadeIn(q, shift=UP * 0.4), run_time=1.2)
        self.wait(3.5)  # let them read the full question
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # ────────────────────────────────────────────
    #  IDENTIFY PRIMES in {0,1,2,3,4,5} (10–22s)
    # ────────────────────────────────────────────

    def identify_primes(self):
        title = MathTex(
            r"\text{Rezultatet e mundshme:}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        title.move_to(UP * SAFE_TOP)
        self.play(FadeIn(title), run_time=0.4)

        set_eq = MathTex(
            r"A = \{0,\, 1,\, 2,\, 3,\, 4,\, 5\}",
            font_size=EQ_SIZE, color=WHITE,
        )
        set_eq.next_to(title, DOWN, buff=0.5)
        self.play(Write(set_eq), run_time=0.8)
        self.wait(1.0)

        # Ask: which are prime?
        ask = MathTex(
            r"\text{Cilat janë numra të thjeshtë?}",
            font_size=BODY_SIZE, color=HIGHLIGHT_COLOR,
        )
        ask.next_to(set_eq, DOWN, buff=0.5)
        self.play(FadeIn(ask), run_time=0.5)
        self.wait(1.0)

        # Check each one
        checks = [
            (r"0", r"\text{jo}", DIVIDER_COLOR),
            (r"1", r"\text{jo}", DIVIDER_COLOR),
            (r"2", r"\checkmark \text{ thjeshtë}", ANSWER_COLOR),
            (r"3", r"\checkmark \text{ thjeshtë}", ANSWER_COLOR),
            (r"4 = 2 \times 2", r"\text{jo}", DIVIDER_COLOR),
            (r"5", r"\checkmark \text{ thjeshtë}", ANSWER_COLOR),
        ]

        check_group = VGroup()
        for num, verdict, color in checks:
            row = MathTex(
                num + r" \;\to\; " + verdict,
                font_size=SMALL_SIZE, color=color,
            )
            check_group.add(row)

        check_group.arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        check_group.next_to(ask, DOWN, buff=0.4)
        check_group.set_x(-0.3)

        self.play(
            LaggedStartMap(FadeIn, check_group, lag_ratio=0.2),
            run_time=2.0,
        )
        self.wait(2.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # ────────────────────────────────────────────
    #  COUNT & SOLVE (22–42s)
    # ────────────────────────────────────────────

    def count_and_solve(self):
        # Show the difference table so this reel is fully standalone
        table_title = MathTex(
            r"\text{Numërojmë në tabelën e ndryshesave:}",
            font_size=SMALL_SIZE, color=STEP_TITLE_COLOR,
        )
        table_title.move_to(UP * SAFE_TOP)
        self.play(FadeIn(table_title), run_time=0.4)

        cell_w, cell_h = 0.58, 0.42
        table_cells = VGroup()
        val_cells = {}

        # Corner
        corner = MathTex(r"|i{-}j|", font_size=14, color=DIVIDER_COLOR)
        corner.move_to(ORIGIN)
        table_cells.add(corner)

        # Headers
        for c in range(6):
            h = MathTex(str(c + 1), font_size=TABLE_SIZE, color=SHAPE_COLOR)
            h.move_to(RIGHT * (c + 1) * cell_w)
            table_cells.add(h)
        for r in range(6):
            h = MathTex(str(r + 1), font_size=TABLE_SIZE, color=AUX_COLOR)
            h.move_to(DOWN * (r + 1) * cell_h)
            table_cells.add(h)

        # Values
        for r in range(6):
            for c in range(6):
                val = DIFF[r][c]
                txt = MathTex(str(val), font_size=TABLE_SIZE, color=WHITE)
                txt.move_to(RIGHT * (c + 1) * cell_w + DOWN * (r + 1) * cell_h)
                table_cells.add(txt)
                val_cells[(r, c)] = txt

        table_cells.move_to(UP * 1.8)
        self.play(FadeIn(table_cells), run_time=0.8)
        self.wait(0.8)

        # Highlight prime-valued cells (2, 3, 5)
        prime_rects = VGroup()
        for r in range(6):
            for c in range(6):
                if DIFF[r][c] in PRIMES:
                    rect = SurroundingRectangle(
                        val_cells[(r, c)], color=ANSWER_COLOR,
                        buff=0.03, stroke_width=1.5,
                    )
                    prime_rects.add(rect)

        self.play(LaggedStartMap(Create, prime_rects, lag_ratio=0.03), run_time=0.8)
        self.wait(1.0)

        # Count for each prime value — below the table
        count_2 = MathTex(
            r"\text{Ndryshesa } 2 \;\to\; 8 \text{ herë}",
            font_size=BODY_SIZE, color=ANSWER_COLOR,
        )
        count_3 = MathTex(
            r"\text{Ndryshesa } 3 \;\to\; 6 \text{ herë}",
            font_size=BODY_SIZE, color=ANSWER_COLOR,
        )
        count_5 = MathTex(
            r"\text{Ndryshesa } 5 \;\to\; 2 \text{ herë}",
            font_size=BODY_SIZE, color=ANSWER_COLOR,
        )
        counts = VGroup(count_2, count_3, count_5).arrange(DOWN, buff=0.25)
        counts.next_to(table_cells, DOWN, buff=0.4)
        counts.set_x(0)

        self.play(
            LaggedStartMap(FadeIn, counts, lag_ratio=0.25),
            run_time=1.2,
        )
        self.wait(1.5)

        # Clear table to make room for final calc
        self.play(
            FadeOut(table_cells), FadeOut(prime_rects), FadeOut(table_title),
            run_time=0.4,
        )

        # Sum
        sum_line = MathTex(
            r"\text{Gjithsej: } 8 + 6 + 2 = 16",
            font_size=EQ_SIZE, color=WHITE,
        )
        sum_line.next_to(counts, DOWN, buff=0.5)
        self.play(Write(sum_line), run_time=0.8)
        self.wait(1.0)

        # Formula
        formula = MathTex(
            r"P(\text{thjeshtë}) = \dfrac{16}{36}",
            font_size=EQ_SIZE, color=WHITE,
        )
        formula.next_to(sum_line, DOWN, buff=0.5)
        self.play(Write(formula), run_time=0.8)
        self.wait(0.8)

        # Final answer
        answer = MathTex(
            r"= \dfrac{4}{9}",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        answer.next_to(formula, DOWN, buff=0.4)
        box = make_answer_box(answer)

        self.play(Write(answer), run_time=0.8)
        self.play(Create(box), run_time=0.4)
        self.play(Circumscribe(VGroup(answer, box), color=HIGHLIGHT_COLOR, run_time=0.8))
        self.play(
            Flash(answer.get_center(), color=ANSWER_COLOR,
                  line_length=0.2, num_lines=12, run_time=0.5),
        )
        self.wait(2.0)

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
