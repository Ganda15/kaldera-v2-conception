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
               "prévoit pas. Un seul message/send, au plus 3 s, limité par le budget restant de la demande.", S_ECARTE,
         "écarte"),
        ("r3", "<b>Écarté</b> : toute relance (contrat § 6). Le registre des appels bloque un second appel dans une même "
               "exécution (demande ou lot) ; après un redémarrage, non couvert : limite écrite.", S_ECARTE, "écarte"),
        ("r4", "<b>Ajouté</b> : une validation à cinq niveaux (transport, enveloppe, forme A2A, schéma, cohérence) ; "
               "toute réponse non conforme est écartée, jamais recopiée [E4].", S_RETENU, "ajoute"),
        ("r5", "<b>Retenu</b> : la règle du § 9 pour toutes les causes : 1 500 € ou moins, la demande continue en mode "
               "dégradé ; au-delà, escalade cellule_fraude [E5].", S_RETENU, "retient"),
    ],
    reponses=["non : le partenaire est imposé (§ 2)", "non : sept champs exactement (contrat § 2)",
              "un seul message/send, qui rend une tâche terminée", "non, jamais (contrat § 6)",
              "non : il peut répondre hors contrat", "la règle du mode dégradé (§ 9)"],
    final="<b>Liaison retenue</b> : un seul point de sortie (l'agent Anti-fraude) · filtre en liste blanche, sept champs · "
          "un appel unique, au plus 3 s, limité par le budget restant · aucune relance · validation à cinq niveaux · "
          "une règle de mode dégradé unique",
    tension="<b>Tension à arbitrer</b> : une validation stricte écarte plus de réponses et sollicite davantage le mode "
            "dégradé ; une validation souple laisse passer des réponses douteuses. Le contrat tranche : une réponse non "
            "conforme est écartée, jamais exploitée ; la continuité vient du mode dégradé.",
    legende=[(VIOLET, "Question métier"), (VERT, "Question de conception"), (GRIS, "Option écartée"),
             (BLEU, "Option retenue ou ajoutée"), (ORANGE, "Tension à arbitrer")],
)

# =============================================================================================================
# Schéma 5 : l'échange A2A, le filtre, la validation et le chemin de mode dégradé (aligné sur le code le 08/10/2026)
# =============================================================================================================
s = Schema()
s.box("t", "Kaldera V2 · Échange A2A, filtre, validation et mode dégradé · Chantier 2", 30, 20, 1300, 30, S_TITRE)
s.box("st", "Un seul point de sortie vers le partenaire : rien ne sort hors des sept champs du contrat, rien n'entre sans "
            "validation, rien ne dépasse l'échéance de la demande. Aligné sur le code du 08/10/2026 (a2a/filtre.py, "
            "a2a/client.py, a2a/validation.py, coordination.py).", 30, 54, 1480, 22, S_SOUS)

s.box("kaldera", "Système Kaldera", 30, 95, 1070, 975, S_CONTENEUR)
s.box("externe", "Partenaire anti-fraude (externe)", 1120, 95, 390, 975,
      S_CONTENEUR + f"fillColor=#f7f7f7;strokeColor={GRIS};dashed=1;fontColor=#555555;")

s.box("demande", "<b>Demande</b> (§ 3)<br>assuré, contrat, sinistre, pièces, historique ; lue seulement par "
                 "la Coordination<br><br>"
                 f'<font color="{ROUGE}"><b>Ne part jamais</b> : nom, prénom, e-mail, téléphone, adresse, code postal '
                 "complet, IBAN, identifiant client, numéro de contrat, description, pièces</font>",
      60, 130, 260, 165, S_NOTE)
s.box("af", "<b>Agent Anti-fraude</b> · section avis_fraude<br>reçoit 8 données ; calcule F1 à F4.<br>"
            "<b>Aucun indicateur</b> : avis non requis, aucun appel, jamais marqué mode dégradé", 380, 130, 280, 95, S_AGENT)
s.box("coord", "<b>Coordination</b><br>seule à lire et écrire l'état ; donne à l'agent un accès au partenaire limité au "
               "temps restant ; registre des appels : une référence, un appel par exécution", 720, 130, 290, 110, S_ORCH)
s.box("d0", "Délai du partenaire<br>≥ 0,15 s ?", 420, 255, 200, 95, S_LOSANGE)
s.box("filtre", "<b>Filtre sortant [E3]</b><br>message neuf : les sept champs du contrat, dont deux calculés "
                "(ancienneté, département) ; schéma strict", 380, 375, 280, 110, S_ORCH)
s.box("appel", "<b>Appel unique</b> · POST /a2a, message/send<br>Bearer PARTENAIRE_JETON<br>"
               "délai = min(3 s, échéance − maintenant) · aucune relance · réponse arrivée après l'échéance : jamais lue",
      720, 280, 290, 115, S_ORCH)
s.box("valid", "<b>Validation de la réponse [E4]</b>, cinq niveaux dans l'ordre<br>"
               "1. transport : HTTP 200 (503, 401 : écartée)<br>"
               "2. JSON et enveloppe JSON-RPC : 2.0, même id, result ; un HTTP 200 qui porte error reste une erreur "
               "(INV-06, INV-07, doublon -32029)<br>"
               "3. forme A2A : tâche completed, un artefact, une partie data<br>"
               "4. schéma : six champs exactement, score de 0 à 1, valeurs permises (INV-01, INV-03, INV-05)<br>"
               "5. cohérence : même dossier, niveau cohérent avec le score (INV-02, INV-04)",
      720, 430, 290, 205, S_ORCH)
s.box("d1", "Avis conforme reçu<br>avant l'échéance<br>autorisée ?", 755, 665, 220, 110, S_LOSANGE)
s.box("ok", "<b>Avis retenu</b>, rangé par la Coordination<br>fiche : niveau et score (§ 11) ; evaluation_id gardé "
            "dans la section avis_fraude", 720, 805, 290, 75, FIN_OK)
s.box("regle4", "<b>Règle 4</b> : faible poursuit · modéré gestionnaire · élevé cellule_fraude", 720, 905, 290, 70,
      S_ORCH + MILIEU)
s.box("indispo", "<b>Avis indisponible</b><br>budget épuisé, requête refusée, doublon, délai dépassé, erreur (503, 401, "
                 "-32xxx) ou réponse écartée ; la raison (code court) va dans la trace, jamais le contenu reçu",
      380, 700, 280, 110, S_AMBIG)
s.box("dd", "Montant estimé<br>≤ 1 500 € ?", 420, 840, 200, 90, S_LOSANGE)
s.box("cont", "<b>La demande continue</b> sans avis<br>règles 5 et 6 · marquée mode dégradé", 380, 960, 280, 80, FIN_OK)
s.box("journal", "<b>Trace</b>, écrite par la Coordination<br>agent, action, durée, statut, appel externe, raison d'une "
                 "indisponibilité (delai_depasse, schema, http_503…) ; jamais le message, le jeton ni le contenu d'une "
                 "réponse écartée", 60, 330, 260, 150, S_CYL)
s.box("budget", "<b>Échéance de la demande</b><br>arrivée + 10 s − 0,4 s de réserve pour la fiche (déduite une seule "
                "fois).<br>Délai du partenaire = min(3 s, échéance − maintenant).<br><i>Exemple : contrôles finis à 8 s, "
                "il reste 1,6 s : le partenaire reçoit 1,6 s, pas 3 s (schéma 7). Réserve et seuil de 0,15 s tirés de la mesure.</i>", 60, 505, 225, 190, S_NOTE)
s.box("esc", "<b>ESCALADE cellule_fraude</b><br>contrôle anti-fraude manuel · mode dégradé", 60, 850, 260, 70, FIN_ESC)
s.box("note", "Jamais de relance (contrat § 6). Doublon dans une même exécution (demande ou lot) : bloqué par le "
              "registre, aucun appel. Après un redémarrage : non couvert (limite écrite) ; le partenaire répond -32029, "
              "traité comme une erreur.", 60, 945, 260, 110, S_NOTE)

s.box("partenaire", "<b>Partenaire anti-fraude</b><br>agent A2A · Agent Card en /.well-known/agent.json", 1140, 285, 350,
      90, S_EXT)
s.box("contrat", "<b>Contrat v2.0</b><br>• requête : une partie data, sept champs exactement<br>"
                 "• réponse : tâche completed, six champs<br>• niveau : faible &lt; 0,40 ≤ modéré &lt; 0,75 ≤ élevé<br>"
                 "• réponse garantie en 2 s ; abandon au plus tard 3 s après l'envoi, plus tôt si l'échéance de la "
                 "demande l'exige<br>• un appel par dossier, aucune relance<br>"
                 "• erreurs : 401, 503, -32700, -32600, -32601, -32602, -32029",
      1140, 560, 350, 190, S_NOTE)

s.edge("x1", "demande", "coord", E_DEP, "lit", [(190, 112), (865, 112)], sortie=(0.5, 0), entree=(0.5, 0))
s.edge("x2", "coord", "af", E_DELEG, "8 données", sortie=(0, 0.25), entree=(1, 0.25))
s.edge("x2b", "af", "coord", E_DEP, "résultat", sortie=(1, 0.8), entree=(0, 0.75))
s.edge("x3", "af", "d0", E_DEP, "indicateur présent", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("x3b", "d0", "filtre", E_DEP, "oui", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("x3c", "d0", "indispo", E_ESC, "non : aucun appel", [(350, 302), (350, 740)], sortie=(0, 0.5), entree=(0, 0.36))
s.edge("x4", "filtre", "appel", E_DEP, "7 champs", [(690, 430), (690, 340)], sortie=(1, 0.5), entree=(0, 0.52))
s.edge("x4b", "filtre", "indispo", E_ESC, "refusé : aucun appel réseau", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("x5", "appel", "partenaire", E_DEP, "message/send", sortie=(1, 0.5), entree=(0, 0.5))
s.edge("x6", "partenaire", "valid", E_EXT, "réponse ou erreur", [(1245, 481)], sortie=(0.3, 1), entree=(1, 0.25))
s.edge("x7", "appel", "valid", E_DEP, "fin de l'attente", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("x8", "valid", "d1", E_DEP, "", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("x9", "d1", "ok", E_OK, "oui", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("x10", "ok", "regle4", E_DEP, "", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("x11", "d1", "indispo", E_ESC, "non", sortie=(0, 0.5), entree=(1, 0.4))
s.edge("x12", "indispo", "dd", E_ESC, "§ 9", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("x13", "dd", "esc", E_ESC, "non", sortie=(0, 0.5), entree=(1, 0.5))
s.edge("x14", "dd", "cont", E_OK, "oui", sortie=(0.5, 1), entree=(0.5, 0))

s.legende([(VERT, "Contrôle écrit en code"), (BLEU, "Agent"), (GRIS, "Partenaire externe"),
           (OK, "Suite normale"), (ESC, "Chemin de repli"), (ORANGE, "Avis indisponible"), (ROUGE, "Données interdites")],
          30, 1095)
s.ecrire("schema-5-echange-a2a", "Échange A2A et mode dégradé", 1540, 1140)

# =============================================================================================================
# Schéma 6 : le plan d'épreuve, attendu et mesuré (mesures du 08/10/2026)
# =============================================================================================================
s = Schema()
s.box("t", "Kaldera V2 · Plan d'épreuve : scénarios × signaux × ajustements · Chantier 2", 30, 20, 1300, 30, S_TITRE)
s.box("st", "Chaque famille de eval/scenarios.jsonl est rejouée par traiter_lot contre le partenaire simulé fourni ; ses "
            "signaux sont comparés au champ attendu. Colonne « mesuré » : outils/mesurer_epreuve.py et tests/integration, "
            "le 08/10/2026.", 30, 54, 1380, 22, S_SOUS)

etapes = [
    ("c1", "<b>1. Rejouer</b> un scénario<br>traiter_lot, partenaire simulé : normal, lent, invalide ou panne", S_ORCH),
    ("c2", "<b>2. Observer</b> les signaux<br>issue, trace (avec la raison d'un échec), appels, durées", S_ORCH),
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

S_CELLULE = BASE + GAUCHE + MILIEU + "rounded=0;fillColor=#ffffff;strokeColor=#bbbbbb;fontSize=11;"
S_MESURE = BASE + GAUCHE + MILIEU + f"rounded=0;fillColor=#eef5ea;strokeColor=#bbbbbb;fontSize=11;"
S_ENTETE = BASE + GAUCHE + MILIEU + f"rounded=0;fillColor=#d9ead3;strokeColor={VERT};fontStyle=1;fontSize=11;"


def tableau(prefixe, colonnes, lignes, y0, h, col_mesure):
    x0 = 60
    for j, (texte, largeur) in enumerate(colonnes):
        x = x0 + sum(c[1] for c in colonnes[:j])
        s.box(f"{prefixe}h{j}", texte, x, y0, largeur, 40, S_ENTETE)
        for i, ligne in enumerate(lignes):
            s.box(f"{prefixe}l{i}c{j}", ligne[j], x, y0 + 40 + i * h, largeur, h,
                  S_MESURE if j == col_mesure else S_CELLULE)
    return y0 + 40 + len(lignes) * h


colonnes = [("Scénarios", 200), ("Exigences", 70), ("Signaux observés", 210), ("Attendu", 330),
            ("Mesuré le 08/10", 310), ("Ajustement possible du chantier 1", 190)]
lignes = [
    ("NOM-01 à 11 · nominaux", "E1, E2", "issue, trace (agent, ecrit), appels externes",
     "11 fiches conformes ; chaque section écrite par son seul propriétaire ; 0 appel au partenaire",
     "11/11 conformes ; 0 appel ; trace de 2 à 6 étapes", "frontière (droits), etapes_max"),
    ("AF-01 à 07 · anti-fraude", "E1, E3", "appels, échecs, message envoyé, avis",
     "7 appels, 0 échec ; sept champs exactement ; niveau d'avis et issue conformes",
     "7/7 conformes ; 7 appels, 0 échec ; lot de 0,07 à 0,10 s", "routage des règles 4 et 5"),
    ("INV-01 à 07 · réponses invalides", "E4, E5", "raison du rejet (trace), avis, mode dégradé",
     "7 réponses écartées au bon niveau ; aucun contenu recopié ; 1 500 € ou moins continue, au-delà cellule_fraude",
     "7/7 conformes ; raisons : schema ×3, incoherence ×2, reponse_non_json, enveloppe_invalide",
     "règles de validation"),
    ("PAN-01 · panne, lot de 5", "E5, E6", "appels, échecs, issues du lot",
     "2 appels, 2 échecs, 0 relance ; 0401 et 0405 non touchés ; 5 fiches conformes",
     "5/5 conformes à chacun des 5 rejeux ; 2 appels, 2 échecs (http_503)", "routage du mode dégradé"),
    ("PAN-02 · lent (5 s), lot de 3", "E5, E6", "durée des appels, des demandes, du lot",
     "abandon à 3 s au plus ; chaque demande sous 10 s ; le lot dure environ 3 s, pas 6 s",
     "3/3 conformes ; lot de 3,021 à 3,033 s sur 5 rejeux ; delai_depasse ×2", "duree_max_s, lot en concurrence"),
    ("BCL-01 · piège à boucle", "E1, E6", "longueur de la trace, arret",
     "escalade avec arret ; trace de 8 étapes au plus", "conforme ; arret etat_repete ; trace de 4 étapes",
     "etapes_max, même état, file"),
]
y_fin = tableau("a", colonnes, lignes, 260, 60, 4)

s.box("titre2", "<b>Tests ciblés du chantier 2</b>, hors scénarios : ils prouvent ce que les 28 scénarios ne montrent pas",
      60, y_fin + 25, 1300, 24, S_SOUS)
colonnes2 = [("Test", 250), ("Où", 170), ("Attendu", 410), ("Mesuré le 08/10", 480)]
lignes2 = [
    ("Temps restant réduit", "intégration, unitaire",
     "le partenaire reçoit min(3 s, temps restant) ; sous 0,15 s, aucun appel ; l'issue tient dans le budget",
     "budget de 2 s : issue en 1,52 s, 1 appel ; sous 0,15 s : 0 appel, 950 € accepté en mode dégradé, 6 900 € vers "
     "cellule_fraude"),
    ("Requête refusée par le filtre", "intégration, unitaire",
     "aucun appel réseau ; avis indisponible, raison requete_non_conforme",
     "journal du partenaire vide ; 950 € accepté en mode dégradé"),
    ("Réponse tardive", "intégration (partenaire à 4 s)", "abandon à 3 s ; la fiche rendue ne change plus",
     "fiche rendue vers 3,0 s ; identique 1,5 s plus tard"),
    ("Doublon : HTTP 200 portant l'erreur JSON-RPC -32029", "intégration (deux exécutions)",
     "traité comme une erreur, jamais comme un avis", "HTTP 200, code -32029 ; avis indisponible, mode dégradé"),
    ("Contenu d'une réponse écartée", "intégration (4 variantes)", "ni dans la fiche, ni dans la trace",
     "aucune trace de EVA-NC, rembourser, commentaire, KAL-26-9999"),
    ("Jeton et données dans les journaux", "unitaire", "ni le jeton, ni le code postal complet",
     "absents des journaux du client et d'httpx (une configuration testée)"),
]
y_fin2 = tableau("b", colonnes2, lignes2, y_fin + 60, 52, 3)

s.box("note", "Sur les 28 scénarios (34 demandes) : 34/34 conformes, 18 appels au partenaire, 0 doublon reçu, jamais deux "
              "appels pour un dossier ; aucun ajustement de borne n'a été nécessaire au rejeu final. Le journal des "
              "ajustements consigne les 7 changements faits pendant la construction. Sources : "
              "evaluation/epreuve/rapport.md (généré) et tests/integration/test_chemin_public_a2a.py.",
      60, y_fin2 + 20, 1310, 60, S_NOTE + MILIEU)
s.legende([(VERT, "Étape de contrôle"), (ORANGE, "Ajustement du chantier 1"), (GRIS, "Journal des ajustements")],
          30, y_fin2 + 100)
s.ecrire("schema-6-plan-epreuve", "Plan d'épreuve", 1430, y_fin2 + 140)

# =============================================================================================================
# Schéma 7 : un budget de 10 secondes, deux chemins de repli (exemple illustratif)
# =============================================================================================================
s = Schema()
s.box("t", "Kaldera V2 · Un budget de 10 secondes, deux chemins de repli · Chantiers 1 et 2", 30, 20, 1250, 30, S_TITRE)
s.box("st", "Une seule échéance par demande, posée à l'arrivée du dossier. Exemple illustratif : les durées sont "
            "choisies pour l'explication, ce n'est pas une mesure.", 30, 54, 1250, 22, S_SOUS)
PX = 120  # pixels par seconde
s.box("seg1", "<b>Lecture des pièces</b>, puis Éligibilité, Pièces et Estimation", 60, 100, 8 * PX, 60,
      S_ORCH + CENTRE)
s.box("seg2", "<b>Partenaire</b><br>1,6 s au plus", 60 + 8 * PX, 100, int(1.6 * PX), 60, S_EXT + CENTRE)
s.box("seg3", "fiche", 60 + int(9.6 * PX), 100, int(0.4 * PX), 60, S_AMBIG + CENTRE + "fontSize=10;")
TICK = "text;html=1;fontFamily=Arial;fontSize=11;fontColor=#555555;align=center;verticalAlign=top;"
for libelle, sec in [("0 s", 0), ("8 s", 8), ("9,6 s", 9.6), ("10 s", 10)]:
    s.box(f"tk{sec}", libelle, 60 + int(sec * PX) - 30, 165, 60, 20, TICK)
s.box("explic", "<b>0 s</b> : le dossier arrive ; échéance = 10 s − 0,4 s de réserve pour la fiche, soit 9,6 s.<br>"
                "<b>8 s</b> : lecture et contrôles finis ; un indicateur F1 à F4 demande l'avis du partenaire.<br>"
                "<b>8 à 9,6 s</b> : le partenaire reçoit min(3 s, 9,6 − 8) = 1,6 s, et non 3 s.<br>"
                "<b>9,6 à 10 s</b> : la Coordination produit la fiche, avec l'avis conforme ou le repli prévu (réserve de 0,4 s, tirée de la mesure).",
      60, 200, 1200, 95, S_NOTE)

s.box("g_titre", "Repli 1 · chantier 1", 60, 320, 560, 30, S_SOUS + "fontStyle=1;")
s.box("lect", "<b>Lecture impossible</b><br>modèle en panne, délai dépassé pendant la lecture, contrat illisible",
      60, 355, 560, 70, S_LECTEUR)
s.box("lect_fin", "<b>ESCALADE gestionnaire</b>, motif technique<br>aucune décision sur des données incomplètes ; "
                  "la règle des 1 500 € ne s'applique pas", 60, 470, 560, 75, FIN_ESC)
s.edge("l1", "lect", "lect_fin", E_ESC, "", sortie=(0.5, 1), entree=(0.5, 0))

s.box("d_titre", "Repli 2 · chantier 2", 700, 320, 560, 30, S_SOUS + "fontStyle=1;")
s.box("avis", "<b>Avis anti-fraude indisponible</b>, alors que le contrôle était requis<br>budget épuisé, requête "
              "refusée, délai, erreur ou réponse écartée", 700, 355, 560, 70, S_AMBIG)
s.box("dd7", "Montant estimé<br>≤ 1 500 € ?", 880, 450, 200, 90, S_LOSANGE)
s.box("cont7", "<b>Continue</b>, marquée mode dégradé<br>règles 5 et 6", 700, 570, 260, 65, FIN_OK)
s.box("esc7", "<b>ESCALADE cellule_fraude</b><br>contrôle manuel", 1000, 570, 260, 65, FIN_ESC)
s.edge("a1", "avis", "dd7", E_ESC, "§ 9", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("a2", "dd7", "cont7", E_OK, "oui", sortie=(0, 0.5), entree=(0.5, 0))
s.edge("a3", "dd7", "esc7", E_ESC, "non", sortie=(1, 0.5), entree=(0.5, 0))

s.box("pourquoi", "<b>Pourquoi deux traitements ?</b> Sans lecture fiable, aucun montant n'est sûr : un humain reprend. "
                  "Sans avis du partenaire, les contrôles sont faits et le montant est connu : la spec (§ 9) prévoit la "
                  "règle des 1 500 €. Sans indicateur, aucun avis n'est demandé : jamais de mode dégradé. Échéance déjà "
                  "dépassée avant l'Anti-fraude : escalade gestionnaire par la borne duree_max_s.",
      60, 665, 1200, 80, S_NOTE)
s.legende([(VERT, "Code"), (CYAN, "Agent de lecture"), (GRIS, "Partenaire externe"), (ORANGE, "Avis indisponible"),
           (OK, "Suite normale"), (ESC, "Escalade")], 30, 770)
s.ecrire("schema-7-budget-10-s", "Budget de 10 s et replis", 1300, 810)
