"""
YouTube Video — Ushtrimi 2, Njësia 6.2A
Matematika 12 (Botime Pegi)

Gjeni gjatësinë dhe këndin α për 7 vektorë.
α = këndi i rrotullimit kundërorar nga boshti Ox, -180° ≤ α ≤ 180°.

a) 5i+2j      → |v|=√29≈5,39;   α≈21,8°
b) 7i+9j      → |v|=√130≈11,4;   α≈52,1°
c) -5j        → |v|=5;            α=-90°
d) -2i+3j     → |v|=√13≈3,61;    α≈123,7°
e) 3i-5j      → |v|=√34≈5,83;    α≈-59,0°
f) -6i-5j     → |v|=√61≈7,81;    α≈-140,2°
g) -2i        → |v|=2;            α=180°
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))

from manim import *
import numpy as np
from style_guide import (
    apply_style, make_answer_box, make_divider, fade_all,
    STEP_TITLE_COLOR, BODY_TEXT_COLOR, LABEL_COLOR,
    ANSWER_COLOR, SHAPE_COLOR, HIGHLIGHT_COLOR, DIVIDER_COLOR,
    TITLE_SIZE, SUBTITLE_SIZE, PART_HEADER_SIZE, STEP_TITLE_SIZE,
    BODY_SIZE, CALC_SIZE, ANSWER_SIZE,
    T_TITLE_WRITE, T_SUBTITLE_FADE, T_STEP_TITLE,
    T_BODY_FADE, T_KEY_EQUATION, T_ROUTINE_EQUATION,
    T_TRANSITION,
    W_AFTER_KEY, W_AFTER_ROUTINE, W_AFTER_ANSWER,
    ALBANIAN_TEX, PX,
)


class Ushtrimi2(Scene):
    def construct(self):
        apply_style(self)
        MathTex.set_default(tex_template=ALBANIAN_TEX)
        Tex.set_default(tex_template=ALBANIAN_TEX)

        self.title_screen()
        self.show_formulas()
        self.part_a()
        self.part_b()
        self.part_c()
        self.part_d()
        self.part_e()
        self.part_f()
        self.part_g()
        self.final_summary()
        self.end_screen()

    # ────────────────────────────────────────────
    #  TITLE SCREEN
    # ────────────────────────────────────────────

    def title_screen(self):
        title = MathTex(
            r"\text{Ushtrimi 2 — Njësia 6.2A}",
            font_size=TITLE_SIZE, color=WHITE,
        )
        source = MathTex(
            r"\text{Matematika 12 (Botime Pegi)}",
            font_size=SUBTITLE_SIZE, color=BODY_TEXT_COLOR,
        )
        source.next_to(title, DOWN, buff=0.4)

        self.play(Write(title), run_time=T_TITLE_WRITE)
        self.play(FadeIn(source, shift=UP * 0.2), run_time=T_SUBTITLE_FADE)
        self.wait(W_AFTER_KEY)
        self.play(FadeOut(title), FadeOut(source))
        self.wait(0.5)

    # ────────────────────────────────────────────
    #  FORMULAS
    # ────────────────────────────────────────────

    def show_formulas(self):
        heading = MathTex(
            r"\text{Formulat:}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )

        mag_label = MathTex(
            r"\text{Gjatësia e vektorit:}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        mag_formula = MathTex(
            r"|\vec{v}| = \sqrt{x^2 + y^2}",
            font_size=ANSWER_SIZE, color=WHITE,
        )

        angle_label = MathTex(
            r"\text{Këndi } \alpha \text{ me boshtin } Ox\text{:}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        angle_pos = MathTex(
            r"\alpha = \cos^{-1}\!\Big(\frac{x}{|\vec{v}|}\Big)",
            r"\quad \text{kur } y \geq 0",
            font_size=CALC_SIZE, color=WHITE,
        )
        angle_neg = MathTex(
            r"\alpha = -\cos^{-1}\!\Big(\frac{x}{|\vec{v}|}\Big)",
            r"\quad \text{kur } y < 0",
            font_size=CALC_SIZE, color=WHITE,
        )

        group = VGroup(
            heading, mag_label, mag_formula,
            angle_label, angle_pos, angle_neg,
        ).arrange(DOWN, buff=0.4)
        group.move_to(ORIGIN)

        self.play(Write(heading), run_time=T_STEP_TITLE)
        self.play(FadeIn(mag_label, shift=UP * 0.15), run_time=T_BODY_FADE)
        self.play(Write(mag_formula), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)
        self.play(FadeIn(angle_label, shift=UP * 0.15), run_time=T_BODY_FADE)
        self.play(Write(angle_pos), run_time=T_KEY_EQUATION)
        self.wait(0.5)
        self.play(Write(angle_neg), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_KEY)

        self.play(FadeOut(group), run_time=T_TRANSITION)
        self.wait(0.3)

    # ────────────────────────────────────────────
    #  HELPER: SOLVE ONE VECTOR
    # ────────────────────────────────────────────

    def _solve_vector(self, label, vx, vy, vec_display):
        """Draw vector on left, compute magnitude & angle on right."""

        # ── numeric values ──
        mag_sq = vx**2 + vy**2
        mag = np.sqrt(mag_sq)
        mag_exact = abs(mag - round(mag)) < 1e-9
        angle_rad = np.arctan2(vy, vx)
        angle_deg = np.degrees(angle_rad)
        angle_exact = abs(angle_deg - round(angle_deg)) < 0.01
        negate = vy < 0

        # ── formatting helpers ──
        def sq(v):
            return f"({v})^2" if v < 0 else f"{v}^2"

        def alb(v, d=2, keep_zeros=False):
            s = f"{abs(v):.{d}f}"
            if not keep_zeros and '.' in s:
                s = s.rstrip('0').rstrip('.')
            return s.replace('.', '{,}')

        if mag_exact:
            mag_int = int(round(mag))
            mag_str = f"= {mag_int}"
            mag_denom = str(mag_int)
        else:
            mag_disp = alb(mag, 2)
            mag_str = r"\approx " + mag_disp
            mag_denom = mag_disp

        # ── 1  Part header ──
        header = MathTex(
            r"\text{Pjesa " + label + r")}",
            font_size=PART_HEADER_SIZE, color=STEP_TITLE_COLOR,
        )
        header.to_edge(UP, buff=0.4).set_x(PX)
        self.play(Write(header), run_time=T_STEP_TITLE)

        # ── 2  Vector expression (right panel) ──
        vec_eq = MathTex(
            r"\vec{v} = " + vec_display,
            font_size=CALC_SIZE, color=WHITE,
        )
        vec_eq.next_to(header, DOWN, buff=0.45).set_x(PX)
        self.play(Write(vec_eq), run_time=T_ROUTINE_EQUATION)
        self.wait(0.5)

        # ── 3  Diagram on left ──
        mc = max(abs(vx), abs(vy), 1)
        pad = max(1, mc * 0.25)
        rng = mc + pad
        step = 1 if rng <= 3 else (2 if rng <= 7 else 3)
        rng = int(np.ceil(rng / step) * step)

        axes = Axes(
            x_range=[-rng, rng, step],
            y_range=[-rng, rng, step],
            x_length=3.8, y_length=3.8,
            tips=True,
            axis_config={"color": DIVIDER_COLOR, "stroke_width": 1.5},
        )
        axes.move_to(LEFT * 3.2)

        ax_lbl_x = MathTex("x", font_size=16, color=DIVIDER_COLOR)
        ax_lbl_x.next_to(axes.x_axis.get_end(), DR, buff=0.1)
        ax_lbl_y = MathTex("y", font_size=16, color=DIVIDER_COLOR)
        ax_lbl_y.next_to(axes.y_axis.get_end(), UL, buff=0.1)

        origin = axes.c2p(0, 0)
        tip_pt = axes.c2p(vx, vy)

        vec_arrow = Arrow(
            origin, tip_pt, buff=0,
            color=SHAPE_COLOR, stroke_width=3,
            max_tip_length_to_length_ratio=0.15,
        )

        self.play(Create(axes), FadeIn(ax_lbl_x), FadeIn(ax_lbl_y), run_time=0.8)
        self.play(GrowArrow(vec_arrow), run_time=0.7)
        self.wait(0.3)

        # Component decomposition
        if vx != 0 and vy != 0:
            h_end = axes.c2p(vx, 0)
            h_line = DashedLine(
                origin, h_end, color=LABEL_COLOR,
                stroke_width=1.5, dash_length=0.08,
            )
            v_line = DashedLine(
                h_end, tip_pt, color=LABEL_COLOR,
                stroke_width=1.5, dash_length=0.08,
            )

            x_lbl = MathTex(str(vx), font_size=20, color=LABEL_COLOR)
            x_lbl.next_to(h_line, DOWN if vy > 0 else UP, buff=0.12)
            y_lbl = MathTex(str(vy), font_size=20, color=LABEL_COLOR)
            y_lbl.next_to(v_line, RIGHT if vx > 0 else LEFT, buff=0.12)

            # Right-angle mark at (vx, 0)
            tow_o = origin - h_end
            n1 = np.linalg.norm(tow_o)
            tow_o = tow_o / n1 if n1 > 0 else RIGHT
            tow_t = tip_pt - h_end
            n2 = np.linalg.norm(tow_t)
            tow_t = tow_t / n2 if n2 > 0 else UP
            sq_sz = 0.1
            p1 = h_end + sq_sz * tow_o
            p2 = h_end + sq_sz * tow_t
            p3 = p1 + sq_sz * tow_t
            ra_mark = VGroup(
                Line(p1, p3, stroke_width=1, color=DIVIDER_COLOR),
                Line(p2, p3, stroke_width=1, color=DIVIDER_COLOR),
            )

            self.play(Create(h_line), Create(v_line), run_time=0.5)
            self.play(FadeIn(x_lbl), FadeIn(y_lbl), FadeIn(ra_mark), run_time=0.3)

        elif vx == 0:
            # Vector along y-axis — label component
            y_lbl = MathTex(str(vy), font_size=20, color=LABEL_COLOR)
            y_lbl.next_to(vec_arrow, RIGHT, buff=0.12)
            self.play(FadeIn(y_lbl), run_time=0.3)

        else:  # vy == 0
            # Vector along x-axis — label component
            x_lbl = MathTex(str(vx), font_size=20, color=LABEL_COLOR)
            x_lbl.next_to(vec_arrow, DOWN, buff=0.12)
            self.play(FadeIn(x_lbl), run_time=0.3)

        # Divider
        divider = make_divider()
        self.play(Create(divider), run_time=0.3)

        # ── 4  Magnitude (right panel) ──
        mag_title = MathTex(
            r"\text{Gjatësia:}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        mag_title.next_to(vec_eq, DOWN, buff=0.4).set_x(PX)
        self.play(FadeIn(mag_title, shift=UP * 0.15), run_time=T_BODY_FADE)

        eq1 = MathTex(
            r"|\vec{v}| = \sqrt{" + sq(vx) + " + " + sq(vy) + "}",
            font_size=CALC_SIZE, color=WHITE,
        )
        eq1.next_to(mag_title, DOWN, buff=0.3).set_x(PX)
        self.play(Write(eq1), run_time=T_KEY_EQUATION)
        self.wait(0.5)

        eq2 = MathTex(
            r"= \sqrt{" + str(vx**2) + " + " + str(vy**2)
            + r"} = \sqrt{" + str(mag_sq) + "}",
            font_size=CALC_SIZE, color=WHITE,
        )
        eq2.next_to(eq1, DOWN, buff=0.25).set_x(PX)
        self.play(Write(eq2), run_time=T_ROUTINE_EQUATION)
        self.wait(0.5)

        eq3 = MathTex(
            r"|\vec{v}| " + mag_str,
            font_size=CALC_SIZE, color=ANSWER_COLOR,
        )
        eq3.next_to(eq2, DOWN, buff=0.25).set_x(PX)
        self.play(Write(eq3), run_time=T_ROUTINE_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        # ── 5  Angle (right panel) ──
        # Clear magnitude work, keep result
        self.play(
            FadeOut(mag_title), FadeOut(eq1), FadeOut(eq2),
            eq3.animate.next_to(vec_eq, DOWN, buff=0.35).set_x(PX),
            run_time=0.4,
        )

        ang_title = MathTex(
            r"\text{Këndi } \alpha\text{:}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        ang_title.next_to(eq3, DOWN, buff=0.4).set_x(PX)
        self.play(FadeIn(ang_title, shift=UP * 0.15), run_time=T_BODY_FADE)

        ref = ang_title
        sign_note = None
        if negate:
            sign_note = MathTex(
                r"\text{Meqë } y < 0\text{, këndi negativ:}",
                font_size=BODY_SIZE, color=HIGHLIGHT_COLOR,
            )
            sign_note.next_to(ang_title, DOWN, buff=0.25).set_x(PX)
            self.play(FadeIn(sign_note, shift=UP * 0.15), run_time=T_BODY_FADE)
            self.wait(0.4)
            ref = sign_note

        sign_sym = "-" if negate else ""
        cos_eq = MathTex(
            r"\alpha = " + sign_sym
            + r"\cos^{-1}\!\Big(\frac{" + str(vx)
            + "}{" + mag_denom + r"}\Big)",
            font_size=CALC_SIZE, color=WHITE,
        )
        cos_eq.next_to(ref, DOWN, buff=0.3).set_x(PX)
        self.play(Write(cos_eq), run_time=T_KEY_EQUATION)
        self.wait(0.5)

        # Angle result
        if angle_exact:
            ang_val_tex = str(int(round(angle_deg)))
            angle_res = MathTex(
                r"\alpha = " + ang_val_tex + r"^\circ",
                font_size=CALC_SIZE, color=ANSWER_COLOR,
            )
        else:
            a_abs = alb(abs(angle_deg), 1, keep_zeros=True)
            a_val = ("-" + a_abs) if negate else a_abs
            angle_res = MathTex(
                r"\alpha \approx " + a_val + r"^\circ",
                font_size=CALC_SIZE, color=ANSWER_COLOR,
            )
        angle_res.next_to(cos_eq, DOWN, buff=0.3).set_x(PX)
        self.play(Write(angle_res), run_time=T_ROUTINE_EQUATION)
        self.wait(0.5)

        # ── 6  Angle arc on diagram ──
        arc = Arc(
            radius=0.45,
            start_angle=0,
            angle=angle_rad,
            arc_center=origin,
            color=HIGHLIGHT_COLOR,
            stroke_width=2,
        )
        self.play(Create(arc), run_time=0.6)

        # Angle label near the arc midpoint
        mid_a = angle_rad / 2
        lbl_r = 0.7
        lbl_pos = origin + lbl_r * np.array([
            np.cos(mid_a), np.sin(mid_a), 0,
        ])

        if angle_exact:
            arc_lbl_tex = str(int(round(angle_deg))) + r"^\circ"
        else:
            arc_lbl_tex = a_val + r"^\circ"

        arc_lbl = MathTex(arc_lbl_tex, font_size=18, color=HIGHLIGHT_COLOR)
        arc_lbl.move_to(lbl_pos)
        self.play(FadeIn(arc_lbl), run_time=0.3)
        self.wait(0.5)

        # ── 7  Box answers ──
        fade_items = [ang_title, cos_eq]
        if sign_note is not None:
            fade_items.append(sign_note)
        self.play(*[FadeOut(m) for m in fade_items], run_time=0.3)

        target = VGroup(eq3.copy(), angle_res.copy()).arrange(DOWN, buff=0.25)
        target.move_to(RIGHT * PX + DOWN * 0.3)

        self.play(
            eq3.animate.move_to(target[0]),
            angle_res.animate.move_to(target[1]),
            run_time=0.5,
        )

        box = make_answer_box(VGroup(eq3, angle_res))
        self.play(Create(box), run_time=0.4)
        self.play(
            Circumscribe(
                VGroup(eq3, angle_res),
                color=HIGHLIGHT_COLOR, run_time=0.8,
            ),
        )
        self.wait(W_AFTER_KEY)

        # ── 8  Clean up ──
        fade_all(self)
        self.wait(0.3)

    # ────────────────────────────────────────────
    #  PARTS a – g
    # ────────────────────────────────────────────

    def part_a(self):
        self._solve_vector("a", 5, 2, r"5\vec{i} + 2\vec{j}")

    def part_b(self):
        self._solve_vector("b", 7, 9, r"7\vec{i} + 9\vec{j}")

    def part_c(self):
        self._solve_vector("c", 0, -5, r"-5\vec{j}")

    def part_d(self):
        self._solve_vector("d", -2, 3, r"-2\vec{i} + 3\vec{j}")

    def part_e(self):
        self._solve_vector("e", 3, -5, r"3\vec{i} - 5\vec{j}")

    def part_f(self):
        self._solve_vector("f", -6, -5, r"-6\vec{i} - 5\vec{j}")

    def part_g(self):
        self._solve_vector("g", -2, 0, r"-2\vec{i}")

    # ────────────────────────────────────────────
    #  FINAL SUMMARY
    # ────────────────────────────────────────────

    def final_summary(self):
        heading = MathTex(
            r"\text{Përmbledhje e përgjigjeve:}",
            font_size=PART_HEADER_SIZE, color=STEP_TITLE_COLOR,
        )
        heading.to_edge(UP, buff=0.4)

        left_data = [
            r"\text{a)} \; |\vec{v}| \!\approx\! 5{,}39,"
            r"\;\; \alpha \!\approx\! 21{,}8^\circ",
            r"\text{b)} \; |\vec{v}| \!\approx\! 11{,}4,"
            r"\;\; \alpha \!\approx\! 52{,}1^\circ",
            r"\text{c)} \; |\vec{v}| \!=\! 5,"
            r"\;\; \alpha \!=\! {-90}^\circ",
            r"\text{d)} \; |\vec{v}| \!\approx\! 3{,}61,"
            r"\;\; \alpha \!\approx\! 123{,}7^\circ",
        ]
        right_data = [
            r"\text{e)} \; |\vec{v}| \!\approx\! 5{,}83,"
            r"\;\; \alpha \!\approx\! {-59{,}0}^\circ",
            r"\text{f)} \; |\vec{v}| \!\approx\! 7{,}81,"
            r"\;\; \alpha \!\approx\! {-140{,}2}^\circ",
            r"\text{g)} \; |\vec{v}| \!=\! 2,"
            r"\;\; \alpha \!=\! 180^\circ",
        ]

        left_col = VGroup(*[
            MathTex(t, font_size=24, color=ANSWER_COLOR) for t in left_data
        ]).arrange(DOWN, buff=0.3, aligned_edge=LEFT)

        right_col = VGroup(*[
            MathTex(t, font_size=24, color=ANSWER_COLOR) for t in right_data
        ]).arrange(DOWN, buff=0.3, aligned_edge=LEFT)

        columns = VGroup(left_col, right_col).arrange(
            RIGHT, buff=1.0, aligned_edge=UP,
        )
        columns.next_to(heading, DOWN, buff=0.5)

        box = make_answer_box(columns)

        self.play(Write(heading), run_time=T_STEP_TITLE)
        self.wait(0.3)

        all_items = list(left_col) + list(right_col)
        for i, row in enumerate(all_items):
            self.play(FadeIn(row, shift=RIGHT * 0.3), run_time=0.35)
            if i < len(all_items) - 1:
                self.wait(0.15)

        self.play(Create(box), run_time=0.6)
        self.play(
            Flash(
                columns.get_center(), color=ANSWER_COLOR,
                line_length=0.3, num_lines=16, run_time=0.8,
            ),
        )
        self.wait(W_AFTER_ANSWER)

        self.play(
            FadeOut(VGroup(heading, columns, box)),
            run_time=T_TRANSITION,
        )
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
