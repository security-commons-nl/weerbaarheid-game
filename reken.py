#!/usr/bin/env python3
"""Referentie-implementatie van de rekenregels van de weerbaarheidsgame (redactiestatuut C5).

De game rekent in de browser (`weerbaarheid-game.html`). Dit bestand legt dezelfde regels vast in leesbare vorm,
zodat ze te toetsen zijn zonder de pagina: `tests/test_reken.py` draait het echte script uit de pagina over alle
scenario's, voorbereidingen, maatregelen en complicaties, en eist dat deze referentie overal hetzelfde uitkomt.
Wie een regel verandert, verandert hem aan beide kanten.

De regels:
1. Effectiviteit van een maatregel: een complicatie kan hem overschrijven (bijvoorbeeld "diesel raakt op":
   van 50 naar 20 procent). Anders de waarde uit de data; ontbreekt die, dan 100.
2. Totaal: de effectiviteit van de ingezette reactieve maatregelen telt op, met een plafond van 85 procent.
   Niets ingezet is 0. Een noodoplossing haalt nooit de volledige dienstverlening terug.
3. Voorbereiding: een gekozen voorbereiding kan een maatregel ontgrendelen (defect wordt oranje, met een
   startwaarde), versterken (er komt een bonus bij, ook tot hoogstens 85) of een schakel weerbaarder maken.
4. Uitkomst bij een incident: noodprocedure als er minstens een oranje maatregel is ingezet en het totaal
   minstens 30 procent is; gedeeltelijk als er wel iets is ingezet maar onder die drempel; anders ligt het
   systeem plat. Zonder incident is de dienst operationeel.

Alleen standaardbibliotheek.
"""
from __future__ import annotations

import copy

PLAFOND = 85
DREMPEL = 30


def effectiviteit(maatregel: dict, overschrijving: dict | None = None) -> int:
    """Regel 1. `overschrijving` is {maatregel-id: waarde} na complicaties."""
    if overschrijving and overschrijving.get(maatregel["id"]) is not None:
        return overschrijving[maatregel["id"]]
    waarde = maatregel.get("effectiviteit")
    return 100 if waarde is None else waarde


def totaal(maatregelen: list[dict], actief: set[str], overschrijving: dict | None = None) -> int:
    """Regel 2."""
    ingezet = [m for m in maatregelen if m["type"] == "reactief" and m["id"] in actief]
    if not ingezet:
        return 0
    return min(PLAFOND, sum(effectiviteit(m, overschrijving) for m in ingezet))


def pas_voorbereiding_toe(maatregelen: list[dict], effecten: list[dict]) -> tuple[list[dict], set[str]]:
    """Regel 3. Geeft een nieuwe lijst maatregelen en de set versterkte schakels; de invoer blijft ongemoeid."""
    uit = copy.deepcopy(maatregelen)
    versterkt: set[str] = set()
    for effect in effecten:
        if not effect:
            continue
        doel = next((m for m in uit if m["id"] == effect.get("target")), None)
        if effect["type"] == "unlock":
            if doel and doel.get("status") == "defect":
                doel["status"] = "oranje"
                if effect.get("baseEff") is not None:
                    doel["effectiviteit"] = effect["baseEff"]
        elif effect["type"] == "boost":
            if doel:
                if doel.get("effectiviteit") is None:
                    doel["effectiviteit"] = 0
                doel["effectiviteit"] = min(PLAFOND, doel["effectiviteit"] + effect["bonus"])
        elif effect["type"] == "node-resilience":
            versterkt.add(effect["target"])
    return uit, versterkt


def uitkomst(maatregelen: list[dict], actief: set[str], overschrijving: dict | None = None,
             incident: bool = True) -> str:
    """Regel 4. Geeft de status die de game toont: OPERATIONEEL, NOODPROCEDURE, GEDEELTELIJK of SYSTEEM PLAT."""
    if not incident:
        return "OPERATIONEEL"
    reactief = [m for m in maatregelen if m["type"] == "reactief"]
    ingezet_oranje = [m for m in reactief if m.get("status") == "oranje" and m["id"] in actief]
    eff = totaal(maatregelen, actief, overschrijving)
    if eff >= DREMPEL and ingezet_oranje:
        return "NOODPROCEDURE"
    if ingezet_oranje:
        return "GEDEELTELIJK"
    return "SYSTEEM PLAT"
