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
