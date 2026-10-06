# Schémas du chantier 1 de Kaldera V2 : arbre de décision, carte des agents, orchestration, mémoire partagée.
# Version fondée sur docs/specs_metier.md (v3.2) et docs/interface.md, reçus le 06/10/2026.
# Palette, styles et classe Schema : schema_commun.py.

from schema_commun import *  # noqa: F403 (palette, styles, Schema, arbre_de_decision)

ROUGE_TXT = f'<font color="{ROUGE}"><b>Interdit :</b> '
FIN = "</font>"
CENTRE = "align=center;verticalAlign=middle;spacingLeft=0;"

# =============================================================================================================
# Schéma 1 : la carte des agents
# =============================================================================================================
s = Schema()
s.box("t", "Kaldera V2 · Carte des agents · Chantier 1", 30, 20, 1000, 30, S_TITRE)
s.box("st", "Rôles, frontières, point ambigu tranché, dépendances et parallélisme. Fondé sur specs_metier.md (v3.2) "
            "et interface.md : une section métier n'est écrite que par un seul agent, et un agent n'écrit qu'une seule section.",
      30, 54, 1300, 22, S_SOUS)

s.box("orch", "<b>Coordination</b> (code, sans LLM) · <b>écrit : issue</b><br>"
              "Délègue chaque contrôle, vérifie les bornes, applique les règles de décision dans l'ordre (spec § 10), "
              "conclut la demande. Seule à conclure.<br>"
              + ROUGE_TXT + "refaire un contrôle (éligibilité, pièces, montant, fraude)." + FIN,
      380, 95, 700, 82, S_ORCH)

s.box("par", "Exécutés en parallèle : aucun n'a besoin du résultat de l'autre", 30, 225, 440, 420, S_GROUPE)
s.box("elig", "<b>Éligibilité</b> (règles en code) · <b>écrit : eligibilite</b><br><br>"
              "Vérifie E1 à E5 : contrat actif, cotisations, carence de 30 jours, délai de déclaration, garantie de la formule.<br>"
              "Renvoie : éligible oui ou non, conditions non remplies.<br><br>"
              + ROUGE_TXT + "chiffrer la demande, appliquer le plafond, juger les pièces ou la fraude." + FIN,
      50, 255, 400, 175, S_AGENT)
s.box("pieces", "<b>Pièces justificatives</b> (code) · <b>écrit : pieces</b><br><br>"
                "Vérifie présence, lisibilité et cohérence des pièces exigées. Demande un complément via l'espace assuré "
                "(seulement si la demande est éligible).<br>"
                "Renvoie : complet, ou manquantes ; les factures lisibles.<br><br>"
                + ROUGE_TXT + "conclure ou escalader la demande, chiffrer, juger la fraude." + FIN,
      50, 445, 400, 185, S_AGENT)
s.box("estim", "<b>Estimation</b> (règles en code) · <b>écrit : estimation</b><br><br>"
               "Montant justifié (factures lisibles), montant retenu (le plus petit des deux), "
               "moins la franchise, puis <b>plafond de la formule</b>.<br>"
               "Renvoie : montant justifié et montant estimé.<br><br>"
               + ROUGE_TXT + "juger la fraude, revenir sur l'éligibilité." + FIN,
      540, 255, 360, 200, S_AGENT)
s.box("fraude", "<b>Anti-fraude, liaison avec le partenaire</b> (code) · <b>écrit : avis_fraude</b><br><br>"
                "Calcule les indicateurs F1 à F4. Si au moins un : un seul appel au partenaire, puis contrôle de sa réponse.<br>"
                "Renvoie : non requis, avis (niveau et score), ou indisponible.<br><br>"
                + ROUGE_TXT + "émettre un avis en interne, envoyer une donnée hors contrat, relancer un appel." + FIN,
      1030, 255, 360, 220, S_AGENT)
s.box("partenaire", "<b>Partenaire anti-fraude</b> (agent A2A externe)<br>"
                    "rend l'avis : faible, modéré ou élevé · contrat, filtre et mode dégradé : chantier 2",
      1045, 600, 330, 80, S_EXT)

s.box("ambig", "<b>Point ambigu tranché : qui applique le plafond ?</b><br><br>"
               "La spec range le plafond dans l'éligibilité (§ 4), mais « le contrôle d'éligibilité ne chiffre pas » (§ 2), "
               "et l'estimation (§ 6) ne le cite pas. <b>Choix : l'Estimation</b>, parce que le plafond est un calcul de montant.<br><br>"
               "<i>Preuve, scénario NOM-05 : 4 200 € déclarés, moins 300 € de franchise = 3 900 €, plafonnés à 3 000 €.</i>",
      500, 560, 460, 190, S_AMBIG)
s.box("autres", "<b>Autres frontières tranchées</b><br>"
                "• Pièces manquantes : constatées par Pièces ; l'escalade est décidée par la Coordination (règle 2).<br>"
                "• Montant justifié : calculé par l'Estimation (§ 6), à partir des factures lisibles fournies par Pièces.<br>"
                "• Indicateurs F1 à F4 : Anti-fraude, après l'Estimation, car F4 compare le montant déclaré au montant justifié.",
      30, 670, 440, 130, S_NOTE)

s.edge("d1", "orch", "elig", E_DELEG, "délègue", [(420, 205), (410, 205)], sortie=(0.06, 1), entree=(0.9, 0))
s.edge("d2", "orch", "estim", E_DELEG, "délègue", sortie=(0.4, 1), entree=(0.5, 0))
s.edge("d3", "orch", "fraude", E_DELEG, "délègue", [(1000, 215), (1210, 215)], sortie=(0.89, 1), entree=(0.5, 0))
s.edge("p1", "pieces", "estim", E_DEP, "factures lisibles", [(495, 540), (495, 400)], sortie=(1, 0.5), entree=(0, 0.6))
s.edge("p2", "estim", "fraude", E_DEP, "montant justifié (pour F4)", sortie=(1, 0.5), entree=(0, 0.5))
s.edge("x1", "fraude", "partenaire", E_EXT, "si au moins un indicateur", sortie=(0.4, 1), entree=(0.4, 0))
s.edge("x2", "partenaire", "fraude", E_EXT, "avis à contrôler", [(1325, 560)], sortie=(0.85, 0), entree=(0.81, 1))

s.legende([(VERT, "Code (coordination)"), (BLEU, "Agent de contrôle"), (ORANGE, "Point ambigu tranché"),
           (ROUGE, "Frontière : interdit"), (GRIS, "Externe ou chantier 2")], 30, 830)
s.box("lg2", "Trait plein : dépendance de données · pointillé vert : délégation · « écrit » : la seule section métier de l'agent",
      30, 866, 900, 20, S_SOUS)
s.ecrire("schema-1-carte-des-agents", "Carte des agents", 1420, 900)

# =============================================================================================================
# Schéma 2 : l'orchestration et la terminaison garantie
# =============================================================================================================
s = Schema()
s.box("t", "Kaldera V2 · Orchestration et terminaison garantie · Chantier 1", 30, 20, 1100, 30, S_TITRE)
s.box("st", "Chaque losange est une règle de décision appliquée par la Coordination, dans l'ordre de la spec (§ 10) ; "
            "la première qui s'applique fixe l'issue. Chaque chemin finit par une décision ou par une escalade motivée.",
      30, 54, 1300, 22, S_SOUS)

FIN_REF = S_FIN_OK + CENTRE + "fontSize=11;"
FIN_ESC = S_FIN_ESC + CENTRE + "fontSize=11;"
s.box("s0", "<b>Demande reçue</b><br>état créé, section demande en lecture seule", 120, 95, 300, 52, S_ORCH + CENTRE)
s.box("par", "En parallèle", 30, 172, 520, 100, S_GROUPE)
s.box("e", "<b>Éligibilité</b><br>E1 à E5", 50, 200, 230, 55, S_AGENT + CENTRE)
s.box("p", "<b>Pièces</b><br>présence, lisibilité", 300, 200, 230, 55, S_AGENT + CENTRE)

s.box("r1", "Éligible ?", 160, 300, 220, 90, S_LOSANGE)
s.box("t1", "<b>DÉCISION : REFUSÉE</b> · règle 1<br>0 € ; le motif cite les conditions non remplies", 480, 315, 340, 60, FIN_REF)

s.box("r2", "Pièces exigées<br>présentes et lisibles ?", 160, 420, 220, 100, S_LOSANGE)
s.box("c", "<b>Pièces : demande de complément</b> (2 au plus)<br>via l'espace assuré, puis nouveau contrôle", 480, 440, 340, 60, S_AGENT + CENTRE)
s.box("t2", "<b>ESCALADE gestionnaire</b> · règle 2<br>motif : pièces manquantes", 880, 440, 300, 60, FIN_ESC)

s.box("est", "<b>Estimation</b><br>justifié, retenu, franchise, plafond", 120, 560, 300, 58, S_AGENT + CENTRE)
s.box("r3", "Montant estimé<br>nul ?", 160, 650, 220, 90, S_LOSANGE)
s.box("t3", "<b>DÉCISION : REFUSÉE</b> · règle 3<br>0 € ; dommage inférieur ou égal à la franchise", 480, 665, 340, 60, FIN_REF)

s.box("r4", "Anti-fraude :<br>un indicateur F1 à F4 ?", 160, 775, 220, 100, S_LOSANGE)
s.box("pa", "<b>Avis du partenaire</b> (chantier 2)<br>un seul appel, 3 s au plus, aucune relance", 480, 795, 340, 60, S_EXT)
s.box("t4a", "<b>ESCALADE gestionnaire</b> · avis modéré<br>motif : contrôle renforcé", 880, 745, 300, 56, FIN_ESC)
s.box("t4b", "<b>ESCALADE cellule_fraude</b> · avis élevé<br>motif : suspicion de fraude", 880, 815, 300, 56, FIN_ESC)
s.box("deg", "<b>Avis indisponible : mode dégradé</b> (§ 9)<br>délai dépassé, erreur ou réponse non conforme", 480, 905, 340, 60, S_EXT)
s.box("t4c", "<b>ESCALADE cellule_fraude</b><br>montant estimé &gt; 1 500 €, mode dégradé", 880, 905, 300, 56, FIN_ESC)

s.box("r5", "Montant estimé<br>&gt; 10 000 € ?", 160, 1010, 220, 90, S_LOSANGE)
s.box("t5", "<b>ESCALADE gestionnaire</b> · règle 5<br>motif : seuil de délégation dépassé", 480, 1025, 340, 60, FIN_ESC)
s.box("t6", "<b>DÉCISION : ACCEPTÉE</b> · règle 6<br>montant remboursé = montant estimé", 120, 1140, 300, 60, FIN_REF)

s.box("bornes", "<b>Bornes provisoires</b><br>vérifiées par la Coordination avant chaque délégation<br><br>"
                "• Durée par demande : <b>10 s</b> (engagement de service, spec § 12)<br>"
                "• Étapes par demande : <b>8</b> au plus<br>&nbsp;&nbsp;&nbsp;(chemin nominal : 5 ; plus 2 compléments ; plus 1 de marge)<br>"
                "• Demandes de complément : <b>2</b> au plus<br>"
                "• Même état vu deux fois : arrêt immédiat<br>"
                "• Délai par contrôle interne : 1 s · appel au partenaire : 3 s (contrat § 5)<br><br>"
                "<b>Borne atteinte</b> : ESCALADE gestionnaire, et la fiche le signale dans <i>arret</i> (nom de la borne).<br><br>"
                "<i>Fondées sur le chemin le plus long prévu par la spec et les scénarios ; "
                "le chantier 2 les éprouve (BCL-01, PAN-02), chaque changement entre au journal des ajustements.</i>",
      1240, 95, 400, 330, S_AMBIG + "fillColor=#fff2cc;strokeColor=#bf9000;arcSize=4;")
s.box("qui", "<b>Qui décide que la demande est terminée ?</b><br>"
             "La Coordination seule, en écrivant la section issue (« seule la décision conclut la demande », § 2). "
             "Aucun autre état final : jamais « en attente » sans qu'un humain en soit saisi.",
      1240, 450, 400, 110, S_NOTE)
s.box("comp", "<b>Pourquoi le complément après l'éligibilité ?</b><br>"
              "Une demande non éligible est refusée quel que soit l'état de ses pièces (règle 1) : "
              "inutile de solliciter l'assuré.", 1240, 585, 400, 90, S_NOTE)

s.edge("a1", "s0", "e", E_DELEG, "délègue", [(270, 165), (165, 165)], sortie=(0.5, 1), entree=(0.5, 0))
s.edge("a2", "s0", "p", E_DELEG, "délègue", [(270, 165), (415, 165)], sortie=(0.5, 1), entree=(0.5, 0))
s.edge("a3", "e", "r1", E_DEP, "", [(165, 285), (270, 285)], sortie=(0.5, 1), entree=(0.5, 0))
s.edge("a4", "p", "r1", E_DEP, "", [(415, 285), (270, 285)], sortie=(0.5, 1), entree=(0.5, 0))
s.edge("b1", "r1", "t1", E_OK, "non", sortie=(1, 0.5), entree=(0, 0.5))
s.edge("b2", "r1", "r2", E_DEP, "oui", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("b3", "r2", "c", E_DEP, "non", sortie=(1, 0.5), entree=(0, 0.5))
s.edge("b4", "c", "r2", E_DEP, "nouveau dépôt", [(650, 530), (330, 530)], sortie=(0.5, 1), entree=(0.77, 0.9))
s.edge("b5", "c", "t2", E_ESC, "aucun dépôt du type", sortie=(1, 0.5), entree=(0, 0.5))
s.edge("b6", "r2", "est", E_DEP, "oui", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("b7", "est", "r3", E_DEP, "", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("b8", "r3", "t3", E_OK, "oui", sortie=(1, 0.5), entree=(0, 0.5))
s.edge("b9", "r3", "r4", E_DEP, "non", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("b10", "r4", "pa", E_EXT, "oui", sortie=(1, 0.5), entree=(0, 0.5))
s.edge("b11", "pa", "t4a", E_ESC, "modéré", [(850, 815), (850, 773)], sortie=(1, 0.33), entree=(0, 0.5))
s.edge("b12", "pa", "t4b", E_ESC, "élevé", sortie=(1, 0.75), entree=(0, 0.5))
s.edge("b13", "pa", "deg", E_EXT, "indisponible", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("b14", "deg", "t4c", E_ESC, "> 1 500 €", sortie=(1, 0.5), entree=(0, 0.5))
# point de jonction sur l'axe : la demande poursuit vers la règle 5
s.box("j", "", 264, 974, 12, 12, "ellipse;fillColor=#333333;strokeColor=#333333;")
s.edge("b15", "deg", "j", E_EXT, "", [(650, 980)], sortie=(0.5, 1), entree=(1, 0.5))
s.edge("b16", "pa", "j", E_EXT, "", [(440, 846), (440, 980)], sortie=(0, 0.85), entree=(1, 0.5))
LIB = "text;html=1;fontFamily=Arial;fontSize=11;fontColor=#555555;align=center;verticalAlign=middle;whiteSpace=wrap;"
s.box("lb16", "faible : poursuit", 300, 900, 130, 20, LIB)
s.box("lb15", "≤ 1 500 € : continue, marquée mode dégradé", 470, 986, 350, 18, LIB)
s.edge("b17", "r4", "j", E_DEP, "non", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("b17b", "j", "r5", E_DEP, "", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("b18", "r5", "t5", E_ESC, "oui", sortie=(1, 0.5), entree=(0, 0.5))
s.edge("b19", "r5", "t6", E_OK, "non", sortie=(0.5, 1), entree=(0.5, 0))

s.legende([(VERT, "Règle de la Coordination"), (BLEU, "Contrôle délégué"), (OK, "Fin : décision"),
           (ESC, "Fin : escalade"), (GRIS, "Chantier 2"), (ORANGE, "Bornes provisoires")], 30, 1240)
s.ecrire("schema-2-orchestration", "Orchestration et terminaison", 1670, 1290)

# =============================================================================================================
# Schéma 3 : la mémoire partagée de la demande
# =============================================================================================================
s = Schema()
s.box("t", "Kaldera V2 · Mémoire partagée de la demande · Chantier 1", 30, 20, 1100, 30, S_TITRE)
s.box("st", "Un état par demande. Chaque agent écrit sa seule section métier, une seule fois ; la trace enregistre "
            "qui a écrit quoi (interface.md).", 30, 54, 1200, 22, S_SOUS)

s.box("agents", "Agents : chacun écrit sa section, lit seulement ce dont il a besoin", 30, 100, 400, 640, S_GROUPE)
AG = S_AGENT + "fontSize=11;"
s.box("ae", "<b>Éligibilité</b><br>lit : demande (contrat, sinistre)", 50, 210, 360, 56, AG)
s.box("ap", "<b>Pièces</b><br>lit : demande (pièces, espace assuré)", 50, 282, 360, 56, AG)
s.box("aes", "<b>Estimation</b><br>lit : demande, pieces (factures lisibles)", 50, 354, 360, 56, AG)
s.box("af", "<b>Anti-fraude</b><br>lit : demande, estimation (montant justifié)<br>"
            f'<font color="{ROUGE}">ne lit pas : pieces (contenu des pièces)</font>', 50, 426, 360, 64, AG)
s.box("ac", "<b>Coordination</b><br>lit : toutes les sections · écrit : issue, controle, trace", 50, 506, 360, 56,
      S_ORCH + "fontSize=11;")

s.box("etat", "État de la demande · reference (KAL-AA-NNNN)", 480, 100, 600, 640, S_CONTENEUR)
SEC_NEUTRE = BASE + GAUCHE + "rounded=0;fillColor=#ffffff;strokeColor=#999999;fontSize=11;"
SEC_AGENT = BASE + GAUCHE + f"rounded=0;fillColor=#cfe2f3;strokeColor={BLEU};fontSize=11;"
SEC_ORCH = BASE + GAUCHE + f"rounded=0;fillColor=#d9ead3;strokeColor={VERT};fontSize=11;"
sections = [
    ("demande", "<b>demande</b> : la demande reçue (§ 3)<br>écrite à la création, puis en lecture seule", SEC_NEUTRE, 138),
    ("eligibilite", "<b>eligibilite</b> · écrite par Éligibilité<br>éligible, conditions non remplies", SEC_AGENT, 210),
    ("pieces", "<b>pieces</b> · écrite par Pièces<br>complet ou manquantes, factures lisibles, compléments demandés", SEC_AGENT, 282),
    ("estimation", "<b>estimation</b> · écrite par Estimation<br>montant justifié, montant estimé", SEC_AGENT, 354),
    ("avis_fraude", "<b>avis_fraude</b> · écrite par Anti-fraude<br>non requis, avis (niveau, score, evaluation_id) ou indisponible",
     SEC_AGENT, 426),
    ("issue", "<b>issue</b> · écrite par la Coordination, conclut la demande<br>décision ou escalade, montant, motif, file, mode dégradé",
     SEC_ORCH, 506),
    ("controle", "<b>controle</b> (hors métier) : compteurs des bornes, arret", SEC_ORCH, 584),
    ("trace", "<b>trace</b> (hors métier), ajout seul : une étape par ligne<br>agent, sections écrites, action, durée, statut",
     SEC_ORCH, 648),
]
for sid, texte, style, y in sections:
    s.box(sid, texte, 500, y, 560, 56 if sid not in ("controle",) else 44, style)

for agent, section in [("ae", "eligibilite"), ("ap", "pieces"), ("aes", "estimation"), ("af", "avis_fraude"), ("ac", "issue")]:
    s.edge(f"w{agent}", agent, section, E_DEP, "écrit", sortie=(1, 0.5), entree=(0, 0.5))

s.box("garde", "<b>Comment un agent n'écrase pas le travail d'un autre</b><br>"
               "• Une table fixe propriétaire de chaque section ; écrire dans une autre section est refusé (erreur de droits).<br>"
               "• Chaque section métier est écrite une seule fois.<br>"
               "• Éligibilité et Pièces tournent en parallèle sans conflit : sections différentes.<br>"
               "• La trace note l'agent et les sections écrites à chaque étape : la règle se vérifie par un test.",
      1130, 100, 400, 190, S_AMBIG)
s.box("vit", "<b>Où vit-elle ?</b><br>En mémoire, un objet par demande, créé au début du traitement. "
             "Jamais partagé entre deux demandes : le traitement d'une demande n'en retarde pas une autre (§ 12). "
             "À la fin, la fiche de décision est construite depuis issue, avis_fraude, trace et arret.",
      1130, 310, 400, 140, S_NOTE)
s.box("part", "<b>Partenaire anti-fraude</b><br>reçoit seulement les 7 champs du contrat, construits par Anti-fraude (chantier 2)",
      1130, 470, 400, 70, S_EXT)
s.box("metr", "<b>Métriques par agent</b> (chantier 2)<br>calculées depuis la trace : appels, échecs, latence, appels externes",
      1130, 620, 400, 70, S_EXT)
s.edge("m1", "avis_fraude", "part", E_EXT, "filtre", sortie=(1, 0.5), entree=(0, 0.5))
s.edge("m2", "trace", "metr", E_EXT, "", sortie=(1, 0.5), entree=(0, 0.5))

s.legende([(VERT, "Coordination"), (BLEU, "Section d'un agent"), (ORANGE, "Règle d'écriture"),
           (ROUGE, "Lecture interdite"), (GRIS, "Externe ou chantier 2")], 30, 770)
s.ecrire("schema-3-memoire-partagee", "Mémoire partagée", 1560, 810)

# =============================================================================================================
# Schéma 0 : le choix du pattern, arbre de décision
# =============================================================================================================
arbre_de_decision(
    "schema-0-arbre-de-decision", "Arbre de décision du pattern",
    "Kaldera V2 · Choix du pattern agentique : arbre de décision · Chantier 1",
    "Une question métier, puis cinq questions d'architecture posées dans l'ordre ; chaque réponse élimine une option. "
    "Réponses fondées sur specs_metier.md et interface.md.",
    questions=[
        ("q0", "<b>Q0 · métier</b> : le recours à un système agentique est-il justifié, au regard d'un traitement humain ou de règles simples ?", S_QPROD),
        ("q1", "<b>Q1</b> : un seul agent avec 10 à 15 outils suffit-il ?", S_QTECH),
        ("q2", "<b>Q2</b> : les étapes sont-elles connues d'avance, et dans quel ordre ?", S_QTECH),
        ("q3", "<b>Q3</b> : des sous-tâches peuvent-elles s'exécuter en parallèle ?", S_QTECH),
        ("q4", "<b>Q4</b> : faut-il un contrôle central qui garantit une décision ou une escalade pour chaque demande ?", S_QTECH),
        ("q5", "<b>Q5</b> : quelles métriques par agent faut-il rendre visibles ?", S_QTECH),
    ],
    cotes=[
        ("r0", "<b>Écarté</b> : confier une règle à un LLM. Éligibilité, pièces, montant, indicateurs et décision sont chiffrés "
               "(§ 4 à § 10) : ils restent en code. L'avis de fraude vient du partenaire, un agent externe.", S_ECARTE, "écarte"),
        ("r1", "<b>Écarté</b> : l'agent unique. Ses rôles ne peuvent pas être prouvés séparément ; la trace exige un agent par section.",
         S_ECARTE, "écarte"),
        ("r2", "<b>Écarté</b> : un planificateur LLM qui invente les étapes. Le parcours est fixé par la spec (§ 2), "
               "testable et bornable.", S_ECARTE, "écarte"),
        ("r3", "<b>Retenu</b> : éligibilité et vérification des pièces en parallèle ; la demande de complément seulement "
               "si la demande est éligible.", S_RETENU, "retient"),
        ("r4", "<b>Écarté</b> : des agents qui se passent la main sans contrôle central ; personne ne garantirait l'issue "
               "de chaque demande, ni les 10 s.", S_ECARTE, "écarte"),
        ("r5", "<b>Ajouté</b> : une trace à chaque étape (agent, sections écrites), source des métriques par agent.",
         S_RETENU, "ajoute"),
    ],
    reponses=["en partie : les règles sont chiffrées, l'avis de fraude est externe", "non",
              "oui : éligibilité et pièces, estimation, anti-fraude, issue (§ 2)", "oui : éligibilité et pièces", "oui",
              "appels, échecs, latence, appels externes (interface.md)"],
    final="<b>Pattern retenu</b> : une Coordination centrale en code (pattern superviseur) qui applique les règles de décision, "
          "et quatre agents de contrôle, chacun maître d'une seule section · éligibilité et pièces en parallèle · "
          "un seul appel au partenaire par demande · une trace à chaque étape",
    tension="<b>Tension à arbitrer</b> : le code est prévisible mais rigide ; un système tout agentique est souple mais "
            "difficile à garantir. Ici chaque règle est chiffrée et les engagements sont absolus (issue garantie, 10 s) : "
            "un squelette en code, l'avis externe venant du partenaire.",
    legende=[(VIOLET, "Question métier"), (VERT, "Question d'architecture"), (GRIS, "Option écartée"),
             (BLEU, "Option retenue ou ajoutée"), (ORANGE, "Tension à arbitrer")],
)
