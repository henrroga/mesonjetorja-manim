"""
YouTube Video — Ushtrimi 2, Njësia 4.8A
Matematika 12 (Pegi)

Gjeni syprinat e kufizuara nga drejtëzat/kthesa duke përdorur integralin e caktuar.

a) y=x, y=0, x=1, x=2         → S = 3/2 = 1,5
b) y=-x, y=0, x=-1, x=-2      → S = 3/2 = 1,5
c) y=2x+1, y=0, x=2, x=3      → S = 6
d) y=x²+2, y=0, x=0, x=3      → S = 15
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))

from manim import *
import numpy as np
from style_guide import (
    apply_style, make_answer_box, make_divider,
    BG_COLOR, STEP_TITLE_COLOR, BODY_TEXT_COLOR, LABEL_COLOR,
    ANSWER_COLOR, SHAPE_COLOR, AUX_COLOR, HIGHLIGHT_COLOR, DIVIDER_COLOR,
    TITLE_SIZE, SUBTITLE_SIZE, PART_HEADER_SIZE, STEP_TITLE_SIZE,
    BODY_SIZE, CALC_SIZE, ANSWER_SIZE,
    T_TITLE_WRITE, T_SUBTITLE_FADE, T_STEP_TITLE,
    T_BODY_FADE, T_KEY_EQUATION, T_ROUTINE_EQUATION,
    T_SHAPE_CREATE, T_TRANSITION,
    W_AFTER_KEY, W_AFTER_ROUTINE, W_AFTER_ANSWER,
    PX, ALBANIAN_TEX,
)


class Ushtrimi2(Scene):
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
        self.final_summary()
        self.end_screen()

    # ────────────────────────────────────────────
    #  TITLE SCREEN
    # ────────────────────────────────────────────

    def title_screen(self):
        title = MathTex(
            r"\text{Ushtrimi 2 — Njësia 4.8A}",
            font_size=TITLE_SIZE, color=WHITE,
        )
        source = MathTex(
            r"\text{Matematika 12}",
            font_size=SUBTITLE_SIZE, color=BODY_TEXT_COLOR,
        )
        source.next_to(title, DOWN, buff=0.4)

        self.play(Write(title), run_time=T_TITLE_WRITE)
        self.play(FadeIn(source, shift=UP * 0.2), run_time=T_SUBTITLE_FADE)
        self.wait(W_AFTER_KEY)
        self.play(FadeOut(title), FadeOut(source))
        self.wait(0.5)

    # ────────────────────────────────────────────
    #  SHOW AREA FORMULA
    # ────────────────────────────────────────────

    def show_formula(self):
        heading = MathTex(
            r"\text{Syprina e zonës së kufizuar:}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        formula = MathTex(
            r"S = \int_a^b f(x) \, dx",
            font_size=ANSWER_SIZE, color=WHITE,
        )
        explanation = MathTex(
            r"\text{ku } f(x) \geq 0 \text{ në } [a, b]",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )

        group = VGroup(heading, formula, explanation).arrange(DOWN, buff=0.6)
        group.move_to(ORIGIN)

        self.play(Write(heading), run_time=T_STEP_TITLE)
        self.play(Write(formula), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)
        self.play(FadeIn(explanation, shift=UP * 0.15), run_time=T_BODY_FADE)
        self.wait(W_AFTER_KEY)

        self.play(FadeOut(group))
        self.wait(0.3)

    # ────────────────────────────────────────────
    #  HELPER: SOLVE ONE PART
    # ────────────────────────────────────────────

    def _solve_part(
        self,
        label,              # "a", "b", "c", "d"
        func,               # python lambda for plotting
        func_tex,           # LaTeX of function e.g. r"y = x"
        x_ax_range,         # [x_min, x_max, step] for Axes
        y_ax_range,         # [y_min, y_max, step] for Axes
        plot_x_range,       # [x_min, x_max] for axes.plot
        shade_x_range,      # [x_min, x_max] for get_area
        integral_tex,       # e.g. r"S = \int_1^2 x \, dx"
        antideriv_tex,      # e.g. r"= \left[ \frac{x^2}{2} \right]_1^2"
        sub_tex,            # e.g. r"= \frac{4}{2} - \frac{1}{2}"
        simplify_tex,       # e.g. r"= 2 - \frac{1}{2}"  or None
        answer_tex,         # e.g. r"= \frac{3}{2} = 1{,}5"
        answer_boxed_tex,   # e.g. r"S = \frac{3}{2} = 1{,}5"
        bound_lines=None,   # list of (x_val, y_max_val) for vertical dashed bound lines
    ):
        # --- Part header ---
        header = MathTex(
            r"\text{Pjesa " + label + r")}",
            font_size=PART_HEADER_SIZE, color=STEP_TITLE_COLOR,
        )
        header.to_edge(UP, buff=0.4)
        self.play(Write(header), run_time=T_STEP_TITLE)

        # --- Build graph centered on screen first ---
        axes = Axes(
            x_range=x_ax_range,
            y_range=y_ax_range,
            x_length=4.0,
            y_length=3.0,
            axis_config={
                "include_numbers": True,
                "font_size": 16,
                "color": DIVIDER_COLOR,
                "include_ticks": True,
            },
        )

        # Function label
        func_label = MathTex(func_tex, font_size=BODY_SIZE, color=SHAPE_COLOR)

        # Plot the function
        graph = axes.plot(func, x_range=plot_x_range, color=SHAPE_COLOR, stroke_width=2.5)

        # Shaded area
        area = axes.get_area(
            graph,
            x_range=shade_x_range,
            color=SHAPE_COLOR,
            opacity=0.3,
        )

        # Vertical dashed boundary lines
        bound_group = VGroup()
        if bound_lines:
            for x_val, y_max_val in bound_lines:
                dashed = DashedLine(
                    axes.c2p(x_val, 0),
                    axes.c2p(x_val, y_max_val),
                    color=DIVIDER_COLOR,
                    stroke_width=1.5,
                    dash_length=0.08,
                )
                bound_group.add(dashed)

        # Position the graph group centered
        graph_group = VGroup(axes, graph, area, bound_group)
        func_label.next_to(axes, UP, buff=0.2).align_to(axes, RIGHT)

        full_graph = VGroup(graph_group, func_label)
        full_graph.next_to(header, DOWN, buff=0.5)
        full_graph.set_x(0)

        # --- Animate graph appearance ---
        self.play(Create(axes), run_time=0.8)
        self.play(Create(graph), run_time=T_SHAPE_CREATE)
        self.play(FadeIn(func_label, shift=DOWN * 0.1), run_time=0.4)

        if bound_lines:
            self.play(
                *[Create(bl) for bl in bound_group],
                run_time=0.6,
            )

        self.play(FadeIn(area), run_time=0.8)
        self.wait(W_AFTER_ROUTINE)

        # --- Shift graph left, add divider, show calculation on right ---
        divider = make_divider()

        self.play(
            full_graph.animate.scale(0.85).set_x(-3.5),
            FadeIn(divider),
            run_time=0.8,
        )

        # --- Calculation on right panel ---
        # Integral setup
        eq_integral = MathTex(integral_tex, font_size=CALC_SIZE, color=WHITE)
        eq_integral.move_to(UP * 2.2)
        eq_integral.set_x(PX)
        self.play(Write(eq_integral), run_time=T_KEY_EQUATION)
        self.wait(0.8)

        # Antiderivative
        eq_antideriv = MathTex(antideriv_tex, font_size=CALC_SIZE, color=WHITE)
        eq_antideriv.next_to(eq_integral, DOWN, buff=0.35)
        eq_antideriv.set_x(PX)
        self.play(Write(eq_antideriv), run_time=T_KEY_EQUATION)
        self.wait(0.8)

        # Substitution
        eq_sub = MathTex(sub_tex, font_size=CALC_SIZE, color=WHITE)
        eq_sub.next_to(eq_antideriv, DOWN, buff=0.35)
        eq_sub.set_x(PX)
        self.play(Write(eq_sub), run_time=T_ROUTINE_EQUATION)
        self.wait(0.6)

        # Simplification (optional extra step)
        last_eq = eq_sub
        if simplify_tex:
            eq_simplify = MathTex(simplify_tex, font_size=CALC_SIZE, color=WHITE)
            eq_simplify.next_to(eq_sub, DOWN, buff=0.35)
            eq_simplify.set_x(PX)
            self.play(Write(eq_simplify), run_time=T_ROUTINE_EQUATION)
            self.wait(0.6)
            last_eq = eq_simplify

        # Answer
        eq_answer = MathTex(answer_tex, font_size=CALC_SIZE, color=ANSWER_COLOR)
        eq_answer.next_to(last_eq, DOWN, buff=0.35)
        eq_answer.set_x(PX)
        self.play(Write(eq_answer), run_time=T_KEY_EQUATION)
        self.wait(0.8)

        # Boxed answer
        answer_boxed = MathTex(answer_boxed_tex, font_size=ANSWER_SIZE, color=ANSWER_COLOR)
        answer_boxed.next_to(eq_answer, DOWN, buff=0.45)
        answer_boxed.set_x(PX)

        box = make_answer_box(answer_boxed)
        self.play(GrowFromCenter(answer_boxed), run_time=0.6)
        self.play(Create(box), run_time=0.4)
        self.play(Circumscribe(answer_boxed, color=HIGHLIGHT_COLOR, run_time=0.8))
        self.wait(W_AFTER_KEY)

        # --- Clean up ---
        all_items = VGroup(header, full_graph, divider)
        calc_items = VGroup(eq_integral, eq_antideriv, eq_sub, eq_answer, answer_boxed, box)
        if simplify_tex:
            calc_items.add(eq_simplify)
        all_items.add(calc_items)

        self.play(FadeOut(all_items), run_time=T_TRANSITION)
        self.wait(0.3)

    # ────────────────────────────────────────────
    #  PART A: y=x, y=0, x=1, x=2  →  S = 3/2
    # ────────────────────────────────────────────

    def part_a(self):
        self._solve_part(
            label="a",
            func=lambda x: x,
            func_tex=r"y = x",
            x_ax_range=[-0.5, 3, 1],
            y_ax_range=[-0.5, 3, 1],
            plot_x_range=[0, 2.8],
            shade_x_range=[1, 2],
            integral_tex=r"S = \int_1^2 x \, dx",
            antideriv_tex=r"= \left[ \frac{x^2}{2} \right]_1^2",
            sub_tex=r"= \frac{2^2}{2} - \frac{1^2}{2}",
            simplify_tex=r"= \frac{4}{2} - \frac{1}{2}",
            answer_tex=r"= \frac{3}{2} = 1{,}5",
            answer_boxed_tex=r"S = \frac{3}{2} = 1{,}5",
            bound_lines=[(1, 1), (2, 2)],
        )

    # ────────────────────────────────────────────
    #  PART B: y=-x, y=0, x=-1, x=-2  →  S = 3/2
    # ────────────────────────────────────────────

    def part_b(self):
        # Note: area is above x-axis because y=-x is positive for x<0
        # We integrate ∫₋₂⁻¹ (-x) dx
        self._solve_part(
            label="b",
            func=lambda x: -x,
            func_tex=r"y = -x",
            x_ax_range=[-3, 0.5, 1],
            y_ax_range=[-0.5, 3, 1],
            plot_x_range=[-2.8, 0],
            shade_x_range=[-2, -1],
            integral_tex=r"S = \int_{-2}^{-1} (-x) \, dx",
            antideriv_tex=r"= \left[ -\frac{x^2}{2} \right]_{-2}^{-1}",
            sub_tex=r"= -\frac{(-1)^2}{2} - \left(-\frac{(-2)^2}{2}\right)",
            simplify_tex=r"= -\frac{1}{2} + \frac{4}{2}",
            answer_tex=r"= \frac{3}{2} = 1{,}5",
            answer_boxed_tex=r"S = \frac{3}{2} = 1{,}5",
            bound_lines=[(-2, 2), (-1, 1)],
        )

    # ────────────────────────────────────────────
    #  PART C: y=2x+1, y=0, x=2, x=3  →  S = 6
    # ────────────────────────────────────────────

    def part_c(self):
        self._solve_part(
            label="c",
            func=lambda x: 2 * x + 1,
            func_tex=r"y = 2x + 1",
            x_ax_range=[-0.5, 4, 1],
            y_ax_range=[-0.5, 8, 2],
            plot_x_range=[0, 3.5],
            shade_x_range=[2, 3],
            integral_tex=r"S = \int_2^3 (2x + 1) \, dx",
            antideriv_tex=r"= \left[ x^2 + x \right]_2^3",
            sub_tex=r"= (3^2 + 3) - (2^2 + 2)",
            simplify_tex=r"= (9 + 3) - (4 + 2)",
            answer_tex=r"= 12 - 6 = 6",
            answer_boxed_tex=r"S = 6",
            bound_lines=[(2, 5), (3, 7)],
        )

    # ────────────────────────────────────────────
    #  PART D: y=x²+2, y=0, x=0, x=3  →  S = 15
    # ────────────────────────────────────────────

    def part_d(self):
        self._solve_part(
            label="d",
            func=lambda x: x**2 + 2,
            func_tex=r"y = x^2 + 2",
            x_ax_range=[-0.5, 4, 1],
            y_ax_range=[-0.5, 12, 2],
            plot_x_range=[-0.3, 3.5],
            shade_x_range=[0, 3],
            integral_tex=r"S = \int_0^3 (x^2 + 2) \, dx",
            antideriv_tex=r"= \left[ \frac{x^3}{3} + 2x \right]_0^3",
            sub_tex=r"= \left(\frac{3^3}{3} + 2 \cdot 3\right) - \left(\frac{0^3}{3} + 2 \cdot 0\right)",
            simplify_tex=r"= \left(\frac{27}{3} + 6\right) - 0",
            answer_tex=r"= 9 + 6 = 15",
            answer_boxed_tex=r"S = 15",
            bound_lines=[(0, 2), (3, 11)],
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
            r"\text{a)} \quad S = \frac{3}{2} = 1{,}5",
            r"\text{b)} \quad S = \frac{3}{2} = 1{,}5",
            r"\text{c)} \quad S = 6",
            r"\text{d)} \quad S = 15",
        ]

        rows = VGroup()
        for tex_str in answers_data:
            row = MathTex(tex_str, font_size=CALC_SIZE, color=ANSWER_COLOR)
            rows.add(row)

        rows.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        rows.next_to(heading, DOWN, buff=0.5)

        summary_group = VGroup(heading, rows)
        summary_group.move_to(ORIGIN)
        heading.to_edge(UP, buff=0.6)
        rows.next_to(heading, DOWN, buff=0.5)

        box = make_answer_box(rows)

        self.play(Write(heading), run_time=T_STEP_TITLE)
        self.wait(0.3)

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
