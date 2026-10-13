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

## L6 — Mesure des conversions
- `track(name, props)` dans le script d'`index.html` (segment « MESURE ») : Plausible, Umami et `dataLayer` (nom en snake_case), un `try/catch` par outil. Reprise par les pages `cas/*` et `c/*` via `scripts/pages_common.py`.
- `Booking Slot Selected` et `Booking Confirmed` depuis les `postMessage` Calendly (`event.origin` = `https://calendly.com`).
- `utm_source`, `utm_medium`, `utm_campaign` conservés dans `sessionStorage`, ajoutés à l'URL du widget Calendly et aux propriétés de `Booking Confirmed` et `CV Download`.
- Chat : `Chat Opened`, `Chat Question` (numéro d'ordre uniquement), `Chat Suggestion Click` (clé de la suggestion).
- `Section Viewed` (profil, experiences, cas-usage, references, contact), une fois par section.
- `CV Download` remplace le `dataLayer.push` direct (même événement `cv_download`, propriétés conservées, UTM ajoutés).
- Vérifié avec Chromium : événements, propriétés, filtrage d'origine des `postMessage`, URL Calendly avec UTM.
- Décision Umami / Plausible consignée dans `TODO_CONTENU.md`.

## L7 — Identification des entreprises visiteuses
- Emplacement commenté `loadB2BIdentification()` dans le bloc de consentement (clés en `{{A_COMPLETER}}`), appels commentés pour les cas `granted` et « Accepter ».
- Ligne ajoutée dans le tableau « Cookies et traceurs » des deux pages de confidentialité (« Requis — chargé après acceptation »), avec placeholders.

## L8 — Vérification finale
- Build : `build-en.py`, `build_cas.py`, `new_application.py --all`, `build_llms.py`, `tailwindcss` relancés, `git diff --exit-code` vide hors `sitemap.xml`.
- `html5validator` (Nu Html Checker) : 0 erreur sur `index.html`, `en/index.html`, pages de confidentialité, 5 pages `cas/*` et 3 pages `c/*/index.html`. Gabarits exclus par `--blacklist _template`.
- `lychee` : non exécuté (outil absent de l'environnement). `scripts/check_pages.py` contrôle les liens internes et les ancres. Les liens externes restent à la charge du job CI.
- `scripts/check_jsonld.py` : 7 blocs JSON-LD parsables (index, EN, 5 pages de cas).
- `scripts/check_pages.py` : pages `/c/*` en `noindex, nofollow` et absentes de `sitemap.xml`, `llms.txt`, `llms-full.txt` ; autres pages en `index, follow` ; URL du sitemap résolues en fichiers ; aucun texte français visible dans `en/index.html`. Nouveau job CI `controles-site`.
- Contrôle visuel à 375 px et 1440 px (Chromium) : `index.html`, `en/index.html`, une page de cas, une page de candidature, sans débordement horizontal ni erreur JavaScript.
- Corrections découvertes pendant ce lot :
  - `en/index.html` : 28 puces d'expérience et 6 liens du menu mobile restaient en français (`build-en.py` s'arrêtait au premier `>` d'une classe `before:content-['->']` et ne traitait que la première occurrence d'une clé). Corrigé dans `build-en.py`.
  - Pages `cas/*` et `c/*` : le `<style>` principal (polices QTFrank, `[hidden]`, impression) n'était pas repris, le bandeau de consentement était tronqué d'un `</div>`. Corrigés dans `scripts/pages_common.py`.
