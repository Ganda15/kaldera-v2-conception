# Chantier 2 : la collaboration A2A et l'épreuve du réel

Ce que le brief attend pour ce chantier : le schéma d'échange A2A (contrat, filtre de données, validation des réponses, chemin de mode dégradé) et le plan d'épreuve (scénarios d'intégration × signaux observés × ajustement possible du chantier 1).

Exigences concernées : E3, E4, E5 et E6. Le brief résume l'enjeu en une ligne : le partenaire peut être lent, menteur ou en panne, et le contrat doit être respecté à la lettre.

## 1. Le protocole A2A

### La version visée

La spécification a changé entre la version 0.3.0 et la version 1.0.0, la dernière publiée. Les noms ne sont pas les mêmes d'une version à l'autre. Le dossier doit donc dire laquelle il suit, et c'est le partenaire qui l'impose.

| Élément | Version 0.3.0 | Version 1.0.0 |
|---|---|---|
| Envoyer un message | `message/send` | `SendMessage` |
| Lire une tâche | `tasks/get` | `GetTask` |
| Annuler une tâche | `tasks/cancel` | `CancelTask` |
| États d'une tâche | `submitted`, `working`, `input-required`, `completed`, `canceled`, `failed`, `rejected`, `auth-required`, `unknown` | `TASK_STATE_SUBMITTED`, `TASK_STATE_WORKING`, `TASK_STATE_INPUT_REQUIRED`, `TASK_STATE_COMPLETED`, `TASK_STATE_CANCELED`, `TASK_STATE_FAILED`, `TASK_STATE_REJECTED`, `TASK_STATE_AUTH_REQUIRED`, `TASK_STATE_UNSPECIFIED` |
| Type d'une Part | champ `kind` : `text`, `file` ou `data` | champ `kind` supprimé |
| Champs obligatoires d'une Task | `id`, `contextId`, `kind`, `status` | `id`, `status` |
| Envoi sans attendre la fin de la tâche | `configuration.blocking: false` | `returnImmediately: true` |
| Où se lit la version du protocole | champ `protocolVersion` de l'Agent Card | paramètre de service `A2A-Version` |

Les exemples de ce document suivent la version 0.3.0. Ils seront à transposer si le partenaire suit la version 1.0.0.

### Les objets du protocole

- **Agent Card** : la fiche d'identité de l'agent. Elle dit ce qu'il sait faire (ses *skills*), quelle version du protocole il suit et comment s'authentifier. En version 0.3.0, l'emplacement recommandé est `/.well-known/agent-card.json`.
- **Task** : l'unité de travail, avec un identifiant et un état. Les tâches d'une même conversation partagent un `contextId`.
- **Message** : un tour de parole entre le client et l'agent, découpé en Parts.
- **Part** : un morceau de contenu, texte, fichier ou données JSON.
- **Artifact** : le résultat d'une tâche, lui aussi fait de Parts.

Une réponse à l'envoi d'un message peut être une Task ou directement un Message. Les deux cas doivent être prévus.

### L'échange appliqué à Kaldera

Un envoi qui attend la fin de la tâche ne rend la main qu'une fois la tâche terminée. Si notre délai expire avant, nous n'avons jamais reçu l'identifiant de la tâche : impossible de l'annuler, elle reste orpheline chez le partenaire. Pour pouvoir borner l'attente et annuler, l'agent fraude envoie sans attendre, enregistre l'identifiant dans la mémoire, puis lit l'état de la tâche jusqu'au délai maximum.

```mermaid
sequenceDiagram
    participant F as Agent fraude (Kaldera)
    participant P as Partenaire anti-fraude
    F->>P: Lecture de l'Agent Card (skill, version, authentification)
    F->>F: Filtre : message construit avec les seuls champs du contrat
    F->>P: Envoi sans attendre la fin de la tâche
    P-->>F: Task créée (taskId, contextId) ou Message direct
    F->>F: taskId et contextId enregistrés dans la mémoire
    loop Jusqu'au délai maximum, au rythme permis par le contrat
        F->>P: Lecture de l'état de la tâche
        P-->>F: État courant
    end
    alt Tâche terminée avant le délai
        F->>F: Validation de la réponse (protocole, schéma, sens)
    else Délai dépassé
        F->>P: Annulation de la tâche
        F->>F: Mode dégradé
    end
```

### Questions

- [ ] Quelle version du protocole le partenaire suit-il ?
- [ ] Que contient l'Agent Card du partenaire : quel skill, quelle version, quelle authentification ?
- [ ] Vérifie-t-on l'Agent Card au démarrage ? Que fait-on si le skill ou la version attendus manquent ?
- [ ] Quel mode d'échange choisit-on : envoi avec attente, envoi sans attente puis lecture de l'état, streaming, ou notification push ? Pourquoi ?
- [ ] À quel rythme peut-on lire l'état d'une tâche sans enfreindre le contrat ?
- [ ] Comment relie-t-on une tâche A2A à sa demande Kaldera ?

## 2. Le contrat d'échange [E3] [E4]

| Rubrique | Ce qu'il faut définir |
|---|---|
| Requête | Liste fermée des champs, avec type, format et caractère obligatoire. Exactement les champs du contrat, ni plus ni moins |
| Identifiants | Ce que le contrat prévoit : référence réelle ou pseudonyme. Pseudonymiser relève du contrat ; envoyer un pseudonyme là où le contrat attend une référence réelle le rompt |
| Réponse | Schéma de la partie données : identifiant de corrélation, verdict (liste fermée de valeurs), score (bornes), code motif |
| Délais | Délai par appel, budget total de l'étape anti-fraude, rythme de lecture de l'état |
| Relances | Erreurs rejouables (réseau, HTTP 503) ou non (réponse invalide, paramètres invalides `-32602`). Nombre maximum, délai croissant entre deux essais, respect de l'en-tête `Retry-After` |
| Doublons | Une relance peut créer une deuxième tâche chez le partenaire. Le partenaire dédoublonne-t-il sur le `messageId` ? |
| Version | Version du contrat dans le schéma, pour repérer un changement côté partenaire |

### Questions

- [ ] Quel est le contrat d'échange avec le partenaire anti-fraude (format, champs, délais, règles de relance) ?
- [ ] Quels champs exactement dans la requête, avec quel type et quel format, obligatoires ou non ?
- [ ] Le contrat attend-il une référence client réelle, ou autorise-t-il un pseudonyme ?
- [ ] Quel schéma attend-on en réponse ?
- [ ] Comment repère-t-on que le partenaire a changé la version de son contrat ?

### Exemples fictifs (format 0.3.0)

Les champs métier ci-dessous sont inventés. Les vrais viendront du contrat du partenaire. L'enveloppe A2A, elle, suit la version 0.3.0 : les quatre exemples ont été validés contre le schéma JSON officiel de cette version (lien dans le [README](README.md)).

Envoi de la demande, sans attendre la fin de la tâche :

```json
{
  "jsonrpc": "2.0",
  "id": "req-001",
  "method": "message/send",
  "params": {
    "message": {
      "kind": "message",
      "role": "user",
      "messageId": "msg-7f3a",
      "parts": [
        {
          "kind": "data",
          "data": {
            "claim_ref": "CLM-8842",
            "claim_type": "auto",
            "amount_claimed": 4200.00,
            "incident_date": "2026-09-12"
          }
        }
      ]
    },
    "configuration": { "blocking": false }
  }
}
```

Réponse immédiate : la tâche est créée, son identifiant est enregistré dans la mémoire.

```json
{
  "jsonrpc": "2.0",
  "id": "req-001",
  "result": {
    "kind": "task",
    "id": "task-123",
    "contextId": "ctx-8842",
    "status": { "state": "submitted" }
  }
}
```

Lecture de l'état de la tâche :

```json
{
  "jsonrpc": "2.0",
  "id": "req-002",
  "method": "tasks/get",
  "params": { "id": "task-123" }
}
```

Réponse une fois la tâche terminée :

```json
{
  "jsonrpc": "2.0",
  "id": "req-002",
  "result": {
    "kind": "task",
    "id": "task-123",
    "contextId": "ctx-8842",
    "status": { "state": "completed" },
    "artifacts": [
      {
        "artifactId": "art-1",
        "parts": [
          {
            "kind": "data",
            "data": {
              "claim_ref": "CLM-8842",
              "risk_level": "high",
              "score": 0.82,
              "reason_code": "R12"
            }
          }
        ]
      }
    ]
  }
}
```

## 3. Le filtre des données sortantes [E3]

- **Construire un objet neuf.** Le message ne contient que les champs du contrat, recopiés un par un. On ne part pas de la demande complète pour en retirer des champs : un champ ajouté plus tard à la demande passerait le filtre.
- **Valider avant l'envoi.** Le message sortant est vérifié contre le schéma du contrat, sans champ supplémentaire autorisé (`additionalProperties: false`). En cas d'échec, rien ne part.
- **Un champ en trop est une fuite.** Il est bloqué chez nous, avant l'envoi. Compter sur un refus du partenaire serait trop tard : la donnée serait déjà sortie.
- **Un seul point de sortie.** Seul l'agent fraude parle au partenaire, et seulement à travers ce filtre.
- **Des logs sans fuite.** On journalise ce qui est parti sans recopier les données sensibles dans les traces.
- **La preuve.** Un test glisse des données sensibles dans la mémoire de la demande et vérifie qu'elles n'apparaissent pas dans le message envoyé.

### Questions

- [ ] Quelles données ont le droit de partir chez le partenaire, et comment le filtre garantit-il que rien d'autre ne sort ?
- [ ] Liste blanche ou liste noire ? Que se passe-t-il quand un nouveau champ est ajouté plus tard à la demande ?
- [ ] Valide-t-on le message sortant contre le schéma du contrat avant de l'envoyer ?
- [ ] Un seul agent a-t-il le droit de parler au partenaire ?
- [ ] Nos logs et nos traces laissent-ils fuiter des données qu'on n'a pas le droit d'envoyer ?

## 4. La validation des réponses [E4]

| Niveau | Ce qu'on vérifie |
|---|---|
| Protocole | JSON-RPC valide, `id` identique à celui de la requête, réponse de type Task ou Message, état de tâche connu |
| Schéma | Partie données conforme au contrat, sans champ en trop, avec les bons types. Cette règle vise la partie données : l'enveloppe A2A porte légitimement des champs optionnels (historique, métadonnées) |
| Sens | `claim_ref` identique à celui envoyé, score dans ses bornes, verdict cohérent avec le score, code motif connu |

- Une réponse qui échoue à un seul niveau est rejetée et journalisée. Elle n'entre jamais dans la mémoire partagée.
- Une réponse de type Message, sans tâche, est acceptée si sa partie données respecte le contrat, et rejetée sinon.
- Seuls les champs structurés validés sont gardés. Un texte libre du partenaire n'est jamais injecté dans le prompt d'un autre agent, à cause du risque d'injection.

### Questions

- [ ] Qu'est-ce qu'une réponse non conforme, à chacun des trois niveaux ?
- [ ] Comment repère-t-on un partenaire « menteur », qui répond au bon format avec un contenu faux ?
- [ ] Que fait-on si le partenaire répond par un Message au lieu d'une tâche ?
- [ ] Une réponse rejetée mène-t-elle au mode dégradé ou à une escalade ?
- [ ] Garde-t-on le texte libre du partenaire ? Si oui, comment l'empêcher d'injecter des instructions dans le prompt d'un autre agent ?

## 5. Le mode dégradé [E5]

### Un principe avant les cas

Avant de traiter chaque situation, le dossier fixe une règle commune. Proposition à confronter à `specs_metier.md` : faute de verdict valide du partenaire, quelle qu'en soit la raison, la demande suit le mode dégradé défini par le métier. L'escalade humaine est réservée aux cas que `specs_metier.md` désigne et aux bornes atteintes. Une règle unique donne moins de branches, donc moins de tests, et une réponse plus simple à défendre.

```mermaid
flowchart TD
    A["Appel au partenaire"] --> B{"Verdict valide avant le délai ?"}
    B -- Oui --> C["Verdict écrit dans la mémoire, la demande continue"]
    B -- Non --> D["Mode dégradé défini par specs_metier.md"]
    D --> E{"Le métier prévoit-il une escalade dans ce cas ?"}
    E -- Oui --> F["Escalade humaine motivée"]
    E -- Non --> G["La demande continue ou est routée"]
```

### Questions

- [ ] Que dit `specs_metier.md` : la demande continue, ou elle est routée ? Si elle est routée, vers qui ?
- [ ] À partir de quand le partenaire est-il « indisponible » : délai dépassé, erreur, lenteur ? Avec quel délai ?
- [ ] « Pas de retry sauvage » : quelles erreurs rejoue-t-on, combien de fois, avec quel délai entre deux essais ?
- [ ] Faut-il un disjoncteur (*circuit breaker*) pour arrêter d'appeler un partenaire en panne ?
- [ ] Une relance peut-elle créer deux tâches chez le partenaire ?
- [ ] Annule-t-on la tâche chez le partenaire quand on passe en mode dégradé ?
- [ ] Que fait-on d'une réponse qui arrive après le passage en mode dégradé ?
- [ ] Quelle réaction pour chaque état d'échec ou d'interruption : `failed`, `rejected`, `auth-required`, `input-required` ? Avec `input-required`, le partenaire réclame plus de données, alors que rien ne doit sortir hors contrat.

### Tableau des situations

Réactions proposées, à confronter à `specs_metier.md`. Les états sont nommés selon la version 0.3.0.

| Situation | Ce qu'on observe | Réaction proposée |
|---|---|---|
| Cas nominal | `completed` et partie données valide | Verdict écrit dans la mémoire, la demande continue |
| Partenaire lent | Tâche non terminée au délai maximum | Annulation de la tâche, puis mode dégradé |
| Partenaire en panne | Erreur réseau, HTTP 5xx, aucune réponse | Relances bornées selon le contrat, puis mode dégradé |
| Réponse invalide | Échec au niveau protocole ou schéma | Rejet sans relance, puis mode dégradé |
| Partenaire menteur | Schéma conforme, sens incohérent | Rejet journalisé, puis mode dégradé |
| Refus | `rejected` ou `failed` | Mode dégradé |
| Demande d'informations | `input-required` | Rien n'est envoyé hors contrat : annulation, puis mode dégradé |
| Problème d'accès | `auth-required`, HTTP 401 ou 403 | Pas de relance, alerte technique, puis mode dégradé |
| Réponse tardive | Arrive après le passage en mode dégradé | Journalisée, sans changer la décision déjà prise |

## 6. L'observabilité [E6]

Le brief impose trois métriques par agent : la latence, les échecs et le recours à l'externe.

- [ ] Comment mesure-t-on chacune des trois métriques ?
- [ ] Où ces métriques sont-elles visibles : tableau de bord, logs, rapport ?
- [ ] Quels éléments observe-t-on au niveau de l'équipe et de son orchestration ?
- [ ] Comment montrer qu'une demande a suivi le bon chemin ?

### Tableau à remplir : les métriques

| Métrique | Niveau | Source | Où elle est visible |
|---|---|---|---|
| Latence | Par agent | Journal d'événements | |
| Échecs | Par agent | Journal d'événements | |
| Recours à l'externe | Agent fraude | Journal d'événements | |
| Étapes par demande | Équipe | Compteurs de la mémoire | |
| Bornes atteintes | Équipe | Journal d'événements | |
| Passages en mode dégradé | Équipe | Journal d'événements | |

## 7. Le plan d'épreuve [E6]

- [ ] Comment vérifier automatiquement et rapidement que les specs sont respectées : tests d'acceptance fournis, tests d'intégration sur `eval/scenarios.jsonl` ?
- [ ] Comment prouver que chaque demande se termine par une décision ou une escalade, sur l'ensemble des scénarios ?
- [ ] Comment prouver que le scénario piège à boucle s'arrête dans les bornes ?
- [ ] Quels scénarios rejoue-t-on au minimum ?
- [ ] Pour chaque scénario : quel signal observe-t-on, et quel ajustement du chantier 1 peut-il déclencher ?
- [ ] Comment simule-t-on le partenaire : un bouchon réglable (lent, en panne, menteur) ?
- [ ] Les LLM ne répondent pas toujours pareil : combien de rejeux faut-il pour qu'un résultat soit probant ?

### Tableau à remplir : scénarios × signaux × ajustements

Chaque exigence a au moins un scénario.

| Scénario | Exigence | Signal observé | Ajustement possible du chantier 1 |
|---|---|---|---|
| Cas nominal | E1 | | |
| Agent sollicité hors de son rôle | E2 | | |
| Données en trop dans la demande | E3 | | |
| Réponse invalide | E4 | | |
| Partenaire menteur | E4 | | |
| Partenaire en panne | E5 | | |
| Partenaire lent | E5, E6 | | |
| Piège à boucle | E6 | | |

## 8. Le journal des ajustements [E6]

Le brief exige que chaque ajustement de l'orchestration provoqué par un scénario d'épreuve soit consigné. Les bornes et frontières finales doivent être justifiées par les scénarios rejoués, jamais réglées au jugé.

| Date | Scénario rejoué | Signal observé | Élément ajusté (borne, frontière ou routage) | Valeur avant | Valeur après | Résultat du rejeu |
|---|---|---|---|---|---|---|
| | | | | | | |

## 9. Hors brief, mais réel

- [ ] Une pièce justificative envoyée par le client peut-elle contenir une injection de prompt ? Comment s'en protège-t-on ?

## Schémas à produire pour ce chantier

- Le schéma d'échange A2A : contrat, filtre de données, validation des réponses, chemin de mode dégradé.
- Le plan d'épreuve : scénarios × signaux observés × ajustements du chantier 1.
