"""
Lokaal testen van de nieuwsupdate.

    python src/preview.py         haalt de echte RSS-bronnen op (zoals de dagelijkse run)
    python src/preview.py --nep   gebruikt nepberichten, voor een snelle lay-outcheck zonder internet

Het resultaat komt in src/preview.html en wordt direct in je browser geopend.
Er wordt niets gepubliceerd; dat doet alleen de GitHub-workflow.
"""

import argparse
import os
import sys
import webbrowser
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

import collectors
from renderer import bouw_html


def _nep(categorie, bron, uren_geleden, titel):
    return {
        "categorie": categorie,
        "bron": bron,
        "datum": datetime.now(timezone.utc) - timedelta(hours=uren_geleden),
        "titel": titel,
        "url": "https://example.com",
        "samenvatting": "Voorbeeldsamenvatting om te zien hoe de kaart eruitziet met wat langere tekst erin.",
    }


def nepdata():
    """Mix van berichten binnen en buiten het 24-uursvenster."""
    items = [
        _nep("Toezichthouder (NL)", "Autoriteit Financiële Markten (AFM)", 3, "Nieuw bericht van vanochtend"),
        _nep("Nieuws", "Accountant.nl", 20, "Nieuw bericht van gisteravond"),
        _nep("Toezichthouder (NL)", "Autoriteit Financiële Markten (AFM)", 50, "Ouder bericht, twee dagen geleden"),
        _nep("Centrale Bank", "European Central Bank (ECB)", 96, "Ouder bericht, andere categorie"),
    ]
    return items


def main():
    parser = argparse.ArgumentParser(description="Lokale preview van de nieuwsupdate.")
    parser.add_argument("--nep", action="store_true", help="gebruik nepberichten in plaats van de echte bronnen")
    parser.add_argument("--niet-openen", action="store_true", help="open de preview niet in de browser")
    args = parser.parse_args()

    if args.nep:
        print("== Preview met nepberichten ==")
        items = nepdata()
    else:
        print("== Preview met echte bronnen ==")
        items = collectors.verzamel_alles()
        print(f"Totaal {len(items)} relevante items gevonden.")

    html_output = bouw_html(items)
    uitvoer = Path(__file__).resolve().parent / "preview.html"
    uitvoer.write_text(html_output, encoding="utf-8")
    print(f"Geschreven naar {uitvoer}")
    if not args.niet_openen:
        webbrowser.open(uitvoer.as_uri())


if __name__ == "__main__":
    main()
