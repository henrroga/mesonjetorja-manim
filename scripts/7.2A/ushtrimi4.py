from manim import *
import numpy as np


class Ushtrimi4(Scene):
    """
    Ushtrimi 4 - Njësia 7.2A
    Matematika 10-11: Pjesa II
    """

    def construct(self):
        self.camera.background_color = "#1a1a2e"

        # ====== TITLE ======
        title = Text(
            "Ushtrimi 4 — Njësia 7.2A",
            font_size=48,
            color=YELLOW,
            weight=BOLD,
        )
        source = Text(
            "Matematika 10-11: Pjesa II",
            font_size=30,
            color=GRAY_B,
        )
        source.next_to(title, DOWN, buff=0.4)

        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(source, shift=UP * 0.2), run_time=0.8)
        self.wait(2)
        self.play(FadeOut(title), FadeOut(source))
        self.wait(0.5)

        # ====== PART A ======
        self.part_a()

        # Clear screen
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)
        self.wait(0.8)

        # ====== PART B ======
        self.part_b()

        # Final
        self.wait(3)

    # ------------------------------------------------------------------ #
    #                            PART A                                   #
    # ------------------------------------------------------------------ #
    def part_a(self):
        # ----- Header (small, top-left) -----
        header = Text("Pjesa a)", font_size=32, color=YELLOW, weight=BOLD)
        header.to_corner(UL, buff=0.4)
        self.play(Write(header), run_time=0.6)

        # ----- Problem Statement (centered, full screen) -----
        prob_title = Text(
            "Të dhëna:",
            font_size=32,
            color=TEAL,
            weight=BOLD,
        )
        prob_line1 = MathTex(
            r"\text{Trekëndëshi } ABC, \quad AB = AC = 25 \text{ mm}",
            font_size=36,
        )
        prob_line2 = MathTex(
            r"\angle B = 51^{\circ}",
            font_size=36,
        )
        prob_ask = Text(
            "Gjeni: BC = ?",
            font_size=34,
            color=TEAL,
            weight=BOLD,
        )

        prob_group = VGroup(prob_title, prob_line1, prob_line2, prob_ask)
        prob_group.arrange(DOWN, buff=0.4, center=True)
        prob_group.move_to(ORIGIN)

        self.play(FadeIn(prob_group, shift=UP * 0.3), run_time=1.2)
        self.wait(3)
        self.play(FadeOut(prob_group), run_time=0.8)
        self.wait(0.5)

        # ----- Draw Triangle ABC (centered, large) -----
        angle_B_rad = 51 * DEGREES
        AB_vis = 3.2  # larger triangle
        BH_vis = AB_vis * np.cos(angle_B_rad)
        AH_vis = AB_vis * np.sin(angle_B_rad)

        # Center the triangle first
        B_c = np.array([-BH_vis, -AH_vis / 2, 0])
        C_c = np.array([BH_vis, -AH_vis / 2, 0])
        A_c = np.array([0, AH_vis / 2, 0])
        H_c = np.array([0, -AH_vis / 2, 0])

        # Shift down a bit so there's room for label A above
        center_shift = DOWN * 0.3
        B_c += center_shift
        C_c += center_shift
        A_c += center_shift
        H_c += center_shift

        tri = Polygon(A_c, B_c, C_c, color=BLUE_C, stroke_width=3)
        lA = MathTex("A", font_size=36, color=WHITE).next_to(A_c, UP, buff=0.15)
        lB = MathTex("B", font_size=36, color=WHITE).next_to(B_c, DL, buff=0.15)
        lC = MathTex("C", font_size=36, color=WHITE).next_to(C_c, DR, buff=0.15)

        tri_group = VGroup(tri, lA, lB, lC)

        self.play(Create(tri), run_time=1.2)
        self.play(FadeIn(lA), FadeIn(lB), FadeIn(lC), run_time=0.6)
        self.wait(1)

        # Side labels & tick marks
        s_AB = MathTex("25", font_size=28, color=YELLOW)
        s_AB.move_to(self.midpoint(A_c, B_c) + self.perp_offset(A_c, B_c, -0.4))
        s_AC = MathTex("25", font_size=28, color=YELLOW)
        s_AC.move_to(self.midpoint(A_c, C_c) + self.perp_offset(A_c, C_c, 0.4))
        t1 = self.tick_mark(A_c, B_c, size=0.12)
        t2 = self.tick_mark(A_c, C_c, size=0.12)

        self.play(
            FadeIn(s_AB), FadeIn(s_AC), Create(t1), Create(t2), run_time=0.8
        )

        # Angle B arc
        ang_B_arc = self.angle_arc(B_c, C_c, A_c, radius=0.45, color=GREEN)
        ang_B_lbl = MathTex("51^{\\circ}", font_size=24, color=GREEN)
        ang_B_lbl.move_to(self.angle_label_pos(B_c, C_c, A_c, 0.75))

        self.play(Create(ang_B_arc), FadeIn(ang_B_lbl), run_time=0.8)
        self.wait(2)

        # ----- Move triangle to the left to make room for calculations -----
        left_shift = LEFT * 3.2
        all_tri_objects = VGroup(
            tri, lA, lB, lC, s_AB, s_AC, t1, t2, ang_B_arc, ang_B_lbl
        )
        self.play(all_tri_objects.animate.shift(left_shift), run_time=1)
        self.wait(0.5)

        # Update coordinates after shift
        A = A_c + left_shift
        B = B_c + left_shift
        C = C_c + left_shift
        H = H_c + left_shift

        # Dividing line
        div_line = DashedLine(
            UP * 3.5 + LEFT * 0.3, DOWN * 3.8 + LEFT * 0.3,
            color=GRAY, dash_length=0.15, stroke_width=1, stroke_opacity=0.3,
        )
        self.play(FadeIn(div_line), run_time=0.3)

        # ----- CALCULATIONS (right side) -----
        calc_left = 0.2  # left edge of calculation column

        # Step 1: Isosceles → ∠C = 51°
        s1_title = Text(
            "Hapi 1: Këndet e bazës",
            font_size=26,
            color=TEAL,
            weight=BOLD,
        )
        s1_title.move_to(RIGHT * 3.2 + UP * 3.2)

        s1_txt = Text(
            "Meqë AB = AC, trekëndëshi është\ndybrinjënjëshëm. Këndet e bazës\njanë të barabarta:",
            font_size=22,
            color=GRAY_A,
            line_spacing=1.4,
        )
        s1_txt.next_to(s1_title, DOWN, buff=0.25, aligned_edge=LEFT)

        s1_eq = MathTex(
            r"\angle C = \angle B = 51^{\circ}",
            font_size=34,
            color=GREEN,
        )
        s1_eq.next_to(s1_txt, DOWN, buff=0.25)

        # Angle C on triangle
        ang_C_arc = self.angle_arc(C, A, B, radius=0.45, color=GREEN)
        ang_C_lbl = MathTex("51^{\\circ}", font_size=24, color=GREEN)
        ang_C_lbl.move_to(self.angle_label_pos(C, A, B, 0.75))

        self.play(FadeIn(s1_title), run_time=0.5)
        self.play(FadeIn(s1_txt), run_time=0.8)
        self.wait(1.5)
        self.play(
            Write(s1_eq), Create(ang_C_arc), FadeIn(ang_C_lbl), run_time=1
        )
        self.wait(2)

        # Step 2: ∠A = 78°
        s2_title = Text(
            "Hapi 2: Këndi në kulm",
            font_size=26,
            color=TEAL,
            weight=BOLD,
        )
        s2_title.next_to(s1_eq, DOWN, buff=0.4, aligned_edge=LEFT)

        s2_eq = MathTex(
            r"\angle A = 180^{\circ} - 51^{\circ} - 51^{\circ} = 78^{\circ}",
            font_size=32,
        )
        s2_eq.next_to(s2_title, DOWN, buff=0.2)

        ang_A_arc = self.angle_arc(A, B, C, radius=0.3, color=ORANGE)
        ang_A_lbl = MathTex("78^{\\circ}", font_size=20, color=ORANGE)
        ang_A_lbl.move_to(self.angle_label_pos(A, B, C, 0.55))

        self.play(FadeIn(s2_title), run_time=0.4)
        self.play(Write(s2_eq), run_time=1)
        self.play(Create(ang_A_arc), FadeIn(ang_A_lbl), run_time=0.6)
        self.wait(2)

        # Step 3: Draw altitude AH
        alt = DashedLine(A, H, color=RED_C, dash_length=0.1, stroke_width=2.5)
        ra = self.right_angle_mark(H, C, A, size=0.2, color=RED_C)
        lH = MathTex("H", font_size=32).next_to(H, DOWN, buff=0.15)

        s3_title = Text(
            "Hapi 3: Lartësia",
            font_size=26,
            color=TEAL,
            weight=BOLD,
        )
        s3_title.next_to(s2_eq, DOWN, buff=0.4, aligned_edge=LEFT)

        s3_txt = Text(
            "Heqim lartësinë AH ⊥ BC.\nAjo ndan bazën përgjysmë.",
            font_size=22,
            color=GRAY_A,
            line_spacing=1.4,
        )
        s3_txt.next_to(s3_title, DOWN, buff=0.2, aligned_edge=LEFT)

        self.play(FadeIn(s3_title), run_time=0.4)
        self.play(FadeIn(s3_txt), run_time=0.6)
        self.play(Create(alt), run_time=0.8)
        self.play(Create(ra), FadeIn(lH), run_time=0.5)
        self.wait(2)

        # --- Transition: fade top steps, keep triangle, show cos calc ---
        top_calc_items = VGroup(
            s1_title, s1_txt, s1_eq, s2_title, s2_eq, s3_title, s3_txt
        )
        self.play(FadeOut(top_calc_items), FadeOut(div_line), run_time=0.6)
        self.wait(0.3)

        # New dividing line
        div_line2 = DashedLine(
            UP * 3.5 + LEFT * 0.3, DOWN * 3.8 + LEFT * 0.3,
            color=GRAY, dash_length=0.15, stroke_width=1, stroke_opacity=0.3,
        )
        self.play(FadeIn(div_line2), run_time=0.2)

        # Step 4: cos → BH (now with more room)
        s4_title = Text(
            "Hapi 4: Gjejmë BH",
            font_size=28,
            color=TEAL,
            weight=BOLD,
        )
        s4_title.move_to(RIGHT * 3.2 + UP * 3.0)

        s4_txt = Text(
            "Në trekëndëshin kënddrejtë ABH:",
            font_size=24,
            color=GRAY_A,
        )
        s4_txt.next_to(s4_title, DOWN, buff=0.3, aligned_edge=LEFT)

        s4_eq1 = MathTex(
            r"\cos 51^{\circ} = \frac{BH}{AB}",
            font_size=36,
        )
        s4_eq1.next_to(s4_txt, DOWN, buff=0.35)

        s4_eq2 = MathTex(
            r"BH = 25 \cdot \cos 51^{\circ}",
            font_size=34,
        )
        s4_eq2.next_to(s4_eq1, DOWN, buff=0.3)

        s4_eq3 = MathTex(
            r"BH \approx 15{,}73 \text{ mm}",
            font_size=36,
            color=YELLOW,
        )
        s4_eq3.next_to(s4_eq2, DOWN, buff=0.3)

        self.play(FadeIn(s4_title), run_time=0.5)
        self.play(FadeIn(s4_txt), run_time=0.6)
        self.wait(1)
        self.play(Write(s4_eq1), run_time=1.2)
        self.wait(1.5)
        self.play(Write(s4_eq2), run_time=1)
        self.wait(1)
        self.play(Write(s4_eq3), run_time=1)
        self.wait(2)

        # Step 5: BC = 2·BH
        s5_title = Text(
            "Hapi 5: Gjejmë BC",
            font_size=28,
            color=TEAL,
            weight=BOLD,
        )
        s5_title.next_to(s4_eq3, DOWN, buff=0.5, aligned_edge=LEFT)

        s5_eq1 = MathTex(
            r"BC = 2 \times BH",
            font_size=34,
        )
        s5_eq1.next_to(s5_title, DOWN, buff=0.3)

        s5_eq2 = MathTex(
            r"BC = 2 \times 15{,}73 \approx 31{,}5 \text{ mm}",
            font_size=36,
            color=GREEN,
        )
        s5_eq2.next_to(s5_eq1, DOWN, buff=0.3)

        box = SurroundingRectangle(
            s5_eq2, color=GREEN, buff=0.15, corner_radius=0.08
        )

        self.play(FadeIn(s5_title), run_time=0.4)
        self.play(Write(s5_eq1), run_time=1)
        self.wait(1)
        self.play(Write(s5_eq2), run_time=1.2)
        self.play(Create(box), run_time=0.6)

        # Label BC on triangle
        s_BC = MathTex(
            r"\approx 31{,}5 \text{ mm}", font_size=24, color=GREEN
        )
        s_BC.next_to(Line(B, C), DOWN, buff=0.3)
        self.play(FadeIn(s_BC), run_time=0.6)

        self.wait(4)

    # ------------------------------------------------------------------ #
    #                            PART B                                   #
    # ------------------------------------------------------------------ #
    def part_b(self):
        # ----- Header -----
        header = Text("Pjesa b)", font_size=32, color=YELLOW, weight=BOLD)
        header.to_corner(UL, buff=0.4)
        self.play(Write(header), run_time=0.6)

        # ----- Problem Statement (centered, full screen) -----
        prob_title = Text(
            "Të dhëna:",
            font_size=32,
            color=TEAL,
            weight=BOLD,
        )
        prob_line1 = MathTex(
            r"\text{Trekëndëshi } PQR, \quad PQ = QR = 7 \text{ cm}",
            font_size=36,
        )
        prob_line2 = MathTex(
            r"PR = 4 \text{ cm}",
            font_size=36,
        )
        prob_ask = Text(
            "Gjeni: Të gjitha këndet",
            font_size=34,
            color=TEAL,
            weight=BOLD,
        )

        prob_group = VGroup(prob_title, prob_line1, prob_line2, prob_ask)
        prob_group.arrange(DOWN, buff=0.4, center=True)
        prob_group.move_to(ORIGIN)

        self.play(FadeIn(prob_group, shift=UP * 0.3), run_time=1.2)
        self.wait(3)
        self.play(FadeOut(prob_group), run_time=0.8)
        self.wait(0.5)

        # ----- Draw Triangle PQR (centered, large) -----
        scale_f = 2.8 / 4  # PR = 2.8 visual units
        PQ_v = 7 * scale_f
        PH_v = 2.8 / 2
        QH_v = np.sqrt(PQ_v**2 - PH_v**2)

        center_shift = DOWN * 0.3
        P_c = np.array([-PH_v, -QH_v / 2, 0]) + center_shift
        R_c = np.array([PH_v, -QH_v / 2, 0]) + center_shift
        Q_c = np.array([0, QH_v / 2, 0]) + center_shift
        H_c = np.array([0, -QH_v / 2, 0]) + center_shift

        tri = Polygon(P_c, Q_c, R_c, color=BLUE_C, stroke_width=3)
        lP = MathTex("P", font_size=36, color=WHITE).next_to(P_c, DL, buff=0.15)
        lQ = MathTex("Q", font_size=36, color=WHITE).next_to(Q_c, UP, buff=0.15)
        lR = MathTex("R", font_size=36, color=WHITE).next_to(R_c, DR, buff=0.15)

        self.play(Create(tri), run_time=1.2)
        self.play(FadeIn(lP), FadeIn(lQ), FadeIn(lR), run_time=0.6)
        self.wait(1)

        # Side labels & tick marks
        s_PQ = MathTex("7", font_size=28, color=YELLOW)
        s_PQ.move_to(self.midpoint(P_c, Q_c) + self.perp_offset(P_c, Q_c, -0.35))
        s_QR = MathTex("7", font_size=28, color=YELLOW)
        s_QR.move_to(self.midpoint(Q_c, R_c) + self.perp_offset(Q_c, R_c, 0.35))
        s_PR = MathTex("4", font_size=28, color=YELLOW)
        s_PR.next_to(Line(P_c, R_c), DOWN, buff=0.25)

        t1 = self.tick_mark(P_c, Q_c, size=0.12)
        t2 = self.tick_mark(Q_c, R_c, size=0.12)

        self.play(
            FadeIn(s_PQ), FadeIn(s_QR), FadeIn(s_PR),
            Create(t1), Create(t2),
            run_time=0.8,
        )
        self.wait(2)

        # ----- Move triangle to left -----
        left_shift = LEFT * 3.2
        all_tri = VGroup(tri, lP, lQ, lR, s_PQ, s_QR, s_PR, t1, t2)
        self.play(all_tri.animate.shift(left_shift), run_time=1)
        self.wait(0.5)

        P = P_c + left_shift
        R = R_c + left_shift
        Q = Q_c + left_shift
        H_pt = H_c + left_shift

        div_line = DashedLine(
            UP * 3.5 + LEFT * 0.3, DOWN * 3.8 + LEFT * 0.3,
            color=GRAY, dash_length=0.15, stroke_width=1, stroke_opacity=0.3,
        )
        self.play(FadeIn(div_line), run_time=0.2)

        # ----- Step 1: Isosceles + Altitude -----
        s1_title = Text(
            "Hapi 1: Lartësia",
            font_size=28,
            color=TEAL,
            weight=BOLD,
        )
        s1_title.move_to(RIGHT * 3.2 + UP * 3.0)

        s1_txt = Text(
            "Meqë PQ = QR, trekëndëshi është\ndybrinjënjëshëm. Heqim lartësinë\nQH ⊥ PR, që ndan bazën përgjysmë:",
            font_size=22,
            color=GRAY_A,
            line_spacing=1.4,
        )
        s1_txt.next_to(s1_title, DOWN, buff=0.25, aligned_edge=LEFT)

        # Draw altitude on triangle
        alt = DashedLine(Q, H_pt, color=RED_C, dash_length=0.1, stroke_width=2.5)
        ra = self.right_angle_mark(H_pt, R, Q, size=0.2, color=RED_C)
        lH = MathTex("H", font_size=32).next_to(H_pt, DOWN, buff=0.15)

        s1_eq = MathTex(
            r"PH = HR = \frac{4}{2} = 2 \text{ cm}",
            font_size=32,
        )
        s1_eq.next_to(s1_txt, DOWN, buff=0.3)

        self.play(FadeIn(s1_title), run_time=0.5)
        self.play(FadeIn(s1_txt), run_time=0.8)
        self.wait(1)
        self.play(Create(alt), run_time=0.8)
        self.play(Create(ra), FadeIn(lH), run_time=0.5)
        self.wait(1)
        self.play(Write(s1_eq), run_time=1)
        self.wait(2)

        # ----- Step 2: QH via Pythagorean -----
        s2_title = Text(
            "Hapi 2: Gjejmë QH",
            font_size=28,
            color=TEAL,
            weight=BOLD,
        )
        s2_title.next_to(s1_eq, DOWN, buff=0.45, aligned_edge=LEFT)

        s2_txt = Text(
            "Teorema e Pitagorës në △QPH:",
            font_size=22,
            color=GRAY_A,
        )
        s2_txt.next_to(s2_title, DOWN, buff=0.2, aligned_edge=LEFT)

        s2_eq1 = MathTex(
            r"QH^2 = PQ^2 - PH^2",
            font_size=32,
        )
        s2_eq1.next_to(s2_txt, DOWN, buff=0.25)

        s2_eq2 = MathTex(
            r"QH^2 = 49 - 4 = 45",
            font_size=32,
        )
        s2_eq2.next_to(s2_eq1, DOWN, buff=0.2)

        s2_eq3 = MathTex(
            r"QH = \sqrt{45} = 3\sqrt{5} \approx 6{,}71 \text{ cm}",
            font_size=32,
            color=YELLOW,
        )
        s2_eq3.next_to(s2_eq2, DOWN, buff=0.2)

        self.play(FadeIn(s2_title), run_time=0.4)
        self.play(FadeIn(s2_txt), run_time=0.5)
        self.wait(1)
        self.play(Write(s2_eq1), run_time=1)
        self.wait(1)
        self.play(Write(s2_eq2), run_time=1)
        self.wait(1)
        self.play(Write(s2_eq3), run_time=1)
        self.wait(2)

        # --- Transition: clear calc column for angle calculation ---
        old_calcs = VGroup(
            s1_title, s1_txt, s1_eq,
            s2_title, s2_txt, s2_eq1, s2_eq2, s2_eq3,
        )
        self.play(FadeOut(old_calcs), run_time=0.6)
        self.wait(0.3)

        # ----- Step 3: Find angle P -----
        s3_title = Text(
            "Hapi 3: Gjejmë këndin P",
            font_size=28,
            color=TEAL,
            weight=BOLD,
        )
        s3_title.move_to(RIGHT * 3.2 + UP * 3.0)

        s3_txt = Text(
            "Në trekëndëshin kënddrejtë QPH,\npërdorim sinusin:",
            font_size=22,
            color=GRAY_A,
            line_spacing=1.4,
        )
        s3_txt.next_to(s3_title, DOWN, buff=0.25, aligned_edge=LEFT)

        s3_eq1 = MathTex(
            r"\sin P = \frac{QH}{PQ} = \frac{3\sqrt{5}}{7}",
            font_size=34,
        )
        s3_eq1.next_to(s3_txt, DOWN, buff=0.3)

        s3_eq2 = MathTex(
            r"\sin P \approx 0{,}9583",
            font_size=34,
        )
        s3_eq2.next_to(s3_eq1, DOWN, buff=0.25)

        s3_eq3 = MathTex(
            r"\angle P \approx 73{,}4^{\circ}",
            font_size=38,
            color=GREEN,
        )
        s3_eq3.next_to(s3_eq2, DOWN, buff=0.3)

        self.play(FadeIn(s3_title), run_time=0.5)
        self.play(FadeIn(s3_txt), run_time=0.6)
        self.wait(1.5)
        self.play(Write(s3_eq1), run_time=1.2)
        self.wait(1.5)
        self.play(Write(s3_eq2), run_time=1)
        self.wait(1)
        self.play(Write(s3_eq3), run_time=1)
        self.wait(2)

        # ----- Step 4: ∠R = ∠P, find ∠Q -----
        s4_title = Text(
            "Hapi 4: Këndet e tjera",
            font_size=28,
            color=TEAL,
            weight=BOLD,
        )
        s4_title.next_to(s3_eq3, DOWN, buff=0.5, aligned_edge=LEFT)

        s4_txt = Text(
            "Këndet e bazës janë të barabarta:",
            font_size=22,
            color=GRAY_A,
        )
        s4_txt.next_to(s4_title, DOWN, buff=0.2, aligned_edge=LEFT)

        s4_eq1 = MathTex(
            r"\angle R = \angle P \approx 73{,}4^{\circ}",
            font_size=34,
            color=GREEN,
        )
        s4_eq1.next_to(s4_txt, DOWN, buff=0.25)

        s4_eq2 = MathTex(
            r"\angle Q = 180^{\circ} - 73{,}4^{\circ} - 73{,}4^{\circ}",
            font_size=32,
        )
        s4_eq2.next_to(s4_eq1, DOWN, buff=0.25)

        s4_eq3 = MathTex(
            r"\angle Q \approx 33{,}2^{\circ}",
            font_size=38,
            color=GREEN,
        )
        s4_eq3.next_to(s4_eq2, DOWN, buff=0.25)

        self.play(FadeIn(s4_title), run_time=0.4)
        self.play(FadeIn(s4_txt), run_time=0.5)
        self.wait(1)
        self.play(Write(s4_eq1), run_time=1)
        self.wait(1.5)
        self.play(Write(s4_eq2), run_time=1)
        self.wait(1)
        self.play(Write(s4_eq3), run_time=1)
        self.wait(1.5)

        # --- Transition: show final answer summary ---
        old_calcs2 = VGroup(
            s3_title, s3_txt, s3_eq1, s3_eq2, s3_eq3,
            s4_title, s4_txt, s4_eq1, s4_eq2, s4_eq3,
            div_line,
        )
        self.play(FadeOut(old_calcs2), run_time=0.6)
        self.wait(0.3)

        # Angle arcs on triangle
        ang_P_arc = self.angle_arc(P, R, Q, radius=0.4, color=GREEN)
        ang_P_lbl = MathTex("73{,}4^{\\circ}", font_size=22, color=GREEN)
        ang_P_lbl.move_to(self.angle_label_pos(P, R, Q, 0.7))

        ang_R_arc = self.angle_arc(R, Q, P, radius=0.4, color=GREEN)
        ang_R_lbl = MathTex("73{,}4^{\\circ}", font_size=22, color=GREEN)
        ang_R_lbl.move_to(self.angle_label_pos(R, Q, P, 0.7))

        ang_Q_arc = self.angle_arc(Q, P, R, radius=0.35, color=ORANGE)
        ang_Q_lbl = MathTex("33{,}2^{\\circ}", font_size=22, color=ORANGE)
        ang_Q_lbl.move_to(self.angle_label_pos(Q, P, R, 0.65))

        self.play(
            Create(ang_P_arc), Create(ang_R_arc), Create(ang_Q_arc),
            FadeIn(ang_P_lbl), FadeIn(ang_R_lbl), FadeIn(ang_Q_lbl),
            run_time=1.2,
        )
        self.wait(1.5)

        # Final answer box (right side, centered)
        answer_title = Text(
            "Përgjigja:",
            font_size=32,
            color=TEAL,
            weight=BOLD,
        )

        ans_P = MathTex(
            r"\angle P \approx 73{,}4^{\circ}",
            font_size=38,
            color=GREEN,
        )
        ans_R = MathTex(
            r"\angle R \approx 73{,}4^{\circ}",
            font_size=38,
            color=GREEN,
        )
        ans_Q = MathTex(
            r"\angle Q \approx 33{,}2^{\circ}",
            font_size=38,
            color=ORANGE,
        )

        answer_block = VGroup(answer_title, ans_P, ans_R, ans_Q)
        answer_block.arrange(DOWN, buff=0.35, center=True)
        answer_block.move_to(RIGHT * 3.2)

        ans_box = SurroundingRectangle(
            VGroup(ans_P, ans_R, ans_Q),
            color=GREEN,
            buff=0.25,
            corner_radius=0.1,
        )

        self.play(FadeIn(answer_block), run_time=1)
        self.play(Create(ans_box), run_time=0.6)
        self.wait(4)

    # ------------------------------------------------------------------ #
    #                        HELPER METHODS                               #
    # ------------------------------------------------------------------ #
    @staticmethod
    def midpoint(p1, p2):
        return (np.array(p1) + np.array(p2)) / 2

    @staticmethod
    def perp_offset(p1, p2, dist):
        d = np.array(p2) - np.array(p1)
        d = d / np.linalg.norm(d)
        perp = np.array([-d[1], d[0], 0])
        return perp * dist

    @staticmethod
    def tick_mark(p1, p2, size=0.1):
        mid = (np.array(p1) + np.array(p2)) / 2
        d = np.array(p2) - np.array(p1)
        d = d / np.linalg.norm(d)
        perp = np.array([-d[1], d[0], 0])
        return Line(
            mid - perp * size,
            mid + perp * size,
            color=YELLOW,
            stroke_width=2.5,
        )

    @staticmethod
    def angle_arc(vertex, p1, p2, radius=0.4, color=GREEN):
        v = np.array(vertex)
        d1 = np.array(p1) - v
        d2 = np.array(p2) - v
        a1 = np.arctan2(d1[1], d1[0])
        a2 = np.arctan2(d2[1], d2[0])
        diff = (a2 - a1) % (2 * np.pi)
        if diff > np.pi:
            start = a2
            angle = 2 * np.pi - diff
        else:
            start = a1
            angle = diff
        return Arc(
            radius=radius,
            start_angle=start,
            angle=angle,
            arc_center=v,
            color=color,
            stroke_width=2.5,
        )

    @staticmethod
    def angle_label_pos(vertex, p1, p2, distance=0.55):
        v = np.array(vertex)
        d1 = np.array(p1) - v
        d1 = d1 / np.linalg.norm(d1)
        d2 = np.array(p2) - v
        d2 = d2 / np.linalg.norm(d2)
        bisector = d1 + d2
        norm = np.linalg.norm(bisector)
        if norm < 1e-6:
            bisector = np.array([-d1[1], d1[0], 0])
        else:
            bisector = bisector / norm
        return v + bisector * distance

    @staticmethod
    def right_angle_mark(vertex, p_horiz, p_vert, size=0.2, color=RED_C):
        v = np.array(vertex)
        dh = np.array(p_horiz) - v
        dh = dh / np.linalg.norm(dh) * size
        dv = np.array(p_vert) - v
        dv = dv / np.linalg.norm(dv) * size
        return VGroup(
            Line(v + dh, v + dh + dv, color=color, stroke_width=2.5),
            Line(v + dv, v + dh + dv, color=color, stroke_width=2.5),
        )
