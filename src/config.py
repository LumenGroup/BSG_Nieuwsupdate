"""
Configuratie voor de BrightStone Group nieuwsbrief.
Alle instelbare waarden staan hier bij elkaar, zodat je niets in de logica hoeft aan te passen.
"""

# --- Tijdvenster ---------------------------------------------------------
# Aantal dagen terug dat als "nieuw" telt. Wekelijks = 7.
DAGEN_TERUG = 7

# --- Bronnen -------------------------------------------------------------

RSS_BRONNEN = [
    {
	    "naam": "Het Financiële Dagblad (FD)",
        "categorie": "Nieuws",
        "url": "https://fd.nl/?rss",
        "filter_op_trefwoord": True,
    },
    {
	    "naam": "Accountant.nl",
        "categorie": "Nieuws",
        "url": "https://www.accountant.nl/vaktechniek/?type=rss",
        "filter_op_trefwoord": True,
    },
    {
	    "naam": "FlexNieuws",
	    "categorie": "Nieuws",
	    "url": "https://www.flexnieuws.nl/feed/",
	    "filter_op_trefwoord": False,
    },
    {
	    "naam": "Verenigde Betaal Instellingen Nederland (VBIN)",
	    "categorie": "Brancheorganisatie",
	    "url": "https://www.vbin.nl/category/nieuws/feed/",
	    "filter_op_trefwoord": False,
    },
    {
	    "naam": "Vereniging van Compliance Professionals (VCO)",
	    "categorie": "Brancheorganisatie",
	    "url": "https://www.vco.nl/feed/",
	    "filter_op_trefwoord": False,
    },
    {
	    "naam": "Verenigde Bitcoinbedrijven Nederland (VBNL)",
	    "categorie": "Brancheorganisatie",
	    "url": "https://www.vbnl.org/feed/",
	    "filter_op_trefwoord": False,
    },
    {
	    "naam": "De Nederlandsche Bank (DNB)",
	    "categorie": "Centrale Bank",
	    "url": "https://www.dnb.nl/nl/rss/16451/6882",
	    "filter_op_trefwoord": True,
    },
    {
	    "naam": "Autoriteit Financiële Markten (AFM)",
        "categorie": "Toezichthouder (NL)",
        "url": "https://www.afm.nl/nl-nl/rss-feed/nieuws-professionals",
        "filter_op_trefwoord": False,
    },
    {
	    "naam": "Nederlandse Zorgautoriteit (NZA)",
	    "categorie": "Toezichthouder (NL)",
	    "url": "https://www.nza.nl/api/rss?query=%7B%22filters%22%3A%5B%5D%2C%22resultSearchTerm%22%3A%22%22%2C%22pageTitle%22%3A%22Zoeken%22%7D",
	    "filter_op_trefwoord": True,
    },
    {
	    "naam": "Financial Intelligence Unit-Nederland (FIU-Nederland)",
	    "categorie": "Toezichthouder (NL)",
	    "url": "https://www.fiu-nederland.nl/?feed=rss2",
	    "filter_op_trefwoord": False,
    },
    {
	    "naam": "Autoriteit Consument & Markt (ACM)",
	    "categorie": "Toezichthouder (NL)",
	    "url": "https://www.acm.nl/nl/nieuws/rss/publicaties?field_subjects=All&publication_type=All",
	    "filter_op_trefwoord": True,
    },
    {
	    "naam": "European Banking Authority (EBA)",
        "categorie": "Toezichthouder (EU)",
        "url": "https://eba.europa.eu/news-press/news/rss.xml",
        "filter_op_trefwoord": True,
    }
]

# --- Trefwoorden -------------------------------
# Een publicatie telt als relevant zodra één van deze termen als los woord (of
# woordgroep) voorkomt in de titel, samenvatting of inhoudsindicatie. Kleine
# letters; er wordt hoofdletterongevoelig vergeleken, met woordgrenzen (zie
# _bevat_trefwoord in collectors.py) zodat korte afkortingen niet per ongeluk
# matchen binnen een ander woord.
TREFWOORDEN_COMPLIANCE = [
    # bestaand
    "wwft", "aml", "amlr", "amld6", "anti-money laundering", "amla",
    "financial crime compliance", "klantonderzoek", "cdd", "ubo",
    "transactiemonitoring", "witwassen", "money laundering",
    "terrorismefinanciering", "terrorist financing",
    "sanctiewetgeving", "sanctielijst", "sanctions", "sanctions list",
    "wft", "dora", "nis2", "ai act", "dnb", "afm", "ecb",
    "gap analyse", "gap analysis", "compliance officer",
    # aanvullingen
    "sfdr", "eu taxonomie", "esg-rapportage",
    "wtp", "wet toekomst pensioenen",
    "eba", "esma", "eiopa",
    "crr", "crd", "crr3", "crd6",
    "basel", "basel iv",
    "mifid", "emir",
    "poortwachter", "poortwachtersfunctie",
    "financieel-economische criminaliteit", "fec",
    "fatf", "fiu", "fiu-nederland", "meldplicht", "ongebruikelijke transacties",
    "pep", "politically exposed person",
    "integriteitsrisico", "sira",
    "regtech", "suptech", "kifid",
    "kapitaalvereisten", "capital requirements",
    "depositogarantiestelsel", "deposit guarantee scheme",
    "securitisatie", "securitisation",
    "consumentenbescherming", "consumer protection",
    # "handhaving", "boete", "aanwijzing" en "toezicht" zijn bewust weggelaten:
    # dit zijn generieke woorden die in vrijwel elk artikel van een
    # toezichthouder voorkomen, ook bij NZa (zorg) en ACM (mededinging), en
    # zouden het trefwoordfilter voor die bronnen grotendeels uitschakelen.
]

TREFWOORDEN_RISK = [
    # bestaand
    "enterprise risk management", "erm", "risk appetite",
    "operationeel risico", "operational risk",
    "credit risk", "kredietrisico",
    "compliancerisico", "third party risk", "third-party risk",
    "uitbestedingsrisico", "uitbesteding", "outsourcing",
    "informatiebeveiliging", "cyberweerbaarheid", "cyberrisico",
    "datarisico", "ai risico", "ai-risico",
    "drielijnenmodel", "first line", "second line",
    "third line", "control testing", "root cause analysis", "incidentmanagement",
    # aanvullingen
    "orsa", "icaap", "ilaap", "irrbb", "bcbs 239",
    "modelrisico", "modelvalidatie", "model risk", "model validation",
    "liquiditeitsrisico", "marktrisico", "kapitaalrisico",
    "stresstest", "scenarioanalyse",
    "operationele weerbaarheid", "operational resilience",
    "business continuity", "bcm",
    "rcsa", "risk control self assessment",
    "key risk indicator", "kri",
    "risicoraamwerk", "risicobereidheid",
    "klimaatrisico", "esg-risico", "esg risk",
]

TREFWOORDEN_DATA = [
    # bestaand
    "datagovernance", "data governance", "dmbok", "datakwaliteit",
    "metadata management", "data lineage", "datacatalogus", "data-eigenaarschap",
    "data stewardship", "privacy-by-design", "data security", "analytics",
    "kunstmatige intelligentie", "artificial intelligence",
    # aanvullingen
    "avg", "gdpr", "autoriteit persoonsgegevens", "privacy",
    "datamanagement", "master data management", "mdm",
    "generatieve ai", "genai", "large language model", "llm", "machine learning",
    "eu ai act", "cloud", "databeheer", "data platform",
]

TREFWOORDEN_FINANCE = [
    # bestaand
    "financefunctie", "financial transformation", "financiele transformatie",
    "rapportage", "managementinformatie", "maandafsluiting", "procesverbetering",
    "kpi", "governance", "systeemimplementatie", "erp",
    # aanvullingen
    "ifrs", "ifrs 9", "ifrs 17", "consolidatie", "consolidation",
    "planning & control", "budgettering", "budgeting", "forecasting", "fp&a",
    "record to report", "r2r",
    "sap", "oracle", "power bi",
    "interne beheersing", "internal controls", "in control statement",
    "interne audit", "internal audit", "externe accountant",
    # "workday" is bewust weggelaten: dit is ook het gewone Engelse woord voor
    # "werkdag" en zou daardoor vooral ruis opleveren.
]

# Crypto en betaalinstellingen komen terug via VBNL en VBIN specifiek.
TREFWOORDEN_CRYPTO_PAYMENTS = [
    # bestaand
    "micar", "crypto-activa", "cryptoactiva", "bitcoin",
    "digitale euro", "digital euro",
    "betaalinstelling", "payment institution",
    "e-money", "elektronisch geld", "psd2", "psd3",
    # aanvullingen
    "stablecoin", "casp", "cryptodienstverlener",
    "instant payments", "verordening instant payments", "sepa",
    "open banking", "open finance", "fida",
    "eidas", "digitale identiteit", "digital identity",
    "digital identity wallet", "eudi wallet",
    "betaalfraude", "fraude", "fraud",
]

# Nieuw: arbeidsmarkt / inhuur. Direct relevant voor het eigen businessmodel
# (detachering van senioren) en een actueel thema in de sector.
TREFWOORDEN_ARBEIDSMARKT = [
    "wtta", "schijnzelfstandigheid", "zzp",
    "wet dba", "handhaving dba", "vbar", "wet vbar",
    "detachering", "uitzenden", "terbeschikkingstelling", "sna-keurmerk",
    "interim-inhuur", "inhuur", "arbeidsmarktkrapte", "interim",
]

TREFWOORDEN = (
    TREFWOORDEN_COMPLIANCE + TREFWOORDEN_RISK + TREFWOORDEN_DATA
    + TREFWOORDEN_FINANCE + TREFWOORDEN_CRYPTO_PAYMENTS
    + TREFWOORDEN_ARBEIDSMARKT
)

# --- Huisstijl BSG ----------------------------------------------
# Kleuren en fonts overgenomen uit brightstonegroup.nl (theme-instellingen en
# inline CSS): #0170b9 is het door BrightStone zelf ingestelde themakleur,
# #00a5e1 de knopkleur, #0a3a52 de kopkleur binnen de contentblokken.
HUISSTIJL = {
    "primair": "#0170b9",      # brightstone-blauw (links, knoppen, hover)
    "accent": "#0a3a52",       # donkerblauw (koppen)
    "tekst": "#3a3a3a",
    "tekst_zacht": "#575756",
    "achtergrond": "#ffffff",
    "vlak": "#f5f5f5",
    "lijn": "#e5e5e5",
    "kop_font": "'Coolvetica', Helvetica, Arial, sans-serif",
    "tekst_font": "'Roboto', Arial, sans-serif",
}

# Titel en subtitel van de nieuwsbrief.
NIEUWSBRIEF_TITEL = "BrightStone Group Nieuwsupdate"
NIEUWSBRIEF_SUBTITEL = "Wekelijkse update met nieuws en publicaties in Finance, Data, Risk & Compliance. Update elke maandagochtend. Website wordt niet gearchiveerd, oude versies kunnen worden opgeslagen door de HTML-code lokaal op je pc op te slaan (CTRL+S in de browser)."
