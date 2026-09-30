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

# Guillemets doubles (valeurs sur une ligne contenant une apostrophe, ex.
# "He's ..." ou "... Maxime's client") : sans cette passe, ces clés ne
# matchaient ni le pattern backticks ni le pattern guillemets simples
# ci-dessus et restaient silencieusement absentes de `en`, laissant le
# texte FR affiché tel quel sur la page anglaise.
for m in re.finditer(r"'([^']+)'\s*:\s*\"([^\"]*)\"", block):
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

# data-i18n-placeholder (attribut placeholder — ex. champ de saisie du chat)
def sub_i18n_placeholder(html, key, val):
    """Remplace le placeholder d'un élément portant data-i18n-placeholder="key".
    Suppose l'ordre d'attributs du gabarit source : data-i18n-placeholder="key"
    vient avant placeholder="...". """
    pattern = re.compile(
        r'(data-i18n-placeholder="' + re.escape(key) + r'"[^>]*?placeholder=")[^"]*(")'
    )
    return pattern.sub(lambda m: m.group(1) + val.replace('"', '&quot;') + m.group(2), html, count=1)

for key, val in en.items():
    out = sub_i18n_placeholder(out, key, val)

# ── 3. lang et métadonnées ─────────────────────────────────────────────────
EN_TITLE = "Maxime Girard | B2B Marketing Director, Growth &amp; Acquisition"
EN_DESC = "B2B Marketing &amp; Growth Director and Acquisition Manager based in Bordeaux. 10 years leading acquisition &amp; performance, +\u20ac35M ARR. SEA, CRO, tracking, AI."
EN_DESC_JSON = "B2B Marketing & Growth Director and Acquisition Manager based in Bordeaux. 10 years leading acquisition & performance, +\u20ac35M ARR. SEA, CRO, tracking, AI."
out = re.sub(r'<html lang="fr"', '<html lang="en"', out, count=1)

out = re.sub(r'<title>[^<]*</title>',
    lambda m: '<title>' + EN_TITLE + '</title>', out, count=1)

out = re.sub(r'(<meta name="description" content=")[^"]*(")',
    lambda m: m.group(1) + EN_DESC + m.group(2),
    out, count=1)

out = re.sub(r'(<link rel="canonical" href=")[^"]*(")',
    r'\g<1>https://www.girardmaxime33.com/en/\2', out, count=1)

out = out.replace(
    '<meta property="og:locale" content="fr_FR">',
    '<meta property="og:locale" content="en_US">', 1)
out = out.replace(
    '<meta property="og:locale:alternate" content="en_US">',
    '<meta property="og:locale:alternate" content="fr_FR">', 1)

out = re.sub(r'(<meta property="og:url" content=")[^"]*(")',
    r'\g<1>https://www.girardmaxime33.com/en/\2', out, count=1)

out = re.sub(r'(<meta property="og:title" content=")[^"]*(")',
    lambda m: m.group(1) + EN_TITLE + m.group(2), out, count=1)

out = re.sub(r'(<meta property="og:description" content=")[^"]*(")',
    lambda m: m.group(1) + EN_DESC + m.group(2),
    out, count=1)

out = re.sub(r'(<meta property="og:image:alt" content=")[^"]*(")',
    r'\g<1>Maxime Girard — B2B Marketing Director, Growth &amp; Acquisition, Bordeaux\2', out, count=1)

out = re.sub(r'(<meta name="twitter:title" content=")[^"]*(")',
    lambda m: m.group(1) + EN_TITLE + m.group(2), out, count=1)

out = re.sub(r'(<meta name="twitter:description" content=")[^"]*(")',
    lambda m: m.group(1) + EN_DESC + m.group(2),
    out, count=1)

# JSON-LD : parsé avec json (KeyError bruyant si la structure dérive) plutôt
# que des .replace() littéraux qui se taisent dès que le texte FR source
# change. Les textes EN viennent du dict `en` (t.en) — source de traduction
# unique, pas de texte EN dupliqué dans ce script (sauf métadonnées ci-dessus).
import json
_ld = re.search(r'(<script type="application/ld\+json">\n)(.*?)(\n</script>)', out, re.DOTALL)
_data = json.loads(_ld.group(2))
_nodes = {n["@type"]: n for n in _data["@graph"]}

_nodes["WebSite"]["name"] = "Maxime Girard — Marketing & Growth Director B2B"
_nodes["WebSite"]["inLanguage"] = "en-US"
_nodes["ProfilePage"]["name"] = "Maxime Girard | B2B Marketing Director, Growth & Acquisition"
_nodes["ProfilePage"]["inLanguage"] = "en-US"
_nodes["ProfilePage"]["url"] = "https://www.girardmaxime33.com/en/"

_person = _nodes["Person"]
_person["jobTitle"] = ["Marketing & Growth Director B2B", "B2B Growth Marketing Expert", "Acquisition Manager"]
_person["alternateName"] = ["Maxime Girard Marketing Director", "Maxime Girard Growth Expert"]
_person["description"] = EN_DESC_JSON
_person["hasOccupation"]["name"] = "Marketing & Growth Director B2B"
_person["hasOccupation"]["skills"] = "Acquisition strategy, lead generation, SEA, Social Ads, SEO, CRO, tracking & data, marketing automation"

_review_keys = {
    'Nicolas Pasetti': 'ref1-text',
    'Alexandre Masson': 'ref2-text',
    'Pierre Rocherie': 'ref3-text',
    'Jérémy Fortinon': 'ref4-text',
}
for _r in _person["review"]:
    _r["reviewBody"] = en[_review_keys[_r["author"]["name"]]]

_faq = _nodes["FAQPage"]
_faq["inLanguage"] = "en-US"
for _i, _q in enumerate(_faq["mainEntity"], 1):
    _q["name"] = en[f"faq-q{_i}"]
    _q["acceptedAnswer"]["text"] = en[f"faq-a{_i}"]

out = (out[:_ld.start(2)]
       + json.dumps(_data, ensure_ascii=False, indent=2)
       + out[_ld.end(2):])

# ── 4. Chemins relatifs (depuis en/) ──────────────────────────────────────
out = out.replace('href="favicon.svg"',              'href="../favicon.svg"',              1)
out = out.replace('href="tailwind.css"',             'href="../tailwind.css"',             1)
# index.html (FR) lie le CV FR ; la page EN doit toujours offrir le CV EN,
# quel que soit le lien source — d'où un remplacement fixe plutôt qu'un
# simple ajout de "../" devant le nom de fichier existant.
out = out.replace('href="cv-maxime-girard-fr.pdf"',  'href="../cv-maxime-girard-en.pdf"')
out = re.sub(r'src="logos/', 'src="../logos/', out)
out = re.sub(r'src="testimonials/', 'src="../testimonials/', out)

# ── 5. Lang toggle : EN actif, FR inactif ─────────────────────────────────
# Basé sur data-lang plutôt que sur la liste exacte des classes, pour rester
# robuste aux classes Tailwind ajoutées au bouton actif (bg-lime-400, text-black…).
def _deactivate_lang_btn(m):
    tag = m.group(0)
    tag = re.sub(r'\bactive\s+bg-lime-400\s+text-black\s+', '', tag)
    # aria-current="page" ne doit exister que sur le lien de la langue
    # affichée — pas de valeur "false" en ARIA, on retire l'attribut.
    tag = re.sub(r'\s*aria-current="page"', '', tag)
    return tag

def _activate_lang_btn(m):
    tag = m.group(0)
    if re.search(r'class="lang-btn\s+active\b', tag) is None:
        tag = re.sub(r'class="lang-btn\s+', 'class="lang-btn active bg-lime-400 text-black ', tag, count=1)
    if 'aria-current="page"' not in tag:
        tag = re.sub(r'(\bdata-lang="en")', r'\1 aria-current="page"', tag, count=1)
    return tag

out = re.sub(r'<a\b[^>]*\bdata-lang="fr"[^>]*>', _deactivate_lang_btn, out, count=1)
out = re.sub(r'<a\b[^>]*\bdata-lang="en"[^>]*>', _activate_lang_btn, out, count=1)

# ── 6. Script ──────────────────────────────────────────────────────────────
# Le script principal est conservé tel quel : au-delà de la traduction (déjà
# statique dans le HTML à ce stade), il porte aussi le scrollspy, le menu
# mobile, le widget d'assistant et le chargement différé de Calendly — des
# fonctionnalités communes aux deux langues, pas seulement de l'i18n. L'objet
# `t` reste dans le fichier : c'est la source de traduction lue par ce script
# (section 1 ci-dessus), pas un mécanisme de bascule de langue en direct dans
# le navigateur (supprimé — chaque langue est servie par sa propre page).

# ── 7. Écrire ──────────────────────────────────────────────────────────────
os.makedirs(os.path.dirname(DST), exist_ok=True)
with open(DST, "w", encoding="utf-8") as f:
    f.write(out)

print(f"✓ {DST} ({len(out):,} chars)")

# ── 8. sitemap.xml : lastmod à la date du build ────────────────────────────
# Évite qu'une date figée dérive silencieusement au fil des modifications de
# contenu — ce script tourne déjà à chaque changement d'index.html (voir
# README), c'est le point naturel pour republier ces dates.
import datetime
SITEMAP = os.path.join(os.path.dirname(SRC), "sitemap.xml")
if os.path.exists(SITEMAP):
    with open(SITEMAP, encoding="utf-8") as f:
        sitemap = f.read()
    today = datetime.date.today().isoformat()
    sitemap, n = re.subn(r"<lastmod>[^<]*</lastmod>", f"<lastmod>{today}</lastmod>", sitemap)
    with open(SITEMAP, "w", encoding="utf-8") as f:
        f.write(sitemap)
    print(f"✓ {SITEMAP} ({n} lastmod → {today})")
