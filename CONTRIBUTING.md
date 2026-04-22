# Bijdragen aan weerbaarheid-game

Interactief bestuursdashboard dat gemeentelijke kwetsbaarheid visualiseert.

## 1. Iets aanbieden of melden — geen Git-ervaring nodig

→ [**Bijdrage aanbieden**](https://github.com/security-commons-nl/weerbaarheid-game/issues/new?template=bijdrage-aanbieden.md)
  Een scenario, dataset of ervaring uit een bestuurssessie die de game kan verrijken.

→ [**Fout of verbetering**](https://github.com/security-commons-nl/weerbaarheid-game/issues/new?template=fout-of-verbetering.md)
  Iets klopt niet, kan beter, of mist.

Vul alleen de vragen in die voor jou relevant zijn — we helpen je met de rest.

**Geen GitHub-account?** [Maak er gratis een](https://github.com/signup) (2 minuten), of vraag iemand in je netwerk om namens jou te posten.

## 2. Meediscussiëren

→ [**Discussions**](../../discussions)

Voor vragen, ervaringen en ideeën zonder directe actie.

## 3. Voor ontwikkelaars — UI of scenario aanleveren

### Lokaal draaien

Geen build-stap. Open `weerbaarheid-game.html` in een moderne browser, of serveer:

```bash
python -m http.server 8000
# → http://localhost:8000/weerbaarheid-game.html
```

### Ontwerpprincipes

- Pure HTML5 + vanilla JS + SVG — **geen build-tools, frameworks of bundlers**
- Werkt offline, zonder login, bestuurbaar door niet-technische gebruikers
- Alleen `weerbaarheid-game.html` is publiek; Leiden-specifieke data blijft lokaal

### PRs

- UI-wijzigingen: voeg screenshot of korte screencast toe aan PR-beschrijving
- Inhoudelijke wijzigingen (scenario's, data): onderbouw de bron

---

**Organisatiebrede richtlijnen**: [security-commons-nl/.github](https://github.com/security-commons-nl/.github/blob/main/CONTRIBUTING.md)
