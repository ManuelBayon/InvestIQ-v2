Status: draft | validated
## Goal

valider l'ingestion de 2 bar avec timestamp strictement croissant.

## Input

- 2 `BarAvailable` avec timestamps utc strictement croissants
- 1 `MarketStore`
## Expected

- Mise à jour de `MarketStore`
- `MarketStore.view()[-1]` retourne la dernière bougie ingérée.
## Invariants

- Validation cas nominal de l'invariant timestamp UTC strictement croissant.
## Failure

- Aucun
