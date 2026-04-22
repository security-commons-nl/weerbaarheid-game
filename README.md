# Weerbaarheids-dashboard

> Interactief beslissingsgereedschap dat de kwetsbaarheid van gemeentelijke dienstverlening zichtbaar maakt voor bestuurders.


[![Bijdragen](https://img.shields.io/badge/📝_Bijdragen-Open_een_bericht-238636?style=for-the-badge)](../../issues/new/choose)&nbsp;&nbsp;&nbsp;&nbsp;[![Discussions](https://img.shields.io/badge/💬_Discussions-Meepraten-0969da?style=for-the-badge)](../../discussions)

👉 **Iets delen, feedback geven of een vraag stellen?** Klik op een van de knoppen hierboven — geen Git-ervaring nodig. Zie [CONTRIBUTING.md](CONTRIBUTING.md) voor meer opties.

---

## Wat is het?

Het weerbaarheids-dashboard is een op zichzelf staande HTML-tool die de keten van kritieke gemeentelijke diensten simuleert als tandwielanimaties. Bestuurders (directie, college van B&W) kunnen:

- Een dienst kiezen (uitkering, drinkwater, paspoort, crisis-alert, etc.)
- Een incident simuleren en zien welke tandwielen stoppen
- De aanwezigheid (of afwezigheid) van herstelmaatregelen (DR) zien
- Begrijpen wat inwoners merken als een dienst uitvalt

Het is geen technisch dashboard en bevat geen live data. Het is een **presentatiegereedschap** voor bestuurlijke besluitvorming over weerbaarheid en continuïteit.

---

## Snel starten

Geen installatie nodig. Open het bestand in een browser:

```bash
# Optie 1: Direct openen
open weerbaarheid-game.html

# Optie 2: Via lokale webserver (aanbevolen voor presentaties)
python -m http.server 8080
# Open http://localhost:8080/weerbaarheid-game.html
```

Het werkt op elke moderne browser. Geoptimaliseerd voor volledig scherm op laptop of beamer.

---

## Structuur

De tool heeft drie schermen:

1. **Pijlers** — overzicht van de drie weerbaarheidslagen (preventie, detectie, herstel)
2. **Diensten** — keuze uit 9 gemeentelijke diensten met weerbaarstatus
3. **Machine** — ketanimatie per dienst met incident-simulatie

---

## Aanpassen voor je organisatie

De diensten en hun ketenstappen zijn hardcoded in de HTML. Om de tool aan te passen aan je eigen organisatie:

1. Open `weerbaarheid-game.html` in een editor
2. Zoek de `services`-array (~regel 200)
3. Pas diensten, ketenstappen, SPOF-beschrijvingen en DR-status aan
4. Test lokaal voor gebruik in presentaties

---

## Bijdragen

Zie [CONTRIBUTING.md](https://github.com/security-commons-nl/.github/blob/main/CONTRIBUTING.md) voor de spelregels. Heb je de tool aangepast voor je eigen gemeente en wil je die aanpassing delen? Open een issue of pull request.

---

## Meer documentatie

- [Gebruik](docs/gebruik.md) — hoe je de tool gebruikt in een presentatie
- [Architectuur](docs/architectuur.md) — hoe de tool technisch is opgebouwd
---

## Principes

Dit project volgt de [architectuur- en communityprincipes](https://github.com/security-commons-nl/.github/blob/main/PRINCIPLES.md) van security-commons-nl: EU-soevereiniteit, AI altijd adviserend, auditbaarheid by design, least privilege en open source als standaard.
