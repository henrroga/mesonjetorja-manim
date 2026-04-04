"""
YouTube Video — Ushtrimi 3, Njësia 8.3A
Matematika 10-11: Pjesa II

Dy zare të rregullta hidhen dhe mbahet shënim ndryshesa e pikëve.
a) Ndërtoni tabelën e hapësirës së rezultateve.
b) Bashkësia e rezultateve të mundshme.
c) P(0), P(3), P(6), P(numër i thjeshtë)

NOT using ExerciseScene because the table must persist across all parts.
ExerciseScene calls fade_all() between parts which would destroy it.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))

from manim import *
import numpy as np
from style_guide import (
    apply_style, make_answer_box,
    BG_COLOR, STEP_TITLE_COLOR, BODY_TEXT_COLOR, LABEL_COLOR,
    ANSWER_COLOR, SHAPE_COLOR, AUX_COLOR, HIGHLIGHT_COLOR, DIVIDER_COLOR,
    TITLE_SIZE, SUBTITLE_SIZE, PART_HEADER_SIZE, STEP_TITLE_SIZE,
    BODY_SIZE, CALC_SIZE, ANSWER_SIZE,
    T_TITLE_WRITE, T_SUBTITLE_FADE, T_STEP_TITLE,
    T_BODY_FADE, T_KEY_EQUATION, T_ROUTINE_EQUATION, T_SHAPE_CREATE,
    T_LAYOUT_SHIFT, T_TRANSITION,
    W_AFTER_KEY, W_AFTER_ROUTINE, W_AFTER_ANSWER,
    ALBANIAN_TEX,
)

# ── Data ─────────────────────────────────────
DIFF = [[abs(i - j) for j in range(1, 7)] for i in range(1, 7)]
PRIMES = {2, 3, 5}

# Right-panel x center
PX = 3.2


class Ushtrimi3(Scene):
    def construct(self):
        apply_style(self)
        MathTex.set_default(tex_template=ALBANIAN_TEX)
        Tex.set_default(tex_template=ALBANIAN_TEX)

        self.title_screen()
        self.part_a()
        self.part_b()
        self.part_c_i()
        self.part_c_ii()
        self.part_c_iii()
        self.part_c_iv()
        self.final_summary()
        self.end_screen()

    # ────────────────────────────────────────────
    #  TITLE SCREEN
    # ────────────────────────────────────────────

    def title_screen(self):
        title = MathTex(
            r"\text{Ushtrimi 3 — Njësia 8.3A}",
            font_size=TITLE_SIZE, color=WHITE,
        )
        source = MathTex(
            r"\text{Matematika 10-11: Pjesa II}",
            font_size=SUBTITLE_SIZE, color=BODY_TEXT_COLOR,
        )
        source.next_to(title, DOWN, buff=0.4)

        self.play(Write(title), run_time=T_TITLE_WRITE)
        self.play(FadeIn(source, shift=UP * 0.2), run_time=T_SUBTITLE_FADE)
        self.wait(W_AFTER_KEY)
        self.play(FadeOut(title), FadeOut(source))
        self.wait(0.5)

    # ────────────────────────────────────────────
    #  PART A — Build the table (centered)
    # ────────────────────────────────────────────

    def part_a(self):
        header = MathTex(
            r"\text{Pjesa a)}",
            font_size=PART_HEADER_SIZE, color=LABEL_COLOR,
        )
        header.to_corner(UL, buff=0.4)
        self.play(Write(header), run_time=0.5)

        # Explain
        explain = VGroup(
            MathTex(r"\text{Hidhen dy zare të rregullta.}", font_size=BODY_SIZE, color=BODY_TEXT_COLOR),
            MathTex(r"\text{Shënojmë ndryshesën } |i - j|", font_size=BODY_SIZE, color=BODY_TEXT_COLOR),
            MathTex(r"\text{ku } i \text{ dhe } j \text{ janë pikët e zareve.}", font_size=BODY_SIZE, color=BODY_TEXT_COLOR),
        ).arrange(DOWN, buff=0.2).move_to(UP * 1.5)

        self.play(FadeIn(explain, shift=UP * 0.3), run_time=T_BODY_FADE)
        self.wait(W_AFTER_KEY)
        self.play(FadeOut(explain), FadeOut(header), run_time=T_TRANSITION)

        # Build MathTable
        table_data = [[str(DIFF[r][c]) for c in range(6)] for r in range(6)]
        row_labels = [MathTex(str(i + 1), font_size=22, color=AUX_COLOR) for i in range(6)]
        col_labels = [MathTex(str(j + 1), font_size=22, color=SHAPE_COLOR) for j in range(6)]
        top_left = MathTex(r"|i{-}j|", font_size=18, color=DIVIDER_COLOR)

        self.table = MathTable(
            table_data,
            row_labels=row_labels,
            col_labels=col_labels,
            top_left_entry=top_left,
            include_outer_lines=True,
            v_buff=0.25,
            h_buff=0.4,
            element_to_mobject_config={"font_size": 22},
            line_config={"stroke_width": 1, "color": DIVIDER_COLOR, "stroke_opacity": 0.5},
        )
        self.table.scale(0.85)
        self.table.move_to(ORIGIN)

        table_title = MathTex(
            r"\text{Hapësira e rezultateve — Ndryshesa } |i - j|",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        table_title.to_edge(UP, buff=0.5)

        row_label = MathTex(r"\text{Zari 1 } (i)", font_size=16, color=AUX_COLOR)
        row_label.next_to(self.table, LEFT, buff=0.3).rotate(PI / 2)

        col_label = MathTex(r"\text{Zari 2 } (j)", font_size=16, color=SHAPE_COLOR)
        col_label.next_to(self.table, UP, buff=0.2)

        self.play(FadeIn(table_title), run_time=T_STEP_TITLE)
        self.play(
            FadeIn(self.table), FadeIn(row_label), FadeIn(col_label),
            run_time=T_SHAPE_CREATE,
        )
        self.wait(W_AFTER_KEY)

        total = MathTex(
            r"\text{Gjithsej: } 6 \times 6 = 36 \text{ rezultate}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        total.next_to(self.table, DOWN, buff=0.4)
        self.play(FadeIn(total), run_time=T_BODY_FADE)
        self.wait(W_AFTER_KEY)

        # Store labels for cleanup when shifting
        self.table_labels = VGroup(table_title, row_label, col_label, total)

    # ────────────────────────────────────────────
    #  PART B — Show set of outcomes (table shifts left)
    # ────────────────────────────────────────────

    def part_b(self):
        # Fade out the axis labels and total — they won't fit when small
        self.play(FadeOut(self.table_labels), run_time=0.3)

        # Shift table to the left and scale down — it stays here for the rest
        self.play(
            self.table.animate.scale(0.8).move_to(LEFT * 3.5 + DOWN * 0.2),
            run_time=T_LAYOUT_SHIFT,
        )
        self.wait(0.3)

        header = MathTex(
            r"\text{Pjesa b)}",
            font_size=PART_HEADER_SIZE, color=LABEL_COLOR,
        )
        header.to_corner(UL, buff=0.4)
        self.play(Write(header), run_time=0.5)

        # Color-code unique values on the table
        colors_by_val = {
            0: LABEL_COLOR, 1: WHITE, 2: SHAPE_COLOR,
            3: HIGHLIGHT_COLOR, 4: AUX_COLOR, 5: "#FF69B4",
        }

        for val in range(6):
            entries = [
                self.table.get_entries((r + 2, c + 2))
                for r in range(6) for c in range(6)
                if DIFF[r][c] == val
            ]
            self.play(
                *[e.animate.set_color(colors_by_val[val]) for e in entries],
                run_time=0.25,
            )
        self.wait(0.8)

        # Show answer on the right
        explain = MathTex(
            r"\text{Vlerat e mundshme:}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        explain.move_to(RIGHT * PX + UP * 2.0)

        set_eq = MathTex(
            r"A = \{0, 1, 2, 3, 4, 5\}",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        set_eq.next_to(explain, DOWN, buff=0.5)
        set_eq.set_x(PX)
        box = make_answer_box(set_eq)

        self.play(FadeIn(explain), run_time=T_BODY_FADE)
        self.play(Write(set_eq), run_time=T_KEY_EQUATION)
        self.play(Create(box), run_time=0.4)
        self.wait(W_AFTER_ANSWER)

        # Clean right side + reset table colors
        all_entries = [
            self.table.get_entries((r + 2, c + 2))
            for r in range(6) for c in range(6)
        ]
        self.play(
            FadeOut(explain), FadeOut(set_eq), FadeOut(box), FadeOut(header),
            *[e.animate.set_color(WHITE) for e in all_entries],
            run_time=T_TRANSITION,
        )
        self.wait(0.3)

    # ────────────────────────────────────────────
    #  PART C — Probabilities (table stays left!)
    # ────────────────────────────────────────────

    def _clear_right(self, *mobjects):
        """Fade out right-panel mobjects and reset highlighted table cells."""
        self.play(
            *[FadeOut(m) for m in mobjects],
            run_time=T_TRANSITION,
        )

    def _reset_cells(self, target_val, highlights):
        """Reset highlighted cells back to white and remove rectangles."""
        entries = [
            self.table.get_entries((r + 2, c + 2))
            for r in range(6) for c in range(6)
            if DIFF[r][c] == target_val
        ]
        self.play(
            FadeOut(highlights),
            *[e.animate.set_color(WHITE) for e in entries],
            run_time=0.3,
        )

    def _highlight_cells(self, target_val, color):
        """Highlight all cells matching target_val, return (entries, rects)."""
        entries = []
        rects = VGroup()
        for r in range(6):
            for c in range(6):
                if DIFF[r][c] == target_val:
                    entry = self.table.get_entries((r + 2, c + 2))
                    entries.append(entry)
                    rect = SurroundingRectangle(
                        entry, color=color, buff=0.04, stroke_width=2,
                    )
                    rects.add(rect)

        self.play(
            *[e.animate.set_color(color) for e in entries],
            LaggedStartMap(Create, rects, lag_ratio=0.05),
            run_time=0.7,
        )
        return entries, rects

    def part_c_i(self):
        """P(0) = 6/36 = 1/6"""
        header = MathTex(r"\text{Pjesa c) — i}", font_size=PART_HEADER_SIZE, color=LABEL_COLOR)
        header.to_corner(UL, buff=0.4)
        self.play(Write(header), run_time=0.5)

        # Question
        q = MathTex(r"\text{Gjeni } P(\text{ndryshesa} = 0)", font_size=BODY_SIZE, color=WHITE)
        q.move_to(RIGHT * PX + UP * 2.5)
        self.play(FadeIn(q), run_time=T_STEP_TITLE)

        # Highlight zeros on table
        _, rects = self._highlight_cells(0, LABEL_COLOR)
        self.wait(0.5)

        # Explain
        why = MathTex(
            r"\text{Diagonalja: (1,1), (2,2), ..., (6,6)}",
            font_size=18, color=BODY_TEXT_COLOR,
        )
        why.next_to(q, DOWN, buff=0.3).set_x(PX)
        self.play(FadeIn(why), run_time=T_BODY_FADE)

        count = MathTex(r"6 \text{ herë nga } 36", font_size=CALC_SIZE, color=WHITE)
        count.next_to(why, DOWN, buff=0.35).set_x(PX)
        self.play(Write(count), run_time=T_ROUTINE_EQUATION)
        self.wait(0.5)

        # Answer
        ans = MathTex(
            r"P(0) = \dfrac{6}{36} = \dfrac{1}{6}",
            font_size=CALC_SIZE, color=ANSWER_COLOR,
        )
        ans.next_to(count, DOWN, buff=0.4).set_x(PX)
        box = make_answer_box(ans)
        self.play(Write(ans), run_time=T_KEY_EQUATION)
        self.play(Create(box), run_time=0.4)
        self.wait(W_AFTER_ANSWER)

        # Clean up
        self._reset_cells(0, rects)
        self._clear_right(q, why, count, ans, box, header)
        self.wait(0.3)

    def part_c_ii(self):
        """P(3) = 6/36 = 1/6"""
        header = MathTex(r"\text{Pjesa c) — ii}", font_size=PART_HEADER_SIZE, color=LABEL_COLOR)
        header.to_corner(UL, buff=0.4)
        self.play(Write(header), run_time=0.5)

        q = MathTex(r"\text{Gjeni } P(\text{ndryshesa} = 3)", font_size=BODY_SIZE, color=WHITE)
        q.move_to(RIGHT * PX + UP * 2.5)
        self.play(FadeIn(q), run_time=T_STEP_TITLE)

        _, rects = self._highlight_cells(3, SHAPE_COLOR)
        self.wait(0.5)

        why = MathTex(
            r"\text{(1,4), (4,1), (2,5), (5,2), (3,6), (6,3)}",
            font_size=18, color=BODY_TEXT_COLOR,
        )
        why.next_to(q, DOWN, buff=0.3).set_x(PX)
        self.play(FadeIn(why), run_time=T_BODY_FADE)

        count = MathTex(r"6 \text{ herë nga } 36", font_size=CALC_SIZE, color=WHITE)
        count.next_to(why, DOWN, buff=0.35).set_x(PX)
        self.play(Write(count), run_time=T_ROUTINE_EQUATION)
        self.wait(0.5)

        ans = MathTex(
            r"P(3) = \dfrac{6}{36} = \dfrac{1}{6}",
            font_size=CALC_SIZE, color=ANSWER_COLOR,
        )
        ans.next_to(count, DOWN, buff=0.4).set_x(PX)
        box = make_answer_box(ans)
        self.play(Write(ans), run_time=T_KEY_EQUATION)
        self.play(Create(box), run_time=0.4)
        self.wait(W_AFTER_ANSWER)

        self._reset_cells(3, rects)
        self._clear_right(q, why, count, ans, box, header)
        self.wait(0.3)

    def part_c_iii(self):
        """P(6) = 0"""
        header = MathTex(r"\text{Pjesa c) — iii}", font_size=PART_HEADER_SIZE, color=LABEL_COLOR)
        header.to_corner(UL, buff=0.4)
        self.play(Write(header), run_time=0.5)

        q = MathTex(r"\text{Gjeni } P(\text{ndryshesa} = 6)", font_size=BODY_SIZE, color=WHITE)
        q.move_to(RIGHT * PX + UP * 2.5)
        self.play(FadeIn(q), run_time=T_STEP_TITLE)
        self.wait(0.5)

        # Dim table — nothing matches
        self.play(self.table.animate.set_opacity(0.3), run_time=0.5)

        why = MathTex(
            r"\text{Ndryshesa max: } |1 - 6| = 5",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        why.next_to(q, DOWN, buff=0.4).set_x(PX)
        self.play(FadeIn(why), run_time=T_BODY_FADE)
        self.wait(W_AFTER_ROUTINE)

        why2 = MathTex(r"\text{Asnjë çift me ndryshesë 6!}", font_size=BODY_SIZE, color=AUX_COLOR)
        why2.next_to(why, DOWN, buff=0.3).set_x(PX)
        self.play(FadeIn(why2), run_time=T_BODY_FADE)
        self.wait(0.8)

        ans = MathTex(r"P(6) = 0", font_size=ANSWER_SIZE, color=ANSWER_COLOR)
        ans.next_to(why2, DOWN, buff=0.5).set_x(PX)
        box = make_answer_box(ans)
        self.play(Write(ans), run_time=T_KEY_EQUATION)
        self.play(Create(box), run_time=0.4)
        self.play(Flash(ans.get_center(), color=AUX_COLOR, line_length=0.15, num_lines=8, run_time=0.5))
        self.wait(W_AFTER_ANSWER)

        # Restore table
        self.play(
            self.table.animate.set_opacity(1.0),
            run_time=0.3,
        )
        self._clear_right(q, why, why2, ans, box, header)
        self.wait(0.3)

    def part_c_iv(self):
        """P(prime) = 16/36 = 4/9"""
        header = MathTex(r"\text{Pjesa c) — iv}", font_size=PART_HEADER_SIZE, color=LABEL_COLOR)
        header.to_corner(UL, buff=0.4)
        self.play(Write(header), run_time=0.5)

        q = MathTex(
            r"\text{Gjeni } P(\text{numër i thjeshtë})",
            font_size=BODY_SIZE, color=WHITE,
        )
        q.move_to(RIGHT * PX + UP * 2.8)
        self.play(FadeIn(q), run_time=T_STEP_TITLE)

        # Which are prime
        prime_info = MathTex(
            r"\text{Thjeshtë nga } \{0..5\}: \; 2, 3, 5",
            font_size=BODY_SIZE, color=ANSWER_COLOR,
        )
        prime_info.next_to(q, DOWN, buff=0.35).set_x(PX)
        self.play(FadeIn(prime_info), run_time=T_BODY_FADE)
        self.wait(W_AFTER_ROUTINE)

        # Highlight ALL prime cells
        prime_entries = []
        prime_rects = VGroup()
        for r in range(6):
            for c in range(6):
                if DIFF[r][c] in PRIMES:
                    entry = self.table.get_entries((r + 2, c + 2))
                    prime_entries.append(entry)
                    rect = SurroundingRectangle(
                        entry, color=HIGHLIGHT_COLOR, buff=0.03, stroke_width=1.5,
                    )
                    prime_rects.add(rect)

        self.play(
            *[e.animate.set_color(HIGHLIGHT_COLOR) for e in prime_entries],
            LaggedStartMap(Create, prime_rects, lag_ratio=0.02),
            run_time=1.0,
        )
        self.wait(W_AFTER_KEY)

        # Counts
        count_line = MathTex(
            r"2 \to 8, \;\; 3 \to 6, \;\; 5 \to 2",
            font_size=BODY_SIZE, color=WHITE,
        )
        count_line.next_to(prime_info, DOWN, buff=0.3).set_x(PX)
        self.play(Write(count_line), run_time=T_ROUTINE_EQUATION)
        self.wait(0.5)

        sum_line = MathTex(
            r"\text{Gjithsej: } 8 + 6 + 2 = 16",
            font_size=BODY_SIZE, color=WHITE,
        )
        sum_line.next_to(count_line, DOWN, buff=0.25).set_x(PX)
        self.play(Write(sum_line), run_time=T_ROUTINE_EQUATION)
        self.wait(0.8)

        # Answer
        ans = MathTex(
            r"P(\text{thjeshtë}) = \dfrac{16}{36} = \dfrac{4}{9}",
            font_size=CALC_SIZE, color=ANSWER_COLOR,
        )
        ans.next_to(sum_line, DOWN, buff=0.4).set_x(PX)
        box = make_answer_box(ans)
        self.play(Write(ans), run_time=T_KEY_EQUATION)
        self.play(Create(box), run_time=0.4)
        self.play(Circumscribe(VGroup(ans, box), color=HIGHLIGHT_COLOR, run_time=0.8))
        self.wait(W_AFTER_ANSWER)

        # Clean up everything including the table
        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=T_TRANSITION,
        )
        self.wait(0.3)

    # ────────────────────────────────────────────
    #  FINAL SUMMARY
    # ────────────────────────────────────────────

    def final_summary(self):
        title = MathTex(
            r"\text{Përmbledhje e përgjigjeve}",
            font_size=PART_HEADER_SIZE + 4, color=WHITE,
        )
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=T_TITLE_WRITE)

        rows = VGroup(
            MathTex(r"A = \{0, 1, 2, 3, 4, 5\}", font_size=ANSWER_SIZE, color=ANSWER_COLOR),
            MathTex(r"P(0) = \dfrac{1}{6}", font_size=ANSWER_SIZE, color=ANSWER_COLOR),
            MathTex(r"P(3) = \dfrac{1}{6}", font_size=ANSWER_SIZE, color=ANSWER_COLOR),
            MathTex(r"P(6) = 0", font_size=ANSWER_SIZE, color=ANSWER_COLOR),
            MathTex(r"P(\text{thjeshtë}) = \dfrac{4}{9}", font_size=ANSWER_SIZE, color=ANSWER_COLOR),
        )
        rows.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        box = make_answer_box(rows)
        content = VGroup(rows, box).move_to(ORIGIN).shift(DOWN * 0.3)

        if content.get_top()[1] > title.get_bottom()[1] - 0.4:
            content.next_to(title, DOWN, buff=0.5)

        self.play(
            LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3) for r in rows], lag_ratio=0.15),
            run_time=2.0,
        )
        self.play(Create(box), run_time=0.6)
        self.wait(W_AFTER_ANSWER)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=T_TRANSITION)

    # ────────────────────────────────────────────
    #  END SCREEN
    # ────────────────────────────────────────────

    def end_screen(self):
        domain = MathTex(
            r"\text{mesonjetorja.com}",
            font_size=TITLE_SIZE, color=WHITE,
        )
        domain.move_to(UP * 0.5)

        tagline = MathTex(
            r"\text{Më shumë ushtrime në faqen tonë!}",
            font_size=SUBTITLE_SIZE, color=BODY_TEXT_COLOR,
        )
        tagline.next_to(domain, DOWN, buff=0.5)

        self.play(
            GrowFromCenter(domain),
            FadeIn(tagline, shift=UP * 0.3),
            run_time=1.0,
        )
        self.wait(8.0)
