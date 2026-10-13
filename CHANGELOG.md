# CHANGELOG

## L1 — Corrections
- Dates des trois premières expériences traduites en EN (`exp0-date`, `exp1-date`, `exp2-date`).
- `alt` des quatre portraits de références renseigné en FR et EN. `build-en.py` gère l'attribut `data-i18n-alt`.
- Logos conservés en `alt=""` : le nom de l'entreprise figure en texte à côté.
- Une seule commit pour les sous-tâches 1 et 2 (fichiers `index.html`, `build-en.py` et `en/index.html` communs).

## L2 — Indexation par les IA
- `llms.txt` (résultats recopiés de `index.html`, placeholders de disponibilité et de postes visés).
- `scripts/build_llms.py` génère `llms-full.txt`. Appelé dans le job `build-check` de la CI.
- Métadonnées des PDF consignées dans `TODO_CONTENU.md`, PDF non modifiés.

## L3 — Première vue et FAQ orientées recruteur
- `#hero-availability` et `#hero-kpis` (placeholders) avec clés `t.fr` / `t.en`.
- FAQ : deux questions génériques remplacées (HTML, `t.fr`, `t.en`, JSON-LD `FAQPage`), réponses en placeholder.
- JSON-LD `Person` : `worksFor` (Pollen AM, InRealArt), `alumniOf` Inseec Business School.
- Cartes de valeurs conservées, proposition « Périmètre » dans `TODO_CONTENU.md`.
