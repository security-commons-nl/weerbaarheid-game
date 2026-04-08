# Context: Programma Maatschappelijke Weerbaarheid en Veerkracht — Gemeente Leiden

## Wie
- **de CISO** — CISO Leiden/Leiderdorp/Oegstgeest/Zoeterwoude. Technisch sterk, werkt ook op bestuurlijk niveau.
- **Programmamanager MWeV**
- **Bestuurlijk opdrachtgever:** Burgemeester
- **Ambtelijk opdrachtgever:** Directeur Publiekszaken, Handhaving en Veiligheid

## Wat
Programma Maatschappelijke Weerbaarheid en Veerkracht (MWeV). Aanleiding: NCTV-brief aan alle burgemeesters 6 december 2024. Drie programmalijnen: Weerbare stad / Vitale basisvoorzieningen / Weerbare gemeente.

## Kernprobleem
Urgentiebesef ontbreekt intern. Budget voor uitvoering heeft nog geen dekking. BCM/DR bij alle vitale gemeentelijke processen: **DEFECT** (bevestigd in Status BCM-DT.pdf). Crisisruimte verwijderd uit stadhuis, geen vervanging.

## Mijlpaal
College-presentatie **21 april 2026**. Doel: commitment + budget + mandate.

## Bestanden in deze map
- `weerbaarheid-dashboard.html` — interactieve tandwiel-visualisatie voor DT/College (v3)
- `plan-dashboard.md` — volledig ontwerp- en specificatieplan met bronverantwoording (v1.1)
- `Werkdocument programma MWeV.pdf` — formeel werkdocument (versie 26 mrt 2026)
- `20260211 Verkenning weerbaar en veerkracht Leiden (nulmeting).pdf` — nulmeting Q1 2026

## Dashboard — huidige staat (v3, 26 mrt 2026)
3 schermen: pijlers → diensten → machine. 9 diensten over 3 pijlers.

Per dienst: **5-staps keten** met echte processtappen (burgerstaal, bijv. Baliemedewerker → ID-verificatie → BRP-koppeling → Drukker → Paspoort uitgifte). SPOF altijd op positie 3 (k2). Tandwielen grijpen visueel in elkaar (meshing via centrum-tot-centrum berekening). Responsief: schalen mee met stage-breedte.

**Maatregelen — twee typen:**
- 🔴/🟡 **Reactief** → vormen bypass-keten onder de SPOF. Bypass werkt alleen als ALLE schakels oranje + actief zijn. Defecte schakel breekt de bypass permanent.
- 🔴/🟡 **Preventief** → satelliet-tandwiel boven hun host-gear. Draaien mee als actief, raken de keten niet. Educatief/politiek argument.

**Combinatielogica:** bypassComplete → NOODPROCEDURE | bypassPartial → GEDEELTELIJK | geen/defect → SYSTEEM PLAT.

Status gebaseerd op echte brondocumenten (BCM-status, security rapportages, governance).

Zie `plan-dashboard.md` voor de volledige specificatie en bronverantwoording.

## Contextdocumenten (elders)
Interne brondocumenten: security rapportages, BIO2, BCM-status, governance, systeemanalyse, domeinschetsen.

## Toon en aanpak
- Burgerstaal, geen IT-jargon
- Visueel argument > tekstargument
- Binaire logica (werkt / werkt niet) is sterker dan gradaties
- Alles wat gebouwd wordt, dient de presentatie van 21 april
