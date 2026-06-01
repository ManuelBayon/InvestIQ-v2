
Date: 2026-05-18
Status: Updated

## Context

- Recherche des évènements canoniques
- Recherche pipeline causal `BarAvailable → Intention` 
## Problem

Je me suis rendu compte que je gère uniquement les ordres au marché ce qui est un peu naif.

---
## Decision

J'ai décidé de gérer 4 types d'ordres.

- `MarketOrder`
- `LimitOrder` 
- `Stop-Market`
- `BracketOrder`:
	- entry (market ou limite)
	- optionnel: stop-loss
	- optionnel: take-profit

**2026-05-18 :** 
- La stratégie ne produisant pas directement des ordres broker aware etc. il fallait une abstraction simple à utiliser par le développeur de la stratégie (chercheur, trader, etc.)pour exprimer son intention. 
- Pour chaque type d'ordre supporter j'ai créé une abstraction simple a utiliser de type intention utilisé dans le contrat de sortie du pipeline causale côté stratégie.

---
### `MarketOrder`

Description : Exécution immédiate sans contrainte de prix explicite.

- BUY Market : Acheter immédiatement au meilleur prix vendeur disponible.    
- SELL Market : Vendre immédiatement au meilleur prix acheteur disponible.

### `MarketOrderIntent`

```python
@dataclass(frozen=True)  
class MarketOrderIntent(Intent):  
    quantity: float  
    direction : Side
```

#### Invariants :
- Quantité
	- Quantité finie
	- Quantité strictement positive

---
### `LimitOrder`

Description : Ordre avec contrainte de prix maximale (achat) ou minimale (vente).

BUY Limit : Acheter uniquement à un prix inférieur ou égal à la limite définie.
SELL Limit : Vendre uniquement à un prix supérieur ou égal à la limite définie.

### `LimitOrderIntent`

```python
@dataclass(frozen=True)  
class LimitOrderIntent(Intent):  
    price: float  
    quantity: float  
    direction: Side
```

#### Invariants :
- Quantité
	- Quantité finie
	- Quantité strictement positive
- Prix
	- Prix fini
	- Prix strictement positif

---
### `Stop-Market`

Description : Ordre au marché sur franchissement d'un seuil.

- BUY Stop-Market: déclenche si prix monte à/au-dessus du trigger  
- SELL Stop-Market: déclenche si prix baisse à/au-dessous du trigger

### `StopMarketOrderIntent`

```python
@dataclass(frozen=True)  
class StopMarketOrderIntent(Intent):  
    trigger_price: float  
    market_order_intent : MarketOrderIntent
```

#### Invariants :
- `trigger_price`
	- fini
	- strictement positif

---

### `BracketOrderIntent`

```python
@dataclass(frozen=True)  
class BracketOrderIntent(Intent):  
    main: MarketOrderIntent | LimitOrderIntent  
    stop_market: list[StopMarketOrderIntent] | None  
    limit: list[LimitOrderIntent] | None
```

#### Invariants :
- Au moins 1 liste de `stop_loss` ou `take_profit` sinon pas d'intérêt Bracket.
- SL et TP Side doivent être opposé au Side de l'entrée
- quantité totale SL <= quantité entry
- quantité totale TP <= quantité entry

## Consequences

- Permet de tester des stratégies plus réalistes avec ordres limites, stop-loss, target-profit.

## Alternatives considered

- `MarketOrder` only → trop naif
- Ensemble complet d'ordres → over-engineering

## Invalidation conditions

- Besoin d'ordre spécifiques.
