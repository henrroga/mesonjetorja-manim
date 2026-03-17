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
    T_STEP_TITLE, T_BODY_FADE, T_KEY_EQUATION, T_ROUTINE_EQUATION,
    T_SHAPE_CREATE, T_LAYOUT_SHIFT, T_TRANSITION,
    W_AFTER_KEY, W_AFTER_ROUTINE, W_AFTER_ANSWER, W_PROBLEM,
    CALC_TOP, CALC_CENTER, PX,
)


# ── Ball color definitions ──
BALL_COLORS = {
    "red": RED,
    "white": WHITE,
    "black": "#555555",
    "purple": PURPLE,
    "blue": BLUE,
    "brown": "#8B4513",
    "green": GREEN,
    "yellow": YELLOW,
}

BALL_STROKE = {
    "red": RED_D,
    "white": GRAY,
    "black": WHITE,
    "purple": PURPLE_D,
    "blue": BLUE_D,
    "brown": "#5C2D0A",
    "green": GREEN_D,
    "yellow": YELLOW_D,
}


def make_ball(color_name, radius=0.18):
    """Create a single colored ball circle."""
    return Circle(
        radius=radius,
        fill_opacity=1,
        fill_color=BALL_COLORS[color_name],
        stroke_color=BALL_STROKE[color_name],
        stroke_width=1.5,
    )


class Ushtrimi8(ExerciseScene):
    """
    Ushtrimi 8 -- Njesia 15.1 -- Matematika 8

    Probability with colored balls in a bag.
    Visual storytelling -- no voiceover.
    """

    exercise_number = 8
    unit = "15.1"
    textbook = "Matematika 8"
    parts = ["a", "b", "c", "d", "e"]

    def construct(self):
        """Override construct to insert intro before parts."""
        from style_guide import apply_style
        apply_style(self)
        self.title_screen()

        # ── Introduction: show bag contents + count + formula ──
        self.intro_balls()
        fade_all(self)
        self.wait(0.5)

        # ── Parts ──
        for part_name in self.parts:
            method = getattr(self, f"part_{part_name}")
            method()
            fade_all(self)
            self.wait(0.5)

        # ── Final summary ──
        self.final_summary()
        self.wait(W_AFTER_ANSWER)

    # ================================================================
    #  BALL DIAGRAM BUILDER
    # ================================================================

    def build_ball_diagram(self, center=ORIGIN, scale=1.0):
        """
        Build the full ball diagram: 15 red in a 5x3 grid, 7 others in a row.
        Returns (all_balls_group, red_group, other_balls_dict, count_labels).

        all_balls_group contains everything (balls + labels).
        other_balls_dict maps color name -> ball mobject.
        """
        r = 0.18 * scale
        gap = 0.44 * scale

        # ── Red balls: 5 columns x 3 rows ──
        red_balls = VGroup()
        for row in range(3):
            for col in range(5):
                b = make_ball("red", radius=r)
                b.move_to(np.array([col * gap, -row * gap, 0]))
                red_balls.add(b)

        # Center the red grid
        red_balls.move_to(ORIGIN)

        # Label "15" above red group
        red_label = MathTex(
            r"\text{15 te kuqe}",
            font_size=20, color=RED,
        )
        red_label.next_to(red_balls, UP, buff=0.2)

        # ── Other balls: single row below ──
        other_names = ["white", "black", "purple", "blue", "brown", "green", "yellow"]
        other_balls = VGroup()
        other_dict = {}
        for i, name in enumerate(other_names):
            b = make_ball(name, radius=r)
            b.move_to(np.array([i * gap, 0, 0]))
            other_balls.add(b)
            other_dict[name] = b

        other_balls.move_to(ORIGIN)
        other_balls.next_to(red_balls, DOWN, buff=0.5)

        # Tiny color labels under each other ball
        other_labels_al = [
            "bardhe", "zi", "vjollce", "blu", "kafe", "gjelber", "verdhe"
        ]
        other_name_labels = VGroup()
        for i, (name, al_name) in enumerate(zip(other_names, other_labels_al)):
            lbl = MathTex(
                r"\text{" + al_name + r"}",
                font_size=14, color=BALL_COLORS[name],
            )
            # White text on dark bg is fine; black label needs special color
            if name == "black":
                lbl.set_color(GRAY_B)
            lbl.next_to(other_dict[name], DOWN, buff=0.12)
            other_name_labels.add(lbl)

        # Count label for others
        other_count = MathTex(
            r"\text{7 te tjera}",
            font_size=20, color=BODY_TEXT_COLOR,
        )
        other_count.next_to(other_name_labels, DOWN, buff=0.2)

        all_group = VGroup(
            red_balls, red_label,
            other_balls, other_name_labels, other_count,
        )
        all_group.move_to(center)

        return all_group, red_balls, other_balls, other_dict, red_label, other_name_labels, other_count

    # ================================================================
    #  INTRO: Show bag contents, count, probability formula
    # ================================================================

    def intro_balls(self):
        # ── Title ──
        intro_t = MathTex(
            r"\text{Te dhenat e ushtrimit:}",
            font_size=STEP_TITLE_SIZE + 6, color=STEP_TITLE_COLOR,
        )
        intro_t.to_edge(UP, buff=0.5)
        self.play(FadeIn(intro_t), run_time=0.8)
        self.wait(1)

        # ── Problem description ──
        desc1 = MathTex(
            r"\text{Nje qese permban topa me ngjyra:}",
            font_size=BODY_SIZE + 2, color=BODY_TEXT_COLOR,
        )
        desc1.next_to(intro_t, DOWN, buff=0.4)
        self.play(FadeIn(desc1), run_time=0.6)
        self.wait(1.5)

        # ── Build ball diagram centered ──
        (all_group, red_balls, other_balls, other_dict,
         red_label, other_name_labels, other_count) = self.build_ball_diagram(
            center=DOWN * 0.2
        )

        # Animate balls appearing
        self.play(
            LaggedStart(
                *[FadeIn(b, scale=0.5) for b in red_balls],
                lag_ratio=0.03,
            ),
            FadeIn(red_label),
            run_time=1.5,
        )
        self.wait(1)

        self.play(
            LaggedStart(
                *[FadeIn(b, scale=0.5) for b in other_balls],
                lag_ratio=0.08,
            ),
            FadeIn(other_name_labels),
            FadeIn(other_count),
            run_time=1.2,
        )
        self.wait(2)

        # ── Fade balls, show counting ──
        self.play(
            FadeOut(all_group), FadeOut(desc1), FadeOut(intro_t),
            run_time=0.7,
        )
        self.wait(0.5)

        # ── Count total ──
        count_t = MathTex(
            r"\text{Sa topa ka gjithsej?}",
            font_size=STEP_TITLE_SIZE + 4, color=STEP_TITLE_COLOR,
        )
        count_t.move_to(UP * 2.5)
        self.play(FadeIn(count_t), run_time=0.6)
        self.wait(1.5)

        count_eq1 = MathTex(
            r"\text{Totali} = 15 + 1 + 1 + 1 + 1 + 1 + 1 + 1",
            font_size=CALC_SIZE, color=WHITE,
        )
        count_eq1.next_to(count_t, DOWN, buff=0.5)
        self.play(Write(count_eq1), run_time=1.2)
        self.wait(2)

        count_eq2 = MathTex(
            r"\text{Totali} = 22",
            font_size=CALC_SIZE + 4, color=LABEL_COLOR,
        )
        count_eq2.next_to(count_eq1, DOWN, buff=0.4)
        self.play(Write(count_eq2), run_time=T_KEY_EQUATION)
        self.wait(2)

        # ── Probability formula ──
        formula_t = MathTex(
            r"\text{Formula e probabilitetit:}",
            font_size=STEP_TITLE_SIZE, color=STEP_TITLE_COLOR,
        )
        formula_t.next_to(count_eq2, DOWN, buff=0.6)
        self.play(FadeIn(formula_t), run_time=0.5)
        self.wait(1)

        formula_eq = MathTex(
            r"P = \frac{\text{rastet e favorshme}}{\text{rastet e mundshme}}",
            font_size=CALC_SIZE + 2, color=WHITE,
        )
        formula_eq.next_to(formula_t, DOWN, buff=0.4)
        self.play(Write(formula_eq), run_time=1.2)
        self.wait(3)

    # ================================================================
    #  HELPER: Setup split layout with balls on left
    # ================================================================

    def setup_ball_split(self):
        """
        Create ball diagram on the left side with divider.
        Returns all references needed to manipulate balls.
        """
        (all_group, red_balls, other_balls, other_dict,
         red_label, other_name_labels, other_count) = self.build_ball_diagram(
            center=LEFT * 3.5 + DOWN * 0.3, scale=0.85,
        )

        div = make_divider()

        self.play(
            LaggedStart(
                *[FadeIn(b, scale=0.5) for b in red_balls],
                lag_ratio=0.02,
            ),
            LaggedStart(
                *[FadeIn(b, scale=0.5) for b in other_balls],
                lag_ratio=0.05,
            ),
            FadeIn(red_label),
            FadeIn(other_name_labels),
            FadeIn(other_count),
            FadeIn(div),
            run_time=1.2,
        )
        self.wait(1)

        return (all_group, red_balls, other_balls, other_dict,
                red_label, other_name_labels, other_count, div)

    def highlight_balls(self, favorable, unfavorable):
        """Highlight favorable balls, dim unfavorable ones."""
        anims = []
        for b in favorable:
            anims.append(b.animate.scale(1.25).set_stroke(color=ANSWER_COLOR, width=3))
        for b in unfavorable:
            anims.append(b.animate.set_opacity(0.25))
        self.play(*anims, run_time=0.8)

    def reset_balls(self, all_balls, scale_back=True):
        """Reset all balls to normal appearance."""
        anims = []
        for b in all_balls:
            anims.append(b.animate.set_opacity(1))
            if scale_back:
                # Reset scale by restoring to original
                pass
        self.play(*anims, run_time=0.5)

    # ================================================================
    #  PART A — P(red) = 15/22
    # ================================================================

    def part_a(self):
        header = self.show_part_header("a")

        # Problem statement
        prob = MathTex(
            r"\text{Gjeni probabilitetin qe topi te jete i kuq.}",
            font_size=BODY_SIZE + 4, color=BODY_TEXT_COLOR,
        )
        prob.next_to(header, DOWN, buff=0.3).set_x(0)
        self.play(FadeIn(prob), run_time=0.6)
        self.wait(2)
        self.play(FadeOut(prob), run_time=0.4)

        # Setup ball diagram
        (all_group, red_balls, other_balls, other_dict,
         red_label, other_name_labels, other_count, div) = self.setup_ball_split()

        # Highlight red balls, dim others
        highlight_anims = []
        for b in red_balls:
            highlight_anims.append(
                b.animate.scale(1.2).set_stroke(color=ANSWER_COLOR, width=3)
            )
        dim_anims = []
        for b in other_balls:
            dim_anims.append(b.animate.set_opacity(0.25))
        dim_anims.append(other_name_labels.animate.set_opacity(0.25))
        dim_anims.append(other_count.animate.set_opacity(0.25))

        self.play(*highlight_anims, *dim_anims, run_time=0.8)
        self.wait(1.5)

        # Right panel calculation
        t1 = self.panel_title("Rastet e favorshme:", y_pos=2.8)

        txt1 = self.panel_text([
            r"\text{Topat e kuq: } 15",
        ], t1)
        self.wait(1.5)

        txt2 = self.panel_text([
            r"\text{Topat gjithsej: } 22",
        ], txt1)
        self.wait(1.5)

        eq1 = self.panel_eq(
            r"P(\text{i kuq}) = \frac{15}{22}",
            txt2, color=ANSWER_COLOR, font_size=ANSWER_SIZE, key=True,
        )

        box = make_answer_box(eq1)
        self.play(Create(box), run_time=0.5)
        self.wait(3)

    # ================================================================
    #  PART B — P(not red) = 7/22
    # ================================================================

    def part_b(self):
        header = self.show_part_header("b")

        # Problem statement
        prob = MathTex(
            r"\text{Gjeni probabilitetin qe topi te mos jete i kuq.}",
            font_size=BODY_SIZE + 2, color=BODY_TEXT_COLOR,
        )
        prob.next_to(header, DOWN, buff=0.3).set_x(0)
        self.play(FadeIn(prob), run_time=0.6)
        self.wait(2)
        self.play(FadeOut(prob), run_time=0.4)

        # Setup ball diagram
        (all_group, red_balls, other_balls, other_dict,
         red_label, other_name_labels, other_count, div) = self.setup_ball_split()

        # Highlight OTHER balls, dim red
        highlight_anims = []
        for b in other_balls:
            highlight_anims.append(
                b.animate.scale(1.25).set_stroke(color=ANSWER_COLOR, width=3)
            )
        highlight_anims.append(other_name_labels.animate.set_color(ANSWER_COLOR))

        dim_anims = []
        for b in red_balls:
            dim_anims.append(b.animate.set_opacity(0.25))
        dim_anims.append(red_label.animate.set_opacity(0.25))

        self.play(*highlight_anims, *dim_anims, run_time=0.8)
        self.wait(1.5)

        # Right panel
        t1 = self.panel_title("Jo i kuq = te gjitha PERVEC te kuqve", y_pos=2.8)
        self.wait(2)

        txt1 = self.panel_text([
            r"\text{Totali: } 22",
            r"\text{Te kuqe: } 15",
        ], t1)
        self.wait(1.5)

        eq1 = self.panel_eq(
            r"\text{Jo te kuqe} = 22 - 15 = 7",
            txt1, font_size=CALC_SIZE,
        )
        self.wait(1.5)

        eq2 = self.panel_eq(
            r"P(\text{jo i kuq}) = \frac{7}{22}",
            eq1, color=ANSWER_COLOR, font_size=ANSWER_SIZE, key=True,
        )

        box = make_answer_box(eq2)
        self.play(Create(box), run_time=0.5)
        self.wait(3)

    # ================================================================
    #  PART C — P(black) = 1/22
    # ================================================================

    def part_c(self):
        header = self.show_part_header("c")

        prob = MathTex(
            r"\text{Gjeni probabilitetin qe topi te jete i zi.}",
            font_size=BODY_SIZE + 4, color=BODY_TEXT_COLOR,
        )
        prob.next_to(header, DOWN, buff=0.3).set_x(0)
        self.play(FadeIn(prob), run_time=0.6)
        self.wait(1.5)
        self.play(FadeOut(prob), run_time=0.4)

        # Setup ball diagram
        (all_group, red_balls, other_balls, other_dict,
         red_label, other_name_labels, other_count, div) = self.setup_ball_split()

        # Highlight ONLY the black ball
        black_ball = other_dict["black"]
        highlight_anims = [
            black_ball.animate.scale(1.4).set_stroke(color=ANSWER_COLOR, width=3),
        ]
        dim_anims = []
        for b in red_balls:
            dim_anims.append(b.animate.set_opacity(0.25))
        for b in other_balls:
            if b is not black_ball:
                dim_anims.append(b.animate.set_opacity(0.25))
        dim_anims.append(red_label.animate.set_opacity(0.25))
        dim_anims.append(other_name_labels.animate.set_opacity(0.25))
        dim_anims.append(other_count.animate.set_opacity(0.25))

        self.play(*highlight_anims, *dim_anims, run_time=0.8)
        self.wait(1.5)

        # Right panel
        t1 = self.panel_title("Rast i favorshem: 1 top i zi", y_pos=2.8)
        self.wait(1)

        eq1 = self.panel_eq(
            r"P(\text{i zi}) = \frac{1}{22}",
            t1, buff=0.5, color=ANSWER_COLOR, font_size=ANSWER_SIZE, key=True,
        )

        box = make_answer_box(eq1)
        self.play(Create(box), run_time=0.5)
        self.wait(2.5)

    # ================================================================
    #  PART D — P(not black) = 21/22
    # ================================================================

    def part_d(self):
        header = self.show_part_header("d")

        prob = MathTex(
            r"\text{Gjeni probabilitetin qe topi te mos jete i zi.}",
            font_size=BODY_SIZE + 2, color=BODY_TEXT_COLOR,
        )
        prob.next_to(header, DOWN, buff=0.3).set_x(0)
        self.play(FadeIn(prob), run_time=0.6)
        self.wait(1.5)
        self.play(FadeOut(prob), run_time=0.4)

        # Setup ball diagram
        (all_group, red_balls, other_balls, other_dict,
         red_label, other_name_labels, other_count, div) = self.setup_ball_split()

        # Highlight ALL EXCEPT the black ball
        black_ball = other_dict["black"]
        highlight_anims = []
        for b in red_balls:
            highlight_anims.append(
                b.animate.set_stroke(color=ANSWER_COLOR, width=2.5)
            )
        for b in other_balls:
            if b is not black_ball:
                highlight_anims.append(
                    b.animate.scale(1.15).set_stroke(color=ANSWER_COLOR, width=2.5)
                )

        dim_anims = [
            black_ball.animate.set_opacity(0.25),
        ]

        self.play(*highlight_anims, *dim_anims, run_time=0.8)
        self.wait(1.5)

        # Right panel
        t1 = self.panel_title("Jo i zi = te gjitha PERVEC te ziut", y_pos=2.8)
        self.wait(1.5)

        eq1 = self.panel_eq(
            r"\text{Jo te zi} = 22 - 1 = 21",
            t1, buff=0.5, font_size=CALC_SIZE,
        )
        self.wait(1)

        eq2 = self.panel_eq(
            r"P(\text{jo i zi}) = \frac{21}{22}",
            eq1, color=ANSWER_COLOR, font_size=ANSWER_SIZE, key=True,
        )

        box = make_answer_box(eq2)
        self.play(Create(box), run_time=0.5)
        self.wait(2.5)

    # ================================================================
    #  PART E — P(white or black) = 2/22 = 1/11
    # ================================================================

    def part_e(self):
        header = self.show_part_header("e")

        prob = MathTex(
            r"\text{Gjeni probabilitetin: i bardhe OSE i zi.}",
            font_size=BODY_SIZE + 4, color=BODY_TEXT_COLOR,
        )
        prob.next_to(header, DOWN, buff=0.3).set_x(0)
        self.play(FadeIn(prob), run_time=0.6)
        self.wait(2)
        self.play(FadeOut(prob), run_time=0.4)

        # Setup ball diagram
        (all_group, red_balls, other_balls, other_dict,
         red_label, other_name_labels, other_count, div) = self.setup_ball_split()

        # Highlight white AND black balls
        white_ball = other_dict["white"]
        black_ball = other_dict["black"]
        highlight_anims = [
            white_ball.animate.scale(1.4).set_stroke(color=ANSWER_COLOR, width=3),
            black_ball.animate.scale(1.4).set_stroke(color=ANSWER_COLOR, width=3),
        ]
        dim_anims = []
        for b in red_balls:
            dim_anims.append(b.animate.set_opacity(0.25))
        for b in other_balls:
            if b is not white_ball and b is not black_ball:
                dim_anims.append(b.animate.set_opacity(0.25))
        dim_anims.append(red_label.animate.set_opacity(0.25))
        dim_anims.append(other_name_labels.animate.set_opacity(0.25))
        dim_anims.append(other_count.animate.set_opacity(0.25))

        self.play(*highlight_anims, *dim_anims, run_time=0.8)
        self.wait(1.5)

        # Right panel — explain "or"
        t1 = self.panel_title("'OSE' = mbledhim rastet", y_pos=2.8)
        self.wait(2)

        txt1 = self.panel_text([
            r"\text{I bardhe: 1 top}",
            r"\text{I zi: 1 top}",
        ], t1)
        self.wait(1.5)

        eq1 = self.panel_eq(
            r"\text{Favorshme} = 1 + 1 = 2",
            txt1, font_size=CALC_SIZE,
        )
        self.wait(1.5)

        eq2 = self.panel_eq(
            r"P = \frac{2}{22}",
            eq1, font_size=CALC_SIZE + 2,
        )
        self.wait(1.5)

        # Simplification
        simp_t = self.panel_text([
            r"\text{Thjeshtojme (pjestojme me 2):}",
        ], eq2, buff=0.3)
        self.wait(1.5)

        eq3 = self.panel_eq(
            r"\frac{2}{22} = \frac{2 \div 2}{22 \div 2} = \frac{1}{11}",
            simp_t, font_size=CALC_SIZE + 2,
        )
        self.wait(2)

        eq4 = self.panel_eq(
            r"P(\text{i bardhe ose i zi}) = \frac{1}{11}",
            eq3, color=ANSWER_COLOR, font_size=ANSWER_SIZE, key=True,
        )

        box = make_answer_box(eq4)
        self.play(Create(box), run_time=0.5)
        self.wait(3)

    # ================================================================
    #  FINAL SUMMARY
    # ================================================================

    def final_summary(self):
        self.show_summary_table(
            "Permbledhje",
            [
                r"\text{a) } P(\text{i kuq}) = \frac{15}{22}",
                r"\text{b) } P(\text{jo i kuq}) = \frac{7}{22}",
                r"\text{c) } P(\text{i zi}) = \frac{1}{22}",
                r"\text{d) } P(\text{jo i zi}) = \frac{21}{22}",
                r"\text{e) } P(\text{i bardhe ose i zi}) = \frac{1}{11}",
            ],
            font_size=30,
        )
