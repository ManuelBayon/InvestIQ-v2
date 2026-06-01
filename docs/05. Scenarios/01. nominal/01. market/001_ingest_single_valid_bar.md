Status: validated

## Goal

- Valider l'ingestion d'une bougie par `MarketStore` avec `BarAvailable` valide.

## Input

- 1 `BarAvailable` valide
- 1 `MarketStore`

## Expected

- Mise à jour de `MarketStore`
- `MarketStore.view()[-1]` retourne la dernière bougie ingérée.

## Invariants

- Aucun

## Failure

- Aucun