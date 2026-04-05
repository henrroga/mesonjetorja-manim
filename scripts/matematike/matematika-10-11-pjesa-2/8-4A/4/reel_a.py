"""
Reel A — Ushtrimi 4, Njësia 8.4A
"Si duket diagrami pemë i probabilitetit?"

Standalone reel: states the Jetmira problem, builds a probability tree
with car/bus branches and late/on-time sub-branches.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))

from manim import *
import numpy as np
from style_guide import (
    apply_style, make_answer_box, BG_COLOR,
    STEP_TITLE_COLOR, BODY_TEXT_COLOR, LABEL_COLOR,
    ANSWER_COLOR, SHAPE_COLOR, AUX_COLOR, HIGHLIGHT_COLOR, DIVIDER_COLOR,
    ALBANIAN_TEX,
)

# -- Vertical 9:16 config --
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 8
config.frame_height = 8 * (1920 / 1080)

# -- Safe zone --
SAFE_TOP = 4.8
SAFE_BOTTOM = -3.3

# -- Font sizes --
HOOK_SIZE = 38
QUESTION_SIZE = 42
EQ_SIZE = 38
ANSWER_SIZE = 42
BODY_SIZE = 32
SMALL_SIZE = 28


class ReelA(Scene):
    def construct(self):
        apply_style(self)
        MathTex.set_default(tex_template=ALBANIAN_TEX)
        Tex.set_default(tex_template=ALBANIAN_TEX)

        self.hook()
        self.build_tree()
        self.cta()

    # -----------------------------------------------
    #  HOOK — state the problem (0-10s)
    # -----------------------------------------------

    def hook(self):
        line1 = MathTex(
            r"\text{Jetmira shkon në punë:}",
            font_size=HOOK_SIZE, color=WHITE,
        )
        line2 = MathTex(
            r"\text{Me makinë 2 ditë/javë}",
            font_size=HOOK_SIZE, color=SHAPE_COLOR,
        )
        line3 = MathTex(
            r"\text{Me autobus 3 ditë/javë}",
            font_size=HOOK_SIZE, color=AUX_COLOR,
        )
        line4 = MathTex(
            r"\text{Vonohet 10\% me makinë,}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        line5 = MathTex(
            r"\text{20\% me autobus.}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        hook_group = VGroup(line1, line2, line3, line4, line5).arrange(DOWN, buff=0.35)
        hook_group.move_to(UP * 2.5)

        ask = MathTex(
            r"\text{Si duket diagrami pemë?}",
            font_size=QUESTION_SIZE, color=HIGHLIGHT_COLOR,
        )
        ask.next_to(hook_group, DOWN, buff=0.7)

        self.play(FadeIn(hook_group, shift=UP * 0.4), run_time=1.2)
        self.wait(3.0)
        self.play(FadeIn(ask, shift=UP * 0.3), run_time=0.8)
        self.wait(2.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # -----------------------------------------------
    #  BUILD TREE (10-40s)
    # -----------------------------------------------

    def build_tree(self):
        title = MathTex(
            r"\text{Diagrami pemë:}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        title.move_to(UP * SAFE_TOP)
        self.play(FadeIn(title), run_time=0.5)

        # Root node
        root = MathTex(r"\text{J}", font_size=BODY_SIZE, color=WHITE)
        root.move_to(UP * 3.5)

        # Level 1 — transport
        car_label = MathTex(r"\text{M}", font_size=BODY_SIZE, color=SHAPE_COLOR)
        bus_label = MathTex(r"\text{A}", font_size=BODY_SIZE, color=AUX_COLOR)
        car_label.move_to(LEFT * 2.5 + UP * 1.2)
        bus_label.move_to(RIGHT * 2.5 + UP * 1.2)

        # Branches root -> level 1
        line_car = Line(root.get_bottom(), car_label.get_top(), buff=0.15,
                        color=SHAPE_COLOR, stroke_width=2.5)
        line_bus = Line(root.get_bottom(), bus_label.get_top(), buff=0.15,
                        color=AUX_COLOR, stroke_width=2.5)

        # Branch probabilities
        p_car = MathTex(r"0{,}4", font_size=SMALL_SIZE, color=SHAPE_COLOR)
        p_car.move_to(line_car.get_center() + LEFT * 0.6)
        p_bus = MathTex(r"0{,}6", font_size=SMALL_SIZE, color=AUX_COLOR)
        p_bus.move_to(line_bus.get_center() + RIGHT * 0.6)

        # Level 2 — late/on-time from car
        car_late = MathTex(r"\text{V}", font_size=BODY_SIZE, color=LABEL_COLOR)
        car_ok = MathTex(r"\text{NK}", font_size=BODY_SIZE, color=ANSWER_COLOR)
        car_late.move_to(LEFT * 3.5 + DOWN * 1.2)
        car_ok.move_to(LEFT * 1.5 + DOWN * 1.2)

        line_cl = Line(car_label.get_bottom(), car_late.get_top(), buff=0.15,
                       color=LABEL_COLOR, stroke_width=2.5)
        line_co = Line(car_label.get_bottom(), car_ok.get_top(), buff=0.15,
                       color=ANSWER_COLOR, stroke_width=2.5)

        p_cl = MathTex(r"0{,}1", font_size=SMALL_SIZE, color=LABEL_COLOR)
        p_cl.move_to(line_cl.get_center() + LEFT * 0.55)
        p_co = MathTex(r"0{,}9", font_size=SMALL_SIZE, color=ANSWER_COLOR)
        p_co.move_to(line_co.get_center() + RIGHT * 0.55)

        # Level 2 — late/on-time from bus
        bus_late = MathTex(r"\text{V}", font_size=BODY_SIZE, color=LABEL_COLOR)
        bus_ok = MathTex(r"\text{NK}", font_size=BODY_SIZE, color=ANSWER_COLOR)
        bus_late.move_to(RIGHT * 1.5 + DOWN * 1.2)
        bus_ok.move_to(RIGHT * 3.5 + DOWN * 1.2)

        line_bl = Line(bus_label.get_bottom(), bus_late.get_top(), buff=0.15,
                       color=LABEL_COLOR, stroke_width=2.5)
        line_bo = Line(bus_label.get_bottom(), bus_ok.get_top(), buff=0.15,
                       color=ANSWER_COLOR, stroke_width=2.5)

        p_bl = MathTex(r"0{,}2", font_size=SMALL_SIZE, color=LABEL_COLOR)
        p_bl.move_to(line_bl.get_center() + LEFT * 0.55)
        p_bo = MathTex(r"0{,}8", font_size=SMALL_SIZE, color=ANSWER_COLOR)
        p_bo.move_to(line_bo.get_center() + RIGHT * 0.55)

        # Animate: root
        self.play(GrowFromCenter(root), run_time=0.5)

        # Level 1 branches
        self.play(
            Create(line_car), Create(line_bus),
            run_time=0.7,
        )
        self.play(
            GrowFromCenter(car_label), GrowFromCenter(bus_label),
            run_time=0.5,
        )
        self.play(
            FadeIn(p_car), FadeIn(p_bus),
            run_time=0.5,
        )
        self.wait(1.0)

        # Level 2 — car side
        self.play(
            Create(line_cl), Create(line_co),
            run_time=0.7,
        )
        self.play(
            GrowFromCenter(car_late), GrowFromCenter(car_ok),
            run_time=0.5,
        )
        self.play(
            FadeIn(p_cl), FadeIn(p_co),
            run_time=0.5,
        )
        self.wait(1.0)

        # Level 2 — bus side
        self.play(
            Create(line_bl), Create(line_bo),
            run_time=0.7,
        )
        self.play(
            GrowFromCenter(bus_late), GrowFromCenter(bus_ok),
            run_time=0.5,
        )
        self.play(
            FadeIn(p_bl), FadeIn(p_bo),
            run_time=0.5,
        )
        self.wait(1.5)

        # Legend
        legend = VGroup(
            MathTex(r"\text{M = Makinë, A = Autobus}", font_size=SMALL_SIZE, color=BODY_TEXT_COLOR),
            MathTex(r"\text{V = Vonë, NK = Në kohë}", font_size=SMALL_SIZE, color=BODY_TEXT_COLOR),
        ).arrange(DOWN, buff=0.25)
        legend.move_to(DOWN * 2.8)

        self.play(FadeIn(legend, shift=UP * 0.2), run_time=0.6)
        self.wait(2.5)

        # Outcome probabilities
        self.play(FadeOut(legend), run_time=0.3)

        outcomes_title = MathTex(
            r"\text{Probabilitetet e degëve:}",
            font_size=SMALL_SIZE, color=STEP_TITLE_COLOR,
        )
        outcomes_title.move_to(DOWN * 2.3)

        o1 = MathTex(r"P(M \cap V) = 0{,}4 \times 0{,}1 = 0{,}04",
                      font_size=SMALL_SIZE, color=LABEL_COLOR)
        o2 = MathTex(r"P(M \cap NK) = 0{,}4 \times 0{,}9 = 0{,}36",
                      font_size=SMALL_SIZE, color=ANSWER_COLOR)
        o3 = MathTex(r"P(A \cap V) = 0{,}6 \times 0{,}2 = 0{,}12",
                      font_size=SMALL_SIZE, color=LABEL_COLOR)
        o4 = MathTex(r"P(A \cap NK) = 0{,}6 \times 0{,}8 = 0{,}48",
                      font_size=SMALL_SIZE, color=ANSWER_COLOR)

        outcomes = VGroup(o1, o2, o3, o4).arrange(DOWN, buff=0.2)
        outcomes.next_to(outcomes_title, DOWN, buff=0.3)

        self.play(FadeIn(outcomes_title), run_time=0.4)
        for o in [o1, o2, o3, o4]:
            self.play(FadeIn(o, shift=UP * 0.15), run_time=0.4)
            self.wait(0.5)

        self.wait(2.5)

    # -----------------------------------------------
    #  CTA
    # -----------------------------------------------

    def cta(self):
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

        handle = MathTex(r"\text{mesonjetorja.com}", font_size=BODY_SIZE, color=WHITE)
        handle.move_to(UP * 0.5)
        tagline = MathTex(
            r"\text{Më shumë ushtrime në faqen tonë!}",
            font_size=SMALL_SIZE, color=BODY_TEXT_COLOR,
        )
        tagline.next_to(handle, DOWN, buff=0.4)

        self.play(GrowFromCenter(handle), FadeIn(tagline, shift=UP * 0.3), run_time=0.8)
        self.wait(1.5)
