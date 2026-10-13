#!/usr/bin/env python3
"""
Fragments partagés entre index.html et les pages générées (cas/*.html,
c/<slug>/index.html).

Les pages générées reprennent depuis index.html : le <style> de tête, les
scripts de mesure, le header, le pied de page, le bandeau de consentement et
les segments de script (consentement, mesure, clic CV, horloge, menu mobile,
année). Rien n'est recopié à la main : un changement dans index.html se
propage au prochain lancement de build_cas.py / new_application.py, et la CI
(job build-check) échoue si le résultat committé diverge.
"""
import html
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.girardmaxime33.com"

with open(os.path.join(ROOT, "index.html"), encoding="utf-8") as _f:
    INDEX = _f.read()


def esc(text):
    return html.escape(text, quote=False)


def esc_attr(text):
    return html.escape(text, quote=True)


# ── Traductions FR (t.fr) ──────────────────────────────────────────────────
def t_fr():
    start = INDEX.index("  fr: {")
    end = INDEX.index("\n  },", start)
    block = INDEX[start:end]
    out = {}
    pat = re.compile(
        r"^    '([^']+)':\s*(?:'((?:[^'\\]|\\.)*)'|\"((?:[^\"\\]|\\.)*)\"|`(.*?)`)\s*,?\s*$",
        re.M | re.S,
    )
    for m in pat.finditer(block):
        if m.group(2) is not None:
            out[m.group(1)] = m.group(2).replace("\\'", "'")
        elif m.group(3) is not None:
            out[m.group(1)] = m.group(3).replace('\\"', '"')
        else:
            out[m.group(1)] = m.group(4)
    return out


# ── Fragments HTML ─────────────────────────────────────────────────────────
def _strip_i18n(fragment):
    return re.sub(r'\s+data-i18n(?:-html|-placeholder|-alt)?="[^"]*"', "", fragment)


def _root_hrefs(fragment):
    fragment = re.sub(r'href="#(?!main-content)([a-z-]+)"', r'href="/#\1"', fragment)
    fragment = fragment.replace('href="cv-maxime-girard-fr.pdf"', 'href="/cv-maxime-girard-fr.pdf"')
    return fragment


def header():
    m = re.search(r"<header .*?</header>", INDEX, re.S)
    return _root_hrefs(_strip_i18n(m.group(0)))


def footer():
    m = re.search(r"<footer .*?</footer>", INDEX, re.S)
    frag = _strip_i18n(m.group(0)).replace('href="#hero"', 'href="#main-content"')
    return frag


def cookie_banner():
    m = re.search(r'<div id="cookie-consent".*?\n</div>\n</div>\n', INDEX, re.S)
    return _strip_i18n(m.group(0)).rstrip("\n")


def head_shared():
    """Polices, CSS, <style> et scripts de mesure, identiques à index.html."""
    style = re.search(r"<style>.*?</style>", INDEX, re.S).group(0)
    umami = re.search(r'<script defer src="https://cloud\.umami\.is/script\.js"[^>]*></script>', INDEX).group(0)
    plausible = re.search(r'<script defer data-domain=[^>]*></script>\n<script>window\.plausible[^\n]*</script>', INDEX).group(0)
    return "\n".join([
        umami,
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
        '<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700;800&display=swap" rel="stylesheet">',
        "<noscript><style>.reveal { opacity: 1; transform: none; }</style></noscript>",
        '<link rel="stylesheet" href="/tailwind.css">',
        style,
        plausible,
    ])


# ── Segments de script ─────────────────────────────────────────────────────
SEGMENTS = [
    "LANGUE", "CONSENTEMENT COOKIES", "MESURE", "SUIVI CLIC CV",
    "HORLOGE BORDEAUX", "MOBILE NAV", "ANNÉE DU FOOTER",
]


def script_segments():
    start = INDEX.index("<script>\n// ── TRANSLATIONS")
    script = INDEX[start:INDEX.rindex("</script>")]
    heads = list(re.finditer(r"^// ── ([^─\n]+?) ?(?:\([^)\n]*\) ?)?──.*$", script, re.M))
    parts = {}
    for i, h in enumerate(heads):
        name = h.group(1).strip()
        end = heads[i + 1].start() if i + 1 < len(heads) else len(script)
        parts[name] = script[h.start():end].rstrip() + "\n"
    out = []
    for want in SEGMENTS:
        key = next((k for k in parts if k.startswith(want)), None)
        if key:
            out.append(parts[key])
    return "<script>\n" + "\n".join(out) + "</script>"


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


def fill(template, values):
    """Remplace les jetons [[CLE]] du gabarit ; échoue si un jeton reste."""
    out = template
    for k, v in values.items():
        out = out.replace("[[%s]]" % k, v)
    left = re.findall(r"\[\[[A-Z_]+\]\]", out)
    if left:
        raise ValueError("jetons non remplacés : %s" % sorted(set(left)))
    return out
