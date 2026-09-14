// Source unique des données du profil de Maxime Girard, utilisée par
// chat-worker.js pour construire le system prompt. Modifier CE fichier
// quand le CV/le site change — ne pas dupliquer le texte ailleurs dans
// chat-worker.js. Les mêmes faits sont maintenus séparément dans
// index.html (site statique, pas de build step) : garder les deux
// synchronisés à la main quand le contenu du CV évolue.

export const PROFILE = {
  identity: {
    name: 'Maxime Girard',
    title: 'Directeur Marketing & Growth — B2B / B2B2C',
    location: 'Bordeaux, France',
    email: 'girard.maxime33@gmail.com',
    linkedin: 'https://www.linkedin.com/in/maxime-girard-head-of-marketing/',
    booking: 'Bouton "Prendre RDV" du site → calendrier Calendly en bas de page',
  },

  metrics: [
    '+35 M€ d’ARR généré ou piloté',
    '5 marchés internationaux ouverts',
    '5 mandats COMEX (Comité Exécutif)',
    '10 ans de direction marketing B2B',
  ],

  pitch: 'Profil hybride stratégie / data / automatisation. Je construis des systèmes marketing qui génèrent de la croissance mesurable. Vision CMO + exécution growth engineer : je code, j’automatise, je pilote les données, je structure les équipes. J’ai opéré en startup en amorçage, en scale-up en hypercroissance et en PME en structuration, avec des résultats mesurables à chaque stade. Périmètre France, Europe, US et Japon.',

  traits: [
    { title: 'Combatif', desc: 'Détermination à relever les défis et à se dépasser. Encourage persévérance, audace et esprit d’initiative dans les équipes.' },
    { title: 'Ambitieux', desc: 'Vision orientée impact immédiat. Inspire l’excellence et anticipe les besoins futurs des clients et des marchés.' },
    { title: 'Accessible', desc: 'Approche inclusive, simplicité et proximité avec toutes les parties. Peut communiquer avec des profils techniques et non techniques.' },
  ],

  experiences: [
    {
      period: 'Avr. 2026 — Aujourd’hui',
      company: 'Pollen AM',
      type: 'Startup industrielle · Impression 3D pellets',
      title: 'Founding Marketing Lead',
      comex: false,
      bullets: [
        'Construction de la fonction marketing ex-nihilo : positionnement, messaging, demand gen, ABM grands comptes industriels',
        'Budget marketing ~€100–150k, priorité salons industriels (Formnext, Global Industrie) et contenu technique B2B',
        'Cibles : fabricants aéronautique, ferroviaire, pharmaceutique (Airbus, Alstom, Sanofi déjà clients)',
      ],
      result: 'En ramp-up · Q2–Q3 2026',
    },
    {
      period: 'Jan. 2025 – Nov. 2025',
      company: 'Camping Car Park',
      type: 'PME · Tourisme · SaaS',
      title: 'Directeur Marketing Europe B2B',
      comex: true,
      bullets: [
        'Pilotage des opérations marketing européennes : Allemagne, Benelux, Espagne, Portugal, Autriche',
        'Responsabilité directe du budget marketing européen, arbitrages stratégiques, reporting au CMO et CEO',
        'Campagnes B2B ciblant 700+ collectivités locales — CRM, RP, lobbying',
      ],
      result: '+30 M€ ARR · +30% croissance mois/mois',
    },
    {
      period: '2021 – 2024',
      company: 'Sense4data',
      type: 'PME · Conseil · RA OEM',
      title: 'Directeur Marketing B2B',
      comex: true,
      bullets: [
        'Pilotage du marketing mix modeling interne et externe, impact direct sur la priorisation commerciale et l’allocation des ressources — clients PME & ETI (Eurofeu, Réseau CCI, Cegid)',
        'Définition de la stratégie de positionnement, messaging et offre commerciale',
        'Supervision de la génération de leads, du suivi commercial et de l’expérience client',
      ],
      result: '+1 M€ ARR · +10 MVP industrialisés',
    },
    {
      period: '2020 – 2021',
      company: 'Eyelights',
      type: 'Scale-up · IoT & AR',
      title: 'Directeur Croissance B2B2C',
      comex: true,
      bullets: [
        'Lancement commercial sur 5 marchés : France, USA, Allemagne, UK, Japon',
        '+200M d’impressions, +80k leads collectés, 1M$ investis en SEA',
        'Conception et déploiement d’un chatbot interne visant l’automatisation des opérations marketing, produit et SAV, avec gains de productivité mesurables',
      ],
      result: '+3M€ ARR · +300% croissance YoY',
    },
    {
      period: '2019 – 2020',
      company: 'Groupe Actiplay',
      type: 'Agence Marketing',
      title: 'Directeur Traffic B2B',
      comex: true,
      bullets: [
        'Stratégie d’acquisition et supervision des campagnes clients (Fnac, Cdiscount, BMW)',
        'Développement des outils de collecte de données',
      ],
      result: '300 k€ ARR · +220% performance collecte',
    },
    {
      period: '2016 – 2018',
      company: 'Facebots',
      type: 'Startup · Chatbot & IA',
      title: 'Directeur Marketing B2B',
      comex: true,
      bullets: [
        'Offre commerciale chatbots & AI Flows — SNCF, Métropoles',
        'Arbitrage technologique, supervision des intégrations API',
      ],
      result: '300 k€ levés · 2 appels d’offres publics remportés',
    },
    {
      period: '2012 – 2015',
      company: 'Sopexa',
      type: 'Multinationale · Tokyo, Japon',
      title: 'Jr Account Manager B2B2C',
      comex: false,
      bullets: [
        'Développement commercial et marketing sur le marché japonais',
        'Gestion de comptes internationaux français et américains',
        '3 ans en environnement multiculturel — première exposition internationale longue durée',
      ],
      result: null,
    },
  ],

  cases: [
    {
      title: 'Première IA Transport en Commun',
      text: 'En 2016, connexion de Facebook Messenger aux API des transporteurs de Bordeaux Métropole en 10 jours. Trambots est devenu la première IA dédiée au transport en commun en France — croissance 100% organique via presse nationale.',
      stats: ['+100k utilisateurs/jour', '30 métropoles couvertes', '+1M messages/jour', 'Devant SNCF & Expédia en usage'],
    },
    {
      title: 'Growth & Crowdfunding International',
      text: 'Pour le lancement d’EYERIDE chez Eyelights, pilotage de l’ensemble de la stratégie growth et paid sur 4 marchés simultanément. Campagne Indiegogo réussie à 984k$ sur 30 jours, +3M€ de CA générés en 3 mois.',
      stats: ['+200M impressions', '+80k leads', '1M$ de budget SEA investi', '4 marchés simultanés'],
    },
    {
      title: 'Système IA Multi-agent Marketing',
      text: 'Système autonome d’automatisation marketing déployé en production : orchestrateur Claude API + Trello comme file de tâches, 9 agents spécialisés (SEO, Content, Ads, Analytics, Social, Email, Brand, Strategy, Lead Research), versionning automatique sur Git.',
      stats: ['9 agents spécialisés', 'Orchestrateur Claude API', 'Production autonome', 'Déployé en production'],
    },
  ],

  skills: [
    { title: 'Go-to-market & Stratégie commerciale', tools: 'Positionnement, messaging, lancement produit, structuration des offres, partenariats, marchés B2B et B2B2C — de l’amorçage au LBO' },
    { title: 'Acquisition & Growth', tools: 'SEO / SEA, lead generation, CRM (HubSpot, Pipedrive, Zoho, Klaviyo), campagnes multi-canal, LinkedIn Ads, Meta, Google Ads, TikTok' },
    { title: 'Data & Analytics', tools: 'GA4, Looker Studio, Metabase, tracking avancé (GTM, Umami.js, Hotjar, Clarity), Excel VBA, Google Sheets AppScript, Python (Pandas, NumPy)' },
    { title: 'Automation & IA Générative', tools: 'Make, n8n, Zapier, Claude API, ChatGPT, Gemini, Cursor — conception de workflows autonomes, agents LLM, intégrations MCP' },
    { title: 'Développement Web', tools: 'Python, JavaScript / TypeScript, REST API, Google Cloud Platform, WordPress, Firebase, GitHub, Jupyter — autonome de la spec au déploiement' },
  ],

  testimonials: [
    { text: 'Il est constamment en train d’innover et de rechercher les innovations qui lui permettront d’aller plus loin. C’est un profil ultra intéressant pour contribuer à faire grossir une entreprise.', name: 'Nicolas Pasetti', role: 'CEO, eteam_work — a managé Maxime directement' },
    { text: 'Sur le plan technique, Maxime est extrêmement compétent. Il maîtrise Python et JavaScript, et ses compétences en scraping et automatisation sont remarquables pour un directeur marketing.', name: 'Alexandre Masson', role: 'Data Engineer, ColisPrivé — a reporté à Maxime' },
    { text: 'Toujours plusieurs coups d’avance, c’est ça qu’on aime chez lui ! Son analyse est très pointue sur des sujets concernant le marketing, le management et la growth pure.', name: 'Pierre Rocherie', role: 'Directeur Général, FM Auto' },
    { text: 'Il connaît très bien son marché, son positionnement et les enjeux technologiques et commerciaux de ses clients. Il est passionné par son métier, extrêmement curieux — cela facilite grandement les échanges.', name: 'Jérémy Fortinon', role: 'Expert transformation des SI — client de Maxime' },
  ],
};
