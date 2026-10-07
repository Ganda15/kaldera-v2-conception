# Rend un fichier Markdown en PDF dans le STYLE MAISON d'Era (posé le 25/09/2026, modèle : veille « Alternatives à
# Claude ») : page 1 = titre, sous-titre, auteur, date centrés + « Table des matières » verte (sections en gras,
# sous-sections à points de conduite) ; en-tête = titre + filet vert ; pied = auteur · page · date + filet vert ;
# titres verts numérotés ; tableaux à trois filets ; chaque schéma sur sa propre page paysage, avec sa légende.
# Numéros de page RÉELS : deux passes (rendu, lecture des pages par PyMuPDF, injection, second rendu, vérification).
# Copie du 07/10/2026 pour Kaldera V2 (légende « Figure n : », note vers le .drawio). Adapté de la chaîne de Mardik ③ (C:\Users\kanda\Desktop\Mardik_La nouvelle version\scripts\md2pdf.py, non modifiée).
# Usage : C:\Python314\python.exe scripts\md2pdf.py Chapitre-Industrialisation-RITA.md
# Options : --auteur "…"  --date AAAA-MM-JJ  --sous-titre "…"
# Sortie : <même nom>.html (intermédiaire, gardé pour contrôle) et <même nom>.pdf, dans le dossier du .md.

import argparse
import datetime as dt
import html
import re
import subprocess
from pathlib import Path

import fitz  # PyMuPDF
import markdown

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
VERT = "#2e6b3e"
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre",
        "novembre", "décembre"]

POLICES = ("<link rel='preconnect' href='https://fonts.googleapis.com'>"
           "<link href='https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;"
           "0,8..60,600;0,8..60,700;1,8..60,400&family=JetBrains+Mono:wght@400;600&display=swap' rel='stylesheet'>")

CSS = """
@page { size: A4; margin: 22mm 20mm 22mm 20mm;
  @top-left { content: "__TITRE__"; width: 100%; vertical-align: bottom; padding-bottom: 3pt;
              border-bottom: 0.75pt solid __VERT__; color: __VERT__; font: 9pt 'Source Serif 4', Georgia, serif; }
  @bottom-left { content: "__AUTEUR__"; width: 33.3%; vertical-align: top; padding-top: 3pt;
                 border-top: 0.75pt solid __VERT__; color: __VERT__; font: 9pt 'Source Serif 4', Georgia, serif; }
  @bottom-center { content: counter(page); width: 33.4%; vertical-align: top; padding-top: 3pt;
                   border-top: 0.75pt solid __VERT__; color: __VERT__; font: 9pt 'Source Serif 4', Georgia, serif; }
  @bottom-right { content: "__DATE_LONGUE__"; width: 33.3%; text-align: right; vertical-align: top; padding-top: 3pt;
                  border-top: 0.75pt solid __VERT__; color: __VERT__; font: 9pt 'Source Serif 4', Georgia, serif; } }
@page :first { @top-left { content: none; border: none; } @bottom-left { content: none; border: none; }
  @bottom-right { content: none; border: none; } @bottom-center { border: none; color: #444; } }
@page paysage { size: A4 landscape; margin: 18mm 20mm 18mm 20mm;
  @top-left { content: "__TITRE__"; width: 100%; vertical-align: bottom; padding-bottom: 3pt;
              border-bottom: 0.75pt solid __VERT__; color: __VERT__; font: 9pt 'Source Serif 4', Georgia, serif; }
  @bottom-left { content: "__AUTEUR__"; width: 33.3%; vertical-align: top; padding-top: 3pt;
                 border-top: 0.75pt solid __VERT__; color: __VERT__; font: 9pt 'Source Serif 4', Georgia, serif; }
  @bottom-center { content: counter(page); width: 33.4%; vertical-align: top; padding-top: 3pt;
                   border-top: 0.75pt solid __VERT__; color: __VERT__; font: 9pt 'Source Serif 4', Georgia, serif; }
  @bottom-right { content: "__DATE_LONGUE__"; width: 33.3%; text-align: right; vertical-align: top; padding-top: 3pt;
                  border-top: 0.75pt solid __VERT__; color: __VERT__; font: 9pt 'Source Serif 4', Georgia, serif; } }

html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: 'Source Serif 4', Georgia, serif; font-size: 10.5pt; line-height: 1.5; color: #444; margin: 0; }
.couverture { text-align: center; margin: 0 0 6mm 0; }
.couverture .titre { font-size: 19pt; line-height: 1.25; color: #444; margin: 0 0 4pt 0; font-weight: 400; }
.couverture .sous-titre { font-size: 11pt; margin: 0 0 8pt 0; }
.couverture .auteur, .couverture .date { font-size: 11pt; margin: 1pt 0; }
h2 { font-size: 14.3pt; font-weight: 700; color: __VERT__; margin: 18pt 0 6pt 0; page-break-after: avoid; }
h2.first { page-break-before: always; margin-top: 0; }
h3 { font-size: 12pt; font-weight: 700; color: #333; margin: 13pt 0 4pt 0; page-break-after: avoid; }
h4 { font-size: 10.5pt; font-weight: 700; color: #333; margin: 10pt 0 3pt 0; page-break-after: avoid; }
h2 .num, h3 .num { display: inline-block; min-width: 2.1em; }
p { margin: 5pt 0; text-wrap: pretty; }
ul, ol { margin: 4pt 0 6pt 0; padding-left: 20pt; }
li { margin: 2pt 0; }
strong { color: #333; }
a { color: __VERT__; text-decoration: none; }
code { font-family: 'JetBrains Mono', Consolas, monospace; font-size: 8.6pt; background: #f4f4f2; padding: 0 3px;
       border-radius: 2px; }
pre { font-family: 'JetBrains Mono', Consolas, monospace; font-size: 8.4pt; line-height: 1.45; background: #f7f7f5;
      border: 1px solid #e0e0da; border-radius: 3px; padding: 7pt 9pt; white-space: pre-wrap; word-break: break-word;
      page-break-inside: avoid; margin: 6pt 0; color: #333; }
pre code { background: none; padding: 0; font-size: inherit; }
blockquote { margin: 8pt 0; padding: 6pt 10pt; background: #f3f7f4; border: 1px solid #c9dccd; border-radius: 3px; }
blockquote p { margin: 3pt 0; }
table { width: 100%; border-collapse: collapse; font-size: 9pt; line-height: 1.4; margin: 8pt 0 10pt 0;
        border-top: 1.2pt solid #444; border-bottom: 1.2pt solid #444; }
thead { display: table-header-group; }
thead tr { border-bottom: 0.75pt solid #444; }
tr { page-break-inside: avoid; }
th { text-align: left; vertical-align: bottom; font-weight: 600; color: #333; padding: 4pt 6pt; }
td { vertical-align: top; padding: 3pt 6pt; word-break: normal; overflow-wrap: break-word; }
td code { white-space: nowrap; }
th:first-child, td:first-child { padding-left: 0; }
th:last-child, td:last-child { padding-right: 0; }
img { max-width: 100%; height: auto; display: block; margin: 6pt auto; }
hr { border: 0; border-top: 0.75pt solid #ccc; margin: 12pt 0; }
ul.glossaire { font-size: 9.8pt; }
table.num td:first-child, table.num th:first-child { white-space: nowrap; width: 1%; }
/* un schéma = une page paysage à lui seul, sa légende, et où trouver la version zoomable */
.paysage { page: paysage; page-break-before: always; page-break-after: always; text-align: center; padding-top: 8pt; }
.paysage img { max-height: 150mm; width: auto; max-width: 100%; margin: 0 auto 4pt auto; }
.paysage .legende { font-style: italic; font-size: 9.5pt; margin: 2pt 0; }
.paysage .zoom { font-size: 8.8pt; color: #555; margin: 0; }
/* table des matières */
.toc h2 { margin: 0 0 5pt 0; font-size: 14.3pt; }
.toc ol { list-style: none; padding: 0; margin: 0; }
.toc li { display: flex; align-items: baseline; margin: 0; font-size: 9pt; line-height: 1.28; }
.toc li.n2 { font-weight: 700; color: #444; margin-top: 4pt; }
.toc li.n3 { padding-left: 18pt; }
.toc .n { display: inline-block; min-width: 2.4em; }
.toc li.n2 .n { min-width: 1.6em; }
.toc .d { flex: 1; border-bottom: 1.2pt dotted #9a9a9a; margin: 0 5pt; min-width: 10pt; position: relative; top: -3pt; }
.toc li.n2 .d { border-bottom: none; }
.toc .p { white-space: nowrap; font-variant-numeric: tabular-nums; }
"""

EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\uFE0F]")


def date_longue(iso: str) -> str:
    d = dt.date.fromisoformat(iso)
    return f"{d.day} {MOIS[d.month - 1]} {d.year}"


def sans_sommaire_md(md: str) -> str:
    """Retire le bloc « ## Sommaire » du Markdown : le PDF reçoit la table des matières numérotée à sa place."""
    return re.sub(r"^## Sommaire\s*\n.*?(?=^## )", "", md, count=1, flags=re.S | re.M)


def couper_titre(texte: str):
    """« 1. Objectifs de service » → ("1", "Objectifs de service") ; « 1.1 Utilisateur » → ("1.1", "Utilisateur ») ;
    « 📖 Glossaire » → ("", "Glossaire")."""
    texte = EMOJI.sub("", re.sub(r"[`*]", "", texte)).strip()
    m = re.match(r"^(\d+(?:\.\d+)*)\.?\s+(.*)$", texte)
    return (m.group(1), m.group(2).strip()) if m else ("", texte)


def entetes(md: str):
    """Les titres de niveau 2 et 3, dans l'ordre : (niveau, numéro, texte) — hors « Sommaire »."""
    res = []
    for ligne in md.splitlines():
        m = re.match(r"^(##|###) (.+?)\s*$", ligne)
        if m:
            num, texte = couper_titre(m.group(2))
            if texte.lower() == "sommaire":
                continue
            res.append((len(m.group(1)), num, texte))
    return res


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", EMOJI.sub("", re.sub(r"[`*]", "", s))).strip().lower()


def cle(num: str, texte: str) -> str:
    return _norm(f"{num} {texte}" if num else texte)


def pages_des_entetes(pdf: Path, titres, apres_sommaire: bool = False):
    """Page (1-based) où chaque titre apparaît, en cherchant « numéro + texte » page par page, dans l'ordre.
    Avec la table des matières en tête, la recherche commence à la page où la section 1 débute réellement."""
    doc = fitz.open(pdf)
    textes = [_norm(p.get_text()) for p in doc]
    pages, depuis = [], 0
    if apres_sommaire:
        premier = cle(titres[0][1], titres[0][2])
        for i in range(1, len(textes)):
            if textes[i][:160].find(premier) != -1:
                depuis = i
                break
    for _niv, num, texte in titres:
        k = cle(num, texte)
        trouve = next((i + 1 for i in range(depuis, len(textes)) if k in textes[i]), None)
        if trouve is None:  # repli : les 30 premiers caractères
            trouve = next((i + 1 for i in range(depuis, len(textes)) if k[:30] in textes[i]), None)
        pages.append(trouve)
        if trouve:
            depuis = trouve - 1
    doc.close()
    return pages


def sommaire_html(titres, pages) -> str:
    items = []
    for (niv, num, texte), page in zip(titres, pages):
        cls = "n2" if niv == 2 else "n3"
        items.append(f'<li class="{cls}"><span class="n">{html.escape(num)}</span><span class="t">{html.escape(texte)}'
                     f'</span><span class="d"></span><span class="p">{page if page else "?"}</span></li>')
    return '<div class="toc"><h2>Table des matières</h2><ol>' + "".join(items) + "</ol></div>"


def _titre_numerote(m):
    niv, contenu = m.group(1), m.group(2)
    num, texte = couper_titre(html.unescape(re.sub(r"<[^>]+>", "", contenu)))
    if not num:
        return f"<h{niv}>{html.escape(texte)}</h{niv}>"
    return f'<h{niv}><span class="num">{num}</span>{html.escape(texte)}</h{niv}>'


def corps_html(md: str, dossier: Path, sommaire: str = "") -> str:
    corps = markdown.markdown(md, extensions=["tables", "fenced_code", "sane_lists", "attr_list", "md_in_html"],
                              output_format="html5")
    corps = re.sub(r"<h1>.*?</h1>\s*", "", corps, count=1, flags=re.S)                 # le titre va sur la couverture
    corps = re.sub(r"<blockquote>.*?</blockquote>\s*", "", corps, count=1, flags=re.S)  # le chapeau aussi
    corps = re.sub(r"<h([23])>(.*?)</h\1>", _titre_numerote, corps)
    corps = corps.replace('<h2><span class="num">1</span>', '<h2 class="first"><span class="num">1</span>', 1)
    corps = re.sub(r"(<h2>Glossaire</h2>\s*)<ul>", r'\1<ul class="glossaire">', corps)
    corps = re.sub(r"<table>(\s*<thead>\s*<tr>\s*<th>#</th>)", r'<table class="num">\1', corps)

    # chaque schéma sur sa propre page paysage, avec sa légende et l'adresse de sa version zoomable
    numero = [0]

    def _figure(m):
        alt, src = m.group(1), m.group(2)
        numero[0] += 1
        zoom = Path(src).with_suffix(".html").as_posix()
        editable = Path(src).with_suffix(".drawio").as_posix()
        note = ""
        if (dossier / zoom).exists():
            note = (f'<p class="zoom">Version zoomable : <code>{zoom}</code> · version éditable : '
                    f'<code>{editable}</code></p>')
        elif (dossier / editable).exists():
            note = f'<p class="zoom">Version éditable : <code>{editable.replace("../", "")}</code></p>'
        return (f'<div class="paysage"><img class="schema" alt="{alt}" src="{src}">'
                f'<p class="legende">Figure {numero[0]} : {alt}.</p>{note}</div>')
    corps = re.sub(r'<p>\s*<img alt="([^"]*)" src="([^"]+)"\s*/?>\s*</p>', _figure, corps)
    return sommaire + corps


def ecrire_et_rendre(chemin_md: Path, corps: str, meta: dict) -> Path:
    css = (CSS.replace("__VERT__", VERT).replace("__TITRE__", meta["titre"].replace('"', "'"))
           .replace("__AUTEUR__", meta["auteur"]).replace("__DATE_LONGUE__", date_longue(meta["date"])))
    couverture = (f'<div class="couverture"><p class="titre">{html.escape(meta["titre"])}</p>'
                  f'<p class="sous-titre">{html.escape(meta["sous_titre"])}</p>'
                  f'<p class="auteur">{html.escape(meta["auteur"])}</p><p class="date">{meta["date"]}</p></div>')
    page = (f"<!doctype html><html lang='fr'><head><meta charset='utf-8'><title>{html.escape(meta['titre'])}</title>"
            f"{POLICES}<style>{css}</style></head><body>{couverture}{corps}</body></html>")
    chemin_html = chemin_md.with_suffix(".html")
    chemin_html.write_text(page, encoding="utf-8")
    chemin_pdf = chemin_md.with_suffix(".pdf")
    if chemin_pdf.exists():
        chemin_pdf.unlink()
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-first-run", "--no-pdf-header-footer",
                    "--virtual-time-budget=15000", f"--print-to-pdf={chemin_pdf}", chemin_html.resolve().as_uri()],
                   check=True)
    return chemin_pdf


def lire_meta(md_brut: str, args) -> dict:
    lignes = md_brut.splitlines()
    titre = lignes[0].lstrip("# ").strip()
    chapeau = next((re.sub(r"^>\s*", "", l).strip() for l in lignes[1:] if l.startswith(">")), "")
    return {"titre": titre, "sous_titre": args.sous_titre or chapeau, "auteur": args.auteur, "date": args.date}


def rendre(chemin_md: Path, args) -> Path:
    brut = chemin_md.read_text(encoding="utf-8")
    meta = lire_meta(brut, args)
    md = sans_sommaire_md(brut)
    titres = entetes(md)
    dossier = chemin_md.parent
    # passe 1 : sans table des matières, pour connaître la pagination de base
    pdf = ecrire_et_rendre(chemin_md, corps_html(md, dossier), meta)
    pages = pages_des_entetes(pdf, titres)
    # passes suivantes : avec la table, jusqu'à ce que les numéros annoncés soient les numéros réels (3 essais max)
    for essai in range(3):
        pdf = ecrire_et_rendre(chemin_md, corps_html(md, dossier, sommaire_html(titres, pages)), meta)
        reels = pages_des_entetes(pdf, titres, apres_sommaire=True)
        if reels == pages:
            print(f"table des matieres verifiee a la passe {essai + 2} : {len(titres)} entrees, numeros conformes")
            break
        pages = reels
    else:
        print("ATTENTION : la table des matieres n'a pas converge - verifier les numeros a la main")
    for (niv, num, texte), p in zip(titres, pages):
        ligne = f"  {'  ' if niv == 3 else ''}{(num + ' ' + texte).strip()[:60]:<62} p. {p}"
        print(ligne.encode("ascii", "replace").decode("ascii"))
    return pdf


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Markdown -> PDF, style maison d'Era")
    ap.add_argument("fichier")
    ap.add_argument("--auteur", default="Eramalingam GANDAKUMAR")
    ap.add_argument("--date", default=dt.date.today().isoformat())
    ap.add_argument("--sous-titre", dest="sous_titre", default="")
    args = ap.parse_args()
    md = Path(args.fichier).resolve()
    pdf = rendre(md, args)
    print("ecrit :", md.with_suffix(".html"))
    print("ecrit :", pdf, f"({pdf.stat().st_size} octets, {fitz.open(pdf).page_count} pages)")
