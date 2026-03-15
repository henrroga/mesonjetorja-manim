import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from manim import *
import numpy as np
from style_guide import (
    apply_style, make_answer_box, fade_all,
    BG_COLOR, BODY_TEXT_COLOR, LABEL_COLOR,
    ANSWER_COLOR, SHAPE_COLOR, AUX_COLOR, HIGHLIGHT_COLOR, DIVIDER_COLOR,
    T_TRANSITION,
)


def dilate_point(p, center, k):
    p = np.array(p, dtype=float)
    c = np.array(center, dtype=float)
    return c + k * (p - c)


class Ushtrimi5(Scene):
    A_VERTS = [(2, 4), (10, 4), (10, 8), (2, 8)]
    D_VERTS = [(-4, 5), (0, 5), (0, 7), (-4, 7)]

    def construct(self):
        apply_style(self)

        self.title_screen()
        self.wait(1)

        self.part_a()
        fade_all(self)
        self.wait(1)

        self.part_b()
        fade_all(self)
        self.wait(1)

        self.part_c()
        fade_all(self)
        self.wait(1)

        self.final_summary()
        self.wait(4)

    # ────────────────────────────────────────
    #  TITLE
    # ────────────────────────────────────────
    def title_screen(self):
        title = MathTex(
            r"\text{Ushtrimi 5 — Përsëritje 7}",
            font_size=44, color=WHITE,
        )
        source = MathTex(
            r"\text{Matematika 10-11: Pjesa I}",
            font_size=28, color=BODY_TEXT_COLOR,
        )
        source.next_to(title, DOWN, buff=0.4)

        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(source, shift=UP * 0.2), run_time=0.8)
        self.wait(2)
        self.play(FadeOut(title), FadeOut(source))
        self.wait(0.5)

    # ────────────────────────────────────────
    #  HELPERS
    # ────────────────────────────────────────
    def _axes(self, x_range, y_range, scale=0.4):
        return Axes(
            x_range=x_range, y_range=y_range,
            x_length=(x_range[1] - x_range[0]) * scale,
            y_length=(y_range[1] - y_range[0]) * scale,
            axis_config={
                "include_tip": True,
                "include_numbers": True,
                "font_size": 14,
                "color": DIVIDER_COLOR,
            },
        )

    def _rect(self, axes, verts, color, label_tex=None, label_dir=UR,
              fill_opacity=0.2):
        corners = [axes.c2p(v[0], v[1]) for v in verts]
        rect = Polygon(*corners, color=color, fill_color=color,
                        fill_opacity=fill_opacity, stroke_width=2.5)
        lbl = None
        if label_tex:
            center = sum(np.array(c) for c in corners) / 4
            lbl = MathTex(label_tex, font_size=26, color=color)
            lbl.next_to(center, label_dir, buff=0.15)
        return rect, lbl

    # ────────────────────────────────────────
    #  PART A — dilation from (6,0), k=0.25
    # ────────────────────────────────────────
    def part_a(self):
        # Header
        header = MathTex(r"\text{Pjesa a)}", font_size=30, color=LABEL_COLOR)
        header.to_corner(UL, buff=0.4)
        self.play(Write(header), run_time=0.6)

        # Problem statement
        prob = MathTex(
            r"\text{Zmadhim me qendër } Q(6,\,0) \text{ dhe } k = 0{,}25",
            font_size=32,
        )
        prob.move_to(ORIGIN)
        self.play(FadeIn(prob), run_time=1)
        self.wait(3)
        self.play(FadeOut(prob), run_time=0.7)
        self.wait(0.5)

        # ── Screen 1: Show grid + rectangle A + center Q ──
        axes = self._axes([-2, 12, 2], [-1, 10, 2], scale=0.45)
        axes.move_to(ORIGIN)
        ax_labels = axes.get_axis_labels(
            x_label=MathTex("x", font_size=18),
            y_label=MathTex("y", font_size=18),
        )

        rect_a, lbl_a = self._rect(axes, self.A_VERTS, SHAPE_COLOR,
                                     label_tex="A", label_dir=UP)

        center_dot = Dot(axes.c2p(6, 0), color=HIGHLIGHT_COLOR, radius=0.08)
        center_lbl = MathTex(r"Q(6,\,0)", font_size=18, color=HIGHLIGHT_COLOR)
        center_lbl.next_to(center_dot, DOWN, buff=0.15)

        self.play(Create(axes), FadeIn(ax_labels), run_time=1.2)
        self.wait(1)
        self.play(Create(rect_a), FadeIn(lbl_a), run_time=1.2)
        self.wait(2)
        self.play(FadeIn(center_dot), FadeIn(center_lbl), run_time=0.8)
        self.wait(2)

        # Fade the graph
        graph_all = VGroup(axes, ax_labels, rect_a, lbl_a, center_dot, center_lbl)
        self.play(FadeOut(graph_all), run_time=0.7)
        self.wait(0.5)

        # ── Screen 2: Explain the formula ──
        formula_title = MathTex(
            r"\text{Formula e zmadhimit:}",
            font_size=28, color=BODY_TEXT_COLOR,
        )
        formula_title.move_to(UP * 2)

        formula1 = MathTex(r"x' = x_Q + k(x - x_Q)", font_size=34, color=LABEL_COLOR)
        formula2 = MathTex(r"y' = y_Q + k(y - y_Q)", font_size=34, color=LABEL_COLOR)
        formula1.next_to(formula_title, DOWN, buff=0.5)
        formula2.next_to(formula1, DOWN, buff=0.3)

        values = MathTex(
            r"\text{ku } Q(6,\,0), \quad k = 0{,}25",
            font_size=28, color=BODY_TEXT_COLOR,
        )
        values.next_to(formula2, DOWN, buff=0.5)

        self.play(FadeIn(formula_title), run_time=0.8)
        self.wait(1.5)
        self.play(Write(formula1), run_time=1.2)
        self.wait(2)
        self.play(Write(formula2), run_time=1.2)
        self.wait(2)
        self.play(FadeIn(values), run_time=0.8)
        self.wait(3)

        self.play(FadeOut(VGroup(formula_title, formula1, formula2, values)),
                  run_time=0.7)
        self.wait(0.5)

        # ── Screen 3: Calculate first vertex in detail ──
        calc_title = MathTex(
            r"\text{Llogaritim kulmin } (2,\,4)\text{:}",
            font_size=28, color=BODY_TEXT_COLOR,
        )
        calc_title.move_to(UP * 2.5)

        eq1 = MathTex(r"x' = 6 + 0{,}25 \cdot (2 - 6)", font_size=32)
        eq1b = MathTex(r"= 6 + 0{,}25 \cdot (-4) = 6 - 1 = 5", font_size=32)
        eq2 = MathTex(r"y' = 0 + 0{,}25 \cdot (4 - 0)", font_size=32)
        eq2b = MathTex(r"= 0{,}25 \cdot 4 = 1", font_size=32)
        result1 = MathTex(r"(2,\,4) \;\rightarrow\; (5,\,1)", font_size=34, color=ANSWER_COLOR)

        eq1.next_to(calc_title, DOWN, buff=0.5)
        eq1b.next_to(eq1, DOWN, buff=0.2)
        eq2.next_to(eq1b, DOWN, buff=0.4)
        eq2b.next_to(eq2, DOWN, buff=0.2)
        result1.next_to(eq2b, DOWN, buff=0.5)

        self.play(FadeIn(calc_title), run_time=0.8)
        self.wait(1)
        self.play(Write(eq1), run_time=1.2)
        self.wait(2)
        self.play(Write(eq1b), run_time=1.2)
        self.wait(2)
        self.play(Write(eq2), run_time=1.2)
        self.wait(2)
        self.play(Write(eq2b), run_time=1.2)
        self.wait(2)
        self.play(Write(result1), run_time=1)
        self.wait(3)

        self.play(FadeOut(VGroup(calc_title, eq1, eq1b, eq2, eq2b, result1)),
                  run_time=0.7)
        self.wait(0.5)

        # ── Screen 4: Remaining vertices (concise) ──
        remaining_title = MathTex(
            r"\text{Në të njëjtën mënyrë:}",
            font_size=28, color=BODY_TEXT_COLOR,
        )
        remaining_title.move_to(UP * 2)

        r2 = MathTex(r"(10,\,4) \;\rightarrow\; (7,\,1)", font_size=32)
        r3 = MathTex(r"(2,\,8) \;\rightarrow\; (5,\,2)", font_size=32)
        r4 = MathTex(r"(10,\,8) \;\rightarrow\; (7,\,2)", font_size=32)

        r2.next_to(remaining_title, DOWN, buff=0.5)
        r3.next_to(r2, DOWN, buff=0.3)
        r4.next_to(r3, DOWN, buff=0.3)

        self.play(FadeIn(remaining_title), run_time=0.8)
        self.wait(1)
        self.play(Write(r2), run_time=1)
        self.wait(1.5)
        self.play(Write(r3), run_time=1)
        self.wait(1.5)
        self.play(Write(r4), run_time=1)
        self.wait(3)

        self.play(FadeOut(VGroup(remaining_title, r2, r3, r4)), run_time=0.7)
        self.wait(0.5)

        # ── Screen 5: Draw both rectangles on grid ──
        axes2 = self._axes([-2, 12, 2], [-1, 10, 2], scale=0.45)
        axes2.move_to(ORIGIN)
        ax2_labels = axes2.get_axis_labels(
            x_label=MathTex("x", font_size=18),
            y_label=MathTex("y", font_size=18),
        )

        rect_a2, lbl_a2 = self._rect(axes2, self.A_VERTS, SHAPE_COLOR,
                                       label_tex="A", label_dir=UP)

        Q = (6, 0)
        k = 0.25
        B_verts = [tuple(dilate_point(v, Q, k)) for v in self.A_VERTS]
        rect_b, lbl_b = self._rect(axes2, B_verts, ANSWER_COLOR,
                                    label_tex="B", label_dir=DOWN)

        # Dilation lines
        dil_lines = VGroup()
        for av, bv in zip(self.A_VERTS, B_verts):
            line = DashedLine(
                axes2.c2p(Q[0], Q[1]), axes2.c2p(av[0], av[1]),
                color=DIVIDER_COLOR, dash_length=0.06, stroke_width=1.5,
            )
            dil_lines.add(line)

        center_dot2 = Dot(axes2.c2p(6, 0), color=HIGHLIGHT_COLOR, radius=0.08)

        self.play(Create(axes2), FadeIn(ax2_labels), run_time=1.2)
        self.play(Create(rect_a2), FadeIn(lbl_a2), run_time=1)
        self.play(FadeIn(center_dot2), run_time=0.5)
        self.wait(1)
        self.play(Create(dil_lines), run_time=1.5)
        self.wait(1)
        self.play(Create(rect_b), FadeIn(lbl_b), run_time=1.5)
        self.wait(4)

    # ────────────────────────────────────────
    #  PART B — dilation from origin, k=-1.5
    # ────────────────────────────────────────
    def part_b(self):
        header = MathTex(r"\text{Pjesa b)}", font_size=30, color=LABEL_COLOR)
        header.to_corner(UL, buff=0.4)
        self.play(Write(header), run_time=0.6)

        # Problem
        prob = MathTex(
            r"\text{Zmadhim me qendër në origjinë dhe } k = -1{,}5",
            font_size=32,
        )
        prob.move_to(ORIGIN)
        self.play(FadeIn(prob), run_time=1)
        self.wait(3)
        self.play(FadeOut(prob), run_time=0.7)
        self.wait(0.5)

        # ── Screen 1: Explain negative k ──
        expl1 = MathTex(
            r"\text{Kur } k < 0 \text{, figura rrotullohet } 180^\circ",
            font_size=30,
        )
        expl2 = MathTex(
            r"\text{dhe zmadhohet/zvogëlohet.}",
            font_size=30,
        )
        expl1.move_to(UP * 1.5)
        expl2.next_to(expl1, DOWN, buff=0.3)

        formula = MathTex(
            r"\text{Kur qendra} = O(0,0): \quad x' = kx, \quad y' = ky",
            font_size=30, color=LABEL_COLOR,
        )
        formula.next_to(expl2, DOWN, buff=0.6)

        self.play(FadeIn(expl1), run_time=1)
        self.wait(2)
        self.play(FadeIn(expl2), run_time=1)
        self.wait(2)
        self.play(Write(formula), run_time=1.2)
        self.wait(3)

        self.play(FadeOut(VGroup(expl1, expl2, formula)), run_time=0.7)
        self.wait(0.5)

        # ── Screen 2: Calculate vertices ──
        calc_title = MathTex(
            r"\text{Llogaritim kulmet me } k = -1{,}5\text{:}",
            font_size=28, color=BODY_TEXT_COLOR,
        )
        calc_title.move_to(UP * 2.5)

        calcs = [
            MathTex(r"(2,\,4) \;\rightarrow\; (-1{,}5 \cdot 2,\; -1{,}5 \cdot 4) = (-3,\,-6)", font_size=28),
            MathTex(r"(10,\,4) \;\rightarrow\; (-15,\,-6)", font_size=28),
            MathTex(r"(2,\,8) \;\rightarrow\; (-3,\,-12)", font_size=28),
            MathTex(r"(10,\,8) \;\rightarrow\; (-15,\,-12)", font_size=28),
        ]
        calcs[0].next_to(calc_title, DOWN, buff=0.5)
        for i in range(1, len(calcs)):
            calcs[i].next_to(calcs[i-1], DOWN, buff=0.3)

        self.play(FadeIn(calc_title), run_time=0.8)
        self.wait(1)
        for c in calcs:
            self.play(Write(c), run_time=1.2)
            self.wait(2)

        self.wait(2)
        self.play(FadeOut(VGroup(calc_title, *calcs)), run_time=0.7)
        self.wait(0.5)

        # ── Screen 3: Show on grid ──
        axes = self._axes([-16, 12, 4], [-14, 10, 4], scale=0.25)
        axes.move_to(ORIGIN)
        ax_labels = axes.get_axis_labels(
            x_label=MathTex("x", font_size=16),
            y_label=MathTex("y", font_size=16),
        )

        rect_a, lbl_a = self._rect(axes, self.A_VERTS, SHAPE_COLOR,
                                     label_tex="A")

        C_verts = [tuple(dilate_point(v, (0, 0), -1.5)) for v in self.A_VERTS]
        rect_c, lbl_c = self._rect(axes, C_verts, AUX_COLOR,
                                    label_tex="C", label_dir=DOWN)

        origin_dot = Dot(axes.c2p(0, 0), color=HIGHLIGHT_COLOR, radius=0.07)

        # Dilation lines through origin
        dil_lines = VGroup()
        for av, cv in zip(self.A_VERTS, C_verts):
            line = DashedLine(
                axes.c2p(av[0], av[1]), axes.c2p(cv[0], cv[1]),
                color=DIVIDER_COLOR, dash_length=0.06, stroke_width=1,
            )
            dil_lines.add(line)

        self.play(Create(axes), FadeIn(ax_labels), run_time=1.2)
        self.play(Create(rect_a), FadeIn(lbl_a), run_time=1)
        self.play(FadeIn(origin_dot), run_time=0.5)
        self.wait(1.5)
        self.play(Create(dil_lines), run_time=1.5)
        self.wait(1)
        self.play(Create(rect_c), FadeIn(lbl_c), run_time=1.5)
        self.wait(4)

    # ────────────────────────────────────────
    #  PART C — describe transformation A → D
    # ────────────────────────────────────────
    def part_c(self):
        header = MathTex(r"\text{Pjesa c)}", font_size=30, color=LABEL_COLOR)
        header.to_corner(UL, buff=0.4)
        self.play(Write(header), run_time=0.6)

        # Problem
        prob = MathTex(
            r"\text{Përshkruani shndërrimin } A \rightarrow D",
            font_size=32,
        )
        prob.move_to(ORIGIN)
        self.play(FadeIn(prob), run_time=1)
        self.wait(3)
        self.play(FadeOut(prob), run_time=0.7)
        self.wait(0.5)

        # ── Screen 1: Show both on grid ──
        axes = self._axes([-6, 12, 2], [-1, 10, 2], scale=0.42)
        axes.move_to(ORIGIN)
        ax_labels = axes.get_axis_labels(
            x_label=MathTex("x", font_size=16),
            y_label=MathTex("y", font_size=16),
        )

        rect_a, lbl_a = self._rect(axes, self.A_VERTS, SHAPE_COLOR,
                                     label_tex="A")
        rect_d, lbl_d = self._rect(axes, self.D_VERTS, HIGHLIGHT_COLOR,
                                     label_tex="D", label_dir=LEFT)

        self.play(Create(axes), FadeIn(ax_labels), run_time=1.2)
        self.play(Create(rect_a), FadeIn(lbl_a), run_time=1)
        self.wait(1.5)
        self.play(Create(rect_d), FadeIn(lbl_d), run_time=1)
        self.wait(3)

        graph_all = VGroup(axes, ax_labels, rect_a, lbl_a, rect_d, lbl_d)
        self.play(FadeOut(graph_all), run_time=0.7)
        self.wait(0.5)

        # ── Screen 2: Find scale factor ──
        step_title = MathTex(
            r"\text{Gjejmë koeficientin:}",
            font_size=28, color=BODY_TEXT_COLOR,
        )
        step_title.move_to(UP * 2.5)

        eq1 = MathTex(r"\text{Gjatësia e A} = 10 - 2 = 8", font_size=30)
        eq2 = MathTex(r"\text{Gjatësia e D} = 0 - (-4) = 4", font_size=30)
        eq3 = MathTex(r"k = \frac{4}{8} = 0{,}5", font_size=34, color=ANSWER_COLOR)

        eq1.next_to(step_title, DOWN, buff=0.5)
        eq2.next_to(eq1, DOWN, buff=0.3)
        eq3.next_to(eq2, DOWN, buff=0.5)

        self.play(FadeIn(step_title), run_time=0.8)
        self.wait(1)
        self.play(Write(eq1), run_time=1.2)
        self.wait(2)
        self.play(Write(eq2), run_time=1.2)
        self.wait(2)
        self.play(Write(eq3), run_time=1.2)
        self.wait(3)

        self.play(FadeOut(VGroup(step_title, eq1, eq2, eq3)), run_time=0.7)
        self.wait(0.5)

        # ── Screen 3: Find center ──
        center_title = MathTex(
            r"\text{Gjejmë qendrën e zmadhimit:}",
            font_size=28, color=BODY_TEXT_COLOR,
        )
        center_title.move_to(UP * 2.5)

        expl = MathTex(
            r"\text{Bashkojmë pikat korresponduese me drejtëza.}",
            font_size=26, color=BODY_TEXT_COLOR,
        )
        expl.next_to(center_title, DOWN, buff=0.4)

        expl2 = MathTex(
            r"\text{Drejtëzat priten në qendrën e zmadhimit.}",
            font_size=26, color=BODY_TEXT_COLOR,
        )
        expl2.next_to(expl, DOWN, buff=0.2)

        center_result = MathTex(
            r"\text{Qendra:} \quad (-10,\,6)",
            font_size=34, color=ANSWER_COLOR,
        )
        center_result.next_to(expl2, DOWN, buff=0.6)

        self.play(FadeIn(center_title), run_time=0.8)
        self.wait(1)
        self.play(FadeIn(expl), run_time=1)
        self.wait(2)
        self.play(FadeIn(expl2), run_time=1)
        self.wait(2)
        self.play(Write(center_result), run_time=1.2)
        self.wait(3)

        self.play(FadeOut(VGroup(center_title, expl, expl2, center_result)),
                  run_time=0.7)
        self.wait(0.5)

        # ── Screen 4: Final answer ──
        ans_title = MathTex(
            r"\text{Përgjigja:}",
            font_size=28, color=BODY_TEXT_COLOR,
        )
        ans_title.move_to(UP * 1.5)

        ans1 = MathTex(r"\text{Zmadhim me qendër } (-10,\,6)", font_size=32, color=ANSWER_COLOR)
        ans2 = MathTex(r"\text{dhe koeficient } k = 0{,}5", font_size=32, color=ANSWER_COLOR)

        ans1.next_to(ans_title, DOWN, buff=0.6)
        ans2.next_to(ans1, DOWN, buff=0.3)

        box = SurroundingRectangle(
            VGroup(ans1, ans2), color=ANSWER_COLOR,
            buff=0.25, corner_radius=0.08,
        )

        self.play(FadeIn(ans_title), run_time=0.8)
        self.wait(1)
        self.play(Write(ans1), run_time=1.2)
        self.wait(2)
        self.play(Write(ans2), run_time=1.2)
        self.wait(1)
        self.play(Create(box), run_time=0.6)
        self.wait(4)

    # ────────────────────────────────────────
    #  SUMMARY
    # ────────────────────────────────────────
    def final_summary(self):
        title = MathTex(
            r"\text{Përmbledhje}",
            font_size=36, color=WHITE,
        )
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=1)

        rows = VGroup(
            MathTex(r"\text{a)} \;\; B: (5,1),\,(7,1),\,(7,2),\,(5,2)", font_size=26, color=ANSWER_COLOR),
            MathTex(r"\text{b)} \;\; C: (-3,-6),\,(-15,-6),\,(-15,-12),\,(-3,-12)", font_size=26, color=ANSWER_COLOR),
            MathTex(r"\text{c)} \;\; A \to D: \text{ qendër } (-10,6),\; k = 0{,}5", font_size=26, color=ANSWER_COLOR),
        )
        rows.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        rows.next_to(title, DOWN, buff=0.6)

        box = SurroundingRectangle(rows, color=ANSWER_COLOR, buff=0.25, corner_radius=0.08)

        self.play(
            LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3) for r in rows], lag_ratio=0.3),
            run_time=2,
        )
        self.play(Create(box), run_time=0.6)
