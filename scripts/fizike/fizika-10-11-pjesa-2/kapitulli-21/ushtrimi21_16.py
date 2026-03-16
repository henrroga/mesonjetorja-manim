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
    STEP_TITLE_SIZE, BODY_SIZE, CALC_SIZE, ANSWER_SIZE,
    PART_HEADER_SIZE, DIAGRAM_LABEL_SIZE, DIAGRAM_VALUE_SIZE,
    T_STEP_TITLE, T_BODY_FADE, T_KEY_EQUATION, T_ROUTINE_EQUATION,
    T_SHAPE_CREATE, T_LAYOUT_SHIFT, T_TRANSITION,
    W_AFTER_KEY, W_AFTER_ROUTINE, W_AFTER_ANSWER, W_PROBLEM,
    CALC_TOP, PX,
)


class Ushtrimi21_16(ExerciseScene):
    """
    Ushtrimi 21.16 — Kapitulli 21 — Fizika 10-11: Pjesa e Dyte

    Transformer problem: step-down from 230V to 6.0V.
    a) Find secondary turns
    b) Find secondary current
    c) Assumption: ideal transformer

    Visual storytelling — no voiceover.
    """

    exercise_number = "21.16"
    unit = "Kapitulli 21"
    textbook = "Fizika 10-11: Pjesa e Dyte"
    parts = ["a", "b", "c"]

    # ── Transformer diagram builder ──

    def _build_transformer(self):
        """
        Build a simplified transformer diagram.
        Returns a dict with all named mobjects and the full VGroup.

        Layout:
        - Iron core: rectangular frame (two vertical bars + top/bottom connectors)
        - Primary coil: zigzag on left vertical bar
        - Secondary coil: zigzag on right vertical bar (fewer turns)
        - Labels for voltages, turns, currents
        """
        parts = {}

        # Iron core — rectangular frame
        core_w = 2.4
        core_h = 3.0
        bar_w = 0.2

        # Left vertical bar
        left_bar = Rectangle(
            width=bar_w, height=core_h,
            fill_color="#777777", fill_opacity=0.6,
            stroke_color="#999999", stroke_width=1.5,
        ).move_to(LEFT * core_w / 2)

        # Right vertical bar
        right_bar = Rectangle(
            width=bar_w, height=core_h,
            fill_color="#777777", fill_opacity=0.6,
            stroke_color="#999999", stroke_width=1.5,
        ).move_to(RIGHT * core_w / 2)

        # Top connector
        top_bar = Rectangle(
            width=core_w + bar_w, height=bar_w,
            fill_color="#777777", fill_opacity=0.6,
            stroke_color="#999999", stroke_width=1.5,
        ).move_to(UP * (core_h / 2 - bar_w / 2))

        # Bottom connector
        bot_bar = Rectangle(
            width=core_w + bar_w, height=bar_w,
            fill_color="#777777", fill_opacity=0.6,
            stroke_color="#999999", stroke_width=1.5,
        ).move_to(DOWN * (core_h / 2 - bar_w / 2))

        core = VGroup(left_bar, right_bar, top_bar, bot_bar)
        parts["core"] = core

        # Primary coil (left side) — zigzag pattern representing many turns
        coil_h = 2.0
        n_primary_zigs = 10  # more zigzags = more turns visually
        prim_x = -core_w / 2 - 0.35
        prim_points = []
        for i in range(n_primary_zigs + 1):
            y = coil_h / 2 - i * coil_h / n_primary_zigs
            x_offset = -0.25 if i % 2 == 0 else 0.0
            prim_points.append(np.array([prim_x + x_offset, y, 0]))

        primary_coil = VMobject(color=SHAPE_COLOR, stroke_width=2.5)
        primary_coil.set_points_as_corners(prim_points)
        parts["primary_coil"] = primary_coil

        # Secondary coil (right side) — fewer zigzags (step-down)
        n_secondary_zigs = 4
        sec_x = core_w / 2 + 0.35
        sec_points = []
        for i in range(n_secondary_zigs + 1):
            y = coil_h / 2 - i * coil_h / n_secondary_zigs
            x_offset = 0.25 if i % 2 == 0 else 0.0
            sec_points.append(np.array([sec_x + x_offset, y, 0]))

        secondary_coil = VMobject(color=HIGHLIGHT_COLOR, stroke_width=2.5)
        secondary_coil.set_points_as_corners(sec_points)
        parts["secondary_coil"] = secondary_coil

        # Wire extensions from coils to connection points
        prim_top_wire = Line(
            prim_points[0], prim_points[0] + LEFT * 0.6,
            color=SHAPE_COLOR, stroke_width=2,
        )
        prim_bot_wire = Line(
            prim_points[-1], prim_points[-1] + LEFT * 0.6,
            color=SHAPE_COLOR, stroke_width=2,
        )
        sec_top_wire = Line(
            sec_points[0], sec_points[0] + RIGHT * 0.6,
            color=HIGHLIGHT_COLOR, stroke_width=2,
        )
        sec_bot_wire = Line(
            sec_points[-1], sec_points[-1] + RIGHT * 0.6,
            color=HIGHLIGHT_COLOR, stroke_width=2,
        )
        parts["prim_top_wire"] = prim_top_wire
        parts["prim_bot_wire"] = prim_bot_wire
        parts["sec_top_wire"] = sec_top_wire
        parts["sec_bot_wire"] = sec_bot_wire

        # Labels — coil names
        prim_label = MathTex(
            r"\text{Paresori}", font_size=20, color=SHAPE_COLOR,
        ).next_to(primary_coil, LEFT, buff=0.35)
        sec_label = MathTex(
            r"\text{Dytesori}", font_size=20, color=HIGHLIGHT_COLOR,
        ).next_to(secondary_coil, RIGHT, buff=0.35)
        parts["prim_label"] = prim_label
        parts["sec_label"] = sec_label

        # Voltage labels
        vp_label = MathTex(
            r"V_p = 230\,\text{V}", font_size=20, color=LABEL_COLOR,
        ).next_to(prim_bot_wire, DOWN, buff=0.25).shift(LEFT * 0.2)
        vs_label = MathTex(
            r"V_s = 6{,}0\,\text{V}", font_size=20, color=LABEL_COLOR,
        ).next_to(sec_bot_wire, DOWN, buff=0.25).shift(RIGHT * 0.2)
        parts["vp_label"] = vp_label
        parts["vs_label"] = vs_label

        # Turns labels
        np_label = MathTex(
            r"N_p = 6000", font_size=20, color=SHAPE_COLOR,
        ).next_to(prim_label, DOWN, buff=0.2)
        ns_label = MathTex(
            r"N_s = \;?", font_size=20, color=HIGHLIGHT_COLOR,
        ).next_to(sec_label, DOWN, buff=0.2)
        parts["np_label"] = np_label
        parts["ns_label"] = ns_label

        # Current arrows (will be added later in parts a/b)
        # Primary current arrow — pointing downward on left
        ip_arrow = Arrow(
            prim_top_wire.get_end() + UP * 0.1,
            prim_top_wire.get_end() + DOWN * 0.5,
            buff=0, color=SHAPE_COLOR, stroke_width=2,
            max_tip_length_to_length_ratio=0.3,
        ).shift(LEFT * 0.35)
        ip_label = MathTex(
            r"I_p", font_size=18, color=SHAPE_COLOR,
        ).next_to(ip_arrow, LEFT, buff=0.1)
        parts["ip_arrow"] = ip_arrow
        parts["ip_label"] = ip_label

        # Secondary current arrow — pointing downward on right
        is_arrow = Arrow(
            sec_top_wire.get_end() + UP * 0.1,
            sec_top_wire.get_end() + DOWN * 0.5,
            buff=0, color=HIGHLIGHT_COLOR, stroke_width=2,
            max_tip_length_to_length_ratio=0.3,
        ).shift(RIGHT * 0.35)
        is_label = MathTex(
            r"I_s", font_size=18, color=HIGHLIGHT_COLOR,
        ).next_to(is_arrow, RIGHT, buff=0.1)
        parts["is_arrow"] = is_arrow
        parts["is_label"] = is_label

        # Radio label on secondary side
        radio_label = MathTex(
            r"\text{Radio}", font_size=18, color=BODY_TEXT_COLOR,
        ).next_to(sec_label, UP, buff=0.6)
        radio_box = SurroundingRectangle(
            radio_label, color=BODY_TEXT_COLOR, buff=0.1,
            corner_radius=0.05, stroke_width=1,
        )
        parts["radio_label"] = radio_label
        parts["radio_box"] = radio_box

        # Core label
        core_label = MathTex(
            r"\text{Berthame hekuri}", font_size=16, color=DIVIDER_COLOR,
        ).move_to(core.get_center() + DOWN * 0.2)
        parts["core_label"] = core_label

        # Full group (without current elements — those are added per-part)
        base_group = VGroup(
            core, primary_coil, secondary_coil,
            prim_top_wire, prim_bot_wire, sec_top_wire, sec_bot_wire,
            prim_label, sec_label,
            vp_label, vs_label,
            np_label, ns_label,
            core_label,
            radio_label, radio_box,
        )
        parts["base_group"] = base_group

        return parts

    # ================================================================
    #  PART A — Find secondary turns Ns
    # ================================================================
    def part_a(self):
        self.show_part_header("a")

        # ── Problem statement ──
        prob_title = MathTex(
            r"\text{Te dhena:}",
            font_size=STEP_TITLE_SIZE + 6, color=STEP_TITLE_COLOR,
        )
        prob_lines = VGroup(
            MathTex(r"V_p = 230\,\text{V},\quad V_s = 6{,}0\,\text{V}",
                    font_size=CALC_SIZE),
            MathTex(r"N_p = 6000", font_size=CALC_SIZE),
            MathTex(r"\text{Gjeni: } N_s = \;?",
                    font_size=CALC_SIZE, color=STEP_TITLE_COLOR),
        ).arrange(DOWN, buff=0.3)
        self.show_problem(prob_title, prob_lines)

        # ── Build transformer diagram ──
        tx = self._build_transformer()
        diagram = tx["base_group"].copy()
        diagram.scale(0.85).move_to(ORIGIN)

        self.play(FadeIn(diagram), run_time=T_SHAPE_CREATE)
        self.wait(W_AFTER_ROUTINE)

        # ── Shift diagram left ──
        self.play(diagram.animate.shift(LEFT * 3.2), run_time=T_LAYOUT_SHIFT)
        div = make_divider()
        self.play(FadeIn(div), run_time=0.2)
        self.wait(0.5)

        # Store references to diagram labels for flashing
        # (indices match the order in base_group)
        vp_mob = diagram[9]   # vp_label
        vs_mob = diagram[10]  # vs_label
        np_mob = diagram[11]  # np_label
        ns_mob = diagram[12]  # ns_label

        # ── Step 1: Show the turns ratio formula ──
        s1t = self.panel_title("Hapi 1: Raporti i mbeshtetjellave", y_pos=3.0)

        s1txt = self.panel_text([
            r"\text{Tek nje transformator, raporti}",
            r"\text{i mbeshtetjellave eshte:}",
        ], s1t)
        self.wait(2)

        # Flash Vp and Vs on the diagram
        self.play(
            Indicate(vp_mob, color=YELLOW, scale_factor=1.3),
            Indicate(vs_mob, color=YELLOW, scale_factor=1.3),
            run_time=0.6,
        )
        self.wait(0.5)

        eq1 = self.panel_eq(
            r"\frac{V_p}{V_s} = \frac{N_p}{N_s}",
            s1txt, font_size=36, key=True,
        )

        # ── Step 2: Rearrange for Ns ──
        s2txt = self.panel_text([
            r"\text{Risistemojme per } N_s\text{:}",
        ], eq1, buff=0.3)
        self.wait(1.5)

        eq2 = self.panel_eq(
            r"N_s = N_p \times \frac{V_s}{V_p}",
            s2txt, font_size=34, key=True,
        )

        # ── Step 3: Substitute ──
        # Flash Np on diagram
        self.play(Indicate(np_mob, color=YELLOW, scale_factor=1.3), run_time=0.5)

        eq3 = self.panel_eq(
            r"N_s = 6000 \times \frac{6{,}0}{230}",
            eq2, font_size=32,
        )

        # ── Clear right panel for arithmetic ──
        calc1 = VGroup(s1t, s1txt, eq1, s2txt, eq2)
        self.play(FadeOut(calc1), run_time=0.5)
        self.wait(0.3)

        # Move eq3 to the top
        self.play(eq3.animate.move_to(np.array([PX, 2.8, 0])), run_time=0.5)

        # ── Step 4: Arithmetic detail ──
        s4t = self.panel_title("Hapi 2: Llogaritja", ref=eq3, buff=0.4)

        eq4a = self.panel_eq(
            r"\frac{6{,}0}{230} = 0{,}02609\ldots",
            s4t, font_size=30,
        )

        eq4b = self.panel_eq(
            r"N_s = 6000 \times 0{,}02609",
            eq4a, font_size=30,
        )

        eq4c = self.panel_eq(
            r"N_s = 156{,}5",
            eq4b, font_size=32,
        )

        # ── Step 5: Rounding explanation ──
        s5txt = self.panel_text([
            r"\text{Mbeshtetjellat duhet te jene}",
            r"\text{numer i plote, keshtu rrumbullakosim:}",
        ], eq4c, buff=0.3)
        self.wait(2)

        eq5 = self.panel_eq(
            r"N_s \approx 157 \text{ mbeshtetjella}",
            s5txt, color=ANSWER_COLOR, font_size=34, key=True,
        )

        box = make_answer_box(eq5)
        self.play(Create(box), run_time=0.5)
        self.wait(1.5)

        # ── Transfer value to diagram ──
        # Replace "?" with "157" on the diagram
        ns_new = MathTex(
            r"N_s = 157", font_size=20, color=ANSWER_COLOR,
        ).move_to(ns_mob.get_center())
        ns_new.shift(LEFT * 3.2)  # match diagram shift

        self.transfer_value(eq5, ns_new)
        self.play(FadeOut(ns_mob), run_time=0.3)
        self.wait(W_AFTER_ANSWER)

        # Store ns_new in diagram for reference
        diagram.add(ns_new)

    # ================================================================
    #  PART B — Find secondary current Is
    # ================================================================
    def part_b(self):
        self.show_part_header("b")

        # ── Problem statement ──
        prob_title = MathTex(
            r"\text{Te dhena:}",
            font_size=STEP_TITLE_SIZE + 6, color=STEP_TITLE_COLOR,
        )
        prob_lines = VGroup(
            MathTex(r"V_p = 230\,\text{V},\quad V_s = 6{,}0\,\text{V}",
                    font_size=CALC_SIZE),
            MathTex(r"I_p = 0{,}040\,\text{A}",
                    font_size=CALC_SIZE),
            MathTex(r"\text{Gjeni: } I_s = \;?",
                    font_size=CALC_SIZE, color=STEP_TITLE_COLOR),
        ).arrange(DOWN, buff=0.3)
        self.show_problem(prob_title, prob_lines)

        # ── Build transformer diagram with Ns filled and currents ──
        tx = self._build_transformer()
        diagram = tx["base_group"].copy()

        # Replace Ns = ? with Ns = 157
        ns_idx = 12  # ns_label index in base_group
        old_ns = diagram[ns_idx]
        new_ns = MathTex(
            r"N_s = 157", font_size=20, color=ANSWER_COLOR,
        ).move_to(old_ns.get_center())
        diagram.remove(old_ns)
        diagram.add(new_ns)

        # Add current arrows and labels
        ip_arrow = tx["ip_arrow"].copy()
        ip_label = tx["ip_label"].copy()
        # Show Ip value
        ip_val = MathTex(
            r"I_p = 0{,}040\,\text{A}", font_size=18, color=SHAPE_COLOR,
        ).next_to(ip_label, DOWN, buff=0.15)

        is_arrow = tx["is_arrow"].copy()
        is_label = tx["is_label"].copy()
        is_val = MathTex(
            r"I_s = \;?", font_size=18, color=HIGHLIGHT_COLOR,
        ).next_to(is_label, DOWN, buff=0.15)

        current_group = VGroup(ip_arrow, ip_label, ip_val,
                               is_arrow, is_label, is_val)
        full_diagram = VGroup(diagram, current_group)
        full_diagram.scale(0.85).move_to(ORIGIN)

        self.play(FadeIn(full_diagram), run_time=T_SHAPE_CREATE)
        self.wait(W_AFTER_ROUTINE)

        # ── Shift left ──
        self.play(full_diagram.animate.shift(LEFT * 3.2), run_time=T_LAYOUT_SHIFT)
        div = make_divider()
        self.play(FadeIn(div), run_time=0.2)
        self.wait(0.5)

        # ── Step 1: Explain power conservation ──
        s1t = self.panel_title("Hapi 1: Ruajtja e fuqise", y_pos=3.0)

        s1txt = self.panel_text([
            r"\text{Per nje transformator ideal,}",
            r"\text{fuqia hyn = fuqia del:}",
        ], s1t)
        self.wait(2)

        eq1 = self.panel_eq(
            r"P_p = P_s",
            s1txt, font_size=36, key=True, color=LABEL_COLOR,
        )

        s1txt2 = self.panel_text([
            r"\text{Dmth:}",
        ], eq1, buff=0.2)

        eq1b = self.panel_eq(
            r"V_p \times I_p = V_s \times I_s",
            s1txt2, font_size=34, key=True,
        )

        # ── Step 2: Rearrange for Is ──
        s2txt = self.panel_text([
            r"\text{Risistemojme per } I_s\text{:}",
        ], eq1b, buff=0.3)
        self.wait(1.5)

        eq2 = self.panel_eq(
            r"I_s = I_p \times \frac{V_p}{V_s}",
            s2txt, font_size=34, key=True,
        )

        # ── Clear panel for arithmetic ──
        calc1 = VGroup(s1t, s1txt, eq1, s1txt2, eq1b, s2txt)
        self.play(FadeOut(calc1), run_time=0.5)
        self.wait(0.3)

        # Move eq2 to top
        self.play(eq2.animate.move_to(np.array([PX, 2.8, 0])), run_time=0.5)

        # ── Step 3: Substitute ──
        s3t = self.panel_title("Hapi 2: Zevendesimi", ref=eq2, buff=0.4)

        # Flash Ip on diagram
        self.play(Indicate(ip_val, color=YELLOW, scale_factor=1.3), run_time=0.5)

        eq3 = self.panel_eq(
            r"I_s = 0{,}040 \times \frac{230}{6{,}0}",
            s3t, font_size=32,
        )

        # ── Step 4: Arithmetic ──
        eq4a = self.panel_eq(
            r"\frac{230}{6{,}0} = 38{,}33\ldots",
            eq3, font_size=30,
        )

        eq4b = self.panel_eq(
            r"I_s = 0{,}040 \times 38{,}33",
            eq4a, font_size=30,
        )

        eq4c = self.panel_eq(
            r"I_s \approx 1{,}53\,\text{A}",
            eq4b, color=ANSWER_COLOR, font_size=36, key=True,
        )

        box = make_answer_box(eq4c)
        self.play(Create(box), run_time=0.5)
        self.wait(1.5)

        # ── Transfer to diagram ──
        is_new = MathTex(
            r"I_s = 1{,}53\,\text{A}", font_size=18, color=ANSWER_COLOR,
        ).move_to(is_val.get_center())

        self.transfer_value(eq4c, is_new)
        self.play(FadeOut(is_val), run_time=0.3)
        self.wait(1)

        # ── Intuition: step-down voltage → step-up current ──
        calc2 = VGroup(eq2, s3t, eq3, eq4a, eq4b, eq4c, box)
        self.play(FadeOut(calc2), run_time=0.5)
        self.wait(0.3)

        s5t = self.panel_title("Kuptimi fizik:", y_pos=2.8)

        s5txt = self.panel_text([
            r"\text{Tensioni ulet:}",
            r"230\,\text{V} \to 6{,}0\,\text{V}",
            r"\text{Rryma rritet:}",
            r"0{,}040\,\text{A} \to 1{,}53\,\text{A}",
            r"\text{Fuqia mbetet e njejte!}",
        ], s5t)
        self.wait(W_AFTER_ANSWER)

    # ================================================================
    #  PART C — What assumption? Ideal transformer
    # ================================================================
    def part_c(self):
        self.show_part_header("c")

        # ── Question ──
        q_text = MathTex(
            r"\text{Cfare supozimi duhet te bejme}",
            font_size=BODY_SIZE + 4, color=WHITE,
        )
        q_text2 = MathTex(
            r"\text{per te zgjidhur pjesen b)?}",
            font_size=BODY_SIZE + 4, color=WHITE,
        )
        q_group = VGroup(q_text, q_text2).arrange(DOWN, buff=0.2)
        q_group.move_to(UP * 2.5)
        self.play(FadeIn(q_group), run_time=T_BODY_FADE)
        self.wait(W_AFTER_ROUTINE)

        # ── Answer: Ideal transformer ──
        ans_title = MathTex(
            r"\text{Supozimi:}", font_size=STEP_TITLE_SIZE + 4,
            color=STEP_TITLE_COLOR,
        )
        ans_title.next_to(q_group, DOWN, buff=0.6)
        self.play(FadeIn(ans_title), run_time=T_STEP_TITLE)
        self.wait(1)

        ans_line1 = MathTex(
            r"\text{Transformatori eshte ideal}",
            font_size=CALC_SIZE, color=ANSWER_COLOR,
        )
        ans_line1.next_to(ans_title, DOWN, buff=0.3)
        self.play(Write(ans_line1), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_KEY)

        # ── Show what "ideal" means ──
        self.play(FadeOut(q_group), run_time=0.4)

        meaning_title = MathTex(
            r"\text{Kjo do te thote:}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        meaning_title.next_to(ans_line1, DOWN, buff=0.5)
        self.play(FadeIn(meaning_title), run_time=T_STEP_TITLE)
        self.wait(1)

        # Power equation
        power_eq = MathTex(
            r"P_p = P_s", font_size=CALC_SIZE + 4, color=LABEL_COLOR,
        )
        power_eq.next_to(meaning_title, DOWN, buff=0.35)
        self.play(Write(power_eq), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_KEY)

        # Expanded
        power_expand = MathTex(
            r"V_p \times I_p = V_s \times I_s",
            font_size=CALC_SIZE, color=LABEL_COLOR,
        )
        power_expand.next_to(power_eq, DOWN, buff=0.3)
        self.play(Write(power_expand), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        # Explanation bullets
        bullet1 = MathTex(
            r"\text{Efikasiteti = 100\%}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        bullet2 = MathTex(
            r"\text{Asnje humbje energjie si nxehtesi}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        bullet3 = MathTex(
            r"\text{Asnje humbje e fluksit magnetik}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )

        bullets = VGroup(bullet1, bullet2, bullet3)
        bullets.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        bullets.next_to(power_expand, DOWN, buff=0.4)
        self.play(
            LaggedStart(
                *[FadeIn(b, shift=RIGHT * 0.3) for b in bullets],
                lag_ratio=0.3,
            ),
            run_time=1.5,
        )
        self.wait(W_AFTER_KEY)

        # Box the answer
        answer_block = VGroup(ans_line1)
        ans_box = make_answer_box(answer_block)
        self.play(Create(ans_box), run_time=0.5)
        self.wait(W_AFTER_ANSWER)

    # ================================================================
    #  FINAL SUMMARY
    # ================================================================
    def final_summary(self):
        self.show_summary_table(
            "Permbledhje e pergjigjeve",
            [
                r"\text{a)}\quad N_s \approx 157 \text{ mbeshtetjella}",
                r"\text{b)}\quad I_s \approx 1{,}53\,\text{A}",
                r"\text{c)}\quad \text{Transformatori eshte ideal (efikasitet 100\%)}",
            ],
            font_size=28,
        )
