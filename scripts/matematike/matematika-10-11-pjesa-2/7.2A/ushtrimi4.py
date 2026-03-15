import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from manim import *
import numpy as np
from components import ExerciseScene
from style_guide import (
    make_answer_box, make_divider, fade_all,
    STEP_TITLE_COLOR, BODY_TEXT_COLOR, LABEL_COLOR,
    ANSWER_COLOR, SHAPE_COLOR, AUX_COLOR, HIGHLIGHT_COLOR,
    PART_HEADER_SIZE, STEP_TITLE_SIZE,
    BODY_SIZE, CALC_SIZE, ANSWER_SIZE, DIAGRAM_LABEL_SIZE,
    T_STEP_TITLE, T_BODY_FADE, T_KEY_EQUATION, T_ROUTINE_EQUATION,
    T_SHAPE_CREATE, T_LAYOUT_SHIFT, T_TRANSITION,
    W_AFTER_KEY, W_AFTER_ROUTINE, W_AFTER_ANSWER, W_PROBLEM,
    CALC_TOP,
)

# Right-panel center x — all titles, text, and equations align here
PX = 3.2


class Ushtrimi4(ExerciseScene):
    """
    Ushtrimi 4 — Njësia 7.2A
    Matematika 10-11: Pjesa II

    Isosceles triangle calculations.
    """

    exercise_number = 4
    unit = "7.2A"
    parts = ["a", "b"]

    # ── Alignment helpers: every element centered at x = PX ──

    def _title(self, text, ref=None, y_pos=None, buff=0.5):
        t = MathTex(
            r"\text{" + text + r"}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        if y_pos is not None:
            t.move_to(np.array([PX, y_pos, 0]))
        elif ref is not None:
            t.next_to(ref, DOWN, buff=buff)
            t.set_x(PX)
        self.play(FadeIn(t), run_time=T_STEP_TITLE)
        return t

    def _text(self, lines, ref, buff=0.25):
        parts = [MathTex(l, font_size=BODY_SIZE, color=BODY_TEXT_COLOR) for l in lines]
        g = VGroup(*parts).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        g.next_to(ref, DOWN, buff=buff)
        g.set_x(PX)
        self.play(FadeIn(g), run_time=T_BODY_FADE)
        return g

    def _eq(self, tex, ref, buff=0.25, color=None, fs=None, key=False):
        eq = MathTex(tex, font_size=fs or CALC_SIZE)
        if color:
            eq.set_color(color)
        eq.next_to(ref, DOWN, buff=buff)
        eq.set_x(PX)
        self.play(Write(eq), run_time=T_KEY_EQUATION if key else T_ROUTINE_EQUATION)
        self.wait(W_AFTER_KEY if key else 0.6)
        return eq

    # ================================================================
    #  PART A — Given AB=AC=25, angle B=51°, find BC
    # ================================================================
    def part_a(self):
        self.show_part_header("a")

        # Problem Statement
        prob_title = MathTex(
            r"\text{Të dhëna:}",
            font_size=STEP_TITLE_SIZE + 6, color=STEP_TITLE_COLOR,
        )
        prob_line1 = MathTex(
            r"\text{Trekëndëshi } ABC, \quad AB = AC = 25 \text{ mm}",
            font_size=36,
        )
        prob_line2 = MathTex(r"\angle B = 51^{\circ}", font_size=36)
        prob_ask = MathTex(
            r"\text{Gjeni: } BC = \text{ ?}",
            font_size=34, color=STEP_TITLE_COLOR,
        )
        self.show_problem(prob_title, prob_line1, prob_line2, prob_ask)

        # Draw Triangle ABC
        angle_B_rad = 51 * DEGREES
        AB_vis = 3.2
        BH_vis = AB_vis * np.cos(angle_B_rad)
        AH_vis = AB_vis * np.sin(angle_B_rad)

        center_shift = DOWN * 0.3
        B_c = np.array([-BH_vis, -AH_vis / 2, 0]) + center_shift
        C_c = np.array([BH_vis, -AH_vis / 2, 0]) + center_shift
        A_c = np.array([0, AH_vis / 2, 0]) + center_shift
        H_c = np.array([0, -AH_vis / 2, 0]) + center_shift

        tri = Polygon(A_c, B_c, C_c, color=SHAPE_COLOR, stroke_width=3)
        lA = MathTex("A", font_size=36, color=WHITE).next_to(A_c, UP, buff=0.15)
        lB = MathTex("B", font_size=36, color=WHITE).next_to(B_c, DL, buff=0.15)
        lC = MathTex("C", font_size=36, color=WHITE).next_to(C_c, DR, buff=0.15)

        self.play(Create(tri), run_time=T_SHAPE_CREATE)
        self.play(FadeIn(lA), FadeIn(lB), FadeIn(lC), run_time=0.6)
        self.wait(1)

        # Side labels & tick marks
        s_AB = MathTex("25", font_size=28, color=LABEL_COLOR)
        s_AB.move_to(self.midpoint(A_c, B_c) + self.perp_offset(A_c, B_c, -0.4))
        s_AC = MathTex("25", font_size=28, color=LABEL_COLOR)
        s_AC.move_to(self.midpoint(A_c, C_c) + self.perp_offset(A_c, C_c, 0.4))
        t1 = self.tick_mark(A_c, B_c, size=0.12)
        t2 = self.tick_mark(A_c, C_c, size=0.12)

        self.play(FadeIn(s_AB), FadeIn(s_AC), Create(t1), Create(t2), run_time=0.8)

        # Angle B arc
        ang_B_arc = self.angle_arc(B_c, C_c, A_c, radius=0.45, color=ANSWER_COLOR)
        ang_B_lbl = MathTex("51^{\\circ}", font_size=24, color=ANSWER_COLOR)
        ang_B_lbl.move_to(self.angle_label_pos(B_c, C_c, A_c, 0.75))

        self.play(Create(ang_B_arc), FadeIn(ang_B_lbl), run_time=0.8)
        self.wait(2)

        # Move triangle left
        all_tri_objects = VGroup(tri, lA, lB, lC, s_AB, s_AC, t1, t2, ang_B_arc, ang_B_lbl)
        self.play(all_tri_objects.animate.shift(LEFT * 3.2), run_time=T_LAYOUT_SHIFT)
        self.wait(0.5)

        A = A_c + LEFT * 3.2
        B = B_c + LEFT * 3.2
        C = C_c + LEFT * 3.2
        H = H_c + LEFT * 3.2

        div = make_divider()
        self.play(FadeIn(div), run_time=0.3)

        # ── Steps 1–3 ──

        s1t = self._title("Hapi 1: Këndet e bazës", y_pos=3.2)

        s1txt = self._text([
            r"\text{Meqë } AB = AC\text{, trekëndëshi është}",
            r"\text{dybrinjënjëshëm. Këndet e bazës}",
            r"\text{janë të barabarta:}",
        ], s1t)
        self.wait(2)

        s1eq = self._eq(
            r"\angle C = \angle B = 51^{\circ}",
            s1txt, color=ANSWER_COLOR, fs=34, key=True,
        )

        # Show angle C on triangle
        ang_C_arc = self.angle_arc(C, A, B, radius=0.45, color=ANSWER_COLOR)
        ang_C_lbl = MathTex("51^{\\circ}", font_size=24, color=ANSWER_COLOR)
        ang_C_lbl.move_to(self.angle_label_pos(C, A, B, 0.75))
        self.play(Create(ang_C_arc), FadeIn(ang_C_lbl), run_time=1)
        self.wait(2)

        # Step 2: ∠A = 78°
        s2t = self._title("Hapi 2: Këndi në kulm", ref=s1eq)

        s2eq = self._eq(
            r"\angle A = 180^{\circ} - 51^{\circ} - 51^{\circ} = 78^{\circ}",
            s2t, fs=32,
        )

        # Show angle A arc briefly on triangle
        ang_A_arc = self.angle_arc(A, B, C, radius=0.3, color=HIGHLIGHT_COLOR)
        ang_A_lbl = MathTex("78^{\\circ}", font_size=20, color=HIGHLIGHT_COLOR)
        ang_A_lbl.move_to(self.angle_label_pos(A, B, C, 0.55))
        self.play(Create(ang_A_arc), FadeIn(ang_A_lbl), run_time=0.6)
        self.wait(3)

        # Step 3: Altitude — fade angle A first to avoid overlap with dashed line
        self.play(FadeOut(ang_A_arc), FadeOut(ang_A_lbl), run_time=0.4)

        s3t = self._title("Hapi 3: Lartësia", ref=s2eq)

        s3txt = self._text([
            r"\text{Heqim lartësinë } AH \perp BC\text{.}",
            r"\text{Ajo ndan bazën përgjysmë.}",
        ], s3t, buff=0.2)

        alt = DashedLine(A, H, color=AUX_COLOR, dash_length=0.1, stroke_width=2.5)
        ra = self.right_angle_mark(H, C, A, size=0.2, color=AUX_COLOR)
        lH_mob = MathTex("H", font_size=32).next_to(H, DOWN, buff=0.15)

        self.play(Create(alt), run_time=0.8)
        self.play(Create(ra), FadeIn(lH_mob), run_time=0.5)
        self.wait(2)

        # Transition: clear calc column
        calc1 = VGroup(s1t, s1txt, s1eq, s2t, s2eq, s3t, s3txt)
        self.play(FadeOut(calc1), FadeOut(div), run_time=0.6)
        self.wait(0.5)

        div2 = make_divider()
        self.play(FadeIn(div2), run_time=0.2)

        # ── Steps 4–5 ──

        s4t = self._title("Hapi 4: Gjejmë BH", y_pos=3.0)

        s4txt = self._text([
            r"\text{Në trekëndëshin kënddrejtë } ABH\text{:}",
        ], s4t, buff=0.3)
        self.wait(2)

        eq4a = self._eq(r"\cos 51^{\circ} = \frac{BH}{AB}", s4txt, key=True, fs=36)
        eq4b = self._eq(r"BH = 25 \cdot \cos 51^{\circ}", eq4a, fs=34)
        eq4c = self._eq(
            r"BH \approx 15{,}73 \text{ mm}",
            eq4b, color=LABEL_COLOR, fs=36, key=True,
        )

        # Step 5: BC = 2·BH
        s5t = self._title("Hapi 5: Gjejmë BC", ref=eq4c)

        eq5a = self._eq(r"BC = 2 \times BH", s5t, fs=34)
        eq5b = self._eq(
            r"BC = 2 \times 15{,}73 \approx 31{,}5 \text{ mm}",
            eq5a, color=ANSWER_COLOR, fs=36, key=True,
        )

        box = make_answer_box(eq5b)
        self.play(Create(box), run_time=0.6)

        # Label BC on triangle
        s_BC = MathTex(r"\approx 31{,}5 \text{ mm}", font_size=24, color=ANSWER_COLOR)
        s_BC.next_to(Line(B, C), DOWN, buff=0.3)
        self.play(FadeIn(s_BC), run_time=0.6)
        self.wait(4)

    # ================================================================
    #  PART B — Given PQ=QR=7, PR=4, find all angles
    # ================================================================
    def part_b(self):
        self.show_part_header("b")

        # Problem Statement
        prob_title = MathTex(
            r"\text{Të dhëna:}",
            font_size=STEP_TITLE_SIZE + 6, color=STEP_TITLE_COLOR,
        )
        prob_line1 = MathTex(
            r"\text{Trekëndëshi } PQR, \quad PQ = QR = 7 \text{ cm}",
            font_size=36,
        )
        prob_line2 = MathTex(r"PR = 4 \text{ cm}", font_size=36)
        prob_ask = MathTex(
            r"\text{Gjeni: Të gjitha këndet}",
            font_size=34, color=STEP_TITLE_COLOR,
        )
        self.show_problem(prob_title, prob_line1, prob_line2, prob_ask)

        # Draw Triangle PQR
        scale_f = 2.8 / 4
        PQ_v = 7 * scale_f
        PH_v = 2.8 / 2
        QH_v = np.sqrt(PQ_v**2 - PH_v**2)

        center_shift = DOWN * 0.3
        P_c = np.array([-PH_v, -QH_v / 2, 0]) + center_shift
        R_c = np.array([PH_v, -QH_v / 2, 0]) + center_shift
        Q_c = np.array([0, QH_v / 2, 0]) + center_shift
        H_c = np.array([0, -QH_v / 2, 0]) + center_shift

        tri = Polygon(P_c, Q_c, R_c, color=SHAPE_COLOR, stroke_width=3)
        lP = MathTex("P", font_size=36, color=WHITE).next_to(P_c, DL, buff=0.15)
        lQ = MathTex("Q", font_size=36, color=WHITE).next_to(Q_c, UP, buff=0.15)
        lR = MathTex("R", font_size=36, color=WHITE).next_to(R_c, DR, buff=0.15)

        self.play(Create(tri), run_time=T_SHAPE_CREATE)
        self.play(FadeIn(lP), FadeIn(lQ), FadeIn(lR), run_time=0.6)
        self.wait(1)

        # Side labels & tick marks
        s_PQ = MathTex("7", font_size=28, color=LABEL_COLOR)
        s_PQ.move_to(self.midpoint(P_c, Q_c) + self.perp_offset(P_c, Q_c, -0.35))
        s_QR = MathTex("7", font_size=28, color=LABEL_COLOR)
        s_QR.move_to(self.midpoint(Q_c, R_c) + self.perp_offset(Q_c, R_c, 0.35))
        s_PR = MathTex("4", font_size=28, color=LABEL_COLOR)
        s_PR.next_to(Line(P_c, R_c), DOWN, buff=0.25)
        t1 = self.tick_mark(P_c, Q_c, size=0.12)
        t2 = self.tick_mark(Q_c, R_c, size=0.12)

        self.play(FadeIn(s_PQ), FadeIn(s_QR), FadeIn(s_PR), Create(t1), Create(t2), run_time=0.8)
        self.wait(2)

        # Move triangle left
        all_tri = VGroup(tri, lP, lQ, lR, s_PQ, s_QR, s_PR, t1, t2)
        self.play(all_tri.animate.shift(LEFT * 3.2), run_time=T_LAYOUT_SHIFT)
        self.wait(0.5)

        P = P_c + LEFT * 3.2
        R = R_c + LEFT * 3.2
        Q = Q_c + LEFT * 3.2
        H_pt = H_c + LEFT * 3.2

        div = make_divider()
        self.play(FadeIn(div), run_time=0.2)

        # ── Steps 1–2 ──

        s1t = self._title("Hapi 1: Lartësia", y_pos=3.0)

        s1txt = self._text([
            r"\text{Meqë } PQ = QR\text{, trekëndëshi është}",
            r"\text{dybrinjënjëshëm. Heqim lartësinë}",
            r"QH \perp PR\text{, që ndan bazën përgjysmë:}",
        ], s1t)
        self.wait(2)

        alt = DashedLine(Q, H_pt, color=AUX_COLOR, dash_length=0.1, stroke_width=2.5)
        ra = self.right_angle_mark(H_pt, R, Q, size=0.2, color=AUX_COLOR)
        lH_mob = MathTex("H", font_size=32).next_to(H_pt, DOWN, buff=0.15)

        self.play(Create(alt), run_time=0.8)
        self.play(Create(ra), FadeIn(lH_mob), run_time=0.5)
        self.wait(2)

        s1eq = self._eq(
            r"PH = HR = \frac{4}{2} = 2 \text{ cm}",
            s1txt, buff=0.3, fs=32,
        )
        self.wait(2)

        # Step 2: QH via Pythagorean
        s2t = self._title("Hapi 2: Gjejmë QH", ref=s1eq, buff=0.45)

        s2txt = self._text([
            r"\text{Teorema e Pitagorës në } \triangle QPH\text{:}",
        ], s2t, buff=0.2)
        self.wait(2)

        eq2a = self._eq(r"QH^2 = PQ^2 - PH^2", s2txt, fs=32)
        eq2b = self._eq(r"QH^2 = 49 - 4 = 45", eq2a, fs=32)
        eq2c = self._eq(
            r"QH = \sqrt{45} = 3\sqrt{5} \approx 6{,}71 \text{ cm}",
            eq2b, color=LABEL_COLOR, fs=32, key=True,
        )

        # Transition: clear calc column
        calc1 = VGroup(s1t, s1txt, s1eq, s2t, s2txt, eq2a, eq2b, eq2c)
        self.play(FadeOut(calc1), run_time=0.6)
        self.wait(0.5)

        # ── Steps 3–4 ──

        s3t = self._title("Hapi 3: Gjejmë këndin P", y_pos=3.0)

        s3txt = self._text([
            r"\text{Në trekëndëshin kënddrejtë } QPH\text{,}",
            r"\text{përdorim sinusin:}",
        ], s3t)
        self.wait(2)

        eq3a = self._eq(
            r"\sin P = \frac{QH}{PQ} = \frac{3\sqrt{5}}{7}",
            s3txt, buff=0.3, fs=34, key=True,
        )
        eq3b = self._eq(r"\sin P \approx 0{,}9583", eq3a, fs=34)
        eq3c = self._eq(
            r"\angle P \approx 73{,}4^{\circ}",
            eq3b, color=ANSWER_COLOR, fs=38, key=True,
        )

        # Transition: clear calc column
        calc2 = VGroup(s3t, s3txt, eq3a, eq3b, eq3c)
        self.play(FadeOut(calc2), run_time=0.6)
        self.wait(0.5)

        # Step 4: ∠R = ∠P, find ∠Q
        s4t = self._title("Hapi 4: Këndet e tjera", y_pos=3.0)

        s4txt = self._text([
            r"\text{Këndet e bazës janë të barabarta:}",
        ], s4t)
        self.wait(2)

        eq4a = self._eq(
            r"\angle R = \angle P \approx 73{,}4^{\circ}",
            s4txt, color=ANSWER_COLOR, fs=34, key=True,
        )
        eq4b = self._eq(
            r"\angle Q = 180^{\circ} - 73{,}4^{\circ} - 73{,}4^{\circ}",
            eq4a, fs=32,
        )
        eq4c = self._eq(
            r"\angle Q \approx 33{,}2^{\circ}",
            eq4b, color=HIGHLIGHT_COLOR, fs=38, key=True,
        )

        # Transition: clear calc column and divider
        calc3 = VGroup(s4t, s4txt, eq4a, eq4b, eq4c, div)
        self.play(FadeOut(calc3), run_time=0.6)
        self.wait(0.5)

        # Fade altitude before showing angle arcs to avoid overlap at vertex Q
        self.play(FadeOut(alt), FadeOut(ra), FadeOut(lH_mob), run_time=0.4)

        # Angle arcs on triangle
        ang_P_arc = self.angle_arc(P, R, Q, radius=0.4, color=ANSWER_COLOR)
        ang_P_lbl = MathTex("73{,}4^{\\circ}", font_size=22, color=ANSWER_COLOR)
        ang_P_lbl.move_to(self.angle_label_pos(P, R, Q, 0.7))

        ang_R_arc = self.angle_arc(R, Q, P, radius=0.4, color=ANSWER_COLOR)
        ang_R_lbl = MathTex("73{,}4^{\\circ}", font_size=22, color=ANSWER_COLOR)
        ang_R_lbl.move_to(self.angle_label_pos(R, Q, P, 0.7))

        ang_Q_arc = self.angle_arc(Q, P, R, radius=0.35, color=HIGHLIGHT_COLOR)
        ang_Q_lbl = MathTex("33{,}2^{\\circ}", font_size=22, color=HIGHLIGHT_COLOR)
        ang_Q_lbl.move_to(self.angle_label_pos(Q, P, R, 0.65))

        self.play(
            Create(ang_P_arc), Create(ang_R_arc), Create(ang_Q_arc),
            FadeIn(ang_P_lbl), FadeIn(ang_R_lbl), FadeIn(ang_Q_lbl),
            run_time=1.2,
        )
        self.wait(2)

        # Final answer box
        answer_title = MathTex(
            r"\text{Përgjigja:}",
            font_size=STEP_TITLE_SIZE + 6, color=STEP_TITLE_COLOR,
        )
        ans_P = MathTex(r"\angle P \approx 73{,}4^{\circ}", font_size=38, color=ANSWER_COLOR)
        ans_R = MathTex(r"\angle R \approx 73{,}4^{\circ}", font_size=38, color=ANSWER_COLOR)
        ans_Q = MathTex(r"\angle Q \approx 33{,}2^{\circ}", font_size=38, color=HIGHLIGHT_COLOR)

        answer_block = VGroup(answer_title, ans_P, ans_R, ans_Q)
        answer_block.arrange(DOWN, buff=0.35, center=True)
        answer_block.move_to(RIGHT * PX)

        ans_box = make_answer_box(VGroup(ans_P, ans_R, ans_Q))

        self.play(FadeIn(answer_block), run_time=1)
        self.play(Create(ans_box), run_time=0.6)
        self.wait(4)
