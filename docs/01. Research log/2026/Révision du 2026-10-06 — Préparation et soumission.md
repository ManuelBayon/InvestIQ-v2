### 1. Réception nouvelle donnée marché par `IBKR`

**Réception du marché — thread IB** : le callback construit `TradeReceived` et le place dans la file canonique.

```
TradeReceived:
	run_id="TEST_RUN"
	event_id="EVT_00001"
	symbol="MNQZ6"
	timestamp_utc=datetime(...)
	price=29898.50
	size=1.0
```

### 2. Thread canonique : `TradeReceivedHandler.handle(event)`

**Génération de l’intention — thread canonique** : `TradeReceivedHandler` utilise la stratégie pour produire `IntentGenerated`, journalisé par la boucle.

```
IntentGenerated:
	run_id="TEST_RUN",
	event_id="EVT_00002",
	
	causation_id="EVT_00001",
	instrument_id="MNQZ6",
	
	order_spec=BraketOrderSpec(
		entry=MarketOrderSpec(
			side=BUY, 
			quantity=1.0, 
			tif="DAY"
		),
		stop_loss=StoplossSpec(
			price=29800, 
			tif="DAY"
		),
		take_profit=TakeProfitSpec(price=30200, tif="DAY")
	)
```

>[!warning] Attention révision du modèle en cours. 
>Le modèle d'intention actuel impose que le quantité des SL et TP soient identiques à la quantité de l'entrée.
>Je souhaite un modèle d'intention plus libre permettant de déclarer et gérer les ordres. 

###  3. Thread canonique : `IntentGeneratedHandler.handle(event)`

**Demande de préparation — thread canonique** : `IntentGeneratedHandler` attribue les identifiants internes, construit les spécifications individuelles et retourne `PrepareBracket`.

```
prepare=PrepareBracket(
	run_id="TEST_RUN",
	command_id="CMD_00001",
	
	intention_id=event.event_id,
	instrument_id=event.instrument_id,
	
	entry=OrderToPrepare(
		order_id=1,
		parent_id=None,
		spec=event.order_spec.entry
	),
	
	stop_loss=OrderToPrepare(
		order_id=2,
		parent_id=1,
		spec=event.order_spec.stop_loss
	),
	
	take_profit=OrderToPrepare(
		order_id=3,
		parent_id=1,
		spec=event.order_spec.take_profit
	),
)

return HandlerResult(
	events=(),
	commands=(prepare,),
)
```

### 4. Thread canonique : `PrepareBracket.handle(command)`

**Programmation — thread canonique** : `PrepareBracketHandler` programme la préparation sur la boucle IB via `call_soon_threadsafe`, puis termine sans attendre.

```
self._ib_client.ib_loop.call_soon_threadsafe(
	self._ib_adapter.prepare_on_ib_thread,
	command,
)
```

### 5. Thread IB : `ib_adapter.prepare_on_ib_thread(command)`

**Préparation — thread IB** : l’adaptateur attribue les identifiants broker, établit la parenté et les valeurs de `transmit`, puis place `BracketPrepared` dans la file canonique. **Aucun ordre n’est encore soumis.**

```
prepared = BracketPrepared(
    run_id=command.run_id,
    event_id="EVT_00003"
    
    intention_id=command.intention_id,
    preparation_id=command.command_id,
    instrument_id=command.instrument_id,
    
    entry=PreparedOrder(
        order_id=command.entry.order_id,
        parent_id=command.entry.parent_id,
        spec=command.entry.spec,
        broker_order_id=278,
        broker_parent_id=0,
        transmit=False,
    ),
    
    stop_loss=PreparedOrder(
        order_id=command.stop_loss.order_id,
        parent_id=command.stop_loss.parent_id,
        spec=command.stop_loss.spec,
        broker_order_id=279,
        broker_parent_id=278,
        transmit=False if command.take_profit else True,
    ),
    
    take_profit=PreparedOrder(
        order_id=command.take_profit.order_id,
        parent_id=command.take_profit.parent_id,
        spec=command.take_profit.spec,
        broker_order_id=280,
        broker_parent_id=278,
        transmit=True,
    ),
)

internal_event_queue.enqueue(prepared)
```

### 6. Thread canonique : `BracketPreparedHandler.handle(event)`

**Entrée — ordre interne `1`, ordre broker `278`**

```
entry_created = OrderCreated(
    run_id=event.run_id,
    event_id="EVT_00004",
    intention_id=event.intention_id,
    instrument_id=event.instrument_id,
    order_id=event.entry.order_id,                  # 1
    parent_id=event.entry.parent_id,                # None
    broker_order_id=event.entry.broker_order_id,    # 278
    broker_parent_id=event.entry.broker_parent_id,  # 0
    spec=event.entry.spec,                          # ENTRY
)

submit_entry = IBSubmitOrder(
    run_id=event.run_id,
    command_id="CMD_00002",
    instrument_id=event.instrument_id,
    order_spec=event.entry.spec,
    broker_order_id=event.entry.broker_order_id,
    broker_parent_id=event.entry.broker_parent_id,
    transmit=event.entry.transmit,                 # False
)
```

**StopLoss — ordre interne `2`, ordre broker `279`**

```
stop_loss_created = OrderCreated(
    run_id=event.run_id,
    event_id="EVT_00005",
    intention_id=event.intention_id,
    instrument_id=event.instrument_id,
    order_id=event.stop_loss.order_id,                  # 2
    parent_id=event.stop_loss.parent_id,                # 1
    broker_order_id=event.stop_loss.broker_order_id,    # 279
    broker_parent_id=event.stop_loss.broker_parent_id,  # 278
    spec=event.stop_loss.spec,                          # STOP_LOSS
)

submit_stop_loss = IBSubmitOrder(
    run_id=event.run_id,
    command_id="CMD_00003",
    instrument_id=event.instrument_id,
    order_spec=event.stop_loss.spec,
    broker_order_id=event.stop_loss.broker_order_id,
    broker_parent_id=event.stop_loss.broker_parent_id,
    transmit=event.stop_loss.transmit,                 # False
)
```

**TakeProfit — ordre interne `3`, ordre broker `280`**

```
take_profit_created = OrderCreated(
    run_id=event.run_id,
    event_id="EVT_00006",
    intention_id=event.intention_id,
    instrument_id=event.instrument_id,
    order_id=event.take_profit.order_id,                  # 3
    parent_id=event.take_profit.parent_id,                # 1
    broker_order_id=event.take_profit.broker_order_id,    # 280
    broker_parent_id=event.take_profit.broker_parent_id,  # 278
    spec=event.take_profit.spec,                          # TAKE_PROFIT
)

submit_take_profit = IBSubmitOrder(
    run_id=event.run_id,
    command_id="CMD_00004",
    instrument_id=event.instrument_id,
    order_spec=event.take_profit.spec,
    broker_order_id=event.take_profit.broker_order_id,
    broker_parent_id=event.take_profit.broker_parent_id,
    transmit=event.take_profit.transmit,                 # True
)
```

```
return HandlerResult(
    events=(entry_created, stop_loss_created, take_profit_created),
    commands=(submit_entry, submit_stop_loss, submit_take_profit),
)
```
### 7. Traitement du résultat par la boucle canonique

```
1. Journaliser les trois OrderCreated.
2. Mettre à jour la table de corrélation :
       broker 278 ↔ interne 1
       broker 279 ↔ interne 2
       broker 280 ↔ interne 3
3. Acheminer les commandes dans cet ordre :
       entrée → stop-loss → take-profit
```

>[!warning] Je vois apparaître le besoin de distinguer les `event` des `command`. 
>- `events` : faits à journaliser utilisé pour le replay et la projection ou comprendre une décision.
>- `command` : actions à réaliser par le système

### 8. Thread canonique : `IBSubmitOrderHandler.handle(command)`

```
def handle(self, command):
    self._ib_client.ib_loop.call_soon_threadsafe(
        self._ib_adapter.submit_on_ib_thread,
        command,
    )
```


### 9. Thread IB : `ib_adapter.submit_on_ib_thread(command)`

```
def submit_on_ib_thread(self, command):
    contract = self.resolve_contract(command.instrument_id)

    ib_order = self.convert_order(
        spec=command.order_spec,
        order_id=command.broker_order_id,
        parent_id=command.broker_parent_id,
        transmit=command.transmit,
    )

    self._ib_client.ib.placeOrder(contract, ib_order)
```

