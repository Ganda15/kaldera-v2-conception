# Kaldera V2 : préparation de la conception

Préparation du dossier de conception du brief « Kaldera, développer une équipe d'agents de bout en bout » (Simplon × Wild Code School, formation Développeur IA, RNCP 37827).

Le dépôt rassemble les questions que le dossier de conception doit trancher, rangées par chantier, avec les points de vigilance repérés et les tableaux à remplir. Il ne contient pas encore les réponses : la plupart dépendent de `specs_metier.md`, de `eval/scenarios.jsonl` et des tests d'acceptance, qui n'ont pas encore été fournis.

## Démarche

Les questions de réflexion ont été discutées en groupe pendant la séance du 05/10/2026. Cette préparation et les réponses du dossier de conception sont individuelles.

## Organisation

| Fichier | Contenu |
|---|---|
| [chantier-1-equipe-orchestration.md](chantier-1-equipe-orchestration.md) | Chantier 1 : le produit d'abord (existant, besoin, attendu), choix du pattern par arbre de décision, carte des agents avec contrats et garde-fous, orchestration, mémoire partagée, observabilité et plan de preuve |
| [chantier-2-a2a-epreuve.md](chantier-2-a2a-epreuve.md) | Chantier 2 : protocole et contrat A2A, filtre des données, validation des réponses, mode dégradé, plan d'épreuve, journal des ajustements |
| [schemas/](schemas/) | Schémas du chantier 1, en `.drawio` (modifiable) et en `.png` |
| [scripts/](scripts/) | Générateur des schémas (`make_schemas_ch1.py`) et de leur légende en puces |

## Les six exigences de la direction des opérations

| | Exigence |
|---|---|
| E1 | Toute demande se termine par une décision ou une escalade humaine motivée, jamais par un blocage silencieux |
| E2 | Chaque agent a un rôle et une frontière définis ; aucun agent n'empiète sur le rôle d'un autre |
| E3 | Seules les données prévues au contrat partent chez le partenaire anti-fraude, rien d'autre |
| E4 | Une réponse du partenaire non conforme au contrat est rejetée, jamais propagée telle quelle |
| E5 | Partenaire indisponible : le mode dégradé défini par le métier s'applique (la demande continue ou est routée, selon `specs_metier.md`) |
| E6 | Aucune boucle infinie ; les métriques par agent (latence, échecs, recours à l'externe) sont visibles ; tout ajustement de l'orchestration provoqué par un scénario d'épreuve est consigné |

Les six sont des garanties absolues. Aucune ne peut reposer sur la seule bonne volonté d'un LLM : chacune doit être tenue par du code et prouvée par un test.

## Couverture des schémas attendus par le brief

| Schéma attendu | Où il se prépare |
|---|---|
| Questions produit (existant, besoin, attendu) et choix du pattern | Chantier 1, sections 1 et 2 |
| Carte des agents : rôles, frontières (point ambigu tranché), dépendances, parallélisme | Chantier 1, section 3 |
| Schéma d'orchestration : délégations, conditions d'arrêt, bornes provisoires | Chantier 1, section 4 |
| Modèle de la mémoire partagée | Chantier 1, sections 5 et 6 |
| Schéma d'échange A2A : contrat, filtre de données, validation des réponses, chemin de mode dégradé | Chantier 2, sections 1 à 5 |
| Plan d'épreuve : scénarios d'intégration × signaux observés × ajustement possible du chantier 1 | Chantier 2, sections 6 à 8 |

## Mode d'emploi

- Écrire la réponse sous chaque question, puis cocher la case.
- `[E1]` à `[E6]` renvoient aux exigences ci-dessus.
- Une réponse qui dépend de `specs_metier.md` reste marquée « provisoire » tant que ce fichier n'a pas été lu.

## État

- [ ] `specs_metier.md`, `eval/scenarios.jsonl` et tests d'acceptance reçus
- [ ] Réponses du chantier 1
- [ ] Réponses du chantier 2
- [x] Schémas du chantier 1 : arbre de décision, carte des agents, orchestration, mémoire partagée (proposition provisoire)
- [ ] Schémas du chantier 2 : échange A2A et mode dégradé, plan d'épreuve
- [ ] Dossier validé par le formateur, avant tout code

## Questions pour le formateur

1. Où trouver `specs_metier.md`, `eval/scenarios.jsonl` et les tests d'acceptance ?
2. Le partenaire anti-fraude est-il fourni sous forme de bouchon, ou faut-il le simuler ?
3. Quelle version du protocole A2A le partenaire suit-il : 0.3.0 ou 1.0.0 ?
4. Le contrat réel du partenaire est-il fourni (champs, délais, règles de relance, fréquence de consultation) ?
5. La pile technique est-elle libre ? Un composant à base de règles compte-t-il comme un agent ?
6. Les demandes déjà bloquées depuis des semaines font-elles partie du périmètre ?
7. Les questions guides des deux chantiers sont vides sur la page du brief : sont-elles à venir ?
8. Quelles sont les échéances du dossier de conception et du code ?

## Sources

- Brief « Kaldera, développer une équipe d'agents de bout en bout », Simplonline (accès restreint)
- Spécification A2A, dernière version publiée (1.0.0) : [a2a-protocol.org/latest/specification](https://a2a-protocol.org/latest/specification/)
- Spécification A2A 0.3.0 : [a2a-protocol.org/v0.3.0/specification](https://a2a-protocol.org/v0.3.0/specification/)
- Schéma JSON officiel de la version 0.3.0 : [a2aproject/A2A, specification/json/a2a.json](https://github.com/a2aproject/A2A/blob/v0.3.0/specification/json/a2a.json)

## Lexique

- **A2A (Agent-to-Agent)** : protocole qui permet à deux agents de systèmes différents d'échanger selon un format commun.
- **Agent Card** : fiche publiée par un agent A2A ; elle décrit ses compétences, la version du protocole suivie et le mode d'authentification.
- **Bouchon (mock)** : faux partenaire réglable, utilisé pour simuler un partenaire lent, en panne ou menteur.
- **Borne** : limite dure (nombre d'étapes, d'appels, durée) qui arrête une boucle.
- **Contrat d'échange** : format exact et liste fermée des champs que les deux parties s'engagent à échanger.
- **Escalade motivée** : transfert d'une demande à un humain, avec le motif, l'étape atteinte, les données disponibles et les tentatives faites.
- **Mode dégradé** : chemin de repli défini par le métier quand le partenaire est indisponible.
- **Plan d'épreuve** : tableau qui associe à chaque scénario rejoué les signaux à observer et l'ajustement du chantier 1 qu'il peut provoquer.
