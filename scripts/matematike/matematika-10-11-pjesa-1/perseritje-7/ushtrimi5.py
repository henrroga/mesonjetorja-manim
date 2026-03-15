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
    T_ROUTINE_EQUATION, T_SHAPE_CREATE, T_LAYOUT_SHIFT, T_TRANSITION,
    W_AFTER_KEY, W_AFTER_ROUTINE, W_AFTER_ANSWER, W_PROBLEM,
    CALC_TOP, CALC_CENTER,
)

# Dilation helper: P' = Q + k*(P - Q)
def dilate_point(p, center, k):
    """Apply dilation with given center and scale factor k to point p."""
    p = np.array(p)
    c = np.array(center)
    return c + k * (p - c)


class Ushtrimi5(ExerciseScene):
    """
    Ushtrimi 5 — Përsëritje 7
    Matematika 10 - 11: Pjesa I

    Zmadhime (dilation) — ndërtimi i figurave B, C dhe përshkrimi A→D.
    """

    exercise_number = 5
    unit = "Përsëritje 7"
    textbook = "Matematika 10 - 11: Pjesa I"
    parts = ["a", "b", "c"]

    # Rectangle A vertices (counter-clockwise from bottom-left)
    A_VERTS = [(2, 4), (10, 4), (10, 8), (2, 8)]
    # Rectangle D vertices (read from graph in solution)
    D_VERTS = [(-4, 5), (0, 5), (0, 7), (-4, 7)]

    def _make_grid_axes(self, x_range, y_range, scale=0.4):
        """Create a coordinate grid scaled to fit the scene."""
        axes = Axes(
            x_range=x_range,
            y_range=y_range,
            x_length=(x_range[1] - x_range[0]) * scale,
            y_length=(y_range[1] - y_range[0]) * scale,
            axis_config={
                "include_tip": True,
                "include_numbers": True,
                "font_size": 14,
                "color": DIVIDER_COLOR,
                "numbers_to_exclude": [],
            },
            tips=True,
        )
        return axes

    def _make_rect(self, axes, verts, color, label_tex=None, label_dir=UR,
                    fill_opacity=0.25):
        """Draw a rectangle on axes from 4 vertex coordinates."""
        corners = [axes.c2p(v[0], v[1]) for v in verts]
        rect = Polygon(*corners, color=color, fill_color=color,
                        fill_opacity=fill_opacity, stroke_width=2.5)

        lbl = None
        if label_tex:
            center = sum(np.array(c) for c in corners) / 4
            lbl = MathTex(label_tex, font_size=28, color=color)
            lbl.next_to(center, label_dir, buff=0.15)

        return rect, lbl

    def _show_dilation_calc(self, point, center, k, result, label=""):
        """Show one dilation calculation as equation chain."""
        px, py = point
        cx, cy = center
        rx, ry = result
        k_str = str(k).replace(".", "{,}")
        rx_str = str(rx).replace(".", "{,}").replace("-", "-")
        ry_str = str(ry).replace(".", "{,}").replace("-", "-")

        return [
            {"tex": rf"\text{{Për }}({px},\,{py}):", "font_size": BODY_SIZE + 2,
             "color": BODY_TEXT_COLOR},
            {"tex": rf"x' = {cx} + {k_str}({px} - {cx}) = {rx_str}",
             "font_size": CALC_SIZE - 2},
            {"tex": rf"y' = {cy} + {k_str}({py} - {cy}) = {ry_str}",
             "font_size": CALC_SIZE - 2},
            {"tex": rf"\rightarrow ({rx_str},\,{ry_str})",
             "color": ANSWER_COLOR, "key": True},
        ]

    # ================================================================
    #  PART A — Dilation from (6,0), k=0.25 → Figure B
    # ================================================================
    def part_a(self):
        self.show_part_header("a")

        # Problem statement
        self.show_problem(
            Text("Ndërtoni zmadhimin me qendër (6, 0)", font_size=BODY_SIZE + 2, color=WHITE),
            Text("dhe koeficient 0,25 të figurës A.", font_size=BODY_SIZE + 2, color=WHITE),
            Text("Etiketojeni atë me B.", font_size=BODY_SIZE, color=LABEL_COLOR),
        )

        # --- STEP 1: Show the grid with rectangle A ---
        s1 = self.show_step_title("Hapi 1: Identifikojmë figurën A dhe qendrën")

        axes = self._make_grid_axes([-2, 12, 2], [-1, 10, 2], scale=0.45)
        axes.move_to(LEFT * 3 + DOWN * 0.5)
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")

        rect_a, lbl_a = self._make_rect(axes, self.A_VERTS, SHAPE_COLOR,
                                          label_tex="A", label_dir=UP)

        # Mark center of dilation
        center_dot = Dot(axes.c2p(6, 0), color=HIGHLIGHT_COLOR, radius=0.1)
        center_lbl = MathTex("Q(6,\\,0)", font_size=20, color=HIGHLIGHT_COLOR)
        center_lbl.next_to(center_dot, DOWN, buff=0.15)

        self.play(Create(axes), FadeIn(axes_labels), run_time=T_SHAPE_CREATE)
        self.play(Create(rect_a), FadeIn(lbl_a), run_time=T_SHAPE_CREATE)
        self.play(FadeIn(center_dot), FadeIn(center_lbl), run_time=0.6)
        self.wait(W_AFTER_KEY)

        # Divider
        div = make_divider()
        self.play(FadeIn(div), run_time=0.2)

        # --- STEP 2: Explain the formula ---
        s2 = self.show_step_title("Hapi 2: Formula e zmadhimit")

        s2_txt = Text(
            "Për çdo pikë P(x,y), imazhi P'(x',y')\nllogaritet me formulën:",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR, line_spacing=1.4,
        )
        s2_txt.next_to(s2, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(FadeIn(s2_txt), run_time=T_BODY_FADE)

        formula = VGroup(
            MathTex(r"x' = x_Q + k(x - x_Q)", font_size=CALC_SIZE, color=LABEL_COLOR),
            MathTex(r"y' = y_Q + k(y - y_Q)", font_size=CALC_SIZE, color=LABEL_COLOR),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        formula.next_to(s2_txt, DOWN, buff=0.3)
        self.play(Write(formula), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_KEY)

        s2b_txt = Text(
            "ku Q(6,0) dhe k = 0,25",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        s2b_txt.next_to(formula, DOWN, buff=0.2)
        self.play(FadeIn(s2b_txt), run_time=T_BODY_FADE)
        self.wait(W_AFTER_ROUTINE)

        # --- STEP 3: Calculate one vertex in detail ---
        self.play(FadeOut(VGroup(s1, s2, s2_txt, formula, s2b_txt)), run_time=T_TRANSITION)
        self.wait(0.3)

        s3 = self.show_step_title("Hapi 3: Llogaritim kulmet e B")

        # Show first vertex calculation in detail
        eqs = self.show_equation_chain([
            {"tex": r"\text{Për }(2,\,4):", "font_size": BODY_SIZE + 2, "color": BODY_TEXT_COLOR},
            r"x' = 6 + 0{,}25(2 - 6) = 6 + 0{,}25(-4) = 5",
            r"y' = 0 + 0{,}25(4 - 0) = 1",
            {"tex": r"\rightarrow (5,\,1)", "color": ANSWER_COLOR, "key": True},
        ], start_reference=s3)

        # Show remaining vertices more concisely
        remaining = MathTex(
            r"(10,4) \rightarrow (7,1) \quad (2,8) \rightarrow (5,2) \quad (10,8) \rightarrow (7,2)",
            font_size=CALC_SIZE - 4, color=ANSWER_COLOR,
        )
        remaining.next_to(eqs[-1], DOWN, buff=0.4)
        self.play(Write(remaining), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_ROUTINE)

        # --- STEP 4: Animate the dilation on the graph ---
        self.play(FadeOut(VGroup(s3, *eqs, remaining, div)), run_time=T_TRANSITION)
        self.wait(0.3)

        # Calculate B vertices
        Q = (6, 0)
        k = 0.25
        B_verts = [tuple(dilate_point(v, Q, k)) for v in self.A_VERTS]

        rect_b, lbl_b = self._make_rect(axes, B_verts, ANSWER_COLOR,
                                          label_tex="B", label_dir=DOWN)

        # Draw dilation lines from center to each vertex
        dilation_lines = VGroup()
        for av, bv in zip(self.A_VERTS, B_verts):
            line = DashedLine(
                axes.c2p(Q[0], Q[1]), axes.c2p(av[0], av[1]),
                color=DIVIDER_COLOR, dash_length=0.06, stroke_width=1.5,
            )
            dilation_lines.add(line)

        self.play(Create(dilation_lines), run_time=T_SHAPE_CREATE)
        self.play(Create(rect_b), FadeIn(lbl_b), run_time=T_SHAPE_CREATE)
        self.wait(W_AFTER_ANSWER)

    # ================================================================
    #  PART B — Dilation from origin, k=-1.5 → Figure C
    # ================================================================
    def part_b(self):
        self.show_part_header("b")

        self.show_problem(
            Text("Ndërtoni zmadhimin me qendër në origjinë", font_size=BODY_SIZE + 2, color=WHITE),
            Text("dhe koeficient −1,5 të figurës A.", font_size=BODY_SIZE + 2, color=WHITE),
            Text("Etiketojeni atë me C.", font_size=BODY_SIZE, color=LABEL_COLOR),
        )

        # --- Explain negative scale factor ---
        s1 = self.show_step_title("Hapi 1: Çfarë do të thotë k negativ?")

        s1_txt = Text(
            "Kur koeficienti k është negativ, imazhi\njo vetëm zmadhohet/zvogëlohet, por\nedhe kthehet (rrotullohet 180°)\nrreth qendrës së zmadhimit.",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR, line_spacing=1.4,
        )
        s1_txt.next_to(s1, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(FadeIn(s1_txt), run_time=T_BODY_FADE)
        self.wait(W_AFTER_KEY)

        # Simplified formula for origin center
        s1b = Text(
            "Kur qendra është origjina (0,0),\nformula thjeshtohet:",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR, line_spacing=1.4,
        )
        s1b.next_to(s1_txt, DOWN, buff=0.3)
        self.play(FadeIn(s1b), run_time=T_BODY_FADE)

        formula = MathTex(r"x' = kx \qquad y' = ky", font_size=CALC_SIZE + 2, color=LABEL_COLOR)
        formula.next_to(s1b, DOWN, buff=0.25)
        self.play(Write(formula), run_time=T_KEY_EQUATION)
        self.wait(W_AFTER_KEY)

        self.play(FadeOut(VGroup(s1, s1_txt, s1b, formula)), run_time=T_TRANSITION)
        self.wait(0.3)

        # --- Calculate vertices ---
        s2 = self.show_step_title("Hapi 2: Llogaritim kulmet e C")

        eqs = self.show_equation_chain([
            {"tex": r"\text{Me } k = -1{,}5:", "font_size": BODY_SIZE + 2, "color": BODY_TEXT_COLOR},
            r"(2,4) \rightarrow (-1{,}5 \cdot 2,\; -1{,}5 \cdot 4) = (-3,\,-6)",
            r"(10,4) \rightarrow (-15,\,-6)",
            r"(2,8) \rightarrow (-3,\,-12)",
            {"tex": r"(10,8) \rightarrow (-15,\,-12)", "color": ANSWER_COLOR, "key": True},
        ], start_reference=s2)

        self.wait(W_AFTER_ROUTINE)
        self.play(FadeOut(VGroup(s2, *eqs)), run_time=T_TRANSITION)
        self.wait(0.3)

        # --- Show on larger grid ---
        s3 = self.show_step_title("Hapi 3: Vizatojmë figurën C", position=UP * 3.3)

        axes = self._make_grid_axes([-16, 12, 4], [-14, 10, 4], scale=0.28)
        axes.move_to(DOWN * 0.3)
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")

        rect_a, lbl_a = self._make_rect(axes, self.A_VERTS, SHAPE_COLOR,
                                          label_tex="A")

        Q = (0, 0)
        k = -1.5
        C_verts = [tuple(dilate_point(v, Q, k)) for v in self.A_VERTS]
        rect_c, lbl_c = self._make_rect(axes, C_verts, AUX_COLOR,
                                          label_tex="C", label_dir=DOWN)

        # Origin dot
        origin_dot = Dot(axes.c2p(0, 0), color=HIGHLIGHT_COLOR, radius=0.08)
        origin_lbl = MathTex("O", font_size=18, color=HIGHLIGHT_COLOR)
        origin_lbl.next_to(origin_dot, DL, buff=0.08)

        self.play(Create(axes), FadeIn(axes_labels), run_time=T_SHAPE_CREATE)
        self.play(Create(rect_a), FadeIn(lbl_a), run_time=T_SHAPE_CREATE)
        self.play(FadeIn(origin_dot), FadeIn(origin_lbl), run_time=0.4)
        self.wait(W_AFTER_ROUTINE)

        # Dilation lines through origin
        dilation_lines = VGroup()
        for av, cv in zip(self.A_VERTS, C_verts):
            line = DashedLine(
                axes.c2p(av[0], av[1]), axes.c2p(cv[0], cv[1]),
                color=DIVIDER_COLOR, dash_length=0.06, stroke_width=1,
            )
            dilation_lines.add(line)

        self.play(Create(dilation_lines), run_time=T_SHAPE_CREATE)
        self.play(Create(rect_c), FadeIn(lbl_c), run_time=T_SHAPE_CREATE)

        # Note about 180° rotation
        note = Text(
            "Vini re: C është e kthyer (rrotulluar 180°)\ndhe 1,5x më e madhe se A.",
            font_size=BODY_SIZE - 2, color=STEP_TITLE_COLOR, line_spacing=1.4,
        )
        note.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(note), run_time=T_BODY_FADE)
        self.wait(W_AFTER_ANSWER)

    # ================================================================
    #  PART C — Describe transformation A → D
    # ================================================================
    def part_c(self):
        self.show_part_header("c")

        self.show_problem(
            Text("Përshkruani shndërrimin që çon A në D.", font_size=BODY_SIZE + 2, color=WHITE),
        )

        # --- Step 1: Show both figures ---
        s1 = self.show_step_title("Hapi 1: Krahasojmë figurat A dhe D")

        axes = self._make_grid_axes([-6, 12, 2], [-1, 10, 2], scale=0.42)
        axes.move_to(LEFT * 2.5 + DOWN * 0.3)
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")

        rect_a, lbl_a = self._make_rect(axes, self.A_VERTS, SHAPE_COLOR,
                                          label_tex="A")
        rect_d, lbl_d = self._make_rect(axes, self.D_VERTS, HIGHLIGHT_COLOR,
                                          label_tex="D", label_dir=LEFT)

        self.play(Create(axes), FadeIn(axes_labels), run_time=T_SHAPE_CREATE)
        self.play(Create(rect_a), FadeIn(lbl_a), run_time=T_SHAPE_CREATE)
        self.play(Create(rect_d), FadeIn(lbl_d), run_time=T_SHAPE_CREATE)
        self.wait(W_AFTER_KEY)

        # --- Step 2: Find scale factor ---
        div = make_divider()
        self.play(FadeIn(div), run_time=0.2)

        s2 = self.show_step_title("Hapi 2: Gjejmë koeficientin")

        s2_txt = Text(
            "Krahasojmë dimensionet:",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,
        )
        s2_txt.next_to(s2, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(FadeIn(s2_txt), run_time=T_BODY_FADE)

        eqs2 = self.show_equation_chain([
            r"\text{Gjatësia e A} = 10 - 2 = 8",
            r"\text{Gjatësia e D} = 0 - (-4) = 4",
            {"tex": r"k = \frac{4}{8} = 0{,}5", "color": ANSWER_COLOR, "key": True},
        ], start_reference=s2_txt)

        s2b = Text(
            "Lartësia konfirmon: 4/2 = (8-4)/(7-5)",
            font_size=BODY_SIZE - 2, color=BODY_TEXT_COLOR,
        )
        s2b.next_to(eqs2[-1], DOWN, buff=0.2)
        self.play(FadeIn(s2b), run_time=T_BODY_FADE)
        self.wait(W_AFTER_KEY)

        # Transition
        self.play(FadeOut(VGroup(s1, s2, s2_txt, *eqs2, s2b, div)), run_time=T_TRANSITION)
        self.wait(0.3)

        # --- Step 3: Find center ---
        div2 = make_divider()
        self.play(FadeIn(div2), run_time=0.2)

        s3 = self.show_step_title("Hapi 3: Gjejmë qendrën e zmadhimit")

        s3_txt = Text(
            "Bashkojmë pikat korresponduese\n(p.sh. kulmin e sipërm djathtas)\nme një drejtëz. Qendra ndodhet\nku drejtëzat priten.",
            font_size=BODY_SIZE, color=BODY_TEXT_COLOR, line_spacing=1.4,
        )
        s3_txt.next_to(s3, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(FadeIn(s3_txt), run_time=T_BODY_FADE)
        self.wait(W_AFTER_KEY)

        # Draw connecting lines on graph
        pairs = list(zip(self.A_VERTS, self.D_VERTS))
        for (ax, ay), (dx, dy) in pairs[:2]:
            line = DashedLine(
                axes.c2p(ax, ay), axes.c2p(dx, dy),
                color=LABEL_COLOR, dash_length=0.08, stroke_width=1.5,
            )
            self.play(Create(line), run_time=0.5)

        eqs3 = self.show_equation_chain([
            {"tex": r"\text{Drejtëzat priten në } (-10,\,6)", "color": LABEL_COLOR, "key": True},
        ], start_reference=s3_txt, buff=0.5)

        self.wait(W_AFTER_ROUTINE)

        # Transition
        self.play(FadeOut(VGroup(s3, s3_txt, *eqs3, div2)), run_time=T_TRANSITION)
        self.wait(0.3)

        # --- Final answer ---
        s4 = self.show_step_title("Përgjigja")

        ans_txt = Text(
            "Shndërrimi A → D është një zmadhim\n(dilation) me:",
            font_size=BODY_SIZE + 2, color=WHITE, line_spacing=1.4,
        )
        ans_txt.next_to(s4, DOWN, buff=0.3)
        self.play(FadeIn(ans_txt), run_time=T_BODY_FADE)

        ans1 = MathTex(r"\text{Qendër: } (-10,\,6)", font_size=ANSWER_SIZE, color=ANSWER_COLOR)
        ans2 = MathTex(r"\text{Koeficient: } k = 0{,}5", font_size=ANSWER_SIZE, color=ANSWER_COLOR)

        ans_group = VGroup(ans1, ans2).arrange(DOWN, buff=0.3)
        ans_group.next_to(ans_txt, DOWN, buff=0.4)
        box = make_answer_box(ans_group)

        self.play(Write(ans_group), run_time=T_KEY_EQUATION)
        self.play(Create(box), run_time=0.5)
        self.wait(W_AFTER_ANSWER)

    # ================================================================
    #  FINAL SUMMARY
    # ================================================================
    def final_summary(self):
        self.show_summary_table(
            "Përmbledhje e përgjigjeve",
            [
                r"\text{a)}\; B: (5,1),\,(7,1),\,(7,2),\,(5,2) \;\; [Q(6,0),\; k\!=\!0{,}25]",
                r"\text{b)}\; C: (-3,-6),\,(-15,-6),\,(-15,-12),\,(-3,-12) \;\; [O,\; k\!=\!-1{,}5]",
                r"\text{c)}\; A \to D: \text{zmadhim me qendër } (-10,6),\; k = 0{,}5",
            ],
            font_size=24,
        )
