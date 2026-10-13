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
