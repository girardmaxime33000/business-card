# CHANGELOG

## L1 — Corrections
- Dates des trois premières expériences traduites en EN (`exp0-date`, `exp1-date`, `exp2-date`).
- `alt` des quatre portraits de références renseigné en FR et EN. `build-en.py` gère l'attribut `data-i18n-alt`.
- Logos conservés en `alt=""` : le nom de l'entreprise figure en texte à côté.
- Un seul commit pour les sous-tâches 1 et 2 (fichiers `index.html`, `build-en.py` et `en/index.html` communs).

## L2 — Indexation par les IA
- `llms.txt` (résultats recopiés de `index.html`, placeholders de disponibilité et de postes visés).
- `scripts/build_llms.py` génère `llms-full.txt`. Appelé dans le job `build-check` de la CI.
- Métadonnées des PDF consignées dans `TODO_CONTENU.md`, PDF non modifiés.

## L3 — Première vue et FAQ orientées recruteur
- `#hero-availability` et `#hero-kpis` (placeholders) avec clés `t.fr` / `t.en`.
- FAQ : deux questions génériques remplacées (HTML, `t.fr`, `t.en`, JSON-LD `FAQPage`), réponses en placeholder.
- JSON-LD `Person` : `worksFor` (Pollen AM, InRealArt), `alumniOf` Inseec Business School.
- Cartes de valeurs conservées, proposition « Périmètre » dans `TODO_CONTENU.md`.

## L4 — Pages de cas indexables
- `cas/_template.html` et `scripts/build_cas.py` : head, header, pied de page, bandeau de consentement et scripts repris d'`index.html` via `scripts/pages_common.py`. Textes lus dans `t.fr`, mot pour mot.
- Cinq pages : `trambots-ia-transport`, `eyeride-crowdfunding-international`, `systeme-ia-multi-agent-marketing`, `camping-car-park-marketing-europe`, `sense4data-stack-marketing`. Données dans `data/cas/*.json`.
- Liens « Voir le détail » sur les trois cartes de cas et les deux expériences (clés `link-detail-*`). Côté EN, ils pointent vers la page FR.
- Pages ajoutées à `sitemap.xml` (priorité 0.7), `tailwind.config.js`, `ci.yml` (html5validator, lychee, régénération) et `llms.txt`.
- Écart avec la demande : les deux pages d'expérience renvoient vers `/#experiences` (les trois pages de cas vers `/#cas-usage`).

## L5 — Pages de candidature personnalisées
- `c/_template/index.html`, `scripts/new_application.py` (`--slug … --entreprise … --poste … --lieu …`, `--all`) et `data/candidatures/<slug>.json`.
- Trois candidatures : `ynov`, `teddy-smith`, `bdl-club-invest`. `noindex, nofollow`, absentes de `sitemap.xml` et de `llms.txt`.
- Worker : route `POST /notify` (origines autorisées, limitation de débit KV avec clé séparée, relais vers le secret `N8N_WEBHOOK_URL`, aucune IP ni user-agent transmis). Documentée dans `cloudflare-worker/README.md`.
- Pages de confidentialité FR et EN : finalité, données transmises, ligne `sessionStorage`, durée de conservation de l'IP.
