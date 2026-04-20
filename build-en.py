#!/usr/bin/env python3
"""
Génère en/index.html depuis index.html en appliquant les traductions t.en.
Usage : python3 build-en.py
"""
import re, os

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
DST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "en", "index.html")

with open(SRC, encoding="utf-8") as f:
    src = f.read()

# ── 1. Extraire t.en depuis le JS ──────────────────────────────────────────
# On extrait clé par clé avec un pattern simple : 'key': 'value' ou 'key': `value`
en = {}
en_section = re.search(r"en:\s*\{(.+?)\n  \}\n\};", src, re.DOTALL)
if not en_section:
    raise ValueError("Bloc t.en introuvable")

block = en_section.group(1)

# Template literals (backticks, potentiellement multi-lignes)
for m in re.finditer(r"'([^']+)'\s*:\s*`(.*?)`", block, re.DOTALL):
    en[m.group(1)] = m.group(2).strip()

# Guillemets simples (valeurs sur une ligne)
for m in re.finditer(r"'([^']+)'\s*:\s*'([^']*)'", block):
    if m.group(1) not in en:
        en[m.group(1)] = m.group(2)

print(f"  {len(en)} clés EN extraites")

# ── 2. Appliquer les traductions dans le HTML ──────────────────────────────
out = src

def sub_i18n(html, key, val, is_html=False):
    """Remplace le contenu d'un élément portant data-i18n[[-html]]="key"."""
    attr = 'data-i18n-html' if is_html else 'data-i18n'
    # Trouver l'ouverture du tag : <TAG ...data-i18n[-html]="key"...>
    tag_open = re.search(
        r'<(\w+)[^>]*' + re.escape(attr) + r'="' + re.escape(key) + r'"[^>]*>',
        html
    )
    if not tag_open:
        return html
    tag_name = tag_open.group(1)
    start = tag_open.start()
    end_open = tag_open.end()

    # Trouver la fermeture correspondante (depth=0)
    depth = 1
    pos = end_open
    while depth > 0 and pos < len(html):
        nxt_open  = re.search(r'<'  + tag_name + r'[\s>]', html[pos:])
        nxt_close = re.search(r'</' + tag_name + r'\s*>',   html[pos:])
        if nxt_close is None:
            break
        if nxt_open and nxt_open.start() < nxt_close.start():
            depth += 1
            pos += nxt_open.end()
        else:
            depth -= 1
            if depth == 0:
                close_start = pos + nxt_close.start()
                close_end   = pos + nxt_close.end()
                new_inner = val if is_html else val
                return html[:end_open] + new_inner + html[close_start:]
            pos += nxt_close.end()
    return html

# data-i18n-html (innerHTML)
for key, val in en.items():
    out = sub_i18n(out, key, val, is_html=True)

# data-i18n (textContent — valeurs sans HTML uniquement)
for key, val in en.items():
    if "<" not in val:
        out = sub_i18n(out, key, val, is_html=False)

# ── 3. lang et métadonnées ─────────────────────────────────────────────────
out = out.replace('<html lang="fr">', '<html lang="en">', 1)

out = re.sub(r'<title>[^<]*</title>',
    '<title>Maxime Girard | Marketing &amp; Growth Director B2B — Bordeaux</title>',
    out, count=1)

out = re.sub(r'(<meta name="description" content=")[^"]*(")',
    lambda m: m.group(1) + 'Marketing &amp; Growth Director B2B \u2014 10 years, 5 Exec. Committees, '
    '+35M\u20ac ARR. Strategist AND practitioner, B2B/B2B2C. France, Europe, US, Japan.' + m.group(2),
    out, count=1)

out = re.sub(r'(<link rel="canonical" href=")[^"]*(")',
    r'\g<1>https://girardmaxime33000.github.io/business-card/en/\2', out, count=1)

out = out.replace(
    '<meta property="og:locale" content="fr_FR">',
    '<meta property="og:locale" content="en_US">', 1)
out = out.replace(
    '<meta property="og:locale:alternate" content="en_US">',
    '<meta property="og:locale:alternate" content="fr_FR">', 1)

out = re.sub(r'(<meta property="og:url" content=")[^"]*(")',
    r'\g<1>https://girardmaxime33000.github.io/business-card/en/\2', out, count=1)

out = re.sub(r'(<meta property="og:title" content=")[^"]*(")',
    r'\g<1>Maxime Girard | Marketing &amp; Growth Director B2B — Bordeaux\2', out, count=1)

out = re.sub(r'(<meta property="og:description" content=")[^"]*(")',
    lambda m: m.group(1) + 'Marketing &amp; Growth Director B2B \u2014 10 years, 5 Exec. Committees, '
    '+35M\u20ac ARR. Strategist AND practitioner, B2B/B2B2C.' + m.group(2),
    out, count=1)

out = re.sub(r'(<meta property="og:image:alt" content=")[^"]*(")',
    r'\g<1>Maxime Girard — Marketing &amp; Growth Director B2B, Bordeaux\2', out, count=1)

out = re.sub(r'(<meta name="twitter:title" content=")[^"]*(")',
    r'\g<1>Maxime Girard | Marketing &amp; Growth Director B2B — Bordeaux\2', out, count=1)

out = re.sub(r'(<meta name="twitter:description" content=")[^"]*(")',
    lambda m: m.group(1) + 'Marketing &amp; Growth Director B2B \u2014 10 years, 5 Exec. Committees, '
    '+35M\u20ac ARR. Strategist AND practitioner, B2B/B2B2C.' + m.group(2),
    out, count=1)

out = out.replace(
    '"jobTitle": "Directeur Marketing & Growth B2B"',
    '"jobTitle": "Marketing & Growth Director B2B"', 1)
out = out.replace(
    '"description": "Directeur Marketing & Growth B2B — 10 ans d\'expérience, '
    '5 COMEX, +35M€ ARR. Stratège ET technicien, B2B/B2B2C. France, Europe, US, Japon."',
    '"description": "Marketing & Growth Director B2B — 10 years, '
    '5 Exec. Committees, +35M€ ARR. Strategist AND practitioner, B2B/B2B2C. France, Europe, US, Japan."',
    1)

# ── 4. Chemins relatifs (depuis en/) ──────────────────────────────────────
out = out.replace('href="favicon.svg"',              'href="../favicon.svg"',              1)
out = out.replace('href="cv-maxime-girard-fr.pdf"',  'href="../cv-maxime-girard-en.pdf"')
out = out.replace('href="cv-maxime-girard-en.pdf"',  'href="../cv-maxime-girard-en.pdf"')

# ── 5. Lang toggle : EN actif, FR inactif ─────────────────────────────────
out = out.replace(
    'class="lang-btn active" data-lang="fr" aria-pressed="true"',
    'class="lang-btn"        data-lang="fr" aria-pressed="false"', 1)
out = out.replace(
    'class="lang-btn" data-lang="en" aria-pressed="false"',
    'class="lang-btn active" data-lang="en" aria-pressed="true"', 1)

# ── 6. Supprimer le système i18n JS (contenu déjà statique) ───────────────
minimal_script = '''<script>
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
}, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
document.querySelectorAll('#hero .reveal').forEach((el, i) => {
  setTimeout(() => el.classList.add('visible'), 100 + i * 100);
});
</script>'''

out = re.sub(r'<script>\s*// ── TRANSLATIONS ──.*?</script>',
             minimal_script, out, flags=re.DOTALL, count=1)

# ── 7. Écrire ──────────────────────────────────────────────────────────────
os.makedirs(os.path.dirname(DST), exist_ok=True)
with open(DST, "w", encoding="utf-8") as f:
    f.write(out)

print(f"✓ {DST} ({len(out):,} chars)")
