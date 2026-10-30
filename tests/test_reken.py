"""reken.py is de referentie van de rekenregels; de game moet er overal mee overeenkomen (redactiestatuut C5).

tests/harnas.mjs draait het echte script uit weerbaarheid-game.html buiten de browser, over elk scenario, elke
combinatie van voorbereidingen (tot het maximum dat de game toestaat), elke inzet van reactieve maatregelen en elke
complicatie. Deze test rekent dezelfde gevallen na met reken.py en eist een gelijke uitkomst: de maatregelen na de
voorbereiding, de versterkte schakels, het totaal en de status die de game toont.

    python -m pytest tests/test_reken.py -v

Node is nodig (in CI standaard aanwezig). Zonder node faalt de test: een vergelijking die stil wordt overgeslagen,
bewijst niets.
"""
from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
import reken  # noqa: E402


@pytest.fixture(scope="module")
def uitkomsten() -> dict:
    node = shutil.which("node")
    assert node, "node ontbreekt; de vergelijking met de game kan niet draaien"
    r = subprocess.run([node, str(REPO / "tests" / "harnas.mjs")], capture_output=True, text=True, encoding="utf-8", check=False)
    assert r.returncode == 0, r.stderr[-2000:]
    return json.loads(r.stdout)


def _kern(maatregelen: list[dict]) -> list[tuple]:
    return [(m["id"], m.get("type"), m.get("status"), m.get("effectiviteit")) for m in maatregelen]


def test_het_harnas_dekt_alle_scenarios_en_uitkomsten(uitkomsten):
    assert len(uitkomsten["scenarios"]) >= 15
    assert len(uitkomsten["gevallen"]) > 5000
    statussen = {g["status"] for g in uitkomsten["gevallen"]}
    assert statussen == {"NOODPROCEDURE", "GEDEELTELIJK", "SYSTEEM PLAT"}, statussen
    assert any(g["combo"] for g in uitkomsten["gevallen"]), "geen enkele voorbereiding meegenomen"
    assert any(g["ov"] for g in uitkomsten["gevallen"]), "geen enkele complicatie meegenomen"


def test_voorbereiding_geeft_dezelfde_maatregelen(uitkomsten):
    verschil = []
    gezien = set()
    for g in uitkomsten["gevallen"]:
        sleutel = (g["dienst"], g["idx"], tuple(g["combo"]))
        if sleutel in gezien:
            continue
        gezien.add(sleutel)
        sc = uitkomsten["scenarios"][f'{g["dienst"]}#{g["idx"]}']
        opties = {o["id"]: o for o in (sc["prep"] or {}).get("opties", [])}
        # In de volgorde van de lijst in de game, niet van de klikvolgorde: zo past de game ze ook toe.
        effecten = [o.get("effect") for oid, o in opties.items() if oid in g["combo"]]
        na, versterkt = reken.pas_voorbereiding_toe(sc["basis"], effecten)
        if _kern(na) != _kern(g["naPrep"]) or versterkt != set(g["versterkt"]):
            verschil.append(sleutel)
    assert not verschil, f"{len(verschil)} voorbereidingen anders dan de game, bijvoorbeeld {verschil[:3]}"


def test_totaal_en_status_gelijk_aan_de_game(uitkomsten):
    verschil = []
    for g in uitkomsten["gevallen"]:
        actief = set(g["actief"])
        eff = reken.totaal(g["naPrep"], actief, g["ov"])
        status = reken.uitkomst(g["naPrep"], actief, g["ov"])
        if eff != g["eff"] or status != g["status"]:
            verschil.append((g["dienst"], g["idx"], g["combo"], g["actief"], g["ov"], eff, g["eff"], status, g["status"]))
    assert not verschil, f"{len(verschil)} gevallen anders dan de game, bijvoorbeeld {verschil[:3]}"


def test_zonder_incident_operationeel(uitkomsten):
    assert all(z["status"] == "OPERATIONEEL" for z in uitkomsten["zonder"])
    assert reken.uitkomst([], set(), incident=False) == "OPERATIONEEL"


# De regels zelf, los van de game.
M = [{"id": "m1", "type": "reactief", "status": "oranje", "effectiviteit": 50},
     {"id": "m2", "type": "reactief", "status": "oranje", "effectiviteit": 60},
     {"id": "m3", "type": "reactief", "status": "defect", "effectiviteit": 0},
     {"id": "m4", "type": "preventief", "status": "defect", "effectiviteit": 0}]


def test_totaal_heeft_een_plafond_van_85():
    assert reken.totaal(M, {"m1", "m2"}) == 85


def test_niets_ingezet_is_nul_en_preventief_telt_niet():
    assert reken.totaal(M, set()) == 0
    assert reken.totaal(M, {"m4"}) == 0


def test_complicatie_overschrijft_de_effectiviteit():
    assert reken.totaal(M, {"m1"}, {"m1": 20}) == 20
    assert reken.uitkomst(M, {"m1"}, {"m1": 20}) == "GEDEELTELIJK"


def test_drempel_van_30_voor_de_noodprocedure():
    assert reken.uitkomst(M, {"m1"}, {"m1": 30}) == "NOODPROCEDURE"
    assert reken.uitkomst(M, {"m1"}, {"m1": 29}) == "GEDEELTELIJK"


def test_alleen_een_defecte_maatregel_ingezet_is_plat():
    assert reken.uitkomst(M, {"m3"}) == "SYSTEEM PLAT"


def test_ontgrendelen_en_versterken():
    na, _ = reken.pas_voorbereiding_toe(M, [{"type": "unlock", "target": "m3", "baseEff": 25},
                                            {"type": "boost", "target": "m1", "bonus": 50}])
    m = {x["id"]: x for x in na}
    assert m["m3"]["status"] == "oranje" and m["m3"]["effectiviteit"] == 25
    assert m["m1"]["effectiviteit"] == 85
    assert M[2]["status"] == "defect", "de invoer mag niet veranderen"


def test_ontgrendelen_raakt_een_oranje_maatregel_niet():
    na, _ = reken.pas_voorbereiding_toe(M, [{"type": "unlock", "target": "m1", "baseEff": 10}])
    assert {x["id"]: x for x in na}["m1"]["effectiviteit"] == 50


def test_een_schakel_versterken():
    _, versterkt = reken.pas_voorbereiding_toe(M, [{"type": "node-resilience", "target": "k2"}])
    assert versterkt == {"k2"}
