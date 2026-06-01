## Current focus

J'ai supprimé des transitions imbriquées dans la FSM de mon `TickAggregator`. Le problème initiale était que dans certain cas plusieurs transitions devait voir le même tick par exemple : 

WARMUP + tick(new_minute) -> NEW_BAR + new WorkingBar initialized -> ACTIVE + attente

Conceptuellement le modèle revenait à faire ca : 

```
STATE_A
    -> appelle STATE_B
        -> appelle STATE_C
```

ou

``` python
if state == A:
    ...
    if state == B:
        ...
        if state == C:
            ...
```

Or en python, quand un case (match/case) a été traité il n'est pas possible d'en créé un autre du coup j'ai réduit les états et transitions à INIT, WARMUP, ACTIVE et inséré la logique de NEW_BAR dans la transition de WARMUP à ACTIVE.

Mais j'étais toujours à la recherche d'un modèle potentiellement plus propre et plus scalable pour ma machine à état que ce soit en python ou dans un autre language.

---
# Ancien modèle FSM

FSM orientée états vs FSM orientée évènements.

Au début, presque tout le monde pense :

```
Je suis dans un état.
J'appelle le handler de cet état.
Le handler décide tout.
```

Donc mentalement :

```
ACTIVE    
	-> _on_active()
```

Le problème est que progressivement les handlers deviennent énormes :

```
_on_active()    
	si cas A ...    
	si cas B ...    
	si cas C ...
```

ou pire :

```
_on_active()    
	->
_on_bar_available()    
	->
_on_new_bar()
```

La logique de transition est alors dispersée dans les handlers.

---
# Nouveau modèle 

Un handler par couple (state, event) qui produit le couple (state', effects).

