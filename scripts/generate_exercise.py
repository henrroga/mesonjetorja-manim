#!/usr/bin/env python3
"""
Exercise Script Generator
=========================

Parses exercise JSON (from mesonjetorja.com) and generates a Manim script
that uses ExerciseScene components.

Usage:
    python generate_exercise.py exercise.json
    python generate_exercise.py exercise.json --output scripts/5.1B/ushtrimi2.py
    echo '{"name":"1",...}' | python generate_exercise.py -

The generated script is a working starting point — review and adjust
animations, timing, and explanations before rendering.
"""

import json
import re
import sys
import os
import html
from textwrap import dedent, indent


# ──────────────────────────────────────────
#  HTML/KaTeX PARSING
# ──────────────────────────────────────────

def extract_latex_formulas(html_str):
    """Extract LaTeX from ql-formula data-value attributes."""
    return re.findall(r'data-value="([^"]+)"', html_str)


def strip_html(html_str):
    """Strip HTML tags, decode entities, return plain text."""
    text = re.sub(r'<[^>]+>', ' ', html_str)
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    # Remove the KaTeX rendered spans (they appear as ﻿ characters)
    text = text.replace('﻿', '')
    return text


def extract_parts_from_question(html_str):
    """
    Parse the question HTML into a list of parts.

    Returns list of dicts: [{"letter": "a", "latex": "...", "text": "..."}]
    """
    parts = []

    # Find all <li> items (each is a sub-problem)
    li_pattern = re.compile(r'<li[^>]*>(.*?)</li>', re.DOTALL)
    matches = li_pattern.findall(html_str)

    letters = "abcdefghijklmnopqrstuvwxyz"
    for i, li_html in enumerate(matches):
        formulas = extract_latex_formulas(li_html)
        text = strip_html(li_html)
        parts.append({
            "letter": letters[i] if i < 26 else str(i + 1),
            "latex": formulas[0] if formulas else text,
            "all_formulas": formulas,
            "text": text,
        })

    return parts


def extract_solution_steps(solution_html):
    """
    Parse solution HTML into steps per part.

    Returns dict: {"a": [{"text": "...", "latex": [...]}], ...}
    """
    parts = {}
    letters = "abcdefghijklmnopqrstuvwxyz"

    # Split by <p><strong>N. headings
    sections = re.split(r'<p>\s*<strong>\s*(\d+)\.', solution_html)

    # sections[0] is before first heading, then pairs of (number, content)
    for i in range(1, len(sections), 2):
        part_num = int(sections[i]) - 1
        letter = letters[part_num] if part_num < 26 else str(part_num + 1)
        content = sections[i + 1] if i + 1 < len(sections) else ""

        # Extract LaTeX from $...$ delimiters
        latex_formulas = re.findall(r'\$([^$]+)\$', content)

        # Extract steps from <li> items
        steps = []
        li_matches = re.findall(r'<li>(.*?)</li>', content, re.DOTALL)
        for li in li_matches:
            step_formulas = re.findall(r'\$([^$]+)\$', li)
            step_text = strip_html(re.sub(r'\$[^$]+\$', '□', li))
            steps.append({
                "text": step_text,
                "latex": step_formulas,
            })

        parts[letter] = {
            "steps": steps,
            "all_latex": latex_formulas,
        }

    return parts


def find_final_answer(steps_data):
    """Try to find the final answer equation from solution steps."""
    all_latex = steps_data.get("all_latex", [])
    if not all_latex:
        return None

    # The last equation with x = ... or similar is usually the answer
    for latex in reversed(all_latex):
        if re.search(r'x\s*=\s*', latex):
            return latex

    return all_latex[-1] if all_latex else None


# ──────────────────────────────────────────
#  SOLUTION STEP CLASSIFIER
# ──────────────────────────────────────────

def classify_step(step_latex_list, step_text):
    """
    Classify a solution step to determine how to animate it.

    Returns dict with: type, title (Albanian), equations, explanation
    """
    text_lower = step_text.lower()

    if any(w in text_lower for w in ["përkufizim", "definition", "b^c"]):
        return {"type": "definition", "title": "Përkufizimi i logaritmit"}
    elif any(w in text_lower for w in ["zbritj", "subtrac", "log_b a - log_b"]):
        return {"type": "log_property", "title": "Vetia e zbritjes"}
    elif any(w in text_lower for w in ["mbledh", "addit", "log_b a + log_b"]):
        return {"type": "log_property", "title": "Vetia e mbledhjes"}
    elif any(w in text_lower for w in ["faktoriz", "factor"]):
        return {"type": "factoring", "title": "Faktorizimi"}
    elif any(w in text_lower for w in ["argument", "elimin", "nuk pranon"]):
        return {"type": "argument", "title": "Argumentimi"}
    elif any(w in text_lower for w in ["baraz", "equal"]):
        return {"type": "simplify", "title": "Barazojmë argumentet"}
    elif any(w in text_lower for w in ["zgjidhj", "solv", "pjesëtoj", "kaloj"]):
        return {"type": "solve", "title": "Zgjidhim për x"}
    else:
        return {"type": "generic", "title": "Thjeshtimi"}


# ──────────────────────────────────────────
#  CODE GENERATION
# ──────────────────────────────────────────

def escape_latex(s):
    """Escape a LaTeX string for Python raw string."""
    return s.replace("\\", "\\\\") if not s.startswith("r") else s


def generate_part_method(letter, part_question, solution_data):
    """Generate the Python code for a single part method."""
    latex_eq = part_question["latex"]
    sol = solution_data.get(letter, {})
    steps = sol.get("steps", [])
    final_answer = find_final_answer(sol)

    lines = []
    lines.append(f"    def part_{letter}(self):")
    lines.append(f'        self.show_part_header("{letter}")')
    lines.append(f"        self.show_problem(")
    lines.append(f'            MathTex(r"{latex_eq}", font_size=PROBLEM_MATH_SIZE + 4),')
    lines.append(f"        )")
    lines.append("")

    # Generate steps
    step_num = 0
    prev_var = None
    all_eq_vars = []

    for i, step in enumerate(steps):
        step_num += 1
        classification = classify_step(step["latex"], step["text"])
        step_title = classification["title"]

        # Step title
        if i == 0:
            lines.append(f'        s{step_num} = self.show_step_title("Hapi {step_num}: {step_title}")')
        elif prev_var:
            lines.append(f'        s{step_num} = self.show_step_title("Hapi {step_num}: {step_title}", reference={prev_var})')
        else:
            lines.append(f'        s{step_num} = self.show_step_title("Hapi {step_num}: {step_title}")')

        # Explanation text if step has descriptive text
        has_explanation = len(step["text"]) > 5 and "□" not in step["text"][:10]
        if has_explanation and step["text"].strip() not in ["", "□"]:
            clean_text = step["text"].replace("□", "").strip()
            if len(clean_text) > 5:
                lines.append(f"")
                lines.append(f'        s{step_num}_txt = Text(')
                lines.append(f'            "{clean_text[:60]}",')
                lines.append(f"            font_size=BODY_SIZE, color=BODY_TEXT_COLOR,")
                lines.append(f"        )")
                lines.append(f"        s{step_num}_txt.next_to(s{step_num}, DOWN, buff=0.25, aligned_edge=LEFT)")
                lines.append(f"        self.play(FadeIn(s{step_num}_txt), run_time=T_BODY_FADE)")
                lines.append(f"        self.wait(W_AFTER_ROUTINE)")

        # Equations
        if step["latex"]:
            eq_specs = []
            for j, eq_latex in enumerate(step["latex"]):
                is_last_eq = (j == len(step["latex"]) - 1)
                is_answer = is_last_eq and (i == len(steps) - 1) and final_answer and eq_latex == final_answer
                is_key = is_last_eq

                spec = {}
                spec["tex"] = eq_latex
                if is_answer:
                    spec["color"] = "ANSWER_COLOR"
                    spec["font_size"] = "CALC_SIZE + 2"
                elif is_key and j > 0:
                    spec["color"] = "LABEL_COLOR"
                if is_key:
                    spec["key"] = True

                eq_specs.append(spec)

            var_name = f"eqs{step_num}"
            all_eq_vars.append(var_name)
            lines.append(f"")

            ref_part = f"start_reference=s{step_num}"
            if has_explanation:
                ref_part = f"start_reference=s{step_num}_txt"

            lines.append(f"        {var_name} = self.show_equation_chain([")
            for spec in eq_specs:
                if len(spec) == 1:
                    lines.append(f'            r"{spec["tex"]}",')
                else:
                    parts = [f'"tex": r"{spec["tex"]}"']
                    if "color" in spec:
                        parts.append(f'"color": {spec["color"]}')
                    if "font_size" in spec:
                        parts.append(f'"font_size": {spec["font_size"]}')
                    if spec.get("key"):
                        parts.append(f'"key": True')
                    lines.append("            {" + ", ".join(parts) + "},")
            lines.append(f"        ], {ref_part})")
            prev_var = f"{var_name}[-1]"
        else:
            prev_var = f"s{step_num}"

        lines.append("")

    # Final answer
    if final_answer:
        ref = prev_var or f"s{step_num}"
        lines.append(f'        self.show_answer_below(r"{final_answer}", {ref})')
    else:
        lines.append(f"        # TODO: Add final answer")

    lines.append("")
    return "\n".join(lines)


def generate_script(exercise_json):
    """Generate a complete Manim script from exercise JSON."""
    name = exercise_json["name"]
    unit = exercise_json["unit"]
    source = exercise_json.get("source", "Matematika 10-11: Pjesa II")
    question_html = exercise_json["question"]
    solution_html = exercise_json.get("solution", "")

    # Parse
    parts = extract_parts_from_question(question_html)
    solution_steps = extract_solution_steps(solution_html) if solution_html else {}

    # Question description
    question_text = strip_html(question_html.split("<ol")[0]) if "<ol" in question_html else strip_html(question_html)

    part_letters = [p["letter"] for p in parts]
    parts_list_str = ", ".join(f'"{l}"' for l in part_letters)

    # Unit directory
    unit_dir = unit

    # Generate imports
    script = f'''import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from manim import *
import numpy as np
from components import ExerciseScene
from style_guide import (
    STEP_TITLE_COLOR, BODY_TEXT_COLOR, LABEL_COLOR,
    ANSWER_COLOR, SHAPE_COLOR,
    STEP_TITLE_SIZE, BODY_SIZE, PROBLEM_MATH_SIZE, CALC_SIZE,
    T_STEP_TITLE, T_BODY_FADE, T_KEY_EQUATION,
    T_SHAPE_CREATE, T_TRANSITION,
    W_AFTER_KEY, W_AFTER_ROUTINE, W_PROBLEM,
    CALC_TOP,
)


class Ushtrimi{name}(ExerciseScene):
    """
    Ushtrimi {name} — Njësia {unit}
    {source}

    {question_text[:80]}
    """

    exercise_number = {name}
    unit = "{unit}"
    textbook = "{source}"
    parts = [{parts_list_str}]

'''

    # Generate each part method
    for part in parts:
        letter = part["letter"]
        sol_data = solution_steps
        method_code = generate_part_method(letter, part, sol_data)
        script += method_code + "\n"

    # Generate final summary
    summary_rows = []
    for part in parts:
        letter = part["letter"]
        sol = solution_steps.get(letter, {})
        answer = find_final_answer(sol)
        if answer:
            row = '                r"\\text{' + letter + ')}\\ \\quad ' + answer + '",'
        else:
            row = '                r"\\text{' + letter + ')}\\ \\quad \\text{TODO}",'
        summary_rows.append(row)

    rows_block = "\n".join(summary_rows)
    script += """    # ================================================================
    #  FINAL SUMMARY
    # ================================================================
    def final_summary(self):
        self.show_summary_table(
            "Përmbledhje e përgjigjeve",
            [
""" + rows_block + """
            ],
            font_size=30,
        )
"""

    return script


# ──────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate a Manim exercise script from exercise JSON.",
        epilog="Example: python generate_exercise.py exercise.json",
    )
    parser.add_argument(
        "input",
        help="JSON file path, or '-' to read from stdin.",
    )
    parser.add_argument(
        "--output", "-o",
        help="Output .py file path. Default: auto-generate from unit/name.",
    )
    parser.add_argument(
        "--print", "-p",
        action="store_true",
        help="Print to stdout instead of writing a file.",
    )

    args = parser.parse_args()

    # Read input
    if args.input == "-":
        data = json.load(sys.stdin)
    else:
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)

    # Generate
    script = generate_script(data)

    # Output
    if args.print:
        print(script)
    else:
        output_path = args.output
        if not output_path:
            unit = data["unit"]
            name = data["name"]
            base_dir = os.path.dirname(os.path.abspath(__file__))
            unit_dir = os.path.join(base_dir, unit)
            os.makedirs(unit_dir, exist_ok=True)
            output_path = os.path.join(unit_dir, f"ushtrimi{name}.py")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(script)

        print(f"Generated: {output_path}")
        print(f"  Exercise: Ushtrimi {data['name']} — {data['unit']}")
        print(f"  Parts: {len(extract_parts_from_question(data['question']))}")
        print(f"  Review the script and adjust animations before rendering.")


if __name__ == "__main__":
    main()
