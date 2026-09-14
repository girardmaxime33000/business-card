# business-card — Maxime Girard

Portfolio / carte de visite personnelle. Site statique single-page, déployé sur GitHub Pages.

**URL prod :** https://girardmaxime33000.github.io/business-card/

---

## Actions manuelles requises avant déploiement

### 1. Convertir `og-image.svg` → `og-image.jpg`

Les crawlers LinkedIn, Slack et iMessage ne rendent pas toujours les SVG en Open Graph.
Il faut exporter `og-image.svg` en `og-image.jpg` **1200×630 px** avant de pousser en production.

Options :
- **Figma** : File → Import SVG → Export as JPG 1200×630
- **Inkscape** : `inkscape og-image.svg --export-type=png --export-filename=og-image.png -w 1200 -h 630` puis convertir en JPG
- **CloudConvert** : https://cloudconvert.com/svg-to-jpg
- **Sharp (Node.js)** : `npx sharp-cli og-image.svg -o og-image.jpg -w 1200 -h 630`

Le fichier `og-image.jpg` doit être placé à la **racine du repo**.

### 2. CV PDF

`cv-maxime-girard-en.pdf` contient le vrai CV (anglais). Décision prise : ce même
fichier est utilisé comme lien de téléchargement sur les deux langues du site
(pas de CV français disponible). `cv-maxime-girard-fr.pdf` reste un fichier
vide (0 octet) et n'est référencé nulle part — à fournir et relier si un CV
français doit un jour remplacer l'anglais sur la version FR du site.

### 3. Créer un compte Plausible

Le tracking Plausible est configuré pour le domaine `girardmaxime33000.github.io`.

**Important :** `girardmaxime33000.github.io` est un domaine partagé entre tous les repos GitHub Pages de l'utilisateur. Le tracking Plausible sera donc global à l'ensemble des pages hébergées sous ce domaine, pas uniquement `business-card/`.

**Recommandation :** Brancher un domaine custom (ex. `maxime-girard.fr`) et mettre à jour l'attribut `data-domain` dans le script Plausible ainsi que toutes les URLs canoniques, OG et sitemap.

Pour activer la collecte :
1. Créer un compte sur https://plausible.io (ou auto-héberger)
2. Ajouter le site avec le domaine `girardmaxime33000.github.io`

### 4. Fournir les URLs LinkedIn des référents

Les profils LinkedIn des personnes citées dans la section Références sont marqués `<!-- TODO: LinkedIn URL -->` dans le code. Une fois les URLs disponibles, remplacer les `<span class="ref-name">` par des `<a>` avec les liens correspondants.

Référents :
- Nicolas Pasetti (CEO, eteam_work)
- Alexandre Masson (Data Engineer, ColisPrivé)
- Pierre Rocherie (Directeur Général, FM Auto)
- Jérémy Fortinon (Expert transformation des SI)

---

## Déploiement

```bash
git push -u origin claude/refactor-business-card-exggy
```

Puis configurer GitHub Pages sur la branche souhaitée (Settings → Pages).

---

## Structure du repo

```
business-card/
├── index.html              # Site FR (source unique, ~1000 lignes)
├── en/
│   └── index.html          # Version EN — générée par build-en.py, ne pas éditer à la main
├── build-en.py              # Génère en/index.html depuis index.html (traductions t.en)
├── tailwind.config.js       # Config Tailwind (content, couleurs, polices)
├── tailwind-input.css       # Point d'entrée @tailwind base/components/utilities
├── tailwind.css             # CSS Tailwind précompilé — généré, ne pas éditer à la main
├── favicon.svg             # Favicon monogramme MG.
├── og-image.svg            # Source OG image (à exporter en .jpg)
├── og-image.jpg            # ⚠ À créer manuellement (voir ci-dessus)
├── robots.txt
├── sitemap.xml
├── cv-maxime-girard-fr.pdf # ⚠ Vide — voir « CV PDF » ci-dessus
├── cv-maxime-girard-en.pdf # Vrai CV, utilisé sur les deux langues
└── README.md
```

---

## Mise à jour du site

Le site reste 100 % statique à l'usage (aucune installation pour un visiteur),
mais deux fichiers sont **générés** et doivent être régénérés après toute
modification d'`index.html` :

### Régénérer `en/index.html` (après un changement de contenu ou de structure)

```bash
python3 build-en.py
```

Applique les traductions `t.en` du script d'`index.html` sur les éléments
`data-i18n`/`data-i18n-html`, réécrit les chemins relatifs (`../`), et bascule
`lang`, les métadonnées et le sélecteur de langue actif. Le script principal
(scrollspy, menu mobile, assistant, chargement différé de Calendly) est
conservé tel quel — commun aux deux langues, pas seulement de l'i18n.

### Régénérer `tailwind.css` (après un changement de classes Tailwind)

```bash
npx tailwindcss@3.4.13 -i ./tailwind-input.css -o ./tailwind.css --minify
```

Scanne `index.html` et `en/index.html` (voir `content` dans `tailwind.config.js`)
pour ne générer que les classes utilisées. Remplace le CDN runtime
`cdn.tailwindcss.com` (compilation à la volée côté client, pénalisant le
premier rendu) par un fichier statique commité — toujours régénérer **avant**
de lancer `build-en.py`, puisque celui-ci recopie `<link rel="stylesheet"
href="tailwind.css">` vers `en/index.html`.

**Ordre à respecter** après une modification d'`index.html` touchant des
classes Tailwind : régénérer `tailwind.css`, puis `en/index.html`.
