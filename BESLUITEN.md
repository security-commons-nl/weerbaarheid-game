# Besluiten

Append-only. Datum, besluit, een zin onderbouwing. Nieuwste bovenaan.

- **2026-10-30 · De rekenregels hebben een referentie-implementatie.** `reken.py` legt effectiviteit, totaal,
  voorbereiding en uitkomst vast; `tests/test_reken.py` vergelijkt hem met het echte script over alle scenario's
  (ruim 20.000 gevallen). Reden: de lat (C5) vraagt een referentie met tests; daarmee is ook het laatste open punt
  van de vorige regel dicht. Getoetst dat de vergelijking echt vergelijkt: een drempel van 31 in plaats van 30
  laat 910 gevallen falen.
- **2026-10-29 · De game haalt als eerste de lat van het redactiestatuut (C5).** Kruimelpad, versie en status
  op de pagina, een link naar de tests in CI, en de stand als bestand van de gebruiker (opslaan en laden,
  getoetst in `tests/test_stand.py`). Reden: hij staat op de bestuurdersroute van de voorpagina en was het
  instrument met de minste toetsbaarheid (plan *de site is het product*, 29-10-2026). De
  referentie-implementatie van de rekenregels volgde op 30-10 (zie boven).
- **2026-09-03 · De naam blijft `weerbaarheid-game`, de ondertitel wordt scherper.** "Game" belooft een
  spel terwijl dit een gespreksinstrument is, maar de repo wordt op 23 plekken buiten zijn eigen map
  genoemd en de URL wordt gebruikt in bestuursgesprekken; een dode link bij een bestuurder weegt zwaarder
  dan een naam die net niet klopt. Op de pagina en in de projectentabel heet hij voortaan
  *weerbaarheidsgame, gespreksinstrument voor college en directie*. Hernoemen kan alsnog bij de
  oplevering van v2, met een redirect vanaf het oude pad.
- **2026-09-03 · De voorbeeldcijfers blijven, maar zichtbaar als voorbeeld, en je eigen organisatie
  begint leeg.** Een demonstratie met alles op onbekend maakt geen gesprek los; tegelijk mag niemand per
  ongeluk de cijfers van een andere organisatie aan zijn college tonen. De meegeleverde set draagt een
  balk *voorbeeldcijfers, maart 2026*, en zodra je een organisatienaam invult staat alles op onbekend,
  met een knop om de voorbeeldcijfers bewust over te nemen.
- **2026-09-03 · Er komen drie diensten bij: belastingen en invordering, vergunningen en toezicht,
  verkiezingen.** Na uitkering en paspoort raken die de meeste inwoners, en verkiezingen zijn periodiek
  onvermijdelijk en politiek zichtbaar. Daarmee komt de game op twaalf diensten.
- **2026-09-03 · v2 haalt de inhoud uit de code naar `spel.json`.** De negen diensten en al hun statussen
  staan hard in 4.239 regels HTML, dus een andere organisatie kan de game niet met eigen cijfers draaien.
  Het plan staat in `.github/plannen/2026-09-03-weerbaarheid-game-v2.md`.
