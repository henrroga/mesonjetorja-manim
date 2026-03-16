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
    CALC_TOP, PX,
)


class Ushtrimi4(ExerciseScene):
    """
    Ushtrimi 4 — Njësia 7.2A — Matematika 10-11: Pjesa II

    Visual storytelling approach — no voiceover.
    Every computed value animates onto the figure.
    Sub-shapes are highlighted when worked on.
    """

    exercise_number = 4
    unit = "7.2A"
    parts = ["a", "b"]

    # ================================================================
    #  PART A — Triangle ABC: AB = AC = 25 mm, ∠B = 51°, find BC
    # ================================================================
    def part_a(self):
        self.show_part_header("a")

        # ── Problem statement ──
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

        # ── Build triangle ABC ──
        angle_B_rad = 51 * DEGREES
        AB_vis = 3.0
        BH_vis = AB_vis * np.cos(angle_B_rad)
        AH_vis = AB_vis * np.sin(angle_B_rad)

        cy = DOWN * 0.2
        B_c = np.array([-BH_vis, -AH_vis / 2, 0]) + cy
        C_c = np.array([BH_vis, -AH_vis / 2, 0]) + cy
        A_c = np.array([0, AH_vis / 2, 0]) + cy
        H_c = np.array([0, -AH_vis / 2, 0]) + cy

        tri = Polygon(A_c, B_c, C_c, color=SHAPE_COLOR, stroke_width=3)
        lA = MathTex("A", font_size=32, color=WHITE).next_to(A_c, UP, buff=0.18)
        lB = MathTex("B", font_size=32, color=WHITE).next_to(B_c, DL, buff=0.18)
        lC = MathTex("C", font_size=32, color=WHITE).next_to(C_c, DR, buff=0.18)

        self.play(Create(tri), run_time=T_SHAPE_CREATE)
        self.play(FadeIn(lA), FadeIn(lB), FadeIn(lC), run_time=0.6)
        self.wait(1)

        # Side length labels + tick marks
        s_AB = MathTex("25", font_size=26, color=LABEL_COLOR)
        s_AB.move_to(self.midpoint(A_c, B_c) + self.perp_offset(A_c, B_c, -0.40))
        s_AC = MathTex("25", font_size=26, color=LABEL_COLOR)
        s_AC.move_to(self.midpoint(A_c, C_c) + self.perp_offset(A_c, C_c, 0.40))
        t1 = self.tick_mark(A_c, B_c, size=0.12)
        t2 = self.tick_mark(A_c, C_c, size=0.12)

        self.play(FadeIn(s_AB), FadeIn(s_AC), Create(t1), Create(t2), run_time=0.8)
        self.wait(1)

        # Angle B arc
        ang_B_arc = self.angle_arc(B_c, C_c, A_c, radius=0.45, color=ANSWER_COLOR)
        ang_B_lbl = MathTex("51^{\\circ}", font_size=22, color=ANSWER_COLOR)
        ang_B_lbl.move_to(self.angle_label_pos(B_c, C_c, A_c, 0.78))
        self.play(Create(ang_B_arc), FadeIn(ang_B_lbl), run_time=0.8)
        self.wait(2)

        # ── Shift triangle left ──
        all_tri = VGroup(tri, lA, lB, lC, s_AB, s_AC, t1, t2, ang_B_arc, ang_B_lbl)
        self.play(all_tri.animate.shift(LEFT * 3.2), run_time=T_LAYOUT_SHIFT)
        self.wait(0.5)

        A = A_c + LEFT * 3.2
        B = B_c + LEFT * 3.2
        C = C_c + LEFT * 3.2
        H = H_c + LEFT * 3.2

        div = make_divider()
        self.play(FadeIn(div), run_time=0.3)

        # ────────────────────────────────────────────
        # Step 1: Base angles — with visual feedback on figure
        # ────────────────────────────────────────────
        s1t = self.panel_title("Hapi 1: Këndet e bazës", y_pos=3.2)

        s1txt = self.panel_text([
            r"\text{Meqë } AB = AC\text{, trekëndëshi}",
            r"\text{është dybrinjënjëshëm.}",
            r"\text{Këndet e bazës janë të barabarta:}",
        ], s1t)
        self.wait(2)

        # Flash the equal sides on the figure to show WHY
        self.play(
            Indicate(s_AB, color=YELLOW, scale_factor=1.3),
            Indicate(s_AC, color=YELLOW, scale_factor=1.3),
            run_time=0.6,
        )
        self.wait(0.5)

        s1eq = self.panel_eq(
            r"\angle C = \angle B = 51^{\circ}",
            s1txt, color=ANSWER_COLOR, font_size=34, key=True,
        )

        # Transfer: show angle C appearing on figure
        ang_C_arc = self.angle_arc(C, A, B, radius=0.45, color=ANSWER_COLOR)
        ang_C_lbl = MathTex("51^{\\circ}", font_size=22, color=ANSWER_COLOR)
        ang_C_lbl.move_to(self.angle_label_pos(C, A, B, 0.78))
        self.transfer_value(s1eq, VGroup(ang_C_arc, ang_C_lbl))
        self.wait(2)

        # ────────────────────────────────────────────
        # Step 2: Vertex angle
        # ────────────────────────────────────────────
        s2t = self.panel_title("Hapi 2: Këndi në kulm", ref=s1eq)

        s2txt = self.panel_text([
            r"\text{Shuma e këndeve} = 180^{\circ}\text{:}",
        ], s2t, buff=0.2)
        self.wait(1.5)

        s2eq = self.panel_eq(
            r"\angle A = 180^{\circ} - 51^{\circ} - 51^{\circ} = 78^{\circ}",
            s2txt, font_size=30,
        )

        # Transfer angle A to figure (briefly — will fade before altitude)
        ang_A_arc = self.angle_arc(A, B, C, radius=0.28, color=HIGHLIGHT_COLOR)
        ang_A_lbl = MathTex("78^{\\circ}", font_size=18, color=HIGHLIGHT_COLOR)
        ang_A_lbl.move_to(self.angle_label_pos(A, B, C, 0.55))
        self.transfer_value(s2eq, VGroup(ang_A_arc, ang_A_lbl))
        self.wait(2.5)

        # ────────────────────────────────────────────
        # Step 3: Altitude — highlight sub-triangle
        # ────────────────────────────────────────────
        # Fade angle A (altitude will pass through it)
        self.play(FadeOut(ang_A_arc), FadeOut(ang_A_lbl), run_time=0.4)

        s3t = self.panel_title("Hapi 3: Lartësia", ref=s2eq)

        s3txt = self.panel_text([
            r"\text{Heqim lartësinë } AH \perp BC\text{.}",
            r"\text{Ajo ndan bazën përgjysmë.}",
        ], s3t, buff=0.2)

        # Draw altitude
        alt = DashedLine(A, H, color=AUX_COLOR, dash_length=0.1, stroke_width=2.5)
        ra = self.right_angle_mark(H, C, A, size=0.18, color=AUX_COLOR)
        lH_mob = MathTex("H", font_size=28).next_to(H, DOWN, buff=0.18)
        lH_mob.shift(LEFT * 0.25)

        self.play(Create(alt), run_time=0.8)
        self.play(Create(ra), FadeIn(lH_mob), run_time=0.5)
        self.wait(2)

        # ── Clear right panel ──
        calc1 = VGroup(s1t, s1txt, s1eq, s2t, s2txt, s2eq, s3t, s3txt)
        self.play(FadeOut(calc1), FadeOut(div), run_time=0.6)
        self.wait(0.5)

        div2 = make_divider()
        self.play(FadeIn(div2), run_time=0.2)

        # ────────────────────────────────────────────
        # Step 4: cos → BH — highlight right triangle ABH
        # ────────────────────────────────────────────

        # Highlight right triangle ABH with shading
        sub_ABH = Polygon(A, B, H,
                          fill_color=SHAPE_COLOR, fill_opacity=0.12,
                          stroke_color=SHAPE_COLOR, stroke_width=2)
        # Dim the other half of the triangle
        self.play(
            FadeIn(sub_ABH),
            tri.animate.set_stroke(opacity=0.3),
            ang_C_arc.animate.set_stroke(opacity=0.3),
            ang_C_lbl.animate.set_opacity(0.3),
            s_AC.animate.set_opacity(0.3),
            t2.animate.set_stroke(opacity=0.3),
            run_time=0.6,
        )
        self.wait(1)

        s4t = self.panel_title("Hapi 4: Gjejmë BH", y_pos=3.0)

        s4txt = self.panel_text([
            r"\text{Në trekëndëshin kënddrejtë } ABH\text{:}",
        ], s4t, buff=0.3)
        self.wait(1.5)

        # Flash angle B on figure before using it
        self.play(Indicate(ang_B_arc, color=YELLOW), run_time=0.5)

        eq4a = self.panel_eq(
            r"\cos 51^{\circ} = \frac{BH}{AB}",
            s4txt, key=True, font_size=36,
        )

        # Flash AB side (the hypotenuse we know)
        self.play(Indicate(s_AB, color=YELLOW, scale_factor=1.3), run_time=0.5)

        eq4b = self.panel_eq(r"BH = 25 \cdot \cos 51^{\circ}", eq4a, font_size=34)
        eq4c = self.panel_eq(
            r"BH \approx 15{,}73 \text{ mm}",
            eq4b, color=LABEL_COLOR, font_size=36, key=True,
        )

        # Transfer BH value to figure — place it on segment BH
        bh_lbl = MathTex("15{,}73", font_size=20, color=LABEL_COLOR)
        bh_mid = self.midpoint(B, H)
        bh_lbl.move_to(bh_mid + DOWN * 0.25)
        self.transfer_value(eq4c, bh_lbl)
        self.wait(1.5)

        # ────────────────────────────────────────────
        # Step 5: BC = 2·BH — restore full triangle
        # ────────────────────────────────────────────
        s5t = self.panel_title("Hapi 5: Gjejmë BC", ref=eq4c)

        s5txt = self.panel_text([
            r"\text{Meqë } H \text{ ndan bazën përgjysmë:}",
        ], s5t, buff=0.2)
        self.wait(1)

        # Restore full triangle visibility
        self.play(
            FadeOut(sub_ABH),
            tri.animate.set_stroke(opacity=1),
            ang_C_arc.animate.set_stroke(opacity=1),
            ang_C_lbl.animate.set_opacity(1),
            s_AC.animate.set_opacity(1),
            t2.animate.set_stroke(opacity=1),
            FadeOut(bh_lbl),
            run_time=0.5,
        )

        eq5a = self.panel_eq(r"BC = 2 \times BH", s5txt, font_size=34)
        eq5b = self.panel_eq(
            r"BC = 2 \times 15{,}73 \approx 31{,}5 \text{ mm}",
            eq5a, color=ANSWER_COLOR, font_size=34, key=True,
        )

        box = make_answer_box(eq5b)
        self.play(Create(box), run_time=0.6)
        self.wait(1.5)

        # Fade altitude so BC label doesn't overlap with H label
        self.play(FadeOut(alt), FadeOut(ra), FadeOut(lH_mob), run_time=0.4)

        # Transfer final BC value to figure
        s_BC = MathTex(r"BC \approx 31{,}5 \text{ mm}", font_size=22, color=ANSWER_COLOR)
        s_BC.next_to(Line(B, C), DOWN, buff=0.25)
        self.transfer_value(eq5b, s_BC)

        # Highlight the base to emphasize the answer
        base_highlight = Line(B, C, color=ANSWER_COLOR, stroke_width=5)
        self.play(Create(base_highlight), run_time=0.6)
        self.wait(4)

    # ================================================================
    #  PART B — Triangle PQR: PQ = QR = 7 cm, PR = 4 cm, find angles
    # ================================================================
    def part_b(self):
        self.show_part_header("b")

        # ── Problem statement ──
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

        # ── Build triangle PQR ──
        scale_f = 2.8 / 4
        PQ_v = 7 * scale_f
        PH_v = 2.8 / 2
        QH_v = np.sqrt(PQ_v**2 - PH_v**2)

        cy = DOWN * 0.1
        P_c = np.array([-PH_v, -QH_v / 2, 0]) + cy
        R_c = np.array([PH_v, -QH_v / 2, 0]) + cy
        Q_c = np.array([0, QH_v / 2, 0]) + cy
        H_c = np.array([0, -QH_v / 2, 0]) + cy

        tri = Polygon(P_c, Q_c, R_c, color=SHAPE_COLOR, stroke_width=3)
        lP = MathTex("P", font_size=32, color=WHITE).next_to(P_c, DL, buff=0.18)
        lQ = MathTex("Q", font_size=32, color=WHITE).next_to(Q_c, UP, buff=0.18)
        lR = MathTex("R", font_size=32, color=WHITE).next_to(R_c, DR, buff=0.18)

        self.play(Create(tri), run_time=T_SHAPE_CREATE)
        self.play(FadeIn(lP), FadeIn(lQ), FadeIn(lR), run_time=0.6)
        self.wait(1)

        # Side labels
        s_PQ = MathTex("7", font_size=26, color=LABEL_COLOR)
        s_PQ.move_to(self.midpoint(P_c, Q_c) + self.perp_offset(P_c, Q_c, -0.38))
        s_QR = MathTex("7", font_size=26, color=LABEL_COLOR)
        s_QR.move_to(self.midpoint(Q_c, R_c) + self.perp_offset(Q_c, R_c, 0.38))

        # "4" shifted right from center to avoid overlap with future "H" label
        s_PR = MathTex("4", font_size=26, color=LABEL_COLOR)
        pr_mid = self.midpoint(P_c, R_c)
        s_PR.move_to(pr_mid + DOWN * 0.30 + RIGHT * 0.7)

        t1 = self.tick_mark(P_c, Q_c, size=0.12)
        t2 = self.tick_mark(Q_c, R_c, size=0.12)

        self.play(
            FadeIn(s_PQ), FadeIn(s_QR), FadeIn(s_PR),
            Create(t1), Create(t2),
            run_time=0.8,
        )
        self.wait(2)

        # ── Shift triangle left ──
        all_tri = VGroup(tri, lP, lQ, lR, s_PQ, s_QR, s_PR, t1, t2)
        self.play(all_tri.animate.shift(LEFT * 3.2), run_time=T_LAYOUT_SHIFT)
        self.wait(0.5)

        P = P_c + LEFT * 3.2
        R = R_c + LEFT * 3.2
        Q = Q_c + LEFT * 3.2
        H_pt = H_c + LEFT * 3.2

        div = make_divider()
        self.play(FadeIn(div), run_time=0.2)

        # ────────────────────────────────────────────
        # Step 1: Altitude — draw on figure with explanation
        # ────────────────────────────────────────────
        s1t = self.panel_title("Hapi 1: Lartësia", y_pos=3.0)

        s1txt = self.panel_text([
            r"\text{Meqë } PQ = QR\text{, trekëndëshi}",
            r"\text{është dybrinjënjëshëm.}",
            r"\text{Heqim lartësinë } QH \perp PR\text{.}",
        ], s1t)
        self.wait(2)

        # Flash equal sides before drawing altitude
        self.play(
            Indicate(s_PQ, color=YELLOW, scale_factor=1.3),
            Indicate(s_QR, color=YELLOW, scale_factor=1.3),
            run_time=0.6,
        )
        self.wait(0.5)

        # Draw altitude on figure
        alt = DashedLine(Q, H_pt, color=AUX_COLOR, dash_length=0.1, stroke_width=2.5)
        ra = self.right_angle_mark(H_pt, R, Q, size=0.18, color=AUX_COLOR)
        lH_mob = MathTex("H", font_size=28).next_to(H_pt, DOWN, buff=0.18)
        lH_mob.shift(LEFT * 0.3)

        self.play(Create(alt), run_time=0.8)
        self.play(Create(ra), FadeIn(lH_mob), run_time=0.5)
        self.wait(2)

        s1eq = self.panel_eq(
            r"PH = HR = \frac{4}{2} = 2 \text{ cm}",
            s1txt, buff=0.3, font_size=32,
        )

        # Transfer: show "2" labels on PH and HR segments
        ph_lbl = MathTex("2", font_size=20, color=LABEL_COLOR)
        ph_lbl.move_to(self.midpoint(P, H_pt) + DOWN * 0.22)
        hr_lbl = MathTex("2", font_size=20, color=LABEL_COLOR)
        hr_lbl.move_to(self.midpoint(H_pt, R) + DOWN * 0.22)
        self.transfer_value(s1eq, VGroup(ph_lbl, hr_lbl))
        self.wait(2)

        # ────────────────────────────────────────────
        # Step 2: QH via Pythagorean — highlight right triangle QPH
        # ────────────────────────────────────────────
        s2t = self.panel_title("Hapi 2: Gjejmë QH", ref=s1eq, buff=0.45)

        # Highlight left right-triangle QPH
        sub_QPH = Polygon(Q, P, H_pt,
                          fill_color=SHAPE_COLOR, fill_opacity=0.12,
                          stroke_color=SHAPE_COLOR, stroke_width=2)
        self.play(
            FadeIn(sub_QPH),
            tri.animate.set_stroke(opacity=0.3),
            s_QR.animate.set_opacity(0.3),
            t2.animate.set_stroke(opacity=0.3),
            hr_lbl.animate.set_opacity(0.3),
            run_time=0.6,
        )

        s2txt = self.panel_text([
            r"\text{Teorema e Pitagorës në } \triangle QPH\text{:}",
        ], s2t, buff=0.2)
        self.wait(2)

        eq2a = self.panel_eq(r"QH^2 = PQ^2 - PH^2", s2txt, font_size=32)

        # Flash PQ and PH on figure when used
        self.play(Indicate(s_PQ, color=YELLOW), run_time=0.4)

        eq2b = self.panel_eq(r"QH^2 = 49 - 4 = 45", eq2a, font_size=32)
        eq2c = self.panel_eq(
            r"QH = \sqrt{45} = 3\sqrt{5} \approx 6{,}71 \text{ cm}",
            eq2b, color=LABEL_COLOR, font_size=30, key=True,
        )

        # Transfer QH value to figure
        qh_lbl = MathTex("6{,}71", font_size=20, color=LABEL_COLOR)
        qh_mid = self.midpoint(Q, H_pt)
        qh_lbl.move_to(qh_mid + RIGHT * 0.35)
        self.transfer_value(eq2c, qh_lbl)
        self.wait(1.5)

        # Restore full triangle
        self.play(
            FadeOut(sub_QPH),
            tri.animate.set_stroke(opacity=1),
            s_QR.animate.set_opacity(1),
            t2.animate.set_stroke(opacity=1),
            hr_lbl.animate.set_opacity(1),
            run_time=0.5,
        )

        # ── Clear right panel ──
        calc1 = VGroup(s1t, s1txt, s1eq, s2t, s2txt, eq2a, eq2b, eq2c)
        self.play(FadeOut(calc1), run_time=0.6)
        self.wait(0.5)

        # ────────────────────────────────────────────
        # Step 3: angle P via sine — highlight right triangle again
        # ────────────────────────────────────────────
        s3t = self.panel_title("Hapi 3: Gjejmë këndin P", y_pos=3.0)

        # Highlight right triangle QPH again
        sub_QPH2 = Polygon(Q, P, H_pt,
                           fill_color=SHAPE_COLOR, fill_opacity=0.12,
                           stroke_color=SHAPE_COLOR, stroke_width=2)
        self.play(
            FadeIn(sub_QPH2),
            tri.animate.set_stroke(opacity=0.3),
            s_QR.animate.set_opacity(0.3),
            t2.animate.set_stroke(opacity=0.3),
            hr_lbl.animate.set_opacity(0.3),
            run_time=0.5,
        )

        s3txt = self.panel_text([
            r"\text{Në trekëndëshin kënddrejtë } QPH\text{,}",
            r"\text{përdorim sinusin:}",
        ], s3t)
        self.wait(2)

        # Flash QH and PQ on figure
        self.play(Indicate(qh_lbl, color=YELLOW), run_time=0.4)
        self.play(Indicate(s_PQ, color=YELLOW), run_time=0.4)

        eq3a = self.panel_eq(
            r"\sin P = \frac{QH}{PQ} = \frac{3\sqrt{5}}{7}",
            s3txt, buff=0.3, font_size=34, key=True,
        )
        eq3b = self.panel_eq(r"\sin P \approx 0{,}9583", eq3a, font_size=34)
        eq3c = self.panel_eq(
            r"\angle P \approx 73{,}4^{\circ}",
            eq3b, color=ANSWER_COLOR, font_size=36, key=True,
        )

        # Transfer angle P to figure
        ang_P_arc = self.angle_arc(P, R, Q, radius=0.40, color=ANSWER_COLOR)
        ang_P_lbl = MathTex("73{,}4^{\\circ}", font_size=20, color=ANSWER_COLOR)
        ang_P_lbl.move_to(self.angle_label_pos(P, R, Q, 0.72))

        # Restore triangle before showing arc
        self.play(
            FadeOut(sub_QPH2),
            tri.animate.set_stroke(opacity=1),
            s_QR.animate.set_opacity(1),
            t2.animate.set_stroke(opacity=1),
            hr_lbl.animate.set_opacity(1),
            run_time=0.4,
        )
        self.transfer_value(eq3c, VGroup(ang_P_arc, ang_P_lbl))
        self.wait(1.5)

        # ── Clear right panel ──
        calc2 = VGroup(s3t, s3txt, eq3a, eq3b, eq3c)
        self.play(FadeOut(calc2), run_time=0.6)
        self.wait(0.5)

        # ────────────────────────────────────────────
        # Step 4: remaining angles
        # ────────────────────────────────────────────
        s4t = self.panel_title("Hapi 4: Këndet e tjera", y_pos=3.0)

        s4txt = self.panel_text([
            r"\text{Këndet e bazës janë të barabarta:}",
        ], s4t)
        self.wait(2)

        eq4a = self.panel_eq(
            r"\angle R = \angle P \approx 73{,}4^{\circ}",
            s4txt, color=ANSWER_COLOR, font_size=34, key=True,
        )

        # Transfer angle R to figure
        ang_R_arc = self.angle_arc(R, Q, P, radius=0.40, color=ANSWER_COLOR)
        ang_R_lbl = MathTex("73{,}4^{\\circ}", font_size=20, color=ANSWER_COLOR)
        ang_R_lbl.move_to(self.angle_label_pos(R, Q, P, 0.72))
        self.transfer_value(eq4a, VGroup(ang_R_arc, ang_R_lbl))
        self.wait(1)

        eq4b_txt = self.panel_text([
            r"\text{Këndi në kulm:}",
        ], eq4a, buff=0.3)
        self.wait(1)

        eq4b = self.panel_eq(
            r"\angle Q = 180^{\circ} - 73{,}4^{\circ} - 73{,}4^{\circ}",
            eq4b_txt, font_size=32,
        )
        eq4c = self.panel_eq(
            r"\angle Q \approx 33{,}2^{\circ}",
            eq4b, color=HIGHLIGHT_COLOR, font_size=36, key=True,
        )

        # Fade altitude before showing angle Q arc (they overlap at vertex Q)
        self.play(
            FadeOut(alt), FadeOut(ra), FadeOut(lH_mob),
            FadeOut(qh_lbl), FadeOut(ph_lbl), FadeOut(hr_lbl),
            run_time=0.4,
        )

        # Transfer angle Q to figure (small angle — use small arc + font)
        ang_Q_arc = self.angle_arc(Q, P, R, radius=0.25, color=HIGHLIGHT_COLOR)
        ang_Q_lbl = MathTex("33{,}2^{\\circ}", font_size=18, color=HIGHLIGHT_COLOR)
        ang_Q_lbl.move_to(self.angle_label_pos(Q, P, R, 0.85))
        self.transfer_value(eq4c, VGroup(ang_Q_arc, ang_Q_lbl))
        self.wait(2)

        # ── Clear right panel + divider ──
        calc3 = VGroup(s4t, s4txt, eq4a, eq4b_txt, eq4b, eq4c, div)
        self.play(FadeOut(calc3), run_time=0.6)
        self.wait(0.5)

        # ── Final answer box ──
        answer_title = MathTex(
            r"\text{Përgjigja:}",
            font_size=STEP_TITLE_SIZE + 6, color=STEP_TITLE_COLOR,
        )
        ans_P = MathTex(r"\angle P \approx 73{,}4^{\circ}", font_size=36, color=ANSWER_COLOR)
        ans_R = MathTex(r"\angle R \approx 73{,}4^{\circ}", font_size=36, color=ANSWER_COLOR)
        ans_Q = MathTex(r"\angle Q \approx 33{,}2^{\circ}", font_size=36, color=HIGHLIGHT_COLOR)

        answer_block = VGroup(answer_title, ans_P, ans_R, ans_Q)
        answer_block.arrange(DOWN, buff=0.35, center=True)
        answer_block.set_x(PX)

        ans_box = make_answer_box(VGroup(ans_P, ans_R, ans_Q))

        self.play(FadeIn(answer_block), run_time=1)
        self.play(Create(ans_box), run_time=0.6)
        self.wait(4)
