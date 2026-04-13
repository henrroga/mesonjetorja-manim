"""
YouTube Video — Ushtrimi 5, Njësia 10.2A
Matematika 10-11: Pjesa I

Zgjidhni 10 ekuacione kuadratike me formulën kuadratike.

1) x²+9x-25=0  → x₁≈2,2   x₂≈-11,2
2) x²+3x-11=0  → x₁≈2,1   x₂≈-5,1
3) x²-8x+6=0   → x₁≈7,2   x₂≈0,8
4) x²-7x+3=0   → x₁≈6,5   x₂≈0,5
5) x²+20x=45   → x₁≈2,0   x₂≈-22,0
6) x²+13x=2    → x₁≈0,2   x₂≈-13,2
7) 3x²+3x-2=0  → x₁≈0,5   x₂≈-1,5
8) 5x²+7x-12=0 → x₁=1     x₂=-2,4
9) 0=6x²+12x-15→ x₁≈0,9   x₂≈-2,9
10)0=4x²+11x-18→ x₁≈1,2   x₂≈-3,9
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


class Ushtrimi5(Scene):
    def construct(self):
        apply_style(self)
        MathTex.set_default(tex_template=ALBANIAN_TEX)
        Tex.set_default(tex_template=ALBANIAN_TEX)

        self.title_screen()
        self.show_formula()
        self.part_1()
        self.part_2()
        self.part_3()
        self.part_4()
        self.part_5()
        self.part_6()
        self.part_7()
        self.part_8()
        self.part_9()
        self.part_10()
        self.final_summary()
        self.end_screen()

    # ────────────────────────────────────────────
    #  TITLE SCREEN
    # ────────────────────────────────────────────

    def title_screen(self):
        title = MathTex(
            r"\text{Ushtrimi 5 — Njësia 10.2A}",
            font_size=TITLE_SIZE, color=WHITE,
        )
        source = MathTex(
            r"\text{Matematika 10-11: Pjesa I}",
            font_size=SUBTITLE_SIZE, color=BODY_TEXT_COLOR,
        )
        source.next_to(title, DOWN, buff=0.4)

        self.play(Write(title), run_time=T_TITLE_WRITE)
        self.play(FadeIn(source, shift=UP * 0.2), run_time=T_SUBTITLE_FADE)
        self.wait(W_AFTER_KEY)
        self.play(FadeOut(title), FadeOut(source))
        self.wait(0.5)

    # ────────────────────────────────────────────
    #  SHOW QUADRATIC FORMULA
    # ────────────────────────────────────────────

    def show_formula(self):
        heading = MathTex(
            r"\text{Formula kuadratike:}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        disc_formula = MathTex(
            r"D = b^2 - 4ac",
            font_size=ANSWER_SIZE, color=LABEL_COLOR,
        )
        x_formula = MathTex(
            r"x = \frac{-b \pm \sqrt{D}}{2a}",
            font_size=ANSWER_SIZE, color=WHITE,
        )

        group = VGroup(heading, disc_formula, x_formula).arrange(DOWN, buff=0.6)
        group.move_to(ORIGIN)

        self.play(Write(heading), run_time=T_STEP_TITLE)
        self.play(Write(disc_formula), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)
        self.play(Write(x_formula), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_KEY)

        self.play(FadeOut(group))
        self.wait(0.3)

    # ────────────────────────────────────────────
    #  HELPER: SOLVE ONE PART
    # ────────────────────────────────────────────

    def _solve_part(
        self,
        label,              # e.g. "1"
        eq_tex,             # original equation, e.g. r"x^2 + 9x - 25 = 0"
        a_tex,              # e.g. "1"
        b_tex,              # e.g. "9"
        c_tex,              # e.g. "-25"
        d_tex,              # discriminant calc, e.g. r"9^2 - 4(1)(-25) = 81 + 100 = 181"
        d_val,              # discriminant value, e.g. "181"
        x_formula_tex,      # formula substitution, e.g. r"\frac{-9 \pm \sqrt{181}}{2}"
        x1_tex,             # e.g. r"x_1 \approx 2{,}2"
        x2_tex,             # e.g. r"x_2 \approx -11{,}2"
        rearrange_tex=None, # for parts needing rearrangement
        d_note=None,        # optional note about D (e.g. "= 17^2" for part 8)
    ):
        # --- Part header ---
        header = MathTex(
            r"\text{Pjesa " + label + r")}",
            font_size=PART_HEADER_SIZE, color=STEP_TITLE_COLOR,
        )
        header.to_edge(UP, buff=0.4)
        self.play(Write(header), run_time=T_STEP_TITLE)

        # --- Show equation (centered) ---
        equation = MathTex(eq_tex, font_size=CALC_SIZE, color=WHITE)
        equation.next_to(header, DOWN, buff=0.5)
        equation.set_x(PX)
        self.play(Write(equation), run_time=T_KEY_EQUATION)
        self.wait(0.6)

        # --- Rearrange if needed ---
        if rearrange_tex is not None:
            rearrange_label = MathTex(
                r"\text{Rirendisim:}",
                font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
            )
            rearrange_label.next_to(equation, DOWN, buff=0.4)
            rearrange_label.set_x(PX)
            self.play(FadeIn(rearrange_label, shift=UP * 0.15), run_time=T_BODY_FADE)
            self.wait(0.4)

            rearranged = MathTex(rearrange_tex, font_size=CALC_SIZE, color=WHITE)
            rearranged.next_to(rearrange_label, DOWN, buff=0.35)
            rearranged.set_x(PX)
            self.play(Write(rearranged), run_time=T_ROUTINE_EQUATION)
            self.wait(0.6)

            # Fade original + rearrange label, keep rearranged as new equation
            self.play(
                FadeOut(equation), FadeOut(rearrange_label),
                rearranged.animate.next_to(header, DOWN, buff=0.5).set_x(PX),
                run_time=0.5,
            )
            equation = rearranged
            self.wait(0.3)

        # --- Identify a, b, c ---
        coeffs = MathTex(
            r"a = " + a_tex + r", \quad b = " + b_tex + r", \quad c = " + c_tex,
            font_size=CALC_SIZE, color=SHAPE_COLOR,
        )
        coeffs.next_to(equation, DOWN, buff=0.45)
        coeffs.set_x(PX)
        self.play(Write(coeffs), run_time=T_ROUTINE_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        # --- Fade equation, move coeffs up to save space ---
        self.play(
            FadeOut(equation),
            coeffs.animate.next_to(header, DOWN, buff=0.5).set_x(PX),
            run_time=0.4,
        )

        # --- Calculate discriminant ---
        d_label = MathTex(
            r"\text{Dallori:}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        d_label.next_to(coeffs, DOWN, buff=0.45)
        d_label.set_x(PX)
        self.play(FadeIn(d_label, shift=UP * 0.15), run_time=T_BODY_FADE)

        d_calc = MathTex(
            r"D = b^2 - 4ac = " + d_tex,
            font_size=CALC_SIZE, color=WHITE,
        )
        d_calc.next_to(d_label, DOWN, buff=0.35)
        d_calc.set_x(PX)
        self.play(Write(d_calc), run_time=T_KEY_EQUATION)
        self.wait(0.6)

        # Highlight D value
        d_result = MathTex(
            r"D = " + d_val,
            font_size=CALC_SIZE, color=LABEL_COLOR,
        )
        d_result.next_to(d_calc, DOWN, buff=0.35)
        d_result.set_x(PX)
        self.play(Write(d_result), run_time=T_ROUTINE_EQUATION)

        # Optional note about D (e.g. perfect square)
        if d_note is not None:
            note = MathTex(
                d_note, font_size=BODY_SIZE, color=HIGHLIGHT_COLOR,
            )
            note.next_to(d_result, RIGHT, buff=0.3)
            self.play(FadeIn(note, shift=LEFT * 0.2), run_time=0.4)
            self.wait(0.5)
        else:
            self.wait(0.6)

        # --- Clear discriminant work, keep coeffs and D result ---
        fade_items = [d_label, d_calc]
        if d_note is not None:
            fade_items.append(note)
        self.play(
            *[FadeOut(item) for item in fade_items],
            d_result.animate.next_to(coeffs, DOWN, buff=0.4).set_x(PX),
            run_time=0.4,
        )

        # --- Apply formula ---
        formula_label = MathTex(
            r"\text{Zbatojmë formulën:}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        formula_label.next_to(d_result, DOWN, buff=0.45)
        formula_label.set_x(PX)
        self.play(FadeIn(formula_label, shift=UP * 0.15), run_time=T_BODY_FADE)

        x_calc = MathTex(
            r"x = " + x_formula_tex,
            font_size=CALC_SIZE, color=WHITE,
        )
        x_calc.next_to(formula_label, DOWN, buff=0.35)
        x_calc.set_x(PX)
        self.play(Write(x_calc), run_time=T_KEY_EQUATION)
        self.wait(0.8)

        # --- Show x₁ and x₂ ---
        x1 = MathTex(x1_tex, font_size=CALC_SIZE, color=ANSWER_COLOR)
        x2 = MathTex(x2_tex, font_size=CALC_SIZE, color=ANSWER_COLOR)

        answers = VGroup(x1, x2).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        answers.next_to(x_calc, DOWN, buff=0.45)
        answers.set_x(PX)

        self.play(Write(x1), run_time=T_ROUTINE_EQUATION)
        self.wait(0.4)
        self.play(Write(x2), run_time=T_ROUTINE_EQUATION)
        self.wait(0.6)

        # --- Box the answers ---
        box = make_answer_box(answers)
        self.play(Create(box), run_time=0.4)
        self.play(Circumscribe(answers, color=HIGHLIGHT_COLOR, run_time=0.8))
        self.wait(W_AFTER_KEY)

        # --- Clean up ---
        all_items = VGroup(
            header, coeffs, d_result,
            formula_label, x_calc,
            x1, x2, box,
        )
        self.play(FadeOut(all_items), run_time=T_TRANSITION)
        self.wait(0.3)

    # ────────────────────────────────────────────
    #  PART 1: x² + 9x - 25 = 0
    # ────────────────────────────────────────────

    def part_1(self):
        self._solve_part(
            label="1",
            eq_tex=r"x^2 + 9x - 25 = 0",
            a_tex="1", b_tex="9", c_tex="-25",
            d_tex=r"9^2 - 4(1)(-25) = 81 + 100 = 181",
            d_val="181",
            x_formula_tex=r"\frac{-9 \pm \sqrt{181}}{2}",
            x1_tex=r"x_1 \approx 2{,}2",
            x2_tex=r"x_2 \approx -11{,}2",
        )

    # ────────────────────────────────────────────
    #  PART 2: x² + 3x - 11 = 0
    # ────────────────────────────────────────────

    def part_2(self):
        self._solve_part(
            label="2",
            eq_tex=r"x^2 + 3x - 11 = 0",
            a_tex="1", b_tex="3", c_tex="-11",
            d_tex=r"3^2 - 4(1)(-11) = 9 + 44 = 53",
            d_val="53",
            x_formula_tex=r"\frac{-3 \pm \sqrt{53}}{2}",
            x1_tex=r"x_1 \approx 2{,}1",
            x2_tex=r"x_2 \approx -5{,}1",
        )

    # ────────────────────────────────────────────
    #  PART 3: x² - 8x + 6 = 0
    # ────────────────────────────────────────────

    def part_3(self):
        self._solve_part(
            label="3",
            eq_tex=r"x^2 - 8x + 6 = 0",
            a_tex="1", b_tex="-8", c_tex="6",
            d_tex=r"(-8)^2 - 4(1)(6) = 64 - 24 = 40",
            d_val="40",
            x_formula_tex=r"\frac{8 \pm \sqrt{40}}{2}",
            x1_tex=r"x_1 \approx 7{,}2",
            x2_tex=r"x_2 \approx 0{,}8",
        )

    # ────────────────────────────────────────────
    #  PART 4: x² - 7x + 3 = 0
    # ────────────────────────────────────────────

    def part_4(self):
        self._solve_part(
            label="4",
            eq_tex=r"x^2 - 7x + 3 = 0",
            a_tex="1", b_tex="-7", c_tex="3",
            d_tex=r"(-7)^2 - 4(1)(3) = 49 - 12 = 37",
            d_val="37",
            x_formula_tex=r"\frac{7 \pm \sqrt{37}}{2}",
            x1_tex=r"x_1 \approx 6{,}5",
            x2_tex=r"x_2 \approx 0{,}5",
        )

    # ────────────────────────────────────────────
    #  PART 5: x² + 20x = 45
    # ────────────────────────────────────────────

    def part_5(self):
        self._solve_part(
            label="5",
            eq_tex=r"x^2 + 20x = 45",
            a_tex="1", b_tex="20", c_tex="-45",
            d_tex=r"20^2 - 4(1)(-45) = 400 + 180 = 580",
            d_val="580",
            x_formula_tex=r"\frac{-20 \pm \sqrt{580}}{2}",
            x1_tex=r"x_1 \approx 2{,}0",
            x2_tex=r"x_2 \approx -22{,}0",
            rearrange_tex=r"x^2 + 20x - 45 = 0",
        )

    # ────────────────────────────────────────────
    #  PART 6: x² + 13x = 2
    # ────────────────────────────────────────────

    def part_6(self):
        self._solve_part(
            label="6",
            eq_tex=r"x^2 + 13x = 2",
            a_tex="1", b_tex="13", c_tex="-2",
            d_tex=r"13^2 - 4(1)(-2) = 169 + 8 = 177",
            d_val="177",
            x_formula_tex=r"\frac{-13 \pm \sqrt{177}}{2}",
            x1_tex=r"x_1 \approx 0{,}2",
            x2_tex=r"x_2 \approx -13{,}2",
            rearrange_tex=r"x^2 + 13x - 2 = 0",
        )

    # ────────────────────────────────────────────
    #  PART 7: 3x² + 3x - 2 = 0
    # ────────────────────────────────────────────

    def part_7(self):
        self._solve_part(
            label="7",
            eq_tex=r"3x^2 + 3x - 2 = 0",
            a_tex="3", b_tex="3", c_tex="-2",
            d_tex=r"3^2 - 4(3)(-2) = 9 + 24 = 33",
            d_val="33",
            x_formula_tex=r"\frac{-3 \pm \sqrt{33}}{6}",
            x1_tex=r"x_1 \approx 0{,}5",
            x2_tex=r"x_2 \approx -1{,}5",
        )

    # ────────────────────────────────────────────
    #  PART 8: 5x² + 7x - 12 = 0
    # ────────────────────────────────────────────

    def part_8(self):
        self._solve_part(
            label="8",
            eq_tex=r"5x^2 + 7x - 12 = 0",
            a_tex="5", b_tex="7", c_tex="-12",
            d_tex=r"7^2 - 4(5)(-12) = 49 + 240 = 289",
            d_val="289",
            x_formula_tex=r"\frac{-7 \pm 17}{10}",
            x1_tex=r"x_1 = \frac{-7 + 17}{10} = \frac{10}{10} = 1",
            x2_tex=r"x_2 = \frac{-7 - 17}{10} = \frac{-24}{10} = -2{,}4",
            d_note=r"= 17^2 \text{ (katror i plotë!)}",
        )

    # ────────────────────────────────────────────
    #  PART 9: 0 = 6x² + 12x - 15
    # ────────────────────────────────────────────

    def part_9(self):
        self._solve_part(
            label="9",
            eq_tex=r"0 = 6x^2 + 12x - 15",
            a_tex="6", b_tex="12", c_tex="-15",
            d_tex=r"12^2 - 4(6)(-15) = 144 + 360 = 504",
            d_val="504",
            x_formula_tex=r"\frac{-12 \pm \sqrt{504}}{12}",
            x1_tex=r"x_1 \approx 0{,}9",
            x2_tex=r"x_2 \approx -2{,}9",
            rearrange_tex=r"6x^2 + 12x - 15 = 0",
        )

    # ────────────────────────────────────────────
    #  PART 10: 0 = 4x² + 11x - 18
    # ────────────────────────────────────────────

    def part_10(self):
        self._solve_part(
            label="10",
            eq_tex=r"0 = 4x^2 + 11x - 18",
            a_tex="4", b_tex="11", c_tex="-18",
            d_tex=r"11^2 - 4(4)(-18) = 121 + 288 = 409",
            d_val="409",
            x_formula_tex=r"\frac{-11 \pm \sqrt{409}}{8}",
            x1_tex=r"x_1 \approx 1{,}2",
            x2_tex=r"x_2 \approx -3{,}9",
            rearrange_tex=r"4x^2 + 11x - 18 = 0",
        )

    # ────────────────────────────────────────────
    #  FINAL SUMMARY
    # ────────────────────────────────────────────

    def final_summary(self):
        heading = MathTex(
            r"\text{Përmbledhje e përgjigjeve:}",
            font_size=PART_HEADER_SIZE, color=STEP_TITLE_COLOR,
        )
        heading.to_edge(UP, buff=0.4)

        # Two columns of 5 answers each
        left_data = [
            r"\text{1)} \; x_1 \!\approx\! 2{,}2, \; x_2 \!\approx\! -11{,}2",
            r"\text{2)} \; x_1 \!\approx\! 2{,}1, \; x_2 \!\approx\! -5{,}1",
            r"\text{3)} \; x_1 \!\approx\! 7{,}2, \; x_2 \!\approx\! 0{,}8",
            r"\text{4)} \; x_1 \!\approx\! 6{,}5, \; x_2 \!\approx\! 0{,}5",
            r"\text{5)} \; x_1 \!\approx\! 2{,}0, \; x_2 \!\approx\! -22{,}0",
        ]
        right_data = [
            r"\text{6)} \; x_1 \!\approx\! 0{,}2, \; x_2 \!\approx\! -13{,}2",
            r"\text{7)} \; x_1 \!\approx\! 0{,}5, \; x_2 \!\approx\! -1{,}5",
            r"\text{8)} \; x_1 \!=\! 1, \; x_2 \!=\! -2{,}4",
            r"\text{9)} \; x_1 \!\approx\! 0{,}9, \; x_2 \!\approx\! -2{,}9",
            r"\text{10)} \; x_1 \!\approx\! 1{,}2, \; x_2 \!\approx\! -3{,}9",
        ]

        left_col = VGroup()
        for tex_str in left_data:
            row = MathTex(tex_str, font_size=24, color=ANSWER_COLOR)
            left_col.add(row)
        left_col.arrange(DOWN, buff=0.3, aligned_edge=LEFT)

        right_col = VGroup()
        for tex_str in right_data:
            row = MathTex(tex_str, font_size=24, color=ANSWER_COLOR)
            right_col.add(row)
        right_col.arrange(DOWN, buff=0.3, aligned_edge=LEFT)

        columns = VGroup(left_col, right_col).arrange(RIGHT, buff=1.0, aligned_edge=UP)
        columns.next_to(heading, DOWN, buff=0.5)

        all_rows = VGroup(heading, columns)
        # Ensure it fits on screen
        if all_rows.get_bottom()[1] < -3.5:
            columns.scale(0.9)
            columns.next_to(heading, DOWN, buff=0.4)

        box = make_answer_box(columns)

        self.play(Write(heading), run_time=T_STEP_TITLE)
        self.wait(0.3)

        # Reveal answers one by one
        all_items = list(left_col) + list(right_col)
        for i, row in enumerate(all_items):
            self.play(FadeIn(row, shift=RIGHT * 0.3), run_time=0.35)
            if i < len(all_items) - 1:
                self.wait(0.2)

        self.play(Create(box), run_time=0.6)
        self.play(
            Flash(columns.get_center(), color=ANSWER_COLOR,
                  line_length=0.3, num_lines=16, run_time=0.8),
        )
        self.wait(W_AFTER_ANSWER)

        self.play(FadeOut(VGroup(heading, columns, box)), run_time=T_TRANSITION)
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
