
Status: draft | validated
## Goal

## Input

## Expected

## Invariants

## Failure


---
# Example :

## Goal

Validate nominal propagation: `BarAvailable` -> `IntentGenerated(MarketOrderIntent)`

## Input

- 1 valid BarAvailable
- MarketOrderScenarioDecisionLayer
## Expected

- MarketStore updated
- FeatureStore updated
- IntentGenerated emitted
- MarketOrderIntent(BUY, quantity=1)
## Invariants

- deterministic output
- causal linkage preserved
## Failure

- invalid bar rejected before decision layer