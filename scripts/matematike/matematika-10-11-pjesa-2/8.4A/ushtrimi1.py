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
    PART_HEADER_SIZE, STEP_TITLE_SIZE,
    BODY_SIZE, CALC_SIZE, ANSWER_SIZE,
    DIAGRAM_LABEL_SIZE, DIAGRAM_VALUE_SIZE,
    T_STEP_TITLE, T_BODY_FADE, T_KEY_EQUATION, T_ROUTINE_EQUATION,
    T_SHAPE_CREATE, T_LAYOUT_SHIFT, T_TRANSITION,
    W_AFTER_KEY, W_AFTER_ROUTINE, W_AFTER_ANSWER, W_PROBLEM,
    CALC_TOP, PX,
)


class Ushtrimi1(ExerciseScene):
    """
    Ushtrimi 1 -- Njesia 8.4A -- Matematika 10-11: Pjesa II

    Probability frequency tree diagram.
    3250 students surveyed: 2000 live with parents, 1250 do not.
    1/4 of those with parents work part-time.
    3/5 of those without parents work part-time.

    a) Construct frequency tree with counts on each branch.
    b) Find P(works part-time).

    Visual storytelling approach -- no voiceover.
    """

    exercise_number = 1
    unit = "8.4A"
    parts = ["a", "b"]

    # ── Tree geometry constants ──

    ROOT_POS = UP * 3.0
    L1_LEFT = UP * 0.8 + LEFT * 3.5
    L1_RIGHT = UP * 0.8 + RIGHT * 3.5
    L2_LL = DOWN * 1.8 + LEFT * 5.2
    L2_LR = DOWN * 1.8 + LEFT * 1.8
    L2_RL = DOWN * 1.8 + RIGHT * 1.8
    L2_RR = DOWN * 1.8 + RIGHT * 5.2

    NODE_RADIUS = 0.06
    BRANCH_WIDTH = 2.5
    BRANCH_COLOR = DIVIDER_COLOR

    # ================================================================
    #  PART A -- Build the frequency tree
    # ================================================================

    def part_a(self):
        header = self.show_part_header("a")

        # ── Problem statement ──
        prob1 = MathTex(
            r"\text{Nje universitet anketoi 3250 studente.}",
            font_size=STEP_TITLE_SIZE + 2, color=STEP_TITLE_COLOR,
        )
        prob2 = MathTex(
            r"\sim 2000 \text{ jetojne me prindrit.}",
            font_size=BODY_SIZE + 2, color=BODY_TEXT_COLOR,
        )
        prob3 = MathTex(
            r"\tfrac{1}{4} \text{ e tyre punojne me kohe te pjesshme.}",
            font_size=BODY_SIZE + 2, color=BODY_TEXT_COLOR,
        )
        prob4 = MathTex(
            r"\tfrac{3}{5} \text{ e atyre qe nuk jetojne me prindrit punojne PT.}",
            font_size=BODY_SIZE + 2, color=BODY_TEXT_COLOR,
        )
        prob5 = MathTex(
            r"\text{Ndertoni pemen e dendurive.}",
            font_size=STEP_TITLE_SIZE, color=LABEL_COLOR,
        )
        self.show_problem(prob1, prob2, prob3, prob4, prob5, wait_time=5.0)

        # ── Build tree step by step ──
        self._build_tree()

    def _build_tree(self):
        """Animate the full frequency tree construction."""

        # ────────────────────────────────
        # Step 1: Root node — 3250
        # ────────────────────────────────
        root_dot = Dot(self.ROOT_POS, radius=self.NODE_RADIUS, color=WHITE)
        root_label = MathTex(r"3250", font_size=DIAGRAM_LABEL_SIZE, color=WHITE)
        root_label.next_to(root_dot, UP, buff=0.15)

        self.play(GrowFromCenter(root_dot), run_time=0.5)
        self.play(Write(root_label), run_time=T_ROUTINE_EQUATION)
        self.wait(W_AFTER_KEY)

        # ────────────────────────────────
        # Step 2: First split — with parents / without parents
        # ────────────────────────────────

        # Explanatory text
        split_text = MathTex(
            r"\text{Ndajme ne dy grupe:}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        split_text.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(split_text), run_time=T_BODY_FADE)
        self.wait(1.5)

        # Left branch: lives with parents
        branch_left = Line(
            self.ROOT_POS, self.L1_LEFT,
            color=SHAPE_COLOR, stroke_width=2.5,
        )
        l1_left_dot = Dot(self.L1_LEFT, radius=self.NODE_RADIUS, color=SHAPE_COLOR)
        l1_left_val = MathTex(r"2000", font_size=DIAGRAM_LABEL_SIZE, color=SHAPE_COLOR)
        l1_left_val.next_to(l1_left_dot, DOWN, buff=0.15)
        l1_left_desc = MathTex(
            r"\text{Me prindrit}",
            font_size=BODY_SIZE, color=SHAPE_COLOR,
        )
        l1_left_desc.next_to(l1_left_val, DOWN, buff=0.12)

        self.play(
            Create(branch_left, run_time=T_SHAPE_CREATE),
            GrowFromCenter(l1_left_dot),
        )
        self.play(Write(l1_left_val), run_time=T_ROUTINE_EQUATION)
        self.play(FadeIn(l1_left_desc), run_time=0.5)
        self.wait(1.5)

        # Right branch: doesn't live with parents
        # First show subtraction: 3250 - 2000 = 1250
        sub_eq = MathTex(
            r"3250 - 2000 = 1250",
            font_size=BODY_SIZE + 2, color=HIGHLIGHT_COLOR,
        )
        sub_eq.to_edge(DOWN, buff=0.4)
        self.play(
            FadeOut(split_text),
            FadeIn(sub_eq),
            run_time=0.6,
        )
        self.wait(2.0)

        branch_right = Line(
            self.ROOT_POS, self.L1_RIGHT,
            color=HIGHLIGHT_COLOR, stroke_width=2.5,
        )
        l1_right_dot = Dot(self.L1_RIGHT, radius=self.NODE_RADIUS, color=HIGHLIGHT_COLOR)
        l1_right_val = MathTex(r"1250", font_size=DIAGRAM_LABEL_SIZE, color=HIGHLIGHT_COLOR)
        l1_right_val.next_to(l1_right_dot, DOWN, buff=0.15)
        l1_right_desc = MathTex(
            r"\text{Pa prindrit}",
            font_size=BODY_SIZE, color=HIGHLIGHT_COLOR,
        )
        l1_right_desc.next_to(l1_right_val, DOWN, buff=0.12)

        self.play(
            Create(branch_right, run_time=T_SHAPE_CREATE),
            GrowFromCenter(l1_right_dot),
        )
        self.play(Write(l1_right_val), run_time=T_ROUTINE_EQUATION)
        self.play(FadeIn(l1_right_desc), run_time=0.5)
        self.wait(2.0)

        self.play(FadeOut(sub_eq), run_time=0.4)

        # ────────────────────────────────
        # Step 3: Left sub-branches (with parents → PT / not PT)
        # ────────────────────────────────

        # Flash the 1/4 fraction on left branch
        frac_left = MathTex(
            r"\tfrac{1}{4}",
            font_size=DIAGRAM_VALUE_SIZE, color=LABEL_COLOR,
        )
        frac_mid_left = (np.array(self.L1_LEFT) + np.array(self.L2_LL)) / 2
        frac_left.move_to(frac_mid_left + LEFT * 0.4)

        # Show computation: 1/4 x 2000
        comp_text = MathTex(
            r"\tfrac{1}{4} \times 2000",
            font_size=BODY_SIZE + 4, color=LABEL_COLOR,
        )
        comp_text.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(comp_text), run_time=0.5)
        self.wait(1.5)

        comp_step = MathTex(
            r"= \dfrac{2000}{4} = 500",
            font_size=BODY_SIZE + 4, color=ANSWER_COLOR,
        )
        comp_step.next_to(comp_text, RIGHT, buff=0.3)
        self.play(Write(comp_step), run_time=T_KEY_EQUATION)
        self.wait(2.0)

        # Branch: with parents → part-time (500)
        branch_ll = Line(
            self.L1_LEFT, self.L2_LL,
            color=ANSWER_COLOR, stroke_width=2,
        )
        l2_ll_dot = Dot(self.L2_LL, radius=self.NODE_RADIUS, color=ANSWER_COLOR)
        l2_ll_val = MathTex(r"500", font_size=DIAGRAM_VALUE_SIZE, color=ANSWER_COLOR)
        l2_ll_val.next_to(l2_ll_dot, DOWN, buff=0.12)
        l2_ll_desc = MathTex(
            r"\text{PT}",
            font_size=BODY_SIZE - 2, color=ANSWER_COLOR,
        )
        l2_ll_desc.next_to(l2_ll_val, DOWN, buff=0.08)

        self.play(
            Create(branch_ll, run_time=T_SHAPE_CREATE),
            GrowFromCenter(l2_ll_dot),
            FadeIn(frac_left),
        )
        self.play(Write(l2_ll_val), run_time=T_ROUTINE_EQUATION)
        self.play(FadeIn(l2_ll_desc), run_time=0.4)
        self.wait(1.5)

        # Clean up computation
        self.play(FadeOut(comp_text), FadeOut(comp_step), run_time=0.4)

        # Branch: with parents → NOT part-time (1500)
        comp2_text = MathTex(
            r"2000 - 500 = 1500",
            font_size=BODY_SIZE + 4, color=AUX_COLOR,
        )
        comp2_text.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(comp2_text), run_time=0.5)
        self.wait(2.0)

        frac_left_comp = MathTex(
            r"\tfrac{3}{4}",
            font_size=DIAGRAM_VALUE_SIZE, color=LABEL_COLOR,
        )
        frac_mid_left_r = (np.array(self.L1_LEFT) + np.array(self.L2_LR)) / 2
        frac_left_comp.move_to(frac_mid_left_r + RIGHT * 0.4)

        branch_lr = Line(
            self.L1_LEFT, self.L2_LR,
            color=AUX_COLOR, stroke_width=2,
        )
        l2_lr_dot = Dot(self.L2_LR, radius=self.NODE_RADIUS, color=AUX_COLOR)
        l2_lr_val = MathTex(r"1500", font_size=DIAGRAM_VALUE_SIZE, color=AUX_COLOR)
        l2_lr_val.next_to(l2_lr_dot, DOWN, buff=0.12)
        l2_lr_desc = MathTex(
            r"\text{Jo PT}",
            font_size=BODY_SIZE - 2, color=AUX_COLOR,
        )
        l2_lr_desc.next_to(l2_lr_val, DOWN, buff=0.08)

        self.play(
            Create(branch_lr, run_time=T_SHAPE_CREATE),
            GrowFromCenter(l2_lr_dot),
            FadeIn(frac_left_comp),
        )
        self.play(Write(l2_lr_val), run_time=T_ROUTINE_EQUATION)
        self.play(FadeIn(l2_lr_desc), run_time=0.4)
        self.wait(1.5)

        self.play(FadeOut(comp2_text), run_time=0.4)

        # ────────────────────────────────
        # Step 4: Right sub-branches (without parents → PT / not PT)
        # ────────────────────────────────

        # Flash the 3/5 fraction on right branch
        frac_right = MathTex(
            r"\tfrac{3}{5}",
            font_size=DIAGRAM_VALUE_SIZE, color=LABEL_COLOR,
        )
        frac_mid_right = (np.array(self.L1_RIGHT) + np.array(self.L2_RL)) / 2
        frac_right.move_to(frac_mid_right + LEFT * 0.4)

        # Show computation: 3/5 x 1250
        comp3_text = MathTex(
            r"\tfrac{3}{5} \times 1250",
            font_size=BODY_SIZE + 4, color=LABEL_COLOR,
        )
        comp3_text.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(comp3_text), run_time=0.5)
        self.wait(1.5)

        comp3_step = MathTex(
            r"= \dfrac{3 \times 1250}{5} = \dfrac{3750}{5} = 750",
            font_size=BODY_SIZE + 4, color=ANSWER_COLOR,
        )
        comp3_step.next_to(comp3_text, RIGHT, buff=0.3)
        self.play(Write(comp3_step), run_time=T_KEY_EQUATION)
        self.wait(2.0)

        # Branch: without parents → part-time (750)
        branch_rl = Line(
            self.L1_RIGHT, self.L2_RL,
            color=ANSWER_COLOR, stroke_width=2,
        )
        l2_rl_dot = Dot(self.L2_RL, radius=self.NODE_RADIUS, color=ANSWER_COLOR)
        l2_rl_val = MathTex(r"750", font_size=DIAGRAM_VALUE_SIZE, color=ANSWER_COLOR)
        l2_rl_val.next_to(l2_rl_dot, DOWN, buff=0.12)
        l2_rl_desc = MathTex(
            r"\text{PT}",
            font_size=BODY_SIZE - 2, color=ANSWER_COLOR,
        )
        l2_rl_desc.next_to(l2_rl_val, DOWN, buff=0.08)

        self.play(
            Create(branch_rl, run_time=T_SHAPE_CREATE),
            GrowFromCenter(l2_rl_dot),
            FadeIn(frac_right),
        )
        self.play(Write(l2_rl_val), run_time=T_ROUTINE_EQUATION)
        self.play(FadeIn(l2_rl_desc), run_time=0.4)
        self.wait(1.5)

        # Clean up computation
        self.play(FadeOut(comp3_text), FadeOut(comp3_step), run_time=0.4)

        # Branch: without parents → NOT part-time (500)
        comp4_text = MathTex(
            r"1250 - 750 = 500",
            font_size=BODY_SIZE + 4, color=AUX_COLOR,
        )
        comp4_text.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(comp4_text), run_time=0.5)
        self.wait(2.0)

        frac_right_comp = MathTex(
            r"\tfrac{2}{5}",
            font_size=DIAGRAM_VALUE_SIZE, color=LABEL_COLOR,
        )
        frac_mid_right_r = (np.array(self.L1_RIGHT) + np.array(self.L2_RR)) / 2
        frac_right_comp.move_to(frac_mid_right_r + RIGHT * 0.4)

        branch_rr = Line(
            self.L1_RIGHT, self.L2_RR,
            color=AUX_COLOR, stroke_width=2,
        )
        l2_rr_dot = Dot(self.L2_RR, radius=self.NODE_RADIUS, color=AUX_COLOR)
        l2_rr_val = MathTex(r"500", font_size=DIAGRAM_VALUE_SIZE, color=AUX_COLOR)
        l2_rr_val.next_to(l2_rr_dot, DOWN, buff=0.12)
        l2_rr_desc = MathTex(
            r"\text{Jo PT}",
            font_size=BODY_SIZE - 2, color=AUX_COLOR,
        )
        l2_rr_desc.next_to(l2_rr_val, DOWN, buff=0.08)

        self.play(
            Create(branch_rr, run_time=T_SHAPE_CREATE),
            GrowFromCenter(l2_rr_dot),
            FadeIn(frac_right_comp),
        )
        self.play(Write(l2_rr_val), run_time=T_ROUTINE_EQUATION)
        self.play(FadeIn(l2_rr_desc), run_time=0.4)
        self.wait(1.5)

        self.play(FadeOut(comp4_text), run_time=0.4)

        # ────────────────────────────────
        # Step 5: Verification — totals add up
        # ────────────────────────────────
        verify_text = MathTex(
            r"\text{Verifikojme: }",
            font_size=BODY_SIZE + 2, color=STEP_TITLE_COLOR,
        )
        verify_eq = MathTex(
            r"500 + 1500 + 750 + 500 = 3250 \checkmark",
            font_size=BODY_SIZE + 2, color=ANSWER_COLOR,
        )
        verify_group = VGroup(verify_text, verify_eq).arrange(RIGHT, buff=0.2)
        verify_group.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(verify_group), run_time=T_BODY_FADE)
        self.wait(3.0)

        # Store tree mobjects for part b
        self.tree_group = VGroup(
            root_dot, root_label,
            branch_left, l1_left_dot, l1_left_val, l1_left_desc,
            branch_right, l1_right_dot, l1_right_val, l1_right_desc,
            branch_ll, l2_ll_dot, l2_ll_val, l2_ll_desc,
            frac_left,
            branch_lr, l2_lr_dot, l2_lr_val, l2_lr_desc,
            frac_left_comp,
            branch_rl, l2_rl_dot, l2_rl_val, l2_rl_desc,
            frac_right,
            branch_rr, l2_rr_dot, l2_rr_val, l2_rr_desc,
            frac_right_comp,
            verify_group,
        )

        # Store references to PT leaves for part b
        self.pt_left_val = l2_ll_val
        self.pt_right_val = l2_rl_val
        self.pt_left_dot = l2_ll_dot
        self.pt_right_dot = l2_rl_dot

        self.wait(2.0)

    # ================================================================
    #  PART B -- P(works part-time)
    # ================================================================

    def part_b(self):
        header = self.show_part_header("b")

        # ── Problem statement ──
        prob1 = MathTex(
            r"\text{Nje student zgjidhet rastesisht.}",
            font_size=STEP_TITLE_SIZE + 2, color=STEP_TITLE_COLOR,
        )
        prob2 = MathTex(
            r"\text{Gjeni probabilitetin qe ai punon me kohe te pjesshme.}",
            font_size=BODY_SIZE + 2, color=BODY_TEXT_COLOR,
        )
        self.show_problem(prob1, prob2, wait_time=4.0)

        # ── Rebuild tree (smaller, on left side) ──
        self._build_mini_tree()

        # ── Calculation on right panel ──
        divider = make_divider()
        self.play(FadeIn(divider), run_time=0.3)

        self._compute_probability()

    def _build_mini_tree(self):
        """Rebuild the frequency tree smaller on the left side of screen."""
        # Scale and shift tree to left half
        cx = -3.3
        root_pos = np.array([cx, 2.8, 0])
        l1_l = np.array([cx - 2.0, 1.0, 0])
        l1_r = np.array([cx + 2.0, 1.0, 0])
        l2_ll = np.array([cx - 3.0, -0.8, 0])
        l2_lr = np.array([cx - 1.0, -0.8, 0])
        l2_rl = np.array([cx + 1.0, -0.8, 0])
        l2_rr = np.array([cx + 3.0, -0.8, 0])

        sz = 20  # small font
        nd = 0.04  # node radius

        # Root
        root_d = Dot(root_pos, radius=nd, color=WHITE)
        root_l = MathTex(r"3250", font_size=sz, color=WHITE)
        root_l.next_to(root_d, UP, buff=0.1)

        # Level 1
        br_l = Line(root_pos, l1_l, color=SHAPE_COLOR, stroke_width=2)
        d1l = Dot(l1_l, radius=nd, color=SHAPE_COLOR)
        v1l = MathTex(r"2000", font_size=sz, color=SHAPE_COLOR)
        v1l.next_to(d1l, LEFT, buff=0.1)

        br_r = Line(root_pos, l1_r, color=HIGHLIGHT_COLOR, stroke_width=2)
        d1r = Dot(l1_r, radius=nd, color=HIGHLIGHT_COLOR)
        v1r = MathTex(r"1250", font_size=sz, color=HIGHLIGHT_COLOR)
        v1r.next_to(d1r, RIGHT, buff=0.1)

        # Level 2 — left sub-tree
        br_ll = Line(l1_l, l2_ll, color=ANSWER_COLOR, stroke_width=1.5)
        d2ll = Dot(l2_ll, radius=nd, color=ANSWER_COLOR)
        v2ll = MathTex(r"500", font_size=sz, color=ANSWER_COLOR)
        v2ll.next_to(d2ll, DOWN, buff=0.08)
        desc_ll = MathTex(r"\text{PT}", font_size=sz - 4, color=ANSWER_COLOR)
        desc_ll.next_to(v2ll, DOWN, buff=0.05)
        fl = MathTex(r"\tfrac{1}{4}", font_size=sz - 4, color=LABEL_COLOR)
        fl.move_to((np.array(l1_l) + np.array(l2_ll)) / 2 + LEFT * 0.3)

        br_lr = Line(l1_l, l2_lr, color=AUX_COLOR, stroke_width=1.5)
        d2lr = Dot(l2_lr, radius=nd, color=AUX_COLOR)
        v2lr = MathTex(r"1500", font_size=sz, color=AUX_COLOR)
        v2lr.next_to(d2lr, DOWN, buff=0.08)
        desc_lr = MathTex(r"\text{Jo PT}", font_size=sz - 4, color=AUX_COLOR)
        desc_lr.next_to(v2lr, DOWN, buff=0.05)
        flc = MathTex(r"\tfrac{3}{4}", font_size=sz - 4, color=LABEL_COLOR)
        flc.move_to((np.array(l1_l) + np.array(l2_lr)) / 2 + RIGHT * 0.35)

        # Level 2 — right sub-tree
        br_rl = Line(l1_r, l2_rl, color=ANSWER_COLOR, stroke_width=1.5)
        d2rl = Dot(l2_rl, radius=nd, color=ANSWER_COLOR)
        v2rl = MathTex(r"750", font_size=sz, color=ANSWER_COLOR)
        v2rl.next_to(d2rl, DOWN, buff=0.08)
        desc_rl = MathTex(r"\text{PT}", font_size=sz - 4, color=ANSWER_COLOR)
        desc_rl.next_to(v2rl, DOWN, buff=0.05)
        fr = MathTex(r"\tfrac{3}{5}", font_size=sz - 4, color=LABEL_COLOR)
        fr.move_to((np.array(l1_r) + np.array(l2_rl)) / 2 + LEFT * 0.3)

        br_rr = Line(l1_r, l2_rr, color=AUX_COLOR, stroke_width=1.5)
        d2rr = Dot(l2_rr, radius=nd, color=AUX_COLOR)
        v2rr = MathTex(r"500", font_size=sz, color=AUX_COLOR)
        v2rr.next_to(d2rr, DOWN, buff=0.08)
        desc_rr = MathTex(r"\text{Jo PT}", font_size=sz - 4, color=AUX_COLOR)
        desc_rr.next_to(v2rr, DOWN, buff=0.05)
        frc = MathTex(r"\tfrac{2}{5}", font_size=sz - 4, color=LABEL_COLOR)
        frc.move_to((np.array(l1_r) + np.array(l2_rr)) / 2 + RIGHT * 0.35)

        # Assemble and animate
        tree = VGroup(
            root_d, root_l,
            br_l, d1l, v1l,
            br_r, d1r, v1r,
            br_ll, d2ll, v2ll, desc_ll, fl,
            br_lr, d2lr, v2lr, desc_lr, flc,
            br_rl, d2rl, v2rl, desc_rl, fr,
            br_rr, d2rr, v2rr, desc_rr, frc,
        )

        self.play(FadeIn(tree), run_time=1.5)
        self.wait(1.5)

        # Store PT leaf references for highlighting
        self.mini_pt_left = VGroup(d2ll, v2ll, desc_ll)
        self.mini_pt_right = VGroup(d2rl, v2rl, desc_rl)
        self.mini_v2ll = v2ll
        self.mini_v2rl = v2rl
        self.mini_tree = tree

    def _compute_probability(self):
        """Compute P(part-time) = 5/13 on the right panel."""

        # ── Focus on the two PT leaves ──
        self.focus_on(self.mini_pt_left, run_time=0.8)
        self.play(
            Indicate(self.mini_pt_left, color=ANSWER_COLOR),
            run_time=0.6,
        )
        self.focus_on(self.mini_pt_right, run_time=0.8)
        self.play(
            Indicate(self.mini_pt_right, color=ANSWER_COLOR),
            run_time=0.6,
        )
        self.wait(1.0)

        # ── Step 1: Identify part-time totals ──
        t1 = self.panel_title(
            "Studente me kohe te pjesshme:",
            y_pos=2.8,
        )

        eq1 = self.panel_eq(
            r"\text{PT} = 500 + 750",
            t1, buff=0.4, color=ANSWER_COLOR,
        )
        self.wait(1.5)

        eq2 = self.panel_eq(
            r"= 1250",
            eq1, color=ANSWER_COLOR, key=True,
        )
        self.wait(2.0)

        # ── Step 2: Total students ──
        t2 = self.panel_title("Totali:", ref=eq2, buff=0.4)

        eq3 = self.panel_eq(
            r"\text{Total} = 3250",
            t2, color=WHITE,
        )
        self.wait(1.5)

        # ── Step 3: Probability fraction ──
        t3 = self.panel_title("Probabiliteti:", ref=eq3, buff=0.4)

        eq4 = self.panel_eq(
            r"P(\text{PT}) = \dfrac{1250}{3250}",
            t3, buff=0.4, font_size=CALC_SIZE + 2,
        )
        self.wait(2.0)

        # ── Step 4: Simplify the fraction step by step ──
        self.play(
            FadeOut(VGroup(t1, eq1, eq2, t2, eq3, t3)),
            eq4.animate.move_to(np.array([PX, 2.5, 0])),
            run_time=0.7,
        )
        self.wait(0.5)

        simp_title = self.panel_title("Thjeshtojme:", ref=eq4, buff=0.4)

        # Step-by-step simplification
        eq5 = self.panel_eq(
            r"= \dfrac{1250}{3250}",
            simp_title, font_size=CALC_SIZE,
        )
        self.wait(1.0)

        simp_text1 = self.panel_text(
            [r"\text{Pjestojme numeruesin dhe emeruesin me 250:}"],
            eq5, buff=0.3,
        )
        self.wait(2.0)

        eq6 = self.panel_eq(
            r"= \dfrac{1250 \div 250}{3250 \div 250} = \dfrac{5}{13}",
            simp_text1, font_size=CALC_SIZE, color=ANSWER_COLOR, key=True,
        )
        self.wait(2.5)

        # Clean up simplification steps
        self.play(
            FadeOut(VGroup(eq4, simp_title, eq5, simp_text1)),
            eq6.animate.move_to(np.array([PX, 2.0, 0])),
            run_time=0.7,
        )
        self.wait(0.5)

        # ── Step 5: Show alternative — total probability formula ──
        formula_title = self.panel_title(
            "Ligji i probabilitetit total:",
            ref=eq6, buff=0.5,
        )

        eq7 = self.panel_eq(
            r"P(B) = P(B|A) \cdot P(A) + P(B|A') \cdot P(A')",
            formula_title, font_size=BODY_SIZE + 2, color=BODY_TEXT_COLOR,
        )
        self.wait(2.5)

        eq8 = self.panel_eq(
            r"= \tfrac{1}{4} \cdot \tfrac{2000}{3250} + \tfrac{3}{5} \cdot \tfrac{1250}{3250}",
            eq7, font_size=BODY_SIZE + 2,
        )
        self.wait(2.0)

        eq9 = self.panel_eq(
            r"= \tfrac{1}{4} \cdot \tfrac{8}{13} + \tfrac{3}{5} \cdot \tfrac{5}{13}",
            eq8, font_size=BODY_SIZE + 2,
        )
        self.wait(2.0)

        eq10 = self.panel_eq(
            r"= \tfrac{8}{52} + \tfrac{15}{65}",
            eq9, font_size=BODY_SIZE + 2,
        )
        self.wait(1.5)

        eq11 = self.panel_eq(
            r"= \tfrac{2}{13} + \tfrac{3}{13} = \tfrac{5}{13}",
            eq10, font_size=CALC_SIZE, color=ANSWER_COLOR, key=True,
        )
        self.wait(2.0)

        # ── Clean and show final answer ──
        self.play(
            FadeOut(VGroup(
                eq6, formula_title, eq7, eq8, eq9, eq10,
            )),
            eq11.animate.move_to(np.array([PX, 1.5, 0])),
            run_time=0.7,
        )
        self.wait(0.5)

        # ── Final boxed answer ──
        final_ans = MathTex(
            r"P(\text{kohe e pjesshme}) = \dfrac{5}{13}",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        final_ans.move_to(np.array([PX, 0.0, 0]))
        box = make_answer_box(final_ans)

        self.play(
            FadeOut(eq11),
            Write(final_ans),
            run_time=T_KEY_EQUATION,
        )
        self.play(Create(box), run_time=0.5)
        self.highlight_result(VGroup(final_ans, box))
        self.wait(2.0)

        # ── Fraction bar visualization ──
        self.fraction_bar(
            5, 13,
            position=np.array([PX, -1.5, 0]),
            color=ANSWER_COLOR,
            run_time=1.5,
        )

        frac_label = MathTex(
            r"\approx 38.5\%",
            font_size=BODY_SIZE + 2, color=ANSWER_COLOR,
        )
        frac_label.move_to(np.array([PX, -2.2, 0]))
        self.play(FadeIn(frac_label), run_time=0.5)
        self.wait(2.0)

        # ── Celebrate final answer ──
        self.celebrate(VGroup(final_ans, box))
        self.wait(W_AFTER_ANSWER)

    # ================================================================
    #  FINAL SUMMARY
    # ================================================================

    def final_summary(self):
        self.show_summary_table(
            "Permbledhje",
            [
                r"\text{a) } 2000 \text{ me prindrit } (500 \text{ PT}, 1500 \text{ jo})",
                r"\phantom{\text{a) }} 1250 \text{ pa prindrit } (750 \text{ PT}, 500 \text{ jo})",
                r"\text{b) } P(\text{PT}) = \frac{5}{13} \approx 38{,}5\%",
            ],
            font_size=26,
        )
