## Context

Création du modèle d'injection des données dans mon système évènementiel.
## Problem

Après avoir consulté la documentation de l'API `ib_insync`, je constate que les 2 options pour la data live est soit de recevoir des bougies de 5 secondes soit de souscrire aux données par ticks. 

Je cherchais pour simplifier le développement du système une méthode qui me donne des bar agrégées côté broker malheureusement elle n'existe pas avec IBKR.
## Decision

Je vais devoir créer un composant qui agrège les ticks pour produire des `Bar`.

Dans ce composant j'injecterai  : 
- `EventIdentityProvider` pour que mes évènements canonique `BarAvailable` puissent être construit avec run_id et event_id.
- `Event-Loop`

Le composant sera bootstrappé  grace à la config au démarrage

Ce composant pourra ensuite injecter les bougies dans la boucle évènementielle (event-loop)

### Politique de l'agrégation : Event-driven close

Pour le MVP je choisis  un event-driven close 

La bar se ferme quand un tick arrive avec :

```
tick.timestamp >= theoretical_close_ts
```

Donc si la bar est `09:30:00 → 09:31:00`, elle ne sera émise qu’au premier tick reçu à partir de `09:31:00`.

## Consequences

Avantage :

- simple ;
- pas besoin de scheduler ;
- déterministe à partir des ticks.

Inconvénient :

- si aucun tick n’arrive, la bar n’est pas émise ;
- latence de clôture variable ;
- gaps mal gérés.

## Alternatives considered

- Scheduler-driven close at theoretical boundary
- Hybrid: scheduler closes, but late ticks policy explicite
## Invalidation conditions

- N.A