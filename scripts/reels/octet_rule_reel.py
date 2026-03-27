"""
Vertical Reel — Octet Rule Exception (Matura 2026, Q6)
=======================================================

9:16 vertical (1080×1920), ~55 seconds.
Hook: "Which molecule BREAKS the octet rule?"
Builds Lewis structures step-by-step (atoms → bonds → lone pairs),
checks octet for each, reveals BCl₃ as the exception.

Render:
    cd scripts && manim -qh reels/octet_rule_reel.py OctetRuleReel
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from manim import *
import numpy as np
from style_guide import (
    BG_COLOR, ALBANIAN_TEX,
    STEP_TITLE_COLOR, BODY_TEXT_COLOR, LABEL_COLOR,
    ANSWER_COLOR, SHAPE_COLOR, AUX_COLOR, HIGHLIGHT_COLOR, DIVIDER_COLOR,
)

# ── Vertical frame config ──
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 8
config.frame_height = 8 * (1920 / 1080)  # ≈ 14.22

# Colors
CORRECT_COLOR = ANSWER_COLOR
WRONG_COLOR = AUX_COLOR
BOND_COLOR = WHITE
ELECTRON_COLOR = LABEL_COLOR
BORON_COLOR = HIGHLIGHT_COLOR


class OctetRuleReel(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        MathTex.set_default(tex_template=ALBANIAN_TEX)
        Tex.set_default(tex_template=ALBANIAN_TEX)

        self.hook()
        self.show_options()
        self.check_h2s()
        self.check_cs2()
        self.check_ch4()
        self.check_bcl3()
        self.punchline()

    # ── Atom / Bond helpers ──
    def _atom(self, label, color=WHITE, radius=0.4, font_size=28):
        c = Circle(radius=radius, color=color, stroke_width=2)
        l = MathTex(label, font_size=font_size, color=color)
        l.move_to(c.get_center())
        return VGroup(c, l)

    def _bond(self, start, end, double=False):
        if not double:
            return Line(start, end, color=BOND_COLOR, stroke_width=2.5)
        d = np.array(end) - np.array(start)
        d_norm = d / np.linalg.norm(d)
        perp = np.array([-d_norm[1], d_norm[0], 0]) * 0.08
        l1 = Line(start + perp, end + perp, color=BOND_COLOR, stroke_width=2)
        l2 = Line(start - perp, end - perp, color=BOND_COLOR, stroke_width=2)
        return VGroup(l1, l2)

    def _lone_pair(self, center, direction, color=ELECTRON_COLOR):
        perp = np.array([-direction[1], direction[0], 0])
        norm = max(np.linalg.norm(perp), 0.001)
        perp = perp / norm * 0.08
        d1 = Dot(center + direction * 0.28 + perp, radius=0.04, color=color)
        d2 = Dot(center + direction * 0.28 - perp, radius=0.04, color=color)
        return VGroup(d1, d2)

    # ── Animated Lewis builder ──
    def _build_lewis(self, central, outers, bonds, lone_pairs, center_pos):
        """Animate building a Lewis structure step by step."""
        # Position everything
        all_parts = VGroup(central, *outers, *bonds, *lone_pairs)
        all_parts.move_to(center_pos)

        # Step 1: Central atom grows in
        self.play(GrowFromCenter(central), run_time=0.5)

        # Step 2: Outer atoms grow in
        self.play(
            LaggedStartMap(GrowFromCenter, VGroup(*outers), lag_ratio=0.12),
            run_time=0.6,
        )

        # Step 3: Bonds draw from center outward
        self.play(
            LaggedStart(*[Create(b) for b in bonds], lag_ratio=0.1),
            run_time=0.6,
        )

        # Step 4: Lone pairs pop in
        if lone_pairs:
            self.play(
                LaggedStartMap(FadeIn, VGroup(*lone_pairs), lag_ratio=0.08),
                run_time=0.5,
            )

        return all_parts

    # ── Electron count animation ──
    def _count_electrons(self, atom_label, bonds_list, lone_pairs_list,
                         target_count, y_pos, passes):
        """Animate counting electrons around an atom with a running counter."""
        color = CORRECT_COLOR if passes else WRONG_COLOR
        count = 0

        counter = MathTex(
            f"\\text{{{atom_label}: }}" + f"{count}e^-",
            font_size=30, color=color,
        )
        counter.move_to(np.array([0, y_pos, 0]))
        self.add(counter)

        # Flash each bond pair
        for bond in bonds_list:
            count += 2
            self.play(
                Indicate(bond, color=LABEL_COLOR, scale_factor=1.15),
                run_time=0.25,
            )
            new_counter = MathTex(
                f"\\text{{{atom_label}: }}" + f"{count}e^-",
                font_size=30, color=color,
            )
            new_counter.move_to(counter.get_center())
            self.remove(counter)
            self.add(new_counter)
            counter = new_counter

        # Flash each lone pair
        for lp in lone_pairs_list:
            count += 2
            self.play(
                Indicate(lp, color=ELECTRON_COLOR, scale_factor=1.3),
                run_time=0.25,
            )
            new_counter = MathTex(
                f"\\text{{{atom_label}: }}" + f"{count}e^-",
                font_size=30, color=color,
            )
            new_counter.move_to(counter.get_center())
            self.remove(counter)
            self.add(new_counter)
            counter = new_counter

        # Show final verdict
        symbol = r"\checkmark" if passes else r"\times"
        final = MathTex(
            f"\\text{{{atom_label}: }}{count}e^-"
            + f" / {target_count}e^- \\quad {symbol}",
            font_size=30, color=color,
        )
        final.move_to(counter.get_center())
        self.play(
            FadeOut(counter), FadeIn(final),
            run_time=0.3,
        )

        if passes:
            self.play(Circumscribe(final, color=CORRECT_COLOR, run_time=0.5))
        else:
            self.play(
                Flash(final.get_center(), color=WRONG_COLOR,
                      line_length=0.15, num_lines=8, run_time=0.4),
            )

        return final

    # ════════════════════════════════════════
    #  HOOK (0-4s)
    # ════════════════════════════════════════
    def hook(self):
        q = MathTex(r"?", font_size=180, color=WRONG_COLOR)
        q.move_to(UP * 3.5)

        hook1 = MathTex(
            r"\text{Cila molekulë}",
            font_size=48, color=WHITE,
        )
        hook2 = MathTex(
            r"\text{THYEN rregullin e oktetit?}",
            font_size=42, color=WRONG_COLOR,
        )
        hook_g = VGroup(hook1, hook2).arrange(DOWN, buff=0.35)
        hook_g.move_to(UP * 0.3)

        sub = MathTex(
            r"\text{Matura 2026 — Kimi}",
            font_size=28, color=BODY_TEXT_COLOR,
        )
        sub.next_to(hook_g, DOWN, buff=0.6)

        self.play(
            GrowFromCenter(q),
            FadeIn(hook_g, shift=UP * 0.5),
            FadeIn(sub, shift=UP * 0.2),
            run_time=0.8,
        )
        self.play(q.animate.scale(1.15), rate_func=there_and_back, run_time=0.5)
        self.wait(1.5)
        self.play(FadeOut(q), FadeOut(hook_g), FadeOut(sub), run_time=0.4)

    # ════════════════════════════════════════
    #  SHOW 4 OPTIONS (4-8s)
    # ════════════════════════════════════════
    def show_options(self):
        title = MathTex(
            r"\text{Opsionet:}",
            font_size=32, color=STEP_TITLE_COLOR,
        )
        title.move_to(UP * 4.5)

        def card(letter, formula):
            lbl = MathTex(f"\\text{{{letter})}}", font_size=32,
                          color=BODY_TEXT_COLOR)
            mol = MathTex(formula, font_size=44, color=SHAPE_COLOR)
            row = VGroup(lbl, mol).arrange(RIGHT, buff=0.4)
            box = SurroundingRectangle(row, color=SHAPE_COLOR, buff=0.25,
                                        corner_radius=0.1, stroke_width=1.5)
            return VGroup(row, box)

        options = VGroup(
            card("A", r"H_2S"), card("B", r"CS_2"),
            card("C", r"CH_4"), card("D", r"BCl_3"),
        ).arrange(DOWN, buff=0.5).move_to(UP * 1.0)

        self.play(FadeIn(title), run_time=0.4)
        self.play(
            LaggedStart(*[FadeIn(o, shift=RIGHT * 0.5) for o in options],
                         lag_ratio=0.12),
            run_time=1.0,
        )
        self.wait(2.0)
        self.play(FadeOut(title), FadeOut(options), run_time=0.4)

    # ════════════════════════════════════════
    #  A) H₂S (8-17s)
    # ════════════════════════════════════════
    def check_h2s(self):
        header = MathTex(r"\text{A)\ } H_2S", font_size=38, color=WHITE)
        header.move_to(UP * 5.0)
        self.play(FadeIn(header), run_time=0.4)

        # Build atoms
        s = self._atom("S", SHAPE_COLOR, 0.45, 30)
        h1 = self._atom("H", WHITE, 0.35, 26)
        h2 = self._atom("H", WHITE, 0.35, 26)

        s.move_to(ORIGIN)
        h1.move_to(LEFT * 1.5)
        h2.move_to(RIGHT * 1.5)

        b1 = self._bond(LEFT * 1.1, LEFT * 0.5)
        b2 = self._bond(RIGHT * 0.5, RIGHT * 1.1)

        lp1 = self._lone_pair(ORIGIN, UP)
        lp2 = self._lone_pair(ORIGIN, DOWN)

        lewis = self._build_lewis(
            s, [h1, h2], [b1, b2], [lp1, lp2],
            center_pos=UP * 1.8,
        )
        self.wait(1.0)

        # Count electrons on S
        verdict = self._count_electrons(
            "S", [b1, b2], [lp1, lp2],
            target_count=8, y_pos=-1.0, passes=True,
        )

        # Status
        status = MathTex(
            r"\text{Okteti: i plotësuar } \checkmark",
            font_size=32, color=CORRECT_COLOR,
        )
        status.move_to(DOWN * 2.5)
        status_box = SurroundingRectangle(status, color=CORRECT_COLOR,
                                           buff=0.15, corner_radius=0.08)
        self.play(FadeIn(status), Create(status_box), run_time=0.5)
        self.wait(2.0)

        self.play(FadeOut(VGroup(header, lewis, verdict, status, status_box)),
                  run_time=0.4)

    # ════════════════════════════════════════
    #  B) CS₂ (17-26s)
    # ════════════════════════════════════════
    def check_cs2(self):
        header = MathTex(r"\text{B)\ } CS_2", font_size=38, color=WHITE)
        header.move_to(UP * 5.0)
        self.play(FadeIn(header), run_time=0.4)

        c = self._atom("C", SHAPE_COLOR, 0.45, 30)
        s1 = self._atom("S", WHITE, 0.4, 26)
        s2 = self._atom("S", WHITE, 0.4, 26)

        c.move_to(ORIGIN)
        s1.move_to(LEFT * 1.8)
        s2.move_to(RIGHT * 1.8)

        b1 = self._bond(LEFT * 1.35, LEFT * 0.5, double=True)
        b2 = self._bond(RIGHT * 0.5, RIGHT * 1.35, double=True)

        lp1a = self._lone_pair(LEFT * 1.8, UP)
        lp1b = self._lone_pair(LEFT * 1.8, DOWN)
        lp2a = self._lone_pair(RIGHT * 1.8, UP)
        lp2b = self._lone_pair(RIGHT * 1.8, DOWN)

        lewis = self._build_lewis(
            c, [s1, s2], [b1, b2], [lp1a, lp1b, lp2a, lp2b],
            center_pos=UP * 1.8,
        )

        # Label double bonds
        db_label = MathTex(
            r"\text{Lidhje dyfishe!}",
            font_size=22, color=BODY_TEXT_COLOR,
        )
        db_label.next_to(lewis, DOWN, buff=0.3)
        self.play(FadeIn(db_label), run_time=0.3)
        self.wait(0.8)

        # Count on C: double bond = 4e⁻ each side
        verdict = self._count_electrons(
            "C", [b1, b2], [],
            target_count=8, y_pos=-1.3, passes=True,
        )

        status = MathTex(
            r"\text{Okteti: i plotësuar } \checkmark",
            font_size=32, color=CORRECT_COLOR,
        )
        status.move_to(DOWN * 2.5)
        status_box = SurroundingRectangle(status, color=CORRECT_COLOR,
                                           buff=0.15, corner_radius=0.08)
        self.play(FadeIn(status), Create(status_box), run_time=0.5)
        self.wait(2.0)

        self.play(FadeOut(VGroup(header, lewis, db_label, verdict,
                                 status, status_box)), run_time=0.4)

    # ════════════════════════════════════════
    #  C) CH₄ (26-34s)
    # ════════════════════════════════════════
    def check_ch4(self):
        header = MathTex(r"\text{C)\ } CH_4", font_size=38, color=WHITE)
        header.move_to(UP * 5.0)
        self.play(FadeIn(header), run_time=0.4)

        c = self._atom("C", SHAPE_COLOR, 0.45, 30)
        c.move_to(ORIGIN)

        positions = [UP * 1.3, DOWN * 1.3, LEFT * 1.5, RIGHT * 1.5]
        h_atoms = [self._atom("H", WHITE, 0.35, 26).move_to(p) for p in positions]

        bond_inner = [UP * 0.5, DOWN * 0.5, LEFT * 0.5, RIGHT * 0.5]
        bond_outer = [UP * 0.9, DOWN * 0.9, LEFT * 1.1, RIGHT * 1.1]
        bonds = [self._bond(i, o) for i, o in zip(bond_inner, bond_outer)]

        lewis = self._build_lewis(
            c, h_atoms, bonds, [],
            center_pos=UP * 1.8,
        )
        self.wait(0.8)

        verdict = self._count_electrons(
            "C", bonds, [],
            target_count=8, y_pos=-1.0, passes=True,
        )

        status = MathTex(
            r"\text{Okteti: i plotësuar } \checkmark",
            font_size=32, color=CORRECT_COLOR,
        )
        status.move_to(DOWN * 2.5)
        status_box = SurroundingRectangle(status, color=CORRECT_COLOR,
                                           buff=0.15, corner_radius=0.08)
        self.play(FadeIn(status), Create(status_box), run_time=0.5)
        self.wait(2.0)

        self.play(FadeOut(VGroup(header, lewis, verdict, status, status_box)),
                  run_time=0.4)

    # ════════════════════════════════════════
    #  D) BCl₃ — THE EXCEPTION (34-48s)
    # ════════════════════════════════════════
    def check_bcl3(self):
        header = MathTex(r"\text{D)\ } BCl_3", font_size=38, color=WHITE)
        header.move_to(UP * 5.0)
        self.play(FadeIn(header), run_time=0.4)

        b = self._atom("B", BORON_COLOR, 0.45, 30)
        b.move_to(ORIGIN)

        # Trigonal planar
        positions = [
            UP * 1.5,
            DOWN * 0.75 + LEFT * 1.3,
            DOWN * 0.75 + RIGHT * 1.3,
        ]
        cl_atoms = [self._atom("Cl", WHITE, 0.4, 24).move_to(p) for p in positions]

        bonds = []
        for p in positions:
            d = p / np.linalg.norm(p)
            bonds.append(self._bond(d * 0.5, d * 1.0))

        # 3 lone pairs on each Cl
        lone_pairs = []
        for p in positions:
            d = p / np.linalg.norm(p)
            perp = np.array([-d[1], d[0], 0])
            lone_pairs.append(self._lone_pair(p, d))
            lone_pairs.append(self._lone_pair(p, perp))
            lone_pairs.append(self._lone_pair(p, -perp))

        lewis = self._build_lewis(
            b, cl_atoms, bonds, lone_pairs,
            center_pos=UP * 1.8,
        )
        self.wait(1.0)

        # Count electrons on B — only 3 bonds, no lone pairs = 6e⁻
        verdict = self._count_electrons(
            "B", bonds, [],
            target_count=8, y_pos=-1.0, passes=False,
        )
        self.wait(1.0)

        # Dramatic highlight on B
        # Find B atom in the lewis group
        self.play(
            Indicate(b, color=WRONG_COLOR, scale_factor=1.4),
            run_time=0.6,
        )

        # Explanation
        expl = MathTex(
            r"\text{Bori ka vetëm 6 elektrone valentore!}",
            font_size=28, color=WRONG_COLOR,
        )
        expl.move_to(DOWN * 2.2)
        self.play(Write(expl), run_time=0.6)
        self.wait(1.0)

        status = MathTex(
            r"\text{Okteti: NUK plotësohet!}",
            font_size=36, color=WRONG_COLOR,
        )
        status.move_to(DOWN * 3.3)
        status_box = SurroundingRectangle(status, color=WRONG_COLOR,
                                           buff=0.2, corner_radius=0.1)
        self.play(FadeIn(status), Create(status_box), run_time=0.5)
        self.play(
            Flash(status.get_center(), color=WRONG_COLOR,
                  line_length=0.3, num_lines=10, run_time=0.5),
        )
        self.wait(2.5)

        self.play(FadeOut(VGroup(header, lewis, verdict, expl,
                                 status, status_box)), run_time=0.4)

    # ════════════════════════════════════════
    #  PUNCHLINE (48-58s)
    # ════════════════════════════════════════
    def punchline(self):
        ans_label = MathTex(
            r"\text{Përgjigja:}",
            font_size=36, color=WHITE,
        )
        ans_label.move_to(UP * 3.5)

        ans_d = MathTex(
            r"\text{D)}\quad BCl_3",
            font_size=56, color=WRONG_COLOR,
        )
        ans_d.move_to(UP * 1.5)
        box = SurroundingRectangle(ans_d, color=WRONG_COLOR, buff=0.3,
                                    corner_radius=0.12)

        explanation = VGroup(
            MathTex(
                r"\text{Bori (B) ka vetëm 3 elektrone valentore}",
                font_size=26, color=BODY_TEXT_COLOR,
            ),
            MathTex(
                r"\text{Formon 3 lidhje = 6e}^- \text{ (jo 8)}",
                font_size=26, color=BODY_TEXT_COLOR,
            ),
            MathTex(
                r"\text{Përjashtim klasik i rregullit të oktetit!}",
                font_size=28, color=HIGHLIGHT_COLOR,
            ),
        ).arrange(DOWN, buff=0.3)
        explanation.move_to(DOWN * 0.8)

        cta = MathTex(
            r"\text{@mesonjetorja}",
            font_size=32, color=STEP_TITLE_COLOR,
        )
        cta.move_to(DOWN * 3.0)

        self.play(Write(ans_label), run_time=0.5)
        self.play(
            GrowFromCenter(ans_d), Create(box),
            run_time=0.7,
        )
        self.play(
            Flash(ans_d.get_center(), color=WRONG_COLOR,
                  line_length=0.25, num_lines=12, run_time=0.5),
        )
        self.wait(0.8)
        self.play(
            LaggedStart(*[FadeIn(e, shift=UP * 0.2) for e in explanation],
                         lag_ratio=0.2),
            run_time=1.0,
        )
        self.wait(2.5)
        self.play(FadeIn(cta, shift=UP * 0.2), run_time=0.4)
        self.play(
            Circumscribe(VGroup(ans_d, box), color=WRONG_COLOR, run_time=0.8),
        )
        self.wait(2.5)
