// Cloudflare Worker — assistant IA du site (Workers AI, free tier).
// Reçoit { question } en POST, interroge un modèle open-source hébergé par
// Cloudflare via le binding AI, répond en JSON { answer }. Aucune clé API
// à gérer : le binding AI donne l'accès au modèle directement.
//
// Les données du profil vivent dans profile-data.js (source unique) —
// ce fichier ne fait que les sérialiser en system prompt. Ne pas
// réintroduire de texte profil codé en dur ici : modifier profile-data.js.

import { PROFILE } from './profile-data.js';

const ALLOWED_ORIGINS = [
  'https://www.girardmaxime33.com',
  'https://girardmaxime33.com',
  'https://girardmaxime33000.github.io',
  'http://localhost:8080',
];

const MODEL = '@cf/mistralai/mistral-small-3.1-24b-instruct';

function buildSystemPrompt(profile) {
  const expLines = profile.experiences.map(e => {
    const label = e.comex ? `${e.title} (COMEX)` : e.title;
    const bullets = e.bullets.map(b => `  · ${b}`).join('\n');
    const result = e.result ? `\n  Résultat : ${e.result}` : '';
    return `- ${e.period} — ${label}, ${e.company} (${e.type})\n${bullets}${result}`;
  }).join('\n\n');

  const caseLines = profile.cases.map((c, i) =>
    `${i + 1}. ${c.title} — ${c.text} Chiffres clés : ${c.stats.join(', ')}.`
  ).join('\n\n');

  const skillLines = profile.skills.map(s => `- ${s.title} : ${s.tools}`).join('\n');

  const traitLines = profile.traits.map(t => `- ${t.title} : ${t.desc}`).join('\n');

  const testimonialLines = profile.testimonials.map(t =>
    `- « ${t.text} » — ${t.name}, ${t.role}.`
  ).join('\n');

  return `Tu es l'assistant du site personnel de ${profile.identity.name}, ${profile.identity.title}. Réponds UNIQUEMENT à partir des informations ci-dessous. Si la question sort de ce périmètre (profil professionnel de ${profile.identity.name}), dis poliment que tu ne peux répondre qu'à ce sujet. Réponds dans la langue de la question, en 2 à 5 phrases maximum, ton direct et professionnel, sans emoji.

--- PROFIL ---
${profile.identity.name} — ${profile.identity.title}. ${profile.identity.location}.
${profile.metrics.join(' · ')}.

${profile.pitch}

Traits de personnalité :
${traitLines}

--- PARCOURS (du plus récent au plus ancien) ---
${expLines}

--- CAS D'USAGE MARQUANTS ---
${caseLines}

--- COMPÉTENCES ---
${skillLines}

--- TÉMOIGNAGES ---
${testimonialLines}

--- CONTACT ---
Email : ${profile.identity.email}
LinkedIn : ${profile.identity.linkedin}
Prise de rendez-vous : ${profile.identity.booking}`;
}

const SYSTEM_PROMPT = buildSystemPrompt(PROFILE);

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
