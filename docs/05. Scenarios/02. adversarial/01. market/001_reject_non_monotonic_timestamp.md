## Goal

Valider l'invariant principal du `MarketStore` : les timestamps UTC des bougies ingérées doivent être strictement croissant.
## Input

- 2 `BarAvailable` avec même timestamp UTC.
- 1 `MarketStore`
## Expected

- Lève `EventOrderingViolation`
- `MarketStore.view()[-1]` retourne la dernière bougie valide ingérée.
## Invariants

- Timestamps UTC strictement croissant sinon lève et pas de mutation de l'état.
## Failure

- Aucun