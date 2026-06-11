## Current focus

Je travaille actuellement sur la chaine cause de `BarAvailable` → `Intention` de la stratégie.

## Hypotheses

- Types d'ordre supporté en v1.2 : `MarketOrder`, `LimitOrder`, `StopMarketOrder`, `StopLimitOrder`.
- L'intention doit être facilement exprimable par le développeur de la stratégie.
- Cette décision ne doit pas être broker-aware.

## Experiments / prototypes

2026-05-18 : 
- Mis à jour ADR_001 avec les intention d'ordres. 
- En attente des tests unitaires des invariants intentions d'ordres
- En attente scénarios pipeline causal avec intentions d'ordres et `NoOperation`.

## Observations
Ce qui a été observé.

## Breakages / ambiguities
Ce qui casse ou reste flou.

## Decisions emerging
Décisions qui commencent à émerger.

## Open questions
Questions encore non résolues.

## Next iteration
Prochaine étape.