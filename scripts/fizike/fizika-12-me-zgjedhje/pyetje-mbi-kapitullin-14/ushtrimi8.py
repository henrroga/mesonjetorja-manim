import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from manim import *
import numpy as np
from components import ExerciseScene
from style_guide import (
    make_answer_box, make_divider, fade_all,
    STEP_TITLE_COLOR, BODY_TEXT_COLOR, LABEL_COLOR,
    ANSWER_COLOR, SHAPE_COLOR, AUX_COLOR, HIGHLIGHT_COLOR, DIVIDER_COLOR,
    STEP_TITLE_SIZE, BODY_SIZE, PROBLEM_MATH_SIZE, CALC_SIZE, ANSWER_SIZE,
    PART_HEADER_SIZE,
    T_TITLE_WRITE, T_STEP_TITLE, T_BODY_FADE, T_KEY_EQUATION,
    T_ROUTINE_EQUATION, T_SHAPE_CREATE, T_TRANSITION,
    W_AFTER_KEY, W_AFTER_ROUTINE, W_AFTER_ANSWER, W_PROBLEM,
    CALC_TOP,
)


class Ushtrimi8(ExerciseScene):
    """
    Ushtrimi 8 — Pyetje mbi Kapitullin 14
    Fizika 12 (me zgjedhje)

    Rezistenca, kombinimi i rezistencave, ligji i Omit.
    """

    exercise_number = 8
    unit = "Pyetje mbi Kapitullin 14"
    textbook = "Fizika 12 (me zgjedhje)"
    parts = ["a", "b", "c"]

    # ================================================================
    #  PART A — Explain resistance (conceptual, no calculation)
    # ================================================================
    def part_a(self):
        self.show_part_header("a")

        # Show the question
        q_text = MathTex(
            r"\text{Shpjegoni çfarë kuptojmë me rezistencë.}",
            font_size=BODY_SIZE + 4, color=WHITE,
        )
        q_text.move_to(UP * 2.5)
        self.play(FadeIn(q_text), run_time=T_BODY_FADE)
        self.wait(W_AFTER_ROUTINE)

        # Definition
        s1 = self.show_step_title("Përkufizimi", position=UP * 1.5)

        defn_lines = VGroup(
            MathTex(r"\text{Rezistenca e një elementi tregon sa}",
                    font_size=BODY_SIZE, color=BODY_TEXT_COLOR),
            MathTex(r"\text{shumë ai element e kundërshton}",
                    font_size=BODY_SIZE, color=BODY_TEXT_COLOR),
            MathTex(r"\text{kalimin e rrymës elektrike.}",
                    font_size=BODY_SIZE, color=BODY_TEXT_COLOR),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        defn_lines.next_to(s1, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(FadeIn(defn_lines), run_time=T_BODY_FADE)
        self.wait(W_AFTER_KEY)

        # Formal formula
        formula = MathTex(
            r"R = \frac{V}{I}",
            font_size=CALC_SIZE + 8, color=LABEL_COLOR,
        )
        formula.next_to(defn_lines, DOWN, buff=0.4)
        self.play(Write(formula), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        # Explain each symbol
        explain = VGroup(
            MathTex(r"R", font_size=BODY_SIZE + 4, color=SHAPE_COLOR),
            MathTex(r"\text{ — rezistenca (në } \Omega \text{)}",
                    font_size=BODY_SIZE, color=BODY_TEXT_COLOR),
        ).arrange(RIGHT, buff=0.1)
        explain2 = VGroup(
            MathTex(r"V", font_size=BODY_SIZE + 4, color=AUX_COLOR),
            MathTex(r"\text{ — diferenca e potencialeve (në V)}",
                    font_size=BODY_SIZE, color=BODY_TEXT_COLOR),
        ).arrange(RIGHT, buff=0.1)
        explain3 = VGroup(
            MathTex(r"I", font_size=BODY_SIZE + 4, color=ANSWER_COLOR),
            MathTex(r"\text{ — intensiteti i rrymës (në A)}",
                    font_size=BODY_SIZE, color=BODY_TEXT_COLOR),
        ).arrange(RIGHT, buff=0.1)

        legend = VGroup(explain, explain2, explain3).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        legend.next_to(formula, DOWN, buff=0.4)

        self.play(FadeIn(legend), run_time=T_SHAPE_CREATE)
        self.wait(W_AFTER_ROUTINE)

        # FadeOut definition + formula + legend before showing intuition
        self.play(
            FadeOut(VGroup(q_text, s1, defn_lines, formula, legend)),
            run_time=T_TRANSITION,
        )
        self.wait(0.3)

        # Physical intuition — clean screen
        s2 = self.show_step_title("Intuita fizike", position=UP * 2)

        intuition_lines = VGroup(
            MathTex(r"\text{Sa më e madhe rezistenca, aq më pak}",
                    font_size=BODY_SIZE, color=BODY_TEXT_COLOR),
            MathTex(r"\text{rrymë kalon — njëlloj si një tub}",
                    font_size=BODY_SIZE, color=BODY_TEXT_COLOR),
            MathTex(r"\text{i ngushtë lejon më pak ujë.}",
                    font_size=BODY_SIZE, color=BODY_TEXT_COLOR),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        intuition_lines.next_to(s2, DOWN, buff=0.4)
        self.play(FadeIn(intuition_lines), run_time=T_BODY_FADE)
        self.wait(W_AFTER_ANSWER)

    # ================================================================
    #  PART B — Show equivalent resistance = 40 Ω
    #  Circuit: R1=40Ω, R2=20Ω in series → 60Ω, then parallel with
    #  60Ω (the R3), then series with R5=96Ω, then parallel with
    #  R'=60Ω. Final = 40Ω.
    # ================================================================
    def part_b(self):
        self.show_part_header("b")
        self.show_problem(
            MathTex(r"\text{Tregoni se rezistenca e njëvlerëshme}",
                    font_size=BODY_SIZE + 2, color=WHITE),
            MathTex(r"\text{e kombinimit të rezistencave është } 40\;\Omega\text{.}",
                    font_size=BODY_SIZE + 2, color=WHITE),
            MathTex(r"\varepsilon = 6{,}0 \;\text{V}", font_size=CALC_SIZE, color=LABEL_COLOR),
        )

        # ---- Draw the circuit diagram ----
        circ_title = self.show_step_title("Hapi 1: Skema e qarkut", position=UP * 3)

        # Node positions
        A = np.array([-4, 1.5, 0])
        B = np.array([0, 1.5, 0])
        C = np.array([0, -0.5, 0])
        D = np.array([-4, -0.5, 0])

        # Top branch: R1 + R2 in series
        r1, r1_lbl = self.draw_resistor(A + RIGHT * 0.5, A + RIGHT * 2,
                                         label_tex=r"R_1=40\,\Omega", color=SHAPE_COLOR)
        r2, r2_lbl = self.draw_resistor(A + RIGHT * 2, A + RIGHT * 3.5,
                                         label_tex=r"R_2=20\,\Omega", color=SHAPE_COLOR)

        # Bottom branch: R3
        r3, r3_lbl = self.draw_resistor(D + RIGHT * 1, D + RIGHT * 3,
                                         label_tex=r"R_3=60\,\Omega", color=AUX_COLOR)

        # Vertical wires connecting branches
        wire_left = self.draw_wire(A, D)
        wire_right_top = self.draw_wire(B, A + RIGHT * 3.5)
        wire_right_bot = self.draw_wire(C, D + RIGHT * 3)
        wire_right_vert = self.draw_wire(B, C)

        # Battery on far left
        bat_pos = (A + D) / 2 + LEFT * 0.5
        battery, bat_lbl = self.draw_battery(bat_pos, direction=UP,
                                              label_tex=r"\varepsilon = 6\,\text{V}")

        # Series resistor after parallel combination
        r5, r5_lbl = self.draw_resistor(C, C + RIGHT * 2.5,
                                         label_tex=r"R_5=96\,\Omega", color=HIGHLIGHT_COLOR)

        # Connect R5 to battery return
        wire_bottom = self.draw_wire(C + RIGHT * 2.5, C + RIGHT * 3, C + RIGHT * 3 + DOWN * 1,
                                      D + DOWN * 1, D)

        # Nodes
        node_A = self.draw_node(A)
        node_B = self.draw_node(B)
        node_C = self.draw_node(C)
        node_D = self.draw_node(D)

        circuit = VGroup(
            wire_left, wire_right_top, wire_right_bot, wire_right_vert,
            wire_bottom,
            r1, r2, r3, r5,
            battery,
            node_A, node_B, node_C, node_D,
        )
        labels = VGroup(r1_lbl, r2_lbl, r3_lbl, r5_lbl, bat_lbl)

        # Scale and position
        full_circuit = VGroup(circuit, labels)
        full_circuit.scale(0.7).move_to(ORIGIN + DOWN * 0.3)

        self.play(Create(circuit), run_time=T_SHAPE_CREATE * 1.5)
        self.play(FadeIn(labels), run_time=T_BODY_FADE)
        self.wait(W_AFTER_KEY)

        # ---- Shift left for calculations ----
        self.play(
            FadeOut(circ_title),
            full_circuit.animate.shift(LEFT * 3.5).scale(0.8),
            run_time=1,
        )
        div = make_divider()
        self.play(FadeIn(div), run_time=0.2)

        # ---- Step 2: Series combination R1 + R2 ----
        s2 = self.show_step_title("Hapi 2: R₁ + R₂ në seri")

        s2_txt = MathTex(
            r"\text{Rezistencat në seri mblidhen:}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        s2_txt.next_to(s2, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(FadeIn(s2_txt), run_time=T_BODY_FADE)

        eqs2 = self.show_equation_chain([
            r"R' = R_1 + R_2",
            {"tex": r"R' = 40 + 20 = 60\;\Omega", "color": LABEL_COLOR, "key": True},
        ], start_reference=s2_txt)
        self.wait(W_AFTER_KEY)

        # ---- FadeOut step 2 calcs before step 3 ----
        self.play(FadeOut(VGroup(s2, s2_txt, *eqs2)), run_time=T_TRANSITION)
        self.wait(0.3)

        # ---- Step 3: Parallel R' ∥ R3 ----
        s3 = self.show_step_title("Hapi 3: R' ∥ R₃ në paralel")

        s3_lines = VGroup(
            MathTex(r"\text{Në paralel përdorim formulën}",
                    font_size=BODY_SIZE, color=BODY_TEXT_COLOR),
            MathTex(r"\text{e reciproke:}",
                    font_size=BODY_SIZE, color=BODY_TEXT_COLOR),
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        s3_lines.next_to(s3, DOWN, buff=0.2, aligned_edge=LEFT)
        self.play(FadeIn(s3_lines), run_time=T_BODY_FADE)

        eqs3 = self.show_equation_chain([
            r"\frac{1}{R''} = \frac{1}{60} + \frac{1}{60}",
            r"= \frac{1+1}{60} = \frac{2}{60}",
            {"tex": r"R'' = 30\;\Omega", "color": LABEL_COLOR, "key": True},
        ], start_reference=s3_lines)
        self.wait(W_AFTER_KEY)

        # ---- FadeOut step 3 calcs before step 4 ----
        self.play(FadeOut(VGroup(s3, s3_lines, *eqs3)), run_time=T_TRANSITION)
        self.wait(0.3)

        # ---- Step 4: Series R'' + R5 ----
        s4 = self.show_step_title("Hapi 4: R'' + R₅ në seri")

        eqs4 = self.show_equation_chain([
            r"R''' = R'' + R_5",
            {"tex": r"R''' = 24 + 96 = 120\;\Omega", "color": LABEL_COLOR, "key": True},
        ], start_reference=s4)
        self.wait(W_AFTER_KEY)

        # ---- FadeOut step 4 calcs before step 5 ----
        self.play(FadeOut(VGroup(s4, *eqs4)), run_time=T_TRANSITION)
        self.wait(0.3)

        # ---- Step 5: Final parallel ----
        s5 = self.show_step_title("Hapi 5: R' ∥ R''' (paralel përfundimtar)")

        eqs5 = self.show_equation_chain([
            r"\frac{1}{R_p} = \frac{1}{60} + \frac{1}{120}",
            r"= \frac{2+1}{120} = \frac{3}{120}",
            {"tex": r"R_p = \frac{120}{3} = 40\;\Omega", "color": ANSWER_COLOR,
             "font_size": CALC_SIZE + 2, "key": True},
        ], start_reference=s5)
        self.wait(W_AFTER_KEY)

        ans = MathTex(r"R_{\text{njëvl.}} = 40\;\Omega", font_size=ANSWER_SIZE, color=ANSWER_COLOR)
        ans.next_to(eqs5[-1], DOWN, buff=0.4)
        box = make_answer_box(ans)
        self.play(Write(ans), run_time=T_KEY_EQUATION)
        self.play(Create(box), run_time=0.5)
        self.wait(W_AFTER_ANSWER)

    # ================================================================
    #  PART C — Current through the 60 Ω resistor
    # ================================================================
    def part_c(self):
        self.show_part_header("c")
        self.show_problem(
            MathTex(r"\text{Llogaritni intensitetin e rrymës}",
                    font_size=BODY_SIZE + 2, color=WHITE),
            MathTex(r"\text{në rezistencën } 60\;\Omega",
                    font_size=BODY_SIZE + 4, color=WHITE),
        )

        # Step 1: Explain approach
        s1 = self.show_step_title("Hapi 1: Strategjia")

        s1_lines = VGroup(
            MathTex(r"\text{Për të gjetur rrymën në } R_3 = 60\;\Omega\text{,}",
                    font_size=BODY_SIZE, color=BODY_TEXT_COLOR),
            MathTex(r"\text{duhet të gjejmë diferencën e potencialeve}",
                    font_size=BODY_SIZE, color=BODY_TEXT_COLOR),
            MathTex(r"\text{në skajet e saj. Përdorim ndarësin}",
                    font_size=BODY_SIZE, color=BODY_TEXT_COLOR),
            MathTex(r"\text{e tensionit.}",
                    font_size=BODY_SIZE, color=BODY_TEXT_COLOR),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        s1_lines.next_to(s1, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(FadeIn(s1_lines), run_time=T_BODY_FADE)
        self.wait(W_AFTER_KEY)

        # FadeOut step 1 before step 2
        self.play(FadeOut(VGroup(s1, s1_lines)), run_time=T_TRANSITION)
        self.wait(0.3)

        # Step 2: Voltage across parallel section
        s2 = self.show_step_title("Hapi 2: Tensioni në lidhjen paralele")

        s2_lines = VGroup(
            MathTex(r"R'' = 24\;\Omega \text{ në seri me } R_5 = 96\;\Omega",
                    font_size=BODY_SIZE, color=BODY_TEXT_COLOR),
            MathTex(r"\text{jep } R''' = 120\;\Omega\text{. Tensioni ndahet:}",
                    font_size=BODY_SIZE, color=BODY_TEXT_COLOR),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        s2_lines.next_to(s2, DOWN, buff=0.2, aligned_edge=LEFT)
        self.play(FadeIn(s2_lines), run_time=T_BODY_FADE)
        self.wait(W_AFTER_ROUTINE)

        eqs2 = self.show_equation_chain([
            {"tex": r"V' = \frac{R''}{R'''} \times V", "key": True},
            r"V' = \frac{24}{120} \times 6",
            {"tex": r"V' = 1{,}2 \;\text{V}", "color": LABEL_COLOR, "key": True},
        ], start_reference=s2_lines)
        self.wait(W_AFTER_KEY)

        # FadeOut step 2 before step 3
        self.play(FadeOut(VGroup(s2, s2_lines, *eqs2)), run_time=T_TRANSITION)
        self.wait(0.3)

        # Step 3: Apply Ohm's law
        s3 = self.show_step_title("Hapi 3: Ligji i Omit")

        s3_lines = VGroup(
            MathTex(r"\text{Tani që dimë tensionin në lidhjen}",
                    font_size=BODY_SIZE, color=BODY_TEXT_COLOR),
            MathTex(r"\text{paralele (1,2 V), mund të gjejmë}",
                    font_size=BODY_SIZE, color=BODY_TEXT_COLOR),
            MathTex(r"\text{rrymën në } R_3 = 60\;\Omega \text{ me ligjin e Omit:}",
                    font_size=BODY_SIZE, color=BODY_TEXT_COLOR),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        s3_lines.next_to(s3, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(FadeIn(s3_lines), run_time=T_BODY_FADE)
        self.wait(W_AFTER_KEY)

        eqs3 = self.show_equation_chain([
            {"tex": r"I = \frac{V'}{R_3}", "key": True},
            r"I = \frac{1{,}2\;\text{V}}{60\;\Omega}",
            {"tex": r"I = 0{,}02\;\text{A} = 20\;\text{mA}", "color": ANSWER_COLOR,
             "font_size": CALC_SIZE + 2, "key": True},
        ], start_reference=s3_lines)
        self.wait(W_AFTER_KEY)

        self.show_answer_below(r"I_{60\,\Omega} = 0{,}02\;\text{A}", eqs3[-1])

    # ================================================================
    #  FINAL SUMMARY
    # ================================================================
    def final_summary(self):
        self.show_summary_table(
            "Përmbledhje e përgjigjeve",
            [
                r"\text{a)}\quad R = V/I \text{ — raporti i tensionit me rrymën}",
                r"\text{b)}\quad R_{\text{njëvl.}} = 40\;\Omega",
                r"\text{c)}\quad I_{60\,\Omega} = 0{,}02\;\text{A}",
            ],
            font_size=28,
        )
