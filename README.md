# business-card — Maxime Girard

Portfolio / carte de visite personnelle. Site statique single-page, déployé sur GitHub Pages.

**URL prod :** https://www.girardmaxime33.com/

---

## Actions manuelles requises avant déploiement

### 1. Régénérer `og-image.jpg` après modification d'`og-image.svg`

Les crawlers LinkedIn, Slack et iMessage ne rendent pas toujours les SVG en Open Graph ;
`og-image.jpg` (1200×630 px, généré depuis `og-image.svg`) est ce qu'ils affichent réellement.
`og-image.svg` reflète la charte actuelle du site (fond clair, accent lime, Plus Jakarta Sans /
JetBrains Mono) — à ne pas confondre avec une éventuelle ancienne version au thème sombre/orange.

Régénération (nécessite les polices Plus Jakarta Sans/JetBrains Mono installées, ou une police
de secours proche) :
```bash
python3 -c "
import cairosvg, io
from PIL import Image
png = cairosvg.svg2png(url='og-image.svg', output_width=1200, output_height=630)
Image.open(io.BytesIO(png)).convert('RGB').save('og-image.jpg', 'JPEG', quality=90, optimize=True)
"
```
Alternative sans dépendance Python : Figma (File → Import SVG → Export as JPG 1200×630),
Inkscape, ou https://cloudconvert.com/svg-to-jpg.

### 2. Créer un compte Plausible

Domaine custom retenu : `www.girardmaxime33.com` (voir `CNAME`). Toutes les URLs
canoniques, OG, hreflang, JSON-LD, `sitemap.xml`, `robots.txt` et l'attribut
`data-domain` du script Plausible pointent désormais vers ce domaine — plus
vers `girardmaxime33000.github.io` (domaine partagé entre tous les repos
GitHub Pages de l'utilisateur, à ne plus utiliser comme référence).

Pré-requis encore à vérifier côté hébergement avant mise en prod :
- DNS du domaine custom configuré vers GitHub Pages et certificat HTTPS actif
  (Settings → Pages du repo doit afficher le domaine sans erreur).
- GitHub Pages configuré pour appliquer strictement le domaine custom
  (« Enforce HTTPS »), sinon `girardmaxime33000.github.io/business-card/`
  reste accessible en parallèle et sert le même contenu sous une URL non
  canonique.

Pour activer la collecte :
1. Créer un compte sur https://plausible.io (ou auto-héberger)
2. Ajouter le site avec le domaine `www.girardmaxime33.com`

### 3. Fournir les URLs LinkedIn des référents

Les profils LinkedIn des personnes citées dans la section Références ne
sont pas liés (URLs non disponibles). Une fois obtenues, transformer les
`<span>` du nom en `<a href="...">` correspondants dans `index.html` (les
4 occurrences dans `#references`), puis régénérer `en/index.html`.

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
├── og-image.svg            # Source OG image — régénérer og-image.jpg après édition (voir ci-dessus)
├── og-image.jpg            # Généré depuis og-image.svg
├── logos/                  # Logos employeurs (.webp), affichés dans Expériences
├── testimonials/           # Portraits des référents (.webp), affichés dans Références
├── robots.txt
├── sitemap.xml
├── cv-maxime-girard-fr.pdf # CV FR, lié depuis index.html
├── cv-maxime-girard-en.pdf # CV EN, lié depuis en/index.html
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
`data-i18n`/`data-i18n-html`/`data-i18n-placeholder`, réécrit les chemins
relatifs (`../`), et bascule `lang`, les métadonnées (y compris le JSON-LD) et
le sélecteur de langue actif. Le script principal (scrollspy, menu mobile,
assistant, chargement différé de Calendly) est conservé tel quel — commun aux
deux langues, pas seulement de l'i18n.

Ce même run met aussi à jour `<lastmod>` dans `sitemap.xml` à la date du jour
— pas besoin d'y toucher à la main.

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

### CI (`.github/workflows/ci.yml`)

Trois checks sur chaque push/PR :
- **Fichiers générés à jour** — relance les deux commandes ci-dessus et
  échoue si le résultat diverge de ce qui est commité (hors `sitemap.xml`,
  dont le `<lastmod>` change de façon attendue à chaque run).
- **Validation HTML** (Nu Html Checker, via `html5validator`) sur
  `index.html` et `en/index.html`. Une règle est ignorée : le vérificateur
  CSS embarqué ne connaît pas le raccourci `inset`, pourtant supporté par
  tous les navigateurs actuels — faux positif documenté du validateur.
- **Liens morts** (`lychee`) sur les deux pages. Deux exclusions
  temporaires : `girardmaxime33.com` (domaine custom pas encore joignable,
  voir § Plausible ci-dessus — à retirer une fois le DNS/HTTPS en place) et
  `linkedin.com` (bloque systématiquement les clients automatisés).
