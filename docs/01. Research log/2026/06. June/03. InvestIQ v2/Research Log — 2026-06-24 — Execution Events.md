
Pour un ordre au marché j'ai identifié les évènements d'exécution suivants transmis par le broker, l'objectif étant de les canoniser.

- trade.statusEvent
- trade.commissionReportEvent
- trade.fillEvent
- trade.filledEvent

---

A ce stade je propose le mapping suivant : 

- trade.statusEvent -> OrderStatusUpdated
- trade.fillEvent -> FillReceived
- trade.filledEvent -> OrderFilled
- trade.commissionReportEvent -> CommissionReportReceived

---
## OrderStatusUpdated

Commencon par le premier évènement canonique recu lors du placement d'un ordre au marché.

J'ai créé un évènement canonique vide pour l'instant, l'objectif de cet étape étant d'extraire les champs qui me semblent intéressant à garder tout en sachant que je pourrais facilement grâce à l'abstraction `OrderStatusUpdated`.



