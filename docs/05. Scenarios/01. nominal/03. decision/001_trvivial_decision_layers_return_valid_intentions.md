Status: draft 
## Goal

Les `DecisionLayer` triviaux sont des **test fixtures exécutables** pour les scénarios d’intégration. Donc il faut les tester au minimum, sinon les tests pipeline reposent sur un générateur non vérifié.
## Input

```python
run_id: str,  
next_event_id: str,  
bar_event_id: str,  
market_view: tuple[Bar,  ...],  
features_view: tuple[float, ...],
```

## Expected

- type d'évènement valide
- type d'intention valide
## Invariants

- Aucun
## Failure

- Aucun cas d'erreur implémenté dans les pipelines de tests triviaux.