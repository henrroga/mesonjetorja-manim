"""
YouTube Video — Ushtrimi 6, Njësia 8.5A
Matematika 10-11: Pjesa II

Testi mjekësor / gabimi i bazës (base rate fallacy)
- 800,000 të rritur, sëmundja 1/500 (0.002), testi 98% true positive, 1% false positive
- Pemë: 800,000 → 1,600 sëmurë / 798,400 shëndetshëm → 1,568/32/7,984/790,416
- P(S|N) = 32/790,448 ≈ 0.00004
- P(S|P) = 1,568/9,552 ≈ 0.164 = 16.4% (SURPRIZA)

NOT using ExerciseScene because the tree diagram must persist across all parts.
ExerciseScene calls fade_all() between parts which would destroy it.
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
    T_BODY_FADE, T_KEY_EQUATION, T_ROUTINE_EQUATION, T_SHAPE_CREATE,
    T_LAYOUT_SHIFT, T_TRANSITION,
    W_AFTER_KEY, W_AFTER_ROUTINE, W_AFTER_ANSWER,
    ALBANIAN_TEX, PX,
)

# ── Tree layout coordinates (pre-shift, centered) ──
ROOT = LEFT * 5.0
MID_S = LEFT * 1.8 + UP * 1.8        # Sëmurë (blue)
MID_SH = LEFT * 1.8 + DOWN * 1.8     # Shëndetshëm (red)
END_SP = RIGHT * 2.0 + UP * 2.8      # Sick → Pozitiv (orange)
END_SN = RIGHT * 2.0 + UP * 0.8      # Sick → Negativ (green)
END_SHP = RIGHT * 2.0 + DOWN * 0.8   # Healthy → Pozitiv (orange)
END_SHN = RIGHT * 2.0 + DOWN * 2.8   # Healthy → Negativ (green)


class Ushtrimi6(Scene):
    def construct(self):
        apply_style(self)
        MathTex.set_default(tex_template=ALBANIAN_TEX)
        Tex.set_default(tex_template=ALBANIAN_TEX)

        self.title_screen()
        self.part_a()
        self.part_b()
        self.part_c()
        self.final_summary()
        self.end_screen()

    # ────────────────────────────────────────────
    #  TITLE SCREEN
    # ────────────────────────────────────────────

    def title_screen(self):
        title = MathTex(
            r"\text{Ushtrimi 6 — Njësia 8.5A}",
            font_size=TITLE_SIZE, color=WHITE,
        )
        source = MathTex(
            r"\text{Matematika 10-11: Pjesa II}",
            font_size=SUBTITLE_SIZE, color=BODY_TEXT_COLOR,
        )
        source.next_to(title, DOWN, buff=0.4)

        self.play(Write(title), run_time=T_TITLE_WRITE)
        self.play(FadeIn(source, shift=UP * 0.2), run_time=T_SUBTITLE_FADE)
        self.wait(W_AFTER_KEY)
        self.play(FadeOut(title), FadeOut(source))
        self.wait(0.5)

    # ────────────────────────────────────────────
    #  PART A — Problem + Build Frequency Tree
    # ────────────────────────────────────────────

    def part_a(self):
        header = MathTex(
            r"\text{Pjesa a)}",
            font_size=PART_HEADER_SIZE, color=LABEL_COLOR,
        )
        header.to_corner(UL, buff=0.4)
        self.play(Write(header), run_time=0.5)

        # ── Problem explanation ──
        explain = VGroup(
            MathTex(
                r"\text{800.000 të rritur testohen për një sëmundje.}",
                font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
            ),
            MathTex(
                r"\text{Sëmundja prek 1 në 500 persona (0{,}2\%).}",
                font_size=BODY_SIZE, color=SHAPE_COLOR,
            ),
            MathTex(
                r"\text{Testi: 98\% saktësi për të sëmurët (true positive).}",
                font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
            ),
            MathTex(
                r"\text{Testi: 1\% alarm i rremë për të shëndetshëm (false positive).}",
                font_size=BODY_SIZE, color=AUX_COLOR,
            ),
        ).arrange(DOWN, buff=0.25).move_to(UP * 0.5)

        self.play(
            LaggedStart(*[FadeIn(e, shift=UP * 0.2) for e in explain], lag_ratio=0.2),
            run_time=2.0,
        )
        self.wait(W_AFTER_KEY + 1.0)
        self.play(FadeOut(explain), run_time=T_TRANSITION)
        self.wait(0.3)

        # ── Build the frequency tree ──
        self._build_tree()

        # ── Add probability labels ──
        self._add_probability_labels()
        self.wait(W_AFTER_ROUTINE)

        # ── Calculate level-1 frequencies ──
        self._add_level1_frequencies()
        self.wait(W_AFTER_ROUTINE)

        # ── Build level-2 branches ──
        self._build_level2()
        self.wait(W_AFTER_ROUTINE)

        # ── Add level-2 probability labels ──
        self._add_level2_prob_labels()
        self.wait(W_AFTER_ROUTINE)

        # ── Calculate level-2 frequencies ──
        self._add_level2_frequencies()
        self.wait(W_AFTER_ANSWER)

        # Clean header
        self.play(FadeOut(header), run_time=T_TRANSITION)
        self.wait(0.3)

    def _build_tree(self):
        """Build level-0 and level-1 structure of the tree."""
        # Root
        root_dot = Dot(ROOT, color=WHITE, radius=0.06)
        root_label = MathTex(r"800.000", font_size=20, color=WHITE)
        root_label.next_to(root_dot, LEFT, buff=0.15)

        # Level-1 branches
        branch_s = Line(ROOT, MID_S, color=SHAPE_COLOR, stroke_width=2.5)
        branch_sh = Line(ROOT, MID_SH, color=AUX_COLOR, stroke_width=2.5)

        # Level-1 nodes
        node_s = Dot(MID_S, color=SHAPE_COLOR, radius=0.06)
        node_sh = Dot(MID_SH, color=AUX_COLOR, radius=0.06)

        label_s = MathTex(r"\text{S}", font_size=22, color=SHAPE_COLOR)
        label_s.next_to(node_s, UP, buff=0.15)
        label_sh = MathTex(r"\text{Sh}", font_size=22, color=AUX_COLOR)
        label_sh.next_to(node_sh, DOWN, buff=0.15)

        # Animate root
        self.play(
            GrowFromCenter(root_dot),
            FadeIn(root_label),
            run_time=0.5,
        )

        # Animate level-1 branches
        self.play(
            Create(branch_s), Create(branch_sh),
            run_time=T_SHAPE_CREATE,
        )
        self.play(
            GrowFromCenter(node_s), GrowFromCenter(node_sh),
            FadeIn(label_s), FadeIn(label_sh),
            run_time=0.6,
        )
        self.wait(W_AFTER_ROUTINE)

        # Store refs
        self.root_dot = root_dot
        self.root_label = root_label
        self.branch_s = branch_s
        self.branch_sh = branch_sh
        self.node_s = node_s
        self.node_sh = node_sh
        self.label_s = label_s
        self.label_sh = label_sh

        # Start tree group
        self.tree_group = VGroup(
            root_dot, root_label,
            branch_s, branch_sh,
            node_s, node_sh,
            label_s, label_sh,
        )

    def _add_probability_labels(self):
        """Add probability labels to level-1 branches."""
        p_s = MathTex(r"0{,}002", font_size=16, color=LABEL_COLOR)
        p_s.move_to(self.branch_s.get_center() + UP * 0.3 + LEFT * 0.15)
        p_sh = MathTex(r"0{,}998", font_size=16, color=LABEL_COLOR)
        p_sh.move_to(self.branch_sh.get_center() + DOWN * 0.3 + LEFT * 0.15)

        self.play(
            FadeIn(p_s, shift=DOWN * 0.1),
            FadeIn(p_sh, shift=UP * 0.1),
            run_time=T_BODY_FADE,
        )

        self.p_s = p_s
        self.p_sh = p_sh
        self.tree_group.add(p_s, p_sh)

    def _add_level1_frequencies(self):
        """Calculate and show frequencies at level-1 nodes."""
        # Sick: 800,000 × 0.002 = 1,600
        freq_s = MathTex(r"1.600", font_size=18, color=SHAPE_COLOR)
        freq_s.next_to(self.node_s, RIGHT, buff=0.2)

        # Healthy: 800,000 × 0.998 = 798,400
        freq_sh = MathTex(r"798.400", font_size=18, color=AUX_COLOR)
        freq_sh.next_to(self.node_sh, RIGHT, buff=0.2)

        # Brief calculation overlay
        calc_s = MathTex(
            r"800.000 \times 0{,}002 = 1.600",
            font_size=BODY_SIZE, color=SHAPE_COLOR,
        )
        calc_s.to_edge(UP, buff=0.4)
        self.play(Write(calc_s), run_time=T_KEY_EQUATION)
        self.wait(0.8)
        self.play(FadeIn(freq_s, shift=LEFT * 0.2), run_time=0.5)
        self.play(FadeOut(calc_s), run_time=0.4)

        calc_sh = MathTex(
            r"800.000 \times 0{,}998 = 798.400",
            font_size=BODY_SIZE, color=AUX_COLOR,
        )
        calc_sh.to_edge(UP, buff=0.4)
        self.play(Write(calc_sh), run_time=T_KEY_EQUATION)
        self.wait(0.8)
        self.play(FadeIn(freq_sh, shift=LEFT * 0.2), run_time=0.5)
        self.play(FadeOut(calc_sh), run_time=0.4)

        self.freq_s = freq_s
        self.freq_sh = freq_sh
        self.tree_group.add(freq_s, freq_sh)

    def _build_level2(self):
        """Build level-2 branches and endpoint nodes."""
        # Branches from S (Sick)
        branch_sp = Line(MID_S, END_SP, color=SHAPE_COLOR, stroke_width=2)
        branch_sn = Line(MID_S, END_SN, color=SHAPE_COLOR, stroke_width=2)

        # Branches from Sh (Healthy)
        branch_shp = Line(MID_SH, END_SHP, color=AUX_COLOR, stroke_width=2)
        branch_shn = Line(MID_SH, END_SHN, color=AUX_COLOR, stroke_width=2)

        # Endpoint dots
        dot_sp = Dot(END_SP, color=HIGHLIGHT_COLOR, radius=0.05)
        dot_sn = Dot(END_SN, color=ANSWER_COLOR, radius=0.05)
        dot_shp = Dot(END_SHP, color=HIGHLIGHT_COLOR, radius=0.05)
        dot_shn = Dot(END_SHN, color=ANSWER_COLOR, radius=0.05)

        # Endpoint labels (+/-)
        lbl_sp = MathTex(r"+", font_size=18, color=HIGHLIGHT_COLOR)
        lbl_sp.next_to(dot_sp, UR, buff=0.1)
        lbl_sn = MathTex(r"-", font_size=18, color=ANSWER_COLOR)
        lbl_sn.next_to(dot_sn, DR, buff=0.1)
        lbl_shp = MathTex(r"+", font_size=18, color=HIGHLIGHT_COLOR)
        lbl_shp.next_to(dot_shp, UR, buff=0.1)
        lbl_shn = MathTex(r"-", font_size=18, color=ANSWER_COLOR)
        lbl_shn.next_to(dot_shn, DR, buff=0.1)

        # Animate level-2 branches
        self.play(
            Create(branch_sp), Create(branch_sn),
            Create(branch_shp), Create(branch_shn),
            run_time=T_SHAPE_CREATE,
        )
        self.play(
            GrowFromCenter(dot_sp), GrowFromCenter(dot_sn),
            GrowFromCenter(dot_shp), GrowFromCenter(dot_shn),
            FadeIn(lbl_sp), FadeIn(lbl_sn),
            FadeIn(lbl_shp), FadeIn(lbl_shn),
            run_time=0.6,
        )

        # Store refs
        self.branch_sp = branch_sp
        self.branch_sn = branch_sn
        self.branch_shp = branch_shp
        self.branch_shn = branch_shn
        self.dot_sp = dot_sp
        self.dot_sn = dot_sn
        self.dot_shp = dot_shp
        self.dot_shn = dot_shn
        self.lbl_sp = lbl_sp
        self.lbl_sn = lbl_sn
        self.lbl_shp = lbl_shp
        self.lbl_shn = lbl_shn

        self.tree_group.add(
            branch_sp, branch_sn, branch_shp, branch_shn,
            dot_sp, dot_sn, dot_shp, dot_shn,
            lbl_sp, lbl_sn, lbl_shp, lbl_shn,
        )

    def _add_level2_prob_labels(self):
        """Add probability labels to level-2 branches."""
        # Sick branches: 0.98 (true positive), 0.02 (false negative)
        p_sp = MathTex(r"0{,}98", font_size=16, color=LABEL_COLOR)
        p_sp.move_to(self.branch_sp.get_center() + UP * 0.25 + LEFT * 0.1)
        p_sn = MathTex(r"0{,}02", font_size=16, color=LABEL_COLOR)
        p_sn.move_to(self.branch_sn.get_center() + DOWN * 0.25 + LEFT * 0.1)

        # Healthy branches: 0.01 (false positive), 0.99 (true negative)
        p_shp = MathTex(r"0{,}01", font_size=16, color=LABEL_COLOR)
        p_shp.move_to(self.branch_shp.get_center() + UP * 0.25 + LEFT * 0.1)
        p_shn = MathTex(r"0{,}99", font_size=16, color=LABEL_COLOR)
        p_shn.move_to(self.branch_shn.get_center() + DOWN * 0.25 + LEFT * 0.1)

        self.play(
            FadeIn(p_sp), FadeIn(p_sn),
            FadeIn(p_shp), FadeIn(p_shn),
            run_time=T_BODY_FADE,
        )

        self.p_sp = p_sp
        self.p_sn = p_sn
        self.p_shp = p_shp
        self.p_shn = p_shn
        self.tree_group.add(p_sp, p_sn, p_shp, p_shn)

    def _add_level2_frequencies(self):
        """Calculate and show frequencies at level-2 endpoints."""
        # ── Sick branch ──
        # S → + : 1,600 × 0.98 = 1,568
        calc1 = MathTex(
            r"1.600 \times 0{,}98 = 1.568",
            font_size=BODY_SIZE, color=HIGHLIGHT_COLOR,
        )
        calc1.to_edge(UP, buff=0.4)
        self.play(Write(calc1), run_time=T_KEY_EQUATION)

        freq_sp = MathTex(r"1.568", font_size=16, color=HIGHLIGHT_COLOR)
        freq_sp.next_to(self.dot_sp, RIGHT, buff=0.25)
        self.play(FadeIn(freq_sp, shift=LEFT * 0.2), run_time=0.5)
        self.wait(0.5)
        self.play(FadeOut(calc1), run_time=0.4)

        # S → - : 1,600 × 0.02 = 32
        calc2 = MathTex(
            r"1.600 \times 0{,}02 = 32",
            font_size=BODY_SIZE, color=ANSWER_COLOR,
        )
        calc2.to_edge(UP, buff=0.4)
        self.play(Write(calc2), run_time=T_KEY_EQUATION)

        freq_sn = MathTex(r"32", font_size=16, color=ANSWER_COLOR)
        freq_sn.next_to(self.dot_sn, RIGHT, buff=0.25)
        self.play(FadeIn(freq_sn, shift=LEFT * 0.2), run_time=0.5)
        self.wait(0.5)
        self.play(FadeOut(calc2), run_time=0.4)

        # ── Healthy branch ──
        # Sh → + : 798,400 × 0.01 = 7,984
        calc3 = MathTex(
            r"798.400 \times 0{,}01 = 7.984",
            font_size=BODY_SIZE, color=HIGHLIGHT_COLOR,
        )
        calc3.to_edge(UP, buff=0.4)
        self.play(Write(calc3), run_time=T_KEY_EQUATION)

        freq_shp = MathTex(r"7.984", font_size=16, color=HIGHLIGHT_COLOR)
        freq_shp.next_to(self.dot_shp, RIGHT, buff=0.25)
        self.play(FadeIn(freq_shp, shift=LEFT * 0.2), run_time=0.5)
        self.wait(0.5)
        self.play(FadeOut(calc3), run_time=0.4)

        # Sh → - : 798,400 × 0.99 = 790,416
        calc4 = MathTex(
            r"798.400 \times 0{,}99 = 790.416",
            font_size=BODY_SIZE, color=ANSWER_COLOR,
        )
        calc4.to_edge(UP, buff=0.4)
        self.play(Write(calc4), run_time=T_KEY_EQUATION)

        freq_shn = MathTex(r"790.416", font_size=16, color=ANSWER_COLOR)
        freq_shn.next_to(self.dot_shn, RIGHT, buff=0.25)
        self.play(FadeIn(freq_shn, shift=LEFT * 0.2), run_time=0.5)
        self.wait(0.5)
        self.play(FadeOut(calc4), run_time=0.4)

        # Store refs
        self.freq_sp = freq_sp
        self.freq_sn = freq_sn
        self.freq_shp = freq_shp
        self.freq_shn = freq_shn
        self.tree_group.add(freq_sp, freq_sn, freq_shp, freq_shn)

    # ────────────────────────────────────────────
    #  PART B — P(S|N) = 32 / 790,448
    # ────────────────────────────────────────────

    def part_b(self):
        header = MathTex(
            r"\text{Pjesa b)}",
            font_size=PART_HEADER_SIZE, color=LABEL_COLOR,
        )
        header.to_corner(UL, buff=0.4)
        self.play(Write(header), run_time=0.5)

        # Shift tree left to make room for calculations
        self.play(
            self.tree_group.animate.scale(0.7).move_to(LEFT * 4.0),
            run_time=T_LAYOUT_SHIFT,
        )
        self.wait(0.3)

        # Add divider
        divider = make_divider()
        self.play(Create(divider), run_time=0.3)
        self.divider = divider

        # Part title
        b_title = MathTex(
            r"P(\text{S} | \text{Negativ}) = \; ?",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        b_title.move_to(RIGHT * PX + UP * 3.0)
        self.play(Write(b_title), run_time=T_STEP_TITLE)

        # Highlight the two negative endpoints on the tree
        self.play(
            Indicate(self.freq_sn, color=ANSWER_COLOR, scale_factor=1.5),
            Indicate(self.freq_shn, color=ANSWER_COLOR, scale_factor=1.5),
            run_time=0.8,
        )

        # Total negatives
        why1 = MathTex(
            r"\text{Negativ gjithsej:}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        why1.next_to(b_title, DOWN, buff=0.4).set_x(PX)
        self.play(FadeIn(why1), run_time=T_BODY_FADE)

        eq1 = MathTex(
            r"32 + 790.416 = 790.448",
            font_size=CALC_SIZE, color=WHITE,
        )
        eq1.next_to(why1, DOWN, buff=0.25).set_x(PX)
        self.play(Write(eq1), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        # Sick AND Negative
        why2 = MathTex(
            r"\text{Sëmurë DHE Negativ: } 32",
            font_size=BODY_SIZE, color=SHAPE_COLOR,
        )
        why2.next_to(eq1, DOWN, buff=0.35).set_x(PX)
        self.play(FadeIn(why2), run_time=T_BODY_FADE)
        self.play(Indicate(self.freq_sn, color=SHAPE_COLOR, scale_factor=1.5), run_time=0.6)
        self.wait(0.8)

        # P(S|N) formula
        eq2 = MathTex(
            r"P(\text{S}|\text{N}) = \frac{32}{790.448}",
            font_size=CALC_SIZE, color=WHITE,
        )
        eq2.next_to(why2, DOWN, buff=0.35).set_x(PX)
        self.play(Write(eq2), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        # Result
        ans_b = MathTex(
            r"\approx 0{,}00004",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        ans_b.next_to(eq2, DOWN, buff=0.35).set_x(PX)
        box_b = make_answer_box(ans_b)
        self.play(Write(ans_b), run_time=T_KEY_EQUATION)
        self.play(Create(box_b), run_time=0.4)
        self.wait(0.8)

        # Interpretation
        interp = MathTex(
            r"\text{Testi negativ} = \text{pothuajse i sigurt!}",
            font_size=BODY_SIZE, color=ANSWER_COLOR,
        )
        interp.next_to(box_b, DOWN, buff=0.4).set_x(PX)
        self.play(FadeIn(interp, shift=UP * 0.2), run_time=T_BODY_FADE)
        self.play(
            Circumscribe(VGroup(ans_b, box_b), color=ANSWER_COLOR, run_time=0.8),
        )
        self.wait(W_AFTER_ANSWER)

        # Store answer for summary
        self.ans_b_text = r"\approx 0{,}00004"

        # Clean right panel only (tree stays!)
        self.play(
            FadeOut(header), FadeOut(b_title),
            FadeOut(why1), FadeOut(eq1), FadeOut(why2), FadeOut(eq2),
            FadeOut(ans_b), FadeOut(box_b), FadeOut(interp),
            run_time=T_TRANSITION,
        )
        self.wait(0.3)

    # ────────────────────────────────────────────
    #  PART C — P(S|P) = 1,568 / 9,552 ≈ 16.4% (THE SURPRISE)
    # ────────────────────────────────────────────

    def part_c(self):
        header = MathTex(
            r"\text{Pjesa c)}",
            font_size=PART_HEADER_SIZE, color=LABEL_COLOR,
        )
        header.to_corner(UL, buff=0.4)
        self.play(Write(header), run_time=0.5)

        # Part title
        c_title = MathTex(
            r"P(\text{S} | \text{Pozitiv}) = \; ?",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        c_title.move_to(RIGHT * PX + UP * 3.0)
        self.play(Write(c_title), run_time=T_STEP_TITLE)
        self.wait(0.8)

        # ── TEASE: Let the viewer assume 98% ──
        tease = MathTex(
            r"\text{Testi ka saktësi 98\%...}",
            font_size=CALC_SIZE, color=HIGHLIGHT_COLOR,
        )
        tease.move_to(RIGHT * PX + UP * 1.8)
        self.play(Write(tease), run_time=T_KEY_EQUATION)
        self.wait(3.0)  # Dramatic pause — let viewers think "98%!"
        self.play(FadeOut(tease), run_time=T_TRANSITION)
        self.wait(0.3)

        # Highlight the two positive endpoints on the tree
        self.play(
            Indicate(self.freq_sp, color=HIGHLIGHT_COLOR, scale_factor=1.5),
            Indicate(self.freq_shp, color=HIGHLIGHT_COLOR, scale_factor=1.5),
            run_time=0.8,
        )

        # Total positives
        why1 = MathTex(
            r"\text{Pozitiv gjithsej:}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        why1.next_to(c_title, DOWN, buff=0.4).set_x(PX)
        self.play(FadeIn(why1), run_time=T_BODY_FADE)

        eq1 = MathTex(
            r"1.568 + 7.984 = 9.552",
            font_size=CALC_SIZE, color=WHITE,
        )
        eq1.next_to(why1, DOWN, buff=0.25).set_x(PX)
        self.play(Write(eq1), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        # P(S|P) formula
        eq2 = MathTex(
            r"P(\text{S}|\text{P}) = \frac{1.568}{9.552}",
            font_size=CALC_SIZE, color=WHITE,
        )
        eq2.next_to(eq1, DOWN, buff=0.35).set_x(PX)
        self.play(Write(eq2), run_time=T_KEY_EQUATION)
        self.wait(2.0)  # Dramatic pause before the reveal

        # ── THE REVEAL ──
        ans_c = MathTex(
            r"\approx 0{,}164 = 16{,}4\%",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        ans_c.next_to(eq2, DOWN, buff=0.35).set_x(PX)
        box_c = make_answer_box(ans_c)
        self.play(Write(ans_c), run_time=T_KEY_EQUATION)
        self.play(Create(box_c), run_time=0.4)

        # Circumscribe + Flash for dramatic effect
        self.play(
            Circumscribe(VGroup(ans_c, box_c), color=HIGHLIGHT_COLOR, run_time=1.0),
        )
        self.play(
            Flash(ans_c.get_center(), color=HIGHLIGHT_COLOR, line_length=0.3, num_lines=16, run_time=0.8),
        )
        self.wait(W_AFTER_KEY)

        # ── SURPRISE TEXT ──
        surprise = MathTex(
            r"\text{Vetëm 16{,}4\% — JO 98\%!}",
            font_size=CALC_SIZE + 4, color=HIGHLIGHT_COLOR,
        )
        surprise.next_to(box_c, DOWN, buff=0.5).set_x(PX)
        self.play(Write(surprise), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_KEY)

        # Clean surprise and calculations, but keep answer visible briefly
        self.play(
            FadeOut(c_title), FadeOut(why1), FadeOut(eq1), FadeOut(eq2),
            FadeOut(surprise),
            run_time=T_TRANSITION,
        )
        self.wait(0.3)

        # ── EXPLANATION: Why so low? ──
        exp_title = MathTex(
            r"\text{Pse kaq e ulët?}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        exp_title.move_to(RIGHT * PX + UP * 3.0)
        self.play(Write(exp_title), run_time=T_STEP_TITLE)

        exp1 = MathTex(
            r"\text{Sëmundja: shumë e rrallë (1 në 500)}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        exp1.next_to(exp_title, DOWN, buff=0.4).set_x(PX)
        self.play(FadeIn(exp1, shift=UP * 0.2), run_time=T_BODY_FADE)
        self.wait(W_AFTER_ROUTINE)

        exp2 = MathTex(
            r"\text{7.984 alarme të rreme}",
            font_size=BODY_SIZE, color=HIGHLIGHT_COLOR,
        )
        exp2.next_to(exp1, DOWN, buff=0.3).set_x(PX)
        self.play(FadeIn(exp2, shift=UP * 0.2), run_time=T_BODY_FADE)

        # Indicate the false positive node on the tree
        self.play(
            Indicate(self.freq_shp, color=HIGHLIGHT_COLOR, scale_factor=1.8),
            run_time=0.8,
        )
        self.wait(0.8)

        exp3 = MathTex(
            r"\text{vs vetëm 1.568 të vërtetë}",
            font_size=BODY_SIZE, color=SHAPE_COLOR,
        )
        exp3.next_to(exp2, DOWN, buff=0.3).set_x(PX)
        self.play(FadeIn(exp3, shift=UP * 0.2), run_time=T_BODY_FADE)

        # Indicate the true positive node on the tree
        self.play(
            Indicate(self.freq_sp, color=SHAPE_COLOR, scale_factor=1.5),
            run_time=0.8,
        )
        self.wait(W_AFTER_KEY)

        # Store answer for summary
        self.ans_c_text = r"\approx 0{,}164 = 16{,}4\%"

        # Clean right panel
        self.play(
            FadeOut(header), FadeOut(exp_title),
            FadeOut(exp1), FadeOut(exp2), FadeOut(exp3),
            FadeOut(ans_c), FadeOut(box_c),
            run_time=T_TRANSITION,
        )
        self.wait(0.3)

    # ────────────────────────────────────────────
    #  FINAL SUMMARY
    # ────────────────────────────────────────────

    def final_summary(self):
        # Fade tree and divider for clean summary
        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=T_TRANSITION,
        )
        self.wait(0.3)

        title = MathTex(
            r"\text{Përmbledhje e përgjigjeve}",
            font_size=PART_HEADER_SIZE + 4, color=WHITE,
        )
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=T_TITLE_WRITE)

        rows = VGroup(
            MathTex(
                r"\text{a) Diagrami pemë i frekuencave: i ndërtuar}",
                font_size=24, color=ANSWER_COLOR,
            ),
            MathTex(
                r"\text{b) } P(\text{S}|\text{N}) = \frac{32}{790.448} \approx 0{,}00004",
                font_size=24, color=ANSWER_COLOR,
            ),
            MathTex(
                r"\text{c) } P(\text{S}|\text{P}) = \frac{1.568}{9.552} \approx 16{,}4\%",
                font_size=ANSWER_SIZE, color=HIGHLIGHT_COLOR,
            ),
        )
        rows.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        box = make_answer_box(rows)
        content = VGroup(rows, box).move_to(ORIGIN).shift(DOWN * 0.3)

        if content.get_top()[1] > title.get_bottom()[1] - 0.4:
            content.next_to(title, DOWN, buff=0.5)

        self.play(
            LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3) for r in rows], lag_ratio=0.15),
            run_time=2.0,
        )
        self.play(Create(box), run_time=0.6)

        # Highlight part c as the key takeaway
        self.play(
            Circumscribe(rows[2], color=HIGHLIGHT_COLOR, run_time=1.0),
        )
        self.wait(W_AFTER_ANSWER)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=T_TRANSITION)

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
