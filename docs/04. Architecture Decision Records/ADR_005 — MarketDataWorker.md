## Context

Dans le cadre du développement du runtime live, je m'interroge sur les modèles de récupération des données et d'injection dans le pipeline principal.

## Problem

**2026-05-26**

Le problème auquel je fais face dans le modèle de runtime actuel est que mon callback  fourni à IBKR est bloquant alors qu'il avait explicitement conseillé d'éviter ce comportement pour éviter de bloquer la boucle de récupération des données.

Le modèle actuel fait : 
```
ticks IBKR
	-> callback
		-> aggregation
		-> ingress
		-> ...
```

## Decision

Création de 2 boucles asynchrones en plus du callback orchestré par l'API IBKR.

- callback IBKR: `on_pending_ticker(tickers)`

- Boucle secondaire :
	- agrégation,
	- canonisation,
	- injection des données dans la boucle principale.

- Boucle principale :
	- décision
	- risque
	- construction ordre
	- gestion ordre
	- exécution
	- portefeuille
	- etc.

Ce qui nous intéresse dans décision d'architecture c'est la boucle secondaire d'agrégation / injection. Le composant orchestrant cette boucle sera nommé `MarketDataWorker`.

## Consequences

- Indépendance des 3 boucles.

## Alternatives considered

- callback ibkr bloquant

## Invalidation conditions