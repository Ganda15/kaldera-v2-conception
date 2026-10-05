# Schémas du chantier 1 de Kaldera V2 : arbre de décision, carte des agents, orchestration, mémoire partagée.
# Palette, styles et classe Schema : schema_commun.py.

from schema_commun import *  # noqa: F403 (palette, styles, Schema, arbre_de_decision)

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

# =============================================================================================================
# Schéma 0 : le choix du pattern, arbre de décision
# =============================================================================================================
arbre_de_decision(
    "schema-0-arbre-de-decision", "Arbre de décision du pattern",
    "Kaldera V2 · Choix du pattern agentique : arbre de décision · Chantier 1",
    "Une question métier, puis cinq questions d'architecture posées dans l'ordre ; chaque réponse élimine une option. "
    "Réponses provisoires, à confirmer avec specs_metier.md.",
    questions=[
        ("q0", "<b>Q0 · métier</b> : le recours à un système agentique est-il justifié, au regard d'un traitement humain ou de règles simples ?", S_QPROD),
        ("q1", "<b>Q1</b> : un seul agent avec 10 à 15 outils suffit-il ?", S_QTECH),
        ("q2", "<b>Q2</b> : les étapes sont-elles connues d'avance, et dans quel ordre ?", S_QTECH),
        ("q3", "<b>Q3</b> : des sous-tâches peuvent-elles s'exécuter en parallèle ?", S_QTECH),
        ("q4", "<b>Q4</b> : faut-il un contrôle central qui garantit une décision ou une escalade pour chaque demande ?", S_QTECH),
        ("q5", "<b>Q5</b> : quelles métriques par agent faut-il rendre visibles ?", S_QTECH),
    ],
    cotes=[
        ("r0", "<b>Écarté</b> : tout confier à un LLM. L'éligibilité et les plafonds sont des règles, elles restent en code.", S_ECARTE, "écarte"),
        ("r1", "<b>Écarté</b> : l'agent unique. Ses rôles ne peuvent pas être prouvés séparément (E2) ; c'est le défaut de l'agent actuel.", S_ECARTE, "écarte"),
        ("r2", "<b>Écarté</b> : un planificateur LLM qui invente les étapes. Le routage se fait par règles, testables et bornables.", S_ECARTE, "écarte"),
        ("r3", "<b>Retenu</b> : éligibilité et pièces en parallèle, puis regroupement de leurs résultats ; la suite s'enchaîne dans l'ordre.", S_RETENU, "retient"),
        ("r4", "<b>Écarté</b> : des agents qui se passent la main sans contrôle central ; personne ne garantirait la fin de chaque demande (E1).", S_ECARTE, "écarte"),
        ("r5", "<b>Ajouté</b> : un journal d'événements à chaque étape, source des métriques par agent (E6).", S_RETENU, "ajoute"),
    ],
    reponses=["oui, en partie : pour lire le texte libre des pièces", "non",
              "oui : éligibilité et pièces, puis estimation, fraude, décision", "oui : éligibilité et pièces", "oui",
              "latence, échecs, appels au partenaire"],
    final="<b>Pattern retenu</b> : un orchestrateur central écrit en code (pattern superviseur) et quatre agents spécialistes · "
          "éligibilité et pièces en parallèle · un LLM seulement pour lire le texte libre des pièces · "
          "un journal d'événements à chaque étape",
    tension="<b>Tension à arbitrer</b> : le code déterministe est prévisible mais peu flexible ; un système tout agentique "
            "est flexible mais difficile à garantir. Choix : un squelette en code, et le LLM seulement là où il faut lire "
            "du texte libre.",
    legende=[(VIOLET, "Question métier"), (VERT, "Question d'architecture"), (GRIS, "Option écartée"),
             (BLEU, "Option retenue ou ajoutée"), (ORANGE, "Tension à arbitrer")],
)
