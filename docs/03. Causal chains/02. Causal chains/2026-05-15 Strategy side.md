
Nom: Intention Generation Causal Chain
Version: 0.1
Status: Implemented
## Goal

 Transformer une nouvelle `Bar` en état de marché, en indicateurs puis en décision de trading.

## Canonical input

```python
@dataclass(frozen=True)  
class BarAvailable(BaseEvent):  
    received_at_utc: datetime  
    bar: Bar
```

## Causal flow

```
BarAvailable 
	↓ 
MarketStore.ingest() 
	↓ 
FeatureStore.update()
	↓
DecisionLayer.evaluate()
	↓
IntentGenerated | NoOperation
```

## Owned states

- Market history
- Feature history

## Guarantees

- Les composants sont appelés séquentiellement dans l'ordre :
	- `MarketStore` 
	- `FeatureStore` 
	- `DecisionLayer`
- l'ordre des outputs décisionnels suit l'ordre des `BarAvailable` traités,
- chaque `BarAvailable` produit exactement une décision,
- la décision est produite après mutation du `MarketStore` et `FeatureStore`.

## Failure / refusal cases

- `BarAvailable` avec timestamp <= dernière `Bar` ingérée → refus par `MarketStore`, aucun output décisionnel produit.
- market vide impossible après ingestion valide.

## Scenario coverage

- Nominal path : `BarAvailable` valide → décision valide

## Out of scope

- Ne gère pas le risque,
- Ne créé pas d'ordre,
- N'envoie pas d'ordre. 
## Known limitations

- mono-instrument implicite
- mono-bar_size implicite
- une seule feature codée en dur `sma_2`
- `NoOperation` utilisé aussi quand feature absente

## Open questions


## Evolution Log


