## Context

Ce jour j'ai compris que j'ai besoin de 3 boucles pour faire tourner le pipeline de décision, il m'en faudra peut etre plus dans le future pour recevoir les Fills, ack, cancel etc (évènement exécution broker) mais ce n'est pas l'objet de cette ADR.
## Problem

Comment lancer le runtime composé de 3 boucles tout en gardant un runtime composable et aussi propre que possible conceptuellement ?

## Decision

- Utiliser `asyncio`
- Créer un composant runtime qui lancer les boucles en parrallèle.


## Consequences

## Alternatives considered

## Invalidation conditions