"""
Hoofdscript. Draai dit wekelijks (via GitHub Actions of lokaal):
    python src/main.py

Resultaat: een bestand build/index.html dat GitHub Pages publiceert.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import collectors
import renderer


def main():
    print("== BSG Update: nieuwsbrief samenstellen ==")
    items = collectors.verzamel_alles()
    print(f"Totaal {len(items)} relevante items gevonden.")

    html = renderer.bouw_html(items)

    uit_map = os.path.join(os.path.dirname(__file__), "..", "build")
    os.makedirs(uit_map, exist_ok=True)
    pad = os.path.join(uit_map, "index.html")
    with open(pad, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Geschreven naar {os.path.abspath(pad)}")


if __name__ == "__main__":
    main()
