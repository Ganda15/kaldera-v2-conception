# Schémas du chantier 1 de Kaldera V2 : carte des agents, orchestration, mémoire partagée.
# Pour chaque schéma : un .drawio (éditable sur app.diagrams.net) et un .html (rendu par le viewer draw.io),
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

BASE = "whiteSpace=wrap;html=1;fontFamily=Arial;fontSize=12;"
GAUCHE = "align=left;spacingLeft=10;spacingRight=8;verticalAlign=top;spacingTop=6;"
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


ROUGE_TXT = f'<font color="{ROUGE}"><b>Interdit :</b> '
FIN = "</font>"

# =============================================================================================================
# Schéma 1 : la carte des agents
# =============================================================================================================
s = Schema()
s.box("t", "Kaldera V2 · Carte des agents · Chantier 1", 30, 20, 1000, 30, S_TITRE)
s.box("st", "Rôles, frontières, point ambigu tranché, dépendances et parallélisme. "
            "Proposition provisoire, à confirmer avec specs_metier.md.", 30, 54, 1100, 22, S_SOUS)

s.box("orch", "<b>Orchestrateur</b> (code, sans LLM)<br>"
              "Délègue chaque étape, applique les bornes, écrit le statut final.<br>"
              + ROUGE_TXT + "refaire un contrôle métier (éligibilité, pièces, montant, fraude)." + FIN,
      400, 95, 640, 78, S_ORCH)

s.box("par", "Exécutées en parallèle : aucune n'a besoin du résultat de l'autre", 30, 225, 440, 400, S_GROUPE)
s.box("elig", "<b>Éligibilité</b> (règles en code)<br><br>"
              "Vérifie que le contrat couvre la demande.<br>"
              "Renvoie : éligible oui ou non, avec le motif.<br><br>"
              + ROUGE_TXT + "calculer un montant, juger les pièces, juger la fraude." + FIN,
      50, 260, 400, 150, S_AGENT)
s.box("pieces", "<b>Pièces justificatives</b> (code, LLM pour lire le texte libre)<br><br>"
                "Vérifie que les pièces exigées sont présentes et cohérentes.<br>"
                "Renvoie : complet oui ou non, pièces manquantes, incohérences constatées.<br><br>"
                + ROUGE_TXT + "conclure à la fraude ; il constate une incohérence, il ne la qualifie pas." + FIN,
      50, 435, 400, 170, S_AGENT)
s.box("estim", "<b>Estimation</b> (règles en code)<br><br>"
               "Calcule le montant à rembourser, plafond et franchise compris.<br>"
               "Renvoie : le montant et le détail du calcul.<br><br>"
               + ROUGE_TXT + "juger la fraude, revenir sur l'éligibilité." + FIN,
      540, 300, 340, 170, S_AGENT)
s.box("fraude", "<b>Fraude, liaison avec le partenaire</b> (code)<br><br>"
                "Tourne à chaque demande : décide s'il y a suspicion. Si oui seulement, interroge le partenaire et contrôle sa réponse.<br>"
                "Renvoie : pas de suspicion, verdict validé, réponse rejetée ou partenaire indisponible.<br><br>"
                + ROUGE_TXT + "rendre lui-même un verdict de fraude, envoyer une donnée hors contrat." + FIN,
      950, 280, 380, 210, S_AGENT)
s.box("partenaire", "<b>Partenaire anti-fraude</b> (agent A2A externe)<br>"
                    "Contrat, filtre des données et mode dégradé : chantier 2",
      1000, 610, 300, 70, S_EXT)

s.box("ambig", "<b>Point ambigu tranché : qui déclare une suspicion de fraude ?</b><br><br>"
               "Seul l'agent Fraude. Pièces et Estimation lui transmettent des faits (une incohérence, un montant), "
               "jamais le mot « fraude ». Le partenaire rend le verdict ; l'agent Fraude décide seulement s'il faut le demander.<br><br>"
               "<i>Raison : le brief interdit déjà à l'estimation de juger la fraude ; un seul propriétaire donne "
               "une seule liste de critères à tester et une seule porte vers le partenaire.</i>",
      500, 560, 440, 190, S_AMBIG)
s.box("autres", "<b>Deux autres frontières tranchées</b><br>"
                "• Plafond du contrat : Estimation, car il fait partie du calcul du montant.<br>"
                "• Pièces manquantes : constatées par Pièces ; le statut est décidé par l'orchestrateur, avec sa table de décision.",
      30, 660, 440, 100, S_NOTE)

# délégations (pointillé vert)
s.edge("d1", "orch", "elig", E_DELEG, "délègue", [(451, 200), (410, 200)], sortie=(0.08, 1), entree=(0.9, 0))
s.edge("d2", "orch", "estim", E_DELEG, "délègue", sortie=(0.3, 1), entree=(0.5, 0))
s.edge("d3", "orch", "fraude", E_DELEG, "délègue", [(980, 230), (1140, 230)], sortie=(0.9, 1), entree=(0.5, 0))
# dépendances de données (trait plein)
s.edge("p1", "elig", "estim", E_DEP, "éligible = oui", sortie=(1, 0.5), entree=(0, 0.35))
s.edge("p2", "pieces", "estim", E_DEP, "pièces complètes", [(495, 500), (495, 420)], sortie=(1, 0.38), entree=(0, 0.7))
s.edge("p3", "estim", "fraude", E_DEP, "montant (un fait)", sortie=(1, 0.5), entree=(0, 0.55))
# fait transmis à Fraude (pointillé orange)
s.edge("f1", "pieces", "fraude", E_FAIT, "incohérences constatées (des faits)", [(480, 590), (480, 530), (1000, 530)],
       sortie=(1, 0.89), entree=(0.13, 1))
# partenaire (gris, chantier 2)
s.edge("x1", "fraude", "partenaire", E_EXT, "seulement si suspicion", sortie=(0.45, 1), entree=(0.4, 0))
s.edge("x2", "partenaire", "fraude", E_EXT, "verdict à valider", [(1250, 560)], sortie=(0.83, 0), entree=(0.79, 1))

s.legende([(VERT, "Code (orchestration)"), (BLEU, "Agent spécialiste"), (ORANGE, "Point ambigu tranché"),
           (ROUGE, "Frontière : interdit"), (GRIS, "Externe ou chantier 2")], 30, 800)
s.box("lg2", "Trait plein : dépendance de données · pointillé vert : délégation · pointillé orange : fait transmis à Fraude",
      30, 836, 900, 20, S_SOUS)
s.ecrire("schema-1-carte-des-agents", "Carte des agents", 1360, 870)

# =============================================================================================================
# Schéma 2 : l'orchestration et la terminaison garantie
# =============================================================================================================
s = Schema()
s.box("t", "Kaldera V2 · Orchestration et terminaison garantie · Chantier 1", 30, 20, 1100, 30, S_TITRE)
s.box("st", "Délégations, conditions d'arrêt et bornes provisoires. Chaque chemin finit par une décision "
            "ou par une escalade humaine motivée.", 30, 54, 1100, 22, S_SOUS)

s.box("deleg", "Chaque flèche est une transition décidée par l'orchestrateur (code). "
               "Les agents ne s'appellent jamais entre eux. L'état est sauvegardé après chaque étape.",
      560, 100, 440, 60, S_NOTE)
s.box("s0", "<b>Demande reçue</b><br>état créé et sauvegardé", 170, 95, 320, 52, S_ORCH + "align=center;spacingLeft=0;")
s.box("par", "En parallèle", 40, 182, 580, 110, S_GROUPE)
s.box("e", "<b>Éligibilité</b>", 60, 215, 250, 55, S_AGENT + "align=center;verticalAlign=middle;spacingLeft=0;")
s.box("p", "<b>Pièces justificatives</b>", 350, 215, 250, 55, S_AGENT + "align=center;verticalAlign=middle;spacingLeft=0;")
s.box("d1", "Refus bloquant ?", 230, 325, 200, 100, S_LOSANGE)
s.box("crit", "Refus bloquant : non éligible, ou pièces manquantes si specs_metier.md le prévoit (à confirmer).",
      560, 330, 330, 60, S_AMBIG + "fontSize=11;")
s.box("est", "<b>Estimation</b>", 180, 475, 300, 55, S_AGENT + "align=center;verticalAlign=middle;spacingLeft=0;")
s.box("d2", "Agent Fraude :<br>suspicion ?", 230, 570, 200, 100, S_LOSANGE)
s.box("part", "<b>Appel au partenaire A2A</b><br>chantier 2", 560, 590, 280, 60, S_EXT)
s.box("deg", "<b>Mode dégradé</b> défini par specs_metier.md<br>chantier 2", 560, 715, 280, 60, S_EXT)
s.box("tab", "<b>Table de décision</b><br>orchestrateur, code", 180, 800, 300, 60, S_ORCH + "align=center;spacingLeft=0;")

s.box("acc", "<b>DÉCISION : ACCEPTÉE</b><br>montant fixé par l'Estimation", 40, 950, 260, 64, S_FIN_OK)
s.box("ref", "<b>DÉCISION : REFUSÉE</b><br>avec le motif", 360, 950, 260, 64, S_FIN_OK)
s.box("esc", "<b>ESCALADE HUMAINE MOTIVÉE</b><br>motif · étape atteinte · données disponibles · tentatives faites",
      700, 940, 340, 84, S_FIN_ESC)

s.box("bornes", "<b>Bornes provisoires</b><br>vérifiées par l'orchestrateur avant chaque délégation<br><br>"
                "• Étapes par demande : 10 au plus<br>&nbsp;&nbsp;&nbsp;(le chemin le plus long prévu en compte 7)<br>"
                "• Appels par agent : 2 au plus<br>&nbsp;&nbsp;&nbsp;(1 essai, puis 1 relance si exception, sortie invalide ou délai dépassé)<br>"
                "• Même état vu deux fois : arrêt immédiat<br>"
                "• Délai global par demande : 120 s<br>"
                "• Budget LLM par demande : fixé après mesure du cas nominal<br><br>"
                "<i>Valeurs de départ. Le plan d'épreuve du chantier 2 les confirme ou les ajuste ; "
                "chaque changement entre au journal des ajustements.</i>",
      1080, 100, 400, 240, S_AMBIG + "fillColor=#fff2cc;strokeColor=#bf9000;arcSize=4;")

s.edge("a1", "s0", "e", E_DELEG, "délègue", [(330, 168), (185, 168)], sortie=(0.5, 1), entree=(0.5, 0))
s.edge("a2", "s0", "p", E_DELEG, "délègue", [(330, 168), (475, 168)], sortie=(0.5, 1), entree=(0.5, 0))
s.edge("a3", "e", "d1", E_DEP, "", [(185, 305), (330, 305)], sortie=(0.5, 1), entree=(0.5, 0))
s.edge("a4", "p", "d1", E_DEP, "", [(475, 305), (330, 305)], sortie=(0.5, 1), entree=(0.5, 0))
s.edge("a5", "d1", "est", E_DEP, "non", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("a6", "d1", "tab", E_DEP, "oui : arrêt anticipé", [(140, 375), (140, 830)], sortie=(0, 0.5), entree=(0, 0.5))
s.edge("a6b", "d1", "crit", E_FAIT, "", sortie=(1, 0.5), entree=(0, 0.5))
s.edge("a7", "est", "d2", E_DEP, "", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("a8", "d2", "tab", E_DEP, "non", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("a9", "d2", "part", E_EXT, "oui", sortie=(1, 0.5), entree=(0, 0.5))
s.edge("a10", "part", "tab", E_EXT, "verdict validé", [(588, 700), (450, 700)], sortie=(0.1, 1), entree=(0.9, 0))
s.edge("a11", "part", "deg", E_EXT, "indisponible, trop lent ou réponse rejetée", sortie=(0.6, 1), entree=(0.6, 0))
s.edge("a12", "deg", "tab", E_EXT, "la demande continue", [(520, 745), (520, 836)], sortie=(0, 0.5), entree=(1, 0.6))
s.edge("a13", "deg", "esc", E_ESC, "la demande est routée", sortie=(0.85, 1), entree=(0.55, 0))
s.edge("a14", "tab", "acc", E_OK, "", [(240, 905), (170, 905)], sortie=(0.2, 1), entree=(0.5, 0))
s.edge("a15", "tab", "ref", E_OK, "", [(360, 905), (490, 905)], sortie=(0.6, 1), entree=(0.5, 0))
s.edge("a16", "tab", "esc", E_ESC, "selon la table", [(450, 920), (980, 920)], sortie=(0.9, 1), entree=(0.82, 0))
s.edge("a17", "bornes", "esc", E_ESC, "borne atteinte, ou agent en échec après sa relance",
       [(1280, 982)], sortie=(0.5, 1), entree=(1, 0.5))

s.legende([(VERT, "Décision de l'orchestrateur"), (BLEU, "Étape déléguée"), (OK, "Fin : décision"),
           (ESC, "Fin : escalade humaine"), (GRIS, "Chantier 2"), (ORANGE, "À confirmer")], 30, 1060)
s.ecrire("schema-2-orchestration", "Orchestration et terminaison", 1510, 1100)

# =============================================================================================================
# Schéma 3 : la mémoire partagée de la demande
# =============================================================================================================
s = Schema()
s.box("t", "Kaldera V2 · Mémoire partagée de la demande · Chantier 1", 30, 20, 1100, 30, S_TITRE)
s.box("st", "Un état par demande, sauvegardé après chaque étape. Chaque section a un seul propriétaire, "
            "et l'orchestrateur est le seul à écrire.", 30, 54, 1100, 22, S_SOUS)

s.box("orch", "<b>Orchestrateur : le seul à écrire</b><br>"
              "1. reçoit le résultat d'un agent · 2. le valide contre le schéma de sortie de cet agent · "
              "3. l'écrit dans la section de cet agent, et nulle part ailleurs · 4. ajoute l'événement au journal · 5. sauvegarde l'état",
      430, 92, 640, 78, S_ORCH)

s.box("agents", "Agents spécialistes : lecture seule, sections utiles seulement", 30, 230, 350, 560, S_GROUPE)
s.box("ae", "<b>Éligibilité</b><br>lit : demande", 50, 270, 310, 60, S_AGENT)
s.box("ap", "<b>Pièces justificatives</b><br>lit : demande", 50, 350, 310, 60, S_AGENT)
s.box("aes", "<b>Estimation</b><br>lit : demande, eligibilite, pieces<br>"
             f'<font color="{ROUGE}">ne lit pas : fraude</font>', 50, 430, 310, 80, S_AGENT)
s.box("af", "<b>Fraude</b><br>lit : demande, pieces (incohérences), estimation (montant)", 50, 530, 310, 70, S_AGENT)
s.box("apar", "Éligibilité et Pièces tournent en parallèle sans conflit : chacune a sa section, et un seul écrivain.",
      50, 620, 310, 70, S_NOTE)

s.box("etat", "État de la demande · claim_id", 430, 230, 640, 560, S_CONTENEUR)
SEC_NEUTRE = BASE + GAUCHE + "rounded=0;fillColor=#ffffff;strokeColor=#999999;"
SEC_AGENT = BASE + GAUCHE + f"rounded=0;fillColor=#cfe2f3;strokeColor={BLEU};"
SEC_ORCH = BASE + GAUCHE + f"rounded=0;fillColor=#d9ead3;strokeColor={VERT};"
sections = [
    ("demande", "<b>demande</b> : données reçues<br>écrite à la création, puis en lecture seule · lue par : tous les agents", SEC_NEUTRE),
    ("eligibilite", "<b>eligibilite</b><br>propriétaire : Éligibilité · lue par : orchestrateur, Estimation", SEC_AGENT),
    ("pieces", "<b>pieces</b><br>propriétaire : Pièces · lue par : orchestrateur, Estimation, Fraude", SEC_AGENT),
    ("estimation", "<b>estimation</b><br>propriétaire : Estimation · lue par : orchestrateur, Fraude", SEC_AGENT),
    ("fraude", "<b>fraude</b> : suspicion, verdict validé, taskId et contextId A2A<br>propriétaire : Fraude · lue par : orchestrateur seulement", SEC_AGENT),
    ("controle", "<b>controle</b> : étape en cours, compteurs des bornes, statut final, motif d'escalade<br>"
                 "propriétaire : orchestrateur · lue par : orchestrateur, humain en cas d'escalade", SEC_ORCH),
    ("journal", "<b>journal</b> : un événement par étape (qui, quoi, quand, durée, résultat), ajout seul<br>"
                "source des métriques par agent (latence, échecs, recours à l'externe)", SEC_ORCH),
]
y = 270
for sid, texte, style in sections:
    s.box(sid, texte, 450, y, 600, 60, style)
    y += 72

s.box("sauve", "<b>Sauvegarde après chaque étape</b><br>reprise après un crash, sans demande oubliée", 1140, 270, 320, 110, S_CYL)
s.box("front", "<b>La frontière passe aussi par les données</b><br>"
               "Un agent n'écrit jamais lui-même. L'Estimation ne voit pas la section fraude, "
               "donc elle ne peut pas s'en servir.", 1140, 410, 340, 84, S_AMBIG)
s.box("part", "<b>Partenaire anti-fraude</b><br>reçoit seulement les champs du contrat, construits par le filtre (chantier 2)",
      1140, 548, 320, 80, S_EXT)
s.box("metr", "<b>Monitorage par agent</b> (chantier 2)<br>calculé à partir du journal", 1140, 702, 320, 60, S_EXT)

s.edge("m1", "agents", "orch", E_DEP, "renvoie son résultat, jamais d'écriture directe", [(205, 131)],
       sortie=(0.5, 0), entree=(0, 0.5))
s.edge("m2", "orch", "etat", E_DEP, "écrit, après validation", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("m3", "etat", "agents", E_DELEG + "strokeWidth=2;", "lit", sortie=(0, 0.482), entree=(1, 0.482))
s.edge("m4", "etat", "sauve", E_OK, "sauvegarde", sortie=(1, 0.125), entree=(0, 0.5))
s.edge("m5", "fraude", "part", E_EXT, "filtre", sortie=(1, 0.5), entree=(0, 0.5))
s.edge("m6", "journal", "metr", E_EXT, "", sortie=(1, 0.5), entree=(0, 0.5))

s.legende([(VERT, "Orchestrateur, seul écrivain"), (BLEU, "Section d'un agent"), (ORANGE, "Frontière par les données"),
           (ROUGE, "Lecture interdite"), (GRIS, "Externe ou chantier 2")], 30, 820)
s.ecrire("schema-3-memoire-partagee", "Mémoire partagée", 1490, 860)
