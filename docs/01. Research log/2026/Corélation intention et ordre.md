## Hypothèse 

- Un seul client par run ⇒ `client_id` = 1
- Un seul compte par run ⇒ account_num=DUK2...7

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
## Problème 

Je voudrais pouvoir relier le retour broker à l'ordre interne et l'intention qui l'a produite.

### - Avant soumission

```
Order:
	order_id=278 # Connu avant soumission
	parent_id=0 # Connu avant soumission
	
	intention_id="EVT_00002" # Connu avant soumission	
	
	status="Created" # Initialisé avant soumission
```

```
Order:
	order_id=279 # Connu avant soumission
	parent_id=278 # Connu avant soumission
	
	intention_id="EVT_00002" # Connu avant soumission	
	
	status="Created" # Initialisé avant soumission
```

```
Order:
	order_id=280 # Connu avant soumission
	parent_id=278 # Connu avant soumission
	
	intention_id="EVT_00002" # Connu avant soumission	
	
	status="Created" # Initialisé avant soumission
```

### - `statusEvent`

Déclenchement du callback par `ibinsync` : 

```
statusEvent:
	order_id=279
	parent_id=278
	status="PreSubmitted"
```

```
Order:
	order_id=279 # Connu avant soumission
	parent_id=278 # Connu avant soumission
	
	intention_id="EVT_00002" # Connu avant soumission	
	
	status="PreSubmitted" # Mis à jour
```

### - `statusEvent`

Déclenchement du callback par `ibinsync` : 

```
statusEvent:
	order_id=280
	parent_id=278
	status="PreSubmitted"
```

```
Order:
	order_id=280 # Connu avant soumission
	parent_id=278 # Connu avant soumission
	
	intention_id="EVT_00002" # Connu avant soumission	
	
	status="PreSubmitted" # Mis à jour
```

### - `statusEvent`

Déclenchement du callback par `ibinsync` : 

```
statusEvent:
	order_id=278
	parent_id=0
	status="PreSubmitted"
```

```
Order:
	order_id=278 # Connu avant soumission
	parent_id=0 # Connu avant soumission
	
	intention_id="EVT_00002" # Connu avant soumission	
	
	status="PreSubmitted" # Mis à jour
```

### - `fillEvent`

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

### Hypothèse :

- `fillEvent` met à jour les champs comptable de l'ordre.
- les champs comptable sont interne à l'ordre ?
- `statusEvent` mute uniquement le champs `status` de l'ordre.

## Interrogation architecturale

Quel modèle pour les ordres, je pensais à `EventSourcing`. Quels sont les alternatives ainsi que leurs avantages et inconvénient respectifs ? 

| Approche                           | Principe                                                                                                     | Avantages                                                                         | Inconvénients                                                                                                                 |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **État courant**                   | Tu conserves une fiche `Order` et mets ses champs à jour.                                                    | Simple à comprendre ; lecture directe ; peu d’infrastructure.                     | Les anciennes valeurs sont perdues sans historique ; difficile d’expliquer comment on est arrivé à cet état.                  |
| **État courant + journal d’audit** | Tu conserves la fiche actuelle et un historique des changements. La fiche reste la référence opérationnelle. | Consultation simple et traçabilité ; utile pour enquêter sur une anomalie.        | Il faut garantir la cohérence entre état et journal ; le journal n’est pas nécessairement suffisant pour reconstruire l’état. |
| **Event sourcing**                 | Les événements persistés font autorité. L’état courant est calculé à partir de leur succession.              | Reconstruction de l’état, analyse historique, possibilité de recalculer des vues. | Évolution des schémas d’événements, rejeu, ordre d’application et gestion des doublons demandent de la rigueur.               |
Source : ChatGPT

---

Poursuivre la recherche du modèle pour les ordres mais la solution suivante est envisagée : 

- Source de vérité : évènements 
	- externes : `statusEvent`, `fillEvent`, `commissionReport`
	- internes: `IntentGenerated`,  `RiskRejected`, etc.
- Les évènements sont journalisé et éventuellement persistés
- Projection le l'état d'exécution à partir des évènements canoniques et de projecteurs déterministes :
	- État des ordres, 
	- État des positions, 
	- État du portefeuille,
	- État du PnL .

Justification : Unicité de la source de vérité (journal canonique des évènements).

```
Journal canonique
      ↓
 ┌────┼──────────┬──────────┐
 ↓    ↓          ↓          ↓
OMS  Position  Portfolio    PnL
```
