"""
YouTube Video — Ushtrimi 3, Njësia 8.3A
Matematika 10-11: Pjesa II

Dy zare të rregullta hidhen dhe mbahet shënim ndryshesa e pikëve.
a) Ndërtoni tabelën e hapësirës së rezultateve.
b) Bashkësia e rezultateve të mundshme.
c) P(0), P(3), P(6), P(numër i thjeshtë)
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))

from manim import *
import numpy as np
from components import ExerciseScene
from style_guide import (
    make_answer_box, fade_all,
    BG_COLOR, STEP_TITLE_COLOR, BODY_TEXT_COLOR, LABEL_COLOR,
    ANSWER_COLOR, SHAPE_COLOR, AUX_COLOR, HIGHLIGHT_COLOR, DIVIDER_COLOR,
    TITLE_SIZE, SUBTITLE_SIZE, PART_HEADER_SIZE, STEP_TITLE_SIZE,
    BODY_SIZE, CALC_SIZE, ANSWER_SIZE,
    T_TITLE_WRITE, T_SUBTITLE_FADE, T_HEADER_WRITE, T_STEP_TITLE,
    T_BODY_FADE, T_KEY_EQUATION, T_ROUTINE_EQUATION, T_SHAPE_CREATE,
    T_LAYOUT_SHIFT, T_TRANSITION,
    W_AFTER_KEY, W_AFTER_ROUTINE, W_AFTER_ANSWER, W_PROBLEM,
    ALBANIAN_TEX, PX,
)

# ── Difference table data ────────────────────
# |d(i,j)| = |i - j| for i,j in 1..6
DIFF_TABLE = [
    [0, 1, 2, 3, 4, 5],
    [1, 0, 1, 2, 3, 4],
    [2, 1, 0, 1, 2, 3],
    [3, 2, 1, 0, 1, 2],
    [4, 3, 2, 1, 0, 1],
    [5, 4, 3, 2, 1, 0],
]

# Counts per difference value
COUNTS = {0: 6, 1: 10, 2: 8, 3: 6, 4: 4, 5: 2}


class Ushtrimi3(ExerciseScene):
    exercise_number = 3
    unit = "8.3A"
    textbook = "Matematika 10-11: Pjesa II"
    parts = ["a", "b", "c"]

    # ────────────────────────────────────────────
    #  PART A — Build the difference table
    # ────────────────────────────────────────────

    def part_a(self):
        header = self.show_part_header("a")

        # Explain what we're doing
        explain1 = MathTex(
            r"\text{Hidhen dy zare të rregullta.}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        explain2 = MathTex(
            r"\text{Shënojmë ndryshesën } |i - j|",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        explain3 = MathTex(
            r"\text{ku } i \text{ dhe } j \text{ janë pikët e zareve.}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        explain_group = VGroup(explain1, explain2, explain3).arrange(DOWN, buff=0.2)
        explain_group.move_to(UP * 1.5)

        self.play(
            FadeIn(explain_group, shift=UP * 0.3),
            run_time=T_BODY_FADE,
        )
        self.wait(W_AFTER_KEY)
        self.play(FadeOut(explain_group), run_time=T_TRANSITION)
        self.wait(0.3)

        # Build the 6x6 table with headers
        table_title = MathTex(
            r"\text{Hapësira e rezultateve — Ndryshesa } |i - j|",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        table_title.to_edge(UP, buff=0.6)
        self.play(FadeIn(table_title), run_time=T_STEP_TITLE)

        cell_w, cell_h = 0.85, 0.55

        # Top-left corner label
        corner = MathTex(r"|i{-}j|", font_size=20, color=DIVIDER_COLOR)

        # Column headers (zari 2: j = 1..6)
        col_headers = VGroup()
        for c in range(6):
            h = MathTex(str(c + 1), font_size=22, color=SHAPE_COLOR)
            col_headers.add(h)

        # Row headers (zari 1: i = 1..6)
        row_headers = VGroup()
        for r in range(6):
            h = MathTex(str(r + 1), font_size=22, color=AUX_COLOR)
            row_headers.add(h)

        # Value cells
        value_cells = {}
        all_values = VGroup()
        for r in range(6):
            for c in range(6):
                val = DIFF_TABLE[r][c]
                txt = MathTex(str(val), font_size=22, color=WHITE)
                value_cells[(r, c)] = txt
                all_values.add(txt)

        # Position everything in grid
        grid_origin = UP * 0.8 + LEFT * 2.5
        corner.move_to(grid_origin)

        for c in range(6):
            col_headers[c].move_to(grid_origin + RIGHT * (c + 1) * cell_w)

        for r in range(6):
            row_headers[r].move_to(grid_origin + DOWN * (r + 1) * cell_h)
            for c in range(6):
                value_cells[(r, c)].move_to(
                    grid_origin + RIGHT * (c + 1) * cell_w + DOWN * (r + 1) * cell_h
                )

        # Column header label
        col_label = MathTex(
            r"\text{Zari 2 } (j)",
            font_size=18, color=SHAPE_COLOR,
        )
        col_label.next_to(VGroup(*col_headers), UP, buff=0.3)

        # Row header label
        row_label = MathTex(
            r"\text{Zari 1 } (i)",
            font_size=18, color=AUX_COLOR,
        )
        row_label.next_to(VGroup(*row_headers), LEFT, buff=0.3)
        row_label.rotate(PI / 2)

        # Animate: headers first
        self.play(
            FadeIn(corner),
            FadeIn(col_label),
            FadeIn(row_label),
            LaggedStartMap(GrowFromCenter, col_headers, lag_ratio=0.1),
            LaggedStartMap(GrowFromCenter, row_headers, lag_ratio=0.1),
            run_time=1.0,
        )
        self.wait(0.5)

        # Fill in values row by row
        for r in range(6):
            row_vals = VGroup(*[value_cells[(r, c)] for c in range(6)])
            self.play(
                LaggedStartMap(FadeIn, row_vals, lag_ratio=0.08),
                run_time=0.5,
            )
        self.wait(W_AFTER_KEY)

        # Draw horizontal and vertical grid lines
        grid_lines = VGroup()
        total_w = 6 * cell_w
        total_h = 6 * cell_h
        start_x = grid_origin[0] + cell_w * 0.5
        start_y = grid_origin[1] - cell_h * 0.5

        # Horizontal lines
        for r in range(7):
            y = start_y - r * cell_h + cell_h
            line = Line(
                np.array([start_x - cell_w * 0.5, y, 0]),
                np.array([start_x + total_w, y, 0]),
                stroke_width=0.5, color=DIVIDER_COLOR, stroke_opacity=0.3,
            )
            grid_lines.add(line)

        # Vertical lines
        for c in range(8):
            x = start_x + (c - 1) * cell_w + cell_w * 0.5
            if c > 7:
                break
            line = Line(
                np.array([x, start_y + cell_h, 0]),
                np.array([x, start_y - total_h + cell_h, 0]),
                stroke_width=0.5, color=DIVIDER_COLOR, stroke_opacity=0.3,
            )
            grid_lines.add(line)

        self.play(
            LaggedStartMap(Create, grid_lines, lag_ratio=0.02),
            run_time=0.8,
        )
        self.wait(0.3)

        # Explain: 36 total outcomes
        total_label = MathTex(
            r"\text{Gjithsej: } 6 \times 6 = 36 \text{ rezultate}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        total_label.next_to(
            VGroup(*[value_cells[(5, c)] for c in range(6)]),
            DOWN, buff=0.6,
        )
        self.play(FadeIn(total_label), run_time=T_BODY_FADE)
        self.wait(W_AFTER_KEY)

        # Store table elements for part_c
        self.value_cells = value_cells
        self.table_elements = VGroup(
            table_title, corner, col_label, row_label,
            col_headers, row_headers, all_values, grid_lines, total_label,
        )

    # ────────────────────────────────────────────
    #  PART B — Set of all possible outcomes
    # ────────────────────────────────────────────

    def part_b(self):
        header = self.show_part_header("b")

        explain = MathTex(
            r"\text{Nga tabela, vlerat e mundshme të ndryshesës janë:}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        explain.move_to(UP * 1.5)
        self.play(FadeIn(explain), run_time=T_BODY_FADE)
        self.wait(0.8)

        # Show each value with its count
        values_info = [
            (0, 6, LABEL_COLOR),
            (1, 10, WHITE),
            (2, 8, WHITE),
            (3, 6, WHITE),
            (4, 4, WHITE),
            (5, 2, WHITE),
        ]

        count_items = VGroup()
        for val, count, color in values_info:
            item = MathTex(
                str(val) + r" \to " + str(count) + r"\text{ herë}",
                font_size=BODY_SIZE, color=color,
            )
            count_items.add(item)

        count_items.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        count_items.next_to(explain, DOWN, buff=0.5)
        count_items.set_x(0)

        self.play(
            LaggedStartMap(FadeIn, count_items, lag_ratio=0.15),
            run_time=1.5,
        )
        self.wait(W_AFTER_ROUTINE)

        # Final answer: the set
        set_eq = MathTex(
            r"A = \{0, 1, 2, 3, 4, 5\}",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        set_eq.next_to(count_items, DOWN, buff=0.6)
        box = make_answer_box(set_eq)

        self.play(Write(set_eq), run_time=T_KEY_EQUATION)
        self.play(Create(box), run_time=0.5)
        self.wait(W_AFTER_ANSWER)

    # ────────────────────────────────────────────
    #  PART C — Probabilities
    # ────────────────────────────────────────────

    def part_c(self):
        header = self.show_part_header("c")

        # ── c.i) P(0) ──────────────────────────
        self._show_probability(
            label="i",
            question_text=r"\text{Gjeni } P(\text{ndryshesa} = 0)",
            why_text=r"\text{Ndryshesa 0: kur të dy zaret tregojnë njëlloj}",
            explanation_text=r"\text{Diagonalja kryesore: (1,1), (2,2), ..., (6,6)}",
            favorable=6,
            total=36,
            simplified_num=1,
            simplified_den=6,
            color=LABEL_COLOR,
        )

        # ── c.ii) P(3) ─────────────────────────
        self._show_probability(
            label="ii",
            question_text=r"\text{Gjeni } P(\text{ndryshesa} = 3)",
            why_text=r"\text{Ndryshesa 3: } |i - j| = 3",
            explanation_text=r"\text{Çiftet: (1,4), (4,1), (2,5), (5,2), (3,6), (6,3)}",
            favorable=6,
            total=36,
            simplified_num=1,
            simplified_den=6,
            color=SHAPE_COLOR,
        )

        # ── c.iii) P(6) ────────────────────────
        self._show_probability_zero(
            label="iii",
            question_text=r"\text{Gjeni } P(\text{ndryshesa} = 6)",
            why_text=r"\text{Ndryshesa maksimale: } |1 - 6| = 5",
            explanation_text=r"\text{Nuk ka asnjë çift me ndryshesë 6!}",
        )

        # ── c.iv) P(numër i thjeshtë) ──────────
        self._show_probability_prime()

    def _show_probability(self, label, question_text, why_text,
                          explanation_text, favorable, total,
                          simplified_num, simplified_den, color):
        """Show a single probability calculation step."""
        # Question
        q_label = MathTex(
            r"\textbf{" + label + r")}",
            font_size=STEP_TITLE_SIZE, color=color,
        )
        q_text = MathTex(question_text, font_size=BODY_SIZE, color=WHITE)
        q_row = VGroup(q_label, q_text).arrange(RIGHT, buff=0.3)
        q_row.move_to(UP * 2.5)

        self.play(FadeIn(q_row), run_time=T_STEP_TITLE)
        self.wait(0.5)

        # Why text
        why = MathTex(why_text, font_size=BODY_SIZE, color=BODY_TEXT_COLOR)
        why.next_to(q_row, DOWN, buff=0.4)
        self.play(FadeIn(why), run_time=T_BODY_FADE)
        self.wait(0.6)

        # Explanation
        expl = MathTex(explanation_text, font_size=BODY_SIZE, color=BODY_TEXT_COLOR)
        expl.next_to(why, DOWN, buff=0.3)
        self.play(FadeIn(expl), run_time=T_BODY_FADE)
        self.wait(W_AFTER_ROUTINE)

        # Formula
        formula = MathTex(
            r"P = \dfrac{\text{rastet e favorshme}}{\text{gjithë rastet}}",
            font_size=CALC_SIZE, color=WHITE,
        )
        formula.next_to(expl, DOWN, buff=0.5)
        self.play(Write(formula), run_time=T_KEY_EQUATION)
        self.wait(0.6)

        # Substitution
        subst = MathTex(
            r"P(" + str(DIFF_TABLE[0][0] if label == "i" else 3) + r") = \dfrac{"
            + str(favorable) + r"}{" + str(total) + r"}",
            font_size=CALC_SIZE, color=WHITE,
        )
        subst.next_to(formula, DOWN, buff=0.35)
        self.play(Write(subst), run_time=T_ROUTINE_EQUATION)
        self.wait(0.5)

        # Simplified answer
        answer = MathTex(
            r"= \dfrac{" + str(simplified_num) + r"}{" + str(simplified_den) + r"}",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        answer.next_to(subst, DOWN, buff=0.35)
        box = make_answer_box(answer)

        self.play(Write(answer), run_time=T_KEY_EQUATION)
        self.play(Create(box), run_time=0.5)
        self.play(Circumscribe(VGroup(answer, box), color=color, run_time=0.8))
        self.wait(W_AFTER_ANSWER)

        fade_all(self)
        self.wait(0.3)

    def _show_probability_zero(self, label, question_text, why_text,
                                explanation_text):
        """Show P(6) = 0 with emphasis on impossibility."""
        q_label = MathTex(
            r"\textbf{" + label + r")}",
            font_size=STEP_TITLE_SIZE, color=AUX_COLOR,
        )
        q_text = MathTex(question_text, font_size=BODY_SIZE, color=WHITE)
        q_row = VGroup(q_label, q_text).arrange(RIGHT, buff=0.3)
        q_row.move_to(UP * 2.5)

        self.play(FadeIn(q_row), run_time=T_STEP_TITLE)
        self.wait(0.5)

        # Why
        why = MathTex(why_text, font_size=BODY_SIZE, color=BODY_TEXT_COLOR)
        why.next_to(q_row, DOWN, buff=0.4)
        self.play(FadeIn(why), run_time=T_BODY_FADE)
        self.wait(W_AFTER_ROUTINE)

        # Explanation
        expl = MathTex(explanation_text, font_size=BODY_SIZE, color=AUX_COLOR)
        expl.next_to(why, DOWN, buff=0.3)
        self.play(FadeIn(expl), run_time=T_BODY_FADE)
        self.wait(W_AFTER_ROUTINE)

        # Answer
        answer = MathTex(r"P(6) = 0", font_size=ANSWER_SIZE, color=ANSWER_COLOR)
        answer.next_to(expl, DOWN, buff=0.6)
        box = make_answer_box(answer)

        self.play(Write(answer), run_time=T_KEY_EQUATION)
        self.play(Create(box), run_time=0.5)
        self.play(
            Flash(answer.get_center(), color=AUX_COLOR,
                  line_length=0.15, num_lines=8, run_time=0.5),
        )
        self.wait(W_AFTER_ANSWER)

        fade_all(self)
        self.wait(0.3)

    def _show_probability_prime(self):
        """Show P(prime number) with detailed counting."""
        q_label = MathTex(
            r"\textbf{iv)}",
            font_size=STEP_TITLE_SIZE, color=HIGHLIGHT_COLOR,
        )
        q_text = MathTex(
            r"\text{Gjeni } P(\text{numër i thjeshtë})",
            font_size=BODY_SIZE, color=WHITE,
        )
        q_row = VGroup(q_label, q_text).arrange(RIGHT, buff=0.3)
        q_row.move_to(UP * 2.8)

        self.play(FadeIn(q_row), run_time=T_STEP_TITLE)
        self.wait(0.5)

        # Recall the set
        set_text = MathTex(
            r"A = \{0, 1, 2, 3, 4, 5\}",
            font_size=CALC_SIZE, color=WHITE,
        )
        set_text.next_to(q_row, DOWN, buff=0.5)
        self.play(Write(set_text), run_time=T_ROUTINE_EQUATION)
        self.wait(0.5)

        # Identify primes
        why = MathTex(
            r"\text{Numrat e thjeshtë janë: numra} > 1 \text{ që pjesëtohen vetëm nga 1 dhe vetja}",
            font_size=18, color=BODY_TEXT_COLOR,
        )
        why.next_to(set_text, DOWN, buff=0.3)
        self.play(FadeIn(why), run_time=T_BODY_FADE)
        self.wait(0.8)

        # Check each number
        checks = VGroup()
        check_data = [
            ("0", r"\text{— jo}", DIVIDER_COLOR),
            ("1", r"\text{— jo (1 nuk është i thjeshtë)}", DIVIDER_COLOR),
            ("2", r"\text{— po } \checkmark", ANSWER_COLOR),
            ("3", r"\text{— po } \checkmark", ANSWER_COLOR),
            ("4", r"\text{— jo } (4 = 2 \times 2)", DIVIDER_COLOR),
            ("5", r"\text{— po } \checkmark", ANSWER_COLOR),
        ]

        for num, verdict, color in check_data:
            row = MathTex(num + r" " + verdict, font_size=BODY_SIZE, color=color)
            checks.add(row)

        checks.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        checks.next_to(why, DOWN, buff=0.4)
        checks.set_x(-1.0)

        self.play(
            LaggedStartMap(FadeIn, checks, lag_ratio=0.2),
            run_time=2.0,
        )
        self.wait(W_AFTER_KEY)

        fade_all(self)
        self.wait(0.3)

        # Count favorable outcomes
        count_title = MathTex(
            r"\text{Numërojmë rastet e favorshme:}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        count_title.move_to(UP * 2.8)
        self.play(FadeIn(count_title), run_time=T_STEP_TITLE)

        count_2 = MathTex(
            r"\text{Ndryshesa } 2 \to 8 \text{ herë}",
            font_size=BODY_SIZE, color=ANSWER_COLOR,
        )
        count_3 = MathTex(
            r"\text{Ndryshesa } 3 \to 6 \text{ herë}",
            font_size=BODY_SIZE, color=ANSWER_COLOR,
        )
        count_5 = MathTex(
            r"\text{Ndryshesa } 5 \to 2 \text{ herë}",
            font_size=BODY_SIZE, color=ANSWER_COLOR,
        )
        counts = VGroup(count_2, count_3, count_5).arrange(DOWN, buff=0.25)
        counts.next_to(count_title, DOWN, buff=0.5)
        counts.set_x(0)

        self.play(
            LaggedStartMap(FadeIn, counts, lag_ratio=0.2),
            run_time=1.2,
        )
        self.wait(W_AFTER_ROUTINE)

        # Sum
        sum_eq = MathTex(
            r"\text{Gjithsej: } 8 + 6 + 2 = 16",
            font_size=CALC_SIZE, color=WHITE,
        )
        sum_eq.next_to(counts, DOWN, buff=0.5)
        self.play(Write(sum_eq), run_time=T_KEY_EQUATION)
        self.wait(0.8)

        # Final probability
        prob_eq = MathTex(
            r"P(\text{thjeshtë}) = \dfrac{16}{36}",
            font_size=CALC_SIZE, color=WHITE,
        )
        prob_eq.next_to(sum_eq, DOWN, buff=0.5)
        self.play(Write(prob_eq), run_time=T_KEY_EQUATION)
        self.wait(0.6)

        # Simplify
        answer = MathTex(
            r"= \dfrac{4}{9}",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        answer.next_to(prob_eq, DOWN, buff=0.35)
        box = make_answer_box(answer)

        self.play(Write(answer), run_time=T_KEY_EQUATION)
        self.play(Create(box), run_time=0.5)
        self.play(Circumscribe(VGroup(answer, box), color=HIGHLIGHT_COLOR, run_time=0.8))
        self.wait(W_AFTER_ANSWER)

    # ────────────────────────────────────────────
    #  FINAL SUMMARY
    # ────────────────────────────────────────────

    def final_summary(self):
        self.show_summary_table(
            "Përmbledhje e përgjigjeve",
            [
                r"A = \{0, 1, 2, 3, 4, 5\}",
                r"P(0) = \dfrac{1}{6}",
                r"P(3) = \dfrac{1}{6}",
                r"P(6) = 0",
                r"P(\text{thjeshtë}) = \dfrac{4}{9}",
            ],
            font_size=ANSWER_SIZE,
        )
