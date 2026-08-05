"""
Bouwt uit de verzamelde items een statische HTML-pagina in BSG-huisstijl.
De pagina is bewust selfcontained (inline CSS) zodat GitHub Pages hem direct serveert.
"""

from datetime import datetime, timezone
import html
import base64
from pathlib import Path

import config

MAANDEN = ["", "januari", "februari", "maart", "april", "mei", "juni",
           "juli", "augustus", "september", "oktober", "november", "december"]

# Volgorde waarin categorieën in de nieuwsbrief verschijnen.
CATEGORIE_VOLGORDE = [
    "Nieuws",
    "Brancheorganisatie",
    "Centrale Bank",
    "Toezichthouder (NL)",
    "Toezichthouder (EU)",
]

def _nl_datum(dt: datetime) -> str:
    return f"{dt.day} {MAANDEN[dt.month]} {dt.year}"


def _esc(t: str) -> str:
    return html.escape(t or "")

def _logo_wit_data_uri() -> str:
    pad = Path(__file__).resolve().parent.parent / "media" / "tekst_groot_wit.png"
    data = base64.b64encode(pad.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{data}"

def _logo_zwart_data_uri() -> str:
    pad = Path(__file__).resolve().parent.parent / "media" / "tekst_groot_zwart.png"
    data = base64.b64encode(pad.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{data}"

def _favicon_data_uri() -> str:
    pad = Path(__file__).resolve().parent.parent / "media" / "favicon.png"
    data = base64.b64encode(pad.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{data}"

def bouw_html(items: list) -> str:
    h = config.HUISSTIJL
    nu = datetime.now(timezone.utc)
    logo_wit = _logo_wit_data_uri()
    logo_zwart = _logo_zwart_data_uri()
    favicon = _favicon_data_uri()

    # Groepeer per categorie.
    per_categorie = {}
    for item in items:
        per_categorie.setdefault(item["categorie"], []).append(item)

    # Bouw de secties.
    secties_html = []
    # Bekende categorieën eerst, in vaste volgorde; daarna nieuwe automatisch erachter.
    overige = [c for c in per_categorie if c not in CATEGORIE_VOLGORDE]
    for categorie in CATEGORIE_VOLGORDE + overige:
        groep = per_categorie.get(categorie, [])
        if not groep:
            continue
        kaarten = []
        for item in groep:
            datum_regel = _nl_datum(item["datum"])
            kaarten.append(f"""
            <article class="item">
              <div class="item-meta">
                <span class="bron">{_esc(item['bron'])}</span>
                <span class="datum">{datum_regel}</span>
              </div>
              <h3 class="item-titel">
                <a href="{_esc(item['url'])}" target="_blank" rel="noopener">{_esc(item['titel'])}</a>
              </h3>
              <p class="item-tekst">{_esc(item['samenvatting'])}</p>
            </article>""")
        secties_html.append(f"""
        <section class="categorie">
          <h2 class="categorie-kop">{_esc(categorie)}</h2>
          <div class="items">{''.join(kaarten)}</div>
        </section>""")

    if not secties_html:
        secties_html.append("""
        <section class="categorie">
          <div class="leeg">Deze week zijn er geen nieuwe berichten of uitspraken gevonden binnen de ingestelde criteria.</div>
        </section>""")

    aantal = len(items)
    body = "".join(secties_html)

    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{_esc(config.NIEUWSBRIEF_TITEL)} {_nl_datum(nu)}</title>
<link rel="icon" type="image/png" href="{favicon}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fira+Sans:wght@500;600;700&display=swap" rel="stylesheet">
<style>
  :root {{
    --primair: {h['primair']};
    --accent: {h['accent']};
    --tekst: {h['tekst']};
    --tekst-zacht: {h['tekst_zacht']};
    --achtergrond: {h['achtergrond']};
    --vlak: {h['vlak']};
    --lijn: {h['lijn']};
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    background: var(--achtergrond);
    color: var(--tekst);
    font-family: {h['tekst_font']};
    font-size: 16px;
    line-height: 1.55;
  }}
  .wrap {{ max-width: 760px; margin: 0 auto; padding: 0 24px 80px; }}

  header.hero {{
    background: var(--accent);
    color: #fff;
    padding: 48px 0 44px;
    margin-bottom: 40px;
  }}
  .hero-inner {{ max-width: 760px; margin: 0 auto; padding: 0 24px; }}
  .merk {{
    display: inline-block;
    font-family: {h['kop_font']};
    font-weight: 700;
    letter-spacing: .14em;
    text-transform: uppercase;
    font-size: 12px;
    color: var(--primair);
    margin-bottom: 18px;
  }}
  .logo_groot {{
    display: block;
    height: 64px;
    margin-bottom: 16px;
  }}
  .logo_klein {{
    display: block;
    height: 24px;
    margin-top: 8px;
  }}
  .hero h1 {{
    font-family: {h['kop_font']};
    font-weight: 700;
    font-size: 40px;
    line-height: 1.05;
    margin: 0 0 10px;
  }}
  .hero h1 .accentstreep {{
    display: block; width: 56px; height: 5px;
    background: var(--primair); margin-top: 18px; border-radius: 2px;
  }}
  .hero p.sub {{ margin: 0; font-size: 17px; color: rgba(255,255,255,.82); max-width: 52ch; }}
  .hero .uitgave {{ margin-top: 20px; font-size: 13px; color: rgba(255,255,255,.65); }}

  .categorie {{ margin-bottom: 44px; }}
  .categorie-kop {{
    font-family: {h['kop_font']};
    font-weight: 600;
    font-size: 14px;
    letter-spacing: .06em;
    text-transform: uppercase;
    color: var(--accent);
    margin: 0 0 4px;
    padding-bottom: 10px;
    border-bottom: 2px solid var(--primair);
  }}

  .item {{
    padding: 22px 0 22px 20px;
    border-bottom: 1px solid var(--lijn);
    border-left: 3px solid transparent;
    transition: border-color .15s ease, background .15s ease;
  }}
  .item:hover {{ border-left-color: var(--primair); background: var(--vlak); }}
  .item-meta {{
    display: flex; gap: 12px; align-items: baseline;
    font-size: 12.5px; color: var(--tekst-zacht); margin-bottom: 6px;
  }}
  .bron {{
    font-weight: 600; color: #ffffff;
    background: var(--primair); padding: 2px 8px; border-radius: 3px;
    font-size: 11.5px;
  }}
  .item-titel {{ font-family: {h['kop_font']}; font-weight: 600; font-size: 19px; line-height: 1.3; margin: 0 0 6px; }}
  .item-titel a {{ color: var(--tekst); text-decoration: none; }}
  .item-titel a:hover {{ color: var(--accent); text-decoration: underline; text-decoration-color: var(--primair); }}
  .item-tekst {{ margin: 0; color: var(--tekst-zacht); font-size: 15px; }}

  .leeg {{ padding: 24px; background: var(--vlak); border-radius: 6px; color: var(--tekst-zacht); }}

  footer {{
    margin-top: 56px; padding-top: 24px; border-top: 1px solid var(--lijn);
    font-size: 12.5px; color: var(--tekst-zacht);
  }}
  footer strong {{ color: var(--accent); }}

  @media (max-width: 520px) {{
    .hero h1 {{ font-size: 30px; }}
    .wrap {{ padding: 0 18px 60px; }}
  }}
  @media (prefers-reduced-motion: reduce) {{
    .item {{ transition: none; }}
  }}
</style>
</head>
<body>
  <header class="hero">
    <div class="hero-inner">
      <span class="merk">Finance, Data, Risk & Compliance nieuwsupdate</span>
      <a href="https://www.brightstonegroup.nl" target="_blank" rel="noopener">
        <img src="{logo_wit}" alt="{_esc(config.NIEUWSBRIEF_TITEL)}" class="logo_groot">
      </a>
      <!-- <h1>{_esc(config.NIEUWSBRIEF_TITEL)}<span class="accentstreep"></span></h1> -->
      <p class="sub">{_esc(config.NIEUWSBRIEF_SUBTITEL)}</p>
      <div class="uitgave">Versie {_nl_datum(nu)} · {aantal} {'berichten' if aantal != 1 else 'bericht'} uit de afgelopen {config.DAGEN_TERUG} dagen</div>
    </div>
  </header>

  <main class="wrap">
    {body}

    <footer>
      <p>Deze nieuwsupdate is automatisch samengesteld uit RSS-feeds van openbare bronnen, als de <strong>DNB</strong>, de <strong>AFM</strong>, <strong>EBA</strong>, <strong>FD</strong>, <strong>VBIN</strong>, <strong>FIU</strong> en <strong>VCO</strong></p>
      <p>Samenstelling gebeurt geautomatiseerd. Controleer altijd de oorspronkelijke bron.</p>
      <a href="https://www.brightstonegroup.nl" target="_blank" rel="noopener">
        <img src="{logo_zwart}" class="logo_klein">
      </a>
    </footer>
  </main>
</body>
</html>"""
