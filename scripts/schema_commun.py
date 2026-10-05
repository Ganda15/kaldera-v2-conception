# Outils communs aux générateurs de schémas de Kaldera V2 : palette, styles, classe Schema et arbre de décision.
# Chaque schéma produit un .drawio (éditable sur app.diagrams.net) et un .html (rendu par le viewer draw.io),
# d'où le .png est tiré par Chrome headless. Légende en puces colorées (legende_chips.py).

import html
import json
from pathlib import Path

from legende_chips import chip_cells

SORTIE = Path(__file__).resolve().parent.parent / "schemas"
SORTIE.mkdir(exist_ok=True)

# --- palette et styles --------------------------------------------------------------------------------------
VERT = "#2E6B3E"      # code déterministe, orchestrateur
BLEU = "#3d85c6"      # agent spécialiste
ORANGE = "#e69138"    # point ambigu, à confirmer avec specs_metier.md
GRIS = "#999999"      # externe ou chantier 2
ROUGE = "#cc0000"     # interdit (frontière)
OK = "#6aa84f"        # état final : décision
ESC = "#bf9000"       # état final : escalade
VIOLET = "#8e7cc3"    # question métier

BASE = "whiteSpace=wrap;html=1;fontFamily=Arial;fontSize=12;"
GAUCHE = "align=left;spacingLeft=10;spacingRight=8;verticalAlign=top;spacingTop=6;"
MILIEU = "verticalAlign=middle;spacingTop=0;"
S_TITRE = f"text;html=1;fontFamily=Arial;fontSize=20;fontStyle=1;fontColor={VERT};align=left;verticalAlign=top;"
S_SOUS = "text;html=1;fontFamily=Arial;fontSize=12;fontColor=#555555;align=left;verticalAlign=top;whiteSpace=wrap;"
S_ORCH = BASE + GAUCHE + f"rounded=1;fillColor=#d9ead3;strokeColor={VERT};strokeWidth=2;"
S_AGENT = BASE + GAUCHE + f"rounded=1;fillColor=#cfe2f3;strokeColor={BLEU};strokeWidth=1.5;"
S_AMBIG = BASE + GAUCHE + f"rounded=1;fillColor=#fce5cd;strokeColor={ORANGE};strokeWidth=2;"
S_EXT = BASE + f"rounded=1;fillColor=#f3f3f3;strokeColor={GRIS};dashed=1;fontColor=#555555;"
S_NOTE = BASE + GAUCHE + "shape=note;size=14;fillColor=#ffffff;strokeColor=#999999;fontSize=11;"
S_GROUPE = (f"rounded=1;arcSize=5;whiteSpace=wrap;html=1;fillColor=none;strokeColor={BLEU};dashed=1;dashPattern=8 4;"
            f"verticalAlign=top;align=left;spacingLeft=10;spacingTop=4;fontFamily=Arial;fontSize=11;fontColor={BLEU};")
S_CONTENEUR = ("rounded=1;arcSize=3;whiteSpace=wrap;html=1;fillColor=#fbfbfb;strokeColor=#666666;strokeWidth=1.5;"
               "verticalAlign=top;align=left;spacingLeft=12;spacingTop=6;fontFamily=Arial;fontSize=13;fontStyle=1;fontColor=#333333;")
S_LOSANGE = f"rhombus;whiteSpace=wrap;html=1;fontFamily=Arial;fontSize=11;fillColor=#d9ead3;strokeColor={VERT};strokeWidth=1.5;"
S_FIN_OK = BASE + f"rounded=1;fillColor=#d9ead3;strokeColor={OK};strokeWidth=3;fontStyle=0;"
S_FIN_ESC = BASE + f"rounded=1;fillColor=#fff2cc;strokeColor={ESC};strokeWidth=3;"
S_CYL = (BASE + "shape=cylinder3;boundedLbl=1;backgroundOutline=1;size=12;"
         f"fillColor=#d9ead3;strokeColor={VERT};strokeWidth=1.5;")
# arbre de décision
S_QPROD = BASE + GAUCHE + MILIEU + f"rounded=1;fillColor=#d9d2e9;strokeColor={VIOLET};strokeWidth=2;"
S_QTECH = BASE + GAUCHE + MILIEU + f"rounded=1;fillColor=#d9ead3;strokeColor={VERT};strokeWidth=1.5;"
S_ECARTE = BASE + GAUCHE + MILIEU + "rounded=1;fillColor=#f3f3f3;strokeColor=#999999;dashed=1;fontColor=#555555;fontSize=11;"
S_RETENU = BASE + GAUCHE + MILIEU + f"rounded=1;fillColor=#cfe2f3;strokeColor={BLEU};fontSize=11;"
S_FINAL = BASE + GAUCHE + MILIEU + f"rounded=1;fillColor=#d9ead3;strokeColor={VERT};strokeWidth=3;"

E_BASE = "edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;fontFamily=Arial;fontSize=11;labelBackgroundColor=#ffffff;"
E_DEP = E_BASE + "endArrow=block;endFill=1;strokeColor=#333333;strokeWidth=1.5;"
E_DELEG = E_BASE + f"endArrow=open;endFill=0;dashed=1;strokeColor={VERT};strokeWidth=1.2;fontColor={VERT};"
E_FAIT = E_BASE + f"endArrow=block;endFill=1;dashed=1;dashPattern=3 3;strokeColor={ORANGE};strokeWidth=1.5;fontColor=#b45f06;"
E_EXT = E_BASE + f"endArrow=block;endFill=1;dashed=1;strokeColor={GRIS};strokeWidth=1.2;fontColor=#555555;"
E_ESC = E_BASE + f"endArrow=block;endFill=1;strokeColor={ESC};strokeWidth=1.5;fontColor=#7f6000;"
E_OK = E_BASE + f"endArrow=block;endFill=1;strokeColor={OK};strokeWidth=1.5;fontColor=#38761d;"


class Schema:
    def __init__(self):
        self.cells = []

    def box(self, cid, texte, x, y, w, h, style):
        self.cells.append(
            f'<mxCell id="{cid}" value="{html.escape(texte, quote=True)}" style="{style}" vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'
        )

    def edge(self, eid, src, tgt, style, label="", points=None, sortie=None, entree=None):
        """sortie/entree : (x, y) relatifs à la boîte (0 à 1), pour fixer où la flèche part et arrive."""
        if sortie:
            style += f"exitX={sortie[0]};exitY={sortie[1]};exitDx=0;exitDy=0;"
        if entree:
            style += f"entryX={entree[0]};entryY={entree[1]};entryDx=0;entryDy=0;"
        pts = ""
        if points:
            pts = '<Array as="points">' + "".join(f'<mxPoint x="{px}" y="{py}"/>' for px, py in points) + "</Array>"
        self.cells.append(
            f'<mxCell id="{eid}" value="{html.escape(label, quote=True)}" style="{style}" edge="1" parent="1" '
            f'source="{src}" target="{tgt}"><mxGeometry relative="1" as="geometry">{pts}</mxGeometry></mxCell>'
        )

    def legende(self, items, x, y):
        chips, _ = chip_cells(items, x, y)
        self.cells.extend(chips)

    def ecrire(self, nom, titre, largeur, hauteur):
        xml = (
            f'<mxfile host="app.diagrams.net" type="device"><diagram id="{nom}" name="{html.escape(titre, quote=True)}">'
            '<mxGraphModel dx="1400" dy="1000" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" '
            f'fold="1" page="1" pageScale="1" pageWidth="{largeur}" pageHeight="{hauteur}" math="0" shadow="0"><root>'
            '<mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(self.cells) + "</root></mxGraphModel></diagram></mxfile>"
        )
        (SORTIE / f"{nom}.drawio").write_text(xml, encoding="utf-8")
        config = {"highlight": "#0000ff", "nav": False, "resize": True, "toolbar": "", "edit": "", "xml": xml}
        page = (
            f"<!doctype html><html><head><meta charset='utf-8'><title>{html.escape(titre)}</title>"
            "<style>body{margin:16px;background:#fff}</style></head><body>"
            f"<div class='mxgraph' style='border:0;' data-mxgraph='{html.escape(json.dumps(config), quote=True)}'></div>"
            "<script src='https://viewer.diagrams.net/js/viewer-static.min.js'></script></body></html>"
        )
        (SORTIE / f"{nom}.html").write_text(page, encoding="utf-8")
        print(f"{nom} : {len(self.cells)} cellules")


def arbre_de_decision(nom, titre_page, titre, sous_titre, questions, cotes, reponses, final, tension, legende):
    """Arbre de décision vertical : une question par ligne, l'option écartée ou retenue à droite, le choix final en bas.
    questions : [(id, texte, style)] ; cotes : [(id, texte, style, verbe)] ; reponses : libellés des flèches
    descendantes (un de plus que d'intervalles entre questions, le dernier mène au choix final)."""
    s = Schema()
    s.box("t", titre, 30, 20, 1100, 30, S_TITRE)
    s.box("st", sous_titre, 30, 54, 1180, 22, S_SOUS)
    y0, pas = 110, 120
    for i, ((qid, qtexte, qstyle), (rid, rtexte, rstyle, verbe)) in enumerate(zip(questions, cotes)):
        y = y0 + i * pas
        s.box(qid, qtexte, 60, y, 520, 64, qstyle)
        s.box(rid, rtexte, 700, y, 520, 64, rstyle)
        s.edge(f"e{rid}", qid, rid, E_EXT if rstyle == S_ECARTE else E_DEP, verbe, sortie=(1, 0.5), entree=(0, 0.5))
    y_fin = y0 + len(questions) * pas
    s.box("final", final, 60, y_fin, 520, 90, S_FINAL)
    ids = [q[0] for q in questions] + ["final"]
    for i in range(len(questions)):
        s.edge(f"d{i}", ids[i], ids[i + 1], E_DEP, reponses[i], sortie=(0.5, 1), entree=(0.5, 0))
    s.box("tension", tension, 700, y_fin, 520, 90, S_AMBIG + MILIEU)
    s.legende(legende, 30, y_fin + 120)
    s.ecrire(nom, titre_page, 1260, y_fin + 160)
