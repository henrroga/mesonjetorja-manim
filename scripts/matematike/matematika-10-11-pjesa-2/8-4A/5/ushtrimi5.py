"""
YouTube Video — Ushtrimi 5, Njësia 8.4A
Matematika 10-11: Pjesa II

Testi i dopingut — diagrami pemë i frekuencave
500 atletë, 20% përdorin barna.
Përdoruesit: 19/20 pozitivë. Jo-përdoruesit: 1/50 pozitivë (alarme të rreme).
a) Diagrami pemë i frekuencave
b) Sa atletë rezultojnë pozitivë gjithsej
c) Pozitivë të rremë (jo-përdorues që testojnë pozitiv)
d) P(rezultat i saktë)

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
MID_U = LEFT * 1.5 + UP * 1.5    # Përdorin barna (users)
MID_N = LEFT * 1.5 + DOWN * 1.5  # Nuk përdorin (non-users)
END_UP = RIGHT * 2.0 + UP * 2.5   # Users → Positive
END_UN = RIGHT * 2.0 + UP * 0.5   # Users → Negative
END_NP = RIGHT * 2.0 + DOWN * 0.5  # Non-users → Positive
END_NN = RIGHT * 2.0 + DOWN * 2.5  # Non-users → Negative


class Ushtrimi5(Scene):
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
            r"\text{Ushtrimi 5 — Njësia 8.4A}",
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
    #  PART A — Build frequency tree
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
                r"\text{Testi i dopingut për 500 atletë:}",
                font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
            ),
            MathTex(
                r"\text{20\% përdorin barna}",
                font_size=BODY_SIZE, color=SHAPE_COLOR,
            ),
            MathTex(
                r"\text{Përdoruesit: 19/20 testojnë pozitiv}",
                font_size=BODY_SIZE, color=SHAPE_COLOR,
            ),
            MathTex(
                r"\text{Jo-përdoruesit: 1/50 testojnë pozitiv}",
                font_size=BODY_SIZE, color=AUX_COLOR,
            ),
        ).arrange(DOWN, buff=0.25).move_to(UP * 0.5)

        self.play(
            LaggedStart(*[FadeIn(e, shift=UP * 0.2) for e in explain], lag_ratio=0.2),
            run_time=1.5,
        )
        self.wait(W_AFTER_KEY)
        self.play(FadeOut(explain), run_time=T_TRANSITION)
        self.wait(0.3)

        # ── Build the frequency tree ──
        self._build_tree()

        # Show title
        freq_title = MathTex(
            r"\text{Diagrami pemë i frekuencave}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        freq_title.to_edge(UP, buff=0.4)
        self.play(Write(freq_title), run_time=T_STEP_TITLE)
        self.wait(0.5)

        # Animate probability labels onto branches
        self._add_probability_labels()
        self.wait(0.5)

        # Animate frequency values onto endpoints
        self._add_frequency_values()
        self.wait(W_AFTER_ANSWER)

        # Clean up header and title
        self.play(FadeOut(header), FadeOut(freq_title), run_time=T_TRANSITION)
        self.wait(0.3)

    def _build_tree(self):
        """Build the tree diagram centered on screen."""
        # Root dot
        root_dot = Dot(ROOT, color=WHITE, radius=0.06)
        root_label = MathTex(r"500", font_size=22, color=WHITE)
        root_label.next_to(root_dot, LEFT, buff=0.15)

        # Branch lines — level 1
        branch_u = Line(ROOT, MID_U, color=SHAPE_COLOR, stroke_width=2.5)
        branch_n = Line(ROOT, MID_N, color=AUX_COLOR, stroke_width=2.5)

        # Mid-level nodes
        node_u = Dot(MID_U, color=SHAPE_COLOR, radius=0.06)
        node_n = Dot(MID_N, color=AUX_COLOR, radius=0.06)

        label_u = MathTex(
            r"\text{Përdorin}",
            font_size=18, color=SHAPE_COLOR,
        )
        label_u.next_to(node_u, UP, buff=0.15)
        label_n = MathTex(
            r"\text{Nuk përdorin}",
            font_size=18, color=AUX_COLOR,
        )
        label_n.next_to(node_n, DOWN, buff=0.15)

        # Frequency values at mid-level nodes
        val_100 = MathTex(r"100", font_size=20, color=SHAPE_COLOR)
        val_100.next_to(node_u, RIGHT, buff=0.2)
        val_400 = MathTex(r"400", font_size=20, color=AUX_COLOR)
        val_400.next_to(node_n, RIGHT, buff=0.2)

        # Branch lines — level 2
        branch_up = Line(MID_U, END_UP, color=SHAPE_COLOR, stroke_width=2)
        branch_un = Line(MID_U, END_UN, color=SHAPE_COLOR, stroke_width=2)
        branch_np = Line(MID_N, END_NP, color=AUX_COLOR, stroke_width=2)
        branch_nn = Line(MID_N, END_NN, color=AUX_COLOR, stroke_width=2)

        # Endpoint dots and labels
        dot_up = Dot(END_UP, color=HIGHLIGHT_COLOR, radius=0.05)
        dot_un = Dot(END_UN, color=ANSWER_COLOR, radius=0.05)
        dot_np = Dot(END_NP, color=HIGHLIGHT_COLOR, radius=0.05)
        dot_nn = Dot(END_NN, color=ANSWER_COLOR, radius=0.05)

        lbl_up = MathTex(r"+", font_size=22, color=HIGHLIGHT_COLOR)
        lbl_up.next_to(dot_up, RIGHT, buff=0.15)
        lbl_un = MathTex(r"-", font_size=22, color=ANSWER_COLOR)
        lbl_un.next_to(dot_un, RIGHT, buff=0.15)
        lbl_np = MathTex(r"+", font_size=22, color=HIGHLIGHT_COLOR)
        lbl_np.next_to(dot_np, RIGHT, buff=0.15)
        lbl_nn = MathTex(r"-", font_size=22, color=ANSWER_COLOR)
        lbl_nn.next_to(dot_nn, RIGHT, buff=0.15)

        # Animate root
        self.play(
            GrowFromCenter(root_dot),
            FadeIn(root_label),
            run_time=0.5,
        )

        # Animate level-1 branches
        self.play(
            Create(branch_u), Create(branch_n),
            run_time=T_SHAPE_CREATE,
        )
        self.play(
            GrowFromCenter(node_u), GrowFromCenter(node_n),
            FadeIn(label_u), FadeIn(label_n),
            run_time=0.6,
        )

        # Show 100 and 400 at mid-level
        self.play(
            FadeIn(val_100, shift=LEFT * 0.2),
            FadeIn(val_400, shift=LEFT * 0.2),
            run_time=0.6,
        )
        self.wait(W_AFTER_ROUTINE)

        # Animate level-2 branches
        self.play(
            Create(branch_up), Create(branch_un),
            Create(branch_np), Create(branch_nn),
            run_time=T_SHAPE_CREATE,
        )
        self.play(
            GrowFromCenter(dot_up), GrowFromCenter(dot_un),
            GrowFromCenter(dot_np), GrowFromCenter(dot_nn),
            FadeIn(lbl_up), FadeIn(lbl_un),
            FadeIn(lbl_np), FadeIn(lbl_nn),
            run_time=0.6,
        )
        self.wait(W_AFTER_ROUTINE)

        # Store all tree components as instance attributes
        self.tree_branches_l1 = VGroup(branch_u, branch_n)
        self.tree_branches_l2 = VGroup(branch_up, branch_un, branch_np, branch_nn)
        self.tree_nodes = VGroup(root_dot, node_u, node_n, dot_up, dot_un, dot_np, dot_nn)
        self.tree_labels = VGroup(
            root_label, label_u, label_n,
            lbl_up, lbl_un, lbl_np, lbl_nn,
        )
        self.tree_mid_vals = VGroup(val_100, val_400)

        # Individual refs for later use
        self.dot_up = dot_up
        self.dot_un = dot_un
        self.dot_np = dot_np
        self.dot_nn = dot_nn
        self.lbl_up = lbl_up
        self.lbl_un = lbl_un
        self.lbl_np = lbl_np
        self.lbl_nn = lbl_nn
        self.node_u = node_u
        self.node_n = node_n
        self.branch_u = branch_u
        self.branch_n = branch_n
        self.branch_up = branch_up
        self.branch_un = branch_un
        self.branch_np = branch_np
        self.branch_nn = branch_nn

        # Full tree group for shifting later
        self.tree_group = VGroup(
            self.tree_branches_l1, self.tree_branches_l2,
            self.tree_nodes, self.tree_labels,
            self.tree_mid_vals,
        )

    def _add_probability_labels(self):
        """Add probability labels to each branch of the tree."""
        # Level 1 probabilities
        p_u = MathTex(r"0{,}20", font_size=18, color=LABEL_COLOR)
        p_u.move_to(self.branch_u.get_center() + UP * 0.3 + LEFT * 0.1)
        p_n = MathTex(r"0{,}80", font_size=18, color=LABEL_COLOR)
        p_n.move_to(self.branch_n.get_center() + DOWN * 0.3 + LEFT * 0.1)

        self.play(
            FadeIn(p_u, shift=DOWN * 0.1),
            FadeIn(p_n, shift=UP * 0.1),
            run_time=T_BODY_FADE,
        )
        self.wait(0.5)

        # Level 2 probabilities
        p_up = MathTex(r"\frac{19}{20}", font_size=16, color=LABEL_COLOR)
        p_up.move_to(self.branch_up.get_center() + UP * 0.3 + LEFT * 0.05)
        p_un = MathTex(r"\frac{1}{20}", font_size=16, color=LABEL_COLOR)
        p_un.move_to(self.branch_un.get_center() + DOWN * 0.3 + LEFT * 0.05)

        p_np = MathTex(r"\frac{1}{50}", font_size=16, color=LABEL_COLOR)
        p_np.move_to(self.branch_np.get_center() + UP * 0.3 + LEFT * 0.05)
        p_nn = MathTex(r"\frac{49}{50}", font_size=16, color=LABEL_COLOR)
        p_nn.move_to(self.branch_nn.get_center() + DOWN * 0.3 + LEFT * 0.05)

        self.play(
            FadeIn(p_up), FadeIn(p_un),
            FadeIn(p_np), FadeIn(p_nn),
            run_time=T_BODY_FADE,
        )

        # Store probability labels
        self.prob_labels = VGroup(p_u, p_n, p_up, p_un, p_np, p_nn)
        self.tree_group.add(self.prob_labels)

    def _add_frequency_values(self):
        """Add frequency values at each endpoint of the tree."""
        # Endpoint frequency values
        val_95 = MathTex(r"95", font_size=20, color=HIGHLIGHT_COLOR)
        val_95.next_to(self.lbl_up, RIGHT, buff=0.25)
        val_5 = MathTex(r"5", font_size=20, color=ANSWER_COLOR)
        val_5.next_to(self.lbl_un, RIGHT, buff=0.25)
        val_8 = MathTex(r"8", font_size=20, color=HIGHLIGHT_COLOR)
        val_8.next_to(self.lbl_np, RIGHT, buff=0.25)
        val_392 = MathTex(r"392", font_size=20, color=ANSWER_COLOR)
        val_392.next_to(self.lbl_nn, RIGHT, buff=0.25)

        # Animate them appearing one by one with Indicate on branches
        self.play(Indicate(self.branch_up, color=LABEL_COLOR), run_time=0.4)
        self.play(FadeIn(val_95, shift=LEFT * 0.2), run_time=0.5)

        self.play(Indicate(self.branch_un, color=LABEL_COLOR), run_time=0.4)
        self.play(FadeIn(val_5, shift=LEFT * 0.2), run_time=0.5)

        self.play(Indicate(self.branch_np, color=LABEL_COLOR), run_time=0.4)
        self.play(FadeIn(val_8, shift=LEFT * 0.2), run_time=0.5)

        self.play(Indicate(self.branch_nn, color=LABEL_COLOR), run_time=0.4)
        self.play(FadeIn(val_392, shift=LEFT * 0.2), run_time=0.5)

        self.val_95 = val_95
        self.val_5 = val_5
        self.val_8 = val_8
        self.val_392 = val_392

        self.tree_end_vals = VGroup(val_95, val_5, val_8, val_392)
        self.tree_group.add(self.tree_end_vals)

    # ────────────────────────────────────────────
    #  PART B — Total positive tests
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

        # Highlight the two positive endpoints
        self.play(
            Indicate(self.val_95, color=HIGHLIGHT_COLOR, scale_factor=1.5),
            Indicate(self.val_8, color=HIGHLIGHT_COLOR, scale_factor=1.5),
            run_time=0.8,
        )
        self.play(
            Indicate(self.dot_up, color=HIGHLIGHT_COLOR, scale_factor=2),
            Indicate(self.dot_np, color=HIGHLIGHT_COLOR, scale_factor=2),
            run_time=0.6,
        )

        # Right panel
        q_text = MathTex(
            r"\text{Sa atletë testojnë pozitiv?}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        q_text.move_to(RIGHT * PX + UP * 2.5)
        self.play(Write(q_text), run_time=T_STEP_TITLE)

        why = MathTex(
            r"\text{Mbledhim të dy degët pozitive:}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        why.next_to(q_text, DOWN, buff=0.4).set_x(PX)
        self.play(FadeIn(why), run_time=T_BODY_FADE)

        eq = MathTex(
            r"95 + 8 = 103",
            font_size=CALC_SIZE, color=WHITE,
        )
        eq.next_to(why, DOWN, buff=0.35).set_x(PX)
        self.play(Write(eq), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        ans = MathTex(
            r"\text{Total pozitiv} = 103",
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
    #  PART C — False positives
    # ────────────────────────────────────────────

    def part_c(self):
        header = MathTex(
            r"\text{Pjesa c)}",
            font_size=PART_HEADER_SIZE, color=LABEL_COLOR,
        )
        header.to_corner(UL, buff=0.4)
        self.play(Write(header), run_time=0.5)

        # Highlight the false positive endpoint (8)
        self.play(
            Indicate(self.val_8, color=HIGHLIGHT_COLOR, scale_factor=1.8),
            run_time=0.8,
        )
        self.play(
            Indicate(self.dot_np, color=HIGHLIGHT_COLOR, scale_factor=2),
            Indicate(self.branch_np, color=HIGHLIGHT_COLOR),
            run_time=0.6,
        )

        # Right panel
        q_text = MathTex(
            r"\text{Pozitivë të rremë (false positives)?}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        q_text.move_to(RIGHT * PX + UP * 2.5)
        self.play(Write(q_text), run_time=T_STEP_TITLE)

        why = MathTex(
            r"\text{Atletë që NUK përdorin barna,}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        why.next_to(q_text, DOWN, buff=0.35).set_x(PX)
        why2 = MathTex(
            r"\text{por testojnë pozitiv:}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        why2.next_to(why, DOWN, buff=0.2).set_x(PX)
        self.play(FadeIn(why), run_time=T_BODY_FADE)
        self.play(FadeIn(why2), run_time=T_BODY_FADE)

        ans = MathTex(
            r"\text{Pozitivë të rremë} = 8",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        ans.next_to(why2, DOWN, buff=0.5).set_x(PX)
        box = make_answer_box(ans)
        self.play(Write(ans), run_time=T_KEY_EQUATION)
        self.play(Create(box), run_time=0.4)
        self.play(
            Circumscribe(VGroup(ans, box), color=HIGHLIGHT_COLOR, run_time=0.8),
        )
        self.wait(W_AFTER_ROUTINE)

        # Commentary: "Alarme të rreme!"
        alarm = MathTex(
            r"\text{Alarme të rreme!}",
            font_size=BODY_SIZE, color=AUX_COLOR,
        )
        alarm.next_to(box, DOWN, buff=0.5).set_x(PX)
        self.play(FadeIn(alarm, shift=UP * 0.2), run_time=T_BODY_FADE)
        self.play(
            Indicate(alarm, color=AUX_COLOR, scale_factor=1.2),
            run_time=0.6,
        )
        self.wait(W_AFTER_ANSWER)

        # Clean right panel
        self.play(
            FadeOut(header), FadeOut(q_text), FadeOut(why), FadeOut(why2),
            FadeOut(ans), FadeOut(box), FadeOut(alarm),
            run_time=T_TRANSITION,
        )
        self.wait(0.3)

    # ────────────────────────────────────────────
    #  PART D — P(correct result)
    # ────────────────────────────────────────────

    def part_d(self):
        header = MathTex(
            r"\text{Pjesa d)}",
            font_size=PART_HEADER_SIZE, color=LABEL_COLOR,
        )
        header.to_corner(UL, buff=0.4)
        self.play(Write(header), run_time=0.5)

        # Highlight the "correct" endpoints: 95 (users+positive) and 392 (non-users+negative)
        self.play(
            Indicate(self.val_95, color=ANSWER_COLOR, scale_factor=1.5),
            Indicate(self.val_392, color=ANSWER_COLOR, scale_factor=1.5),
            run_time=0.8,
        )
        self.play(
            Indicate(self.dot_up, color=ANSWER_COLOR, scale_factor=2),
            Indicate(self.dot_nn, color=ANSWER_COLOR, scale_factor=2),
            run_time=0.6,
        )

        # Right panel title
        d_title = MathTex(
            r"\text{P(rezultat i saktë)}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        d_title.move_to(RIGHT * PX + UP * 3.0)
        self.play(Write(d_title), run_time=T_STEP_TITLE)

        # Explain what "correct" means
        why = MathTex(
            r"\text{Rezultat i saktë:}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        why.next_to(d_title, DOWN, buff=0.3).set_x(PX)
        self.play(FadeIn(why), run_time=T_BODY_FADE)

        explain1 = MathTex(
            r"\text{Përdorin barna} \to \text{pozitiv}",
            font_size=20, color=SHAPE_COLOR,
        )
        explain1.next_to(why, DOWN, buff=0.25).set_x(PX)
        explain2 = MathTex(
            r"\text{OSE}",
            font_size=20, color=BODY_TEXT_COLOR,
        )
        explain2.next_to(explain1, DOWN, buff=0.15).set_x(PX)
        explain3 = MathTex(
            r"\text{Nuk përdorin} \to \text{negativ}",
            font_size=20, color=AUX_COLOR,
        )
        explain3.next_to(explain2, DOWN, buff=0.15).set_x(PX)

        self.play(
            FadeIn(explain1, shift=UP * 0.1),
            run_time=T_BODY_FADE,
        )
        self.play(
            FadeIn(explain2, shift=UP * 0.1),
            FadeIn(explain3, shift=UP * 0.1),
            run_time=T_BODY_FADE,
        )
        self.wait(W_AFTER_ROUTINE)

        # Calculation
        eq1 = MathTex(
            r"\text{Saktë} = 95 + 392 = 487",
            font_size=CALC_SIZE, color=WHITE,
        )
        eq1.next_to(explain3, DOWN, buff=0.35).set_x(PX)
        self.play(Write(eq1), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        # Probability
        eq2 = MathTex(
            r"P(\text{i saktë}) = \frac{487}{500}",
            font_size=CALC_SIZE, color=WHITE,
        )
        eq2.next_to(eq1, DOWN, buff=0.3).set_x(PX)
        self.play(Write(eq2), run_time=T_KEY_EQUATION)
        self.wait(0.8)

        # Final answer
        ans = MathTex(
            r"P(\text{i saktë}) = 0{,}974 = 97{,}4\%",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        ans.next_to(eq2, DOWN, buff=0.4).set_x(PX)
        box = make_answer_box(ans)
        self.play(Write(ans), run_time=T_KEY_EQUATION)
        self.play(Create(box), run_time=0.4)
        self.play(
            Flash(ans.get_center(), color=ANSWER_COLOR, line_length=0.2,
                  num_lines=12, run_time=0.6),
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
                r"\text{a) Diagrami pemë i frekuencave (më lart)}",
                font_size=24, color=ANSWER_COLOR,
            ),
            MathTex(
                r"\text{b) Total pozitiv: } 95 + 8 = 103",
                font_size=24, color=ANSWER_COLOR,
            ),
            MathTex(
                r"\text{c) Pozitivë të rremë: } 8",
                font_size=24, color=ANSWER_COLOR,
            ),
            MathTex(
                r"\text{d) } P(\text{i saktë}) = \frac{487}{500} = 0{,}974",
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
