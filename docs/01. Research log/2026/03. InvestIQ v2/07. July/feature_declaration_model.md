# Feature Declaration Model
## Questions

Comment les chercheurs devraient-ils déclarer les données de marchés et les dépendances aux autre indicateurs avant l'exécution du runtime.

## Motivation

La plateforme devrait validé les dépendances des indicateurs avant l'exécution du runtime et produire un plan d'exécution déterministe compatible avec le live, backtest et le replay.

## Qu'est ce qu'un plan d'exécution ?

Dans ce contexte, un plan d'exécution est simplement la représentation explicite de : 

>Dans quel ordre faut-il calculer les choses pour respecter toutes les dépendances.

Dans un système de trading sérieux, on ne veut pas découvrir cet ordre pendant le run.

On préfère : 
```
Déclarations chercheur
        ↓
Validation
        ↓
Construction du plan
        ↓
Exécution
```

Mais pour un moteur déterministe, on veut toujours le même plan.

## Critères de succès

- dépendances explicites au données de marchés en entrée
- dépendances explicites au autres indicateurs
- ordonnancement déterministe des dépendances
- détection des dépendances manquantes
- détection des cycles
- définition agnostiques du runtime

## Exemple initial

```
MarketInput(close:AAPL) 
	↓ 
returns_1 
	↓ 
volatility_20 
	↓ 
signal
```

