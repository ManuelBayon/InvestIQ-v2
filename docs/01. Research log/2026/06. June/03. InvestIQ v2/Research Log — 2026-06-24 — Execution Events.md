
Pour un ordre au marché j'ai identifié les évènements d'exécution suivants transmis par le broker, l'objectif étant de les canoniser.

- trade.statusEvent
- trade.commissionReportEvent
- trade.fillEvent
- trade.filledEvent

---

A ce stade je propose le mapping suivant : 

- trade.statusEvent -> OrderStatusUpdated
- trade.commissionReportEvent -> CommissionReportReceived
- trade.fillEvent -> FillReceived
- trade.filledEvent -> OrderFilled

