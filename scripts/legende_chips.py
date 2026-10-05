# Légende en puces colorées (point coloré + libellé, dans un badge arrondi) pour les schémas draw.io.
# Une puce se reconnaît d'un coup d'oeil ; une ligne de texte « bleu : ... · orange : ... » oblige à lire chaque mot.

import html as _html


def chip_cells(items, x, y, id_prefix="leg", gap=10, hauteur=26, fontsize=11):
    """items : liste de (couleur_hex, libellé). Retourne (cellules mxgraph, abscisse de fin).
    Pose une rangée de puces alignées à gauche à partir de (x, y). La largeur de chaque puce est estimée
    d'après la longueur du libellé, ce qui convient aux libellés courts (un à quatre mots). Au-delà
    d'environ 25 caractères, relire le rendu et élargir gap ou x si besoin."""
    cells = []
    cx = x
    for i, (couleur, texte) in enumerate(items):
        largeur = 26 + len(texte) * 6.4
        # Le HTML de la puce (balise font, entité &nbsp;) est échappé une fois pour devenir une valeur XML
        # valide ; le viewer mxgraph le décode ensuite et le rend comme du HTML (html=1). Sans cet
        # échappement, la cellule disparaît du rendu sans aucune erreur visible.
        interieur = f'<font color="{couleur}">&#9679;</font>&nbsp;{texte}'
        style = (
            "rounded=1;whiteSpace=nowrap;html=1;fillColor=#f8f9fa;strokeColor=#dadce0;"
            f"fontSize={fontsize};fontColor=#3c4043;align=left;spacingLeft=8;verticalAlign=middle;arcSize=40;"
        )
        cells.append(
            f'<mxCell id="{id_prefix}{i}" value="{_html.escape(interieur, quote=True)}" style="{style}" '
            f'vertex="1" parent="1"><mxGeometry x="{cx:.0f}" y="{y}" width="{largeur:.0f}" height="{hauteur}" '
            f'as="geometry"/></mxCell>'
        )
        cx += largeur + gap
    return cells, cx
