"""De game in een echte browser: past hij op het scherm, en heet hij overal hetzelfde?

Deze tool is één HTML-bestand zonder build, dus er valt weinig te unit-testen. Wat er wél toe doet is
of hij het doet op een beamer in een raadzaal, en dat zie je alleen door hem door te lopen. Drie
maten: 1440x900 (laptop), 1366x768 en 1280x720 (de twee formaten die je in vergaderzalen tegenkomt).

Aanleiding (03-09-2026): de uitlegkaart van de keten-walkthrough viel bij stap 1 en 2 links buiten
beeld, op elke breedte. Oorzaak was een transform van het startkaartje die bleef staan. Zulke fouten
zijn onzichtbaar tot iemand voor een zaal staat, dus staan ze hier vast.

    python -m pytest tests -v

Playwright met chromium is nodig; zonder slaat de test zichzelf over.
"""
from __future__ import annotations

import pathlib

import pytest

sync_api = pytest.importorskip("playwright.sync_api", reason="playwright niet beschikbaar")

REPO = pathlib.Path(__file__).resolve().parent.parent
SPEL = (REPO / "weerbaarheid-game.html").as_uri()
MATEN = [(1440, 900), (1366, 768), (1280, 720)]


@pytest.fixture(scope="module")
def browser():
    with sync_api.sync_playwright() as pw:
        try:
            gestart = pw.chromium.launch()
        except Exception as fout:
            pytest.skip(f"chromium niet beschikbaar: {fout}")
        yield gestart
        gestart.close()


@pytest.fixture(params=MATEN, ids=[f"{b}x{h}" for b, h in MATEN])
def blad(browser, request):
    breedte, hoogte = request.param
    context = browser.new_context(viewport={"width": breedte, "height": hoogte})
    pagina = context.new_page()
    fouten: list[str] = []
    pagina.on("pageerror", lambda e: fouten.append(str(e)))
    pagina.on("console", lambda m: fouten.append(m.text) if m.type == "error" else None)
    pagina.goto(SPEL)
    pagina.wait_for_timeout(500)
    yield pagina, breedte, hoogte
    assert not fouten, f"fouten in de browser: {fouten}"
    context.close()


def naar_scenario(pagina) -> None:
    """Van het overzicht naar een draaiende keten: pijler, dienst, een maatregel, starten."""
    pagina.locator(".pillar-tile").first.click()
    pagina.wait_for_timeout(500)
    pagina.locator("text=Crisis-alert aan inwoners").first.click()
    pagina.wait_for_timeout(700)
    pagina.locator("text=Sirenes testen en onderhouden").first.click()
    pagina.wait_for_timeout(150)
    pagina.locator("text=Start scenario").first.click()
    pagina.wait_for_timeout(1400)


def test_de_tool_heet_zoals_de_commons_hem_noemt(blad):
    """De pagina noemde zichzelf Weerbaarheids-Dashboard terwijl alles eromheen game zegt.

    Besluit 03-09-2026: de naam blijft weerbaarheidsgame, met een ondertitel die zegt wat het is.
    """
    pagina, _, _ = blad
    assert "Weerbaarheidsgame" in pagina.title()
    assert "gespreksinstrument" in pagina.title()
    assert "Weerbaarheidsgame" in pagina.locator("h1").first.inner_text()
    assert "Dashboard" not in pagina.locator("body").inner_text()


def test_dienstkaarten_rekken_niet_uit(blad):
    """Een grid rekt zijn cellen uit tot de hoogste; dat gaf drie bijna lege kaarten van 670 pixels."""
    pagina, _, _ = blad
    pagina.locator(".pillar-tile").first.click()
    pagina.wait_for_timeout(700)
    hoogtes = pagina.eval_on_selector_all(
        ".svc-card", "n => n.map(e => Math.round(e.getBoundingClientRect().height))")
    assert hoogtes, "geen dienstkaarten gevonden"
    assert max(hoogtes) <= 320, f"kaart van {max(hoogtes)} px is uitgerekt"


def test_walkthrough_valt_binnen_het_scherm(blad):
    """Elke stap van de keten-uitleg staat helemaal in beeld, ook de eerste twee.

    Die vielen links buiten beeld doordat de startkaart zich centreert met translate(-50%,-50%) en
    die transform bleef staan bij het positioneren per tandwiel. Voor iemand die de game aan een
    college laat zien, valt de knop Volgende dan buiten het scherm.
    """
    pagina, breedte, hoogte = blad
    naar_scenario(pagina)
    pagina.locator("text=Ontdek de keten").first.click()
    pagina.wait_for_timeout(600)
    for stap in range(6):
        doos = pagina.evaluate("""() => {
          const el = document.getElementById('wt-card');
          if (!el) return null;
          const r = el.getBoundingClientRect();
          return {x: r.x, y: r.y, w: r.width, h: r.height};
        }""")
        if doos:
            assert doos["x"] >= 0, f"stap {stap}: {doos['x']:.0f} px links buiten beeld"
            assert doos["y"] >= 0, f"stap {stap}: boven beeld"
            assert doos["x"] + doos["w"] <= breedte, f"stap {stap}: rechts buiten beeld"
            assert doos["y"] + doos["h"] <= hoogte, f"stap {stap}: onder beeld"
        pagina.evaluate(f"() => window.walkthroughStap && window.walkthroughStap({stap + 1})")
        pagina.wait_for_timeout(350)


def test_de_keten_is_te_spelen(blad):
    """De doorloop zelf: pijler, dienst, maatregel, scenario, incident. Zonder fouten in de browser."""
    pagina, _, _ = blad
    naar_scenario(pagina)
    assert pagina.locator("text=Simuleer incident").first.is_visible()
    pagina.locator("text=Overslaan").first.click()
    pagina.wait_for_timeout(400)
    pagina.locator("text=Simuleer incident").first.click()
    pagina.wait_for_timeout(1500)
    tekst = pagina.locator("body").inner_text()
    assert "MAATSCHAPPELIJKE DRUK" in tekst.upper()
