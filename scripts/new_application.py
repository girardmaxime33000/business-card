#!/usr/bin/env python3
"""
Génère c/<slug>/index.html (page de candidature, noindex) depuis
c/_template/index.html et data/candidatures/<slug>.json.

Créer ou mettre à jour une candidature :
  python3 scripts/new_application.py --slug ynov --entreprise "Ynov" \\
      --poste "Head of Performance – Acquisition Digitale" --lieu "Mérignac"

Régénérer toutes les pages à partir des JSON existants (CI) :
  python3 scripts/new_application.py --all

Le JSON est créé avec des placeholders {{A_COMPLETER}} s'il n'existe pas ;
les arguments --entreprise / --poste / --lieu écrasent les valeurs existantes.
Les pages /c/* ne figurent ni dans sitemap.xml ni dans llms.txt.
"""
import argparse
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pages_common as pc  # noqa: E402

PH = "{{A_COMPLETER}}"
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FIELDS = ["slug", "entreprise", "poste", "lieu", "diagnostic", "plan_30", "plan_60", "plan_90", "kpis", "lien_support"]


def notify_endpoint():
    m = re.search(r"const CHAT_ENDPOINT = '([^']+)'", pc.INDEX)
    if not m:
        raise SystemExit("CHAT_ENDPOINT introuvable dans index.html")
    return m.group(1).rstrip("/") + "/notify"


def fill_dunder(template, values):
    out = template
    for k, v in values.items():
        out = out.replace("__%s__" % k, v)
    left = re.findall(r"__[A-Z_]+__", out)
    if left:
        raise ValueError("jetons non remplacés : %s" % sorted(set(left)))
    return out


def list_html(items, placeholder):
    if not items:
        return '<p class="text-sm text-neutral-600 leading-relaxed">%s</p>' % pc.esc(placeholder)
    lis = "\n".join(
        '<li class="relative pl-4 text-sm text-neutral-500 leading-relaxed py-1 before:content-[\'->\'] before:absolute before:left-0 before:text-lime-700 before:text-xs">%s</li>' % pc.esc(x)
        for x in items
    )
    return '<ul>\n%s\n</ul>' % lis


def render(data, template, shared, endpoint):
    slug = data["slug"]
    plan = ""
    for days in (30, 60, 90):
        plan += (
            '<div class="bg-surface border border-neutral-200 rounded-2xl p-6">\n'
            '<h3 class="font-bold text-base text-neutral-900 mb-3">%d jours</h3>\n%s\n</div>\n'
            % (days, list_html(data["plan_%d" % days], "{{A_COMPLETER: plan à %d jours}}" % days))
        )
    support = data["lien_support"]
    if support.startswith("https://"):
        support_html = ('<a href="%s" target="_blank" rel="noopener noreferrer" data-umami-event="Application Support Click" '
                        'class="plausible-event-name=Application+Support+Click inline-flex items-center gap-2 border border-neutral-300 text-neutral-900 font-bold text-sm px-7 py-3.5 rounded-lg transition-all duration-200 hover:border-neutral-400 hover:bg-neutral-100 focus-visible:outline focus-visible:outline-2 focus-visible:outline-lime-600 focus-visible:outline-offset-2">'
                        '<span aria-hidden="true">↗</span> Ouvrir le support</a>') % pc.esc_attr(support)
    else:
        support_html = '<p class="text-sm text-neutral-600">%s</p>' % pc.esc(support)
    return fill_dunder(template, dict(
        shared,
        TITLE=pc.esc("Candidature — %s — %s | Maxime Girard" % (data["poste"], data["entreprise"])),
        POSTE=pc.esc(data["poste"]), ENTREPRISE=pc.esc(data["entreprise"]), LIEU=pc.esc(data["lieu"]),
        DIAGNOSTIC=pc.esc(data["diagnostic"]), PLAN=plan.rstrip("\n"),
        KPIS=list_html(data["kpis"], "{{A_COMPLETER: indicateurs proposés}}"),
        SUPPORT=support_html,
        CALENDLY_URL="https://calendly.com/girard-maxime33?utm_source=candidature&amp;utm_campaign=%s" % slug,
        SLUG=slug, NOTIFY_ENDPOINT=endpoint,
    ))


def load(slug):
    path = os.path.join(pc.ROOT, "data", "candidatures", slug + ".json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {"slug": slug, "entreprise": "", "poste": "", "lieu": "", "diagnostic": PH,
            "plan_30": [], "plan_60": [], "plan_90": [], "kpis": [], "lien_support": PH}


def save(data):
    ordered = {k: data[k] for k in FIELDS}
    pc.write("data/candidatures/%s.json" % data["slug"], json.dumps(ordered, ensure_ascii=False, indent=2) + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--slug")
    ap.add_argument("--entreprise")
    ap.add_argument("--poste")
    ap.add_argument("--lieu")
    ap.add_argument("--all", action="store_true", help="régénère toutes les pages depuis data/candidatures/*.json")
    args = ap.parse_args()

    if args.all:
        slugs = [os.path.splitext(os.path.basename(p))[0] for p in sorted(glob.glob(os.path.join(pc.ROOT, "data", "candidatures", "*.json")))]
    elif args.slug:
        slugs = [args.slug]
    else:
        ap.error("--slug ou --all requis")

    template = pc.read("c/_template/index.html")
    shared = dict(
        HEAD_SHARED=pc.head_shared(), HEADER=pc.header(), FOOTER=pc.footer(),
        COOKIE_BANNER=pc.cookie_banner(), SCRIPT=pc.script_segments(),
    )
    endpoint = notify_endpoint()
    for slug in slugs:
        if not SLUG_RE.match(slug):
            ap.error("slug invalide : %r (minuscules, chiffres et tirets)" % slug)
        data = load(slug)
        data["slug"] = slug
        for field in ("entreprise", "poste", "lieu"):
            value = getattr(args, field, None) if not args.all else None
            if value is not None:
                data[field] = value
            elif not data[field]:
                data[field] = PH
        save(data)
        pc.write("c/%s/index.html" % slug, render(data, template, shared, endpoint))
        print("✓ c/%s/index.html" % slug)


if __name__ == "__main__":
    main()
