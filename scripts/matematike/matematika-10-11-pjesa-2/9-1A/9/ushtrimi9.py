"""
YouTube Video — Ushtrimi 9, Njësia 9.1A
Matematika 10-11: Pjesa II

Gjeni kufizën e n-të të 5 progresioneve aritmetike.

a) 15, 12, 9, 6, 3, ...   -> aₙ = 18 - 3n
b) 10, 6, 2, -2, -6, ...  -> aₙ = 14 - 4n
c) 5, 1, -3, -7, -11, ... -> aₙ = 9 - 4n
d) -2, -5, -8, -11, -14,  -> aₙ = 1 - 3n
e) 1/2, -1/4, -1, -7/4, -5/2, ... -> aₙ = 5/4 - 3/4·n
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
    T_BODY_FADE, T_KEY_EQUATION, T_ROUTINE_EQUATION,
    T_TRANSITION,
    W_AFTER_KEY, W_AFTER_ROUTINE, W_AFTER_ANSWER,
    ALBANIAN_TEX,
)

PX = 0  # centered layout


class Ushtrimi9(Scene):
    def construct(self):
        apply_style(self)
        MathTex.set_default(tex_template=ALBANIAN_TEX)
        Tex.set_default(tex_template=ALBANIAN_TEX)

        self.title_screen()
        self.show_formula()
        self.part_a()
        self.part_b()
        self.part_c()
        self.part_d()
        self.part_e()
        self.final_summary()
        self.end_screen()

    # ────────────────────────────────────────────
    #  TITLE SCREEN
    # ────────────────────────────────────────────

    def title_screen(self):
        title = MathTex(
            r"\text{Ushtrimi 9 — Njësia 9.1A}",
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
    #  SHOW GENERAL FORMULA
    # ────────────────────────────────────────────

    def show_formula(self):
        # Center everything on screen — use the full space naturally
        heading = MathTex(
            r"\text{Kufiza e n-të e progresionit aritmetik:}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        formula = MathTex(
            r"a_n = a_1 + (n - 1) \cdot d",
            font_size=ANSWER_SIZE, color=WHITE,
        )
        explanation = MathTex(
            r"\text{ku } a_1 \text{ = kufiza e parë, } d \text{ = diferenca e përbashkët}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )

        group = VGroup(heading, formula, explanation).arrange(DOWN, buff=0.6)
        group.move_to(ORIGIN)

        self.play(Write(heading), run_time=T_STEP_TITLE)
        self.play(Write(formula), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)
        self.play(FadeIn(explanation, shift=UP * 0.2), run_time=T_BODY_FADE)
        self.wait(W_AFTER_KEY)

        self.play(FadeOut(group))
        self.wait(0.3)

    # ────────────────────────────────────────────
    #  HELPER: SOLVE ONE PART
    # ────────────────────────────────────────────

    def _solve_part(
        self,
        label,          # e.g. "a"
        terms_tex,      # LaTeX for the sequence terms
        d_tex,          # e.g. "-3"
        a1_tex,         # e.g. "15"
        d_display,      # displayed between arrows, e.g. "-3"
        sub_tex,        # substitution line, e.g. r"a_n = 15 + (n-1)(-3)"
        expand_tex,     # expanded, e.g. r"= 15 - 3n + 3"
        answer_tex,     # simplified, e.g. r"= 18 - 3n"
        answer_full,    # full answer for box, e.g. r"a_n = 18 - 3n"
        num_terms=5,    # how many terms in the sequence
    ):
        # --- Part header ---
        header = MathTex(
            r"\text{Pjesa " + label + r")}",
            font_size=PART_HEADER_SIZE, color=STEP_TITLE_COLOR,
        )
        header.to_edge(UP, buff=0.4)
        self.play(Write(header), run_time=T_STEP_TITLE)

        # --- Show the sequence terms — placed high with room for arrows below ---
        terms = MathTex(terms_tex, font_size=CALC_SIZE, color=WHITE)
        terms.next_to(header, DOWN, buff=0.6)
        self.play(Write(terms), run_time=T_KEY_EQUATION)
        self.wait(0.6)

        # --- Curved arrows BELOW the terms (avoids header overlap) ---
        arrows_group = VGroup()
        term_width = terms.width
        spacing = term_width / (num_terms - 0.2)
        left_edge = terms.get_left()[0] + spacing * 0.35

        for i in range(num_terms - 1):
            x_start = left_edge + i * spacing * 0.85
            x_end = left_edge + (i + 1) * spacing * 0.85
            y_base = terms.get_bottom()[1] - 0.15

            start_pt = np.array([x_start, y_base, 0])
            end_pt = np.array([x_end, y_base, 0])

            arrow = CurvedArrow(
                start_pt, end_pt,
                angle=TAU / 4,  # positive angle = curves downward
                color=LABEL_COLOR,
                stroke_width=2,
                tip_length=0.15,
            )

            d_label = MathTex(
                d_display, font_size=18, color=LABEL_COLOR,
            )
            d_label.next_to(arrow, DOWN, buff=0.05)

            arrows_group.add(VGroup(arrow, d_label))

        # Use Create instead of GrowArrow (GrowArrow crashes on CurvedArrow)
        self.play(
            LaggedStart(
                *[Create(ag[0]) for ag in arrows_group],
                lag_ratio=0.15,
            ),
            run_time=0.8,
        )
        self.play(
            LaggedStart(
                *[FadeIn(ag[1], shift=DOWN * 0.1) for ag in arrows_group],
                lag_ratio=0.1,
            ),
            run_time=0.5,
        )
        self.wait(0.6)

        # --- Show a₁ and d (below arrows) ---
        params = MathTex(
            r"a_1 = " + a1_tex + r", \quad d = " + d_tex,
            font_size=CALC_SIZE, color=SHAPE_COLOR,
        )
        params.next_to(arrows_group, DOWN, buff=0.4)
        params.set_x(PX)
        self.play(Write(params), run_time=T_ROUTINE_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        # --- Clear the sequence visual to free screen for calculation ---
        self.play(
            FadeOut(terms), FadeOut(arrows_group),
            run_time=0.4,
        )

        # --- Move params up to make room for the calculation chain ---
        params_target = header.get_bottom() + DOWN * 0.5
        self.play(params.animate.move_to(params_target).set_x(PX), run_time=0.4)

        # --- Substitution ---
        why_text = MathTex(
            r"\text{Zëvendësojmë në formulë:}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        why_text.next_to(params, DOWN, buff=0.5)
        why_text.set_x(PX)
        self.play(FadeIn(why_text, shift=UP * 0.15), run_time=T_BODY_FADE)
        self.wait(0.5)

        sub_eq = MathTex(sub_tex, font_size=CALC_SIZE, color=WHITE)
        sub_eq.next_to(why_text, DOWN, buff=0.4)
        sub_eq.set_x(PX)
        self.play(Write(sub_eq), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        # --- Expand ---
        expand_eq = MathTex(expand_tex, font_size=CALC_SIZE, color=WHITE)
        expand_eq.next_to(sub_eq, DOWN, buff=0.4)
        expand_eq.set_x(PX)
        self.play(Write(expand_eq), run_time=T_ROUTINE_EQUATION)
        self.wait(0.8)

        # --- Simplify = answer ---
        answer_eq = MathTex(answer_tex, font_size=CALC_SIZE, color=ANSWER_COLOR)
        answer_eq.next_to(expand_eq, DOWN, buff=0.4)
        answer_eq.set_x(PX)
        self.play(Write(answer_eq), run_time=T_KEY_EQUATION)
        self.wait(0.8)

        # --- Boxed answer ---
        answer_boxed = MathTex(answer_full, font_size=ANSWER_SIZE, color=ANSWER_COLOR)
        answer_boxed.next_to(answer_eq, DOWN, buff=0.5)
        answer_boxed.set_x(PX)

        box = make_answer_box(answer_boxed)
        self.play(GrowFromCenter(answer_boxed), run_time=0.6)
        self.play(Create(box), run_time=0.4)
        self.play(Circumscribe(answer_boxed, color=HIGHLIGHT_COLOR, run_time=0.8))
        self.wait(W_AFTER_KEY)

        # --- Clean up ---
        all_items = VGroup(
            header, params,
            why_text, sub_eq, expand_eq, answer_eq,
            answer_boxed, box,
        )
        self.play(FadeOut(all_items), run_time=T_TRANSITION)
        self.wait(0.3)

    # ────────────────────────────────────────────
    #  PART A: 15, 12, 9, 6, 3, ...
    # ────────────────────────────────────────────

    def part_a(self):
        self._solve_part(
            label="a",
            terms_tex=r"15, \; 12, \; 9, \; 6, \; 3, \; \ldots",
            d_tex="-3",
            a1_tex="15",
            d_display="-3",
            sub_tex=r"a_n = 15 + (n - 1)(-3)",
            expand_tex=r"= 15 - 3n + 3",
            answer_tex=r"= 18 - 3n",
            answer_full=r"a_n = 18 - 3n",
        )

    # ────────────────────────────────────────────
    #  PART B: 10, 6, 2, -2, -6, ...
    # ────────────────────────────────────────────

    def part_b(self):
        self._solve_part(
            label="b",
            terms_tex=r"10, \; 6, \; 2, \; -2, \; -6, \; \ldots",
            d_tex="-4",
            a1_tex="10",
            d_display="-4",
            sub_tex=r"a_n = 10 + (n - 1)(-4)",
            expand_tex=r"= 10 - 4n + 4",
            answer_tex=r"= 14 - 4n",
            answer_full=r"a_n = 14 - 4n",
        )

    # ────────────────────────────────────────────
    #  PART C: 5, 1, -3, -7, -11, ...
    # ────────────────────────────────────────────

    def part_c(self):
        self._solve_part(
            label="c",
            terms_tex=r"5, \; 1, \; -3, \; -7, \; -11, \; \ldots",
            d_tex="-4",
            a1_tex="5",
            d_display="-4",
            sub_tex=r"a_n = 5 + (n - 1)(-4)",
            expand_tex=r"= 5 - 4n + 4",
            answer_tex=r"= 9 - 4n",
            answer_full=r"a_n = 9 - 4n",
        )

    # ────────────────────────────────────────────
    #  PART D: -2, -5, -8, -11, -14, ...
    # ────────────────────────────────────────────

    def part_d(self):
        self._solve_part(
            label="d",
            terms_tex=r"-2, \; -5, \; -8, \; -11, \; -14, \; \ldots",
            d_tex="-3",
            a1_tex="-2",
            d_display="-3",
            sub_tex=r"a_n = -2 + (n - 1)(-3)",
            expand_tex=r"= -2 - 3n + 3",
            answer_tex=r"= 1 - 3n",
            answer_full=r"a_n = 1 - 3n",
        )

    # ────────────────────────────────────────────
    #  PART E: 1/2, -1/4, -1, -7/4, -5/2, ...
    # ────────────────────────────────────────────

    def part_e(self):
        self._solve_part(
            label="e",
            terms_tex=(
                r"\frac{1}{2}, \; -\frac{1}{4}, \; -1, \;"
                r"-\frac{7}{4}, \; -\frac{5}{2}, \; \ldots"
            ),
            d_tex=r"-\frac{3}{4}",
            a1_tex=r"\frac{1}{2}",
            d_display=r"-\!\frac{3}{4}",
            sub_tex=r"a_n = \frac{1}{2} + (n - 1)\!\left(-\frac{3}{4}\right)",
            expand_tex=r"= \frac{1}{2} - \frac{3}{4}n + \frac{3}{4}",
            answer_tex=r"= \frac{5}{4} - \frac{3}{4}n",
            answer_full=r"a_n = \frac{5}{4} - \frac{3}{4} \cdot n",
        )

    # ────────────────────────────────────────────
    #  FINAL SUMMARY
    # ────────────────────────────────────────────

    def final_summary(self):
        heading = MathTex(
            r"\text{Përmbledhje e përgjigjeve:}",
            font_size=PART_HEADER_SIZE, color=STEP_TITLE_COLOR,
        )
        heading.to_edge(UP, buff=0.6)

        answers_data = [
            (r"\text{a)} \quad a_n = 18 - 3n",),
            (r"\text{b)} \quad a_n = 14 - 4n",),
            (r"\text{c)} \quad a_n = 9 - 4n",),
            (r"\text{d)} \quad a_n = 1 - 3n",),
            (r"\text{e)} \quad a_n = \frac{5}{4} - \frac{3}{4} \cdot n",),
        ]

        rows = VGroup()
        for tex_str, in answers_data:
            row = MathTex(tex_str, font_size=CALC_SIZE, color=ANSWER_COLOR)
            rows.add(row)

        rows.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        rows.next_to(heading, DOWN, buff=0.5)

        # Center the group on screen
        summary_group = VGroup(heading, rows)
        summary_group.move_to(ORIGIN)
        heading.to_edge(UP, buff=0.6)
        rows.next_to(heading, DOWN, buff=0.5)

        box = make_answer_box(rows)

        self.play(Write(heading), run_time=T_STEP_TITLE)
        self.wait(0.3)

        # Reveal answers one by one
        for row in rows:
            self.play(FadeIn(row, shift=RIGHT * 0.3), run_time=0.5)
            self.wait(0.4)

        self.play(Create(box), run_time=0.6)
        self.play(
            Flash(rows.get_center(), color=ANSWER_COLOR,
                  line_length=0.3, num_lines=16, run_time=0.8),
        )
        self.wait(W_AFTER_ANSWER)

        self.play(FadeOut(VGroup(heading, rows, box)), run_time=T_TRANSITION)
        self.wait(0.3)

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
