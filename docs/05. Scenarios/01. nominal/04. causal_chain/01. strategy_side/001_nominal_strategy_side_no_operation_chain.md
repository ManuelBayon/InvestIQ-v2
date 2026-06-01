Status: draft
## Goal

Les composants suivants ont été testés unitairement : 
- `MarketStore`
- `FeatureStore`
- `NoOperationDecisionLayer`

Donc le but ici n'est pas de tester la logique interne  des composants leur enchainement dans le sous système depuis l'évènement canonique exogène `BarAvailable` à l'évènement canonique généré `NoOperation`.
## Input

- `MarketStore`
- `FeatureStore`
- `NoOperationDecisionLayer`
- `list[BarAvailable]`

## Expected

- Bijection `list[BarAvailable]` et `list[NoOperation]`
	- `BarAvailable.event_id == NoOperation.context.bar_event_id`
	- `BarAvailable.bar == NoOperation.context.bar`
	- `FeatureStore.view[-1] == NoOperation.context.feature_value | None`
## Invariants

## Failure