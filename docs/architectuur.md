# Weerbaarheids-dashboard — Architectuur

> Voor contributors die de tool willen aanpassen of uitbreiden.

---

## Opzet

De tool is een **single-file HTML-applicatie**. Geen build-stap, geen dependencies, geen backend. Alles — HTML, CSS, JavaScript en data — zit in `weerbaarheid-game.html`.

Dit is bewust: de tool moet werken zonder installatie, ook offline, ook op een laptop zonder internet.

---

## Structuur van de HTML

```
weerbaarheid-game.html
├── <style>          CSS (inline, TailwindCSS-achtige utility classes + custom)
├── <script>
│   ├── Data         services-array met alle dienstdefinities
│   ├── State        huidige dienst, scherm, incident-status
│   ├── Render       functies die het DOM opbouwen per scherm
│   ├── Animation    tandwiel-rotatie via CSS transforms
│   └── Events       click handlers voor knoppen en navigatie
└── <body>           Drie schermen (pijlers / diensten / machine)
```

---

## Datamodel

Elke dienst heeft hetzelfde schema:

```javascript
{
  naam: "Paspoort aanvragen",
  bevolkingsimpact: "~125.000 inwoners",
  keten: [
    { stap: "Baliemedewerker", type: "normaal" },
    { stap: "ID-verificatie", type: "normaal" },
    { stap: "BRP-koppeling", type: "spof" },    // zwakke schakel
    { stap: "Drukker", type: "normaal" },
    { stap: "Paspoort uitgifte", type: "normaal" }
  ],
  reactief: [
    { naam: "Tijdelijk reisdocument", status: "oranje" },
    { naam: "Rijksfallback", status: "oranje" }
  ],
  preventief: { naam: "Continuïteitsplan", status: "rood", host_stap: 4 },
  dr_status: "DEFECT",
  nulmeting_kleur: "rood"
}
```

**Status-waarden:**
- `groen` — maatregel aanwezig en actief
- `oranje` — in ontwikkeling of gedeeltelijk beschikbaar
- `rood` — niet beschikbaar, geen actief plan

**Bypass-logica:** een bypass werkt alleen als ALLE reactieve maatregelen `oranje` of `groen` zijn. Eén `rood` breekt de bypass permanent.

---

## Tandwielanimaties

Tandwielen zijn SVG-elementen met berekende tanden (`gearPath()`-functie). De rotatie-animatie loopt via CSS `transform: rotate()` updates in een `requestAnimationFrame`-loop.

Tandwielen "grijpen in elkaar" via centrum-tot-centrum berekening: de rotatiesnelheid van elk tandwiel is omgekeerd evenredig aan zijn diameter, zodat de tanden synchroon bewegen.

Bij een incident (`simuleerIncident()`):
1. Alle tandwiel-rotaties stoppen
2. De SPOF-kleur verandert naar rood
3. Alle downstream tandwielen worden ook rood
4. Het DR-tandwiel blijft grijs + doorgestreept

---

## Aanpassen

**Diensten toevoegen of wijzigen:** zoek de `const services = [...]`-array en voeg een object toe of pas een bestaand object aan. Het datamodel hierboven is leidend.

**Kleuren aanpassen:** CSS-variabelen staan bovenin de `<style>`-sectie. Pas `--kleur-groen`, `--kleur-rood`, `--kleur-oranje` aan voor je eigen huisstijl.

**Nieuwe schermen toevoegen:** de render-engine werkt met een `currentScreen`-state. Voeg een nieuwe case toe aan de `renderScreen()`-functie en een knop in de navigatie.

---

## Bewuste beperkingen

- **Geen externe dependencies** — geen npm, geen CDN. Werkt offline.
- **Geen live data-koppelingen** — data is hardcoded; actualiseren is handmatig.
- **Geen login** — presentatietool, geen systeem.
- **Geen mobiele optimalisatie** — ontworpen voor laptop/beamer.
