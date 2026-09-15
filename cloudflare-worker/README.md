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
requêtes. **Désactivé par défaut** (le code tourne sans erreur, sans
limite, tant que le binding n'existe pas) : activer une seule fois,
après le premier déploiement.

```bash
cd cloudflare-worker
npx wrangler kv namespace create RATE_LIMIT
```

La commande affiche un id. Décommenter le bloc `[[kv_namespaces]]` dans
`wrangler.toml`, y coller cet id, puis redéployer :

```bash
npx wrangler deploy
```
