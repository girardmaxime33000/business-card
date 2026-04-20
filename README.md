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

### 2. Uploader les CV PDF

Deux fichiers placeholder ont été créés. Remplace-les par les vrais PDFs :

| Fichier | Langue |
|---------|--------|
| `cv-maxime-girard-fr.pdf` | Français |
| `cv-maxime-girard-en.pdf` | Anglais |

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
├── index.html              # Site FR (source unique, ~1300 lignes)
├── en/
│   └── index.html          # Version EN statique (indexable par Google)
├── favicon.svg             # Favicon monogramme MG.
├── og-image.svg            # Source OG image (à exporter en .jpg)
├── og-image.jpg            # ⚠ À créer manuellement (voir ci-dessus)
├── robots.txt
├── sitemap.xml
├── cv-maxime-girard-fr.pdf # ⚠ À remplacer par le vrai PDF
├── cv-maxime-girard-en.pdf # ⚠ À remplacer par le vrai PDF
└── README.md
```
