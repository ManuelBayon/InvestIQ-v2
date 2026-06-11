## Current focus

Je suis entrain de bosser sur le runtime live (asynchrone).

- J'ai défini `RawTick` qui permet de ne plus dépendre de l'API IBKR en sortie du callback
- J'ai créé une classe `LiveRuntime` qui permet de lancer les différents processus asynchrones.
- J'ai créé `LiveRuntime.run_market_data_feed()` pour lancer la récupération des ticks par via API `ib_insync` et callback fourni .

## Hypotheses

Étant donné que l'aval du callback ne dépend plus de `ib_insync`, il me faut modifier le `TickAggregator` et définir la manière dont il recevra les données. Avant il était directement appelé par le callback avec les ticks reçu mais maintenant il est découplé la partie api externe de la canonisation / injection, il faut donc que je teste le fonctionnement de asyncio et que je construise un modèle mental minimal puis que je teste mes hypothèses.

