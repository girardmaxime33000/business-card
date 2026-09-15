# CLAUDE.md — AI Assistant Guide for `business-card`

## Project Overview

Personal portfolio / business card website for **Maxime Girard**, Directeur
Marketing & Growth B2B (10+ ans d'expérience, France/Europe/US/Japon).
Site statique, bilingue FR/EN, déployé sur GitHub Pages sous le domaine
custom `www.girardmaxime33.com` (voir `CNAME`).

**Live-ready :** pas de serveur de dev requis pour visualiser le rendu
final, mais deux fichiers sont **générés** (voir « Build & génération »
ci-dessous) — ne jamais les éditer à la main.

---

## Repository Structure

```
business-card/
├── index.html               # Site FR — SOURCE UNIQUE de contenu et de script
├── en/
│   └── index.html            # Site EN — GÉNÉRÉ par build-en.py, ne pas éditer à la main
├── build-en.py                # Génère en/index.html + rafraîchit sitemap.xml depuis index.html
├── tailwind.config.js         # Config Tailwind (content, couleurs, polices)
├── tailwind-input.css         # Point d'entrée @tailwind base/components/utilities
├── tailwind.css                # CSS Tailwind précompilé — GÉNÉRÉ, ne pas éditer à la main
├── favicon.svg
├── og-image.svg / og-image.jpg  # og-image.jpg généré depuis og-image.svg (régénération manuelle, voir README)
├── logos/                      # Logos employeurs (.webp/.svg), section Expériences
├── testimonials/               # Portraits des référents (.webp), section Références
├── robots.txt
├── sitemap.xml                  # <lastmod> réécrit automatiquement par build-en.py
├── cv-maxime-girard-en.pdf      # CV réel EN, lié depuis en/index.html
├── cv-maxime-girard-fr.pdf      # CV réel FR, lié depuis index.html
├── CNAME                        # Domaine custom : www.girardmaxime33.com
├── cloudflare-worker/            # Backend de l'assistant IA — déployé séparément, hors GitHub Pages
│   ├── chat-worker.js             # Source unique de vérité des faits/règles du bot (SYSTEM_PROMPT)
│   ├── wrangler.toml
│   └── README.md
└── README.md
```

Pas de `package.json`, pas de framework côté front. `npx tailwindcss` et
`python3` sont les deux seuls outils requis, et uniquement au moment de
régénérer les fichiers dérivés.

---

## Tech Stack

| Layer      | Technology                                          |
|------------|------------------------------------------------------|
| Markup     | HTML5 sémantique, dupliqué FR (`index.html`) / EN (`en/index.html`) |
| Styling    | Tailwind CSS précompilé (`tailwind.css`, généré, pas de CDN runtime) |
| Scripting  | Vanilla JS en bas de `<body>` — IntersectionObserver, scrollspy, menu mobile, horloge, chat |
| i18n       | Objet `t` (fr/en) dans le script d'`index.html`, lu par `build-en.py` au build |
| Backend    | Cloudflare Worker (`cloudflare-worker/chat-worker.js`) — assistant IA, Workers AI |
| Fonts      | Google Fonts — Plus Jakarta Sans + JetBrains Mono     |
| Analytics  | Plausible (`data-domain="www.girardmaxime33.com"`)   |
| Booking    | Widget Calendly, chargé en différé à l'approche de `#contact` |
| Dev tools  | `npx tailwindcss@3.4.13`, `python3` (aucune dépendance à installer côté visiteur) |

---

## Page Sections

Page unique à défilement, sections ancrées, identiques FR/EN :

| Section ID        | Content                                         |
|-------------------|-------------------------------------------------|
| *(hero)*          | Nom, titre, métriques clés, CTA (RDV / CV / LinkedIn) |
| `#profil`         | Pitch professionnel + 3 value cards             |
| `#experiences`    | Timeline de 8 postes avec résultats chiffrés    |
| `#cas-usage`      | 3 cas d'usage (bento) — IA/Growth               |
| `#competences`    | Groupes de compétences (bento)                  |
| `#references`     | 4 témoignages                                   |
| `#contact`        | Email, LinkedIn, widget Calendly                |

Plus : header fixe (nav + horloge Bordeaux + sélecteur de langue + CTA CV),
footer, widget d'assistant IA flottant (fermé par défaut).

---

## i18n — FR/EN

**`index.html` est la seule source à éditer pour le contenu.**
`en/index.html` est un fichier généré ; toute édition manuelle y sera
écrasée au prochain `python3 build-en.py`.

- Tout texte traduisible porte un attribut `data-i18n="clé"` (texte simple),
  `data-i18n-html="clé"` (contient du HTML, ex. un `<strong>` ou un badge
  COMEX) ou `data-i18n-placeholder="clé"` (attribut `placeholder` d'un champ).
- Chaque clé doit exister à la fois dans `t.fr` et `t.en`, dans le `<script>`
  en bas d'`index.html`. Cet objet `t` sert de **source de traduction au
  build** — `build-en.py` l'extrait par regex et l'applique aux éléments
  correspondants pour produire `en/index.html`. Il n'est plus utilisé pour
  une bascule de langue en direct dans le navigateur (supprimée — voir plus
  bas).
- Le sélecteur de langue (`.lang-btn`, header + footer) est un simple
  `<a href="/">` / `<a href="/en/">` : navigation native du navigateur, pas
  de JS. L'URL affichée correspond donc toujours à la langue du contenu.
  Ne pas réintroduire de bascule de texte en JS côté client (c'était la
  cause d'un vrai bug : URL FR affichant du contenu EN sans changer).
- `currentLang` (JS runtime) ne sert plus qu'à choisir le bon message
  d'erreur du chat (`t[currentLang]['chat-error']`), initialisé depuis
  `document.documentElement.lang`.
- Le JSON-LD (`<script type="application/ld+json">`) et les métadonnées
  (title, description, og:*, twitter:*) sont traduits par `build-en.py` via
  des **regex** sur les clés JSON/attributs, pas des `.replace()` sur
  chaîne littérale — un `.replace()` littéral se tait silencieusement dès
  que le texte FR source dérive (bug déjà rencontré une fois sur le JSON-LD
  `description`). Garder ce principe pour toute future métadonnée ajoutée.

---

## Build & génération — ordre à respecter

Après toute modification d'`index.html` :

1. **Si des classes Tailwind ont changé** :
   ```bash
   npx tailwindcss@3.4.13 -i ./tailwind-input.css -o ./tailwind.css --minify
   ```
   Scanne `index.html` + `en/index.html` (`content` dans `tailwind.config.js`).

2. **Toujours, après un changement de contenu ou de structure** :
   ```bash
   python3 build-en.py
   ```
   Régénère `en/index.html` (traductions, chemins relatifs `../`, lang,
   métadonnées, JSON-LD, sélecteur de langue actif) **et** republie
   `<lastmod>` dans `sitemap.xml` à la date du jour.

**Toujours dans cet ordre** : Tailwind d'abord (le `<link>` vers
`tailwind.css` est recopié tel quel par `build-en.py`), puis `build-en.py`.
Une CI vérifie qu'aucun diff ne reste après ces deux commandes — voir
`.github/workflows/` si présent ; sinon, exécuter les deux commandes
manuellement avant de committer reste indispensable.

---

## Assistant IA (chat)

- Frontend : `#chat-toggle` / `#chat-panel` dans `index.html`/`en/index.html`,
  **fermé par défaut** au chargement (ne pas repasser à ouvert — ça masque
  le CTA hero en mobile). Appelle `CHAT_ENDPOINT` (URL du Worker, en dur
  dans le `<script>`) en `POST {question}`, attend `{answer, ...}`.
- Backend : `cloudflare-worker/chat-worker.js`, déployé séparément (pas
  servi par GitHub Pages). `SYSTEM_PROMPT` dans ce fichier est la **source
  unique de vérité** des faits sur Maxime utilisés par le bot — modifier ce
  bloc pour changer ce que le bot sait, ne pas dupliquer ces faits ailleurs.
- CORS : `ALLOWED_ORIGINS` dans `chat-worker.js` couvre le domaine custom,
  l'ancien `girardmaxime33000.github.io` (transition) et `localhost:8080`.
- Rate limiting par IP (10 req/5 min) via un namespace KV `RATE_LIMIT`,
  actif (binding lié dans `wrangler.toml`) — voir
  `cloudflare-worker/README.md` § Rate limiting. Fail-open par conception
  si jamais le binding disparaissait (pas de blocage du chat).

---

## CSS Design System

Design tokens dans `tailwind.config.js` (`theme.extend.colors`,
`fontFamily`) — thème clair, accent `lime` (`#ddff57`).

### Conventions CSS

- Classes utilitaires Tailwind directement dans le HTML — pas de CSS custom
  hors du `<style>` en tête d'`index.html` (overlay de bruit, glows
  ambiants, `.reveal`, styles d'impression, `.nav-active`).
- Ne pas introduire de fichier CSS externe supplémentaire ni réactiver le
  CDN runtime `cdn.tailwindcss.com` (remplacé par `tailwind.css` précompilé
  pour les perfs de premier rendu).
- Breakpoints Tailwind standard (`md:` = 768px, etc.).

---

## Animation & comportements JS

Le script en bas de `<body>` (commun aux deux langues, recopié tel quel par
`build-en.py`) porte, dans l'ordre :

- **Scroll reveal** : `.reveal` / `.reveal.visible`, `IntersectionObserver`
  (`threshold: 0.1`, `rootMargin: '0px 0px -40px 0px'`). Métriques du hero
  déclenchées immédiatement (délai échelonné 100 ms).
- **Scrollspy nav** : surbrillance du lien de nav actif selon la section
  visible.
- **Chargement différé de Calendly** : le script du widget n'est injecté
  qu'à l'approche de `#contact`.
- **Horloge Bordeaux** : heure réelle Europe/Paris, indépendante du fuseau
  du visiteur.
- **Menu mobile**, **année du footer**, **assistant IA** (voir plus haut).

---

## Editing Guidelines for AI Assistants

### Modifier le contenu

- Éditer uniquement `index.html`. Ajouter un texte traduisible = ajouter
  l'attribut `data-i18n*` ET la clé correspondante dans `t.fr` **et** `t.en`.
- Toujours relancer `python3 build-en.py` après un changement de contenu —
  sinon `en/index.html` diverge silencieusement.

### Modifier les styles

- Changer les tokens dans `tailwind.config.js` pour un changement global.
- Après tout changement de classes Tailwind, régénérer `tailwind.css`
  (commande ci-dessus) avant `build-en.py`.

### Modifier le JavaScript

- Script unique en bas d'`index.html`, recopié tel quel dans `en/index.html`
  par `build-en.py` — ne pas diverger entre les deux fichiers.
- Vanilla JS, pas d'import, pas de dépendance npm.

### Ajouter une section

1. Ajouter le `<section id="...">` dans `index.html`, avec `data-i18n*` sur
   les textes et les clés correspondantes dans `t.fr`/`t.en`.
2. Ajouter les classes `.reveal` (et `.reveal-delay-N` si besoin).
3. Ajouter le lien `<a href="#...">` dans la nav (desktop + mobile) si
   pertinent, avec sa propre clé `data-i18n`.
4. Régénérer `tailwind.css` (si nouvelles classes) puis lancer
   `python3 build-en.py`.

### Domaine et métadonnées

Le domaine canonique est `www.girardmaxime33.com` (canonical, hreflang,
og:*, twitter:*, JSON-LD, `sitemap.xml`, `robots.txt`, `data-domain`
Plausible). Ne pas réintroduire `girardmaxime33000.github.io` dans les
métadonnées — ce domaine github.io reste seulement dans les
`ALLOWED_ORIGINS` CORS du Worker, en transition.

### À ne pas « corriger » sans demander

- Références sans lien LinkedIn dans `#references` : les URLs ne sont pas
  disponibles, ne pas en inventer.

---

## Testing

Pas de suite de tests automatisée au-delà d'éventuels checks CI (build
sans diff, validation HTML, liens morts — voir `.github/workflows/` si
présent). Vérification manuelle :

1. Ouvrir `index.html` **et** `en/index.html` dans un navigateur.
2. Vérifier que toutes les sections s'affichent, dans les deux langues.
3. Redimensionner en mobile (≤ 600 px) et tablette (≤ 900 px).
4. Vérifier les animations reveal au scroll.
5. Cliquer tous les liens de nav, CTA, et le sélecteur de langue (doit
   naviguer vers une URL différente, pas juste retraduire le texte).
6. Vérifier que le chat est fermé au chargement et fonctionne à l'ouverture.

---

## Déploiement

- **GitHub Pages** — servi depuis la racine du repo, domaine custom via
  `CNAME`. Pas de build step côté hébergement : les fichiers générés
  (`tailwind.css`, `en/index.html`, `sitemap.xml`) doivent être commités
  à jour.
- **Assistant IA** — déployé séparément sur Cloudflare Workers, voir
  `cloudflare-worker/README.md`.

---

## Git Workflow

```bash
# Travail sur une fonctionnalité/correctif
git add index.html en/index.html tailwind.css sitemap.xml   # + autres fichiers touchés
git commit -m "type: description courte"

# Push (branche de développement de la session)
git push -u origin claude/<session-id>
```

Convention de nommage des branches pour les sessions IA : `claude/<session-id>`.

---

## Key Contacts / Metadata

| Field    | Value                           |
|----------|---------------------------------|
| Owner    | Maxime Girard                   |
| Email    | girard.maxime33@gmail.com       |
| LinkedIn | linkedin.com/in/maxime-girard-head-of-marketing |
| Domaine  | www.girardmaxime33.com          |
| Langues  | Français (source), Anglais (généré) |
