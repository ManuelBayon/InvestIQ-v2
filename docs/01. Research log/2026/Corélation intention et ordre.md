## Hypothèse 

- Un seul client par run ⇒ `client_id` = 1
- Un seul compte par run ⇒ `account_num`=DUK2...7

Ma stratégie produit une intention de trading :

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
## Choix architectural pour les ordres : `EventSourcing`

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
## Simulation

### 1. Callback donnée marché `IBKR`

```
TradeReceived:
	run_id="TEST_RUN"
	event_id="EVT_00001"
	symbol="MNQZ6"
	timestamp_utc=datetime(...)
	price=29898.50
	size=1.0
```

### 2. `TradeReceived`

```
IntentGenerated:
	run_id="TEST_RUN"
	event_id="EVT_00002"
	causation_id="EVT_00001"
	spec=BraketOrderSpec(
		entry=MarketOrderSpec(BUY, 1.0)
		stop_loss=Stoploss(29800)
		take_profit=TakeProfit(30200)
	)
```

---
### 3. `IntentGenerated`

**Parent : BUY@Market**
 
```
OrderCreated:
	run_id="TEST_RUN"
	event_id="EVT_00003"
	intention_id="EVT_00002"
	order_id=001
	parent=0
	broker_id=278
	broker_parent_id=0
```

**Stop-Loss : Stop@29900**

```
OrderCreated:
	run_id="TEST_RUN"
	event_id="EVT_00004"
	intention_id=EVT_00002
	order_id=002
	parent=001
	broker_id=279
	broker_parent_id=278
```

**Take-Profit : Limit@ 30200**

```
OrderCreated:
	run_id="TEST_RUN"
	event_id="EVT_00005"
	intention_id=EVT_00002
	order_id=003
	parent=001
	broker_id=280
	broker_parent_id=278
```

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
	event_id="EVT_00006"
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
	event_id="EVT_00007"
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
	event_id="EVT_00008"
	order_id=001
	parent_id=0
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
	event_id="EVT_00009"
	order_id=001
	parent_id=0
	exec_id="0000e1a7.6aa503e1.01.01"
	timestamp_utc=datetime(...)
	qty_executed=1.0
	side="BOT"
	price=30000.0
	cumul_qty=1.0
```

- Journalise l'évènement `FillReceived`

---
### 8. `CommissionReportReceived`

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
	event_id="EVT_00010"
	order_id=001
	parent_id=0
	exec_id="0000e1a7.6aa503e1.01.01"
	commission=0.61
	currency="USD"
	realized_pnl=0.0
```

- Journalise l'évènement `CommissionReportReceived`