# Assistant IA — Cloudflare Worker

Backend gratuit de l'assistant conversationnel du site (Cloudflare Workers AI,
modèle `@cf/meta/llama-3.1-8b-instruct`). Aucune clé API à stocker : le
binding `AI` donne l'accès au modèle directement depuis le compte Cloudflare.

## Déploiement (2 min, compte Cloudflare gratuit, sans CB)

```bash
cd cloudflare-worker
npx wrangler login        # ouvre le navigateur, connecte le compte Cloudflare
npx wrangler deploy       # publie le Worker sur *.workers.dev
```

La commande affiche l'URL publiée, du type :

```
https://maxime-girard-assistant.<ton-sous-domaine>.workers.dev
```

## Activation côté site

Dans `index.html`, remplacer la constante `CHAT_ENDPOINT` (recherche
`CHAT_ENDPOINT`) par cette URL, puis commit + push. Tant que l'URL n'est
pas renseignée, le widget affiche un message d'erreur avec un lien de repli
vers l'email/Calendly — il ne casse rien.

## Limites du palier gratuit

10 000 "neurons" par jour (largement suffisant pour un site personnel).
Pas de carte bancaire requise pour rester sur ce palier.

## Rate limiting

Le Worker limite chaque IP à 10 requêtes / 5 minutes (voir
`RATE_LIMIT_WINDOW_SECONDS` / `RATE_LIMIT_MAX_REQUESTS` dans
`chat-worker.js`) — protège le quota gratuit ci-dessus d'un bourrage de
requêtes. **Actif** : le namespace KV `RATE_LIMIT` est créé et lié dans
`wrangler.toml`. Si le binding venait à être retiré du fichier de config,
le code tourne quand même sans erreur, simplement sans limite (fail
open) — pas de blocage du chat en cas de régression sur ce point.

Redéployer après toute modification touchant ce mécanisme :

```bash
cd cloudflare-worker
npx wrangler deploy
```

## Route `POST /notify` (alerte de consultation des pages de candidature)

Les pages `/c/<slug>/` (générées par `scripts/new_application.py`, `noindex`)
appellent cette route une fois par session au chargement.

| Élément | Valeur |
|---|---|
| Méthode et chemin | `POST /notify` |
| Corps JSON | `{"slug": "ynov", "ref": "linkedin", "ts": "2026-10-13T10:00:00.000Z"}` |
| `slug` | requis, `^[a-z0-9]+(-[a-z0-9]+)*$`, 64 caractères au plus |
| `ref` | optionnel, caractères `A-Za-z0-9._-` conservés, 64 au plus (paramètre `?ref=` de l'URL de la page) |
| `ts` | optionnel, date ISO 8601 ; remplacé par l'heure du Worker si absent ou invalide |
| Origines acceptées | celles de `ALLOWED_ORIGINS` (sinon `403`) |
| Limitation de débit | compteur KV `RATE_LIMIT` existant (10 requêtes / 5 minutes / IP), clé séparée `nt:<ip>:<fenêtre>` de celle du chat (`429` au-delà) |
| Relais | `POST` JSON `{slug, ref, ts}` vers le secret `N8N_WEBHOOK_URL` |
| Réponses | `200 {"ok": true}`, `400` corps ou slug invalide, `403` origine, `429` limite, `502` webhook en échec, `503` secret absent |

Aucune adresse IP ni aucun user-agent n'est transmis au webhook ; l'IP ne
sert qu'à la clé du compteur KV (TTL 5 minutes).

### Secret `N8N_WEBHOOK_URL`

```bash
cd cloudflare-worker
npx wrangler secret put N8N_WEBHOOK_URL   # colle l'URL du webhook n8n à l'invite
npx wrangler deploy
```

L'URL du webhook n'est écrite dans aucun fichier du dépôt. Tant que le
secret n'existe pas, la route répond `503` et les pages de candidature
continuent de s'afficher normalement (la notification échoue sans effet
visible).
