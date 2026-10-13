#!/usr/bin/env python3
"""
Extrait chaque bloc <script type="application/ld+json"> des pages HTML du
dépôt et vérifie qu'il est parsable (json.loads). Les gabarits (dossiers
nommés _template ou fichiers _template.html, jetons non remplacés) sont
ignorés.

Usage : python3 scripts/check_jsonld.py
Code de sortie : 0 si tous les blocs sont valides, 1 sinon.
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATTERN = re.compile(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', re.S)


def main():
    files = sorted(
        p for p in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True)
        if "_template" not in p and "/.git/" not in p and "node_modules" not in p
    )
    errors = 0
    total = 0
    for path in files:
        rel = os.path.relpath(path, ROOT)
        with open(path, encoding="utf-8") as f:
            blocks = PATTERN.findall(f.read())
        for i, raw in enumerate(blocks, 1):
            total += 1
            try:
                data = json.loads(raw)
                types = [n.get("@type") for n in data.get("@graph", [data])]
                print("✓ %s bloc %d : %s" % (rel, i, ", ".join(map(str, types))))
            except json.JSONDecodeError as e:
                errors += 1
                print("✗ %s bloc %d : %s" % (rel, i, e))
    print("%d bloc(s) JSON-LD, %d erreur(s)" % (total, errors))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
