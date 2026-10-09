# Schéma E de Kaldera V2 : la lecture des pièces (phase E), du document non structuré au JSON de la spec § 3.
# Ajouté le 08/10/2026 : l'entrée réelle est un dossier de pièces (contrat PDF, photos de factures), et non un JSON.
# Fondé sur le code du dépôt kaldera-bout-en-bout_v2 : src/kaldera/extraction/lecteurs.py et dossier.py.
# Mis à jour le 08/10/2026 (nuit) : agent Documents et cohérence (src/kaldera/agents/coherence.py), appel lancé à
# l'arrivée du dossier.
# Palette, styles et classe Schema : schema_commun.py.

from schema_commun import *  # noqa: F403 (palette, styles, Schema)

s = Schema()
s.box("t", "Kaldera V2 · Lecture des pièces : du document au JSON de la spec § 3 · Phase E", 30, 20, 1300, 30, S_TITRE)
s.box("st", "Les agents de lecture lisent et extraient, ils ne décident jamais. Le code teste d'abord ce qu'il sait "
            "tester ; le modèle ne lit que ce que le code ne sait pas lire ; sa réponse passe par un schéma strict. "
            "En bas, ajouté le 08/10 : l'appel de cohérence (§ 5), lancé dès l'arrivée, en parallèle.",
      30, 54, 1540, 22, S_SOUS)

# --- le dossier de l'assuré ---
s.box("dos", "Dossier de l'assuré (dossiers/KAL-26-0101)", 30, 95, 300, 600, S_CONTENEUR)
s.box("f_decl", "<b>declaration.json</b><br>formulaire : référence, assuré, sinistre, historique, numéro de contrat "
                "déclaré", 45, 135, 270, 80, S_NOTE)
s.box("f_ctr", "<b>contrat.pdf</b><br>texte, 3 mises en page", 45, 230, 270, 60, S_NOTE)
s.box("f_fac", "<b>piece-1-facture.png</b><br>photo d'une facture", 45, 365, 270, 60, S_NOTE)
s.box("f_pho", "<b>piece-2-photo.png</b>, <b>…-depot_plainte.png</b><br>le type vient du créneau choisi par "
               "l'assuré", 45, 440, 270, 80, S_NOTE)
s.box("f_dep", "<b>depots/1-facture.png</b><br>dépôts de l'espace assuré (compléments)", 45, 535, 270, 65, S_NOTE)
s.box("f_n", "34 dossiers générés depuis les 34 demandes des scénarios : 34 PDF, 68 images (2 illisibles), 35 JSON.",
      45, 615, 270, 70, S_SOUS)

# --- lecteur de contrat ---
s.box("gc", "Lecteur de contrat · lecteurs.lire_contrat · reçoit un PDF", 360, 95, 880, 200, S_GROUPE)
s.box("c1", "<b>1 · Code</b><br>PyMuPDF extrait le texte du PDF, quelle que soit sa mise en page", 380, 130, 230, 95,
      S_ORCH)
s.box("c2", "<b>2 · Modèle</b> gpt-5.4 (Azure AI Foundry)<br>consigne, phrase de garde, texte entre balises<br>"
            "→ schéma strict <b>ContratLu</b> : formule et statut en liste fermée, date valide, aucun champ en plus",
      640, 130, 300, 145, S_LECTEUR)
s.box("dnum", "Numéro lu =<br>numéro déclaré ?", 980, 135, 220, 110, S_LOSANGE)
s.box("esc_num", "<b>Escalade gestionnaire</b><br>contrat lu différent du contrat déclaré : aucun contrôle lancé "
                 "(escalade_directe)", 1270, 140, 300, 100, S_FIN_ESC)
s.edge("e_c", "f_ctr", "c1", E_DEP, "", sortie=(1, 0.5), entree=(0, 0.5))
s.edge("c12", "c1", "c2", E_DEP, "texte", sortie=(1, 0.5), entree=(0, 0.33))
s.edge("c23", "c2", "dnum", E_DEP, "", sortie=(1, 0.4), entree=(0, 0.5))
s.edge("cnon", "dnum", "esc_num", E_ESC, "non", sortie=(1, 0.5), entree=(0, 0.5))
s.edge("coui", "dnum", "p1", E_OK, "oui : on lit les pièces", [(1090, 307), (495, 307)], sortie=(0.5, 1),
       entree=(0.5, 0))

# --- lecteur de pièces ---
s.box("gp", "Lecteur de pièces · lecteurs.lire_piece · reçoit une image et son type", 360, 320, 1210, 390, S_GROUPE + "align=right;spacingRight=12;")
s.box("p1", "<b>1 · Code</b><br>netteté de l'image (moyenne des contours) ; seuil 3,5, mesuré sur les 68 images",
      380, 355, 230, 95, S_ORCH)
s.box("dnet", "Nette ?", 640, 350, 170, 105, S_LOSANGE)
s.box("p_flou", "<b>illisible</b><br>sans appel au modèle ; aussi une image qui ne s'ouvre pas", 640, 485, 170, 90,
      S_NOTE)
s.box("dtype", "Facture ?", 840, 350, 170, 105, S_LOSANGE)
s.box("p_autre", "photo, dépôt de plainte :<br><b>lisible</b> ; le contenu est vérifié par la cohérence, en bas",
      840, 485, 170, 85, S_NOTE)
s.box("p2", "<b>2 · Modèle</b><br>l'image et la phrase de garde → schéma strict <b>FactureLue</b> : lisible, "
            "montant TTC", 1052, 340, 176, 125, S_LECTEUR)
s.box("ddoute", "Lisible, montant<br>présent, positif ?", 1040, 490, 200, 110, S_LOSANGE)
s.box("p_ok", "<b>lisible</b> et montant, arrondi au centime", 1290, 515, 260, 60, S_NOTE)
s.box("p_dout", "<b>illisible</b> : dans le doute, jamais un montant inventé", 1040, 625, 200, 70, S_NOTE)
for k, (fid, entree) in enumerate((("f_fac", 0.3), ("f_pho", 0.6), ("f_dep", 0.9))):
    s.edge(f"e_p{k}", fid, "p1", E_DEP, "", sortie=(1, 0.5), entree=(0, entree))
s.edge("p1n", "p1", "dnet", E_DEP, "", sortie=(1, 0.5), entree=(0, 0.5))
s.edge("nnon", "dnet", "p_flou", E_DEP, "non", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("noui", "dnet", "dtype", E_DEP, "oui", sortie=(1, 0.5), entree=(0, 0.5))
s.edge("tnon", "dtype", "p_autre", E_DEP, "non", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("toui", "dtype", "p2", E_DEP, "oui", sortie=(1, 0.5), entree=(0, 0.5))
s.edge("p2d", "p2", "ddoute", E_DEP, "", sortie=(0.5, 1), entree=(0.5, 0))
s.edge("doui", "ddoute", "p_ok", E_OK, "oui", sortie=(1, 0.5), entree=(0, 0.5))
s.edge("dnon", "ddoute", "p_dout", E_DEP, "non", sortie=(0.5, 1), entree=(0.5, 0))

# --- sorties : panne, demande § 3, chaîne de décision ---
s.box("panne", "<b>Modèle en panne, délai ou réponse hors schéma</b> → ExtractionImpossible<br>"
               "<b>Escalade gestionnaire</b> motivée, aucun contrôle lancé. Une panne n'est pas la faute de l'assuré : "
               "on ne lui demande pas de complément.", 360, 735, 560, 105, S_FIN_ESC)
s.box("json", "<b>Demande au format § 3</b><br>contrat lu, pièces et dépôts lus, formulaire ; identique à ce que "
              "reçoit le chemin JSON", 950, 735, 300, 105, S_NOTE)
s.box("chaine", "<b>Chaîne de décision</b><br>coordination.traiter : Éligibilité, Pièces, Cohérence (2 bis), "
                "Estimation, Anti-fraude, règles § 10, fiche de décision", 1280, 735, 290, 105, S_ORCH)
s.edge("gpan", "gp", "panne", E_ESC, "lecture impossible (contrat ou facture)", sortie=(0.15, 1), entree=(0.3232, 0))
s.edge("gjs", "gp", "json", E_DEP, "contrat, pièces et dépôts lus", sortie=(0.5496, 1), entree=(0.25, 0))
s.edge("form", "dos", "json", E_DEP, "formulaire (declaration.json)", [(315, 875), (1100, 875)], sortie=(0.95, 1),
       entree=(0.5, 1))
# --- contrôles d'entrée, avant toute lecture (exigence N1, ajoutés le 08/10/2026) ---
s.box("entree", "<b>Avant toute lecture : escalade gestionnaire</b> motivée si le formulaire est absent ou illisible, "
                "le contrat absent, corrompu ou sans texte, ou un fichier non reconnu. Jamais d'erreur brute.",
      30, 735, 270, 105, S_FIN_ESC)
s.edge("dent", "dos", "entree", E_ESC, "", sortie=(0.4, 1), entree=(0.44, 0))
s.edge("jch", "json", "chaine", E_DEP, "", sortie=(1, 0.5), entree=(0, 0.5))

# --- l'agent Documents et cohérence : appel lancé dès l'arrivée, résultat attendu par la Coordination ---
s.box("gk", "Agent Documents et cohérence · agents/coherence.py · appel lancé dès l'arrivée du dossier, en parallèle des "
            "deux lecteurs, sur le même budget de 10 s", 360, 900, 1210, 150, S_GROUPE)
s.box("k1", "<b>1 · Code</b><br>les images nettes du dossier (pièces et dépôts, même mesure de netteté) et la "
            "déclaration", 380, 935, 230, 95, S_ORCH)
s.box("k2", "<b>2 · Modèle</b>, un seul appel<br>toutes les images et la déclaration (type, date, description), entre "
            "balises → schéma strict <b>Interpretation</b> : par pièce, nature, sinistre évoqué, date, concordance",
      640, 930, 330, 105, S_LECTEUR)
s.box("k3", "<b>3 · Code</b><br>écarts explicites : autre sinistre, facture de travaux antérieure au sinistre → "
            "cohérent, contradiction, insuffisant ou non effectué", 1000, 935, 270, 95, S_ORCH)
s.box("k4", "<b>verdict</b>, attendu par la Coordination après un contrôle des pièces complet ; jamais utilisé : "
            "noté avec son coût (non_utilise)", 1300, 935, 255, 95, S_NOTE)
s.edge("k01", "dos", "k1", E_DEP, "", [(345, 683), (345, 982)], sortie=(1, 0.98), entree=(0, 0.5))
s.edge("k12", "k1", "k2", E_DEP, "", sortie=(1, 0.5), entree=(0, 0.5))
s.edge("k23", "k2", "k3", E_DEP, "", sortie=(1, 0.5), entree=(0, 0.5))
s.edge("k34", "k3", "k4", E_DEP, "", sortie=(1, 0.5), entree=(0, 0.5))
s.edge("k4c", "k4", "chaine", E_DEP, "verdict", sortie=(0.5, 0), entree=(0.5, 1))

# --- garde-fous et mesure ---
s.box("garde", "<b>Garde-fous</b><br>• Le texte d'un document est une donnée, jamais une consigne : phrase de garde "
               "dans chaque consigne, document entre balises.<br>• Clé dans .env, jamais dans le code ni dans Git ; "
               "aucune relance automatique.<br>• Un seul budget de 10 s par demande, lecture comprise : chaque appel au modèle "
               "reçoit le temps restant comme délai ; à court de temps, escalade technique. Lecture tracée à part.<br>"
               "• Cohérence : pièces et déclaration entre balises, jamais des consignes ; le modèle interprète, le code rend "
               "le verdict ; une contradiction va à une personne, jamais à un refus.", 30, 1075, 760, 150, S_NOTE)
s.box("mesure", "<b>Mesure E4</b> relancée (08/10/2026, commit 5cb2a4e, 34 dossiers, gpt-5.4)<br>100 % sur chaque "
                "champ (5 du contrat, 33 montants, 68 lisibilités) · 0 lecture impossible · 32/34 décisions identiques au "
                "chemin JSON : les 2 écarts viennent de la cohérence (factures d'incendie jugées incertaines) · moyenne : "
                "contrat 1,69 s, facture 2,10 s, cohérence 3,97 s · 85 719 jetons en entrée, 8 300 en sortie.<br>"
                "<b>Cohérence</b> (essai 4, 42 dossiers étiquetés) : 6/6 contradictions, 0 fausse alerte, 2 examens "
                "inutiles sur 34, 1 échec technique (budget dépassé).<br>"
                "<i>Limites : documents de synthèse ; 2 images illisibles seulement ; photos factices.</i>",
      810, 1075, 760, 150, S_AMBIG)

s.legende([(VERT, "Code, sans modèle"), (CYAN, "Modèle, schéma strict"), (OK, "Suite normale"),
           (ESC, "Escalade gestionnaire"), (ORANGE, "Mesure")], 30, 1250)
s.box("lg2", "Losange : test en code · note : résultat de lecture · « illisible » mène à une demande de complément "
             "(règle 2) ; une panne mène à une escalade, jamais à une demande faite à l'assuré",
      30, 1286, 1400, 20, S_SOUS)
s.ecrire("schema-E-lecture-des-pieces", "Lecture des pièces", 1600, 1320)
