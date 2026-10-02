
## Hypothèse 

Ma stratégie produit une intention de trading ensuite convertie en ordre broker :

```
BraketOrderSpec:
	parent=MarketOrderSpec(BUY, 1.0)
	stoploss=Stoploss(price)
	takeprofit=TakeProfit(price)
``` 

Pour chaque ordre de `BracketOrder` : 
- `IBAdapter` soumet l'ordre
- `IBAdapter` s'abonne aux évènements (status, fill, commissionReport)

Déclenchement du callback par `ibinsync` : 

```
statusEvent:
	order_id: 279
	status="PreSubmitted"
	perm_id: 994812042
	parent_id: 278
```

---
## Problème 

Je voudrais pouvoir relier le retour broker à l'ordre interne et l'intention qui l'a produite.

### Structure de donnée

```
Order:
	order_id: 001 # Connu avant soumission
	group_id: G01 # Connu avant soumission
	intention_id="EVT_XXXXX" # Connu avant soumission
	
	broker_order_id: 279 # Inconnu avant soumission
	broker_parent_id=278 # Inconnu avant soumission
	status: "PreSubmitted" # Inconnu avant soumission
```

>[!note] Pour étudier le rattachement d'un retour broker à l'ordre interne et à son intention d'origine, je laisse provisoirement le type mécanique hors du modèle.

### Mise en oeuvre

Dans le gestionnaire associé à l'évènement `IntentGenerated`, créer un ordre interne : 

```
Order:
	order_id: 001
	group_id: G01
	intention_id: "EVT_XXXXX"
	status: "Created"
	
	broker_order_id: None
	broker_parent_id: None

Order:
	order_id: 002
	group_id: G01
	intention_id: "EVT_XXXXX"
	status: "Created"
	
	broker_order_id: None
	broker_parent_id: None

Order:
	order_id: 003
	group_id: G01
	intention_id: "EVT_XXXXX"
	status: "Created"
	
	broker_order_id: None
	broker_parent_id: None
```


















