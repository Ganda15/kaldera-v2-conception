# Schémas du chantier 2 de Kaldera V2 : arbre de décision de la liaison A2A, échange A2A et mode dégradé,
# plan d'épreuve. Palette, styles et classe Schema : schema_commun.py.

from schema_commun import *  # noqa: F403 (palette, styles, Schema, arbre_de_decision)

# =============================================================================================================
# Schéma 4 : le choix de la liaison avec le partenaire, arbre de décision
# =============================================================================================================
arbre_de_decision(
    "schema-4-arbre-liaison-a2a", "Arbre de décision de la liaison A2A",
    "Kaldera V2 · Choix de la liaison avec le partenaire : arbre de décision · Chantier 2",
    "Une question métier, puis cinq questions de conception posées dans l'ordre ; chaque réponse élimine une option. "
    "Réponses provisoires, à confirmer avec le contrat du partenaire et specs_metier.md.",
    questions=[
        ("q0", "<b>Q0 · métier</b> : le partenaire anti-fraude externe est-il indispensable, ou un contrôle interne suffirait-il ?", S_QPROD),
        ("q1", "<b>Q1</b> : le partenaire peut-il recevoir toutes les données de la demande ?", S_QTECH),
        ("q2", "<b>Q2</b> : faut-il bloquer l'appel jusqu'à la réponse du partenaire ?", S_QTECH),
        ("q3", "<b>Q3</b> : peut-on relancer librement un appel en échec ?", S_QTECH),
        ("q4", "<b>Q4</b> : une réponse bien formée est-elle forcément fiable ?", S_QTECH),
        ("q5", "<b>Q5</b> : que fait la demande quand aucun verdict valide n'arrive ?", S_QTECH),
    ],
    cotes=[
        ("r0", "<b>Écarté</b> : un contrôle de fraude entièrement interne. Le brief impose le partenaire ; à confirmer lors du cadrage.", S_ECARTE, "écarte"),
        ("r1", "<b>Retenu</b> : un filtre en liste blanche. Le message est construit champ par champ et validé contre le contrat avant l'envoi (E3).", S_RETENU, "retient"),
        ("r2", "<b>Écarté</b> : l'envoi avec attente. Si le délai expire, l'identifiant de la tâche n'est jamais reçu : impossible de l'annuler.", S_ECARTE, "écarte"),
        ("r3", "<b>Écarté</b> : les relances libres. Relances bornées par le contrat, seulement sur les erreurs rejouables, avec un délai croissant.", S_ECARTE, "écarte"),
        ("r4", "<b>Ajouté</b> : une validation à trois niveaux, protocole, schéma et sens ; toute réponse non conforme est rejetée (E4).", S_RETENU, "ajoute"),
        ("r5", "<b>Retenu</b> : une règle unique. Sans verdict valide, le mode dégradé défini par le métier s'applique (E5).", S_RETENU, "retient"),
    ],
    reponses=["oui (hypothèse du brief)", "non : seulement les champs du contrat",
              "non : envoi sans attente, puis lecture de l'état jusqu'au délai", "non : pas de relance sauvage",
              "non : le partenaire peut mentir", "mode dégradé selon specs_metier.md"],
    final="<b>Liaison retenue</b> : un seul point de sortie (l'agent Fraude) · filtre en liste blanche · envoi sans attente, "
          "délai par appel et annulation · relances bornées par le contrat · validation à trois niveaux · un mode dégradé unique",
    tension="<b>Tension à arbitrer</b> : une validation stricte rejette plus de réponses et sollicite davantage le mode dégradé ; "
            "une validation souple laisse passer des réponses douteuses. Choix : rigueur sur la validation, continuité "
            "assurée par le mode dégradé.",
    legende=[(VIOLET, "Question métier"), (VERT, "Question de conception"), (GRIS, "Option écartée"),
             (BLEU, "Option retenue ou ajoutée"), (ORANGE, "Tension à arbitrer")],
)

# =============================================================================================================
# Schéma 5 : l'échange A2A, le filtre, la validation et le chemin de mode dégradé
# =============================================================================================================
s = Schema()
s.box("t", "Kaldera V2 · Échange A2A, filtre, validation et mode dégradé · Chantier 2", 30, 20, 1300, 30, S_TITRE)
s.box("st", "Un seul point de sortie vers le partenaire : rien ne sort hors contrat, rien n'entre sans validation. "
            "Proposition provisoire, à confirmer avec le contrat du partenaire et specs_metier.md.", 30, 54, 1450, 22, S_SOUS)

s.box("kaldera", "Système Kaldera", 30, 95, 1070, 880, S_CONTENEUR)
s.box("externe", "Partenaire anti-fraude (externe)", 1120, 95, 390, 880,
      S_CONTENEUR + f"fillColor=#f7f7f7;strokeColor={GRIS};dashed=1;fontColor=#555555;")

s.box("mem", "<b>Mémoire partagée</b><br>section fraude : suspicion, taskId, contextId, verdict validé", 60, 130, 260, 80, S_ORCH)
s.box("fraude", "<b>Agent Fraude</b><br>suspicion déclarée : il faut interroger le partenaire", 380, 130, 280, 80, S_AGENT)
s.box("filtre", "<b>Filtre sortant (E3)</b><br>message neuf, construit champ par champ depuis la liste blanche du contrat ; "
                "validé contre le schéma, aucun champ en plus ; en cas d'échec, rien ne part", 380, 245, 280, 125, S_ORCH)
s.box("envoi", "<b>Envoi sans attendre la fin de la tâche</b><br>taskId et contextId enregistrés aussitôt dans la mémoire",
      720, 260, 290, 90, S_ORCH)
s.box("lecture", "<b>Lecture de l'état de la tâche</b><br>jusqu'au délai maximum, au rythme permis par le contrat",
      720, 395, 290, 70, S_ORCH)
s.box("d1", "Tâche terminée<br>avant le délai ?", 780, 505, 200, 100, S_LOSANGE)
s.box("valid", "<b>Validation de la réponse (E4)</b><br>"
               "• protocole : JSON-RPC valide, même id, réponse de type Task ou Message<br>"
               "• schéma : partie données conforme au contrat, aucun champ en plus<br>"
               "• sens : même claim_ref, score dans ses bornes, verdict cohérent<br>"
               "Toute réponse non conforme est rejetée, jamais propagée.", 340, 625, 380, 140, S_ORCH)
s.box("d2", "Réponse<br>conforme ?", 430, 790, 200, 90, S_LOSANGE)
s.box("ok", "<b>Verdict écrit dans la mémoire</b><br>la demande continue vers la table de décision (chantier 1)",
      60, 805, 260, 70, S_FIN_OK)
s.box("deg", "<b>Mode dégradé (E5)</b>, défini par specs_metier.md<br>la demande continue (table de décision) "
             "ou elle est routée (escalade humaine motivée)", 800, 785, 280, 100, S_AMBIG)
s.box("tardive", "Réponse arrivée après le passage en mode dégradé : journalisée, sans changer la décision prise.",
      800, 900, 280, 55, S_NOTE)
s.box("journal", "<b>Journal d'événements</b><br>message envoyé après filtre, réponse reçue, résultat de la validation, "
                 "durée ; aucune donnée hors contrat", 60, 470, 260, 130, S_CYL)

s.box("contrat", "<b>Contrat d'échange</b> (fourni par le partenaire)<br>champs autorisés · format · délai par appel · "
                 "rythme de lecture de l'état · règles de relance · version<br><i>Il fixe le filtre, les relances et la validation.</i>",
      1140, 130, 350, 105, S_NOTE)
s.box("partenaire", "<b>Partenaire anti-fraude</b><br>Agent Card · tâche A2A · verdict", 1140, 260, 350, 90, S_EXT)

s.edge("x1", "mem", "fraude", E_DEP, "lit", sortie=(1, 0.43), entree=(0, 0.43))
s.edge("x2", "fraude", "filtre", E_DEP, "", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("x3", "filtre", "envoi", E_DEP, "message filtré", sortie=(1, 0.44), entree=(0, 0.44))
s.edge("x4", "envoi", "partenaire", E_DEP, "champs du contrat", sortie=(1, 0.44), entree=(0, 0.44))
s.edge("x5", "envoi", "lecture", E_DEP, "", sortie=(0.552, 1), entree=(0.552, 0))
s.edge("x6", "partenaire", "lecture", E_EXT, "état de la tâche", [(1210, 430)], sortie=(0.2, 1), entree=(1, 0.5))
s.edge("x7", "lecture", "d1", E_DEP, "", sortie=(0.552, 1), entree=(0.5, 0))
s.edge("x8", "d1", "valid", E_DEP, "oui", [(530, 555)], sortie=(0, 0.5), entree=(0.5, 0))
s.edge("x9", "d1", "deg", E_ESC, "non : délai dépassé · annulation de la tâche", sortie=(0.5, 1), entree=(0.286, 0))
s.edge("x10", "valid", "d2", E_DEP, "", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("x11", "d2", "ok", E_OK, "oui", sortie=(0, 0.5), entree=(1, 0.43))
s.edge("x12", "d2", "deg", E_ESC, "non : rejet journalisé", sortie=(1, 0.5), entree=(0, 0.5))
s.edge("x13", "partenaire", "deg", E_ESC, "erreur réseau, panne, accès refusé : relances bornées par le contrat, puis",
       [(1315, 835)], sortie=(0.5, 1), entree=(1, 0.5))
s.edge("x14", "valid", "journal", E_EXT, "trace", [(190, 695)], sortie=(0, 0.5), entree=(0.5, 1))

s.legende([(VERT, "Contrôle écrit en code"), (BLEU, "Agent"), (GRIS, "Partenaire externe"),
           (OK, "Verdict accepté"), (ESC, "Chemin de repli"), (ORANGE, "Selon specs_metier.md")], 30, 1000)
s.ecrire("schema-5-echange-a2a", "Échange A2A et mode dégradé", 1540, 1040)

# =============================================================================================================
# Schéma 6 : le plan d'épreuve, scénarios × signaux × ajustements
# =============================================================================================================
s = Schema()
s.box("t", "Kaldera V2 · Plan d'épreuve : scénarios × signaux × ajustements · Chantier 2", 30, 20, 1300, 30, S_TITRE)
s.box("st", "Chaque scénario est rejoué, ses signaux comparés au critère attendu ; tout écart provoque un ajustement du "
            "chantier 1, consigné, puis un nouveau rejeu. Valeurs et seuils provisoires.", 30, 54, 1350, 22, S_SOUS)

etapes = [
    ("c1", "<b>1. Rejouer</b> un scénario<br>eval/scenarios.jsonl, partenaire simulé par un bouchon réglable", S_ORCH),
    ("c2", "<b>2. Observer</b> les signaux<br>statut final, étapes, latence, rejets, mode dégradé", S_ORCH),
    ("c3", "<b>3. Comparer</b> au critère de réussite<br>écart ou conformité", S_ORCH),
    ("c4", "<b>4. Ajuster</b> le chantier 1<br>borne, frontière ou routage", S_AMBIG),
    ("c5", "<b>5. Consigner</b> au journal<br>scénario, signal, valeur avant et après", S_CYL),
]
for i, (cid, texte, style) in enumerate(etapes):
    s.box(cid, texte, 60 + i * 280, 105, 240, 85, style + ("" if style == S_CYL else MILIEU))
    if i:
        s.edge(f"f{i}", etapes[i - 1][0], cid, E_DEP, "", sortie=(1, 0.5), entree=(0, 0.5))
s.edge("boucle", "c5", "c1", E_DEP, "nouveau rejeu, jusqu'à ce que le critère soit tenu", [(1240, 225), (180, 225)],
       sortie=(0.5, 1), entree=(0.5, 1))

colonnes = [("Scénario", 220), ("Exigence", 90), ("Signal observé", 330), ("Critère de réussite", 330),
            ("Ajustement possible du chantier 1", 330)]
lignes = [
    ("Cas nominal", "E1", "statut final, nombre d'étapes, latence", "une décision, dans les bornes", "aucun : sert de référence"),
    ("Agent sollicité hors de son rôle", "E2", "réponse de l'agent, sections écrites", "refus, aucune écriture hors de sa section", "frontière : schéma de sortie, droits de lecture"),
    ("Données en trop dans la demande", "E3", "champs du message envoyé", "seuls les champs du contrat sont partis", "liste blanche du filtre"),
    ("Réponse invalide", "E4", "rejet au niveau protocole ou schéma", "rejet, rien n'entre dans la mémoire", "règles de validation"),
    ("Partenaire menteur", "E4", "rejet au niveau du sens", "rejet journalisé, puis mode dégradé", "contrôles de cohérence"),
    ("Partenaire en panne", "E5", "relances, passage en mode dégradé", "relances dans la limite du contrat, mode dégradé appliqué", "nombre de relances, disjoncteur"),
    ("Partenaire lent", "E5, E6", "latence de l'agent Fraude, annulation", "annulation au délai, aucune demande bloquée", "délai par appel, délai global"),
    ("Piège à boucle", "E6", "compteur d'étapes, état répété", "arrêt dans les bornes, escalade motivée", "valeurs des bornes, routage"),
]
S_CELLULE = BASE + GAUCHE + MILIEU + "rounded=0;fillColor=#ffffff;strokeColor=#bbbbbb;fontSize=11;"
S_ENTETE = BASE + GAUCHE + MILIEU + f"rounded=0;fillColor=#d9ead3;strokeColor={VERT};fontStyle=1;fontSize=11;"
x0, y0, h = 60, 260, 44
for j, (texte, largeur) in enumerate(colonnes):
    x = x0 + sum(c[1] for c in colonnes[:j])
    s.box(f"h{j}", texte, x, y0, largeur, h, S_ENTETE)
    for i, ligne in enumerate(lignes):
        s.box(f"l{i}c{j}", ligne[j], x, y0 + (i + 1) * h, largeur, h, S_CELLULE)

y_note = y0 + (len(lignes) + 1) * h + 20
s.box("note", "Les LLM ne répondent pas toujours de la même façon : chaque scénario est rejoué plusieurs fois avant de "
              "conclure. Les bornes et frontières finales sont celles que le rejeu a justifiées, jamais un réglage au jugé.",
      60, y_note, 1300, 50, S_NOTE + MILIEU)
s.legende([(VERT, "Étape de contrôle"), (ORANGE, "Ajustement du chantier 1"), (GRIS, "Valeurs provisoires")], 30, y_note + 80)
s.ecrire("schema-6-plan-epreuve", "Plan d'épreuve", 1420, y_note + 120)
