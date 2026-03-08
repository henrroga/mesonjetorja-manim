# mesonjetorja-manim

Video shpjeguese për matematikën me [Manim Community Edition](https://www.manim.community/) — në shqip.

Explanatory math videos using Manim CE — in Albanian.

## Structure

```
scripts/
  └── {unit}/           # e.g. 7.2A
      └── ushtrimi{n}.py  # exercise number
```

Source: **Matematika 10-11: Pjesa II**

## Render

```bash
# Low quality preview
manim -pql scripts/7.2A/ushtrimi4.py Ushtrimi4

# High quality (1080p60)
manim -qh scripts/7.2A/ushtrimi4.py Ushtrimi4
```

## Requirements

- Python 3.8+
- [Manim Community](https://docs.manim.community/en/stable/installation.html)
- LaTeX distribution (e.g. MacTeX, TeX Live)
