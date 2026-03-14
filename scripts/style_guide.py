"""
Mësonjëtorja Manim Video Style Guide
=====================================

3Blue1Brown-inspired professional visual style for all educational math videos.
Import this module in every video script to use the shared constants.

Usage:
    from style_guide import *
"""

from manim import *

# ──────────────────────────────────────────────
#  BACKGROUND
# ──────────────────────────────────────────────
BG_COLOR = "#1C1C1C"  # 3b1b dark charcoal

# ──────────────────────────────────────────────
#  SEMANTIC COLOR ROLES
# ──────────────────────────────────────────────
STEP_TITLE_COLOR = "#5CD0B3"   # Soft teal — step headers ("Hapi 1:")
BODY_TEXT_COLOR = GRAY_B       # #BBBBBB — explanatory prose
LABEL_COLOR = YELLOW           # Diagram numeric labels (side lengths, values)
ANSWER_COLOR = "#83C167"       # Green — final boxed answers
SHAPE_COLOR = "#58C4DD"        # Blue — primary geometric objects (circles, shapes)
AUX_COLOR = "#FC6255"          # Red — construction / auxiliary lines
HIGHLIGHT_COLOR = "#FF862F"    # Orange — secondary emphasis, second point
DIVIDER_COLOR = "#888888"      # Dim gray — dashed dividers, grids

# ──────────────────────────────────────────────
#  TYPOGRAPHY SIZES
# ──────────────────────────────────────────────
TITLE_SIZE = 48
SUBTITLE_SIZE = 30
PART_HEADER_SIZE = 32
STEP_TITLE_SIZE = 26
BODY_SIZE = 22
PROBLEM_MATH_SIZE = 36
CALC_SIZE = 32
ANSWER_SIZE = 36
DIAGRAM_LABEL_SIZE = 32
DIAGRAM_VALUE_SIZE = 26

# ──────────────────────────────────────────────
#  ANIMATION TIMING (seconds)
# ──────────────────────────────────────────────
T_TITLE_WRITE = 1.5
T_SUBTITLE_FADE = 0.8
T_HEADER_WRITE = 0.6
T_STEP_TITLE = 0.5
T_BODY_FADE = 0.7
T_KEY_EQUATION = 1.1
T_ROUTINE_EQUATION = 0.8
T_SHAPE_CREATE = 1.2
T_DOT_FADE = 0.4
T_LAYOUT_SHIFT = 1.0
T_TRANSITION = 0.7

W_AFTER_KEY = 2.0      # Wait after important result
W_AFTER_ROUTINE = 1.2   # Wait after routine step
W_AFTER_ANSWER = 3.5    # Wait after final answer
W_PROBLEM = 3.0         # Wait while showing problem statement

# ──────────────────────────────────────────────
#  LAYOUT CONSTANTS
# ──────────────────────────────────────────────
DIAGRAM_CENTER = LEFT * 3.2
CALC_CENTER = RIGHT * 3.2
CALC_TOP = RIGHT * 3.2 + UP * 3.0
DIVIDER_X = -0.3

# ──────────────────────────────────────────────
#  HELPER: Apply background
# ──────────────────────────────────────────────

def apply_style(scene):
    """Call at the start of construct() to set the background."""
    scene.camera.background_color = BG_COLOR


def make_divider():
    """Create a standard vertical dashed divider line."""
    return DashedLine(
        UP * 3.5 + RIGHT * DIVIDER_X,
        DOWN * 3.8 + RIGHT * DIVIDER_X,
        color=DIVIDER_COLOR,
        dash_length=0.15,
        stroke_width=1,
        stroke_opacity=0.3,
    )


def make_answer_box(mobject, color=None):
    """Create a SurroundingRectangle for answer display."""
    return SurroundingRectangle(
        mobject,
        color=color or ANSWER_COLOR,
        buff=0.2,
        corner_radius=0.08,
    )


def fade_all(scene, run_time=None):
    """Fade out all mobjects on screen."""
    scene.play(
        *[FadeOut(m) for m in scene.mobjects],
        run_time=run_time or T_TRANSITION,
    )
