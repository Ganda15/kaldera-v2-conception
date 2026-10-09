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
s.box("st", "Rôles, frontières, ordre d'exécution et point ambigu tranché. Mis à jour le 08/10/2026 : lecture des pièces "
            "en amont (phase E), contrôles en séquence avec court-circuit (coordination.derouler) ; la nuit : agent "
            "Documents et cohérence (2 bis, spec § 5), dont l'appel au modèle part dès l'arrivée du dossier.",
      30, 54, 1700, 22, S_SOUS)

# --- en amont : lecture des pièces (phase E) et appel de cohérence lancé à l'arrivée ---
s.box("lect", "Avant la Coordination · Lecture des pièces (phase E), comprise dans les 10 s de la demande", 30, 88, 1720, 212,
      S_CONTENEUR)
s.box("docs", "<b>Pièces de l'assuré</b>, non structurées<br>contrat.pdf · images des pièces jointes (factures, photos, "
              "dépôt de plainte) · dépôts de l'espace assuré · formulaire declaration.json",
      50, 123, 300, 160, S_NOTE)
s.box("lc", "<b>Lecteur de contrat</b> (modèle, schéma strict)<br>Texte du PDF : numéro, formule, date, statut, "
            "cotisations.<br>" + ROUGE_TXT + "décider, deviner un champ." + FIN, 400, 123, 330, 95, S_LECTEUR)
s.box("lp", "<b>Lecteur de pièces</b> (netteté en code, puis modèle)<br>Floue : illisible sans appel. Facture nette : "
            "montant lu. Dans le doute : illisible.<br>" + ROUGE_TXT + "décider, inventer un montant." + FIN,
      790, 123, 330, 95, S_LECTEUR)
s.box("cappel", "<b>En même temps, dès l'arrivée : l'appel de cohérence</b> (modèle, vision). Images nettes et "
                "déclaration, un seul appel ; son résultat attend l'agent 2 bis, plus bas. Il ne dépend pas de la lecture.",
      400, 233, 720, 50, S_LECTEUR + "dashed=1;" + MILIEU)
s.box("json", "<b>Demande au format § 3</b><br>la même que sur le chemin JSON. Contrat lu différent du déclaré, ou "
              "modèle en panne : escalade gestionnaire, aucun contrôle lancé.", 1170, 123, 330, 160, S_NOTE)
s.edge("r1", "docs", "lc", E_DEP, "", sortie=(1, 0.3), entree=(0, 0.5))
s.edge("r2", "lc", "lp", E_DEP, "numéro<br>conforme", sortie=(1, 0.5), entree=(0, 0.5))
s.edge("r3", "lp", "json", E_DEP, "", sortie=(1, 0.5), entree=(0, 0.3))
s.edge("r5", "docs", "cappel", E_DEP, "", sortie=(1, 0.86), entree=(0, 0.5))
s.edge("r4", "json", "orch", E_DEP, "demande § 3", sortie=(0.5, 1), entree=(0.8061, 0))

# --- la Coordination et les cinq contrôles, dans l'ordre ---
s.box("orch", "<b>Coordination</b> (code, sans LLM) · <b>écrit : issue</b> · seule à lire et à écrire l'état<br>"
              "Délègue chaque contrôle dans l'ordre, vérifie les bornes, applique les règles de décision (spec § 10) "
              "et conclut dès qu'une règle s'applique. Seule à conclure.<br>"
              + ROUGE_TXT + "refaire un contrôle (éligibilité, pièces, cohérence, montant, fraude)." + FIN,
      150, 330, 1470, 78, S_ORCH)

XS = [30, 380, 730, 1080, 1430]  # cinq colonnes de 290, 60 entre elles
YC, HC = 455, 215
s.box("elig", "<b>1 · Éligibilité</b> (règles en code) · <b>section : eligibilite</b><br><br>"
              "Vérifie E1 à E5 : contrat actif, cotisations, carence de 30 jours, délai de déclaration, garantie de la formule.<br>"
              "Renvoie : éligible oui ou non, conditions non remplies.<br><br>"
              + ROUGE_TXT + "chiffrer, appliquer le plafond, juger les pièces ou la fraude." + FIN,
      XS[0], YC, 290, HC, S_AGENT)
s.box("pieces", "<b>2 · Pièces justificatives</b> (code) · <b>section : pieces</b><br><br>"
                "Vérifie présence, lisibilité (rendue par le Lecteur de pièces) et type attendu. Adresse le complément "
                "quand la Coordination le lui confie, 2 fois au plus.<br>"
                "Renvoie : complet, ou manquantes ; les factures lisibles.<br><br>"
                + ROUGE_TXT + "conclure, chiffrer, juger la fraude, décider seul d'un complément." + FIN,
      XS[1], YC, 290, HC, S_AGENT)
s.box("coh", "<b>2 bis · Documents et cohérence</b> (modèle, vision ; verdict en code) · <b>section : coherence</b><br><br>"
             "Chemin des pièces seulement (§ 5). Le modèle dit à quel sinistre se rapporte chaque pièce nette ; le code "
             "vérifie les écarts (autre sinistre, facture antérieure) et rend : cohérent, contradiction, insuffisant ou "
             "non effectué.<br><br>"
             + ROUGE_TXT + "refuser, chiffrer, juger la preuve ou la fraude." + FIN,
      XS[2], YC, 290, HC, S_LECTEUR)
s.box("estim", "<b>3 · Estimation</b> (règles en code) · <b>section : estimation</b><br><br>"
               "Montant justifié (factures lisibles), montant retenu (le plus petit des deux), "
               "moins la franchise, puis <b>plafond de la formule</b>.<br>"
               "Renvoie : montant justifié et montant estimé.<br><br>"
               + ROUGE_TXT + "juger la fraude, revenir sur l'éligibilité." + FIN,
      XS[3], YC, 290, HC, S_AGENT)
s.box("fraude", "<b>4 · Anti-fraude, liaison avec le partenaire</b> (code) · <b>section : avis_fraude</b><br><br>"
                "Indicateurs F1 à F4. Si au moins un : un seul appel au partenaire, puis contrôle de sa réponse.<br>"
                "Renvoie : non requis, avis (niveau et score), ou indisponible.<br><br>"
                + ROUGE_TXT + "émettre un avis en interne, envoyer une donnée hors contrat, relancer un appel." + FIN,
      XS[4], YC, 290, HC, S_AGENT)

for k, (aid, x) in enumerate(zip(("elig", "pieces", "coh", "estim", "fraude"), XS)):
    s.edge(f"d{k}", "orch", aid, E_DELEG, "délègue" if k == 0 else "", sortie=((x + 145 - 150) / 1470, 1), entree=(0.5, 0))
s.edge("s1", "elig", "pieces", E_DEP, "si<br>éligible", sortie=(1, 0.3), entree=(0, 0.3))
s.edge("s2", "pieces", "coh", E_DEP, "si<br>complet", sortie=(1, 0.3), entree=(0, 0.3))
s.edge("s2b", "coh", "estim", E_DEP, "si<br>cohérent", sortie=(1, 0.3), entree=(0, 0.3))
s.edge("s3", "estim", "fraude", E_DEP, "si<br>montant<br>> 0", sortie=(1, 0.3), entree=(0, 0.3))

# --- les courts-circuits : la Coordination conclut sans lancer la suite ---
YS = YC + HC + 25
s.box("stop1", "Non éligible : <b>refusée</b> (règle 1)<br>les pièces ne sont jamais vérifiées", XS[0], YS, 290, 62, S_FIN_OK)
s.box("stop2", "Pièces encore manquantes, ou aucun dépôt : <b>escalade gestionnaire</b> (règle 2)",
      XS[1], YS, 290, 62, S_FIN_ESC)
s.box("stop2b", "Contradiction, doute ou échec technique : <b>escalade gestionnaire</b>, avec la pièce en cause",
      XS[2], YS, 290, 62, S_FIN_ESC)
s.box("stop3", "Montant nul après la franchise : <b>refusée</b> (règle 3)", XS[3], YS, 290, 62, S_FIN_OK)
s.edge("k1", "elig", "stop1", E_OK, "non", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("k2", "pieces", "stop2", E_ESC, "non", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("k2b", "coh", "stop2b", E_ESC, "non", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("k3", "estim", "stop3", E_OK, "non", sortie=(0.5, 1), entree=(0.5, 0))

s.box("partenaire", "<b>Partenaire anti-fraude</b> (agent A2A externe)<br>"
                    "rend l'avis : faible, modéré ou élevé · contrat, filtre et mode dégradé : chantier 2",
      XS[4], YS + 25, 290, 80, S_EXT)
s.edge("x1", "fraude", "partenaire", E_EXT, "si au moins un indicateur", sortie=(0.3, 1), entree=(0.3, 0))
s.edge("x2", "partenaire", "fraude", E_EXT, "avis à contrôler", sortie=(0.8, 0), entree=(0.8, 1))

YN = YS + 135
s.box("autres", "<b>Autres frontières tranchées</b><br>"
                "• Pièces manquantes : constatées par Pièces ; l'escalade est décidée par la Coordination (règle 2).<br>"
                "• Montant justifié : calculé par l'Estimation (§ 6), à partir des factures lisibles fournies par Pièces.<br>"
                "• Indicateurs F1 à F4 : Anti-fraude, après l'Estimation, car F4 compare le montant déclaré au montant justifié.<br>"
                "• Cohérence avec la déclaration (§ 5) : sur le chemin JSON, le type des pièces (Pièces) ; sur le chemin des "
                "pièces, l'agent 2 bis, dans sa propre section, hors des cinq sections métier : « pieces » reste à Pièces.",
      30, YN, 560, 160, S_NOTE)
s.box("ambig", "<b>Point ambigu tranché : qui applique le plafond ?</b><br><br>"
               "La spec range le plafond dans l'éligibilité (§ 4), mais « le contrôle d'éligibilité ne chiffre pas » (§ 2), "
               "et l'estimation (§ 6) ne le cite pas. <b>Choix : l'Estimation</b>, parce que le plafond est un calcul de montant.<br><br>"
               "<i>Preuve, scénario NOM-05 : 4 200 € déclarés, moins 300 € de franchise = 3 900 €, plafonnés à 3 000 €.</i>",
      620, YN, 520, 160, S_AMBIG)
s.box("ordre", "<b>Ordre et court-circuit</b> (coordination.derouler)<br>"
               "1 Éligibilité, 2 Pièces (avec 2 compléments au plus), 2 bis Cohérence (chemin des pièces), 3 Estimation, "
               "4 Anti-fraude. Un contrôle n'est lancé que si le précédent n'a pas conclu : une demande non éligible ne "
               "fait jamais vérifier ses pièces. C'est la Coordination qui conclut, jamais l'agent.<br>"
               "Après l'Anti-fraude : règle 4 (avis modéré ou élevé, mode dégradé), règle 5 (plus de 10 000 € : "
               "gestionnaire), règle 6 (acceptée).", 1170, YN, 580, 160, S_NOTE)

YL = YN + 190
s.legende([(VERT, "Code (coordination)"), (CYAN, "Agent avec modèle"), (BLEU, "Agent de contrôle"),
           (ORANGE, "Point ambigu tranché"), (ROUGE, "Frontière : interdit"), (OK, "Décision"), (ESC, "Escalade"),
           (GRIS, "Externe ou chantier 2")], 30, YL)
s.box("lg2", "Trait plein : ordre ou données · pointillé vert : délégation · « section » : celle que remplit le résultat "
             "de l'agent, rangé par la Coordination · agent avec modèle : le modèle lit ou interprète, sa sortie est validée "
             "par un schéma strict, le code décide · cadre pointillé : appel lancé à l'arrivée",
      30, YL + 36, 1700, 20, S_SOUS)
s.ecrire("schema-1-carte-des-agents", "Carte des agents", 1780, YL + 70)

# =============================================================================================================
# Schéma 2 : l'orchestration et la terminaison garantie
# =============================================================================================================
s = Schema()
s.box("t", "Kaldera V2 · Orchestration et terminaison garantie · Chantier 1", 30, 20, 1100, 30, S_TITRE)
s.box("st", "Chaque losange est une règle de décision appliquée par la Coordination, dans l'ordre de la spec (§ 10) ; "
            "la première qui s'applique fixe l'issue. Contrôles en séquence (mis à jour le 08/10/2026) : une demande non "
            "éligible ne fait jamais vérifier ses pièces. La nuit : la cohérence des pièces (2 bis, § 5), sur le chemin "
            "des pièces. Chaque chemin finit par une décision ou par une escalade motivée.",
      30, 54, 1500, 22, S_SOUS)

FIN_REF = S_FIN_OK + CENTRE + "fontSize=11;"
FIN_ESC = S_FIN_ESC + CENTRE + "fontSize=11;"
D = 205  # décalage vertical sous l'étape de cohérence
s.box("s0", "<b>Demande reçue</b><br>état créé, section demande en lecture seule", 120, 95, 300, 52, S_ORCH + CENTRE)
s.box("e", "<b>Éligibilité</b> (contrôle 1)<br>E1 à E5", 155, 172, 230, 55, S_AGENT + CENTRE)
s.box("r1", "Éligible ?", 160, 255, 220, 90, S_LOSANGE)
s.box("t1", "<b>DÉCISION : REFUSÉE</b> · règle 1<br>0 € ; le motif cite les conditions non remplies", 480, 270, 340, 60, FIN_REF)
s.box("p", "<b>Pièces</b> (contrôle 2)<br>présence, lisibilité", 155, 375, 230, 55, S_AGENT + CENTRE)

s.box("r2", "Pièces exigées<br>présentes et lisibles ?", 160, 455, 220, 100, S_LOSANGE)
s.box("c", "<b>Pièces : demande de complément</b> (2 au plus)<br>via l'espace assuré, puis nouveau contrôle", 480, 475, 340, 60, S_AGENT + CENTRE)
s.box("t2", "<b>ESCALADE gestionnaire</b> · règle 2<br>motif : pièces manquantes", 880, 475, 300, 60, FIN_ESC)

s.box("coh", "<b>Documents et cohérence</b> (2 bis)<br>chemin des pièces : verdict de l'appel lancé à l'arrivée",
      120, 595, 300, 58, S_LECTEUR + CENTRE)
s.box("rc", "Pièces cohérentes<br>avec la déclaration ?", 160, 680, 220, 100, S_LOSANGE)
s.box("tc", "<b>ESCALADE gestionnaire</b> · § 5<br>contradiction (pièce citée), doute, ou contrôle impossible : trois "
            "motifs distincts", 480, 695, 340, 70, FIN_ESC)

s.box("est", "<b>Estimation</b><br>justifié, retenu, franchise, plafond", 120, 595 + D, 300, 58, S_AGENT + CENTRE)
s.box("r3", "Montant estimé<br>nul ?", 160, 685 + D, 220, 90, S_LOSANGE)
s.box("t3", "<b>DÉCISION : REFUSÉE</b> · règle 3<br>0 € ; dommage inférieur ou égal à la franchise", 480, 700 + D, 340, 60, FIN_REF)

s.box("r4", "Anti-fraude :<br>un indicateur F1 à F4 ?", 160, 810 + D, 220, 100, S_LOSANGE)
s.box("pa", "<b>Avis du partenaire</b> (chantier 2)<br>un seul appel, au plus 3 s dans le temps restant, aucune relance", 480, 830 + D, 340, 60, S_EXT)
s.box("t4a", "<b>ESCALADE gestionnaire</b> · avis modéré<br>motif : contrôle renforcé", 880, 780 + D, 300, 56, FIN_ESC)
s.box("t4b", "<b>ESCALADE cellule_fraude</b> · avis élevé<br>motif : suspicion de fraude", 880, 850 + D, 300, 56, FIN_ESC)
s.box("deg", "<b>Avis indisponible : mode dégradé</b> (§ 9)<br>délai dépassé, erreur ou réponse non conforme", 480, 940 + D, 340, 60, S_EXT)
s.box("t4c", "<b>ESCALADE cellule_fraude</b><br>montant estimé &gt; 1 500 €, mode dégradé", 880, 940 + D, 300, 56, FIN_ESC)

s.box("r5", "Montant estimé<br>&gt; 10 000 € ?", 160, 1045 + D, 220, 90, S_LOSANGE)
s.box("t5", "<b>ESCALADE gestionnaire</b> · règle 5<br>motif : seuil de délégation dépassé", 480, 1060 + D, 340, 60, FIN_ESC)
s.box("t6", "<b>DÉCISION : ACCEPTÉE</b> · règle 6<br>montant remboursé = montant estimé", 120, 1175 + D, 300, 60, FIN_REF)

s.box("bornes", "<b>Bornes</b>, tirées de la spec et de la mesure<br>vérifiées par la Coordination avant chaque délégation<br><br>"
                "• Durée par demande : <b>10 s</b>, lecture des pièces comprise (spec § 12)<br>"
                "• Étapes par demande : <b>8</b> au plus (une étape = une délégation = une ligne de trace)<br>"
                "&nbsp;&nbsp;&nbsp;(chemin JSON : 5 ; plus 2 compléments ; plus 1 de marge)<br>"
                "&nbsp;&nbsp;&nbsp;(chemin des pièces : 6, cohérence comprise ; plus 2 compléments : 8, sans marge)<br>"
                "&nbsp;&nbsp;&nbsp;la dernière étape est réservée à l'issue : la trace ne dépasse jamais 8<br>"
                "• Demandes de complément : <b>2</b> au plus<br>"
                "• Même état vu deux fois : arrêt immédiat<br>"
                "• Appel au partenaire : 3 s (contrat § 5) ; contrôle interne : objectif 1 s, non imposé (mesuré : 0,01 ms)<br>"
                "• Lot : demandes traitées en concurrence, 10 s chacune (§ 12)<br><br>"
                "<b>Borne atteinte</b> : ESCALADE gestionnaire, et la fiche le signale dans <i>arret</i> (nom de la borne).<br><br>"
                "<i>Fondées sur le chemin le plus long prévu par la spec et les scénarios ; "
                "le chantier 2 les éprouve (BCL-01, PAN-02), chaque changement entre au journal des ajustements.</i>",
      1240, 95, 400, 415, S_AMBIG + "fillColor=#fff2cc;strokeColor=#bf9000;arcSize=4;")
s.box("qui", "<b>Qui décide que la demande est terminée ?</b><br>"
             "La Coordination seule, en écrivant la section issue (« seule la décision conclut la demande », § 2). "
             "Aucun autre état final : jamais « en attente » sans qu'un humain en soit saisi.",
      1240, 530, 400, 110, S_NOTE)
s.box("comp", "<b>Pourquoi le complément après l'éligibilité ?</b><br>"
              "Une demande non éligible est refusée quel que soit l'état de ses pièces (règle 1) : "
              "inutile de solliciter l'assuré. La Coordination décide le complément ; Pièces l'adresse.",
      1240, 660, 400, 100, S_NOTE)
s.box("pcoh", "<b>Pourquoi la cohérence à cet endroit ?</b><br>"
              "Après un contrôle des pièces complet : une pièce manquante suit d'abord le complément. Après l'Éligibilité : "
              "un refus du § 4 reste prioritaire. Avant l'Estimation : on ne chiffre pas des pièces qui contredisent la "
              "déclaration. Le modèle interprète chaque pièce et dit si elle concorde ; le code vérifie les écarts et rend le verdict ; aucune issue de la cohérence n'est une décision. "
              "Sur le chemin JSON, l'étape n'existe pas.",
      1240, 780, 400, 150, S_NOTE)

s.edge("a1", "s0", "e", E_DELEG, "délègue", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("a3", "e", "r1", E_DEP, "", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("b1", "r1", "t1", E_OK, "non", sortie=(1, 0.5), entree=(0, 0.5))
s.edge("b2", "r1", "p", E_DELEG, "oui : délègue", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("b2b", "p", "r2", E_DEP, "", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("b3", "r2", "c", E_DEP, "non", sortie=(1, 0.5), entree=(0, 0.5))
s.edge("b4", "c", "r2", E_DEP, "nouveau dépôt", [(650, 565), (330, 565)], sortie=(0.5, 1), entree=(0.77, 0.9))
s.edge("b5", "c", "t2", E_ESC, "aucun dépôt du type", sortie=(1, 0.5), entree=(0, 0.5))
s.edge("b6", "r2", "coh", E_DELEG, "oui : délègue", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("bc1", "coh", "rc", E_DEP, "", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("bc2", "rc", "tc", E_ESC, "non", sortie=(1, 0.5), entree=(0, 0.5))
s.edge("bc3", "rc", "est", E_DEP, "oui (ou chemin JSON)", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("b7", "est", "r3", E_DEP, "", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("b8", "r3", "t3", E_OK, "oui", sortie=(1, 0.5), entree=(0, 0.5))
s.edge("b9", "r3", "r4", E_DEP, "non", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("b10", "r4", "pa", E_EXT, "oui", sortie=(1, 0.5), entree=(0, 0.5))
s.edge("b11", "pa", "t4a", E_ESC, "modéré", [(850, 850 + D), (850, 808 + D)], sortie=(1, 0.33), entree=(0, 0.5))
s.edge("b12", "pa", "t4b", E_ESC, "élevé", sortie=(1, 0.75), entree=(0, 0.5))
s.edge("b13", "pa", "deg", E_EXT, "indisponible", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("b14", "deg", "t4c", E_ESC, "> 1 500 €", sortie=(1, 0.5), entree=(0, 0.5))
# point de jonction sur l'axe : la demande poursuit vers la règle 5
s.box("j", "", 264, 1009 + D, 12, 12, "ellipse;fillColor=#333333;strokeColor=#333333;")
s.edge("b15", "deg", "j", E_EXT, "", [(650, 1015 + D)], sortie=(0.5, 1), entree=(1, 0.5))
s.edge("b16", "pa", "j", E_EXT, "", [(440, 881 + D), (440, 1015 + D)], sortie=(0, 0.85), entree=(1, 0.5))
LIB = "text;html=1;fontFamily=Arial;fontSize=11;fontColor=#555555;align=center;verticalAlign=middle;whiteSpace=wrap;"
s.box("lb16", "faible : poursuit", 300, 935 + D, 130, 20, LIB)
s.box("lb15", "≤ 1 500 € : continue, marquée mode dégradé", 470, 1021 + D, 350, 18, LIB)
s.edge("b17", "r4", "j", E_DEP, "non", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("b17b", "j", "r5", E_DEP, "", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("b18", "r5", "t5", E_ESC, "oui", sortie=(1, 0.5), entree=(0, 0.5))
s.edge("b19", "r5", "t6", E_OK, "non", sortie=(0.5, 1), entree=(0.5, 0))

s.legende([(VERT, "Règle de la Coordination"), (BLEU, "Contrôle délégué"), (CYAN, "Agent avec modèle"),
           (OK, "Fin : décision"), (ESC, "Fin : escalade"), (GRIS, "Chantier 2"), (ORANGE, "Bornes")], 30, 1275 + D)
s.ecrire("schema-2-orchestration", "Orchestration et terminaison", 1670, 1325 + D)

# =============================================================================================================
# Schéma 3 : la mémoire partagée de la demande
# =============================================================================================================
s = Schema()
s.box("t", "Kaldera V2 · Mémoire partagée de la demande · Chantier 1", 30, 20, 1100, 30, S_TITRE)
s.box("st", "Un état par demande. Seule la Coordination le lit et l'écrit : elle passe à chaque agent ses entrées, reçoit son "
            "résultat et le range dans la section de cet agent ; la trace note quel agent a fourni chaque section (interface.md).",
      30, 54, 1600, 22, S_SOUS)

s.box("agents", "Agents : appelés directement, ils ne voient pas l'état (flèches : entrées et résultat)", 30, 100, 380, 490, S_GROUPE)
AG = S_AGENT + "fontSize=11;"
s.box("ae", "<b>Éligibilité</b><br>reçoit : contrat, sinistre (types et dates)", 50, 140, 340, 60, AG)
s.box("ap", "<b>Pièces</b><br>reçoit : type de sinistre, pièces, dépôts de l'espace assuré", 50, 220, 340, 60, AG)
s.box("acoh", "<b>Documents et cohérence</b> (2 bis, chemin des pièces)<br>reçoit : le sinistre déclaré ; les images "
              "nettes du dossier, connues dès l'arrivée", 50, 300, 340, 70, S_LECTEUR + "fontSize=11;")
s.box("aes", "<b>Estimation</b><br>reçoit : montant déclaré, formule, factures lisibles", 50, 390, 340, 60, AG)
s.box("af", "<b>Anti-fraude</b><br>reçoit : 8 données, dont le montant justifié<br>"
            f'<font color="{ROUGE}">ne reçoit jamais : identité, IBAN, description, pièces</font>', 50, 470, 340, 75, AG)

s.box("coord", "<b>Coordination</b><br>seule à lire et à écrire l'état<br><br>1. appelle l'agent avec ses entrées<br>"
               "2. reçoit son résultat<br>3. le range dans la section de cet agent<br>4. décide de l'appel suivant<br><br>"
               "écrit aussi issue et la trace", 440, 100, 170, 490, S_ORCH)

s.box("etat", "État de la demande · reference (KAL-AA-NNNN)", 660, 100, 600, 700, S_CONTENEUR)
SEC_NEUTRE = BASE + GAUCHE + "rounded=0;fillColor=#ffffff;strokeColor=#999999;fontSize=11;"
SEC_AGENT = BASE + GAUCHE + f"rounded=0;fillColor=#cfe2f3;strokeColor={BLEU};fontSize=11;"
SEC_ORCH = BASE + GAUCHE + f"rounded=0;fillColor=#d9ead3;strokeColor={VERT};fontSize=11;"
SEC_COH = BASE + GAUCHE + f"rounded=0;fillColor=#d0e0e3;strokeColor={CYAN};fontSize=11;"
sections = [
    ("demande", "<b>demande</b> : la demande reçue (§ 3)<br>écrite à la création, puis en lecture seule", SEC_NEUTRE, 138),
    ("eligibilite", "<b>eligibilite</b> · résultat d'Éligibilité<br>éligible, conditions non remplies", SEC_AGENT, 210),
    ("pieces", "<b>pieces</b> · résultat de Pièces, rangé à nouveau après chaque dépôt<br>complet ou manquantes, factures lisibles", SEC_AGENT, 282),
    ("coherence", "<b>coherence</b> · résultat de Documents et cohérence (chemin des pièces)<br>verdict et pièces en "
                  "cause ; hors des 5 sections métier d'interface.md", SEC_COH, 354),
    ("estimation", "<b>estimation</b> · résultat d'Estimation<br>montant justifié, montant estimé", SEC_AGENT, 426),
    ("avis_fraude", "<b>avis_fraude</b> · résultat d'Anti-fraude<br>non requis, avis (niveau, score, evaluation_id) ou indisponible "
                    "(raison)",
     SEC_AGENT, 498),
    ("issue", "<b>issue</b> · écrite par la Coordination, conclut la demande<br>décision ou escalade, montant, motif, file, mode dégradé",
     SEC_ORCH, 578),
    ("trace", "<b>trace</b> (hors métier), ajout seul : une étape par ligne<br>agent dont le résultat est rangé, section "
              "remplie, durée, statut, raison d'un avis indisponible", SEC_ORCH, 656),
    ("hors", "<b>hors de l'état</b> : l'échéance de la demande, le registre des appels (une exécution) ; "
             "arret est écrit dans la fiche", SEC_NEUTRE, 724),
]
for sid, texte, style, y in sections:
    s.box(sid, texte, 680, y, 560, 56 if sid not in ("hors",) else 44, style)

for aid, y in [("ae", 170), ("ap", 250), ("acoh", 335), ("aes", 420), ("af", 507)]:
    s.edge(f"io{aid}", "coord", aid, E_DEP + "startArrow=block;startFill=1;", "", sortie=(0, round((y - 100) / 490, 4)),
           entree=(1, 0.5))
s.edge("lit", "etat", "coord", E_DEP, "lit", sortie=(0, 0.12), entree=(1, 0.25))
s.edge("range", "coord", "etat", E_DEP, "range", sortie=(1, 0.55), entree=(0, 0.42))

s.box("garde", "<b>Comment aucun agent n'écrase le travail d'un autre</b><br>"
               "• Seule la Coordination lit et écrit l'état ; aucun agent ne le reçoit.<br>"
               "• Une table fixe associe chaque agent à sa section ; ranger un résultat ailleurs est refusé (erreur de droits).<br>"
               "• pieces est remplie à nouveau après chaque dépôt ; les autres sections métier une seule fois.<br>"
               "• coherence a son propre agent, hors des cinq sections métier : pieces reste au seul agent Pièces.<br>"
               "• La trace note, à chaque étape, l'agent dont le résultat est rangé et la section remplie : la règle se vérifie par un test.",
      1310, 100, 400, 230, S_AMBIG)
s.box("vit", "<b>Où vit-elle ?</b><br>En mémoire, un objet par demande, créé au début du traitement. "
             "Jamais partagé entre deux demandes : le traitement d'une demande n'en retarde pas une autre (§ 12). "
             "À la fin, la fiche de décision est construite depuis issue, avis_fraude, trace et arret.",
      1310, 350, 400, 140, S_NOTE)
s.box("part", "<b>Partenaire anti-fraude</b><br>reçoit seulement les 7 champs du contrat, construits par Anti-fraude (chantier 2)",
      1310, 510, 400, 70, S_EXT)
s.box("metr", "<b>Métriques par agent</b> (chantier 2)<br>calculées depuis la trace : appels, échecs, latence, appels externes",
      1310, 660, 400, 70, S_EXT)
s.edge("m1", "avis_fraude", "part", E_EXT, "filtre", sortie=(1, 0.5), entree=(0, 0.5))
s.edge("m2", "trace", "metr", E_EXT, "", sortie=(1, 0.5), entree=(0, 0.5))

s.legende([(VERT, "Coordination"), (BLEU, "Agent et section remplie par son résultat"), (CYAN, "Agent avec modèle et sa section"),
           (ORANGE, "Règle de rangement"), (ROUGE, "Jamais transmis"), (GRIS, "Externe ou chantier 2")], 30, 830)
s.ecrire("schema-3-memoire-partagee", "Mémoire partagée", 1740, 870)

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
        ("r0", "<b>Retenu</b> : un modèle là où il faut interpréter un document : deux agents de lecture et la "
               "cohérence des pièces avec la déclaration (2 bis). <b>Écarté</b> : une règle chiffrée confiée à un LLM ; "
               "règles, montant et décision restent en code (§ 4 à § 10).", S_RETENU, "retient"),
        ("r1", "<b>Écarté</b> : l'agent unique. Ses rôles ne peuvent pas être prouvés séparément ; la trace exige un agent par section.",
         S_ECARTE, "écarte"),
        ("r2", "<b>Écarté</b> : un planificateur LLM qui invente les étapes. Le parcours est fixé par la spec (§ 2), "
               "testable et bornable.", S_ECARTE, "écarte"),
        ("r3", "<b>Retenu</b> : contrôles en séquence, dans l'ordre de la spec, arrêt dès qu'une règle conclut ; "
               "les demandes d'un lot en parallèle (§ 12).", S_RETENU, "retient"),
        ("r4", "<b>Écarté</b> : des agents qui se passent la main sans contrôle central ; personne ne garantirait l'issue "
               "de chaque demande, ni les 10 s.", S_ECARTE, "écarte"),
        ("r5", "<b>Ajouté</b> : une trace à chaque étape (agent, sections écrites), source des métriques par agent.",
         S_RETENU, "ajoute"),
    ],
    reponses=["en partie : règles chiffrées, avis externe ; des documents à lire et à confronter", "non",
              "oui : éligibilité et pièces, estimation, anti-fraude, issue (§ 2)",
              "dans une demande, non utile (0,01 ms par contrôle) ; entre demandes, oui", "oui",
              "appels, échecs, latence, appels externes (interface.md)"],
    final="<b>Pattern retenu</b> : une Coordination centrale en code (pattern superviseur), seule à conclure · quatre "
          "contrôles déterministes, chacun maître d'une seule section, en séquence avec court-circuit · un agent de "
          "cohérence des pièces (2 bis, modèle qui interprète, verdict en code) · deux agents de lecture en amont (phase E) · "
          "un seul appel au partenaire · une trace à chaque étape",
    tension="<b>Tension à arbitrer</b> : le code est prévisible mais rigide ; un système tout agentique est souple mais "
            "difficile à garantir. Ici chaque règle est chiffrée et les engagements sont absolus (issue garantie, 10 s) : "
            "un squelette en code, l'avis externe venant du partenaire.",
    legende=[(VIOLET, "Question métier"), (VERT, "Question d'architecture"), (GRIS, "Option écartée"),
             (BLEU, "Option retenue ou ajoutée"), (ORANGE, "Tension à arbitrer")],
)

# =============================================================================================================
# Schéma A : l'architecture générale (l'équipe, la mémoire, l'extérieur et les issues sur une seule vue)
# =============================================================================================================
s = Schema()
s.box("t", "Kaldera V2 · Architecture générale · Chantier 1", 30, 20, 1000, 30, S_TITRE)
s.box("st", "Une seule vue : l'entrée, la Coordination, les contrôles, la mémoire partagée de la demande, les échanges "
            "avec l'extérieur et les deux issues possibles. Mis à jour le 08/10/2026 : contrôles en séquence, lecture des "
            "pièces en amont (schéma E) ; la nuit : agent Documents et cohérence (2 bis, § 5).",
      30, 54, 1500, 22, S_SOUS)

s.box("lot", "<b>Entrée</b> : une demande JSON, ou un dossier lu par les deux agents de lecture (schéma E) ; "
             "l'appel de cohérence part dès l'arrivée. Chaque demande a son état et ses 10 s ; un lot est traité en "
             "parallèle (§ 12).",
      30, 100, 250, 100, S_NOTE)
s.box("coord", "<b>Coordination</b> (code, sans LLM) · <b>seule à lire et à écrire la mémoire</b><br>"
               "Appelle chaque agent avec ses entrées, reçoit son résultat et le range ; vérifie les bornes avant chaque délégation (8 étapes, 10 s, 2 compléments), "
               "lance les contrôles dans l'ordre (1, 2, 2 bis sur le chemin des pièces, 3, 4), arrête dès qu'une règle du § 10 "
               "conclut, et conclut seule. "
               "Les agents ne s'appellent jamais entre eux.",
      400, 100, 1010, 80, S_ORCH)

s.box("grp", "", 320, 210, 1100, 225, S_GROUPE)
s.box("contrat", "<b>Contrôles déterministes</b> (cadre bleu) : un contrat fixe, entrée, sortie, erreurs. Réalisés en code ; "
                 "la réalisation peut changer sans toucher à la Coordination ni à la mémoire. <b>Cadre cyan</b> : un "
                 "modèle interprète, un schéma strict valide, le code décide.",
      1460, 395, 170, 185, S_NOTE)
agents = [
    ("ae", "<b>1 · Éligibilité</b> · <b>section : eligibilite</b><br>E1 contrat actif, E2 cotisations, E3 carence 30 j, "
           "E4 délai de déclaration, E5 garantie.<br><i>Règles simples : un statut, une date, une liste.</i>", 340),
    ("ap", "<b>2 · Pièces justificatives</b> · <b>section : pieces</b><br>Présence, lisibilité, type attendu ; "
           "adresse le complément confié par la Coordination.<br><i>Les images sont lues en amont, par le lecteur de "
           "pièces.</i>", 554),
    ("ac", "<b>2 bis · Documents et cohérence</b> · <b>section : coherence</b><br>Chemin des pièces (§ 5) : chaque "
           "pièce nette se rapporte-t-elle au sinistre déclaré ?<br><i>Le modèle interprète, le code rend le verdict ; "
           "appel lancé à l'arrivée.</i>", 768),
    ("aes", "<b>3 · Estimation</b> · <b>section : estimation</b><br>Montant justifié, retenu, estimé ; franchise ; "
            "plafond de la formule.<br><i>Calcul : jamais confié à un LLM.</i>", 982),
    ("af", "<b>4 · Anti-fraude</b> · <b>section : avis_fraude</b><br>Indicateurs F1 à F4 ; un seul appel au partenaire ; "
           "contrôle de sa réponse.<br><i>Seuils en code ; le jugement vient du partenaire.</i>", 1196),
]
for aid, texte, x in agents:
    s.box(aid, texte, x, 250, 206, 165, S_LECTEUR if aid == "ac" else S_AGENT)
    s.edge(f"d{aid}", "coord", aid, E_DELEG, "appel + entrées" if aid == "ae" else "",
           sortie=((x + 62 - 400) / 1010, 1), entree=(0.3, 0))
    s.edge(f"r{aid}", aid, "coord", E_DEP, "résultat" if aid == "ae" else "", sortie=(0.7, 0),
           entree=((x + 144 - 400) / 1010, 1))

s.box("mem", "Mémoire partagée de la demande : un objet par demande ; seule la Coordination la lit et l'écrit ; chaque section reçoit le résultat d'un seul agent",
      320, 450, 1100, 250, S_CONTENEUR + "verticalAlign=bottom;spacingBottom=6;align=right;spacingRight=12;")
for sid, texte, x in [("selig", "<b>eligibilite</b><br>résultat d'Éligibilité", 340),
                      ("spieces", "<b>pieces</b><br>résultat de Pièces, après chaque dépôt", 554),
                      ("scoh", "<b>coherence</b><br>hors des 5 sections métier", 768),
                      ("sestim", "<b>estimation</b><br>résultat d'Estimation", 982),
                      ("sfraude", "<b>avis_fraude</b><br>résultat d'Anti-fraude", 1196)]:
    s.box(sid, texte, x, 490, 206, 60, (S_LECTEUR if sid == "scoh" else S_AGENT) + CENTRE)
s.box("sissue", "<b>issue</b><br>décision ou escalade, motif", 335, 590, 260, 70, S_ORCH + CENTRE)
s.box("sctrl", "<b>hors de l'état</b><br>échéance de la demande, registre des appels (une exécution)", 605, 590, 260, 70, S_EXT)
s.box("sdem", "<b>demande</b><br>données reçues, lecture seule", 875, 590, 260, 70, S_EXT)
s.box("strace", "<b>trace</b>, ajout seul<br>agent, section remplie, durée, statut", 1145, 590, 260, 70, S_ORCH + CENTRE)
s.edge("wcoord", "coord", "mem", E_DEP, "", [(305, 164), (305, 525)], sortie=(0, 0.8), entree=(0, 0.3))

s.edge("e0", "lot", "coord", E_DEP, "une demande", sortie=(1, 0.4), entree=(0, 0.4))
s.box("espace", "<b>Espace assuré</b><br>reçoit la demande de complément ; renvoie les dépôts de l'assuré (§ 5)",
      30, 250, 240, 95, S_EXT)
s.edge("x0", "ap", "espace", E_EXT, "complément", [(595, 232), (285, 232), (285, 297)], sortie=(0.2, 0), entree=(1, 0.5))
s.box("part", "<b>Partenaire anti-fraude</b><br>agent externe, A2A<br>7 champs filtrés, 1 appel, au plus 3 s dans le temps restant<br>(chantier 2)",
      1460, 250, 170, 120, S_EXT)
s.edge("x1", "af", "part", E_EXT, "", sortie=(1, 0.35), entree=(0, 0.45))
s.box("metr", "<b>Métriques par agent</b><br>appels, échecs, latence, appels externes (interface.md)",
      1460, 590, 170, 90, S_EXT)
s.edge("x2", "strace", "metr", E_EXT, "", sortie=(1, 0.5), entree=(0, 0.4))

s.box("fiche", "<b>Fiche de décision</b> (§ 11)<br>construite depuis issue, avis_fraude, trace et arret", 335, 740, 260, 80, S_NOTE)
s.edge("o1", "sissue", "fiche", E_DEP, "", sortie=(0.5, 1), entree=(0.5, 0))
s.box("ok", "<b>Décision</b><br>acceptée (montant) ou refusée, avec un motif", 660, 745, 300, 70, S_FIN_OK)
s.box("esc", "<b>Escalade motivée</b> vers une file humaine<br>gestionnaire ou cellule_fraude", 1000, 745, 405, 70, S_FIN_ESC)
s.edge("o2", "fiche", "ok", E_OK, "", sortie=(1, 0.5), entree=(0, 0.5))
s.edge("o3", "fiche", "esc", E_ESC, "", [(630, 835), (1200, 835)], sortie=(1, 0.85), entree=(0.5, 1))
s.box("degr", "<b>Mode dégradé</b> (§ 9)<br>pas d'avis en 3 s : 1 500 € ou moins, la demande poursuit, marquée ; au-delà, cellule_fraude",
      1460, 700, 170, 130, S_FIN_ESC)
s.edge("o4", "degr", "esc", E_ESC, "> 1 500 €", sortie=(0, 0.5), entree=(1, 0.5))

s.box("pourquoi", "<b>Pourquoi des agents, si les contrôles sont des règles ?</b><br>"
                  "• Chaque agent rend un service sans montrer ses règles : si la carence passe de 30 à 45 jours, "
                  "seul l'agent Éligibilité change.<br>"
                  "• Une section, un propriétaire : la frontière se prouve dans la trace [E2].<br>"
                  "• Le modèle sert là où il faut interpréter un document : la lecture, et la cohérence avec la déclaration "
                  "(2 bis) ; aucune règle chiffrée ne lui est confiée.",
      30, 375, 260, 230, S_AMBIG)
s.box("comm", "<b>Comment ils communiquent</b><br>Aucun agent ne lit la mémoire. Agents internes : fonctions appelées par la Coordination, "
              "dans le même processus. Partenaire : A2A, par le réseau. Un contrôle tenu par un autre service passerait "
              "par une API ou une interface d'agent.",
      30, 615, 260, 175, S_NOTE)

s.legende([(VERT, "Coordination et ses sections"), (BLEU, "Agent de contrôle et sa section"),
           (CYAN, "Agent avec modèle et sa section"), (ORANGE, "Choix d'architecture"), (GRIS, "Externe ou chantier 2"), (ESC, "Escalade")], 30, 875)
s.box("lg2", "Pointillé vert : appel avec ses entrées · trait plein : résultat rendu, ou lecture et rangement de la mémoire par la Coordination · pointillé gris : échange avec l'extérieur",
      30, 911, 900, 20, S_SOUS)
s.ecrire("schema-A-architecture-generale", "Architecture générale", 1660, 945)
