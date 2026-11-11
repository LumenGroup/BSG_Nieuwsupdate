"""
Ophalen van de vier bronnen en normaliseren naar één gemeenschappelijk formaat.

Elk item is een dict:
    {
        "bron": str,          # naam van de bron
        "categorie": str,     # groep waaronder het valt in de nieuwsbrief
        "titel": str,
        "samenvatting": str,  # korte tekst (2-3 zinnen), reeds ingekort
        "url": str,
        "datum": datetime,    # publicatie- of wijzigingsdatum (tz-aware, UTC)
    }
"""

from datetime import datetime, timedelta, timezone
import calendar
import html
import re
from urllib.parse import urlsplit, parse_qsl, urlencode
import xml.etree.ElementTree as ET

import requests
import feedparser

import config

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/rss+xml, application/xml, text/xml, */*",
    "Accept-Language": "nl-NL,nl;q=0.9,en;q=0.8",
}
TIMEOUT = 30


def _nu_utc():
    return datetime.now(timezone.utc)


def _grens():
    return _nu_utc() - timedelta(days=config.DAGEN_TERUG)


def _schoon(tekst: str, max_len: int = 320) -> str:
    """HTML strippen, whitespace normaliseren en inkorten tot ~2-3 zinnen."""
    if not tekst:
        return ""
    tekst = re.sub(r"<[^>]+>", " ", tekst)          # tags weg
    tekst = html.unescape(tekst)
    tekst = re.sub(r"\s+", " ", tekst).strip()
    if len(tekst) <= max_len:
        return tekst
    # Knip netjes af op zinseinde binnen de limiet.
    afgekapt = tekst[:max_len]
    laatste_punt = max(afgekapt.rfind(". "), afgekapt.rfind("! "), afgekapt.rfind("? "))
    if laatste_punt > 120:
        return afgekapt[: laatste_punt + 1]
    return afgekapt.rstrip() + "..."


# Woordgrens-matching in plaats van kale substring-matching: voorkomt dat korte
# afkortingen als "fec" of "erm" per ongeluk matchen binnen gewone woorden
# ("effect", "term").
_TREFWOORD_PATRONEN = [re.compile(r"\b" + re.escape(tw) + r"\b") for tw in config.TREFWOORDEN]


def _bevat_trefwoord(*teksten) -> bool:
    bak = " ".join(t for t in teksten if t).lower()
    return any(patroon.search(bak) for patroon in _TREFWOORD_PATRONEN)


def _struct_naar_dt(struct_time):
    if not struct_time:
        return None
    # feedparser levert de tijd al in UTC. calendar.timegm leest hem ook als
    # UTC; time.mktime zou hem als lokale tijd lezen en is op een Nederlandse
    # pc dan 1 a 2 uur verschoven (relevant voor het 24-uursblok).
    return datetime.fromtimestamp(calendar.timegm(struct_time), tz=timezone.utc)


# --------------------------------------------------------------------------
# RSS-bronnen
# --------------------------------------------------------------------------
def haal_rss(bron: dict) -> list:
    items = []
    grens = _grens()
    # feedparser gebruikt requests-achtige headers via agent-parameter niet
    # altijd; we halen zelf op voor betrouwbare user-agent.
    try:
        resp = requests.get(bron["url"], headers=HEADERS, timeout=TIMEOUT)
        resp.raise_for_status()
        feed = feedparser.parse(resp.content)
    except Exception as e:
        print(f"  [waarschuwing] {bron['naam']} niet bereikbaar: {e}")
        return items

    for entry in feed.entries:
        datum = _struct_naar_dt(
            getattr(entry, "published_parsed", None)
            or getattr(entry, "updated_parsed", None)
        )
        # Items zonder datum slaan we over: met "nu" als datum zouden ze
        # elke dag opnieuw in het 24-uursblok verschijnen.
        if datum is None or datum < grens:
            continue
        titel = getattr(entry, "title", "").strip()
        samenvatting = _schoon(
            getattr(entry, "summary", "") or getattr(entry, "description", "")
        )
        if bron.get("filter_op_trefwoord") and not _bevat_trefwoord(titel, samenvatting):
            continue
        items.append({
            "bron": bron["naam"],
            "categorie": bron["categorie"],
            "titel": titel,
            "samenvatting": samenvatting,
            "url": getattr(entry, "link", ""),
            "datum": datum,
        })
    return items


# --------------------------------------------------------------------------
_TRACKING_PARAMS = {"fbclid", "gclid", "mc_cid", "mc_eid", "ref", "source"}


def _sleutel_url(url: str) -> str:
    """Link zonder trackingparameters (utm_... en dergelijke), #-anker, slash
    aan het eind en hoofdletters. Overige parameters blijven staan: sommige
    bronnen zetten daar het eigenlijke adres in, zoals Rechtspraak.nl
    (details?id=ECLI:...)."""
    delen = urlsplit((url or "").strip())
    query = sorted(
        (k, v) for k, v in parse_qsl(delen.query, keep_blank_values=True)
        if not k.lower().startswith("utm_") and k.lower() not in _TRACKING_PARAMS
    )
    pad = delen.path.rstrip("/")
    return f"{delen.netloc}{pad}?{urlencode(query)}".lower()


def _sleutel_titel(titel: str) -> str:
    return re.sub(r"\s+", " ", (titel or "")).strip().lower()


def ontdubbel(items: list) -> list:
    """Haalt dubbele berichten weg: zelfde link of zelfde titel telt als dubbel.

    Het eerste exemplaar blijft staan. Omdat verzamel_alles de bronnen ophaalt
    in de volgorde van RSS_BRONNEN in config.py, bepaalt die volgorde welke bron
    voorrang krijgt, ook als de dubbelen in verschillende categorieën vallen.
    Het bericht verschijnt dan alleen in de categorie van de bron die wint.
    """
    gezien_url, gezien_titel, uniek = set(), set(), []
    for item in items:
        u, t = _sleutel_url(item["url"]), _sleutel_titel(item["titel"])
        if (u and u in gezien_url) or (t and t in gezien_titel):
            print(f"  [dubbel overgeslagen] {item['bron']}: {item['titel'][:80]}")
            continue
        if u:
            gezien_url.add(u)
        if t:
            gezien_titel.add(t)
        uniek.append(item)
    return uniek


def verzamel_alles() -> list:
    alles = []
    for bron in config.RSS_BRONNEN:
        print(f"Ophalen: {bron['naam']} ...")
        alles.extend(haal_rss(bron))
    # Dubbelen eruit (vóór het sorteren, zodat de bronvolgorde uit config.py
    # bepaalt welk exemplaar blijft).
    alles = ontdubbel(alles)
    # Sorteer nieuwste eerst.
    alles.sort(key=lambda x: x["datum"], reverse=True)
    return alles
