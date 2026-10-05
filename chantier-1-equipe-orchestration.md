# Chantier 1 : l'équipe et son orchestration

Ce que le brief attend pour ce chantier : la carte des agents (rôles, frontières dont le point ambigu tranché, dépendances, parallélisme), le schéma d'orchestration (délégations, conditions d'arrêt, bornes provisoires) et le modèle de la mémoire partagée.

Exigences concernées : E1, E2 et E6, plus E3 pour les champs sensibles de la mémoire. Le détail des exigences est dans le [README](README.md).

Ordre de travail : le produit d'abord (section 1), puis le choix du pattern (section 2), puis l'équipe elle-même (sections 3 à 6). Une architecture choisie avant de connaître le produit risque d'optimiser ce qui n'a pas besoin de l'être.

## 1. Le produit avant les agents

Avant de concevoir l'équipe, on interroge le client sur trois axes : l'existant, le besoin, l'attendu. Challenger ses choix permet de comprendre les vraies contraintes et d'éviter des optimisations inutiles. Sous chaque question, la décision de conception qu'elle permet de prendre.

### L'existant

- [ ] Le système actuel a-t-il déjà fonctionné correctement ? Si oui, depuis quand dérive-t-il, et quelles métriques ou traces montrent le changement ?
  *Décide : la référence de départ, à laquelle comparer la nouvelle équipe.*
- [ ] Quelles métriques et quelles traces existent aujourd'hui (journaux, tableaux de bord, suivi LLMOps ou MLOps) ?
  *Décide : ce qui peut être réutilisé pour l'observabilité.*
- [ ] Pourquoi l'agent généraliste a-t-il été construit ainsi ? Quels choix ont été faits, et pour quelles raisons ?
  *Décide : les contraintes cachées à garder ou à lever.*
- [ ] Combien de demandes arrivent par jour, avec quels pics ? Combien sont bloquées aujourd'hui, et à quelle étape ?
  *Décide : le parallélisme, les bornes, les priorités.*
- [ ] Peut-on suivre une vraie demande de bout en bout ? Où attend-elle ?
  *Décide : les étapes réelles et l'endroit des escalades.*

### Le besoin

- [ ] Un système agentique est-il justifié, face à un traitement humain ou à un système déterministe plus simple ? Pour quelles étapes ?
  *Décide : où un LLM sert vraiment (question Q0 de l'arbre de décision, section 2).*
- [ ] Le partenaire anti-fraude externe est-il indispensable, ou remplaçable par un contrôle maison ?
  *Décide : la place de l'échange A2A et du mode dégradé (chantier 2).*
- [ ] Les règles métier sont-elles écrites (éligibilité, plafonds, pièces exigées) ? Qui les change, et à quelle fréquence ?
  *Décide : règles écrites en code, ou placées dans une configuration.*
- [ ] Un refus entièrement automatique est-il permis, ou un humain doit-il confirmer chaque refus ?
  *Décide : les états finaux. Le RGPD (article 22) encadre les décisions fondées uniquement sur un traitement automatisé ; à confirmer avec le service juridique du client.*
- [ ] Qu'est-ce qui coûte le plus : payer une fraude, ou refuser à tort une demande valide ?
  *Décide : la sévérité du contrôle de fraude et le seuil d'escalade.*
- [ ] Qui traite les escalades, et combien peut-il en absorber par jour ?
  *Décide : le taux d'escalade acceptable, donc la sévérité des bornes.*

### L'attendu

- [ ] Quel délai de décision vise-t-on pour une demande ?
  *Décide : le délai global par demande.*
- [ ] Dans trois mois, quel chiffre dira que le système fonctionne : délai de décision, part de demandes bloquées, part d'escalades, réclamations ?
  *Décide : les métriques suivies et les seuils des tests.*
- [ ] Quelles décisions et quelles traces faut-il conserver, combien de temps, et qui les audite ?
  *Décide : le contenu du journal d'événements et sa durée de conservation.*

Documents à demander au client : `specs_metier.md`, le contrat du partenaire, quelques demandes réelles anonymisées (dont des demandes restées bloquées) et les journaux d'une semaine difficile. Les demandes réelles deviendront des scénarios du plan d'épreuve.

## 2. Le choix du pattern : l'arbre de décision

Les questions se posent dans l'ordre, et chaque réponse élimine une option. Q0 vient de l'axe « besoin » de la section 1 ; Q1 à Q5 portent sur l'architecture. Les réponses sont provisoires en attendant `specs_metier.md` (voir le schéma 0).

| # | Question | Réponse provisoire | Ce qu'elle écarte ou ajoute |
|---|---|---|---|
| Q0 | Un système agentique est-il justifié, face à un humain ou à des règles simples ? | En partie : seulement pour lire le texte libre des pièces | Écarte : tout confier à un LLM. L'éligibilité et les plafonds restent des règles en code |
| Q1 | Un seul agent avec 10 à 15 outils suffit-il ? | Non | Écarte : l'agent unique, dont les rôles ne peuvent pas être prouvés séparément (E2) ; c'est le défaut de l'agent actuel |
| Q2 | Les étapes sont-elles connues d'avance, et dans quel ordre ? | Oui : éligibilité et pièces, puis estimation, fraude, décision | Écarte : un planificateur LLM qui invente les étapes. Le routage se fait par règles, testables et bornables |
| Q3 | Des sous-tâches peuvent-elles s'exécuter en parallèle ? | Oui : éligibilité et pièces | Retient : ces deux étapes en parallèle, puis le regroupement de leurs résultats |
| Q4 | Faut-il un contrôle central qui garantit une décision ou une escalade pour chaque demande ? | Oui | Écarte : des agents qui se passent la main sans contrôle central ; personne ne garantirait alors la fin de chaque demande (E1) |
| Q5 | Quelles métriques par agent faut-il rendre visibles ? | Latence, échecs, appels au partenaire | Ajoute : un journal d'événements à chaque étape, source des métriques (E6) |

Pattern retenu : un orchestrateur central écrit en code (pattern superviseur) et quatre agents spécialistes ; éligibilité et pièces en parallèle ; un LLM seulement pour lire le texte libre des pièces ; un journal d'événements à chaque étape.

La tension à arbitrer : le code déterministe est prévisible mais peu flexible ; un système tout agentique est flexible mais difficile à garantir. Les six exigences sont des garanties absolues (« jamais », « aucun », « rien d'autre »). D'où le choix : un squelette en code (orchestration, bornes, droits sur la mémoire, filtre sortant, validation des réponses A2A), et le LLM seulement à l'intérieur des agents qui lisent du texte libre.

Questions associées :

- [ ] Un seul spécialiste suffit-il pour chaque demande, ou faut-il en combiner plusieurs ?
- [ ] Qui décide de la suite : le code, une boucle, un superviseur, ou les agents se vérifient-ils eux-mêmes ? [E1] [E6]

## 3. La carte des agents [E2]

### Rôles et frontières

- [ ] Quels sont exactement les agents ? Éligibilité, pièces justificatives, estimation, fraude et orchestrateur : faut-il en ajouter un pour la décision finale ou la rédaction du motif ?
- [ ] Pour chaque agent : que peut-il faire, et que ne doit-il surtout pas faire ?
- [ ] Les outils sont-ils partagés entre agents, ou chacun a-t-il les siens ?
- [ ] Qui rend la décision finale, et qui rédige le motif ?
- [ ] Comment prouver par un test qu'un agent ne sort pas de son rôle ?

### Le contrat de chaque agent

Il s'agit du contrat interne entre agents, distinct d'un contrat d'API : l'entrée, la sortie, les erreurs possibles et une docstring qui dit en une phrase le rôle et la frontière de l'agent.

- [ ] Pour chaque agent : quelle entrée, quelle sortie, quelles erreurs, et quelle docstring ?

Exemple provisoire, pour l'agent Éligibilité :

```python
def verifier_eligibilite(demande: Demande, contrat: Contrat) -> ResultatEligibilite:
    """Dit si le contrat couvre la demande, avec le motif.

    Ne calcule aucun montant, ne juge ni les pièces ni la fraude.
    Erreurs : ContratIntrouvable, DonneesIncompletes.
    """
```

| Agent | Entrée | Sortie | Erreurs possibles | Docstring (une phrase) |
|---|---|---|---|---|
| Éligibilité | Demande, contrat | Éligible oui ou non, motif | Contrat introuvable, données incomplètes | Dit si le contrat couvre la demande, avec le motif |
| Pièces justificatives | | | | |
| Estimation | | | | |
| Fraude (liaison avec le partenaire) | | | | |
| Orchestrateur | | | | |

### Garde-fous et métriques de bon fonctionnement, par agent

- [ ] Quels garde-fous chaque agent doit-il contenir ?
- [ ] Quelle métrique dit qu'il fonctionne bien ?

Exemple : pour l'agent Pièces, le texte des justificatifs vient du client ; il est traité comme une donnée et filtré avant d'entrer dans un prompt, sinon une pièce piégée pourrait donner des ordres à l'agent.

| Agent | Garde-fou | Métrique de bon fonctionnement |
|---|---|---|
| Éligibilité | | |
| Pièces justificatives | | |
| Estimation | | |
| Fraude (liaison avec le partenaire) | | |
| Orchestrateur | | |

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

## 4. L'orchestration et la terminaison garantie [E1] [E6]

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

## 5. La mémoire partagée

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

## 6. L'observabilité et le plan de preuve [E6]

Le partenaire peut être lent, en panne ou de mauvaise foi : chaque affirmation sur le comportement de l'équipe doit pouvoir se prouver par une trace ou par un test. Le monitorage se code au chantier 2, mais le journal d'événements vit dans la mémoire partagée : s'il n'est pas prévu ici, il n'y aura rien à mesurer plus tard.

- [ ] Quel événement enregistre-t-on à chaque étape : qui, quoi, quand, combien de temps, avec quel résultat ?
- [ ] Quelles métriques par agent en découlent ?
- [ ] Quels éléments observe-t-on au niveau de l'équipe et de son orchestration ?
- [ ] Comment montrer qu'une demande a suivi le bon chemin, avec une trace rejouable par demande ?
- [ ] Comment prouver E1 : sur tous les scénarios de `eval/scenarios.jsonl`, le statut final est-il toujours une décision ou une escalade ?
- [ ] Comment prouver E2 : quel test confie à un agent une tâche hors de son rôle, et quel refus attend-il ?

Le filtre des données sortantes, la validation des réponses du partenaire et le mode dégradé sont traités au [chantier 2](chantier-2-a2a-epreuve.md).

## Schémas

Première proposition, provisoire : les choix qui dépendent de `specs_metier.md` (propriétaire de la suspicion de fraude, refus bloquant pour pièces manquantes, valeurs des bornes) seront confirmés ou corrigés à sa lecture. Chaque schéma existe en `.drawio`, modifiable sur [app.diagrams.net](https://app.diagrams.net/), et en `.png`. Ils se régénèrent avec `scripts/make_schemas_ch1.py`.

### 0. Le choix du pattern : l'arbre de décision

Une question produit (Q0), puis cinq questions d'architecture posées dans l'ordre ; chaque réponse élimine une option, jusqu'au pattern retenu. Fichiers : [schema-0-arbre-de-decision.drawio](schemas/schema-0-arbre-de-decision.drawio), [PNG](schemas/schema-0-arbre-de-decision.png).

![Arbre de décision du pattern](schemas/schema-0-arbre-de-decision.png)

### 1. La carte des agents

Rôles, frontières (avec le point ambigu tranché), dépendances et parallélisme. Fichiers : [schema-1-carte-des-agents.drawio](schemas/schema-1-carte-des-agents.drawio), [PNG](schemas/schema-1-carte-des-agents.png).

![Carte des agents](schemas/schema-1-carte-des-agents.png)

### 2. L'orchestration et la terminaison garantie

Délégations, conditions d'arrêt, bornes provisoires ; chaque chemin finit par une décision ou une escalade humaine motivée. Fichiers : [schema-2-orchestration.drawio](schemas/schema-2-orchestration.drawio), [PNG](schemas/schema-2-orchestration.png).

![Orchestration et terminaison garantie](schemas/schema-2-orchestration.png)

### 3. La mémoire partagée de la demande

Sections, propriétaire de chaque section, droits de lecture, orchestrateur seul écrivain, sauvegarde après chaque étape, journal d'événements. Fichiers : [schema-3-memoire-partagee.drawio](schemas/schema-3-memoire-partagee.drawio), [PNG](schemas/schema-3-memoire-partagee.png).

![Mémoire partagée de la demande](schemas/schema-3-memoire-partagee.png)
