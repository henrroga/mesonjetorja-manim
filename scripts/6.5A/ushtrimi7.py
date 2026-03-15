import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from manim import *
import numpy as np
from components import ExerciseScene
from style_guide import (
    make_answer_box, fade_all,
    STEP_TITLE_COLOR, BODY_TEXT_COLOR, LABEL_COLOR,
    ANSWER_COLOR, SHAPE_COLOR, AUX_COLOR, HIGHLIGHT_COLOR, DIVIDER_COLOR,
    BODY_SIZE, CALC_SIZE, ANSWER_SIZE, STEP_TITLE_SIZE,
    T_STEP_TITLE, T_BODY_FADE, T_KEY_EQUATION, T_ROUTINE_EQUATION,
    T_SHAPE_CREATE, T_LAYOUT_SHIFT, T_TRANSITION,
    W_AFTER_KEY, W_AFTER_ROUTINE, W_AFTER_ANSWER, W_PROBLEM,
    CALC_TOP,
)


class Ushtrimi7(ExerciseScene):
    """
    Ushtrimi 7 — Njësia 6.5A
    Matematika 10-11: Pjesa II

    Tangjente ndaj rrethit x² + y² = 100 në pika të dhëna.
    """

    exercise_number = 7
    unit = "6.5A"
    parts = ["a", "b", "c"]

    def construct(self):
        from style_guide import apply_style
        apply_style(self)

        self.title_screen()

        # Extra intro step before parts
        self.intro_method()
        fade_all(self)
        self.wait(0.5)

        for part_name in self.parts:
            getattr(self, f"part_{part_name}")()
            fade_all(self)
            self.wait(0.5)

        self.final_summary()
        self.wait(W_AFTER_ANSWER)

    # ================================================================
    #  INTRO — explain the tangent method
    # ================================================================
    def intro_method(self):
        prob_title = Text("Problemi:", font_size=STEP_TITLE_SIZE + 2, color=STEP_TITLE_COLOR, weight=BOLD)
        prob_txt = Text(
            "Një rreth ka ekuacionin x² + y² = 100.\nShkruani ekuacionin e tangjentes në pikat\n(6,8), (8,6), (10,0).",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR, line_spacing=1.4,
        )
        VGroup(prob_title, prob_txt).arrange(DOWN, buff=0.4).move_to(UP * 1)

        self.play(FadeIn(prob_title), run_time=T_STEP_TITLE)
        self.play(FadeIn(prob_txt), run_time=T_BODY_FADE)
        self.wait(W_PROBLEM)

        # Method explanation
        m_title = Text("Metoda:", font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR, weight=BOLD)
        m_title.next_to(prob_txt, DOWN, buff=0.5)

        eqs = [
            MathTex(r"m_{\text{rreze}} = \frac{y_P - 0}{x_P - 0} = \frac{y_P}{x_P}", font_size=CALC_SIZE),
            MathTex(r"m_{\text{tang}} = -\frac{1}{m_{\text{rreze}}} = -\frac{x_P}{y_P}", font_size=CALC_SIZE, color=LABEL_COLOR),
        ]
        eqs[0].next_to(m_title, DOWN, buff=0.3)
        eqs[1].next_to(eqs[0], DOWN, buff=0.25)

        m3_txt = Text("sepse rrezja ⊥ tangjentes", font_size=BODY_SIZE, color=BODY_TEXT_COLOR)
        m3_txt.next_to(eqs[1], DOWN, buff=0.2)

        self.play(FadeIn(m_title), run_time=T_STEP_TITLE)
        self.play(Write(eqs[0]), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)
        self.play(Write(eqs[1]), run_time=T_KEY_EQUATION)
        self.play(FadeIn(m3_txt), run_time=T_BODY_FADE)
        self.wait(W_AFTER_KEY)

    # ================================================================
    #  HELPER: build tangent graph
    # ================================================================
    def _build_tangent_graph(self, point, tangent_func=None, tangent_range=None,
                              tangent_dashed=False, tangent_label=None):
        """Build circle graph with radius + tangent at a point."""
        axes = Axes(
            x_range=[-12, 14, 2], y_range=[-12, 14, 2],
            x_length=5.5, y_length=5.5,
            axis_config={"include_tip": True, "include_numbers": True,
                         "font_size": 16, "color": DIVIDER_COLOR},
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")
        circle = self.plot_circle(axes, 10)

        px, py = point
        radius = Line(axes.c2p(0, 0), axes.c2p(px, py),
                       color=HIGHLIGHT_COLOR, stroke_width=2.5)
        dot_p, lbl_p = self.mark_point(axes, px, py,
                                        f"({px},\\,{py})",
                                        color=LABEL_COLOR,
                                        direction=UR if py > 0 else DR)

        elements = [axes, axes_labels, circle, radius, dot_p, lbl_p]

        if tangent_dashed:
            tangent = DashedLine(
                axes.c2p(px, -11), axes.c2p(px, 11),
                color=AUX_COLOR, stroke_width=2.5, dash_length=0.1,
            )
            elements.append(tangent)
            if tangent_label:
                tang_lbl = MathTex(tangent_label, font_size=22, color=AUX_COLOR)
                tang_lbl.next_to(tangent, RIGHT, buff=0.15).shift(UP * 2)
                elements.append(tang_lbl)
        elif tangent_func:
            tangent = axes.plot(tangent_func, x_range=tangent_range or [-1, 13],
                                color=AUX_COLOR, stroke_width=2.5)
            elements.append(tangent)

        graph_group = VGroup(*elements)

        self.play(Create(axes), FadeIn(axes_labels), run_time=T_SHAPE_CREATE)
        self.play(Create(circle), run_time=T_SHAPE_CREATE * 0.8)
        self.play(Create(radius), FadeIn(dot_p), FadeIn(lbl_p), run_time=T_KEY_EQUATION)
        if tangent_dashed:
            extra = [FadeIn(e) for e in elements[6:]]
        else:
            extra = [Create(tangent)]
        self.play(*extra, run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        return graph_group

    # ================================================================
    #  PART A — tangent at (6, 8)
    # ================================================================
    def part_a(self):
        self.show_part_header("a) — Pika (6, 8)")

        graph_group = self._build_tangent_graph(
            point=(6, 8),
            tangent_func=lambda x: -0.75 * x + 12.5,
            tangent_range=[-1, 13],
        )

        div = self.setup_split_layout(graph_group)

        # Algebra
        s1 = Text("Koef. këndor i rrezes:", font_size=BODY_SIZE, color=BODY_TEXT_COLOR)
        s1.move_to(CALC_TOP)
        self.play(FadeIn(s1), run_time=T_STEP_TITLE)

        eq1 = self.show_equation(r"m = \frac{8}{6} = \frac{4}{3}", reference=s1)

        s2 = Text("Koef. këndor i tangjentes:", font_size=BODY_SIZE, color=BODY_TEXT_COLOR)
        s2.next_to(eq1, DOWN, buff=0.35)
        self.play(FadeIn(s2), run_time=T_STEP_TITLE)

        eq2 = self.show_equation(r"m' = -\frac{1}{\frac{4}{3}} = -\frac{3}{4}",
                                  reference=s2, color=LABEL_COLOR, key=True)

        s3 = Text("Gjejmë c (y = m'x + c):", font_size=BODY_SIZE, color=BODY_TEXT_COLOR)
        s3.next_to(eq2, DOWN, buff=0.35)
        self.play(FadeIn(s3), run_time=T_STEP_TITLE)

        eq3 = self.show_equation(r"8 = -\frac{3}{4} \cdot 6 + c", reference=s3)
        eq4 = self.show_equation(r"c = 8 + \frac{18}{4} = \frac{50}{4} = \frac{25}{2}", reference=eq3)
        self.wait(W_AFTER_ROUTINE)

        self.show_answer_below(r"y = -\frac{3}{4}x + \frac{25}{2}", eq4, buff=0.4)

    # ================================================================
    #  PART B — tangent at (8, 6)
    # ================================================================
    def part_b(self):
        self.show_part_header("b) — Pika (8, 6)")

        graph_group = self._build_tangent_graph(
            point=(8, 6),
            tangent_func=lambda x: -4 / 3 * x + 50 / 3,
            tangent_range=[-1, 13],
        )

        div = self.setup_split_layout(graph_group)

        eqs = self.show_equation_chain([
            r"m = \frac{6}{8} = \frac{3}{4}",
            {"tex": r"m' = -\frac{4}{3}", "color": LABEL_COLOR},
            {"tex": r"6 = -\frac{4}{3} \cdot 8 + c \;\Rightarrow\; c = \frac{50}{3}", "key": True},
        ], start_position=CALC_TOP)

        self.show_answer_below(r"y = -\frac{4}{3}x + \frac{50}{3}", eqs[-1])

    # ================================================================
    #  PART C — tangent at (10, 0) — vertical line
    # ================================================================
    def part_c(self):
        self.show_part_header("c) — Pika (10, 0)")

        graph_group = self._build_tangent_graph(
            point=(10, 0),
            tangent_dashed=True,
            tangent_label="x = 10",
        )

        div = self.setup_split_layout(graph_group)

        txt1 = Text("Rrezja shtrihet përgjatë boshtit Ox.", font_size=BODY_SIZE, color=BODY_TEXT_COLOR)
        txt1.move_to(CALC_TOP)
        txt2 = Text(
            "Tangjentja është pingulja e boshtit\nOx në pikën (10, 0).",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR, line_spacing=1.4,
        )
        txt2.next_to(txt1, DOWN, buff=0.3)

        self.play(FadeIn(txt1), run_time=T_BODY_FADE)
        self.wait(W_AFTER_ROUTINE)
        self.play(FadeIn(txt2), run_time=T_BODY_FADE)
        self.wait(W_AFTER_ROUTINE)

        self.show_answer_below(r"x = 10", txt2)

    # ================================================================
    #  FINAL SUMMARY
    # ================================================================
    def final_summary(self):
        self.show_summary_table(
            "Përmbledhje e përgjigjeve",
            [
                r"\text{a)}\quad y = -\frac{3}{4}x + \frac{25}{2}",
                r"\text{b)}\quad y = -\frac{4}{3}x + \frac{50}{3}",
                r"\text{c)}\quad x = 10",
            ],
            font_size=30,
        )
