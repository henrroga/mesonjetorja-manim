"""
YouTube Video — Ushtrimi 21.16, Kapitulli 21
Fizika 10-11: Pjesa e Dytë (Botime Pegi)

Transformatori: Vp = 230V, Vs = 6,0V, Np = 6000
a) Ns = ?  → ≈ 157 mbështjella
b) Is = ?  (Ip = 0,040A) → ≈ 1,53 A
c) Supozimi: transformator ideal (pa humbje energjie)
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


class Ushtrimi21_16(Scene):
    def construct(self):
        apply_style(self)
        MathTex.set_default(tex_template=ALBANIAN_TEX)
        Tex.set_default(tex_template=ALBANIAN_TEX)

        self.title_screen()
        self.part_a()
        self.part_b()
        self.part_c()
        self.final_summary()
        self.end_screen()

    # ────────────────────────────────────────────
    #  TITLE SCREEN
    # ────────────────────────────────────────────

    def title_screen(self):
        title = MathTex(
            r"\text{Ushtrimi 21.16 — Kapitulli 21}",
            font_size=TITLE_SIZE, color=WHITE,
        )
        source = MathTex(
            r"\text{Fizika 10-11: Pjesa e Dytë}",
            font_size=SUBTITLE_SIZE, color=BODY_TEXT_COLOR,
        )
        source.next_to(title, DOWN, buff=0.4)

        self.play(Write(title), run_time=T_TITLE_WRITE)
        self.play(FadeIn(source, shift=UP * 0.2), run_time=T_SUBTITLE_FADE)
        self.wait(W_AFTER_KEY)
        self.play(FadeOut(title), FadeOut(source))
        self.wait(0.5)

    # ────────────────────────────────────────────
    #  SHOW GIVEN DATA
    # ────────────────────────────────────────────

    def _show_given(self):
        """Show the known values centered, return the group."""
        header = MathTex(
            r"\text{Të dhënat:}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        vp = MathTex(
            r"V_p = 230 \text{ V}",
            font_size=CALC_SIZE, color=SHAPE_COLOR,
        )
        vs = MathTex(
            r"V_s = 6{,}0 \text{ V}",
            font_size=CALC_SIZE, color=AUX_COLOR,
        )
        np_val = MathTex(
            r"N_p = 6000",
            font_size=CALC_SIZE, color=SHAPE_COLOR,
        )

        group = VGroup(header, vp, vs, np_val).arrange(DOWN, buff=0.35)
        group.move_to(UP * 1.5)

        self.play(Write(header), run_time=T_STEP_TITLE)
        self.play(
            LaggedStart(
                Write(vp), Write(vs), Write(np_val),
                lag_ratio=0.3,
            ),
            run_time=1.2,
        )
        self.wait(W_AFTER_KEY)
        return group

    # ────────────────────────────────────────────
    #  PART A — Number of turns in secondary
    # ────────────────────────────────────────────

    def part_a(self):
        # Part header
        part_hdr = MathTex(
            r"\text{a) Sa mbështjella ka dytësori?}",
            font_size=PART_HEADER_SIZE, color=HIGHLIGHT_COLOR,
        )
        part_hdr.to_edge(UP, buff=0.6)
        self.play(Write(part_hdr), run_time=T_STEP_TITLE)
        self.wait(0.8)

        # Show the transformer ratio formula centered
        why = MathTex(
            r"\text{Formula e transformatorit:}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        why.next_to(part_hdr, DOWN, buff=0.5)

        formula = MathTex(
            r"\frac{V_p}{V_s} = \frac{N_p}{N_s}",
            font_size=CALC_SIZE, color=WHITE,
        )
        formula.next_to(why, DOWN, buff=0.4)

        self.play(FadeIn(why, shift=UP * 0.2), run_time=T_BODY_FADE)
        self.play(Write(formula), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_KEY)

        # Rearrange for Ns
        rearrange_why = MathTex(
            r"\text{Izolojmë } N_s \text{:}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        rearrange_why.next_to(formula, DOWN, buff=0.5)

        rearranged = MathTex(
            r"N_s = N_p \times \frac{V_s}{V_p}",
            font_size=CALC_SIZE, color=WHITE,
        )
        rearranged.next_to(rearrange_why, DOWN, buff=0.4)

        self.play(FadeIn(rearrange_why, shift=UP * 0.2), run_time=T_BODY_FADE)
        self.play(Write(rearranged), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        # Clean up top, keep rearranged
        self.play(
            FadeOut(part_hdr), FadeOut(why), FadeOut(formula),
            FadeOut(rearrange_why),
            rearranged.animate.to_edge(UP, buff=0.6),
            run_time=T_TRANSITION,
        )
        self.wait(0.3)

        # Substitute values
        sub_why = MathTex(
            r"\text{Zëvendësojmë vlerat:}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        sub_why.next_to(rearranged, DOWN, buff=0.5)

        substituted = MathTex(
            r"N_s = 6000 \times \frac{6{,}0}{230}",
            font_size=CALC_SIZE, color=WHITE,
        )
        substituted.next_to(sub_why, DOWN, buff=0.4)

        self.play(FadeIn(sub_why, shift=UP * 0.2), run_time=T_BODY_FADE)
        self.play(Write(substituted), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        # Compute step by step
        compute1 = MathTex(
            r"N_s = 6000 \times 0{,}02609",
            font_size=CALC_SIZE, color=WHITE,
        )
        compute1.next_to(substituted, DOWN, buff=0.4)
        self.play(Write(compute1), run_time=T_ROUTINE_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        # Final result
        result = MathTex(
            r"N_s \approx 157 \text{ mbështjella}",
            font_size=CALC_SIZE, color=ANSWER_COLOR,
        )
        result.next_to(compute1, DOWN, buff=0.4)
        self.play(Write(result), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        # Box the answer
        box = make_answer_box(result)
        self.play(Create(box), run_time=0.4)
        self.play(
            Circumscribe(result, color=HIGHLIGHT_COLOR, run_time=0.8),
        )
        self.wait(W_AFTER_KEY)

        # Clean up
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=T_TRANSITION)
        self.wait(0.3)

    # ────────────────────────────────────────────
    #  PART B — Secondary current
    # ────────────────────────────────────────────

    def part_b(self):
        # Part header
        part_hdr = MathTex(
            r"\text{b) Sa është rryma në dytësor?}",
            font_size=PART_HEADER_SIZE, color=HIGHLIGHT_COLOR,
        )
        part_hdr.to_edge(UP, buff=0.6)
        self.play(Write(part_hdr), run_time=T_STEP_TITLE)
        self.wait(0.5)

        # Given: Ip
        given = MathTex(
            r"I_p = 0{,}040 \text{ A}",
            font_size=CALC_SIZE, color=SHAPE_COLOR,
        )
        given.next_to(part_hdr, DOWN, buff=0.5)
        self.play(Write(given), run_time=T_ROUTINE_EQUATION)
        self.wait(0.8)

        # Power conservation principle
        why = MathTex(
            r"\text{Ruajtja e fuqisë (transformator ideal):}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        why.next_to(given, DOWN, buff=0.5)

        formula = MathTex(
            r"V_p \cdot I_p = V_s \cdot I_s",
            font_size=CALC_SIZE, color=WHITE,
        )
        formula.next_to(why, DOWN, buff=0.4)

        self.play(FadeIn(why, shift=UP * 0.2), run_time=T_BODY_FADE)
        self.play(Write(formula), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_KEY)

        # Rearrange for Is
        rearrange_why = MathTex(
            r"\text{Izolojmë } I_s \text{:}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        rearrange_why.next_to(formula, DOWN, buff=0.5)

        rearranged = MathTex(
            r"I_s = \frac{V_p \cdot I_p}{V_s}",
            font_size=CALC_SIZE, color=WHITE,
        )
        rearranged.next_to(rearrange_why, DOWN, buff=0.4)

        self.play(FadeIn(rearrange_why, shift=UP * 0.2), run_time=T_BODY_FADE)
        self.play(Write(rearranged), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        # Clean up, keep rearranged
        self.play(
            FadeOut(part_hdr), FadeOut(given), FadeOut(why),
            FadeOut(formula), FadeOut(rearrange_why),
            rearranged.animate.to_edge(UP, buff=0.6),
            run_time=T_TRANSITION,
        )
        self.wait(0.3)

        # Substitute
        sub_why = MathTex(
            r"\text{Zëvendësojmë vlerat:}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        sub_why.next_to(rearranged, DOWN, buff=0.5)

        substituted = MathTex(
            r"I_s = \frac{230 \times 0{,}040}{6{,}0}",
            font_size=CALC_SIZE, color=WHITE,
        )
        substituted.next_to(sub_why, DOWN, buff=0.4)

        self.play(FadeIn(sub_why, shift=UP * 0.2), run_time=T_BODY_FADE)
        self.play(Write(substituted), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        # Compute numerator
        compute1 = MathTex(
            r"I_s = \frac{9{,}2}{6{,}0}",
            font_size=CALC_SIZE, color=WHITE,
        )
        compute1.next_to(substituted, DOWN, buff=0.4)
        self.play(Write(compute1), run_time=T_ROUTINE_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        # Final result
        result = MathTex(
            r"I_s \approx 1{,}53 \text{ A}",
            font_size=CALC_SIZE, color=ANSWER_COLOR,
        )
        result.next_to(compute1, DOWN, buff=0.4)
        self.play(Write(result), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        # Box the answer
        box = make_answer_box(result)
        self.play(Create(box), run_time=0.4)
        self.play(
            Circumscribe(result, color=HIGHLIGHT_COLOR, run_time=0.8),
        )
        self.wait(W_AFTER_KEY)

        # Clean up
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=T_TRANSITION)
        self.wait(0.3)

    # ────────────────────────────────────────────
    #  PART C — Assumption
    # ────────────────────────────────────────────

    def part_c(self):
        # Part header
        part_hdr = MathTex(
            r"\text{c) Cili supozim u bë në pikën b)?}",
            font_size=PART_HEADER_SIZE, color=HIGHLIGHT_COLOR,
        )
        part_hdr.to_edge(UP, buff=0.8)
        self.play(Write(part_hdr), run_time=T_STEP_TITLE)
        self.wait(1.0)

        # Explanation
        explain1 = MathTex(
            r"\text{Përdorëm formulën } V_p I_p = V_s I_s",
            font_size=CALC_SIZE, color=WHITE,
        )
        explain1.next_to(part_hdr, DOWN, buff=0.6)

        explain2 = MathTex(
            r"\text{Kjo do të thotë:}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        explain2.next_to(explain1, DOWN, buff=0.5)

        power_eq = MathTex(
            r"P_{\text{hyrëse}} = P_{\text{dalëse}}",
            font_size=CALC_SIZE, color=WHITE,
        )
        power_eq.next_to(explain2, DOWN, buff=0.4)

        self.play(Write(explain1), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)
        self.play(FadeIn(explain2, shift=UP * 0.2), run_time=T_BODY_FADE)
        self.play(Write(power_eq), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_KEY)

        # The assumption
        assumption = MathTex(
            r"\text{Supozimi: Transformatori është ideal}",
            font_size=CALC_SIZE, color=ANSWER_COLOR,
        )
        assumption.next_to(power_eq, DOWN, buff=0.6)

        detail = MathTex(
            r"\text{(100\% efikasitet — pa humbje energjie)}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        detail.next_to(assumption, DOWN, buff=0.3)

        self.play(Write(assumption), run_time=T_KEY_EQUATION)
        self.play(FadeIn(detail, shift=UP * 0.2), run_time=T_BODY_FADE)
        self.wait(W_AFTER_ROUTINE)

        # Box the assumption
        ans_group = VGroup(assumption, detail)
        box = make_answer_box(ans_group)
        self.play(Create(box), run_time=0.4)
        self.play(
            Circumscribe(ans_group, color=HIGHLIGHT_COLOR, run_time=0.8),
        )
        self.wait(W_AFTER_KEY)

        # Clean up
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=T_TRANSITION)
        self.wait(0.3)

    # ────────────────────────────────────────────
    #  FINAL SUMMARY
    # ────────────────────────────────────────────

    def final_summary(self):
        title = MathTex(
            r"\text{Përmbledhje e përgjigjeve}",
            font_size=PART_HEADER_SIZE, color=STEP_TITLE_COLOR,
        )
        title.to_edge(UP, buff=0.8)

        ans_a = MathTex(
            r"\text{a) } N_s \approx 157 \text{ mbështjella}",
            font_size=CALC_SIZE, color=ANSWER_COLOR,
        )
        ans_b = MathTex(
            r"\text{b) } I_s \approx 1{,}53 \text{ A}",
            font_size=CALC_SIZE, color=ANSWER_COLOR,
        )
        ans_c = MathTex(
            r"\text{c) Transformator ideal (pa humbje)}",
            font_size=CALC_SIZE, color=ANSWER_COLOR,
        )

        answers = VGroup(ans_a, ans_b, ans_c).arrange(DOWN, buff=0.5)
        answers.move_to(ORIGIN)

        box = make_answer_box(answers)

        self.play(Write(title), run_time=T_STEP_TITLE)
        self.play(
            LaggedStart(
                Write(ans_a), Write(ans_b), Write(ans_c),
                lag_ratio=0.4,
            ),
            run_time=2.0,
        )
        self.wait(W_AFTER_ROUTINE)
        self.play(Create(box), run_time=0.4)
        self.play(
            Flash(answers.get_center(), color=ANSWER_COLOR,
                  line_length=0.3, num_lines=16, run_time=0.8),
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
