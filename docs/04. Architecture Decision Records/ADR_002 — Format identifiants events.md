## Context

Je dois créer des `event_id` et les lier a `causation_id`, il faut donc prendre une décision concernant le format des identifiants des évènements canoniques.
## Problem

- `event_id` est utilisé pour : 
	- audit,
	- replay,
	- debugging,
	- logs,
	- corrélation runtime,
	- etc.

Il faut donc un format standard et relativement explicite.

## Decision

Pour mon architecture actuelle orientée : 

- causalité,
- replay, 
- ordering,
- journal append-only

Je pense que des identifiants globaux, unique et ordonnés est la meilleure solution.

Exemple : `EVT_00001`, `EVT_00002`, etc.

## Consequences

## Alternatives considered

### IDs globaux uniques

Exemple :
```
EVT_000001
EVT_000002
EVT_000003
```

Avantages :
- ordre runtime global explicite
- journal naturellement ordonné
- debugging causal fort
- replay plus lisible
- pas d’ambiguïté d’identité.

Très cohérent avec :
- append-only journal
- causal ordering
- replay

### IDs typés

Exemple :
```
BAR_001
INTENT_001
FILL_001
```

Avantages :
- lecture humaine
- compréhension rapide du type
- logs plus agréables

Mais :
```
INTENT_001
```

ne dit pas :
- quand il est apparu globalement 
- entre quels événements
- dans quel ordre exact inter-type

## Invalidation conditions

- N.A