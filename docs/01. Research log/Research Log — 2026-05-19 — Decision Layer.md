
Ce jour, suite à la définition et validation des `OrderIntent`, j’ai créé plusieurs `DecisionLayer` triviaux, un pour chaque type d’`OrderIntent`.

```python
class NoOperationDecisionLayer:
	...
class MarketOrderIntentDecisionLayer:
	...
class LimitOrderIntentDecisionLayer:
	...
class StopMarketOrderIntentDecisionLayer:
	...
class BracketOrderIntentDecisionLayer:
	...
```

Exemple de code pour l'une des `DecisionLayer` triviale :
```python
class BracketOrderIntentDecisionLayer:  
    """  
    2026-05-19 : Trivial decision pipeline returning 
    StopMarketOrderIntent used to test complete causal pipeline.    
    """
    def evaluate(  
            self,  
            run_id: str,  
            next_event_id: str,  
            bar_event_id: str,  
            market_view: tuple[Bar,  ...],  
            features_view: tuple[float, ...],  
    ) -> IntentGenerated | NoOperation:  
        return IntentGenerated(  
            run_id=run_id,  
            event_id=next_event_id,  
            context=DecisionContext(  
               bar_event_id=bar_event_id,  
               bar=market_view[-1],  
               feature_value=features_view[-1] if features_view else None,  
            ),  
            intent=BracketOrderIntent(  
                entry=MarketOrderIntent(  
                   quantity=1,  
                   direction=Side.BUY,  
                ),  
                stop_loss=[  
                    StopMarketOrderIntent(  
                        trigger_price=90.0,  
                        triggered_order=MarketOrderIntent(  
                            quantity=1,  
                            direction=Side.SELL,  
                        )  
                    )  
                ],  
                take_profit=[  
                    LimitOrderIntent(  
                        quantity=1,  
                        direction=Side.SELL,  
                        price=130.0  
                    )  
                ]  
            ),  
        )
```

---

Cela va me permettre de tester différents jeux d’événements canoniques `BarAvailable` en amont du pipeline causale côté stratégie.

Je noterai pour chaque scénario :
- le jeu de données utilisé,
- le `DecisionLayer` utilisé,
- l’`OrderIntent` généré,
- les événements produits par le pipeline.

---

