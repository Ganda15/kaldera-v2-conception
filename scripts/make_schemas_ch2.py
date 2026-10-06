# Schémas du chantier 2 de Kaldera V2 : arbre de décision de la liaison A2A, échange A2A et mode dégradé,
# plan d'épreuve. Fondés sur external_agent/contrat.md (v2.0), docs/specs_metier.md (v3.2) et eval/scenarios.jsonl.
# Palette, styles et classe Schema : schema_commun.py.

from schema_commun import *  # noqa: F403 (palette, styles, Schema, arbre_de_decision)

CENTRE = "align=center;verticalAlign=middle;spacingTop=0;spacingLeft=6;spacingRight=6;"
FIN_OK = S_FIN_OK + CENTRE + "fontSize=11;"
FIN_ESC = S_FIN_ESC + CENTRE + "fontSize=11;"

# =============================================================================================================
# Schéma 4 : le choix de la liaison avec le partenaire, arbre de décision
# =============================================================================================================
arbre_de_decision(
    "schema-4-arbre-liaison-a2a", "Arbre de décision de la liaison A2A",
    "Kaldera V2 · Choix de la liaison avec le partenaire : arbre de décision · Chantier 2",
    "Une question métier, puis cinq questions de conception posées dans l'ordre ; chaque réponse élimine une option. "
    "Réponses fondées sur contrat.md (v2.0) et specs_metier.md.",
    questions=[
        ("q0", "<b>Q0 · métier</b> : un avis de fraude interne pourrait-il remplacer le partenaire ?", S_QPROD),
        ("q1", "<b>Q1</b> : le partenaire peut-il recevoir toutes les données de la demande ?", S_QTECH),
        ("q2", "<b>Q2</b> : comment appeler le partenaire ?", S_QTECH),
        ("q3", "<b>Q3</b> : peut-on relancer un appel en échec ?", S_QTECH),
        ("q4", "<b>Q4</b> : une réponse bien formée est-elle forcément exploitable ?", S_QTECH),
        ("q5", "<b>Q5</b> : que devient la demande sans avis exploitable ?", S_QTECH),
    ],
    cotes=[
        ("r0", "<b>Écarté</b> : un avis interne. « L'avis de fraude est émis par le partenaire, jamais en interne » (§ 2) ; "
               "Kaldera décide seulement s'il faut le demander (F1 à F4).", S_ECARTE, "écarte"),
        ("r1", "<b>Retenu</b> : un message neuf, construit depuis une liste blanche de sept champs, validé contre un "
               "schéma strict avant l'envoi [E3].", S_RETENU, "retient"),
        ("r2", "<b>Écarté</b> : l'envoi sans attente suivi de lectures d'état et d'une annulation ; le contrat n'en "
               "prévoit pas. Un seul message/send, abandonné à 3 s.", S_ECARTE, "écarte"),
        ("r3", "<b>Écarté</b> : toute relance (contrat § 6). Le marqueur d'appel du chantier 1 empêche aussi un "
               "second appel après une reprise.", S_ECARTE, "écarte"),
        ("r4", "<b>Ajouté</b> : une validation à cinq niveaux (transport, enveloppe, forme A2A, schéma, cohérence) ; "
               "toute réponse non conforme est écartée, jamais recopiée [E4].", S_RETENU, "ajoute"),
        ("r5", "<b>Retenu</b> : la règle du § 9 pour toutes les causes : 1 500 € ou moins, la demande continue en mode "
               "dégradé ; au-delà, escalade cellule_fraude [E5].", S_RETENU, "retient"),
    ],
    reponses=["non : le partenaire est imposé (§ 2)", "non : sept champs exactement (contrat § 2)",
              "un seul message/send, qui rend une tâche terminée", "non, jamais (contrat § 6)",
              "non : il peut répondre hors contrat", "la règle du mode dégradé (§ 9)"],
    final="<b>Liaison retenue</b> : un seul point de sortie (l'agent Anti-fraude) · filtre en liste blanche, sept champs · "
          "un appel unique abandonné à 3 s · aucune relance · validation à cinq niveaux · une règle de mode dégradé unique",
    tension="<b>Tension à arbitrer</b> : une validation stricte écarte plus de réponses et sollicite davantage le mode "
            "dégradé ; une validation souple laisse passer des réponses douteuses. Le contrat tranche : une réponse non "
            "conforme est écartée, jamais exploitée ; la continuité vient du mode dégradé.",
    legende=[(VIOLET, "Question métier"), (VERT, "Question de conception"), (GRIS, "Option écartée"),
             (BLEU, "Option retenue ou ajoutée"), (ORANGE, "Tension à arbitrer")],
)

# =============================================================================================================
# Schéma 5 : l'échange A2A, le filtre, la validation et le chemin de mode dégradé
# =============================================================================================================
s = Schema()
s.box("t", "Kaldera V2 · Échange A2A, filtre, validation et mode dégradé · Chantier 2", 30, 20, 1300, 30, S_TITRE)
s.box("st", "Un seul point de sortie vers le partenaire : rien ne sort hors des sept champs du contrat, rien n'entre sans "
            "validation. Fondé sur contrat.md (v2.0) et specs_metier.md (§ 7, § 9, § 10).", 30, 54, 1450, 22, S_SOUS)

s.box("kaldera", "Système Kaldera", 30, 95, 1070, 960, S_CONTENEUR)
s.box("externe", "Partenaire anti-fraude (externe)", 1120, 95, 390, 960,
      S_CONTENEUR + f"fillColor=#f7f7f7;strokeColor={GRIS};dashed=1;fontColor=#555555;")

s.box("demande", "<b>Demande</b> (§ 3)<br>assuré, contrat, sinistre, pièces, historique ; le filtre n'en lit que "
                 "les champs utiles<br><br>"
                 f'<font color="{ROUGE}"><b>Ne part jamais</b> : nom, prénom, e-mail, téléphone, adresse, code postal '
                 "complet, IBAN, identifiant client, numéro de contrat, description, pièces</font>",
      60, 130, 260, 165, S_NOTE)
s.box("af", "<b>Agent Anti-fraude</b> · écrit : avis_fraude<br>calcule F1 à F4 ; aucun indicateur : avis non requis, "
            "aucun appel", 380, 130, 280, 85, S_AGENT)
s.box("coord", "<b>Coordination</b><br>écrit le marqueur d'appel dans controle, puis délègue l'appel", 720, 130, 290, 85,
      S_ORCH)
s.box("filtre", "<b>Filtre sortant [E3]</b><br>message neuf : exactement les sept champs du contrat, dont deux calculés "
                "(ancienneté, département) ; validé contre un schéma strict ; en cas d'échec, rien ne part",
      380, 255, 280, 135, S_ORCH)
s.box("appel", "<b>Appel unique</b> · POST /a2a, message/send<br>Bearer PARTENAIRE_JETON<br>"
               "délai : 3 s au plus, et jamais au-delà des 10 s de la demande · aucune relance",
      720, 270, 290, 110, S_ORCH)
s.box("journal", "<b>Trace</b><br>agent, durée, statut, raison d'un échec, evaluation_id ; jamais le message, "
                 "le jeton ni une réponse écartée", 60, 345, 260, 130, S_CYL)
s.box("valid", "<b>Validation de la réponse [E4]</b>, cinq niveaux dans l'ordre<br>"
               "1. transport : HTTP 200, JSON lisible (INV-06)<br>"
               "2. enveloppe JSON-RPC : 2.0, même id, result (INV-07)<br>"
               "3. forme A2A : tâche completed, partie data<br>"
               "4. schéma : six champs exactement, valeurs permises (INV-03, INV-05)<br>"
               "5. cohérence : même dossier, score entre 0 et 1, niveau cohérent avec le score (INV-04, INV-01, INV-02)",
      720, 430, 290, 200, S_ORCH)
s.box("d1", "Avis conforme<br>et reçu à temps ?", 765, 665, 200, 100, S_LOSANGE)
s.box("ok", "<b>avis_fraude écrit</b><br>niveau, score, indicateurs, evaluation_id (audit), version_modele", 380, 680, 280, 70,
      FIN_OK)
s.box("regle4", "<b>Coordination, règle 4</b><br>faible : poursuit · modéré : gestionnaire · élevé : cellule_fraude",
      60, 680, 260, 70, S_ORCH + MILIEU)
s.box("indispo", "<b>Avis indisponible</b><br>délai dépassé, erreur (503, 401, -32xxx) ou réponse écartée ; "
                 "seule la raison est gardée, jamais le contenu reçu", 720, 800, 290, 95, S_AMBIG)
s.box("dd", "Montant estimé<br>≤ 1 500 € ?", 410, 805, 200, 90, S_LOSANGE)
s.box("esc", "<b>ESCALADE cellule_fraude</b><br>contrôle anti-fraude manuel · mode dégradé", 60, 815, 260, 70, FIN_ESC)
s.box("cont", "<b>La demande continue</b> sans avis<br>règles 5 et 6 · décision marquée mode dégradé", 380, 935, 260, 75,
      FIN_OK)
s.box("note", "Jamais de relance (contrat § 6). Une réponse tardive n'est pas lue : l'appel est abandonné. Le dossier "
              "n'est jamais rappelé (doublon : -32029, manquement). Les erreurs 401 et -32xxx déclenchent une alerte.",
      720, 925, 290, 110, S_NOTE)

s.box("partenaire", "<b>Partenaire anti-fraude</b><br>agent A2A · Agent Card en /.well-known/agent.json", 1140, 275, 350, 90,
      S_EXT)
s.box("contrat", "<b>Contrat v2.0</b><br>• requête : une partie data, sept champs exactement<br>"
                 "• réponse : tâche completed, six champs<br>• niveau : faible &lt; 0,40 ≤ modéré &lt; 0,75 ≤ élevé<br>"
                 "• réponse garantie en 2 s ; abandon à 3 s<br>• un appel par dossier, aucune relance<br>"
                 "• erreurs : 401, 503, -32700, -32600, -32601, -32602, -32029",
      1140, 560, 350, 175, S_NOTE)

s.edge("x1", "demande", "filtre", E_DEP, "lit", [(350, 212), (350, 323)], sortie=(1, 0.5), entree=(0, 0.5))
s.edge("x2", "coord", "af", E_DELEG, "délègue", sortie=(0, 0.5), entree=(1, 0.5))
s.edge("x3", "af", "filtre", E_DEP, "indicateur présent", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("x4", "filtre", "appel", E_DEP, "7 champs", sortie=(1, 0.52), entree=(0, 0.5))
s.edge("x5", "appel", "partenaire", E_DEP, "message/send", sortie=(1, 0.5), entree=(0, 0.5))
s.edge("x6", "partenaire", "valid", E_EXT, "réponse ou erreur", [(1245, 480)], sortie=(0.3, 1), entree=(1, 0.25))
s.edge("x7", "appel", "valid", E_DEP, "fin de l'attente", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("x8", "valid", "d1", E_DEP, "", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("x9", "d1", "ok", E_OK, "oui", sortie=(0, 0.5), entree=(1, 0.5))
s.edge("x10", "ok", "regle4", E_DEP, "", sortie=(0, 0.5), entree=(1, 0.5))
s.edge("x11", "d1", "indispo", E_ESC, "non", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("x12", "indispo", "dd", E_ESC, "§ 9", sortie=(0, 0.5), entree=(1, 0.5))
s.edge("x13", "dd", "esc", E_ESC, "non", sortie=(0, 0.5), entree=(1, 0.5))
s.edge("x14", "dd", "cont", E_OK, "oui", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("x15", "valid", "journal", E_EXT, "trace", [(350, 530), (350, 410)], sortie=(0, 0.5), entree=(1, 0.5))

s.legende([(VERT, "Contrôle écrit en code"), (BLEU, "Agent"), (GRIS, "Partenaire externe"),
           (OK, "Suite normale"), (ESC, "Chemin de repli"), (ORANGE, "Avis indisponible"), (ROUGE, "Données interdites")],
          30, 1080)
s.ecrire("schema-5-echange-a2a", "Échange A2A et mode dégradé", 1540, 1120)

# =============================================================================================================
# Schéma 6 : le plan d'épreuve, scénarios × signaux × ajustements
# =============================================================================================================
s = Schema()
s.box("t", "Kaldera V2 · Plan d'épreuve : scénarios × signaux × ajustements · Chantier 2", 30, 20, 1300, 30, S_TITRE)
s.box("st", "Chaque famille de eval/scenarios.jsonl est rejouée par traiter_lot ; ses signaux sont comparés au champ "
            "attendu et aux critères ; tout écart provoque un ajustement du chantier 1, consigné, puis un nouveau rejeu.",
      30, 54, 1350, 22, S_SOUS)

etapes = [
    ("c1", "<b>1. Rejouer</b> un scénario<br>traiter_lot, partenaire simulé : normal, lent, invalide ou panne", S_ORCH),
    ("c2", "<b>2. Observer</b> les signaux<br>issue, trace, appels externes, échecs, durées", S_ORCH),
    ("c3", "<b>3. Comparer</b> au champ attendu<br>et aux critères du tableau", S_ORCH),
    ("c4", "<b>4. Ajuster</b> le chantier 1<br>une borne, une frontière ou un routage, un seul à la fois", S_AMBIG),
    ("c5", "<b>5. Consigner</b> au journal<br>scénario, signal, avant, après, rejeu, commit", S_CYL),
]
for i, (cid, texte, style) in enumerate(etapes):
    s.box(cid, texte, 60 + i * 280, 105, 240, 85, style + ("" if style == S_CYL else MILIEU))
    if i:
        s.edge(f"f{i}", etapes[i - 1][0], cid, E_DEP, "", sortie=(1, 0.5), entree=(0, 0.5))
s.edge("boucle", "c5", "c1", E_DEP, "rejeu des 28 scénarios, jusqu'à ce que tous les critères soient tenus",
       [(1240, 225), (180, 225)], sortie=(0.5, 1), entree=(0.5, 1))

colonnes = [("Scénarios", 230), ("Exigences", 90), ("Signaux observés", 290), ("Critère de réussite", 420),
            ("Ajustement possible du chantier 1", 270)]
lignes = [
    ("NOM-01 à 11 · nominaux", "E1, E2", "issue, trace (agent, ecrit), appels externes",
     "11 fiches conformes ; chaque section écrite par son seul propriétaire ; 0 appel au partenaire",
     "frontière (droits), etapes_max"),
    ("AF-01 à 07 · anti-fraude", "E1, E3", "appels, échecs, message envoyé, avis",
     "7 appels, 0 échec ; sept champs exactement ; niveau d'avis et issue conformes", "routage des règles 4 et 5"),
    ("INV-01 à 07 · réponses invalides", "E4, E5", "échecs et niveau de validation, avis, mode dégradé",
     "7 réponses écartées au bon niveau ; aucun avis recopié ; 1 500 € ou moins continue, au-delà cellule_fraude",
     "règles de validation"),
    ("PAN-01 · panne, lot de 5", "E5, E6", "appels, échecs, issues du lot",
     "2 appels, 2 échecs, 0 relance ; 0401 et 0405 non touchés ; 5 fiches conformes", "routage du mode dégradé"),
    ("PAN-02 · lent (5 s), lot de 3", "E5, E6", "durée des appels, des demandes, du lot",
     "abandon à 3 s ; chaque demande sous 10 s ; le lot dure environ 3 s, pas 6 s",
     "duree_max_s, lot en concurrence"),
    ("BCL-01 · piège à boucle", "E1, E6", "longueur de la trace, arret",
     "escalade avec arret ; trace de 8 étapes au plus", "etapes_max, même état, file"),
]
S_CELLULE = BASE + GAUCHE + MILIEU + "rounded=0;fillColor=#ffffff;strokeColor=#bbbbbb;fontSize=11;"
S_ENTETE = BASE + GAUCHE + MILIEU + f"rounded=0;fillColor=#d9ead3;strokeColor={VERT};fontStyle=1;fontSize=11;"
x0, y0, h = 60, 260, 50
for j, (texte, largeur) in enumerate(colonnes):
    x = x0 + sum(c[1] for c in colonnes[:j])
    s.box(f"h{j}", texte, x, y0, largeur, 40, S_ENTETE)
    for i, ligne in enumerate(lignes):
        s.box(f"l{i}c{j}", ligne[j], x, y0 + 40 + i * h, largeur, h, S_CELLULE)

y_note = y0 + 40 + len(lignes) * h + 20
s.box("note", "Aucun LLM dans le chemin de décision et un partenaire simulé déterministe : un rejeu suffit pour juger une "
              "issue ; les scénarios de panne sont rejoués cinq fois pour mesurer les durées. Hors scénarios, des tests "
              "unitaires couvrent le filtre (données sensibles, Corse, outre-mer), les erreurs 401, 503, -32602, -32029 "
              "et la reprise avec marqueur d'appel. Sur les 28 scénarios : 18 appels au partenaire, jamais deux pour un "
              "même dossier.", 60, y_note, 1300, 66, S_NOTE + MILIEU)
s.legende([(VERT, "Étape de contrôle"), (ORANGE, "Ajustement du chantier 1"), (GRIS, "Journal des ajustements")],
          30, y_note + 96)
s.ecrire("schema-6-plan-epreuve", "Plan d'épreuve", 1420, y_note + 136)
