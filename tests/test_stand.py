"""De lat (redactiestatuut C5): versie op de pagina, kruimelpad, en de stand als bestand van de gebruiker.

Opslaan levert een JSON-bestand met de keuzes; laden zet precies die keuzes terug in een verse pagina.
Zonder deze rondgang is "stand opslaan" een knop die een bestand maakt dat niemand kan terugzetten.

    python -m pytest tests/test_stand.py -v

Playwright met chromium is nodig; zonder slaat de test zichzelf over.
"""
from __future__ import annotations

import json
import pathlib
import re

import pytest

sync_api = pytest.importorskip("playwright.sync_api", reason="playwright niet beschikbaar")

REPO = pathlib.Path(__file__).resolve().parent.parent
BESTAND = REPO / "weerbaarheid-game.html"
SPEL = BESTAND.as_uri()


@pytest.fixture(scope="module")
def browser():
    with sync_api.sync_playwright() as pw:
        try:
            gestart = pw.chromium.launch()
        except Exception as fout:
            pytest.skip(f"chromium niet beschikbaar: {fout}")
        yield gestart
        gestart.close()


@pytest.fixture
def pagina(browser):
    context = browser.new_context(viewport={"width": 1366, "height": 768}, accept_downloads=True)
    pagina = context.new_page()
    fouten = []
    pagina.on("pageerror", lambda e: fouten.append(str(e)))
    pagina.goto(SPEL)
    pagina.wait_for_timeout(300)
    yield pagina
    assert fouten == [], fouten
    context.close()


def test_versie_staat_in_het_bestand_en_op_de_pagina(pagina):
    bron = BESTAND.read_text(encoding="utf-8")
    m = re.search(r"const VERSIE = '(\d{4}-\d{2}-\d{2})'", bron)
    assert m, "VERSIE ontbreekt in het bestand"
    assert pagina.locator("#lat-versie").inner_text() == m.group(1)
    tekst = pagina.locator("nav.lat").inner_text()
    assert "status: in gebruik" in tekst
    assert "tests in CI" in tekst


def test_kruimelpad_wijst_naar_de_voorpagina(pagina):
    assert pagina.locator('nav.lat a[href="https://security-commons-nl.github.io/"]').count() == 1
    assert "Security Commons NL" in pagina.locator("nav.lat").inner_text()


def test_opslaan_en_laden_is_een_rondgang(pagina, tmp_path):
    pagina.evaluate("""() => {
        st.pijler = 'stad'; st.dienst = 'afval'; st.prepScenario = 1; st.metBudget = true;
        st.prepKeuzes = new Set(['p1', 'p3']); st.actief = new Set(['m2']); st.versterktNodes = new Set(['k1']);
        st.effectiviteit = { m2: 50 };
    }""")
    with pagina.expect_download() as info:
        pagina.locator("#btn-stand-opslaan").click()
    download = info.value
    pad = tmp_path / download.suggested_filename
    download.save_as(pad)
    assert pad.name.startswith("weerbaarheidsgame-stand-") and pad.suffix == ".json"
    data = json.loads(pad.read_text(encoding="utf-8"))
    assert data["instrument"] == "weerbaarheid-game"
    assert data["pijler"] == "stad" and data["dienst"] == "afval"
    assert sorted(data["prepKeuzes"]) == ["p1", "p3"]
    assert data["actief"] == ["m2"] and data["versterktNodes"] == ["k1"]
    assert data["effectiviteit"] == {"m2": 50}
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", data["versie"])

    # Verse pagina, dan laden: dezelfde keuzes terug, en het instrument meldt het.
    pagina.reload()
    pagina.wait_for_timeout(300)
    assert pagina.evaluate("() => st.pijler") is None
    pagina.locator("#stand-bestand").set_input_files(str(pad))
    pagina.wait_for_timeout(300)
    terug = pagina.evaluate("""() => ({
        pijler: st.pijler, dienst: st.dienst, prepScenario: st.prepScenario, metBudget: st.metBudget,
        prepKeuzes: Array.from(st.prepKeuzes).sort(), actief: Array.from(st.actief), versterkt: Array.from(st.versterktNodes),
        effectiviteit: st.effectiviteit
    })""")
    assert terug == {"pijler": "stad", "dienst": "afval", "prepScenario": 1, "metBudget": True,
                     "prepKeuzes": ["p1", "p3"], "actief": ["m2"], "versterkt": ["k1"], "effectiviteit": {"m2": 50}}
    assert "Stand geladen" in pagina.locator("#lat-melding").inner_text()
    assert pagina.locator("#s-pillar").evaluate("el => el.classList.contains('active')")


def test_een_vreemd_bestand_wordt_geweigerd(pagina, tmp_path):
    fout = tmp_path / "anders.json"
    fout.write_text(json.dumps({"instrument": "procescheck"}), encoding="utf-8")
    pagina.locator("#stand-bestand").set_input_files(str(fout))
    pagina.wait_for_timeout(300)
    assert "Laden mislukt" in pagina.locator("#lat-melding").inner_text()
    assert pagina.evaluate("() => st.pijler") is None


def test_de_lat_past_op_een_beamer_en_een_telefoon(browser):
    for breedte, hoogte in ((1280, 720), (375, 800)):
        context = browser.new_context(viewport={"width": breedte, "height": hoogte})
        p = context.new_page()
        p.goto(SPEL)
        p.wait_for_timeout(200)
        assert p.evaluate("() => document.documentElement.scrollWidth <= window.innerWidth + 1"), breedte
        assert p.locator("nav.lat").is_visible()
        context.close()
