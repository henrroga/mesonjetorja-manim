"""
Reel A — Ushtrimi 3, Njësia 8.3A
"Cila është tabela e ndryshesave kur hidhen dy zare?"

Standalone reel: builds the difference table, shows all 36 outcomes,
reveals the set of possible results {0, 1, 2, 3, 4, 5}.
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
TABLE_SIZE = 24

# ── Difference table ─────────────────────────
DIFF = [[abs(i - j) for j in range(1, 7)] for i in range(1, 7)]


class ReelA(Scene):
    def construct(self):
        apply_style(self)
        MathTex.set_default(tex_template=ALBANIAN_TEX)
        Tex.set_default(tex_template=ALBANIAN_TEX)

        self.hook()
        self.build_table()
        self.reveal_set()
        self.cta()

    # ────────────────────────────────────────────
    #  HOOK — state the problem clearly (0–10s)
    # ────────────────────────────────────────────

    def hook(self):
        line1 = MathTex(
            r"\text{Hidhen dy zare të rregullta.}",
            font_size=HOOK_SIZE, color=WHITE,
        )
        line2 = MathTex(
            r"\text{Mbahet shënim ndryshesa}",
            font_size=HOOK_SIZE, color=WHITE,
        )
        line3 = MathTex(
            r"\text{e pikëve: } |i - j|",
            font_size=HOOK_SIZE, color=LABEL_COLOR,
        )
        question = VGroup(line1, line2, line3).arrange(DOWN, buff=0.35)
        question.move_to(UP * 3.0)

        ask = MathTex(
            r"\text{Si duket tabela e rezultateve?}",
            font_size=QUESTION_SIZE, color=HIGHLIGHT_COLOR,
        )
        ask.next_to(question, DOWN, buff=0.7)

        self.play(FadeIn(question, shift=UP * 0.4), run_time=1.2)
        self.wait(2.5)  # let them read
        self.play(FadeIn(ask, shift=UP * 0.3), run_time=0.8)
        self.wait(2.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # ────────────────────────────────────────────
    #  BUILD TABLE (10–28s)
    # ────────────────────────────────────────────

    def build_table(self):
        title = MathTex(
            r"\text{Tabela: ndryshesa } |i - j|",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        title.move_to(UP * SAFE_TOP)
        self.play(FadeIn(title), run_time=0.5)

        cell_w, cell_h = 0.72, 0.56
        self.value_mobjects = {}

        # Build headers and values as SEPARATE groups to avoid double-animation
        header_group = VGroup()
        value_group = VGroup()

        # Corner cell
        corner = MathTex(r"|i{-}j|", font_size=18, color=DIVIDER_COLOR)
        corner.move_to(ORIGIN)
        header_group.add(corner)

        # Column headers (j = 1..6)
        for c in range(6):
            h = MathTex(str(c + 1), font_size=TABLE_SIZE, color=SHAPE_COLOR)
            h.move_to(RIGHT * (c + 1) * cell_w)
            header_group.add(h)

        # Row headers + values
        for r in range(6):
            rh = MathTex(str(r + 1), font_size=TABLE_SIZE, color=AUX_COLOR)
            rh.move_to(DOWN * (r + 1) * cell_h)
            header_group.add(rh)

            for c in range(6):
                val = DIFF[r][c]
                txt = MathTex(str(val), font_size=TABLE_SIZE, color=WHITE)
                txt.move_to(RIGHT * (c + 1) * cell_w + DOWN * (r + 1) * cell_h)
                value_group.add(txt)
                self.value_mobjects[(r, c)] = txt

        all_cells = VGroup(header_group, value_group)
        all_cells.move_to(UP * 0.8)
        self.table_group = all_cells

        # Animate headers first, then values row by row
        self.play(
            LaggedStartMap(FadeIn, header_group, lag_ratio=0.05),
            run_time=0.8,
        )

        for r in range(6):
            row = VGroup(*[self.value_mobjects[(r, c)] for c in range(6)])
            self.play(
                LaggedStartMap(FadeIn, row, lag_ratio=0.06),
                run_time=0.4,
            )

        self.wait(1.0)

        # Show total count
        total = MathTex(
            r"6 \times 6 = 36 \text{ rezultate gjithsej}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        total.next_to(all_cells, DOWN, buff=0.5)
        self.play(FadeIn(total, shift=UP * 0.2), run_time=0.6)
        self.wait(1.5)

        self.total_label = total
        self.title_label = title

    # ────────────────────────────────────────────
    #  REVEAL THE SET (28–42s)
    # ────────────────────────────────────────────

    def reveal_set(self):
        # Highlight unique values by color-coding them
        colors_by_val = {
            0: LABEL_COLOR,
            1: WHITE,
            2: SHAPE_COLOR,
            3: HIGHLIGHT_COLOR,
            4: AUX_COLOR,
            5: "#FF69B4",  # pink for variety
        }

        # Flash each unique value
        for val in range(6):
            cells = [
                self.value_mobjects[(r, c)]
                for r in range(6) for c in range(6)
                if DIFF[r][c] == val
            ]
            self.play(
                *[cell.animate.set_color(colors_by_val[val]) for cell in cells],
                run_time=0.3,
            )

        self.wait(1.0)

        # Clear and show the set
        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=0.4,
        )

        result_title = MathTex(
            r"\text{Bashkësia e rezultateve:}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        result_title.move_to(UP * 2.5)

        set_eq = MathTex(
            r"A = \{0,\, 1,\, 2,\, 3,\, 4,\, 5\}",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        set_eq.next_to(result_title, DOWN, buff=0.8)

        box = make_answer_box(set_eq)

        self.play(FadeIn(result_title), run_time=0.5)
        self.play(Write(set_eq), run_time=0.9)
        self.play(Create(box), run_time=0.4)
        self.play(
            Flash(set_eq.get_center(), color=ANSWER_COLOR,
                  line_length=0.2, num_lines=10, run_time=0.5),
        )

        note = MathTex(
            r"\text{Ndryshesa max: } |1-6| = 5",
            font_size=SMALL_SIZE, color=BODY_TEXT_COLOR,
        )
        note.next_to(box, DOWN, buff=0.6)
        self.play(FadeIn(note), run_time=0.5)
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
