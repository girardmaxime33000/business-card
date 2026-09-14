// Cloudflare Worker — assistant IA du site (Workers AI, free tier).
// Reçoit { question } en POST, interroge un modèle open-source hébergé par
// Cloudflare via le binding AI, répond en JSON { answer }. Aucune clé API
// à gérer : le binding AI donne l'accès au modèle directement.

const ALLOWED_ORIGINS = [
  'https://girardmaxime33000.github.io',
  'http://localhost:8080',
];

const MODEL = '@cf/mistralai/mistral-small-3.1-24b-instruct';

const SYSTEM_PROMPT = `Tu es l'assistant du site personnel de Maxime Girard, Directeur Marketing & Growth B2B. Réponds UNIQUEMENT à partir des informations ci-dessous. Si la question sort de ce périmètre (profil professionnel de Maxime), dis poliment que tu ne peux répondre qu'à ce sujet. Réponds dans la langue de la question, en 2 à 4 phrases maximum, ton direct et professionnel, sans emoji.

--- PROFIL ---
Maxime Girard — Directeur Marketing & Growth B2B/B2B2C. 10 ans d'expérience, 5 mandats COMEX, +35M€ d'ARR généré ou piloté, marchés France/Europe/US/Japon.

Poste actuel : Founding Marketing Lead chez Pollen AM (startup industrielle, impression 3D pellets) — construction de la fonction marketing ex-nihilo, ABM grands comptes industriels (Airbus, Alstom, Sanofi déjà clients).

Parcours :
- Directeur Marketing Europe B2B, Camping Car Park (COMEX) — pilotage marketing sur 5 pays européens, +30M€ ARR, +30% croissance mois/mois.
- Directeur Marketing B2B, Sense4data (COMEX) — marketing mix modeling, +1M€ ARR, +10 MVP industrialisés.
- Directeur Croissance B2B2C, Eyelights (COMEX) — lancement sur 5 marchés (France, USA, Allemagne, UK, Japon), +3M€ ARR, +300% croissance YoY.
- Directeur Traffic B2B, Groupe Actiplay (COMEX) — acquisition pour Fnac, Cdiscount, BMW.
- Directeur Marketing B2B, Facebots (COMEX) — chatbots IA pour la SNCF et des métropoles.
- Jr Account Manager B2B2C, Sopexa — 3 ans à Tokyo, développement commercial marché japonais.

Compétences :
- Go-to-market & stratégie commerciale : positionnement, messaging, lancement produit, de l'amorçage au LBO.
- Acquisition & growth : SEO/SEA, lead gen, HubSpot/Pipedrive, LinkedIn/Meta/Google/TikTok Ads.
- Data & analytics : GA4, Looker Studio, Python (Pandas, NumPy).
- Automation & IA générative : Make, n8n, Claude API, agents LLM, intégrations MCP.
- Développement web : Python, JavaScript/TypeScript, REST API, GCP, Firebase.

Cas d'usage marquants :
- Trambots (2016) : première IA dédiée au transport en commun en France, connectée en 10 jours, +100k utilisateurs/jour.
- Campagne crowdfunding EYERIDE : 984k$ levés en 30 jours sur Indiegogo, 4 marchés simultanés.
- Système IA multi-agent marketing en production : orchestrateur Claude API, 9 agents spécialisés (SEO, Content, Ads, Analytics, Social, Email, Brand, Strategy, Lead Research).

Contact : email girard.maxime33@gmail.com, LinkedIn (lien "LinkedIn" sur le site), prise de rendez-vous via le bouton "Prendre RDV" (calendrier Calendly en bas de page).`;

function corsHeaders(origin) {
  const allowed = ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0];
  return {
    'Access-Control-Allow-Origin': allowed,
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Vary': 'Origin',
  };
}

export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin') || '';
    const headers = corsHeaders(origin);

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers });
    }
    if (request.method !== 'POST') {
      return new Response(JSON.stringify({ error: 'Method not allowed' }), {
        status: 405,
        headers: { ...headers, 'Content-Type': 'application/json' },
      });
    }

    let body;
    try {
      body = await request.json();
    } catch {
      return new Response(JSON.stringify({ error: 'Invalid JSON' }), {
        status: 400,
        headers: { ...headers, 'Content-Type': 'application/json' },
      });
    }

    const question = (body && body.question ? String(body.question) : '').trim().slice(0, 500);
    if (!question) {
      return new Response(JSON.stringify({ error: 'Question manquante' }), {
        status: 400,
        headers: { ...headers, 'Content-Type': 'application/json' },
      });
    }

    try {
      const result = await env.AI.run(MODEL, {
        messages: [
          { role: 'system', content: SYSTEM_PROMPT },
          { role: 'user', content: question },
        ],
        max_tokens: 300,
      });

      return new Response(JSON.stringify({ answer: (result && result.response) || '' }), {
        headers: { ...headers, 'Content-Type': 'application/json' },
      });
    } catch (err) {
      return new Response(JSON.stringify({ error: 'Erreur du modèle' }), {
        status: 502,
        headers: { ...headers, 'Content-Type': 'application/json' },
      });
    }
  },
};
