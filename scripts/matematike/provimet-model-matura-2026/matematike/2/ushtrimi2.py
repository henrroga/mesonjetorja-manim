"""
YouTube Video — Ushtrimi 2, Matematikë
Provimet Model Matura 2026

Nëse 5% e numrit n është 22, vlera e n është:
A) 1000  B) 440  C) 400  D) 40
Përgjigja: B) 440
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


class Ushtrimi2(Scene):
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
            r"\text{Ushtrimi 2 — Matematikë}",
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
        question = MathTex(
            r"\text{Nëse 5\% e numrit } n \text{ është 22,}",
            font_size=CALC_SIZE, color=WHITE,
        )
        question2 = MathTex(
            r"\text{vlera e } n \text{ është:}",
            font_size=CALC_SIZE, color=HIGHLIGHT_COLOR,
        )

        q_group = VGroup(question, question2).arrange(DOWN, buff=0.35)
        q_group.move_to(UP * 1.2)

        self.play(Write(question), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)
        self.play(FadeIn(question2, shift=UP * 0.2), run_time=T_BODY_FADE)
        self.wait(0.8)

        # Multiple choice options
        opt_a = MathTex(r"\text{A) } 1000", font_size=BODY_SIZE, color=WHITE)
        opt_b = MathTex(r"\text{B) } 440", font_size=BODY_SIZE, color=WHITE)
        opt_c = MathTex(r"\text{C) } 400", font_size=BODY_SIZE, color=WHITE)
        opt_d = MathTex(r"\text{D) } 40", font_size=BODY_SIZE, color=WHITE)

        opts = VGroup(opt_a, opt_b, opt_c, opt_d).arrange(RIGHT, buff=0.8)
        opts.next_to(q_group, DOWN, buff=0.6)

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
        self.problem_group = VGroup(question, question2, opts)
        self.play(FadeOut(self.problem_group), run_time=T_TRANSITION)
        self.wait(0.3)

    # ────────────────────────────────────────────
    #  SOLVE
    # ────────────────────────────────────────────

    def solve(self):
        # Step 1: Convert percentage to decimal
        step1_title = MathTex(
            r"\text{Shprehim 5\% si numër dhjetor:}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        step1_title.to_edge(UP, buff=0.6)

        pct_eq = MathTex(
            r"5\% = \frac{5}{100} = 0{,}05",
            font_size=CALC_SIZE, color=WHITE,
        )
        pct_eq.next_to(step1_title, DOWN, buff=0.5)

        self.play(Write(step1_title), run_time=T_STEP_TITLE)
        self.play(Write(pct_eq), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_KEY)

        # Step 2: Set up the equation
        step2_title = MathTex(
            r"\text{Ndërtojmë ekuacionin:}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        step2_title.next_to(pct_eq, DOWN, buff=0.5)

        equation = MathTex(
            r"0{,}05 \cdot n = 22",
            font_size=CALC_SIZE, color=WHITE,
        )
        equation.next_to(step2_title, DOWN, buff=0.4)

        self.play(Write(step2_title), run_time=T_STEP_TITLE)
        self.play(Write(equation), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_KEY)

        # Clean up steps 1-2, move equation to top
        self.play(
            FadeOut(step1_title), FadeOut(pct_eq), FadeOut(step2_title),
            equation.animate.to_edge(UP, buff=0.6),
            run_time=T_TRANSITION,
        )
        self.wait(0.3)

        # Step 3: Isolate n
        step3_title = MathTex(
            r"\text{Izolojmë } n \text{:}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        step3_title.next_to(equation, DOWN, buff=0.5)

        isolate = MathTex(
            r"n = \frac{22}{0{,}05}",
            font_size=CALC_SIZE, color=WHITE,
        )
        isolate.next_to(step3_title, DOWN, buff=0.4)

        self.play(Write(step3_title), run_time=T_STEP_TITLE)
        self.play(Write(isolate), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_KEY)

        # Step 4: Compute the result
        step4_title = MathTex(
            r"\text{Llogarisim:}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        step4_title.next_to(isolate, DOWN, buff=0.5)

        compute = MathTex(
            r"n = \frac{2200}{5} = 440",
            font_size=CALC_SIZE, color=ANSWER_COLOR,
        )
        compute.next_to(step4_title, DOWN, buff=0.4)

        self.play(Write(step4_title), run_time=T_STEP_TITLE)
        self.play(Write(compute), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        # Highlight the result
        box = make_answer_box(compute)
        self.play(Create(box), run_time=0.4)

        # Show correct option
        answer_b = MathTex(
            r"\text{Përgjigja: B) 440}",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        answer_b.next_to(box, DOWN, buff=0.5)
        self.play(GrowFromCenter(answer_b), run_time=0.8)

        self.play(
            Flash(answer_b.get_center(), color=ANSWER_COLOR,
                  line_length=0.2, num_lines=12, run_time=0.6),
        )
        self.play(
            Circumscribe(answer_b, color=HIGHLIGHT_COLOR, run_time=0.8),
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
