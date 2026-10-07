# Hypothèses

- Un seul client par run ⇒ `client_id` = 1
- Un seul compte par run ⇒ `account_num`=DUK2...7

La stratégie produit une intention de trading :

```
BraketOrderSpec:
	parent=MarketOrderSpec(BUY, 1.0)
	stoploss=Stoploss(price)
	takeprofit=TakeProfit(price)
``` 

Pour chaque ordre de `BracketOrder` : 

- `IBAdapter` converti la spécification en en ordre au format broker,
- `IBAdapter` planifie la soumission de l'ordre dans la boucle `asyncio` du Thread `IBKR`,
- `IBAdapter` s'abonne aux évènements (`statusEvent`, `fillEvent`, `commissionReportEvent`).

---
# Choix architectural pour les ordres : `EventSourcing`

- Source de vérité : évènements canoniques
	- externes : `StatusUpdated`, `FillReceived`, `CommissionReportReceived`
	- internes: `IntentGenerated`,  `OrderCreated` , `RiskAccepted/RiskRejected`.

- Les évènements sont journalisé et éventuellement persistés
- Projection le l'état d'exécution à partir des évènements canoniques et de projecteurs déterministes :
	- État des ordres, 
	- État des positions, 
	- État du portefeuille,
	- État du PnL

Justification : Unicité de la source de vérité (journal canonique des évènements).

```
Journal canonique
      ↓
 ┌────┼──────────┬──────────┐
 ↓    ↓          ↓          ↓
OMS  Position  Portfolio    PnL
```

Le journal canonique doit contenir les évènements externes (données marché, exécution) ainsi que les évènements internes nécessaire à la reconstruction de l'état et de la décision.

---
## Corrélation identifiant interne et broker

**Parent : BUY@Market**

```
BrokerOrderAssigned:
	run_id="TEST_RUN"
	event_id="EVT_00006"
	order_id=001
	broker_order_id=278
	broker_parent_id=0
```

>[!note] Décision en cours
>La séparation entre la création, la corrélation des identifiants ainsi que leur soumission est étudiée [[Révision du 2026-10-06 — Préparation et soumission | ici]].

---

**Stop-Loss : Stop@29800**

```
BrokerOrderAssigned:
	run_id="TEST_RUN"
	event_id="EVT_00007"
	order_id=002
	broker_order_id=279
	broker_parent_id=278
```

**Take-Profit : Limit@ 30200**

```
BrokerOrderAssigned:
	run_id="TEST_RUN"
	event_id="EVT_00008"
	order_id=003
	broker_order_id=280
	broker_parent_id=278
```


### Envoi des commande de soumission d'ordre 

>[!note] étudier la mise en oeuvre de cette solution 



---
### - 4. `statusEvent`

Évènement externe `ibinsync` : 

```
statusEvent:
	order_id=279
	parent_id=278
	status="PreSubmitted"
```

- Fait le mapping entre l'identifiant broker et l'identifiant interne.

```
OrderStatusUpdated:
	run_id="TEST_RUN"
	event_id="EVT_00009"
	order_id=002
	parent_id=001
	status="PreSubmitted"
```

- Journaliser `OrderStatusUpdated`

---
### - 5. `statusEvent`

Déclenchement du callback par `ibinsync` : 

```
statusEvent:
	order_id=280
	parent_id=278
	status="PreSubmitted"
```

- Fait le mapping entre l'identifiant broker et l'identifiant interne.

```
OrderStatusUpdated:
	run_id="TEST_RUN"
	event_id="EVT_00010"
	order_id=003
	parent_id=001
	status="PreSubmitted"
```

---
### - 6. `statusEvent`

Déclenchement du callback par `ibinsync` : 

```
statusEvent:
	order_id=278
	parent_id=0
	status="PreSubmitted"
```

- Fait le mapping entre l'identifiant broker et l'identifiant interne.

```
OrderStatusUpdated:
	run_id="TEST_RUN"
	event_id="EVT_00011"
	order_id=001
	parent_id=None
	status="PreSubmitted"
```

- Journaliser `OrderStatusUpdated`

---
### - 7. `fillEvent`

>[!warning] Distinction sémantique
>
>Je reçois le `fillEvent` avant le `statusEvent` et ils n'ont pas la même sémantique.
>
>-  `fillEvent`: 
>	- timestamp(UTC), 
>	- quantité exécuté, 
>	- side,
>	- prix, 
>	- quantité cumulée de l'ordre.
><br>
>-  `statusEvent`: status(Filled)


- Dans ce scénario le `Fill` arrive avant le `statusEvent(Filled)`

```
fillEvent:
	order_id=278
	parent_id=0
	exec_id="0000e1a7.6aa503e1.01.01"
	timestamp_utc=datetime(...)
	qty_executed=1.0
	side="BOT"
	price=30000.0
	cumul_qty=1.0
```

- Fait le mapping entre l'identifiant broker et l'identifiant interne.

Ne change pas l'objet Order : 
```
FillReceived:
	run_id="TEST_RUN"
	event_id="EVT_00012"
	order_id=001
	parent_id=None
	exec_id="0000e1a7.6aa503e1.01.01"
	timestamp_utc=datetime(...)
	quantity=1.0
	side="BUY"
	price=30000.0
	cumulative_qty=1.0
```

- Journalise l'évènement `FillReceived`

---
### - 8. `statusEvent`

Déclenchement du callback par `ibinsync` : 

```
statusEvent:
	order_id=278
	parent_id=0
	status="Filled"
```

- Fait le mapping entre l'identifiant broker et l'identifiant interne.

```
OrderStatusUpdated:
	run_id="TEST_RUN"
	event_id="EVT_00013"
	order_id=001
	parent_id=None
	status="Filled"
```

- Journaliser `OrderStatusUpdated`

---
### 9. `CommissionReportReceived`

```
commissionReportEvent:
	order_id=278
	parent_id=0
	exec_id="0000e1a7.6aa503e1.01.01"
	commission=0.61
	currency="USD"
	realized_pnl=0.0
```

+ Fait le mapping entre l'identifiant broker et l'identifiant interne.

```
CommissionReportReceived:
	run_id="TEST_RUN"
	event_id="EVT_00014"
	order_id=1
	parent_id=None
	exec_id="0000e1a7.6aa503e1.01.01"
	commission=0.61
	currency="USD"
	realized_pnl=0.0
```

- Journalise l'évènement `CommissionReportReceived`

---
## Résultat attendu de la projection de l'ordre 001

```
Order:
	order_id=001
	parent_id=None
	
	broker_order_id=278
	broker_parent_id=0
	
	intention_id = "EVT_00002"
	
	last_broker_status="Filled"
	
	filled_qty=1.0
	avg_fill_price=30000.0
	
	executions=[
		Execution(
			exec_id="0000e1a7.6aa503e1.01.01"	
			timestamp_utc=datetime(...)
			quantity=1.0
			side="BUY"
			price=30000.0
		),
	]
	
	commission:
		currency="USD"
		value=0.61
	
	
	broker_realized_pnl:
		currency="USD"
		value=0.0
```