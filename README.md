# BrightStone Group Nieuwsupdate

Een geautomatiseerde nieuwsbrief met actueel en relevante nieuwsartikelen en publicaties rondom Finance, Data, Risk en Compliance.

## Wat het doet

Elke werkdag (ma t/m vr, vroeg in de ochtend) haalt het script items op uit de
afgelopen 7 dagen. Bovenaan staan de berichten van de afgelopen 24 uur, nieuwste
eerst. Daaronder de overige berichten van de week, per categorie en binnen elke
categorie de nieuwste bovenaan. Een bericht staat maar op één plek.
Per item toont de nieuwsbrief een kort bericht van twee tot drie zinnen met een
link naar de bron.
Nieuwsitems worden gefilterd op trefwoorden die relevant zijn voor ons vakgebied. 
Mis je een nieuwsbron of -bericht? Laat het weten, en we voegen het toe!

## Handmatig draaien

Wil je niet wachten tot de volgende werkdag, ga dan naar het tabblad **Actions**, kies de workflow
*Dagelijkse nieuwsupdate* en klik op **Run workflow**. Na een minuut staat de nieuwe
editie online.

## Lokaal testen

Installeer eenmalig de benodigdheden en draai daarna de preview:

```
pip install -r requirements.txt
python src/preview.py
```

Dit haalt de echte RSS-bronnen op, net als de dagelijkse run, en opent het
resultaat (`src/preview.html`) in je browser. Er wordt niets gepubliceerd.
Wil je alleen de lay-out checken zonder internet, gebruik dan
`python src/preview.py --nep`.

## Waar staat de nieuwsupdate?

Op `https://lumengroup.github.io/bsg_nieuwsupdate/` staat de nieuwste editie.

## Let op

GitHub pauzeert de planner als een repository 60 dagen geen activiteit heeft.
Eén handmatige run of een kleine commit zet hem weer aan. De publieke bronnen kunnen hun
feed-URL wijzigen; als een bron leeg blijft, controleer dan de URL in `config.py`.

De samenstelling is geautomatiseerd. Controleer een bericht altijd bij de bron
voordat je die met een klant deelt.
