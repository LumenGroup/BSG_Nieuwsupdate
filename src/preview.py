from datetime import datetime, timezone
from pathlib import Path

from renderer import bouw_html

nep_items = [
    {
        "categorie": "Toezichthouder (NL)",
        "bron": "Autoriteit Persoonsgegevens",
        "datum": datetime.now(timezone.utc),
        "titel": "Voorbeeldtitel voor lay-outtest",
        "url": "https://example.com",
        "samenvatting": "Korte voorbeeldsamenvatting om te zien hoe de kaart eruitziet met wat langere tekst erin.",
    },
    {
        "categorie": "Jurisprudentie (EU)",
        "bron": "HvJ-EU",
        "datum": datetime.now(timezone.utc),
        "titel": "Tweede voorbeeld, andere categorie",
        "url": "https://example.com",
        "samenvatting": "Ook hier een voorbeeldtekst.",
    },
]

html_output = bouw_html(nep_items)
uitvoer = Path(__file__).resolve().parent / "preview.html"
uitvoer.write_text(html_output, encoding="utf-8")
print(f"Geschreven naar {uitvoer}")
