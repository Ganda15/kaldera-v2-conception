# Chantier 1 : l'équipe et son orchestration

Ce que le brief attend pour ce chantier : la carte des agents (rôles, frontières dont le point ambigu tranché, dépendances, parallélisme), le schéma d'orchestration (délégations, conditions d'arrêt, bornes provisoires) et le modèle de la mémoire partagée.

Exigences concernées : E1, E2 et E6, plus E3 pour les champs sensibles de la mémoire. Le détail des exigences est dans le [README](README.md).

## 1. Le choix d'architecture

- [ ] Un seul agent avec 10 à 15 outils au maximum suffirait-il ? Sinon, pourquoi ? [E2]
- [ ] Les étapes sont-elles connues d'avance, et dans quel ordre s'enchaînent-elles ?
- [ ] Les sous-tâches sont-elles connues d'avance, et sont-elles indépendantes ?
- [ ] Un seul spécialiste suffit-il pour chaque demande, ou faut-il en combiner plusieurs ?
- [ ] Faut-il un contrôle central et traçable ? [E1]
- [ ] Qui décide de la suite : le code, une boucle, un superviseur, ou les agents se vérifient-ils eux-mêmes ? [E1] [E6]
- [ ] Quelles parties du système doivent être écrites en code plutôt que confiées à un LLM ?

Repère. Le code est prévisible et rend l'arrêt facile à garantir, mais il est peu flexible. Un LLM est flexible, mais il ne garantit rien. Or les six exigences sont des garanties absolues (« jamais », « aucun », « rien d'autre »). Le découpage courant en découle : l'orchestration, les bornes, les droits d'écriture dans la mémoire, le filtre sortant et la validation des réponses A2A sont écrits en code ; le LLM n'intervient qu'à l'intérieur des agents spécialistes, là où il faut lire du texte libre.

## 2. La carte des agents [E2]

### Rôles et frontières

- [ ] Quels sont exactement les agents ? Éligibilité, pièces justificatives, estimation, fraude et orchestrateur : faut-il en ajouter un pour la décision finale ou la rédaction du motif ?
- [ ] Pour chaque agent : que peut-il faire, et que ne doit-il surtout pas faire ?
- [ ] Pour chaque agent : que reçoit-il, que renvoie-t-il, et quelles erreurs peut-il renvoyer ?
- [ ] Quels garde-fous chaque agent doit-il contenir ?
- [ ] Les outils sont-ils partagés entre agents, ou chacun a-t-il les siens ?
- [ ] Qui rend la décision finale, et qui rédige le motif ?
- [ ] Comment prouver par un test qu'un agent ne sort pas de son rôle ?

### Le point ambigu

Le brief demande de le trancher, et il sera questionné à la validation du dossier.

- [ ] Quel est le point ambigu entre deux agents, et qui en est le seul responsable ?
- [ ] Qui déclenche la « suspicion de fraude » qui mène à l'appel du partenaire ?

Candidats à examiner :

| Responsabilité | Agents qui peuvent la revendiquer |
|---|---|
| Déclarer une suspicion de fraude | Pièces (une incohérence), estimation (un montant aberrant), fraude |
| Rejeter une demande dont les pièces manquent | Pièces, éligibilité, orchestrateur |
| Appliquer le plafond du contrat | Estimation, éligibilité |

Le choix se justifie par `specs_metier.md`. Seul repère donné par le brief : « l'éligibilité ne fait pas d'estimation, l'estimation ne juge pas la fraude ».

### Dépendances et parallélisme

Le brief range ces deux points dans la carte des agents.

- [ ] Quelles étapes dépendent les unes des autres, et lesquelles peuvent s'exécuter en parallèle ?
- [ ] Quand deux résultats obtenus en parallèle se contredisent (par exemple : éligible, mais pièces incomplètes), quelle règle l'emporte ?

### Tableau à remplir : la carte des agents

| Agent | Rôle | Reçoit | Renvoie | Ne fait jamais | Code ou LLM |
|---|---|---|---|---|---|
| Orchestrateur | | | | | |
| Éligibilité | | | | | |
| Pièces justificatives | | | | | |
| Estimation | | | | | |
| Fraude (liaison avec le partenaire) | | | | | |

## 3. L'orchestration et la terminaison garantie [E1] [E6]

- [ ] Comment l'orchestrateur délègue-t-il chaque étape, et qui choisit l'étape suivante ?
- [ ] Comment l'orchestrateur garantit-il que chaque demande se termine par une décision ou une escalade humaine motivée ?
- [ ] Quels sont les états finaux possibles ? La machine à états doit montrer que chaque chemin y mène.
- [ ] Comment borne-t-on les boucles : condition de sortie, nombre de tours maximum, état « Done », artefact de sortie ?
- [ ] Quelles bornes provisoires au départ, et sur quelle base les choisit-on ?
- [ ] Que se passe-t-il quand une borne est atteinte ? Jamais un arrêt silencieux : une escalade dont le motif nomme la borne.
- [ ] Qu'est-ce qu'une escalade « motivée » : quel motif, quelles étapes déjà faites, quelles preuves, et à qui l'envoie-t-on ?
- [ ] Que se passe-t-il quand un agent interne plante, renvoie un format invalide ou dépasse son délai ?
- [ ] Quelle gestion d'erreur observable met-on en place dans le workflow ?

### Tableau à remplir : les bornes provisoires

Les valeurs de départ sont provisoires. Le plan d'épreuve du chantier 2 les confirme ou les ajuste, et chaque ajustement entre dans le journal (voir [chantier 2, section 8](chantier-2-a2a-epreuve.md)).

| Borne | Valeur de départ | Justification | Scénario d'épreuve qui la teste |
|---|---|---|---|
| Étapes d'orchestration par demande | | | Piège à boucle |
| Appels par agent et par demande | | | Piège à boucle |
| Allers-retours entre deux agents | | | Piège à boucle |
| Délai global par demande | | | Partenaire lent |
| Détection d'un état déjà vu | | | Piège à boucle |
| Budget de tokens ou de coût par demande | | | Cas nominal |

## 4. La mémoire partagée

Le brief demande une mémoire partagée de la demande, avec un état commun et un accès maîtrisé.

- [ ] Que contient l'état partagé de la demande ? Par exemple : l'identifiant, les données de la demande, le résultat de chaque agent, l'étape en cours, les compteurs, l'historique, le statut final et le motif d'escalade.
- [ ] Sous quelle forme la mémoire partagée est-elle implémentée : objet en mémoire, base de données, fichier ?
- [ ] Accès maîtrisé : qui lit et qui écrit quels champs ? L'estimation doit-elle voir le score de fraude ?
- [ ] Que se passe-t-il si deux agents qui tournent en parallèle écrivent en même temps ?
- [ ] Peut-on reprendre une demande après un crash, sans la bloquer de nouveau ?
- [ ] Quels champs de la mémoire ne doivent jamais partir chez le partenaire ? [E3]
- [ ] Où range-t-on les identifiants de la tâche A2A (`taskId`, `contextId`), pour pouvoir suivre ou annuler une tâche chez le partenaire même après un crash ?

### Tableau à remplir : les droits sur la mémoire

| Section de l'état | Écrite par | Lue par |
|---|---|---|
| Données de la demande | | |
| Résultat de l'éligibilité | | |
| Résultat des pièces | | |
| Résultat de l'estimation | | |
| Résultat de la fraude | | |
| Identifiants de la tâche A2A | | |
| Étape en cours, compteurs, statut final, motif d'escalade | | |
| Journal d'événements | | |

## 5. L'observabilité, à préparer dès maintenant [E6]

Le monitorage se code au chantier 2. Le journal d'événements, lui, vit dans la mémoire partagée : s'il n'est pas prévu ici, il n'y aura rien à mesurer plus tard.

- [ ] Quel événement enregistre-t-on à chaque étape : qui, quoi, quand, combien de temps, avec quel résultat ?
- [ ] Quelles métriques par agent en découlent ?
- [ ] Quels éléments observe-t-on au niveau de l'équipe et de son orchestration ?
- [ ] Comment montrer qu'une demande a suivi le bon chemin, avec une trace rejouable par demande ?

## Schémas à produire pour ce chantier

- La carte des agents : rôles, frontières, point ambigu tranché, dépendances, parallélisme.
- Le schéma d'orchestration et sa machine à états : délégations, conditions d'arrêt, bornes provisoires.
- Le modèle de la mémoire partagée : sections, droits de lecture et d'écriture, journal d'événements.
