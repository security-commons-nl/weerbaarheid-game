# Plan: Weerbaarheids-dashboard Leiden
## Fundament voor de HTML-tool
*Versie 1.2 — 26 maart 2026 — bypass-keten, preventieve satellieten, responsieve layout, ketenstappen per dienst*

---

## 1. Wat willen we bereiken

**Het politieke doel:**
Bestuurders (DT en College van B&W) moeten na het zien van dit dashboard één ding voelen: als er nu een incident is, staat Leiden stil. En: dat is een keuze, geen noodlot.

De tool is geen informatiedashboard. Het is een beslissingsgereedschap. Het doel is dat uit de presentatie van 21 april 2026 een concrete uitkomst volgt: commitment voor budget en mandate voor het programma MWeV.

**Het concrete argument dat de tool maakt:**
Gemeente Leiden levert diensten aan inwoners. Die diensten hangen af van systemen. Die systemen hebben zwakke schakels. Als één schakel uitvalt, stoppen alle tandwielen. Er is op dit moment geen herstelplan. Disaster Recovery = DEFECT. Dit is de huidige toestand. Het programma Maatschappelijke Weerbaarheid herstelt dit — maar alleen als er beslissing en budget zijn.

**Wat de tool dus NIET is:**
- Geen technische documentatie voor IT-afdeling
- Geen volledig overzicht van alle maatregelen
- Geen risicoregister
- Geen projectpresentatie

---

## 2. Doelgroep

**Primair:** College van B&W, DT — bestuurders die sturen op diensten en resultaten, niet op IT of security.

**Hun taal:**
- "Wat betekent dit voor inwoners?"
- "Wat kost het als we niets doen?"
- "Wat verwachten we van onszelf?"

**Hun blinde vlekken:**
- Ze weten niet wat DR is
- Ze denken dat IT "geregeld is"
- Ze voelen urgentie pas als het concreet is — een dienst, een naam, een inwoner

**Wat ze moeten kunnen:** In 3 minuten zelfstandig een dienst kiezen, een incident simuleren, en begrijpen waarom het fout gaat.

---

## 3. Hoe moet het aanvoelen

**Toon:** Serieus, kalm, professioneel — maar met een scherpe ondertoon. Geen paniek, wel urgentie. De tool toont de realiteit; de realiteit is schokkend genoeg.

**Interactie:** Zelf ontdekken werkt harder dan verteld worden. De bestuurder klikt zelf op "start incident" en ziet zelf de tandwielen stoppen. Dat is politiek effectiever dan een slide met bullets.

**Tempo:** Langzaam genoeg om te begrijpen, snel genoeg om het gevoel te houden.

**Stijl:** Gemeente Leiden huisstijl (clean, professioneel) — geen gamification, geen alarmsirenes. Wel een duidelijk kleurcontrast tussen "werkt" en "staat stil".

**Gevoel na gebruik:** "Dit is serieus. Hier moet een beslissing over komen."

---

## 4. Structuur — de drie lagen van de tool

### Laag 1: Overzicht (landingspagina)
Een enkelvoudig scherm met 5 diensten als keuzekaarten. Elke kaart toont:
- Naam van de dienst (in burgers-taal: "Paspoort aanvragen", niet "GBA-koppeling")
- Huidige weerbaarstatus: rood/oranje/groen bolletje (uit de nulmeting)
- Eén korte zin: wat de inwoner merkt als het misgaat

Doel: de bestuurder herkent iets ("paspoort — dat snap ik") en klikt.

---

### Laag 2: Ketenscherm (per dienst)
De kern van de tool. Toont de keten van systeem → dienst → inwoner als tandwielanimatie.

**Elementen:**
- Klein tandwiel = kritieke afhankelijkheid (SPOF) — bijv. SCADA, BRP, Suite4SD
- Middelgroot tandwiel = interne dienst — bijv. informatievoorziening, datacenter
- Groot tandwiel = publieke dienst — bijv. drinkwater, uitkering
- Eindpunt = de inwoner (icoon + tekst: "Uw paspoort is beschikbaar")

**Twee knoppen:**
1. [Simuleer incident] — het kleine tandwiel stopt, alles stopt
2. [Activeer DR] — het reservetandwiel springt in (grijs → groen)

**Standaardtoestand:** DR-tandwiel is grijs en doorgestreept: "NIET BESCHIKBAAR". Dat is de huidige werkelijkheid.

**Na incident zonder DR:** Eindpunt toont rood, tekst: "Uw paspoort is NIET beschikbaar. Geen alternatief."

**Na incident mét DR (als het er was):** Keten herstart langzaam. Eindpunt: "Uw paspoort is beschikbaar via noodprocedure."

---

### Laag 3: Totaalscherm (voor college-presentatie)
Alle 5 diensten tegelijk als compact grid. Elke dienst heeft een statusbol. Knop: [Incident in de stad] — alle rode diensten gaan tegelijk op rood. Toont wat er simultaan misgaat.

Dit is het "what if"-scherm: wat als er een echte crisis is? Niet één dienst — meerdere tegelijk.

---

## 5. Visuele taal

**Kleurpalet:**

| Status            | Kleur                  | Betekenis                    |
|-------------------|------------------------|------------------------------|
| Normaal/draaiend  | #2ecc71 groen          | Keten functioneert           |
| Kwetsbaar         | #f39c12 oranje         | Afhankelijkheid zonder backup|
| Gestopt/incident  | #e74c3c rood           | Dienst niet beschikbaar      |
| DR defect         | #95a5a6 grijs + streep | Herstel niet mogelijk        |
| DR actief         | #27ae60 donkergroen    | Noodprocedure draait         |

**Typografie:** Clean sans-serif, grote koppen voor diensten, kleine labels voor systemen.

**Tandwielen:** SVG, CSS-animatie (rotation). Draaien = gezond. Stoppen = probleem. Reserve-tandwiel staat naast de keten, licht transparant. Wordt opaque + gaat draaien als geactiveerd.

**Stressbar (optioneel):** Een horizontale balk die oploopt bij incident. Label: "Belasting op crisisorganisatie". Werkt zonder uitleg.

**Niet gebruiken:** infografieken, tabellen, bullets, technische termen. Als een term uitgelegd moet worden, heet het iets anders.

---

## 6. Datamodel — per dienst

Elke dienst heeft hetzelfde schema:

```
dienst:
  naam: "Drinkwater leveren"
  bevolkingsimpact: "~125.000 inwoners zonder drinkwater"
  spof:
    naam: "SCADA-besturing"
    type: "industrieel besturingssysteem"
    leverancier: extern
  keten:
    - stap: "Sensor meet waterdruk"
    - stap: "SCADA stuurt pompstation"
    - stap: "Water bereikt huishouden"
  dr_status: DEFECT
  nulmeting_kleur: ROOD
  bcm_kritiek: JA
  intern_dossierhouder: [naam]
  scenario_tekst: "Bij uitval SCADA: geen drinkwater. Geen noodprocedure beschikbaar."
```

Dit datamodel vult de animatie. Alles is vervangbaar zonder de HTML te herschrijven.

---

## 7. De 9 diensten — ketenstappen, SPOF en maatregelen

Status gebaseerd op: *Status BCM - DT.pdf*, *Rapportage Security IV feb 2026*, *Nulmeting weerbaarheid Q1 2026*, *Werkdocument MWeV*.

Elke dienst heeft 5 processtappen (k0–k4). SPOF staat altijd op k2. Maatregelen zijn reactief (bypass-keten) of preventief (satelliet op host-stap).

| Dienst | k0 | k1 | **k2 / SPOF** | k3 | k4 |
|--------|----|----|----------------|----|----|
| Crisis-alert | Meldkamer | Alertsysteem | **Telecomnetwerk** | NL-Alert platform | Inwoner bereikt |
| Noodsteunpunten | Crisiscoördinator | Noodprotocol | **Locatiesysteem** | Activering noodpunten | Opvang operationeel |
| Lokale zorg | Zorgvraag | Intake | **WMO-systeem** | Zorgtoewijzing | Zorg aan huis |
| Drinkwater | Druksensor | Pompgemaal | **SCADA-besturing** | Waterbehandeling | Kraan thuis |
| Uitkering | Klantmanager | Aanvraag | **Suite4SD (datacenter)** | BNG-koppeling | Betaling ontvangen |
| Afval | Vuilniswagen | Chipscanner | **Tag-systeem IT** | Routeplanning | Verwerking & Storten |
| Paspoort | Baliemedewerker | ID-verificatie | **BRP-koppeling** | Drukker | Paspoort uitgifte |
| Crisisbeheersing | Burgemeester/GBT | Crisismelding | **Crisisruimte + Comms** | Coördinatiebesluit | Hulpdiensten actief |
| Informatievoorziening | Gemeentelijk personeel | Werkplek | **M365 & Netwerk** | Applicatielaag | Dienstverlening |

| Dienst | Reactief 1 | Reactief 2 | Preventief (host) |
|--------|-----------|-----------|-------------------|
| Crisis-alert | Sirenes & omroep 🟡 | NCV backup 🟡 | Crisiscomm. protocol 🔴 (k0) |
| Noodsteunpunten | VRHM pilot 🟡 | Papieren lijst 🔴 | Voorraadbeheer 🔴 (k4) |
| Lokale zorg | Papieren dossiers 🔴 | WMO uitwijk 🔴 | BCM zorgketen 🔴 (k0) |
| Drinkwater | UPS noodvoeding 🟡 | Handmatige bediening 🔴 | OT/SCADA beveiliging 🔴 (k2) |
| Uitkering | Handmatige overmaking 🔴 | Uitwijklocatie 🔴 | BCM-plan Sociaal 🔴 (k0) |
| Afval | Analoge registratie 🔴 | Noodrooster 🔴 | Backup tag-systeem 🔴 (k4) |
| Paspoort | Tijdelijk reisdoc. 🟡 | Rijksfallback 🟡 | Continuïteitsplan 🔴 (k4) |
| Crisisbeheersing | Uitwijklocatie GBT 🔴 | GRIP-protocol 🟡 | Oefenprogramma 🔴 (k0) |
| Informatievoorziening | DR-omgeving 🔴 | Backup-procedures 🟡 | Uitwijkomgeving 🔴 (k4) |

🟡 = in ontwikkeling / gedeeltelijk beschikbaar — bypass-schakel activeerbaar
🔴 = niet beschikbaar / geen actief plan — bypass-schakel permanent gebroken

**Bypass-logica:** bypass werkt alleen als ALLE reactieve schakels oranje + actief zijn. Eén defecte schakel breekt de bypass permanent. Zorg, Uitkering en Afval hebben GEEN werkende bypass — het sterkste politieke argument.

**Bronverantwoording:**
- BCM = DEFECT voor alle gemeentelijke processen: *Status BCM - DT.pdf* (IDA-cluster, geen werkende DR, nooit getest, continuïteitsplan terug naar concept)
- Crisisruimte verwijderd uit stadhuis, geen vervanging vastgesteld
- UPS drinkwater: technisch aanwezig, niet getest onder crisisomstandigheden
- VRHM-pilot noodsteunpunten: loopt (Leiden deelnemend)
- Tijdelijk reisdocument / Rijksfallback paspoort: wettelijke procedure bestaat
- GRIP-protocol: bestaat op papier, niet recent geoefend

**Bronverantwoording:**
- BCM = DEFECT voor alle gemeentelijke processen: *Status BCM - DT.pdf* (IDA-cluster, geen werkende DR, nooit getest, continuïteitsplan terug naar concept)
- Crisisruimte verwijderd uit stadhuis, geen vervanging vastgesteld
- UPS drinkwater: technisch aanwezig, niet getest onder crisisomstandigheden
- VRHM-pilot noodsteunpunten: loopt (Leiden deelnemend)
- Tijdelijk reisdocument / Rijksfallback paspoort: wettelijke procedure bestaat
- GRIP-protocol: bestaat op papier, niet recent geoefend
- Backup-procedures M365: aanwezig, maar herstelplannen ontbreken (*Status BCM - DT.pdf*)

---

## 8. Gebruik in presentatie

**Standalone (Francine presenteert):**
Volledig scherm in browser. Francine kiest een dienst, loopt door de animatie, klikt incident, toont het grijze DR-tandwiel. Geen tekst nodig — de tool spreekt.

**Zelfgestuurd (DT/College klikt zelf):**
Op een tablet of laptop kunnen deelnemers zelf klikken. Verhoogt betrokkenheid en levert "aha-momenten" op.

**Exporteren (optioneel v2):**
Printknop genereert A4-overzicht per dienst: status, SPOF, scenario. Als bijlage bij collegevoorstel.

---

## 9. Wat dit NIET bevat (bewuste keuzes)

- Geen login of gebruikersbeheer — presentatietool, geen systeem
- Geen live data-koppelingen — data is hardcoded; actualiseren is handmatig
- Geen volledige nulmeting — de tool toont de conclusie, niet de matrix
- Geen financiële getallen in de tool zelf — die horen in het collegevoorstel
- Geen mobiele optimalisatie (v1) — werkt op laptop/projector

---

## 10. Huidige implementatiestatus (v3, 26 mrt 2026)

`weerbaarheid-dashboard.html` is volledig geïmplementeerd conform dit plan.

**Wat werkt:**
- 3 schermen (pijlers → diensten → machine), breadcrumb navigatie
- 9 diensten met echte processtappen in burgerstaal (k0–k4)
- SVG-tandwielen met berekende tanden (`gearPath()`)
- Tandwielen grijpen visueel in elkaar (meshing via centrum-tot-centrum berekening)
- Responsieve layout: gear-groottes en posities schalen mee met stage-breedte
- Bypass-keten van reactieve maatregelen onder de SPOF
- Preventieve satelliet-gears boven host-gear (koud blauw)
- Combinatielogica: bypassComplete / bypassPartial / bypassBroken / PLAT
- Legenda: "X van Y maatregelen actief (N defect)"
- Stressbar daalt bij NOODPROCEDURE, stijgt snel bij PLAT

**Nog niet gebouwd:**
- Laag 3: totaalscherm (alle 9 diensten tegelijk, "Incident in de stad"-knop)
- Printexport per dienst

---

*Versie 1.2 — 26 maart 2026*
