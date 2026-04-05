"""
Reel B — Ushtrimi 4, Njësia 8.4A
"Sa ditë vonohet Jetmira në 150 ditë pune?"

Standalone reel: builds a frequency tree from 150 work days,
shows 60 car / 90 bus split, then late/on-time counts,
highlights total late = 6 + 18 = 24.
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


class ReelB(Scene):
    def construct(self):
        apply_style(self)
        MathTex.set_default(tex_template=ALBANIAN_TEX)
        Tex.set_default(tex_template=ALBANIAN_TEX)

        self.hook()
        self.frequency_tree()
        self.total_late()
        self.cta()

    # -----------------------------------------------
    #  HOOK (0-8s)
    # -----------------------------------------------

    def hook(self):
        line1 = MathTex(
            r"\text{Jetmira shkon në punë:}",
            font_size=HOOK_SIZE, color=WHITE,
        )
        line2 = MathTex(
            r"\text{Makinë (P=0{,}4), Autobus (P=0{,}6)}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        line3 = MathTex(
            r"\text{Vonohet 10\% me makinë, 20\% me autobus}",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        hook_group = VGroup(line1, line2, line3).arrange(DOWN, buff=0.35)
        hook_group.move_to(UP * 3.0)

        ask = MathTex(
            r"\text{Sa ditë vonohet në 150 ditë pune?}",
            font_size=QUESTION_SIZE, color=HIGHLIGHT_COLOR,
        )
        ask.next_to(hook_group, DOWN, buff=0.7)

        self.play(FadeIn(hook_group, shift=UP * 0.4), run_time=1.2)
        self.wait(2.5)
        self.play(FadeIn(ask, shift=UP * 0.3), run_time=0.8)
        self.wait(2.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # -----------------------------------------------
    #  FREQUENCY TREE (8-35s)
    # -----------------------------------------------

    def frequency_tree(self):
        title = MathTex(
            r"\text{Diagrami i frekuencave:}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        title.move_to(UP * SAFE_TOP)
        self.play(FadeIn(title), run_time=0.5)

        # Root: 150
        root = MathTex(r"150", font_size=EQ_SIZE, color=WHITE)
        root.move_to(UP * 3.2)
        self.play(GrowFromCenter(root), run_time=0.5)

        # Level 1 positions
        car_pos = LEFT * 2.5 + UP * 1.0
        bus_pos = RIGHT * 2.5 + UP * 1.0

        # Lines
        line_car = Line(root.get_bottom(), car_pos + UP * 0.35, buff=0.1,
                        color=SHAPE_COLOR, stroke_width=2.5)
        line_bus = Line(root.get_bottom(), bus_pos + UP * 0.35, buff=0.1,
                        color=AUX_COLOR, stroke_width=2.5)

        # Labels
        car_node = MathTex(r"60", font_size=EQ_SIZE, color=SHAPE_COLOR)
        car_node.move_to(car_pos)
        car_sub = MathTex(r"\text{Makinë}", font_size=SMALL_SIZE, color=SHAPE_COLOR)
        car_sub.next_to(car_node, DOWN, buff=0.15)

        bus_node = MathTex(r"90", font_size=EQ_SIZE, color=AUX_COLOR)
        bus_node.move_to(bus_pos)
        bus_sub = MathTex(r"\text{Autobus}", font_size=SMALL_SIZE, color=AUX_COLOR)
        bus_sub.next_to(bus_node, DOWN, buff=0.15)

        # Calculations
        calc_car = MathTex(r"150 \times 0{,}4 = 60", font_size=SMALL_SIZE, color=SHAPE_COLOR)
        calc_car.move_to(line_car.get_center() + LEFT * 0.1 + UP * 0.35)
        calc_bus = MathTex(r"150 \times 0{,}6 = 90", font_size=SMALL_SIZE, color=AUX_COLOR)
        calc_bus.move_to(line_bus.get_center() + RIGHT * 0.1 + UP * 0.35)

        self.play(Create(line_car), Create(line_bus), run_time=0.6)
        self.play(
            GrowFromCenter(car_node), FadeIn(car_sub),
            GrowFromCenter(bus_node), FadeIn(bus_sub),
            run_time=0.6,
        )
        self.play(FadeIn(calc_car), FadeIn(calc_bus), run_time=0.5)
        self.wait(1.5)

        # Level 2 — car branches
        cl_pos = LEFT * 3.5 + DOWN * 1.5   # car late
        co_pos = LEFT * 1.5 + DOWN * 1.5   # car on-time

        line_cl = Line(car_node.get_bottom() + DOWN * 0.3, cl_pos + UP * 0.35, buff=0.1,
                       color=LABEL_COLOR, stroke_width=2.5)
        line_co = Line(car_node.get_bottom() + DOWN * 0.3, co_pos + UP * 0.35, buff=0.1,
                       color=ANSWER_COLOR, stroke_width=2.5)

        cl_node = MathTex(r"6", font_size=EQ_SIZE, color=LABEL_COLOR)
        cl_node.move_to(cl_pos)
        cl_sub = MathTex(r"\text{Vonë}", font_size=SMALL_SIZE, color=LABEL_COLOR)
        cl_sub.next_to(cl_node, DOWN, buff=0.15)

        co_node = MathTex(r"54", font_size=EQ_SIZE, color=ANSWER_COLOR)
        co_node.move_to(co_pos)
        co_sub = MathTex(r"\text{Në kohë}", font_size=SMALL_SIZE, color=ANSWER_COLOR)
        co_sub.next_to(co_node, DOWN, buff=0.15)

        self.play(Create(line_cl), Create(line_co), run_time=0.6)
        self.play(
            GrowFromCenter(cl_node), FadeIn(cl_sub),
            GrowFromCenter(co_node), FadeIn(co_sub),
            run_time=0.5,
        )
        self.wait(1.0)

        # Level 2 — bus branches
        bl_pos = RIGHT * 1.5 + DOWN * 1.5   # bus late
        bo_pos = RIGHT * 3.5 + DOWN * 1.5   # bus on-time

        line_bl = Line(bus_node.get_bottom() + DOWN * 0.3, bl_pos + UP * 0.35, buff=0.1,
                       color=LABEL_COLOR, stroke_width=2.5)
        line_bo = Line(bus_node.get_bottom() + DOWN * 0.3, bo_pos + UP * 0.35, buff=0.1,
                       color=ANSWER_COLOR, stroke_width=2.5)

        bl_node = MathTex(r"18", font_size=EQ_SIZE, color=LABEL_COLOR)
        bl_node.move_to(bl_pos)
        bl_sub = MathTex(r"\text{Vonë}", font_size=SMALL_SIZE, color=LABEL_COLOR)
        bl_sub.next_to(bl_node, DOWN, buff=0.15)

        bo_node = MathTex(r"72", font_size=EQ_SIZE, color=ANSWER_COLOR)
        bo_node.move_to(bo_pos)
        bo_sub = MathTex(r"\text{Në kohë}", font_size=SMALL_SIZE, color=ANSWER_COLOR)
        bo_sub.next_to(bo_node, DOWN, buff=0.15)

        self.play(Create(line_bl), Create(line_bo), run_time=0.6)
        self.play(
            GrowFromCenter(bl_node), FadeIn(bl_sub),
            GrowFromCenter(bo_node), FadeIn(bo_sub),
            run_time=0.5,
        )
        self.wait(1.5)

        # Highlight the late nodes
        self.play(
            Indicate(cl_node, color=HIGHLIGHT_COLOR, scale_factor=1.3),
            Indicate(bl_node, color=HIGHLIGHT_COLOR, scale_factor=1.3),
            run_time=0.8,
        )
        self.wait(1.0)

        # Store for next section
        self.cl_node = cl_node
        self.bl_node = bl_node

    # -----------------------------------------------
    #  TOTAL LATE (35-45s)
    # -----------------------------------------------

    def total_late(self):
        # Sum equation
        sum_eq = MathTex(
            r"\text{Vonë gjithsej} = 6 + 18 = 24",
            font_size=EQ_SIZE, color=HIGHLIGHT_COLOR,
        )
        sum_eq.move_to(DOWN * 3.2)

        self.play(Write(sum_eq), run_time=1.0)
        self.wait(1.0)

        # Answer
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

        ans_label = MathTex(
            r"\text{Jetmira vonohet:}",
            font_size=BODY_SIZE, color=STEP_TITLE_COLOR,
        )
        ans_label.move_to(UP * 1.5)

        answer = MathTex(
            r"24 \text{ ditë nga 150}",
            font_size=ANSWER_SIZE, color=ANSWER_COLOR,
        )
        answer.next_to(ans_label, DOWN, buff=0.6)
        box = make_answer_box(answer)

        self.play(FadeIn(ans_label), run_time=0.5)
        self.play(Write(answer), run_time=0.8)
        self.play(Create(box), run_time=0.4)
        self.play(
            Flash(answer.get_center(), color=ANSWER_COLOR,
                  line_length=0.2, num_lines=10, run_time=0.5),
        )
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
