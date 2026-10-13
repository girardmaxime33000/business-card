#!/usr/bin/env python3
"""
Génère cas/<slug>.html depuis cas/_template.html et data/cas/<slug>.json.

Les textes sont lus dans t.fr d'index.html (mot pour mot) via la clé `key`
(+ `sentences` pour ne retenir que certaines phrases d'un paragraphe) ; tout
complément absent d'index.html est un placeholder {{A_COMPLETER: …}}.

Usage : python3 scripts/build_cas.py
Appelé par le job build-check de la CI.
"""
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pages_common as pc  # noqa: E402

SECTION_ORDER = [
    ("contexte", "Contexte"), ("enjeu", "Enjeu"), ("actions", "Actions"),
    ("stack", "Stack"), ("resultats", "Résultats"), ("duree", "Durée"), ("role", "Rôle"),
]
PILL = "font-mono text-xs font-medium bg-lime-400/10 text-lime-700 border border-lime-400/20 rounded-full px-3 py-1"


def split_sentences(text):
    return re.split(r"(?<=\.) (?=[A-ZÉÈ])", text)


def resolve(block, tfr):
    """Un bloc de données renvoie (type, valeur) avec le texte lu dans t.fr."""
    if "text" in block:
        return block.get("type", "p"), block["text"]
    if "keys" in block:
        return block.get("type", "p"), " · ".join(tfr[k] for k in block["keys"])
    text = tfr[block["key"]]
    if "sentences" in block:
        parts = split_sentences(text)
        text = " ".join(parts[i] for i in block["sentences"])
    return block.get("type", "p"), text


def render_section(label, blocks, tfr):
    items_html = ""
    ul = []
    for block in blocks:
        kind, text = resolve(block, tfr)
        t = pc.esc(text)
        if block.get("type") == "li":
            ul.append('<li class="relative pl-4 text-sm text-neutral-500 leading-relaxed py-1 before:content-[\'->\'] before:absolute before:left-0 before:text-lime-700 before:text-xs">%s</li>' % t)
            continue
        if ul:
            items_html += '<ul class="mb-4">\n%s\n</ul>\n' % "\n".join(ul)
            ul = []
        if block.get("type") == "pills":
            pills = "".join('<span class="%s">%s</span>' % (PILL, pc.esc(x)) for x in text.split(" · "))
            items_html += '<div class="flex flex-wrap gap-2 mb-4">%s</div>\n' % pills
        elif block.get("type") == "result":
            items_html += '<span class="inline-flex items-center bg-lime-400/10 border border-lime-400/25 text-lime-700 text-sm font-medium px-3 py-1 rounded-md">%s</span>\n' % t
        else:
            items_html += '<p class="text-neutral-600 leading-relaxed mb-4">%s</p>\n' % t
    if ul:
        items_html += '<ul class="mb-4">\n%s\n</ul>\n' % "\n".join(ul)
    return (
        '<section class="mb-12" aria-labelledby="h2-%s">\n'
        '<h2 id="h2-%s" class="flex items-center gap-2 text-xs tracking-[0.2em] uppercase text-lime-700 mb-4 font-mono">'
        '<span class="opacity-60" aria-hidden="true">//</span><span>%s</span></h2>\n%s</section>'
        % (label[0], label[0], pc.esc(label[1]), items_html)
    )


def jsonld(data, canonical):
    return json.dumps({
        "@context": "https://schema.org",
        "@graph": [{
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Accueil", "item": pc.SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": data["breadcrumb"]["label"], "item": pc.SITE + data["breadcrumb"]["href"]},
                {"@type": "ListItem", "position": 3, "name": data["h1"], "item": canonical},
            ],
        }],
    }, ensure_ascii=False, indent=2)


def main():
    tfr = pc.t_fr()
    template = pc.read("cas/_template.html")
    shared = dict(
        HEAD_SHARED=pc.head_shared(), HEADER=pc.header(), FOOTER=pc.footer(),
        COOKIE_BANNER=pc.cookie_banner(), SCRIPT=pc.script_segments(),
    )
    for path in sorted(glob.glob(os.path.join(pc.ROOT, "data", "cas", "*.json"))):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        slug = data["slug"]
        canonical = "%s/cas/%s.html" % (pc.SITE, slug)
        sections = "\n".join(
            render_section((k, label), data["sections"][k], tfr) for k, label in SECTION_ORDER
        )
        page = pc.fill(template, dict(
            shared,
            TITLE=pc.esc_attr(data["title"]), DESCRIPTION=pc.esc_attr(data["description"]),
            CANONICAL=canonical, JSONLD=jsonld(data, canonical),
            BACK_HREF=data["breadcrumb"]["href"], BACK_LABEL=pc.esc(data["back_label"]),
            LABEL=pc.esc(data["label"]), H1=pc.esc(data["h1"]), SECTIONS=sections,
        ))
        pc.write("cas/%s.html" % slug, page)
        print("✓ cas/%s.html" % slug)


if __name__ == "__main__":
    main()
