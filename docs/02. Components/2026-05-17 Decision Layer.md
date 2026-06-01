## Responsabilités

Transformer une vue du marché et d'un indicateur en décision de trading `IntentGenerated` ou `NoOperation`.
## Inputs

- `run_id: str`
- `bar_event_id: str`
- `market: tuple[Bar,  ...]`
- `features: tuple[float, ...]`
## Owned state

Pas d'état maintenu par cette couche, elle applique transformation une pure.
## Outputs

```python
@dataclass(frozen=True)  
class IntentGenerated(BaseEvent):  
    bar_timestamp_utc: datetime  
    market_price: float  
    feature_value: float  
    intention: Intention  
  
@dataclass(frozen=True)  
class NoOperation(BaseEvent):  
    bar_timestamp_utc: datetime  
    market_price: float  
    feature_value: float | None = None
```
## Garanties

Trace chaque décision, même lorsque le modèle ne fait rien avec le contexte dans lequel a été prix la décision : 
- prix courant vu par la couche de décision
- valeur de l'indicateur vue par la couche de décision
## Refus  
## Out of scope

- Ne valide pas le risque,
- Ne construit pas les ordres,
- Ne transmets pas les ordres,
- N'a pas d'effet de bord.

---
## Attributs

- Aucun
## Méthodes

```python
def evaluate(  
        self,  
        run_id: str,  
        bar_event_id: str,  
        market: tuple[Bar,  ...],  
        features: tuple[float, ...],  
) -> IntentGenerated | NoOperation:
```

---
## Évolutions à venir

- Gestion SL
- Gestion TP
- Gestion ordres limites