
2026-06-23

L'objectif de cette note de recherche est de définir le cycle de vie d'un ordre au marché à travers l'intégration de mon broker (IBKR).

Actuellement je peux produire une intention avec les spécificités de l'ordre au marché et le soumettre. En revanche les évènements émis par le broker ne sont ni écouté, ni canonisé et l'ordre n'est pas maintenu dans le système.

Une question ouverte est de déterminer si un composant dédié au suivi des ordres est nécessaire et quelles responsabilités il devrait posséder.

---
## Etape 1 : Observer la soumission d'un ordre au marché.

Pour celà j'utilise la méthode suivante :

```python
placeOrder(self, contract: Contract, order: Order) -> Trade
```

La fonction placeOrder retourne un objet `Trade`, ce dernier contient les évènements suivants:

- 'statusEvent', 
- 'modifyEvent', 
- 'fillEvent', : Fill individuel
- 'commissionReportEvent',
- 'filledEvent', : Fill Complet de lordre
- 'cancelEvent',
- 'cancelledEvent'

On peut donc s'abonner à ces évènements pour être notifier lorsqu'ils se produisent.

---
## Abonnement à l'évènement `filledEvent`

J'ai donc naturellement voulut m'abonner en premier à l'abonnement FilledEvent grace à la reference vers l'instance du trade retourné par `placeOrder()`.

Etape 1 : 
```python
trade = self._ib.placeOrder(contract, order)  
return trade
```

Etape 2 :
```python
def on_fill(trade: Trade):  
    print(f"On_fill: {trade}")
    
_trade = adapter.place_market_order(_order_specs)  
_trade.filledEvent.connect(listener=on_fill)
```

---
## Abonnement à tous les évènements important

```python
def on_fill(trade: Trade, fill: Fill):  
    print(f"On_fill: trade={trade} fill={fill}")  
  
def on_filled(trade: Trade):  
    print(f"On_filled: trade={trade}")  
  
def on_status_update(trade: Trade):  
    print(f"On status update: trade={trade}")  
  
def on_commission_report(  
        trade: Trade,  
        fill: Fill,  
        report: CommissionReport  
) -> None:  
    print(f"""On commission report:   
        trade={trade}  
        fill: {fill}  
        report: {report}""")

adapter = FakeIBKRAdapter()  
adapter.connect()  
  
_order_specs = MarketOrderSpecs(  
    instrument=FutureSpecs(symbol="MNQ", local_symbol="MNQU6"),  
    quantity=1, direction=Side.BUY, tif="DAY",  
)

_trade = adapter.place_market_order(order_specs=_order_specs)  
  
_trade.statusEvent += on_status_update  
_trade.commissionReportEvent += on_commission_report  
_trade.fillEvent += on_fill  
_trade.filledEvent += on_filled
```

Prochaine étape créer des évènements canoniques et améliorer ma méthode de R&D (processus et outillage notamment Git).

Résultat : 
``` terminal
statusEvent(trade): PreSubmitted
fillEvent(trade, fill) : PreSubmitted
statusEvent(trade) : Filled
filledEvent(trade) : Filled
commissionReportEvent(trade, fill, report) : Filled
```

---














