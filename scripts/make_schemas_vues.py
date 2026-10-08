# Vues d'ensemble de Kaldera V2, en trois niveaux : N0 les enjeux et les six exigences, N1 le système complet
# (chantier 1, chantier 2 et partenaire), N2 l'épreuve du réel. Fondées sur l'état de la conception au 07/10/2026 ;
# N1 mis à jour le 08/10/2026 (lecture des pièces, contrôles dans l'ordre).
# Palette, styles et classe Schema : schema_commun.py.

from schema_commun import *  # noqa: F403 (palette, styles, Schema)

ORANGE_E = "#b45f06"
VERT_OK = "#38761d"
S_ROUGE = BASE + GAUCHE + f"rounded=1;fillColor=#f8d7da;strokeColor={ROUGE};strokeWidth=2;"
S_CARTE_E = BASE + GAUCHE + f"rounded=1;fillColor=#ffffff;strokeColor={ORANGE_E};strokeWidth=2;"
S_CARTE = BASE + GAUCHE + f"rounded=1;fillColor=#ffffff;strokeColor={BLEU};strokeWidth=2;"
S_PILULE = BASE + "rounded=1;arcSize=50;fillColor=#f3f3f3;strokeColor=#666666;fontStyle=1;"


def e(*nums):
    """Badge des exigences, par exemple e(1, 2) -> [E1] [E2]."""
    return f'<font color="{ORANGE_E}"><b>' + " ".join(f"[E{n}]" for n in nums) + "</b></font>"


def ok(texte):
    return f'<font color="{VERT_OK}"><b>{texte}</b></font>'


def interdit(texte):
    return f'<font color="{ROUGE}">Interdit : {texte}</font>'


# =============================================================================================================
# N0 : pourquoi Kaldera V2, le problème métier et les six exigences
# =============================================================================================================
s = Schema()
s.box("t", "Kaldera V2 · Pourquoi : le problème métier et les six exigences · Niveau 0", 30, 20, 1300, 30, S_TITRE)
s.box("st", "Ce que le client vit aujourd'hui, ce qui a changé chez le partenaire, et les six exigences de la direction des "
            "opérations, avec ce qui tient chacune dans la conception.", 30, 54, 1440, 22, S_SOUS)

s.box("avant", "<b>Avant : un seul agent généraliste</b><br><br>"
               "Il mélange les rôles : personne ne peut vérifier qui a décidé quoi.<br><br>"
               f'<font color="{ROUGE}"><b>Partenaire muet : la demande reste bloquée, parfois des semaines, '
               "et personne n'est prévenu.</b></font>", 30, 100, 650, 140, S_ROUGE)
s.box("contrat", "<b>Le partenaire a durci son contrat (version 2.0)</b><br><br>"
                 "Schéma strict · exactement 7 champs, aucune donnée d'identité, de coordonnées ni bancaire · "
                 "un seul appel par dossier, aucune relance · réponse garantie en 2 s.<br><br>"
                 + ok("Objectif : une issue pour chaque demande en 10 s, même partenaire en panne, prouvée sur "
                      "28 scénarios."), 30, 260, 650, 165, S_AMBIG)
s.box("reponse", "<b>La réponse de la conception</b><br>"
                 "• une Coordination en code et quatre agents de contrôle (niveau 1, chantier 1)<br>"
                 "• une mémoire de session lue et écrite par la seule Coordination<br>"
                 "• une liaison A2A filtrée et validée, avec un mode dégradé (niveau 1, chantier 2)<br>"
                 "• un plan d'épreuve de 28 scénarios, et un journal des ajustements (niveau 2)",
      30, 445, 650, 135, S_ORCH)

EXIG = [
    ("E1", "Toute demande se termine par une décision ou une escalade humaine motivée, jamais par un blocage silencieux.",
     "les règles du § 10 dans l'ordre et les bornes, signalées dans arret"),
    ("E2", "Chaque agent a un rôle et une frontière définis ; aucun agent n'empiète sur le rôle d'un autre.",
     "une section par agent, rangée par la Coordination ; la trace (agent, ecrit)"),
    ("E3", "Seules les données prévues au contrat partent chez le partenaire, rien d'autre.",
     "huit données passées à l'agent Anti-fraude, puis un filtre de 7 champs"),
    ("E4", "Une réponse du partenaire non conforme au contrat est rejetée, jamais propagée telle quelle.",
     "une validation à cinq niveaux ; seule la raison du rejet est gardée"),
    ("E5", "Partenaire indisponible : le mode dégradé défini par le métier s'applique.",
     "§ 9 : 1 500 € ou moins, la demande poursuit ; au-delà, cellule_fraude"),
    ("E6", "Aucune boucle infinie ; métriques par agent visibles ; tout ajustement provoqué par l'épreuve est consigné.",
     "les bornes, quatre métriques par agent, le journal des ajustements"),
]
for k, (code, texte, tenu) in enumerate(EXIG):
    x = 720 + (k % 2) * 390
    y = 100 + (k // 2) * 165
    s.box(f"c{code}", f'<font style="font-size:26px" color="{ORANGE_E}"><b>{code}</b></font><br>{texte}<br><br>'
                      f"<i>Tenu par : {tenu}.</i>", x, y, 370, 150, S_CARTE_E)

s.legende([(ROUGE, "Le problème"), (ORANGE, "Le contrat du partenaire"), (VERT, "La réponse de la conception"),
           (ORANGE, "Une exigence et ce qui la tient")], 30, 610)
s.ecrire("schema-N0-enjeux-exigences", "Niveau 0 · Enjeux et exigences", 1500, 660)

# =============================================================================================================
# N1 : le système complet, chantier 1, chantier 2 et partenaire
# =============================================================================================================
s = Schema()
s.box("t", "Kaldera V2 · Le système complet : l'équipe, la liaison A2A et le partenaire · Niveau 1", 30, 20, 1500, 30, S_TITRE)
s.box("st", "Un dossier de pièces est lu à gauche (phase E, ajoutée le 08/10/2026) ; la Coordination appelle chaque agent dans "
            "l'ordre, avec ses seules entrées, et range son résultat ; si un indicateur de fraude est présent, un seul appel part "
            "chez le partenaire, à travers le filtre et la validation.",
      30, 54, 1900, 22, S_SOUS)

s.box("ch1", "Chantier 1 · L'équipe et son orchestration", 30, 95, 1150, 835, S_CONTENEUR)
s.box("ch2", "Chantier 2 · La liaison A2A (côté Kaldera)", 1195, 95, 435, 835, S_CONTENEUR)
s.box("ext", "Partenaire (externe)", 1650, 95, 330, 835,
      S_CONTENEUR + f"fillColor=#f7f7f7;strokeColor={GRIS};dashed=1;fontColor=#555555;")

# --- chantier 1 ---
s.box("recv", "<b>Lecture des pièces</b> (phase E)<br>Lecteurs de contrat et de pièces : modèle, schéma strict, "
               "demande § 3 (ou JSON déjà prêt). Un état par demande.",
      50, 130, 230, 105, S_LECTEUR)
s.box("coord", f"<b>Coordination · superviseur</b> (code, sans LLM) {e(1, 2, 6)}<br>"
               "Appelle chaque agent directement avec ses seules entrées, reçoit son résultat et le range dans sa section ; "
               "seule à lire et à écrire l'état. Vérifie les bornes avant chaque appel, applique les règles du § 10 "
               "dans l'ordre, conclut. Ne refait jamais un contrôle.", 300, 135, 560, 125, S_ORCH)
s.box("bornes", f"<b>Bornes</b> {e(1, 6)}, vérifiées avant chaque appel<br>"
                "• 10 s par demande (§ 12)<br>• 8 étapes, la dernière réservée à l'issue<br>• 2 demandes de complément<br>"
                "• même état vu deux fois : arrêt<br>• 1 appel au partenaire, abandon à 3 s<br>• 1 s par contrôle interne",
      880, 135, 280, 150, S_AMBIG)

s.box("par", "Dans l'ordre, 1 à 4 : chacun seulement si le précédent n'a pas conclu", 50, 290, 1120, 230, S_GROUPE + "verticalAlign=bottom;spacingBottom=2;")
s.box("elig", f"<b>1 · Éligibilité</b> {e(2)}<br><i>règles en code</i><br>"
              "E1 à E5 de la spec : contrat actif, cotisations, carence de 30 jours, délai de déclaration, garantie.<br>"
              + interdit("chiffrer, juger les pièces ou la fraude"), 65, 320, 245, 170, S_AGENT)
s.box("pieces", f"<b>2 · Pièces justificatives</b> {e(2)}<br><i>code ; lisibilité rendue par le Lecteur de pièces</i><br>"
                "Présence, lisibilité, type attendu ; adresse le complément que la Coordination lui confie.<br>"
                + interdit("conclure, chiffrer, juger la fraude"), 325, 320, 245, 170, S_AGENT)
s.box("estim", f"<b>3 · Estimation</b> {e(2)}<br><i>calcul en code</i><br>"
               "Justifié, retenu, moins la franchise, puis le plafond (point ambigu tranché).<br>"
               + interdit("juger la fraude, revenir sur l'éligibilité"), 600, 320, 260, 170, S_AGENT)
s.box("af", f"<b>4 · Anti-fraude</b> {e(2, 3)}<br><i>seuils en code</i><br>"
            "Reçoit 8 données, dont le montant justifié, jamais l'identité ni l'IBAN. Indicateurs F1 à F4 ; si l'un est présent, un seul appel "
            "au partenaire.<br>" + interdit("émettre un avis lui-même, relancer"), 880, 320, 280, 190, S_AGENT)

s.edge("e0", "recv", "coord", E_DEP, "", sortie=(1, 0.5), entree=(0, 0.4))
s.edge("d1", "coord", "elig", E_DELEG, "", [(311, 300), (285, 300)], sortie=(0.02, 1), entree=(0.9, 0))
s.edge("d2", "coord", "pieces", E_DELEG, "", sortie=(0.26, 1), entree=(0.5, 0))
s.edge("d3", "coord", "estim", E_DELEG, "", sortie=(0.77, 1), entree=(0.5, 0))
s.edge("d4", "coord", "af", E_DELEG, "", [(849, 310), (1020, 310)], sortie=(0.98, 1), entree=(0.5, 0))
s.edge("p0", "elig", "pieces", E_DEP, "", sortie=(1, 0.75), entree=(0, 0.75))
s.edge("p1", "pieces", "estim", E_DEP, "factures", sortie=(1, 0.75), entree=(0, 0.75))
s.edge("p2", "estim", "af", E_DEP, "", sortie=(1, 0.6), entree=(0, 0.6))

s.box("etat", f"État de la demande (mémoire de session) {e(2, 3)}", 50, 540, 560, 375, S_CONTENEUR)
SEC_N = BASE + GAUCHE + "rounded=0;fillColor=#ffffff;strokeColor=#999999;fontSize=11;"
SEC = [("s_dem", "<b>demande</b> : reçue, lecture seule", None),
       ("s_eli", "<b>eligibilite</b> : résultat d'Éligibilité", None), ("s_pie", "<b>pieces</b> : résultat de Pièces", None),
       ("s_est", "<b>estimation</b> : résultat d'Estimation", None), ("s_avi", "<b>avis_fraude</b> : résultat d'Anti-fraude", None),
       ("s_iss", "<b>issue</b> : écrite par la Coordination", "orch"), ("s_ctl", "<b>controle</b> : bornes, marqueur, arret", "orch"),
       ("s_tra", "<b>trace</b> : une ligne par étape (agent, ecrit)", "orch")]
SEC_A = BASE + GAUCHE + MILIEU + f"rounded=0;fillColor=#cfe2f3;strokeColor={BLEU};fontSize=11;"
SEC_O = BASE + GAUCHE + MILIEU + f"rounded=0;fillColor=#d9ead3;strokeColor={VERT};fontSize=11;"
for k, (sid, txt, kind) in enumerate(SEC):
    style = SEC_N + MILIEU if k == 0 else (SEC_O if kind == "orch" else SEC_A)
    s.box(sid, txt, 65 + (k % 2) * 270, 580 + (k // 2) * 70, 260, 58, style)
s.box("etat_n", "Seule la Coordination lit et écrit ; aucun agent ne reçoit l'état complet ; jamais exposé par A2A.",
      65, 865, 530, 40, S_SOUS)
s.edge("lit", "coord", "etat", E_DEP + "startArrow=block;startFill=1;", "lit et range", [(40, 247), (40, 595)],
       sortie=(0, 0.9), entree=(0, 0.15))

s.box("fF", "Indicateur<br>F1 à F4 ?", 930, 545, 180, 90, S_LOSANGE)
s.edge("af_f", "af", "fF", E_DEP, "", sortie=(0.5, 1), entree=(0.5, 0))
s.box("regles", f"<b>Règles de décision (§ 10)</b> {e(1)}<br>dans l'ordre, la première qui s'applique fixe l'issue : "
                "éligible ? pièces complètes ? montant nul ? avis anti-fraude ? plus de 10 000 € ? sinon acceptée",
      640, 660, 250, 135, S_ORCH)
s.edge("f_non", "fF", "regles", E_DEP, "non : avis non requis", [(765, 590)], sortie=(0, 0.5), entree=(0.5, 0))
s.box("o_acc", "<b>Acceptée</b> · montant remboursé", 920, 660, 240, 48, S_FIN_OK)
s.box("o_ref", "<b>Refusée</b> · motif, conditions citées", 920, 718, 240, 48, S_FIN_OK)
s.box("o_ges", "<b>Escalade gestionnaire</b> · motif", 920, 776, 240, 48, S_FIN_ESC)
s.box("o_cel", "<b>Escalade cellule_fraude</b> · motif", 920, 834, 240, 48, S_FIN_ESC)
for oid in ("o_acc", "o_ref", "o_ges", "o_cel"):
    s.edge(f"r_{oid}", "regles", oid, E_DEP, "", sortie=(1, 0.5), entree=(0, 0.5))
s.box("fiche", "<b>Fiche de décision</b> (§ 11) : issue, montant, motif, file, avis, mode dégradé, trace, arret",
      640, 815, 250, 95, S_NOTE)

# --- chantier 2 ---
s.box("filtre", f"<b>Filtre sortant</b> {e(3)}<br>Message neuf construit depuis une liste blanche : exactement 7 champs, "
                "dont 2 calculés (ancienneté, département). Validé contre un schéma strict ; en cas d'échec, rien ne part.",
      1215, 135, 395, 120, S_ORCH)
s.box("appel", f"<b>Appel unique</b> {e(5)}<br>message/send, jeton Bearer ; marqueur d'appel écrit avant par la "
               "Coordination ; abandon à 3 s ; aucune relance (contrat § 6).", 1215, 285, 395, 110, S_ORCH)
s.box("valid", f"<b>Validation de la réponse</b> {e(4)}, cinq niveaux<br>1 · transport · 2 · enveloppe JSON-RPC · "
               "3 · forme A2A (tâche terminée) · 4 · schéma (6 champs) · 5 · cohérence (même dossier, score de 0 à 1, "
               "niveau cohérent)<br>Au premier échec : réponse écartée, seule la raison est gardée.",
      1215, 425, 395, 160, S_ORCH)
s.box("dv", "Avis conforme<br>et reçu en 3 s ?", 1322, 605, 180, 85, S_LOSANGE)
s.box("retenu", "<b>Avis retenu</b><br>rangé dans avis_fraude ; règle 4 : faible poursuit, modéré gestionnaire, "
                "élevé cellule_fraude", 1215, 720, 190, 110, S_FIN_OK)
s.box("degr", f"<b>Mode dégradé (§ 9)</b> {e(5)}<br>avis indisponible (délai, erreur, réponse écartée) :<br>"
              "• 1 500 € ou moins : la demande poursuit, marquée<br>• au-delà : escalade cellule_fraude<br>"
              "Les demandes sans indicateur ne sont jamais touchées.", 1420, 720, 195, 195, S_AMBIG)
s.box("tard", "Réponse tardive : jamais lue ; jamais de rappel (doublon -32029).", 1215, 845, 190, 70, S_NOTE)
s.edge("f_oui", "fF", "filtre", E_DEP, "oui", [(1185, 590), (1185, 195)], sortie=(1, 0.5), entree=(0, 0.5))
s.edge("x1", "filtre", "appel", E_DEP, "7 champs", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("x2", "valid", "dv", E_DEP, "", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("x3", "dv", "retenu", E_OK, "oui", sortie=(0, 0.5), entree=(0.5, 0))
s.edge("x4", "dv", "degr", E_ESC, "non", sortie=(1, 0.5), entree=(0.5, 0))

# --- partenaire ---
s.box("card", "<b>Agent Card</b><br>GET /.well-known/agent.json ; lue une fois au démarrage", 1670, 135, 290, 90, S_EXT)
s.box("part", "<b>Partenaire anti-fraude</b><br>agent A2A d'une autre entreprise : une boîte noire. Rend un avis "
              "consultatif : faible, modéré ou élevé.", 1670, 285, 290, 110, S_EXT)
s.box("tache", "<b>Tâche A2A</b><br>état completed ; artefact data de 6 champs : référence, score, niveau, indicateurs, "
               "evaluation_id, version du modèle ; renvoyée, ou une erreur, à la validation", 1670, 440, 290, 120, S_EXT)
s.box("cv2", "<b>Contrat d'échange v2.0</b><br>• requête : 7 champs exactement<br>• réponse : 6 champs<br>"
             "• réponse garantie en 2 s ; abandon à 3 s<br>• un appel par dossier, aucune relance<br>"
             "• erreurs : 401, 503, -32700, -32600, -32601, -32602, -32029", 1670, 600, 290, 200, S_NOTE)
s.edge("y1", "appel", "part", E_EXT, "", sortie=(1, 0.5), entree=(0, 0.5))
s.edge("y2", "part", "tache", E_EXT, "", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("y3", "tache", "valid", E_EXT, "", sortie=(0, 0.5), entree=(1, 0.5))

# --- bas : preuve, métriques, journal ---
s.box("preuve", f"<b>Plan de preuve</b> {e(1, 2)}<br>28 scénarios rejoués ; chaque fiche comparée au champ attendu ; "
                "chaque section remplie par son seul agent (niveau 2)", 30, 950, 600, 90, S_NOTE)
s.box("metr", f"<b>Métriques par agent</b> {e(6)}<br>appels, échecs, latence, appels externes, calculés depuis la trace ; "
              "signaux d'équipe : étapes, bornes atteintes, issues, part en mode dégradé", 650, 950, 600, 90, S_EXT)
s.box("journal", f"<b>Journal des ajustements</b> {e(6)}<br>chaque changement provoqué par l'épreuve : scénario, signal, "
                 "valeur avant et après, résultat du rejeu, commit (niveau 2)", 1270, 950, 710, 90, S_NOTE)

s.legende([(VERT, "Code (Coordination, liaison)"), (CYAN, "Agent de lecture"), (BLEU, "Agent de contrôle"), (ORANGE, "Bornes, mode dégradé"),
           (GRIS, "Partenaire externe"), (ESC, "Escalade humaine")], 30, 1065)
s.box("lg2", "Pointillé vert : appel avec ses entrées · trait plein : résultat ou données · pointillé gris : échange avec "
             "le partenaire, à travers la frontière de confiance : tout ce qui la franchit est filtré ou validé · [E1] à [E6] : exigences tenues par le bloc", 30, 1101, 1300, 20, S_SOUS)
s.ecrire("schema-N1-systeme-complet", "Niveau 1 · Système complet", 2000, 1140)

# =============================================================================================================
# N2 : l'épreuve du réel
# =============================================================================================================
s = Schema()
s.box("t", "Kaldera V2 · L'épreuve du réel : rejouer, observer, ajuster · Niveau 2", 30, 20, 1300, 30, S_TITRE)
s.box("st", "Chaque scénario de eval/scenarios.jsonl est rejoué par traiter_lot avec un partenaire simulé ; tout écart provoque "
            "un seul ajustement du chantier 1, consigné, puis un nouveau rejeu.", 30, 54, 1820, 22, S_SOUS)

BOUCLE = [("b1", f"<b>1 · Rejouer</b> {e(6)}<br>un scénario par traiter_lot, partenaire simulé réglé par le scénario", S_ORCH),
          ("b2", f"<b>2 · Observer</b> {e(6)}<br>issue, trace (agent, ecrit), métriques par agent, durées", S_ORCH),
          ("b3", f"<b>3 · Comparer</b> {e(6)}<br>au champ attendu et aux invariants : conforme ou écart", S_ORCH),
          ("b4", f"<b>4 · Ajuster</b> {e(6)}<br>chantier 1 : une borne, une frontière ou un routage ; un seul changement à la fois",
           S_AMBIG)]
for k, (bid, txt, style) in enumerate(BOUCLE):
    s.box(bid, txt, 30 + k * 370, 100, 320, 110, style)
s.box("b5", f"<b>5 · Consigner</b> {e(6)}<br>journal : scénario, signal, avant, après, rejeu, commit", 1510, 95, 340, 125, S_CYL)
for a, b in [("b1", "b2"), ("b2", "b3"), ("b3", "b4"), ("b4", "b5")]:
    s.edge(f"l_{a}", a, b, E_DEP, "", sortie=(1, 0.5), entree=(0, 0.5))
s.edge("l_ret", "b5", "b1", E_DEP, "rejeu des 28 scénarios et des tests unitaires, jusqu'à ce que tous les critères tiennent",
       [(1680, 245), (190, 245)], sortie=(0.5, 1), entree=(0.5, 1))

s.box("bouchon", "Partenaire simulé (bouchon)", 30, 280, 330, 300, S_CONTENEUR)
for k, (txt) in enumerate(["normal · NOM, AF, BCL", "lent · 5 s, au-delà des 3 s · PAN-02",
                           "invalide · 7 variantes · INV", "panne · PAN-01"]):
    s.box(f"m{k}", txt, 50, 320 + k * 55, 290, 42, S_PILULE)
s.box("bouchon_n", "Piloté par scripts/partner_ctl.py, absent de l'archive : un bouchon local le remplace.",
      50, 540, 290, 35, S_SOUS)
s.box("rejeux", "<b>Combien de rejeux ?</b><br>Un seul suffit pour juger une issue : aucun LLM et un bouchon déterministe. "
                "Les scénarios de panne sont rejoués 5 fois pour les durées : c'est la plus lente qui compte face aux 10 s.",
      30, 600, 330, 165, S_NOTE)

CARTES = [
    (f"<b>Cas nominaux · NOM-01 à 11</b> {e(1, 2)}", "issue, trace, étapes, appels externes",
     "11 fiches conformes ; chaque section remplie par son seul agent ; 0 appel au partenaire"),
    (f"<b>Rangement hors section · test unitaire</b> {e(2)}",
     "la Coordination tente de ranger un résultat dans la section d'un autre agent",
     "erreur de droits ; aucun agent ne reçoit l'état complet"),
    (f"<b>Données sensibles · test unitaire</b> {e(3)}", "le message reçu par le bouchon",
     "exactement 7 champs ; ni nom, ni e-mail, ni IBAN, ni description"),
    (f"<b>Anti-fraude · AF-01 à 07</b> {e(1, 3)}", "appels externes, échecs, message envoyé, avis",
     "7 appels, 0 échec ; bon niveau et bonne issue (AF-03 : avis faible mais plus de 10 000 €, escalade)"),
    (f"<b>Réponses invalides · INV-01 à 07</b> {e(4, 5)}", "niveau de rejet et raison, avis, mode dégradé",
     "chacune écartée à son niveau, rien recopié ; 1 500 € ou moins acceptée en mode dégradé, au-delà cellule_fraude"),
    (f"<b>Partenaire en panne · PAN-01, lot de 5</b> {e(5, 6)}", "appels externes, échecs, issues du lot",
     "2 appels, 2 échecs, 0 relance ; 0401 et 0405 non touchés"),
    (f"<b>Partenaire lent · PAN-02, 5 s, lot de 3</b> {e(5, 6)}", "durée de chaque appel, de chaque demande, du lot",
     "abandon à 3 s ; chaque demande sous 10 s ; lot d'environ 3 s, et non 6"),
    (f"<b>Piège à boucle · BCL-01</b> {e(1, 6)}", "longueur de la trace, arret",
     "escalade avec arret ; trace de 8 étapes au plus"),
]
for k, (titre, signal, critere) in enumerate(CARTES):
    x = 390 + (k % 4) * 370
    y = 280 + (k // 4) * 255
    s.box(f"k{k}", f"{titre}<br><br>signal : {signal}<br><br>" + ok("réussite : " + critere), x, y, 355, 235, S_CARTE)

s.box("totaux", "<b>Chiffres attendus sur les 28 scénarios (34 demandes)</b><br>"
                "16 acceptées · 7 refusées · 4 escalades gestionnaire · 6 escalades cellule_fraude · "
                "1 escalade à file non fixée (BCL-01)<br>11 en mode dégradé · 1 borne atteinte · 18 appels au partenaire, "
                "jamais deux par dossier · 11 échecs de l'agent antifraude", 30, 800, 900, 120, S_ORCH)
s.box("ligne", "<b>Une ligne du journal (exemple fictif : aucun ajustement n'a été fait à ce jour)</b><br>"
               "PAN-02 → une demande arrêtée à 10 s rend sa fiche à 10,4 s → duree_max_s abaissée de 10 à 8 s → "
               "rejeu : 28 sur 28, tests unitaires verts → commit.", 950, 800, 900, 120, S_NOTE)

s.legende([(VERT, "Étape de contrôle"), (ORANGE, "Ajustement du chantier 1"), (BLEU, "Scénario ou test"),
           (GRIS, "Partenaire simulé")], 30, 945)
s.ecrire("schema-N2-epreuve-du-reel", "Niveau 2 · Épreuve du réel", 1880, 1000)
