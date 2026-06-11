## Current focus

Développement du runtime live, dernier composant terminé : `TickAggregtor`.

Le problème auquel je fais face dans le modèle actuel est que mon callback est bloquant ce qui était explicitement à éviter selon la documentation de l'API interactive broker.

Le modèle actuel fait : 
```
ticks IBKR
	-> callback
		-> aggregation
		-> ingress
		-> ...
```

## Hypothèses

2026-05-26 :

Je propose de créer 3 boucles asynchrone pour faire tourner le modèle d'ingestion des données et le premier pipeline causal côté stratégie `BarAvailable -> Intention| NoOperation`:

1. Boucle d'injection des données via le callback IBKR et push dans la file d'attente des ticks reçus.
2. Boucle qui produit l'évènement canonique `BarAvailable` à partir de la file d'attente des ticks reçus et pousse l'évènement dans la boucle évènementiel principale.
3. La boucle principale qui itère sur les évènements canoniques (par ex. `BarAvailable`, `IntentionGenerated`, etc.)

---
Un composant **"Worker"** est :

- un composant actif,
- qui exécute une boucle de travail,
- sur une source de données / queue.

Donc :
- il orchestre un sous-flux ;
- il possède une boucle ;
- il consomme une queue / source ;
- il produit / transfère quelque chose ;

En ce qui me concerne j'ai un `Worker` à l'interface entre la `raw_tick_queue` alimentée par le callback IBKR et la boucle principale (pipeline déterministe de décision et exécution).

Ce worker va s'appeler `MarketDataWorker`.

## Experiments / prototypes

## Observations
## Breakages / ambiguities

## Decisions emerging

## Open questions

## Next iteration