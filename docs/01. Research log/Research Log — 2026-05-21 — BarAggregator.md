## Current focus

Je suis sur la boucle asynchrone qui produit l'évènement canonique `BarAvailable` à partir des ticks reçu de manière asynchrone par mon broker.

La réflexion sur la modélisation temporelle de l'agrégation des ticks.
## Hypotheses

### Modèle 1 : Event-driven close

- Phase 1 : Synchronisation (bougie partielle ?)
- Phase 2 : Fermer la bougie quand le timestamp de la bougie dépasse le timestamp prévu t0 + durée.
### Modèle 2 : Time-driven close


- Phase 1 : Synchronisation
- Phase 2 : Calcul durée exacte de la bougie