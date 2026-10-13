#!/usr/bin/env python3
"""
Génère llms-full.txt (texte visible intégral d'index.html, en Markdown) pour
que le fichier reste synchronisé avec la source FR.

Sections reprises : Profil, Parcours, Formation, Cas d'usage, Compétences,
Références, FAQ (dans l'ordre de la page). Les éléments décoratifs
(aria-hidden) sont ignorés.

Usage : python3 scripts/build_llms.py
Appelé par le job build-check de la CI (voir .github/workflows/ci.yml).
"""
import os
import re
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "index.html")
DST = os.path.join(ROOT, "llms-full.txt")

SECTIONS = ["profil", "experiences", "formation", "cas-usage", "competences", "references", "faq"]
VOID = {"br", "img", "hr", "meta", "link", "input"}
BLOCK = {"p", "h1", "h2", "h3", "li", "div", "section", "summary", "details", "ul", "blockquote", "figure", "figcaption"}


class Extractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []          # (tag, flags)
        self.cur = None          # id de la section courante
        self.buf = []
        self.out = {s: [] for s in SECTIONS}
        self.skip_depth = 0
        self.in_script = 0

    def _flush(self, prefix=""):
        text = re.sub(r"\s+", " ", "".join(self.buf)).strip()
        self.buf = []
        # Ignore les guillemets décoratifs et les numéros de carte (« 01 »).
        if text and self.cur and not re.fullmatch(r'["“”]|\d{2}', text):
            self.out[self.cur].append((prefix, text))

    def _prefix_for(self, flags):
        if "h2" in flags:
            return "## "
        if "h3" in flags:
            return "### "
        if "li" in flags or "pill" in flags:
            return "- "
        if "label" in flags:
            return "_"
        return ""

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get("class", "") or ""
        if tag in ("script", "style"):
            self.in_script += 1
            return
        if tag in VOID:
            if tag == "br" and self.cur and self.skip_depth == 0:
                self.buf.append(" ")
            return
        flags = set()
        if tag == "section" and a.get("id") in SECTIONS:
            self.cur = a["id"]
            flags.add("section")
        elif tag in ("h2", "h3"):
            flags.add(tag)
        elif tag == "li":
            flags.add("li")
        elif tag == "p" and "section-label" in cls:
            flags.add("label")
        elif tag == "span" and ("rounded-full" in cls or "inline-flex" in cls):
            flags.add("pill")
        if a.get("aria-hidden") == "true" or tag == "img":
            flags.add("hidden")
            self.skip_depth += 1
        if tag in BLOCK or flags & {"pill", "label"}:
            self._flush()
        self.stack.append((tag, flags))

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.in_script = max(0, self.in_script - 1)
            return
        if tag in VOID:
            return
        # dépile jusqu'au tag correspondant
        while self.stack:
            t, flags = self.stack.pop()
            if "hidden" in flags:
                self.skip_depth -= 1
            if t == tag:
                break
        else:
            return
        if tag in BLOCK or flags & {"pill", "label"}:
            prefix = self._prefix_for(flags)
            if "label" in flags:
                text = re.sub(r"\s+", " ", "".join(self.buf)).strip().lstrip("/ ").strip()
                self.buf = []
                if text and self.cur:
                    self.out[self.cur].append(("_", text + "_"))
            else:
                self._flush(prefix)
        if "section" in flags:
            self._flush()
            self.cur = None

    def handle_data(self, data):
        if self.in_script or self.skip_depth or not self.cur:
            return
        self.buf.append(data)


def main():
    with open(SRC, encoding="utf-8") as f:
        html = f.read()
    ex = Extractor()
    ex.feed(html)
    lines = [
        "# Maxime Girard — texte intégral du site",
        "",
        "> Directeur Marketing & Growth B2B, Bordeaux (France). Contenu de https://www.girardmaxime33.com/ en Markdown, généré depuis index.html par scripts/build_llms.py.",
        "",
    ]
    titles = {
        "profil": "Profil", "experiences": "Parcours", "formation": "Formation",
        "cas-usage": "Cas d'usage", "competences": "Compétences",
        "references": "Références", "faq": "FAQ",
    }
    for s in SECTIONS:
        items = ex.out[s]
        lines.append("<!-- section: %s -->" % s)
        # Les lignes de contexte d'un poste (dates, entreprise, type) qui
        # précèdent le H3 sont regroupées sur une seule ligne.
        merged = []
        run = []
        for prefix, text in items:
            if prefix == "_":
                continue  # libellé « // Section » : redondant avec le H2
            if prefix == "":
                run.append(text)
                continue
            if prefix == "### " and run:
                merged.append(("", " · ".join(run)))
            else:
                merged.extend(("", r) for r in run)
            run = []
            merged.append((prefix, text))
        merged.extend(("", r) for r in run)
        prev = None
        for prefix, text in merged:
            if lines[-1] != "" and not (prefix == "- " and prev == "- "):
                lines.append("")
            lines.append(prefix + text)
            prev = prefix
        if lines[-1] != "":
            lines.append("")
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text).rstrip() + "\n"
    with open(DST, "w", encoding="utf-8") as f:
        f.write(text)
    print("✓ %s (%d caractères)" % (DST, len(text)))


if __name__ == "__main__":
    main()
