# TODO_CONTENU

Placeholders `{{A_COMPLETER: …}}`, décisions à prendre, propositions de reformulation et actions hors code. Mis à jour à chaque lot.

## Placeholders

| Fichier | Ligne | Nature | Lot |
|---|---|---|---|
| `llms.txt` | 3 | Disponibilité, type de contrat, mobilité | L2 |
| `llms.txt` | 7 | Validation de la liste des postes visés | L2 |
| `index.html` | 397 (`#hero-availability`), clé `hero-availability` dans `t.fr` et `t.en` | Date de disponibilité, type de contrat, zone géographique | L3 |
| `index.html` | 405-407 (`#hero-kpis`), clés `hero-kpi1` à `hero-kpi3` dans `t.fr` et `t.en` | Trois indicateurs à choisir parmi les résultats publiés | L3 |
| `index.html` | clés `faq-a2` (disponibilité) et `faq-a3` (postes et secteurs), HTML et JSON-LD `FAQPage` | Réponses aux deux nouvelles questions FAQ | L3 |

## Métadonnées des PDF de CV (constat L2, PDF non régénérés)

| Fichier | Title actuel | Author | Subject | Écart |
|---|---|---|---|---|
| `cv-maxime-girard-fr.pdf` | `CV Maxime Girard FR 2026.docx` | vide | vide | Titre avec extension `.docx`, Author et Subject vides |
| `cv-maxime-girard-en.pdf` | `Maxime Girard CV EN 2026.docx` | vide | vide | Titre avec extension `.docx`, Author et Subject vides |

Valeurs proposées à la régénération des PDF : Title `Maxime Girard — CV — Directeur Marketing & Growth B2B` (FR) / `Maxime Girard — CV — B2B Marketing & Growth Director` (EN), Author `Maxime Girard`, Subject `{{A_COMPLETER: sujet du CV}}`.

## Indicateurs du hero (L3.2)

Résultats publiés dans `index.html`, utilisables pour `hero-kpi1` à `hero-kpi3` (texte à recopier sans modification) :
`+30 M€ ARR` (Camping Car Park), `+3 M€ ARR` (Eyelights), `+1 M€ ARR` (Sense4data), `+300% croissance YoY` (Eyelights), `+100k usagers` (Facebots), `+50 artistes signés` (InRealArt), `+80k leads` (cas EYERIDE), `1 M€/an` de budget d'acquisition (Eyelights).
Le cumul « Plus de 35 M€ d'ARR » figure dans la meta description et dans la FAQ.

## Proposition : remplacer les cartes de valeurs par trois blocs « Périmètre » (L3.3)

Les cartes Combatif / Ambitieux / Accessible sont conservées. Valeurs déjà publiées dans le parcours (lignes de `index.html` au commit du lot L3) :

| Bloc | Valeur publiée | Ligne source |
|---|---|---|
| Taille d'équipe managée | « Management d'une équipe de 5 personnes (chefs de projet, UI/UX designer, growth hacker) » (Sense4data) | 531 (`exp3-b4`) |
| Budget d'acquisition géré | « budget d'acquisition de 1 M€/an multi-agences (France, Japon, USA) » (Eyelights) | 549 (`exp4-b2`) |
| Nombre de pays opérés | « Pilotage des opérations marketing européennes : Allemagne, Espagne, Portugal, Pays-Bas, Belgique » (Camping Car Park, 5 pays) | 508 (`exp2-b1`) |
| Nombre de pays opérés (alternative) | « Lancement commercial sur 4 marchés simultanés : France, USA, Allemagne, Japon » (Eyelights, 4 marchés) | 550 (`exp4-b3`) |
| Nombre de pays opérés (alternative) | « SEO/GEO multi-pays (France, Italie, Espagne, Allemagne, Belgique) » (Pollen AM, 5 pays) | 469 (`exp0-b2`) |

Le nombre de pays opérés, toutes expériences confondues, n'est pas publié : à décider avant de choisir la valeur affichée.

## JSON-LD `Person` (L3.5)

- `worksFor` (Pollen AM, InRealArt) et `alumniOf` Inseec Business School : appliqués.
- `jobTitle` : `Head of Growth` et `Head of Performance` non ajoutés. Décision à prendre : valider l'ajout.
- `image` : reste `og-image.jpg`. `{{A_COMPLETER: photo portrait carrée, fichier /maxime-girard.webp}}` : à remplacer dans `index.html` (JSON-LD `Person.image`) une fois la photo fournie, puis relancer `build-en.py`.

## Pages de candidature `/c/*` (L5)

Décisions à prendre :
- `robots.txt` : `Disallow: /c/` non ajouté. Un `Disallow` empêche Google de lire le `noindex` ; sans `Disallow`, les pages `/c/*` restent accessibles aux robots, qui lisent `noindex, nofollow` et ne les indexent pas.
- Raison sociale exacte à valider : `Groupe Teddy Smith` (donnée fournie dans la demande), `BDL Club Invest` (déduit du slug `bdl-club-invest`, casse à confirmer).
- Intitulé de poste exact à valider : `Direction marketing & digital` (Teddy Smith), `Growth Marketing` (BDL Club Invest).

Actions hors code :
- Créer le webhook n8n, puis `npx wrangler secret put N8N_WEBHOOK_URL` et `npx wrangler deploy` dans `cloudflare-worker/`. Router la sortie n8n vers un e-mail ou Slack.
- Compléter `data/candidatures/<slug>.json`, puis `python3 scripts/new_application.py --all`.
- Diffuser chaque lien sous la forme `https://www.girardmaxime33.com/c/<slug>/?ref=<référent>`.

## Mesure des conversions (L6)

Décision à prendre : redondance Umami / Plausible. Les deux outils mesurent l'audience sans cookie et reçoivent les mêmes événements via `track()`. Ils reçoivent aussi chacun les événements de clic historiques (`data-umami-event` pour Umami, classes `plausible-event-name=…` pour Plausible). Rien n'a été supprimé. Options : conserver les deux, ou retenir un seul outil et retirer son script, ses attributs ou classes d'événements et sa ligne dans les deux pages de confidentialité.

Actions hors code :
- Plausible : déclarer dans Settings → Custom Properties les propriétés `section`, `question_index`, `suggestion`, `cv_location`, `cv_lang`, `utm_source`, `utm_medium`, `utm_campaign`, et créer des objectifs pour `Booking Slot Selected`, `Booking Confirmed`, `CV Download`, `Section Viewed`, `Chat Opened`, `Chat Question`, `Chat Suggestion Click`.
- GTM : créer les déclencheurs d'événement personnalisé `booking_slot_selected`, `booking_confirmed`, `cv_download`, `section_viewed`, `chat_opened`, `chat_question`, `chat_suggestion_click` (GTM ne les reçoit qu'après consentement).
- Calendly : les événements `calendly.date_and_time_selected` et `calendly.event_scheduled` sont émis par le widget inline ; vérifier en production avec un rendez-vous de test.

## Identification B2B des entreprises visiteuses (L7)

- Emplacement `loadB2BIdentification()` en commentaire dans le bloc de consentement d'`index.html` (segment « CONSENTEMENT COOKIES »), appels commentés après `loadClarity()` (cas `granted` et clic sur « Accepter »). Décommenter après avoir choisi le fournisseur (Dealfront, Snitcher ou Albacross) et renseigné l'URL du script et la clé.
- Pages de confidentialité FR et EN : la ligne du tableau « Cookies et traceurs » contient des placeholders (fournisseur, cookie). Elle annonce un traitement non actif tant que le script reste commenté : supprimer la ligne ou la compléter selon la décision.
- Au moment de l'activation : mettre à jour le texte du bandeau de consentement (`cookie-text` dans `t.fr` et `t.en`), qui ne cite aujourd'hui que Google Tag Manager et Microsoft Clarity.
- Hors code : contrat et DPA du fournisseur, base légale de l'identification par adresse IP.

## Récapitulatif des placeholders `{{A_COMPLETER}}` (fin du lot L8)

Fichiers sources (les pages `cas/*.html` et `c/*/index.html` sont générées depuis `data/`). Lignes au dernier commit.

| Fichier | Ligne | Placeholder |
|---|---|---|
| `index.html` | 310 | `{{A_COMPLETER: réponse sur la disponibilité}}` |
| `index.html` | 318 | `{{A_COMPLETER: réponse sur les postes et les secteurs}}` |
| `index.html` | 397 | `{{A_COMPLETER: Disponible à partir de … · CDI · Bordeaux / Nouvelle-Aquitaine / remote}}` |
| `index.html` | 405 | `{{A_COMPLETER: indicateur 1, à choisir parmi les résultats publiés}}` |
| `index.html` | 406 | `{{A_COMPLETER: indicateur 2, à choisir parmi les résultats publiés}}` |
| `index.html` | 407 | `{{A_COMPLETER: indicateur 3, à choisir parmi les résultats publiés}}` |
| `index.html` | 792 | `{{A_COMPLETER: réponse sur la disponibilité}}` |
| `index.html` | 796 | `{{A_COMPLETER: réponse sur les postes et les secteurs}}` |
| `index.html` | 891 | `{{A_COMPLETER: Disponible à partir de … · CDI · Bordeaux / Nouvelle-Aquitaine / remote}}` |
| `index.html` | 892 | `{{A_COMPLETER: indicateur 1, à choisir parmi les résultats publiés}}` |
| `index.html` | 893 | `{{A_COMPLETER: indicateur 2, à choisir parmi les résultats publiés}}` |
| `index.html` | 894 | `{{A_COMPLETER: indicateur 3, à choisir parmi les résultats publiés}}` |
| `index.html` | 1012 | `{{A_COMPLETER: réponse sur la disponibilité}}` |
| `index.html` | 1014 | `{{A_COMPLETER: réponse sur les postes et les secteurs}}` |
| `index.html` | 1062 | `{{A_COMPLETER: Available from … · Permanent contract · Bordeaux / Nouvelle-Aquitaine / remote}}` |
| `index.html` | 1063 | `{{A_COMPLETER: indicator 1, to pick among the published results}}` |
| `index.html` | 1064 | `{{A_COMPLETER: indicator 2, to pick among the published results}}` |
| `index.html` | 1065 | `{{A_COMPLETER: indicator 3, to pick among the published results}}` |
| `index.html` | 1183 | `{{A_COMPLETER: answer on availability}}` |
| `index.html` | 1185 | `{{A_COMPLETER: answer on roles and sectors}}` |
| `index.html` | 1274 | `{{A_COMPLETER: URL du script du fournisseur retenu}}` |
| `index.html` | 1275 | `{{A_COMPLETER: clé du fournisseur}}` |
| `llms.txt` | 3 | `{{A_COMPLETER: disponibilité, type de contrat, mobilité}}` |
| `llms.txt` | 7 | `{{A_COMPLETER: valider la liste}}` |
| `confidentialite.html` | 110 | `{{A_COMPLETER: Dealfront, Snitcher ou Albacross}}` |
| `confidentialite.html` | 112 | `{{A_COMPLETER: selon le fournisseur retenu}}` |
| `en/confidentialite.html` | 110 | `{{A_COMPLETER: Dealfront, Snitcher or Albacross}}` |
| `en/confidentialite.html` | 112 | `{{A_COMPLETER: depends on the selected provider}}` |
| `data/cas/camping-car-park-marketing-europe.json` | 19 | `{{A_COMPLETER: enjeu du poste}}` |
| `data/cas/camping-car-park-marketing-europe.json` | 42 | `{{A_COMPLETER: stack technique}}` |
| `data/cas/eyeride-crowdfunding-international.json` | 14 | `{{A_COMPLETER: contexte du projet}}` |
| `data/cas/eyeride-crowdfunding-international.json` | 19 | `{{A_COMPLETER: enjeu du projet}}` |
| `data/cas/eyeride-crowdfunding-international.json` | 44 | `{{A_COMPLETER: stack technique}}` |
| `data/cas/eyeride-crowdfunding-international.json` | 66 | `{{A_COMPLETER: durée du projet}}` |
| `data/cas/eyeride-crowdfunding-international.json` | 71 | `{{A_COMPLETER: rôle dans le projet}}` |
| `data/cas/sense4data-stack-marketing.json` | 19 | `{{A_COMPLETER: enjeu du poste}}` |
| `data/cas/sense4data-stack-marketing.json` | 42 | `{{A_COMPLETER: stack technique}}` |
| `data/cas/systeme-ia-multi-agent-marketing.json` | 14 | `{{A_COMPLETER: contexte du projet}}` |
| `data/cas/systeme-ia-multi-agent-marketing.json` | 19 | `{{A_COMPLETER: enjeu du projet}}` |
| `data/cas/systeme-ia-multi-agent-marketing.json` | 29 | `{{A_COMPLETER: stack technique}}` |
| `data/cas/systeme-ia-multi-agent-marketing.json` | 43 | `{{A_COMPLETER: résultats chiffrés}}` |
| `data/cas/systeme-ia-multi-agent-marketing.json` | 48 | `{{A_COMPLETER: durée du projet}}` |
| `data/cas/systeme-ia-multi-agent-marketing.json` | 53 | `{{A_COMPLETER: rôle dans le projet}}` |
| `data/cas/trambots-ia-transport.json` | 14 | `{{A_COMPLETER: contexte du projet}}` |
| `data/cas/trambots-ia-transport.json` | 19 | `{{A_COMPLETER: enjeu du projet}}` |
| `data/cas/trambots-ia-transport.json` | 32 | `{{A_COMPLETER: stack technique}}` |
| `data/cas/trambots-ia-transport.json` | 54 | `{{A_COMPLETER: durée du projet}}` |
| `data/cas/trambots-ia-transport.json` | 59 | `{{A_COMPLETER: rôle dans le projet}}` |
| `data/candidatures/bdl-club-invest.json` | 5 | `{{A_COMPLETER}}` |
| `data/candidatures/bdl-club-invest.json` | 6 | `{{A_COMPLETER}}` |
| `data/candidatures/bdl-club-invest.json` | 11 | `{{A_COMPLETER}}` |
| `data/candidatures/teddy-smith.json` | 5 | `{{A_COMPLETER}}` |
| `data/candidatures/teddy-smith.json` | 6 | `{{A_COMPLETER}}` |
| `data/candidatures/teddy-smith.json` | 11 | `{{A_COMPLETER}}` |
| `data/candidatures/ynov.json` | 6 | `{{A_COMPLETER}}` |
| `data/candidatures/ynov.json` | 11 | `{{A_COMPLETER}}` |

## Actions hors code

1. DNS chez le registrar.
   - Apex `girardmaxime33.com` : enregistrements A vers `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` ; enregistrements AAAA vers `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`.
   - `www` : CNAME vers `girardmaxime33000.github.io`.
   - Supprimer toute page de parking ou de redirection du registrar.
2. GitHub, Settings → Pages : domaine personnalisé `www.girardmaxime33.com`, vérification DNS validée, case « Enforce HTTPS » cochée.
3. Vérification du domaine dans GitHub (Settings → Pages → Verified domains), pour empêcher sa reprise.
4. Search Console (propriété de domaine) et Bing Webmaster Tools : soumettre `sitemap.xml`, puis inspecter `/` et `/en/`.
5. Retirer l'exclusion `girardmaxime33\.com` de `lychee` dans `.github/workflows/ci.yml` une fois le domaine joignable.
6. Créer le webhook n8n et notifier les consultations de `/c/*` par e-mail ou sur Slack (voir « Pages de candidature »).
7. Recréer les PDF de CV avec Title, Author et Subject renseignés (voir « Métadonnées des PDF de CV »).
