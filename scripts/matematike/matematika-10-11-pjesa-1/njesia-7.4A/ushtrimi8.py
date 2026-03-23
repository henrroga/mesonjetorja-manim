import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from manim import *
import numpy as np
from style_guide import (
    apply_style, make_answer_box, fade_all,
    BG_COLOR, BODY_TEXT_COLOR, LABEL_COLOR,
    ANSWER_COLOR, SHAPE_COLOR, AUX_COLOR, HIGHLIGHT_COLOR, DIVIDER_COLOR,
    ALBANIAN_TEX,
    T_TRANSITION,
)


# ──────────────────────────────────────────────
#  Reflection across y = x - 1
#  Rule: x' = y + 1,  y' = x - 1
# ──────────────────────────────────────────────
def reflect_across_y_eq_x_minus_1(px, py):
    return (py + 1, px - 1)


def translate(px, py, dx, dy):
    return (px + dx, py + dy)


# Triangle colors
ORIG_COLOR = SHAPE_COLOR       # blue — original triangle
REFL_COLOR = AUX_COLOR         # red — after reflection
TRANS_COLOR = ANSWER_COLOR      # green — after translation
LINE_COLOR = LABEL_COLOR        # yellow — reflection line
EQUIV_COLOR = HIGHLIGHT_COLOR   # orange — equivalent single transformation line


class Ushtrimi8(Scene):
    def construct(self):
        apply_style(self)
        MathTex.set_default(tex_template=ALBANIAN_TEX)
        Tex.set_default(tex_template=ALBANIAN_TEX)

        self.title_screen()
        self.wait(0.5)

        self.part_a()
        fade_all(self)
        self.wait(0.5)

        self.part_b()
        fade_all(self)
        self.wait(0.5)

        self.final_summary()
        self.wait(4)

    # ────────────────────────────────────────
    #  TITLE
    # ────────────────────────────────────────
    def title_screen(self):
        title = MathTex(
            r"\text{Ushtrimi 8 — Njësia 7.4A}",
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
    def _axes(self, x_range, y_range, scale=0.42):
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

    def _triangle(self, axes, pts, color, fill_opacity=0.2, stroke_width=2.5):
        corners = [axes.c2p(p[0], p[1]) for p in pts]
        return Polygon(
            *corners, color=color, fill_color=color,
            fill_opacity=fill_opacity, stroke_width=stroke_width,
        )

    def _label_vertices(self, axes, pts, names, color, directions, font_size=20):
        labels = VGroup()
        for pt, name, d in zip(pts, names, directions):
            lbl = MathTex(name, font_size=font_size, color=color)
            lbl.next_to(axes.c2p(pt[0], pt[1]), d, buff=0.15)
            labels.add(lbl)
        return labels

    def _draw_reflection_line(self, axes, x_range, color=LINE_COLOR):
        """Draw y = x - 1 on given axes."""
        line = axes.plot(lambda x: x - 1, x_range=x_range,
                         color=color, stroke_width=2)
        label = MathTex(r"y = x - 1", font_size=18, color=color)
        # Position label near the end of the line
        label.next_to(axes.c2p(x_range[1], x_range[1] - 1), UR, buff=0.15)
        return line, label

    def _draw_equiv_line(self, axes, slope, intercept, x_range, label_tex,
                         color=EQUIV_COLOR):
        """Draw the equivalent single-transformation line."""
        line = axes.plot(lambda x: slope * x + intercept,
                         x_range=x_range, color=color, stroke_width=2.5)
        lbl = MathTex(label_tex, font_size=18, color=color)
        mid_x = (x_range[0] + x_range[1]) / 2
        lbl.next_to(axes.c2p(mid_x, slope * mid_x + intercept), UL, buff=0.15)
        return line, lbl

    def _perp_connector(self, axes, pt, reflected_pt, color=DIVIDER_COLOR):
        """Dashed line from point to its reflection (through the mirror line)."""
        return DashedLine(
            axes.c2p(pt[0], pt[1]),
            axes.c2p(reflected_pt[0], reflected_pt[1]),
            color=color, dash_length=0.06, stroke_width=1.5,
        )

    def _translation_arrow(self, axes, pt_from, pt_to, color=TRANS_COLOR):
        """Arrow showing translation vector."""
        return Arrow(
            axes.c2p(pt_from[0], pt_from[1]),
            axes.c2p(pt_to[0], pt_to[1]),
            color=color, stroke_width=2, tip_length=0.15,
            buff=0,
        )

    # ────────────────────────────────────────
    #  PART A — Reflection then Translation
    # ────────────────────────────────────────
    def part_a(self):
        # ── Header ──
        header = MathTex(r"\text{Pjesa a)}", font_size=30, color=LABEL_COLOR)
        header.to_corner(UL, buff=0.4)
        self.play(Write(header), run_time=0.6)

        # ── Problem statement ──
        prob1 = MathTex(
            r"\text{Simetri sipas } y = x - 1",
            font_size=30,
        )
        prob2 = MathTex(
            r"\text{pastaj zhvendosje me } \vec{a} = \begin{pmatrix} -4 \\ 4 \end{pmatrix}",
            font_size=30,
        )
        prob_group = VGroup(prob1, prob2).arrange(DOWN, buff=0.3).move_to(ORIGIN)
        self.play(FadeIn(prob_group), run_time=1)
        self.wait(3)
        self.play(FadeOut(prob_group), run_time=0.7)
        self.wait(0.5)

        # ── Original triangle data ──
        A, B, C = (2, 2), (3, 2), (2, 4)
        orig_pts = [A, B, C]
        orig_names = [r"A(2,2)", r"B(3,2)", r"C(2,4)"]
        orig_dirs = [DL, DR, UL]

        # Reflected points
        A1 = reflect_across_y_eq_x_minus_1(*A)  # (3, 1)
        B1 = reflect_across_y_eq_x_minus_1(*B)  # (3, 2) — on the line!
        C1 = reflect_across_y_eq_x_minus_1(*C)  # (5, 1)
        refl_pts = [A1, B1, C1]
        refl_names = [r"A_1(3,1)", r"B_1(3,2)", r"C_1(5,1)"]
        refl_dirs = [DR, UR, DR]

        # Translated points
        A2 = translate(*A1, -4, 4)  # (-1, 5)
        B2 = translate(*B1, -4, 4)  # (-1, 6)
        C2 = translate(*C1, -4, 4)  # (1, 5)
        trans_pts = [A2, B2, C2]
        trans_names = [r"A_2(-1,5)", r"B_2(-1,6)", r"C_2(1,5)"]
        trans_dirs = [DL, UL, DR]

        # ── Screen 1: Show reflection formula ──
        formula_title = MathTex(
            r"\text{Rregulli i simetrisë sipas } y = x - 1\text{:}",
            font_size=28, color=BODY_TEXT_COLOR,
        )
        formula_title.move_to(UP * 2.5)

        formula_why = MathTex(
            r"\text{Për drejtëzën } y = x - c \text{, shëmbëllimi:}",
            font_size=26, color=BODY_TEXT_COLOR,
        )
        formula_why.next_to(formula_title, DOWN, buff=0.4)

        f1 = MathTex(r"x' = y + c", font_size=34, color=LABEL_COLOR)
        f2 = MathTex(r"y' = x - c", font_size=34, color=LABEL_COLOR)
        f1.next_to(formula_why, DOWN, buff=0.4)
        f2.next_to(f1, DOWN, buff=0.25)

        apply_text = MathTex(
            r"\text{Me } c = 1: \quad x' = y + 1, \quad y' = x - 1",
            font_size=30, color=WHITE,
        )
        apply_text.next_to(f2, DOWN, buff=0.5)

        self.play(FadeIn(formula_title), run_time=0.8)
        self.wait(1.5)
        self.play(FadeIn(formula_why), run_time=0.8)
        self.wait(1.5)
        self.play(Write(f1), run_time=1)
        self.wait(1)
        self.play(Write(f2), run_time=1)
        self.wait(2)
        self.play(Write(apply_text), run_time=1.2)
        self.wait(3)

        self.play(FadeOut(VGroup(formula_title, formula_why, f1, f2, apply_text)),
                  run_time=0.7)
        self.wait(0.5)

        # ── Screen 2: Calculate reflection step by step ──
        calc_title = MathTex(
            r"\text{Llogaritim shëmbëllimet:}",
            font_size=28, color=BODY_TEXT_COLOR,
        )
        calc_title.move_to(UP * 2.8)

        calc_rows = [
            MathTex(r"A(2,2): \quad x' = 2+1 = 3, \quad y' = 2-1 = 1", font_size=28),
            MathTex(r"\Rightarrow A_1(3,\,1)", font_size=30, color=REFL_COLOR),
            MathTex(r"B(3,2): \quad x' = 2+1 = 3, \quad y' = 3-1 = 2", font_size=28),
            MathTex(r"\Rightarrow B_1(3,\,2)", font_size=30, color=REFL_COLOR),
            MathTex(r"C(2,4): \quad x' = 4+1 = 5, \quad y' = 2-1 = 1", font_size=28),
            MathTex(r"\Rightarrow C_1(5,\,1)", font_size=30, color=REFL_COLOR),
        ]
        calc_rows[0].next_to(calc_title, DOWN, buff=0.4)
        for i in range(1, len(calc_rows)):
            buff = 0.15 if i % 2 == 1 else 0.3
            calc_rows[i].next_to(calc_rows[i - 1], DOWN, buff=buff)

        self.play(FadeIn(calc_title), run_time=0.8)
        self.wait(1)
        for i, row in enumerate(calc_rows):
            self.play(Write(row), run_time=0.9)
            wait = 2 if i % 2 == 0 else 1.5
            self.wait(wait)

        self.wait(2)
        self.play(FadeOut(VGroup(calc_title, *calc_rows)), run_time=0.7)
        self.wait(0.5)

        # ── Screen 3: Draw original + reflection on axes ──
        axes = self._axes([-3, 7, 1], [-2, 7, 1], scale=0.55)
        axes.move_to(ORIGIN)
        ax_labels = axes.get_axis_labels(
            x_label=MathTex("x", font_size=18),
            y_label=MathTex("y", font_size=18),
        )

        # Reflection line
        refl_line, refl_line_lbl = self._draw_reflection_line(
            axes, [-2, 6.5])

        # Original triangle
        tri_orig = self._triangle(axes, orig_pts, ORIG_COLOR)
        lbl_orig = self._label_vertices(axes, orig_pts, orig_names, ORIG_COLOR,
                                         orig_dirs)

        # Reflected triangle
        tri_refl = self._triangle(axes, refl_pts, REFL_COLOR)
        lbl_refl = self._label_vertices(axes, refl_pts, refl_names, REFL_COLOR,
                                         refl_dirs)

        # Perpendicular connectors (point → reflection)
        perps = VGroup(*[
            self._perp_connector(axes, o, r)
            for o, r in zip(orig_pts, refl_pts)
        ])

        self.play(Create(axes), FadeIn(ax_labels), run_time=1.2)
        self.wait(0.5)

        # Draw reflection line
        self.play(Create(refl_line), FadeIn(refl_line_lbl), run_time=1)
        self.wait(1)

        # Draw original triangle
        self.play(DrawBorderThenFill(tri_orig), run_time=1.2)
        self.play(
            LaggedStart(*[FadeIn(l, shift=DOWN * 0.2) for l in lbl_orig],
                         lag_ratio=0.2),
            run_time=1,
        )
        self.wait(2)

        # Draw perpendicular connectors then reflected triangle
        self.play(Create(perps), run_time=1.2)
        self.wait(1)
        self.play(DrawBorderThenFill(tri_refl), run_time=1.2)
        self.play(
            LaggedStart(*[FadeIn(l, shift=DOWN * 0.2) for l in lbl_refl],
                         lag_ratio=0.2),
            run_time=1,
        )
        self.wait(3)

        # Fade perpendiculars, keep triangles
        self.play(FadeOut(perps), run_time=0.5)
        self.wait(0.5)

        # ── Note: B(3,2) = B₁(3,2) — on the line! ──
        note_b = MathTex(
            r"\text{Vëni re: } B(3,2) = B_1(3,2) \text{ — pika ndodhet mbi drejtëzën!}",
            font_size=22, color=BODY_TEXT_COLOR,
        )
        note_b.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(note_b), run_time=0.8)
        self.play(Indicate(lbl_orig[1], color=LABEL_COLOR), run_time=0.6)
        self.wait(2.5)
        self.play(FadeOut(note_b), run_time=0.5)

        # Store graph elements for later fade
        graph_a_refl = VGroup(axes, ax_labels, refl_line, refl_line_lbl,
                              tri_orig, lbl_orig, tri_refl, lbl_refl)
        self.play(FadeOut(graph_a_refl), run_time=0.7)
        self.wait(0.5)

        # ── Screen 4: Translation calculation ──
        trans_title = MathTex(
            r"\text{Zhvendosja me } \vec{a} = \begin{pmatrix} -4 \\ 4 \end{pmatrix}\text{:}",
            font_size=28, color=BODY_TEXT_COLOR,
        )
        trans_title.move_to(UP * 2.5)

        trans_explain = MathTex(
            r"\text{Shtojmë } (-4,\,4) \text{ tek secila pikë:}",
            font_size=26, color=BODY_TEXT_COLOR,
        )
        trans_explain.next_to(trans_title, DOWN, buff=0.35)

        t_rows = [
            MathTex(r"A_1(3,1) \;\rightarrow\; (3-4,\; 1+4) = A_2(-1,\,5)",
                    font_size=28),
            MathTex(r"B_1(3,2) \;\rightarrow\; (3-4,\; 2+4) = B_2(-1,\,6)",
                    font_size=28),
            MathTex(r"C_1(5,1) \;\rightarrow\; (5-4,\; 1+4) = C_2(1,\,5)",
                    font_size=28),
        ]
        t_rows[0].next_to(trans_explain, DOWN, buff=0.4)
        for i in range(1, len(t_rows)):
            t_rows[i].next_to(t_rows[i - 1], DOWN, buff=0.3)

        self.play(FadeIn(trans_title), run_time=0.8)
        self.wait(1)
        self.play(FadeIn(trans_explain), run_time=0.8)
        self.wait(1.5)
        for row in t_rows:
            self.play(Write(row), run_time=1)
            self.wait(2)

        self.wait(2)
        self.play(FadeOut(VGroup(trans_title, trans_explain, *t_rows)), run_time=0.7)
        self.wait(0.5)

        # ── Screen 5: Full picture — all 3 triangles ──
        axes2 = self._axes([-3, 7, 1], [-2, 8, 1], scale=0.5)
        axes2.move_to(ORIGIN)
        ax2_labels = axes2.get_axis_labels(
            x_label=MathTex("x", font_size=18),
            y_label=MathTex("y", font_size=18),
        )

        refl_line2, refl_line2_lbl = self._draw_reflection_line(axes2, [-2, 6.5])

        tri_o2 = self._triangle(axes2, orig_pts, ORIG_COLOR)
        lbl_o2 = self._label_vertices(
            axes2, orig_pts,
            [r"A", r"B", r"C"],
            ORIG_COLOR, orig_dirs, font_size=18,
        )

        tri_r2 = self._triangle(axes2, refl_pts, REFL_COLOR, fill_opacity=0.15)
        lbl_r2 = self._label_vertices(
            axes2, refl_pts,
            [r"A_1", r"B_1", r"C_1"],
            REFL_COLOR, refl_dirs, font_size=18,
        )

        tri_t2 = self._triangle(axes2, trans_pts, TRANS_COLOR)
        lbl_t2 = self._label_vertices(
            axes2, trans_pts,
            [r"A_2", r"B_2", r"C_2"],
            TRANS_COLOR, trans_dirs, font_size=18,
        )

        # Translation arrows from reflected → final
        t_arrows = VGroup(*[
            self._translation_arrow(axes2, r, t)
            for r, t in zip(refl_pts, trans_pts)
        ])

        self.play(Create(axes2), FadeIn(ax2_labels), run_time=1.2)
        self.play(Create(refl_line2), FadeIn(refl_line2_lbl), run_time=0.8)
        self.wait(0.5)

        # Original
        self.play(DrawBorderThenFill(tri_o2), run_time=1)
        self.play(FadeIn(lbl_o2), run_time=0.5)
        self.wait(1)

        # Reflected (dim)
        self.play(DrawBorderThenFill(tri_r2), run_time=1)
        self.play(FadeIn(lbl_r2), run_time=0.5)
        self.wait(1)

        # Translation arrows + final triangle
        self.play(
            LaggedStart(*[GrowArrow(a) for a in t_arrows], lag_ratio=0.2),
            run_time=1.2,
        )
        self.wait(0.5)
        self.play(DrawBorderThenFill(tri_t2), run_time=1)
        self.play(FadeIn(lbl_t2), run_time=0.5)
        self.wait(3)

        graph_a_full = VGroup(axes2, ax2_labels, refl_line2, refl_line2_lbl,
                              tri_o2, lbl_o2, tri_r2, lbl_r2, tri_t2, lbl_t2,
                              t_arrows)
        self.play(FadeOut(graph_a_full), run_time=0.7)
        self.wait(0.5)

        # ── Screen 6: Find the single transformation ──
        equiv_title = MathTex(
            r"\text{Gjejmë shndërrimin e vetëm:}",
            font_size=28, color=BODY_TEXT_COLOR,
        )
        equiv_title.move_to(UP * 2.8)

        equiv_expl = MathTex(
            r"\text{Krahasojmë pikat fillestare me ato përfundimtare:}",
            font_size=26, color=BODY_TEXT_COLOR,
        )
        equiv_expl.next_to(equiv_title, DOWN, buff=0.35)

        mapping_rows = [
            MathTex(r"A(2,2) \;\rightarrow\; A_2(-1,5)", font_size=28),
            MathTex(r"B(3,2) \;\rightarrow\; B_2(-1,6)", font_size=28),
            MathTex(r"C(2,4) \;\rightarrow\; C_2(1,5)", font_size=28),
        ]
        mapping_rows[0].next_to(equiv_expl, DOWN, buff=0.4)
        for i in range(1, len(mapping_rows)):
            mapping_rows[i].next_to(mapping_rows[i - 1], DOWN, buff=0.2)

        self.play(FadeIn(equiv_title), run_time=0.8)
        self.wait(1)
        self.play(FadeIn(equiv_expl), run_time=0.8)
        self.wait(1)
        for row in mapping_rows:
            self.play(Write(row), run_time=0.8)
            self.wait(1)

        self.wait(1.5)

        # Show midpoint analysis
        mid_expl = MathTex(
            r"\text{Mespikat e segmenteve } AA_2, BB_2, CC_2\text{:}",
            font_size=26, color=BODY_TEXT_COLOR,
        )
        mid_expl.next_to(mapping_rows[-1], DOWN, buff=0.4)

        mid_rows = [
            MathTex(r"M_A = \left(\tfrac{2+(-1)}{2},\, \tfrac{2+5}{2}\right) = (0{,}5;\; 3{,}5)",
                    font_size=26),
            MathTex(r"M_B = \left(\tfrac{3+(-1)}{2},\, \tfrac{2+6}{2}\right) = (1;\; 4)",
                    font_size=26),
            MathTex(r"M_C = \left(\tfrac{2+1}{2},\, \tfrac{4+5}{2}\right) = (1{,}5;\; 4{,}5)",
                    font_size=26),
        ]
        mid_rows[0].next_to(mid_expl, DOWN, buff=0.25)
        for i in range(1, len(mid_rows)):
            mid_rows[i].next_to(mid_rows[i - 1], DOWN, buff=0.15)

        self.play(FadeIn(mid_expl), run_time=0.8)
        self.wait(1)
        for row in mid_rows:
            self.play(Write(row), run_time=0.8)
            self.wait(1.5)

        self.wait(1)

        # These midpoints lie on y = -x + 4
        check_text = MathTex(
            r"\text{Kontrollojmë: } 3{,}5 = -0{,}5 + 4 \;\checkmark \quad "
            r"4 = -1 + 4 \;\checkmark",
            font_size=24, color=BODY_TEXT_COLOR,
        )
        check_text.next_to(mid_rows[-1], DOWN, buff=0.3)
        self.play(FadeIn(check_text), run_time=0.8)
        self.wait(2)

        self.play(FadeOut(VGroup(
            equiv_title, equiv_expl, *mapping_rows,
            mid_expl, *mid_rows, check_text,
        )), run_time=0.7)
        self.wait(0.5)

        # ── Answer ──
        ans_title = MathTex(
            r"\text{Shndërrimi i vetëm:}",
            font_size=28, color=BODY_TEXT_COLOR,
        )
        ans_title.move_to(UP * 1)

        ans = MathTex(
            r"\text{Simetri sipas drejtëzës } y = -x + 4",
            font_size=34, color=ANSWER_COLOR,
        )
        ans.next_to(ans_title, DOWN, buff=0.5)
        box = make_answer_box(ans)

        self.play(FadeIn(ans_title), run_time=0.8)
        self.wait(1)
        self.play(Write(ans), run_time=1.2)
        self.play(Create(box), run_time=0.5)
        self.wait(1)
        self.play(Circumscribe(VGroup(ans, box), color=ANSWER_COLOR, run_time=0.8))
        self.wait(3)

        # ── Screen 7: Show equivalence on graph ──
        self.play(FadeOut(VGroup(ans_title, ans, box)), run_time=0.7)
        self.wait(0.3)

        axes3 = self._axes([-3, 7, 1], [-2, 8, 1], scale=0.5)
        axes3.move_to(ORIGIN)
        ax3_labels = axes3.get_axis_labels(
            x_label=MathTex("x", font_size=18),
            y_label=MathTex("y", font_size=18),
        )

        tri_orig3 = self._triangle(axes3, orig_pts, ORIG_COLOR)
        lbl_orig3 = self._label_vertices(
            axes3, orig_pts, [r"A", r"B", r"C"],
            ORIG_COLOR, orig_dirs, font_size=18,
        )
        tri_final3 = self._triangle(axes3, trans_pts, TRANS_COLOR)
        lbl_final3 = self._label_vertices(
            axes3, trans_pts, [r"A_2", r"B_2", r"C_2"],
            TRANS_COLOR, trans_dirs, font_size=18,
        )

        # Equivalence line y = -x + 4
        equiv_line, equiv_lbl = self._draw_equiv_line(
            axes3, -1, 4, [-2, 6.5],
            r"y = -x + 4", EQUIV_COLOR,
        )

        # Perpendicular connectors original → final (through equiv line)
        equiv_perps = VGroup(*[
            self._perp_connector(axes3, o, t, color=EQUIV_COLOR)
            for o, t in zip(orig_pts, trans_pts)
        ])

        self.play(Create(axes3), FadeIn(ax3_labels), run_time=1)
        self.play(DrawBorderThenFill(tri_orig3), FadeIn(lbl_orig3), run_time=1)
        self.play(DrawBorderThenFill(tri_final3), FadeIn(lbl_final3), run_time=1)
        self.wait(1)

        self.play(Create(equiv_line), FadeIn(equiv_lbl), run_time=1)
        self.wait(0.5)
        self.play(Create(equiv_perps), run_time=1.2)
        self.wait(4)

    # ────────────────────────────────────────
    #  PART B — Translation then Reflection
    # ────────────────────────────────────────
    def part_b(self):
        # ── Header ──
        header = MathTex(r"\text{Pjesa b)}", font_size=30, color=LABEL_COLOR)
        header.to_corner(UL, buff=0.4)
        self.play(Write(header), run_time=0.6)

        # ── Problem statement ──
        prob1 = MathTex(
            r"\text{Fillimisht zhvendosje me } \vec{a} = \begin{pmatrix} -4 \\ 4 \end{pmatrix}",
            font_size=30,
        )
        prob2 = MathTex(
            r"\text{pastaj simetri sipas } y = x - 1",
            font_size=30,
        )
        prob_group = VGroup(prob1, prob2).arrange(DOWN, buff=0.3).move_to(ORIGIN)
        self.play(FadeIn(prob_group), run_time=1)
        self.wait(3)
        self.play(FadeOut(prob_group), run_time=0.7)
        self.wait(0.5)

        # ── Data ──
        A, B, C = (2, 2), (3, 2), (2, 4)
        orig_pts = [A, B, C]
        orig_dirs = [DL, DR, UL]

        # Translated first
        A1p = translate(*A, -4, 4)   # (-2, 6)
        B1p = translate(*B, -4, 4)   # (-1, 6)
        C1p = translate(*C, -4, 4)   # (-2, 8)
        trans_pts = [A1p, B1p, C1p]
        trans_names = [r"A'_1(-2,6)", r"B'_1(-1,6)", r"C'_1(-2,8)"]
        trans_dirs = [DL, DR, UL]

        # Then reflected
        A2p = reflect_across_y_eq_x_minus_1(*A1p)  # (7, -3)
        B2p = reflect_across_y_eq_x_minus_1(*B1p)  # (7, -2)
        C2p = reflect_across_y_eq_x_minus_1(*C1p)  # (9, -3)
        final_pts = [A2p, B2p, C2p]
        final_names = [r"A'_2(7,-3)", r"B'_2(7,-2)", r"C'_2(9,-3)"]
        final_dirs = [DL, UL, DR]

        # ── Screen 1: Translation calculation ──
        t_title = MathTex(
            r"\text{Zhvendosja me } \vec{a} = \begin{pmatrix} -4 \\ 4 \end{pmatrix}\text{:}",
            font_size=28, color=BODY_TEXT_COLOR,
        )
        t_title.move_to(UP * 2.5)

        t_rows = [
            MathTex(r"A(2,2) \;\rightarrow\; (2-4,\; 2+4) = A'_1(-2,\,6)", font_size=28),
            MathTex(r"B(3,2) \;\rightarrow\; (3-4,\; 2+4) = B'_1(-1,\,6)", font_size=28),
            MathTex(r"C(2,4) \;\rightarrow\; (2-4,\; 4+4) = C'_1(-2,\,8)", font_size=28),
        ]
        t_rows[0].next_to(t_title, DOWN, buff=0.4)
        for i in range(1, len(t_rows)):
            t_rows[i].next_to(t_rows[i - 1], DOWN, buff=0.3)

        self.play(FadeIn(t_title), run_time=0.8)
        self.wait(1)
        for row in t_rows:
            self.play(Write(row), run_time=1)
            self.wait(2)

        self.wait(2)
        self.play(FadeOut(VGroup(t_title, *t_rows)), run_time=0.7)
        self.wait(0.5)

        # ── Screen 2: Reflection calculation ──
        r_title = MathTex(
            r"\text{Simetria sipas } y = x - 1 \quad (x' = y+1,\; y' = x-1)\text{:}",
            font_size=26, color=BODY_TEXT_COLOR,
        )
        r_title.move_to(UP * 2.5)

        r_rows = [
            MathTex(r"A'_1(-2,6): \quad x' = 6+1 = 7, \quad y' = -2-1 = -3",
                    font_size=27),
            MathTex(r"\Rightarrow A'_2(7,\,-3)", font_size=30, color=REFL_COLOR),
            MathTex(r"B'_1(-1,6): \quad x' = 6+1 = 7, \quad y' = -1-1 = -2",
                    font_size=27),
            MathTex(r"\Rightarrow B'_2(7,\,-2)", font_size=30, color=REFL_COLOR),
            MathTex(r"C'_1(-2,8): \quad x' = 8+1 = 9, \quad y' = -2-1 = -3",
                    font_size=27),
            MathTex(r"\Rightarrow C'_2(9,\,-3)", font_size=30, color=REFL_COLOR),
        ]
        r_rows[0].next_to(r_title, DOWN, buff=0.35)
        for i in range(1, len(r_rows)):
            buff = 0.12 if i % 2 == 1 else 0.25
            r_rows[i].next_to(r_rows[i - 1], DOWN, buff=buff)

        self.play(FadeIn(r_title), run_time=0.8)
        self.wait(1)
        for i, row in enumerate(r_rows):
            self.play(Write(row), run_time=0.9)
            wait = 2 if i % 2 == 0 else 1.5
            self.wait(wait)

        self.wait(2)
        self.play(FadeOut(VGroup(r_title, *r_rows)), run_time=0.7)
        self.wait(0.5)

        # ── Screen 3: All 3 triangles on graph ──
        axes = self._axes([-4, 11, 1], [-5, 10, 1], scale=0.38)
        axes.move_to(ORIGIN)
        ax_labels = axes.get_axis_labels(
            x_label=MathTex("x", font_size=16),
            y_label=MathTex("y", font_size=16),
        )

        refl_line, refl_line_lbl = self._draw_reflection_line(axes, [-4, 10])

        tri_o = self._triangle(axes, orig_pts, ORIG_COLOR)
        lbl_o = self._label_vertices(
            axes, orig_pts, [r"A", r"B", r"C"],
            ORIG_COLOR, orig_dirs, font_size=16,
        )

        tri_t = self._triangle(axes, trans_pts, TRANS_COLOR, fill_opacity=0.15)
        lbl_t = self._label_vertices(
            axes, trans_pts,
            [r"A'_1", r"B'_1", r"C'_1"],
            TRANS_COLOR, trans_dirs, font_size=16,
        )

        tri_f = self._triangle(axes, final_pts, REFL_COLOR)
        lbl_f = self._label_vertices(
            axes, final_pts,
            [r"A'_2", r"B'_2", r"C'_2"],
            REFL_COLOR, final_dirs, font_size=16,
        )

        # Translation arrows orig → translated
        t_arrows = VGroup(*[
            self._translation_arrow(axes, o, t)
            for o, t in zip(orig_pts, trans_pts)
        ])

        # Perpendicular connectors translated → final
        perps = VGroup(*[
            self._perp_connector(axes, t, f, color=REFL_COLOR)
            for t, f in zip(trans_pts, final_pts)
        ])

        self.play(Create(axes), FadeIn(ax_labels), run_time=1.2)
        self.play(Create(refl_line), FadeIn(refl_line_lbl), run_time=0.8)

        # Original
        self.play(DrawBorderThenFill(tri_o), FadeIn(lbl_o), run_time=1)
        self.wait(1)

        # Translation
        self.play(
            LaggedStart(*[GrowArrow(a) for a in t_arrows], lag_ratio=0.2),
            run_time=1,
        )
        self.play(DrawBorderThenFill(tri_t), FadeIn(lbl_t), run_time=1)
        self.wait(1)

        # Reflection
        self.play(Create(perps), run_time=1)
        self.play(DrawBorderThenFill(tri_f), FadeIn(lbl_f), run_time=1)
        self.wait(3)

        graph_b = VGroup(axes, ax_labels, refl_line, refl_line_lbl,
                         tri_o, lbl_o, tri_t, lbl_t, tri_f, lbl_f,
                         t_arrows, perps)
        self.play(FadeOut(graph_b), run_time=0.7)
        self.wait(0.5)

        # ── Screen 4: Find equivalent single transformation ──
        equiv_title = MathTex(
            r"\text{Gjejmë shndërrimin e vetëm:}",
            font_size=28, color=BODY_TEXT_COLOR,
        )
        equiv_title.move_to(UP * 2.8)

        mapping_rows = [
            MathTex(r"A(2,2) \;\rightarrow\; A'_2(7,-3)", font_size=28),
            MathTex(r"B(3,2) \;\rightarrow\; B'_2(7,-2)", font_size=28),
            MathTex(r"C(2,4) \;\rightarrow\; C'_2(9,-3)", font_size=28),
        ]
        mapping_rows[0].next_to(equiv_title, DOWN, buff=0.4)
        for i in range(1, len(mapping_rows)):
            mapping_rows[i].next_to(mapping_rows[i - 1], DOWN, buff=0.2)

        mid_expl = MathTex(
            r"\text{Mespikat:}",
            font_size=26, color=BODY_TEXT_COLOR,
        )
        mid_expl.next_to(mapping_rows[-1], DOWN, buff=0.35)

        mid_rows = [
            MathTex(r"M_A = \left(\tfrac{2+7}{2},\, \tfrac{2+(-3)}{2}\right) = (4{,}5;\; -0{,}5)",
                    font_size=24),
            MathTex(r"M_B = \left(\tfrac{3+7}{2},\, \tfrac{2+(-2)}{2}\right) = (5;\; 0)",
                    font_size=24),
            MathTex(r"M_C = \left(\tfrac{2+9}{2},\, \tfrac{4+(-3)}{2}\right) = (5{,}5;\; 0{,}5)",
                    font_size=24),
        ]
        mid_rows[0].next_to(mid_expl, DOWN, buff=0.25)
        for i in range(1, len(mid_rows)):
            mid_rows[i].next_to(mid_rows[i - 1], DOWN, buff=0.15)

        check = MathTex(
            r"\text{Kontrollojmë: } -0{,}5 = -4{,}5 + 5 \;\checkmark \quad "
            r"0 = -5 + 5 \;\checkmark",
            font_size=22, color=BODY_TEXT_COLOR,
        )
        check.next_to(mid_rows[-1], DOWN, buff=0.3)

        self.play(FadeIn(equiv_title), run_time=0.8)
        self.wait(1)
        for row in mapping_rows:
            self.play(Write(row), run_time=0.8)
            self.wait(1)
        self.play(FadeIn(mid_expl), run_time=0.6)
        for row in mid_rows:
            self.play(Write(row), run_time=0.8)
            self.wait(1.5)
        self.play(FadeIn(check), run_time=0.8)
        self.wait(2)

        self.play(FadeOut(VGroup(
            equiv_title, *mapping_rows, mid_expl, *mid_rows, check,
        )), run_time=0.7)
        self.wait(0.5)

        # ── Answer ──
        ans_title = MathTex(
            r"\text{Shndërrimi i vetëm:}",
            font_size=28, color=BODY_TEXT_COLOR,
        )
        ans_title.move_to(UP * 1)

        ans = MathTex(
            r"\text{Simetri sipas drejtëzës } y = -x + 5",
            font_size=34, color=ANSWER_COLOR,
        )
        ans.next_to(ans_title, DOWN, buff=0.5)
        box = make_answer_box(ans)

        self.play(FadeIn(ans_title), run_time=0.8)
        self.wait(1)
        self.play(Write(ans), run_time=1.2)
        self.play(Create(box), run_time=0.5)
        self.wait(1)
        self.play(Circumscribe(VGroup(ans, box), color=ANSWER_COLOR, run_time=0.8))
        self.wait(3)

        # ── Screen 5: Show equivalence on graph ──
        self.play(FadeOut(VGroup(ans_title, ans, box)), run_time=0.7)
        self.wait(0.3)

        axes4 = self._axes([-2, 11, 1], [-5, 6, 1], scale=0.42)
        axes4.move_to(ORIGIN)
        ax4_labels = axes4.get_axis_labels(
            x_label=MathTex("x", font_size=16),
            y_label=MathTex("y", font_size=16),
        )

        tri_orig4 = self._triangle(axes4, orig_pts, ORIG_COLOR)
        lbl_orig4 = self._label_vertices(
            axes4, orig_pts, [r"A", r"B", r"C"],
            ORIG_COLOR, orig_dirs, font_size=16,
        )
        tri_final4 = self._triangle(axes4, final_pts, REFL_COLOR)
        lbl_final4 = self._label_vertices(
            axes4, final_pts, [r"A'_2", r"B'_2", r"C'_2"],
            REFL_COLOR, final_dirs, font_size=16,
        )

        equiv_line, equiv_lbl = self._draw_equiv_line(
            axes4, -1, 5, [-1, 10],
            r"y = -x + 5", EQUIV_COLOR,
        )

        equiv_perps = VGroup(*[
            self._perp_connector(axes4, o, f, color=EQUIV_COLOR)
            for o, f in zip(orig_pts, final_pts)
        ])

        self.play(Create(axes4), FadeIn(ax4_labels), run_time=1)
        self.play(DrawBorderThenFill(tri_orig4), FadeIn(lbl_orig4), run_time=1)
        self.play(DrawBorderThenFill(tri_final4), FadeIn(lbl_final4), run_time=1)
        self.wait(0.5)

        self.play(Create(equiv_line), FadeIn(equiv_lbl), run_time=1)
        self.play(Create(equiv_perps), run_time=1.2)
        self.wait(1)

        # Note: different result from part a!
        note = MathTex(
            r"\text{Vëni re: radha e shndërrimeve ndryshon rezultatin!}",
            font_size=24, color=HIGHLIGHT_COLOR,
        )
        note.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(note), run_time=0.8)
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
            MathTex(
                r"\text{a) Simetri } y\!=\!x\!-\!1 \text{, pastaj zhvendosje } "
                r"\vec{a}\!=\!\begin{pmatrix} -4 \\ 4 \end{pmatrix}",
                font_size=24,
            ),
            MathTex(
                r"A(2,2) \to A_2(-1,5), \quad B(3,2) \to B_2(-1,6), \quad "
                r"C(2,4) \to C_2(1,5)",
                font_size=22, color=REFL_COLOR,
            ),
            MathTex(
                r"\text{Ekuivalente: simetri sipas } y = -x + 4",
                font_size=26, color=ANSWER_COLOR,
            ),
            MathTex(
                r"\text{b) Zhvendosje } \vec{a}\!=\!\begin{pmatrix} -4 \\ 4 \end{pmatrix}"
                r"\text{, pastaj simetri } y\!=\!x\!-\!1",
                font_size=24,
            ),
            MathTex(
                r"A(2,2) \to A'_2(7,-3), \quad B(3,2) \to B'_2(7,-2), \quad "
                r"C(2,4) \to C'_2(9,-3)",
                font_size=22, color=REFL_COLOR,
            ),
            MathTex(
                r"\text{Ekuivalente: simetri sipas } y = -x + 5",
                font_size=26, color=ANSWER_COLOR,
            ),
        )
        rows.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        rows.next_to(title, DOWN, buff=0.5)

        # Ensure it fits on screen
        if rows.get_bottom()[1] < -3.5:
            rows.scale_to_fit_height(6.0)
            rows.next_to(title, DOWN, buff=0.5)

        box = SurroundingRectangle(
            rows, color=ANSWER_COLOR, buff=0.25, corner_radius=0.08,
        )

        self.play(
            LaggedStart(
                *[FadeIn(r, shift=RIGHT * 0.3) for r in rows],
                lag_ratio=0.15,
            ),
            run_time=2.5,
        )
        self.play(Create(box), run_time=0.6)
        self.wait(1)
        self.play(
            Flash(box.get_center(), color=ANSWER_COLOR,
                  line_length=0.3, num_lines=12, run_time=0.5),
        )
