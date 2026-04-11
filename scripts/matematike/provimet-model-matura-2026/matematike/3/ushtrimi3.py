"""
YouTube Video — Ushtrimi 3, Matematikë
Provimet Model Matura 2026

log x / log 0,1 = 2  (x > 0)
Gjej x.  Përgjigja: C) 0,01
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


class Ushtrimi3(Scene):
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
            r"\text{Ushtrimi 3 — Matematikë}",
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
        problem_text = MathTex(
            r"\text{Herësi i } \log x \; (x > 0) \text{ me } \log 0{,}1 \text{ është 2.}",
            font_size=CALC_SIZE, color=WHITE,
        )
        question = MathTex(
            r"\text{Gjej } x \text{.}",
            font_size=CALC_SIZE, color=HIGHLIGHT_COLOR,
        )

        stmt = VGroup(problem_text, question).arrange(DOWN, buff=0.45)
        stmt.move_to(UP * 1.2)

        self.play(Write(problem_text), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)
        self.play(FadeIn(question, shift=UP * 0.2), run_time=T_BODY_FADE)
        self.wait(0.8)

        # Multiple choice options
        opt_a = MathTex(r"\text{A) } 100", font_size=BODY_SIZE, color=WHITE)
        opt_b = MathTex(r"\text{B) } 0{,}1", font_size=BODY_SIZE, color=WHITE)
        opt_c = MathTex(r"\text{C) } 0{,}01", font_size=BODY_SIZE, color=WHITE)
        opt_d = MathTex(r"\text{D) } {-2}", font_size=BODY_SIZE, color=WHITE)

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

        self.problem_group = VGroup(problem_text, question, opts)
        self.play(FadeOut(self.problem_group), run_time=T_TRANSITION)
        self.wait(0.3)

    # ────────────────────────────────────────────
    #  SOLVE
    # ────────────────────────────────────────────

    def solve(self):
        # ── Step 1: Write the equation ──────────────────
        step1_title = MathTex(
            r"\text{Shkruajmë ekuacionin:}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        step1_title.to_edge(UP, buff=0.6)

        eq1 = MathTex(
            r"\frac{\log x}{\log 0{,}1} = 2",
            font_size=CALC_SIZE, color=WHITE,
        )
        eq1.next_to(step1_title, DOWN, buff=0.5)

        self.play(Write(step1_title), run_time=T_STEP_TITLE)
        self.play(Write(eq1), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_KEY)

        # ── Step 2: Simplify log 0,1 ────────────────────
        step2_title = MathTex(
            r"\text{Thjeshtojmë } \log 0{,}1 \text{:}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        step2_title.next_to(eq1, DOWN, buff=0.5)

        eq2a = MathTex(
            r"\log 0{,}1 = \log 10^{-1}",
            font_size=CALC_SIZE, color=WHITE,
        )
        eq2a.next_to(step2_title, DOWN, buff=0.4)

        eq2b = MathTex(
            r"\log 10^{-1} = -1",
            font_size=CALC_SIZE, color=LABEL_COLOR,
        )
        eq2b.next_to(eq2a, DOWN, buff=0.35)

        self.play(Write(step2_title), run_time=T_STEP_TITLE)
        self.play(Write(eq2a), run_time=T_ROUTINE_EQUATION)
        self.wait(W_AFTER_ROUTINE)
        self.play(Write(eq2b), run_time=T_ROUTINE_EQUATION)
        self.wait(W_AFTER_KEY)

        # Clean up steps 1-2 and move on
        self.play(
            FadeOut(step1_title), FadeOut(eq1),
            FadeOut(step2_title), FadeOut(eq2a), FadeOut(eq2b),
            run_time=T_TRANSITION,
        )
        self.wait(0.3)

        # ── Step 3: Substitute and solve for log x ──────
        step3_title = MathTex(
            r"\text{Zëvendësojmë:}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        step3_title.to_edge(UP, buff=0.6)

        eq3a = MathTex(
            r"\frac{\log x}{-1} = 2",
            font_size=CALC_SIZE, color=WHITE,
        )
        eq3a.next_to(step3_title, DOWN, buff=0.5)

        eq3b = MathTex(
            r"\log x = 2 \cdot (-1)",
            font_size=CALC_SIZE, color=WHITE,
        )
        eq3b.next_to(eq3a, DOWN, buff=0.4)

        eq3c = MathTex(
            r"\log x = -2",
            font_size=CALC_SIZE, color=LABEL_COLOR,
        )
        eq3c.next_to(eq3b, DOWN, buff=0.4)

        self.play(Write(step3_title), run_time=T_STEP_TITLE)
        self.play(Write(eq3a), run_time=T_ROUTINE_EQUATION)
        self.wait(W_AFTER_ROUTINE)
        self.play(Write(eq3b), run_time=T_ROUTINE_EQUATION)
        self.wait(W_AFTER_ROUTINE)
        self.play(Write(eq3c), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_KEY)

        # ── Step 4: Definition of logarithm → find x ────
        step4_title = MathTex(
            r"\text{Përkufizimi i logaritmit:}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        step4_title.next_to(eq3c, DOWN, buff=0.5)

        eq4a = MathTex(
            r"x = 10^{-2}",
            font_size=CALC_SIZE, color=WHITE,
        )
        eq4a.next_to(step4_title, DOWN, buff=0.4)

        eq4b = MathTex(
            r"x = 0{,}01",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        eq4b.next_to(eq4a, DOWN, buff=0.4)

        self.play(Write(step4_title), run_time=T_STEP_TITLE)
        self.play(Write(eq4a), run_time=T_ROUTINE_EQUATION)
        self.wait(W_AFTER_ROUTINE)
        self.play(Write(eq4b), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        # ── Answer box + correct option ──────────────────
        box = make_answer_box(eq4b)
        self.play(Create(box), run_time=0.4)

        answer_c = MathTex(
            r"\text{Përgjigja: C) } 0{,}01",
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
