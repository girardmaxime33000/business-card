#!/usr/bin/env python3
"""
Contrôles de cohérence du site :
  1. les pages /c/* sont en noindex, nofollow et absentes de sitemap.xml,
     llms.txt et llms-full.txt ;
  2. toutes les autres pages HTML (hors gabarits) sont en « index, follow » ;
  3. chaque URL de sitemap.xml correspond à un fichier existant ;
  4. aucun texte français visible dans en/index.html hors noms propres ;
  5. les liens internes (href en « / », « ../ » ou « # ») pointent vers un
     fichier ou une ancre existants.

Usage : python3 scripts/check_pages.py
Code de sortie : 0 si tout passe, 1 sinon.
"""
import glob
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pages_common as pc  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.girardmaxime33.com"

# Noms propres et emprunts qui contiennent des accents ou des mots français.
PROPER = {
    "Jérémy", "ColisPrivé", "Métropole", "Expédia", "Mérignac", "Sainte", "Marie", "Grand", "Lebrun",
}
FRENCH_WORDS = {
    "le", "la", "les", "des", "du", "une", "un", "pour", "avec", "dans", "sur", "est", "sont",
    "mon", "ma", "mes", "nous", "vous", "je", "il", "elle", "qui", "que", "aux", "ou", "par",
    "plus", "cette", "ces", "son", "sa", "ses", "au", "en", "été", "où", "de", "et", "chez", "vers",
}
ACCENTS = re.compile(r"[àâäçéèêëîïôöùûüÿœæ]", re.I)


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


def html_pages():
    out = []
    for p in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
        rel = os.path.relpath(p, ROOT).replace(os.sep, "/")
        if "_template" in rel or rel.startswith(".git/") or "node_modules" in rel:
            continue
        out.append(rel)
    return sorted(out)


def visible_text(page):
    page = re.sub(r"<(script|style)\b.*?</\1>", " ", page, flags=re.S)
    page = re.sub(r"<!--.*?-->", " ", page, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", page))


def internal_links():
    errors = []
    for rel in html_pages():
        page = read(rel)
        ids = set(re.findall(r'\bid="([^"]+)"', page))
        base = os.path.dirname(rel)
        for href in re.findall(r'<a\b[^>]*\bhref="([^"]*)"', re.sub(r"<script\b.*?</script>", "", page, flags=re.S)):
            href = html.unescape(href)
            if re.match(r"^(https?:|mailto:|tel:|//)", href) or not href:
                continue
            path, _, frag = href.partition("#")
            path = path.split("?")[0]
            if path == "":
                target = rel
            elif path.startswith("/"):
                target = path.lstrip("/")
            else:
                target = os.path.normpath(os.path.join(base, path)).replace(os.sep, "/")
            if target == "" or target.endswith("/"):
                target += "index.html"
            if not os.path.exists(os.path.join(ROOT, target)):
                errors.append("%s : lien interne cassé %s" % (rel, href))
                continue
            if frag and target.endswith(".html"):
                tids = ids if target == rel else set(re.findall(r'\bid="([^"]+)"', read(target)))
                if frag not in tids:
                    errors.append("%s : ancre introuvable %s" % (rel, href))
    return errors


def main():
    errors = []
    sitemap = read("sitemap.xml")
    llms = read("llms.txt") + read("llms-full.txt")

    for rel in html_pages():
        robots = re.search(r'<meta name="robots" content="([^"]*)"', read(rel))
        value = robots.group(1) if robots else None
        if rel.startswith("c/"):
            if value != "noindex, nofollow":
                errors.append("%s : robots = %r, attendu 'noindex, nofollow'" % (rel, value))
            slug_dir = "/" + os.path.dirname(rel) + "/"
            if slug_dir in sitemap or rel in sitemap:
                errors.append("%s présent dans sitemap.xml" % rel)
            if slug_dir in llms or rel in llms:
                errors.append("%s présent dans llms.txt ou llms-full.txt" % rel)
        else:
            if not value or not value.startswith("index, follow"):
                errors.append("%s : robots = %r, attendu 'index, follow…'" % (rel, value))

    for loc in re.findall(r"<loc>([^<]+)</loc>", sitemap):
        path = loc[len(SITE):] if loc.startswith(SITE) else None
        if path is None:
            errors.append("sitemap : URL hors domaine %s" % loc)
            continue
        rel = path.lstrip("/")
        if rel == "" or rel.endswith("/"):
            rel += "index.html"
        if not os.path.exists(os.path.join(ROOT, rel)):
            errors.append("sitemap : fichier introuvable pour %s" % loc)
        if rel.startswith("c/"):
            errors.append("sitemap : page de candidature %s" % loc)

    words = re.findall(r"[^\W\d_]+(?:['’][^\W\d_]+)?", visible_text(read("en/index.html")))
    suspects = sorted({
        w for w in words
        if w not in PROPER and (w.lower() in FRENCH_WORDS and w.lower() not in {"a"} or ACCENTS.search(w))
    })
    # Faux positifs EN : « on », « a »… absents de FRENCH_WORDS ; « plus » et « en » existent en anglais.
    suspects = [w for w in suspects if w.lower() not in {"plus", "en", "sur", "son", "par", "ma", "mon", "il", "la", "le", "du", "ou"} or ACCENTS.search(w)]
    # Textes t.fr restés tels quels dans la page EN (clé traduite différemment).
    en_text = re.sub(r"\s+", " ", visible_text(read("en/index.html")))
    tfr, ten = pc.t_dict("fr"), pc.t_dict("en")
    for key, fr in tfr.items():
        if key in ("page-title",) or fr == ten.get(key):
            continue
        plain = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", fr))).strip()
        if len(plain) > 12 and plain in en_text:
            errors.append("en/index.html : texte FR non traduit pour la clé %s" % key)
    if suspects:
        errors.append("en/index.html : mots français visibles : %s" % ", ".join(suspects))

    errors += internal_links()

    for e in errors:
        print("✗", e)
    if not errors:
        print("✓ robots, sitemap, llms et en/index.html : aucun écart (%d pages HTML contrôlées)" % len(html_pages()))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
