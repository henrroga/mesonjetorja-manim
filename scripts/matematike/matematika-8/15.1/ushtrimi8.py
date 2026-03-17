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

BALL_ALBANIAN = {
    "red": "te kuqe",
    "white": "bardhe",
    "black": "zi",
    "purple": "vjollce",
    "blue": "blu",
    "brown": "kafe",
    "green": "gjelber",
    "yellow": "verdhe",
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
    Uses the full visual toolkit: reveal_sequence, animated_counter,
    fraction_bar, highlight_result, morph_equation, flash_point,
    DrawBorderThenFill.
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
    #  BAG SHAPE
    # ================================================================

    def make_bag(self, center=ORIGIN, width=3.6, height=2.8):
        """Create a visual bag shape (rounded rectangle)."""
        bag = RoundedRectangle(
            corner_radius=0.3,
            width=width,
            height=height,
            fill_color="#2A2A2A",
            fill_opacity=0.5,
            stroke_color=DIVIDER_COLOR,
            stroke_width=2,
        )
        bag.move_to(center)
        return bag

    # ================================================================
    #  BALL DIAGRAM BUILDER
    # ================================================================

    def build_ball_diagram(self, center=ORIGIN, scale=1.0):
        """
        Build the full ball diagram: 15 red in a 5x3 grid, 7 others in a row.
        Returns (all_balls_group, red_group, other_balls_group, other_dict,
                 red_label, other_name_labels, other_count, bag).
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
        other_name_labels = VGroup()
        for i, name in enumerate(other_names):
            al_name = BALL_ALBANIAN[name]
            lbl = MathTex(
                r"\text{" + al_name + r"}",
                font_size=14, color=BALL_COLORS[name],
            )
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

        # Bag shape around everything
        bag = self.make_bag(
            center=all_group.get_center(),
            width=all_group.get_width() + 0.6,
            height=all_group.get_height() + 0.5,
        )

        return all_group, red_balls, other_balls, other_dict, red_label, other_name_labels, other_count, bag

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
         red_label, other_name_labels, other_count, bag) = self.build_ball_diagram(
            center=DOWN * 0.2
        )

        # Show bag first with DrawBorderThenFill
        self.play(DrawBorderThenFill(bag), run_time=1.0)
        self.wait(0.5)

        # Reveal red balls one by one using reveal_sequence
        self.reveal_sequence(list(red_balls), lag_ratio=0.04, run_time=2.0)
        self.play(FadeIn(red_label), run_time=0.5)
        self.wait(1)

        # Reveal other balls one by one using reveal_sequence
        self.reveal_sequence(list(other_balls), lag_ratio=0.12, run_time=1.5)
        self.play(FadeIn(other_name_labels), FadeIn(other_count), run_time=0.6)
        self.wait(2)

        # ── Animated counter: count from 0 to 22 ──
        counter_group = self.animated_counter(
            0, 22,
            prefix="Totali: ",
            font_size=36,
            color=LABEL_COLOR,
            position=DOWN * 2.8,
            run_time=2.5,
        )
        self.wait(2)

        # ── Fade balls and counter, show counting equation ──
        self.play(
            FadeOut(all_group), FadeOut(bag), FadeOut(desc1),
            FadeOut(intro_t), FadeOut(counter_group),
            run_time=0.7,
        )
        self.wait(0.5)

        # ── Count total — written form ──
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
        self.highlight_result(count_eq2, color=LABEL_COLOR)
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
    #  HELPER: Setup split layout with balls on left + bag
    # ================================================================

    def setup_ball_split(self):
        """
        Create ball diagram on the left side with bag + divider.
        Returns all references needed to manipulate balls.
        """
        (all_group, red_balls, other_balls, other_dict,
         red_label, other_name_labels, other_count, bag) = self.build_ball_diagram(
            center=LEFT * 3.5 + DOWN * 0.3, scale=0.85,
        )

        div = make_divider()

        # Draw bag first, then reveal balls inside
        self.play(DrawBorderThenFill(bag), run_time=0.8)
        self.play(
            LaggedStart(
                *[DrawBorderThenFill(b) for b in red_balls],
                lag_ratio=0.02,
            ),
            LaggedStart(
                *[DrawBorderThenFill(b) for b in other_balls],
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
                red_label, other_name_labels, other_count, bag, div)

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

        # Setup ball diagram with bag
        (all_group, red_balls, other_balls, other_dict,
         red_label, other_name_labels, other_count, bag, div) = self.setup_ball_split()

        # Flash each red ball using reveal_sequence style + flash_point
        # First dim the non-red balls
        dim_anims = []
        for b in other_balls:
            dim_anims.append(b.animate.set_opacity(0.25))
        dim_anims.append(other_name_labels.animate.set_opacity(0.25))
        dim_anims.append(other_count.animate.set_opacity(0.25))
        self.play(*dim_anims, run_time=0.6)
        self.wait(0.5)

        # Highlight red balls with green glow border one by one (LaggedStart)
        glow_anims = []
        for b in red_balls:
            glow_anims.append(
                b.animate.set_stroke(color=ANSWER_COLOR, width=3)
            )
        self.play(
            LaggedStart(*glow_anims, lag_ratio=0.03),
            run_time=1.2,
        )
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

        # highlight_result instead of just a box
        self.highlight_result(eq1)
        self.wait(1)

        # Fraction bar — show what 15/22 looks like visually
        bar_group, _ = self.fraction_bar(
            15, 22,
            width=3.0, height=0.35,
            color=RED,
            position=np.array([CALC_CENTER[0], eq1.get_bottom()[1] - 0.6, 0]),
            run_time=1.2,
        )
        self.wait(3)

    # ================================================================
    #  PART B — P(not red) = 7/22
    # ================================================================

    def part_b(self):
        header = self.show_part_header("b")

        prob = MathTex(
            r"\text{Gjeni probabilitetin qe topi te mos jete i kuq.}",
            font_size=BODY_SIZE + 2, color=BODY_TEXT_COLOR,
        )
        prob.next_to(header, DOWN, buff=0.3).set_x(0)
        self.play(FadeIn(prob), run_time=0.6)
        self.wait(2)
        self.play(FadeOut(prob), run_time=0.4)

        # Setup ball diagram with bag
        (all_group, red_balls, other_balls, other_dict,
         red_label, other_name_labels, other_count, bag, div) = self.setup_ball_split()

        # Dim red balls first
        dim_anims = []
        for b in red_balls:
            dim_anims.append(b.animate.set_opacity(0.25))
        dim_anims.append(red_label.animate.set_opacity(0.25))
        self.play(*dim_anims, run_time=0.6)
        self.wait(0.5)

        # Highlight other balls one by one with green glow using LaggedStart
        glow_anims = []
        for b in other_balls:
            glow_anims.append(
                b.animate.set_stroke(color=ANSWER_COLOR, width=3)
            )
        self.play(
            LaggedStart(*glow_anims, lag_ratio=0.1),
            other_name_labels.animate.set_color(ANSWER_COLOR),
            run_time=1.0,
        )
        # Flash each favorable ball
        for b in other_balls:
            self.flash_point(b, color=ANSWER_COLOR, radius=0.2)
        self.wait(1)

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

        self.highlight_result(eq2)
        self.wait(1)

        # Fraction bar — show what 7/22 looks like
        bar_group, _ = self.fraction_bar(
            7, 22,
            width=3.0, height=0.35,
            color=SHAPE_COLOR,
            position=np.array([CALC_CENTER[0], eq2.get_bottom()[1] - 0.6, 0]),
            run_time=1.2,
        )
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

        # Setup ball diagram with bag
        (all_group, red_balls, other_balls, other_dict,
         red_label, other_name_labels, other_count, bag, div) = self.setup_ball_split()

        # Highlight ONLY the black ball — dim everything else
        black_ball = other_dict["black"]

        dim_anims = []
        for b in red_balls:
            dim_anims.append(b.animate.set_opacity(0.25))
        for b in other_balls:
            if b is not black_ball:
                dim_anims.append(b.animate.set_opacity(0.25))
        dim_anims.append(red_label.animate.set_opacity(0.25))
        dim_anims.append(other_name_labels.animate.set_opacity(0.25))
        dim_anims.append(other_count.animate.set_opacity(0.25))
        self.play(*dim_anims, run_time=0.6)
        self.wait(0.5)

        # Green glow on the black ball
        self.play(
            black_ball.animate.set_stroke(color=ANSWER_COLOR, width=3),
            run_time=0.5,
        )
        # Flash the black ball
        self.flash_point(black_ball, color=ANSWER_COLOR, radius=0.3)
        self.wait(1)

        # Right panel
        t1 = self.panel_title("Rast i favorshem: 1 top i zi", y_pos=2.8)
        self.wait(1)

        txt1 = self.panel_text([
            r"\text{Topat e zi: } 1",
            r"\text{Topat gjithsej: } 22",
        ], t1)
        self.wait(1.5)

        eq1 = self.panel_eq(
            r"P(\text{i zi}) = \frac{1}{22}",
            txt1, buff=0.4, color=ANSWER_COLOR, font_size=ANSWER_SIZE, key=True,
        )

        self.highlight_result(eq1)
        self.wait(1)

        # Fraction bar — show how tiny 1/22 is
        bar_group, _ = self.fraction_bar(
            1, 22,
            width=3.0, height=0.35,
            color=GRAY_B,
            position=np.array([CALC_CENTER[0], eq1.get_bottom()[1] - 0.6, 0]),
            run_time=1.2,
        )
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

        # Setup ball diagram with bag
        (all_group, red_balls, other_balls, other_dict,
         red_label, other_name_labels, other_count, bag, div) = self.setup_ball_split()

        # Highlight ALL EXCEPT the black ball
        black_ball = other_dict["black"]

        # Dim only the black ball
        self.play(black_ball.animate.set_opacity(0.25), run_time=0.5)
        self.wait(0.5)

        # Green glow on all non-black balls using LaggedStart
        glow_anims = []
        for b in red_balls:
            glow_anims.append(
                b.animate.set_stroke(color=ANSWER_COLOR, width=2.5)
            )
        for b in other_balls:
            if b is not black_ball:
                glow_anims.append(
                    b.animate.set_stroke(color=ANSWER_COLOR, width=2.5)
                )
        self.play(
            LaggedStart(*glow_anims, lag_ratio=0.02),
            run_time=1.0,
        )
        self.wait(1.5)

        # Right panel
        t1 = self.panel_title("Jo i zi = te gjitha PERVEC te ziut", y_pos=2.8)
        self.wait(1.5)

        txt1 = self.panel_text([
            r"\text{Totali: } 22",
            r"\text{Te zi: } 1",
        ], t1)
        self.wait(1.5)

        eq1 = self.panel_eq(
            r"\text{Jo te zi} = 22 - 1 = 21",
            txt1, font_size=CALC_SIZE,
        )
        self.wait(1.5)

        eq2 = self.panel_eq(
            r"P(\text{jo i zi}) = \frac{21}{22}",
            eq1, color=ANSWER_COLOR, font_size=ANSWER_SIZE, key=True,
        )

        self.highlight_result(eq2)
        self.wait(1)

        # Fraction bar — show how nearly full 21/22 is
        bar_group, _ = self.fraction_bar(
            21, 22,
            width=3.0, height=0.35,
            color=ANSWER_COLOR,
            position=np.array([CALC_CENTER[0], eq2.get_bottom()[1] - 0.6, 0]),
            run_time=1.2,
        )
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

        # Setup ball diagram with bag
        (all_group, red_balls, other_balls, other_dict,
         red_label, other_name_labels, other_count, bag, div) = self.setup_ball_split()

        # Highlight white AND black balls — dim everything else
        white_ball = other_dict["white"]
        black_ball = other_dict["black"]

        dim_anims = []
        for b in red_balls:
            dim_anims.append(b.animate.set_opacity(0.25))
        for b in other_balls:
            if b is not white_ball and b is not black_ball:
                dim_anims.append(b.animate.set_opacity(0.25))
        dim_anims.append(red_label.animate.set_opacity(0.25))
        dim_anims.append(other_name_labels.animate.set_opacity(0.25))
        dim_anims.append(other_count.animate.set_opacity(0.25))
        self.play(*dim_anims, run_time=0.6)
        self.wait(0.5)

        # Green glow on white and black balls, one at a time
        self.play(
            white_ball.animate.set_stroke(color=ANSWER_COLOR, width=3),
            run_time=0.5,
        )
        self.flash_point(white_ball, color=ANSWER_COLOR, radius=0.3)

        self.play(
            black_ball.animate.set_stroke(color=ANSWER_COLOR, width=3),
            run_time=0.5,
        )
        self.flash_point(black_ball, color=ANSWER_COLOR, radius=0.3)
        self.wait(1)

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

        # Simplification — morph_equation: 2/22 -> 1/11
        simp_t = self.panel_text([
            r"\text{Thjeshtojme (pjestojme me 2):}",
        ], eq2, buff=0.3)
        self.wait(1.5)

        # Show the morphing simplification
        eq3 = self.panel_eq(
            r"\frac{2}{22}",
            simp_t, font_size=CALC_SIZE + 4,
        )
        self.wait(1)

        eq3_morphed = self.morph_equation(
            eq3,
            r"\frac{1}{11}",
            font_size=CALC_SIZE + 4,
            color=ANSWER_COLOR,
        )
        self.wait(1.5)

        # Final answer
        eq4 = self.panel_eq(
            r"P(\text{i bardhe ose i zi}) = \frac{1}{11}",
            eq3_morphed, color=ANSWER_COLOR, font_size=ANSWER_SIZE, key=True,
        )

        self.highlight_result(eq4)
        self.wait(1)

        # Fraction bar — show what 1/11 looks like
        bar_group, _ = self.fraction_bar(
            1, 11,
            width=3.0, height=0.35,
            color=SHAPE_COLOR,
            position=np.array([CALC_CENTER[0], eq4.get_bottom()[1] - 0.6, 0]),
            run_time=1.2,
        )
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
