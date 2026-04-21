# Bijdragen aan weerbaarheid-game

Interactief bestuursdashboard dat gemeentelijke kwetsbaarheid visualiseert (HTML5 + vanilla JS + SVG).

Raadpleeg de organisatiebrede richtlijnen van security-commons-nl:

- [CONTRIBUTING.md (org-wide)](https://github.com/security-commons-nl/.github/blob/main/CONTRIBUTING.md)
- [DOCUMENTATION-STANDARD.md](https://github.com/security-commons-nl/.github/blob/main/DOCUMENTATION-STANDARD.md)
- [PRINCIPLES.md](https://github.com/security-commons-nl/.github/blob/main/PRINCIPLES.md)

## Project-specifieke werkwijze

### Lokaal draaien

Geen build-stap. Open `weerbaarheid-game.html` in een moderne browser, of serveer:

```bash
python -m http.server 8000
```
Daarna http://localhost:8000/weerbaarheid-game.html.

### Ontwerpprincipes

- Pure HTML5 + vanilla JS + SVG — **geen build-tools, frameworks of bundlers**
- Werkt offline, werkt zonder login, bestuurbaar door niet-technische gebruikers
- Alleen `weerbaarheid-game.html` is publiek. Onderliggende Leiden-specifieke data/PDFs blijven lokaal

### PRs

- UI-wijzigingen: voeg screenshot of korte screencast toe aan PR-beschrijving
- Inhoudelijke wijzigingen (scenario's, data): onderbouw de bron
