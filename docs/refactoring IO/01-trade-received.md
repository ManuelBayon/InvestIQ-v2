## Sémantique

Une transaction de marché observée sur l’instrument suivi. Chaque événement décrit une transaction individuelle, pas une cotation ni une exécution de notre propre ordre.

Payload immuable, indépendant des objets IBKR. Les métadonnées de réception (`run_id`, `sequence`, `received_at_utc`) appartiennent à une enveloppe distincte.

## Champs

| Champ           | Type proposé   | Définition et justification                                                                                                               |
| --------------- | -------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `symbol`        | `str`          | Référence de l’instrument négocié. Permet de rattacher la transaction à l’instrument et de vérifier sa conformité au run mono-instrument. |
| `timestamp_utc` | `datetime` UTC | Instant de la transaction fourni par la source. Conserve le temps de marché indépendamment de la réception locale.                        |
| `price`         | `Decimal`      | Prix effectivement négocié, exprimé selon la convention de cotation de l’instrument. Entrée du calcul des indicateurs.                    |
| `size`          | `Decimal`      | Quantité échangée dans cette transaction, en actions, contrats ou unité définie par l’instrument. Préserve le volume du fait reçu.        |

## Invariants

- `symbol` est non vide et désigne sans ambiguïté l’instrument attendu dans le contexte du run.
- `timestamp_utc` possède un fuseau et un décalage UTC nul ; aucun timestamp naïf.
- `price` et `size` sont finis ; `size > 0`.
- Les contraintes de prix et de quantité dépendent de l’instrument. Aucun rejet universel des prix négatifs.
- Les valeurs sont conservées sans arrondi implicite ni remplacement silencieux d’une donnée invalide.

## Normalisation à l’entrée

L’intégration IBKR extrait les quatre valeurs du callback, résout la référence instrument, convertit le temps en UTC et applique les conversions numériques convenues. La source synthétique produit le même contrat.

La conversion vers `Decimal` doit être explicite : elle ne restaure pas une précision déjà perdue par la source. Une entrée invalide ne devient pas un `TradeReceived` valide ; sa politique de signalement reste à définir.

Aucune garantie de monotonie du temps de marché. Deux transactions identiques en valeurs peuvent être distinctes : ces champs ne constituent pas une clé de déduplication.

## Vérification du contrat

Cas minimaux : transaction valide ; conversion d’un timestamp avec décalage vers UTC ; instrument inattendu ; timestamp naïf ; prix ou taille non finis ; taille nulle ou négative. Vérifier la conservation du prix, de la taille et de l’instant source.
