"""
YouTube Video — Ushtrimi 4, Njësia 8.4A
Matematika 10-11: Pjesa II

Jetmira shkon në punë me makinë 2 ditë/javë, me autobus 3 ditë/javë.
Vonon 10% me makinë, 20% me autobus.
a) Diagrami pemë i probabiliteteve
b) Diagrami pemë i frekuencave për 150 ditë
c) Gjithsej sa ditë vonon
d) P(Vonë)

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

# ── Tree layout coordinates ─────────────────────
# Root → two branches → four endpoints
# Positions when tree is CENTERED (part_a)
ROOT = LEFT * 4.5
MID_M = LEFT * 1.5 + UP * 1.5   # Makinë node
MID_A = LEFT * 1.5 + DOWN * 1.5  # Autobus node
END_MV = RIGHT * 2.0 + UP * 2.5   # Makinë → Vonë
END_MNK = RIGHT * 2.0 + UP * 0.5  # Makinë → Në Kohë
END_AV = RIGHT * 2.0 + DOWN * 0.5  # Autobus → Vonë
END_ANK = RIGHT * 2.0 + DOWN * 2.5  # Autobus → Në Kohë


class Ushtrimi4(Scene):
    def construct(self):
        apply_style(self)
        MathTex.set_default(tex_template=ALBANIAN_TEX)
        Tex.set_default(tex_template=ALBANIAN_TEX)

        self.title_screen()
        self.part_a()
        self.part_b()
        self.part_c()
        self.part_d()
        self.final_summary()
        self.end_screen()

    # ────────────────────────────────────────────
    #  TITLE SCREEN
    # ────────────────────────────────────────────

    def title_screen(self):
        title = MathTex(
            r"\text{Ushtrimi 4 — Njësia 8.4A}",
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
    #  PART A — Problem explanation + probability tree
    # ────────────────────────────────────────────

    def part_a(self):
        header = MathTex(
            r"\text{Pjesa a)}",
            font_size=PART_HEADER_SIZE, color=LABEL_COLOR,
        )
        header.to_corner(UL, buff=0.4)
        self.play(Write(header), run_time=0.5)

        # Problem explanation
        explain = VGroup(
            MathTex(
                r"\text{Jetmira shkon në punë:}",
                font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
            ),
            MathTex(
                r"\text{Me makinë — 2 ditë/javë}",
                font_size=BODY_SIZE, color=SHAPE_COLOR,
            ),
            MathTex(
                r"\text{Me autobus — 3 ditë/javë}",
                font_size=BODY_SIZE, color=AUX_COLOR,
            ),
            MathTex(
                r"\text{Vonon 10\% me makinë, 20\% me autobus}",
                font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
            ),
        ).arrange(DOWN, buff=0.25).move_to(UP * 0.5)

        self.play(
            LaggedStart(*[FadeIn(e, shift=UP * 0.2) for e in explain], lag_ratio=0.2),
            run_time=1.5,
        )
        self.wait(W_AFTER_KEY)
        self.play(FadeOut(explain), run_time=T_TRANSITION)
        self.wait(0.3)

        # ── Build the probability tree ──
        self._build_tree()

        # Show part header for probabilities
        prob_title = MathTex(
            r"\text{Diagrami pemë i probabiliteteve}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        prob_title.to_edge(UP, buff=0.4)
        self.play(Write(prob_title), run_time=T_STEP_TITLE)
        self.wait(W_AFTER_KEY)

        # Animate probability labels onto branches
        self._add_probability_labels()
        self.wait(W_AFTER_ANSWER)

        # Clean up header and title
        self.play(FadeOut(header), FadeOut(prob_title), run_time=T_TRANSITION)
        self.wait(0.3)

    def _build_tree(self):
        """Build the tree diagram centered on screen."""
        # Root dot
        root_dot = Dot(ROOT, color=WHITE, radius=0.06)
        root_label = MathTex(r"\text{J}", font_size=24, color=WHITE)
        root_label.next_to(root_dot, LEFT, buff=0.15)

        # Branch lines — level 1
        branch_m = Line(ROOT, MID_M, color=SHAPE_COLOR, stroke_width=2.5)
        branch_a = Line(ROOT, MID_A, color=AUX_COLOR, stroke_width=2.5)

        # Mid-level nodes
        node_m = Dot(MID_M, color=SHAPE_COLOR, radius=0.06)
        node_a = Dot(MID_A, color=AUX_COLOR, radius=0.06)

        label_m = MathTex(r"\text{M}", font_size=24, color=SHAPE_COLOR)
        label_m.next_to(node_m, UP, buff=0.15)
        label_a = MathTex(r"\text{A}", font_size=24, color=AUX_COLOR)
        label_a.next_to(node_a, DOWN, buff=0.15)

        # Branch lines — level 2
        branch_mv = Line(MID_M, END_MV, color=SHAPE_COLOR, stroke_width=2)
        branch_mnk = Line(MID_M, END_MNK, color=SHAPE_COLOR, stroke_width=2)
        branch_av = Line(MID_A, END_AV, color=AUX_COLOR, stroke_width=2)
        branch_ank = Line(MID_A, END_ANK, color=AUX_COLOR, stroke_width=2)

        # Endpoint dots and labels
        dot_mv = Dot(END_MV, color=HIGHLIGHT_COLOR, radius=0.05)
        dot_mnk = Dot(END_MNK, color=ANSWER_COLOR, radius=0.05)
        dot_av = Dot(END_AV, color=HIGHLIGHT_COLOR, radius=0.05)
        dot_ank = Dot(END_ANK, color=ANSWER_COLOR, radius=0.05)

        lbl_mv = MathTex(r"\text{V}", font_size=22, color=HIGHLIGHT_COLOR)
        lbl_mv.next_to(dot_mv, RIGHT, buff=0.15)
        lbl_mnk = MathTex(r"\text{NK}", font_size=22, color=ANSWER_COLOR)
        lbl_mnk.next_to(dot_mnk, RIGHT, buff=0.15)
        lbl_av = MathTex(r"\text{V}", font_size=22, color=HIGHLIGHT_COLOR)
        lbl_av.next_to(dot_av, RIGHT, buff=0.15)
        lbl_ank = MathTex(r"\text{NK}", font_size=22, color=ANSWER_COLOR)
        lbl_ank.next_to(dot_ank, RIGHT, buff=0.15)

        # Animate root
        self.play(
            GrowFromCenter(root_dot),
            FadeIn(root_label),
            run_time=0.5,
        )

        # Animate level-1 branches
        self.play(
            Create(branch_m), Create(branch_a),
            run_time=T_SHAPE_CREATE,
        )
        self.play(
            GrowFromCenter(node_m), GrowFromCenter(node_a),
            FadeIn(label_m), FadeIn(label_a),
            run_time=0.6,
        )

        # Animate level-2 branches
        self.play(
            Create(branch_mv), Create(branch_mnk),
            Create(branch_av), Create(branch_ank),
            run_time=T_SHAPE_CREATE,
        )
        self.play(
            GrowFromCenter(dot_mv), GrowFromCenter(dot_mnk),
            GrowFromCenter(dot_av), GrowFromCenter(dot_ank),
            FadeIn(lbl_mv), FadeIn(lbl_mnk),
            FadeIn(lbl_av), FadeIn(lbl_ank),
            run_time=0.6,
        )
        self.wait(W_AFTER_ROUTINE)

        # Store all tree components as instance attributes
        self.tree_branches_l1 = VGroup(branch_m, branch_a)
        self.tree_branches_l2 = VGroup(branch_mv, branch_mnk, branch_av, branch_ank)
        self.tree_nodes = VGroup(root_dot, node_m, node_a, dot_mv, dot_mnk, dot_av, dot_ank)
        self.tree_labels = VGroup(root_label, label_m, label_a, lbl_mv, lbl_mnk, lbl_av, lbl_ank)

        # Individual refs for later use
        self.dot_mv = dot_mv
        self.dot_mnk = dot_mnk
        self.dot_av = dot_av
        self.dot_ank = dot_ank
        self.lbl_mv = lbl_mv
        self.lbl_mnk = lbl_mnk
        self.lbl_av = lbl_av
        self.lbl_ank = lbl_ank
        self.node_m = node_m
        self.node_a = node_a
        self.branch_m = branch_m
        self.branch_a = branch_a
        self.branch_mv = branch_mv
        self.branch_mnk = branch_mnk
        self.branch_av = branch_av
        self.branch_ank = branch_ank

        # Full tree group for shifting later
        self.tree_group = VGroup(
            self.tree_branches_l1, self.tree_branches_l2,
            self.tree_nodes, self.tree_labels,
        )

    def _add_probability_labels(self):
        """Add probability labels to each branch of the tree."""
        # Level 1 probabilities
        p_m = MathTex(r"\frac{2}{5}", font_size=20, color=LABEL_COLOR)
        p_m.move_to(self.branch_m.get_center() + UP * 0.3 + LEFT * 0.1)
        p_a = MathTex(r"\frac{3}{5}", font_size=20, color=LABEL_COLOR)
        p_a.move_to(self.branch_a.get_center() + DOWN * 0.3 + LEFT * 0.1)

        self.play(
            FadeIn(p_m, shift=DOWN * 0.1),
            FadeIn(p_a, shift=UP * 0.1),
            run_time=T_BODY_FADE,
        )
        self.wait(0.5)

        # Level 2 probabilities
        p_mv = MathTex(r"0{,}1", font_size=18, color=LABEL_COLOR)
        p_mv.move_to(self.branch_mv.get_center() + UP * 0.25 + LEFT * 0.05)
        p_mnk = MathTex(r"0{,}9", font_size=18, color=LABEL_COLOR)
        p_mnk.move_to(self.branch_mnk.get_center() + DOWN * 0.25 + LEFT * 0.05)

        p_av = MathTex(r"0{,}2", font_size=18, color=LABEL_COLOR)
        p_av.move_to(self.branch_av.get_center() + UP * 0.25 + LEFT * 0.05)
        p_ank = MathTex(r"0{,}8", font_size=18, color=LABEL_COLOR)
        p_ank.move_to(self.branch_ank.get_center() + DOWN * 0.25 + LEFT * 0.05)

        self.play(
            FadeIn(p_mv), FadeIn(p_mnk),
            FadeIn(p_av), FadeIn(p_ank),
            run_time=T_BODY_FADE,
        )

        # Store probability labels
        self.prob_labels = VGroup(p_m, p_a, p_mv, p_mnk, p_av, p_ank)
        self.tree_group.add(self.prob_labels)

        # Store individual refs
        self.p_m = p_m
        self.p_a = p_a
        self.p_mv = p_mv
        self.p_mnk = p_mnk
        self.p_av = p_av
        self.p_ank = p_ank

    # ────────────────────────────────────────────
    #  PART B — Frequency tree for 150 days
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
            self.tree_group.animate.scale(0.75).move_to(LEFT * 3.8),
            run_time=T_LAYOUT_SHIFT,
        )
        self.wait(0.3)

        # Add divider
        divider = make_divider()
        self.play(Create(divider), run_time=0.3)
        self.divider = divider

        # Right panel title
        freq_title = MathTex(
            r"\text{Frekuencat për 150 ditë}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        freq_title.move_to(RIGHT * PX + UP * 3.0)
        self.play(Write(freq_title), run_time=T_STEP_TITLE)

        # Step 1: Split 150 into car/bus
        why1 = MathTex(
            r"\text{Ditë me makinë:}",
            font_size=BODY_SIZE, color=SHAPE_COLOR,
        )
        why1.move_to(RIGHT * PX + UP * 2.2)

        eq1 = MathTex(
            r"150 \times \frac{2}{5} = 60",
            font_size=CALC_SIZE, color=WHITE,
        )
        eq1.next_to(why1, DOWN, buff=0.25).set_x(PX)
        self.play(FadeIn(why1), run_time=T_BODY_FADE)
        self.play(Write(eq1), run_time=T_KEY_EQUATION)

        # Animate 60 onto the tree near node M
        val_60 = MathTex(r"60", font_size=18, color=SHAPE_COLOR)
        val_60.move_to(self.node_m.get_center() + RIGHT * 0.35 + UP * 0.05)
        val_copy = eq1[-1].copy()
        self.play(
            val_copy.animate.move_to(val_60).scale(0.5),
            run_time=0.8,
        )
        self.play(FadeOut(val_copy), FadeIn(val_60), run_time=0.3)
        self.tree_group.add(val_60)
        self.wait(0.5)

        why2 = MathTex(
            r"\text{Ditë me autobus:}",
            font_size=BODY_SIZE, color=AUX_COLOR,
        )
        why2.next_to(eq1, DOWN, buff=0.35).set_x(PX)

        eq2 = MathTex(
            r"150 \times \frac{3}{5} = 90",
            font_size=CALC_SIZE, color=WHITE,
        )
        eq2.next_to(why2, DOWN, buff=0.25).set_x(PX)
        self.play(FadeIn(why2), run_time=T_BODY_FADE)
        self.play(Write(eq2), run_time=T_KEY_EQUATION)

        # Animate 90 onto the tree near node A
        val_90 = MathTex(r"90", font_size=18, color=AUX_COLOR)
        val_90.move_to(self.node_a.get_center() + RIGHT * 0.35 + DOWN * 0.05)
        val_copy2 = eq2[-1].copy()
        self.play(
            val_copy2.animate.move_to(val_90).scale(0.5),
            run_time=0.8,
        )
        self.play(FadeOut(val_copy2), FadeIn(val_90), run_time=0.3)
        self.tree_group.add(val_90)
        self.wait(W_AFTER_ROUTINE)

        # Clear right panel for next calculations
        self.play(
            FadeOut(freq_title), FadeOut(why1), FadeOut(eq1),
            FadeOut(why2), FadeOut(eq2),
            run_time=T_TRANSITION,
        )

        # Step 2: Split car days into late/on-time
        car_title = MathTex(
            r"\text{Nga 60 ditë me makinë:}",
            font_size=STEP_TITLE_SIZE, color=SHAPE_COLOR,
        )
        car_title.move_to(RIGHT * PX + UP * 2.8)
        self.play(Write(car_title), run_time=T_STEP_TITLE)
        self.play(Indicate(self.node_m, color=SHAPE_COLOR), run_time=0.5)

        eq3 = MathTex(
            r"\text{Vonë: } 60 \times 0{,}1 = 6",
            font_size=CALC_SIZE, color=WHITE,
        )
        eq3.next_to(car_title, DOWN, buff=0.35).set_x(PX)
        self.play(Write(eq3), run_time=T_KEY_EQUATION)

        # Animate 6 onto tree
        val_6 = MathTex(r"6", font_size=18, color=HIGHLIGHT_COLOR)
        val_6.next_to(self.dot_mv, RIGHT, buff=0.4)
        self.play(FadeIn(val_6, shift=LEFT * 0.2), run_time=0.5)
        self.tree_group.add(val_6)
        self.val_6 = val_6

        eq4 = MathTex(
            r"\text{Në kohë: } 60 \times 0{,}9 = 54",
            font_size=CALC_SIZE, color=WHITE,
        )
        eq4.next_to(eq3, DOWN, buff=0.3).set_x(PX)
        self.play(Write(eq4), run_time=T_KEY_EQUATION)

        # Animate 54 onto tree
        val_54 = MathTex(r"54", font_size=18, color=ANSWER_COLOR)
        val_54.next_to(self.dot_mnk, RIGHT, buff=0.4)
        self.play(FadeIn(val_54, shift=LEFT * 0.2), run_time=0.5)
        self.tree_group.add(val_54)
        self.wait(W_AFTER_ROUTINE)

        # Clear and do bus
        self.play(
            FadeOut(car_title), FadeOut(eq3), FadeOut(eq4),
            run_time=T_TRANSITION,
        )

        bus_title = MathTex(
            r"\text{Nga 90 ditë me autobus:}",
            font_size=STEP_TITLE_SIZE, color=AUX_COLOR,
        )
        bus_title.move_to(RIGHT * PX + UP * 2.8)
        self.play(Write(bus_title), run_time=T_STEP_TITLE)
        self.play(Indicate(self.node_a, color=AUX_COLOR), run_time=0.5)

        eq5 = MathTex(
            r"\text{Vonë: } 90 \times 0{,}2 = 18",
            font_size=CALC_SIZE, color=WHITE,
        )
        eq5.next_to(bus_title, DOWN, buff=0.35).set_x(PX)
        self.play(Write(eq5), run_time=T_KEY_EQUATION)

        # Animate 18 onto tree
        val_18 = MathTex(r"18", font_size=18, color=HIGHLIGHT_COLOR)
        val_18.next_to(self.dot_av, RIGHT, buff=0.4)
        self.play(FadeIn(val_18, shift=LEFT * 0.2), run_time=0.5)
        self.tree_group.add(val_18)
        self.val_18 = val_18

        eq6 = MathTex(
            r"\text{Në kohë: } 90 \times 0{,}8 = 72",
            font_size=CALC_SIZE, color=WHITE,
        )
        eq6.next_to(eq5, DOWN, buff=0.3).set_x(PX)
        self.play(Write(eq6), run_time=T_KEY_EQUATION)

        # Animate 72 onto tree
        val_72 = MathTex(r"72", font_size=18, color=ANSWER_COLOR)
        val_72.next_to(self.dot_ank, RIGHT, buff=0.4)
        self.play(FadeIn(val_72, shift=LEFT * 0.2), run_time=0.5)
        self.tree_group.add(val_72)
        self.wait(W_AFTER_KEY)

        # Add 150 at root
        val_150 = MathTex(r"150", font_size=18, color=WHITE)
        val_150.next_to(
            self.tree_nodes[0], LEFT, buff=0.3,
        )
        self.play(FadeIn(val_150), run_time=0.4)
        self.tree_group.add(val_150)

        self.wait(W_AFTER_ANSWER)

        # Clean right panel
        self.play(
            FadeOut(bus_title), FadeOut(eq5), FadeOut(eq6),
            FadeOut(header),
            run_time=T_TRANSITION,
        )
        self.wait(0.3)

    # ────────────────────────────────────────────
    #  PART C — Total late days
    # ────────────────────────────────────────────

    def part_c(self):
        header = MathTex(
            r"\text{Pjesa c)}",
            font_size=PART_HEADER_SIZE, color=LABEL_COLOR,
        )
        header.to_corner(UL, buff=0.4)
        self.play(Write(header), run_time=0.5)

        # Highlight the "late" endpoints on the tree
        self.play(
            Indicate(self.val_6, color=HIGHLIGHT_COLOR, scale_factor=1.5),
            Indicate(self.val_18, color=HIGHLIGHT_COLOR, scale_factor=1.5),
            run_time=0.8,
        )
        self.play(
            Indicate(self.dot_mv, color=HIGHLIGHT_COLOR, scale_factor=2),
            Indicate(self.dot_av, color=HIGHLIGHT_COLOR, scale_factor=2),
            run_time=0.6,
        )

        # Right panel calculation
        q_text = MathTex(
            r"\text{Sa ditë vonon gjithsej?}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        q_text.move_to(RIGHT * PX + UP * 2.5)
        self.play(Write(q_text), run_time=T_STEP_TITLE)

        why = MathTex(
            r"\text{Mbledhim vonësat:}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        why.next_to(q_text, DOWN, buff=0.4).set_x(PX)
        self.play(FadeIn(why), run_time=T_BODY_FADE)

        eq = MathTex(
            r"6 + 18 = 24",
            font_size=CALC_SIZE, color=WHITE,
        )
        eq.next_to(why, DOWN, buff=0.35).set_x(PX)
        self.play(Write(eq), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        ans = MathTex(
            r"\text{Vonon } 24 \text{ ditë nga } 150",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        ans.next_to(eq, DOWN, buff=0.5).set_x(PX)
        box = make_answer_box(ans)
        self.play(Write(ans), run_time=T_KEY_EQUATION)
        self.play(Create(box), run_time=0.4)
        self.play(
            Circumscribe(VGroup(ans, box), color=HIGHLIGHT_COLOR, run_time=0.8),
        )
        self.wait(W_AFTER_ANSWER)

        # Clean right panel
        self.play(
            FadeOut(header), FadeOut(q_text), FadeOut(why),
            FadeOut(eq), FadeOut(ans), FadeOut(box),
            run_time=T_TRANSITION,
        )
        self.wait(0.3)

    # ────────────────────────────────────────────
    #  PART D — P(Vonë) using total probability
    # ────────────────────────────────────────────

    def part_d(self):
        header = MathTex(
            r"\text{Pjesa d)}",
            font_size=PART_HEADER_SIZE, color=LABEL_COLOR,
        )
        header.to_corner(UL, buff=0.4)
        self.play(Write(header), run_time=0.5)

        # Right panel title
        d_title = MathTex(
            r"\text{Probabiliteti i përgjithshëm i vonesës}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        d_title.move_to(RIGHT * PX + UP * 3.0)
        self.play(Write(d_title), run_time=T_STEP_TITLE)

        # Formula
        why = MathTex(
            r"\text{Ligji i probabilitetit total:}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        why.next_to(d_title, DOWN, buff=0.35).set_x(PX)
        self.play(FadeIn(why), run_time=T_BODY_FADE)

        formula = MathTex(
            r"P(V) = P(M) \cdot P(V|M) + P(A) \cdot P(V|A)",
            font_size=22, color=WHITE,
        )
        formula.next_to(why, DOWN, buff=0.3).set_x(PX)
        self.play(Write(formula), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        # Flash the relevant branches on the tree
        self.play(
            Indicate(self.branch_mv, color=LABEL_COLOR),
            Indicate(self.branch_av, color=LABEL_COLOR),
            run_time=0.6,
        )

        # Substitution
        sub = MathTex(
            r"P(V) = \frac{2}{5} \times 0{,}1 + \frac{3}{5} \times 0{,}2",
            font_size=22, color=WHITE,
        )
        sub.next_to(formula, DOWN, buff=0.3).set_x(PX)
        self.play(Write(sub), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        # Compute step by step
        step1 = MathTex(
            r"= 0{,}04 + 0{,}12",
            font_size=CALC_SIZE, color=WHITE,
        )
        step1.next_to(sub, DOWN, buff=0.3).set_x(PX)
        self.play(Write(step1), run_time=T_ROUTINE_EQUATION)
        self.wait(0.8)

        # Final answer
        ans = MathTex(
            r"P(V) = 0{,}16",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        ans.next_to(step1, DOWN, buff=0.4).set_x(PX)
        box = make_answer_box(ans)
        self.play(Write(ans), run_time=T_KEY_EQUATION)
        self.play(Create(box), run_time=0.4)
        self.play(
            Flash(ans.get_center(), color=ANSWER_COLOR, line_length=0.2, num_lines=12, run_time=0.6),
        )
        self.wait(W_AFTER_ANSWER)

        # Clean everything for summary
        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=T_TRANSITION,
        )
        self.wait(0.3)

    # ────────────────────────────────────────────
    #  FINAL SUMMARY
    # ────────────────────────────────────────────

    def final_summary(self):
        title = MathTex(
            r"\text{Përmbledhje e përgjigjeve}",
            font_size=PART_HEADER_SIZE + 4, color=WHITE,
        )
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=T_TITLE_WRITE)

        rows = VGroup(
            MathTex(
                r"\text{a) Diagrami pemë me } P(M)=\tfrac{2}{5}, \; P(A)=\tfrac{3}{5}",
                font_size=24, color=ANSWER_COLOR,
            ),
            MathTex(
                r"\text{b) Frekuencat: } 6, \; 54, \; 18, \; 72",
                font_size=24, color=ANSWER_COLOR,
            ),
            MathTex(
                r"\text{c) Ditë me vonesë: } 6 + 18 = 24",
                font_size=24, color=ANSWER_COLOR,
            ),
            MathTex(
                r"\text{d) } P(V) = 0{,}16",
                font_size=ANSWER_SIZE, color=ANSWER_COLOR,
            ),
        )
        rows.arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        box = make_answer_box(rows)
        content = VGroup(rows, box).move_to(ORIGIN).shift(DOWN * 0.3)

        if content.get_top()[1] > title.get_bottom()[1] - 0.4:
            content.next_to(title, DOWN, buff=0.5)

        self.play(
            LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3) for r in rows], lag_ratio=0.15),
            run_time=2.0,
        )
        self.play(Create(box), run_time=0.6)
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
