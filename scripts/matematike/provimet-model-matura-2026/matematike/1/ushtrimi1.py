"""
YouTube Video — Ushtrimi 1, Matematikë
Provimet Model Matura 2026

A = {x ∈ ℕ | 3 < x < 100}
B = {x ∈ ℕ | 3^x ∈ A}
Sa elemente ka B?  Përgjigja: C) 3
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

PX = 0  # centered layout — no left/right split needed


class Ushtrimi1(Scene):
    def construct(self):
        apply_style(self)
        MathTex.set_default(tex_template=ALBANIAN_TEX)
        Tex.set_default(tex_template=ALBANIAN_TEX)

        self.title_screen()
        self.show_problem()
        self.solve()
        self.end_screen()

    # ────────────────────────────────────────────
    #  TITLE SCREEN
    # ────────────────────────────────────────────

    def title_screen(self):
        title = MathTex(
            r"\text{Ushtrimi 1 — Matematikë}",
            font_size=TITLE_SIZE, color=WHITE,
        )
        source = MathTex(
            r"\text{Provimet Model Matura 2026}",
            font_size=SUBTITLE_SIZE, color=BODY_TEXT_COLOR,
        )
        source.next_to(title, DOWN, buff=0.4)

        self.play(Write(title), run_time=T_TITLE_WRITE)
        self.play(FadeIn(source, shift=UP * 0.2), run_time=T_SUBTITLE_FADE)
        self.wait(W_AFTER_KEY)
        self.play(FadeOut(title), FadeOut(source))
        self.wait(0.5)

    # ────────────────────────────────────────────
    #  SHOW PROBLEM
    # ────────────────────────────────────────────

    def show_problem(self):
        # Set definitions
        set_a = MathTex(
            r"A = \{ x \in \mathbb{N} \mid 3 < x < 100 \}",
            font_size=CALC_SIZE, color=WHITE,
        )
        set_b = MathTex(
            r"B = \{ x \in \mathbb{N} \mid 3^x \in A \}",
            font_size=CALC_SIZE, color=WHITE,
        )
        question = MathTex(
            r"\text{Sa elemente ka bashkësia } B \text{?}",
            font_size=CALC_SIZE, color=HIGHLIGHT_COLOR,
        )

        defs = VGroup(set_a, set_b, question).arrange(DOWN, buff=0.45)
        defs.move_to(UP * 1.2)

        self.play(Write(set_a), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)
        self.play(Write(set_b), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)
        self.play(FadeIn(question, shift=UP * 0.2), run_time=T_BODY_FADE)
        self.wait(0.8)

        # Multiple choice options
        opt_a = MathTex(r"\text{A) } 1", font_size=BODY_SIZE, color=WHITE)
        opt_b = MathTex(r"\text{B) } 2", font_size=BODY_SIZE, color=WHITE)
        opt_c = MathTex(r"\text{C) } 3", font_size=BODY_SIZE, color=WHITE)
        opt_d = MathTex(r"\text{D) } 4", font_size=BODY_SIZE, color=WHITE)

        opts = VGroup(opt_a, opt_b, opt_c, opt_d).arrange(RIGHT, buff=0.8)
        opts.next_to(question, DOWN, buff=0.6)

        self.play(
            LaggedStart(
                FadeIn(opt_a, shift=UP * 0.2),
                FadeIn(opt_b, shift=UP * 0.2),
                FadeIn(opt_c, shift=UP * 0.2),
                FadeIn(opt_d, shift=UP * 0.2),
                lag_ratio=0.15,
            ),
            run_time=1.0,
        )
        self.wait(W_AFTER_KEY)

        # Store for cleanup
        self.problem_group = VGroup(set_a, set_b, question, opts)
        self.play(FadeOut(self.problem_group), run_time=T_TRANSITION)
        self.wait(0.3)

    # ────────────────────────────────────────────
    #  SOLVE
    # ────────────────────────────────────────────

    def solve(self):
        # Step 1: Rewrite the condition
        step1_title = MathTex(
            r"\text{Kushti për } x \in B \text{:}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        step1_title.to_edge(UP, buff=0.6)

        condition = MathTex(
            r"3^x \in A \;\Longleftrightarrow\; 3 < 3^x < 100",
            font_size=CALC_SIZE, color=WHITE,
        )
        condition.next_to(step1_title, DOWN, buff=0.5)

        self.play(Write(step1_title), run_time=T_STEP_TITLE)
        self.play(Write(condition), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_KEY)

        # Step 2: Explain approach
        approach = MathTex(
            r"\text{Provojmë vlerat e } x \in \mathbb{N} \text{:}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        approach.next_to(condition, DOWN, buff=0.5)
        self.play(FadeIn(approach), run_time=T_BODY_FADE)
        self.wait(W_AFTER_ROUTINE)

        # Step 3: Check each x value
        checks_data = [
            (1, 3,   False, r"3^1 = 3",   r"3 \not> 3"),
            (2, 9,   True,  r"3^2 = 9",   r"3 < 9 < 100"),
            (3, 27,  True,  r"3^3 = 27",  r"3 < 27 < 100"),
            (4, 81,  True,  r"3^4 = 81",  r"3 < 81 < 100"),
            (5, 243, False, r"3^5 = 243", r"243 \not< 100"),
        ]

        check_rows = VGroup()
        for x_val, power_val, is_in, power_tex, reason_tex in checks_data:
            if is_in:
                mark = r"\; \checkmark"
                color = ANSWER_COLOR
            else:
                mark = r"\; \times"
                color = AUX_COLOR

            row = MathTex(
                r"x = " + str(x_val) + r": \quad " + power_tex
                + r" \quad \to \quad " + reason_tex + mark,
                font_size=BODY_SIZE, color=color,
            )
            check_rows.add(row)

        check_rows.arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        check_rows.next_to(approach, DOWN, buff=0.4)

        # Reveal one by one
        for row in check_rows:
            self.play(FadeIn(row, shift=RIGHT * 0.3), run_time=0.6)
            self.wait(0.8)

        self.wait(W_AFTER_KEY)

        # Step 4: Conclusion
        self.play(
            FadeOut(step1_title), FadeOut(condition), FadeOut(approach),
            check_rows.animate.move_to(UP * 1.5),
            run_time=T_TRANSITION,
        )
        self.wait(0.5)

        # Show B and |B|
        result_b = MathTex(
            r"B = \{ 2, \, 3, \, 4 \}",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        result_b.next_to(check_rows, DOWN, buff=0.6)

        card_b = MathTex(
            r"|B| = 3",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        card_b.next_to(result_b, DOWN, buff=0.4)

        self.play(Write(result_b), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)
        self.play(Write(card_b), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        # Answer box around |B| = 3
        answer_group = VGroup(result_b, card_b)
        box = make_answer_box(answer_group)
        self.play(Create(box), run_time=0.4)

        # Show the correct option
        answer_c = MathTex(
            r"\text{Përgjigja: C) 3}",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        answer_c.next_to(box, DOWN, buff=0.5)
        self.play(GrowFromCenter(answer_c), run_time=0.8)

        self.play(
            Flash(answer_c.get_center(), color=ANSWER_COLOR,
                  line_length=0.2, num_lines=12, run_time=0.6),
        )
        self.play(
            Circumscribe(answer_c, color=HIGHLIGHT_COLOR, run_time=0.8),
        )
        self.wait(W_AFTER_ANSWER)

        # Clean up
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=T_TRANSITION)
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
