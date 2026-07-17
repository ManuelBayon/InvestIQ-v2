## Context

Je souhaite faire émerger le modèle des features dans mon système de recherche / exécution event-driven, déterministe, rejouable et basé sur une architecture unifiée (backtest, live, replay).

L'étape précédente était d'écrire un exemple simple de feature interdépendantes acycliques.

```
trade event -> returns_1 -> volatility_3  -> z_score_3
```

Les features ont été créé sous la forme la plus simple possible pour ne pas induire d'hypothèses implicites. 

Ceci produit des valeurs et me servira comme référence.

```python
from math import log  
from statistics import stdev, mean  
  
  
def returns_1(price: float, last_price: float) -> float:  
    if last_price == 0.0:  
        raise ValueError("returns_1 is undefined when last_price is zero.")  
    return log(price / last_price)  
  
  
def vol_3(window:list[float]) -> float:  
    if len(window) != 3:  
        raise ValueError(f"len(window)={len(window)} != 3.")  
    return stdev(window)  
  
  
def z_score_3(window: list[float]) -> float:  
    if len(window) != 3:  
        raise ValueError(f"len(window)={len(window)} != 3.")  
  
    value = window[-1]  
    m = mean(window)  
    sigma = stdev(window)  
  
    if sigma == 0.0:  
        raise ValueError("z_score is undefined when standard deviation is zero.")  
  
    return (value - m) / sigma  
  
  
  
if __name__ == "__main__":  
    prices = [100.0, 110.0, 105.0, 90.0, 92.0, 101.0]  
  
    r1 = returns_1(price=prices[1], last_price=prices[0])  
    r2 = returns_1(price=prices[2], last_price=prices[1])  
    r3 = returns_1(price=prices[3], last_price=prices[2])  
    r4 = returns_1(price=prices[4], last_price=prices[3])  
    r5 = returns_1(price=prices[5], last_price=prices[4])  
  
    v1 = vol_3([r1, r2, r3])  
    v2 = vol_3([r2, r3, r4])  
    v3 = vol_3([r3, r4, r5])  
  
    z = z_score_3([v1, v2, v3])  
  
    print(  
        f"prices={prices}\n"  
        f"r1={r1:.3f}, r2={r2:.3f}, r3={r3:.3f}, r4={r4:.3f}, r5={r5:.3f}\n"  
        f"v1={v1:.3f}, v2={v2:.3f}, v3={v3:.3f}\n"  
        f"z_score={z:.3f}"  
    )
```

## Prochaine étape

La prochaine étape pour faire émerger le modèle des features avant de parler de résolution des dépendances, de DAG, etc. est d'orchestrer simplement les features.

Pour éviter de créer des dépendances implicites et de pouvoir évaluer le modèle je vais tester une direction / hypothèse à la fois et je ne vais pas utiliser le moteur complet.

Je vais injecter des trades synthétique dans mon market_store, les récupérer via son API.

Et à partir de la créer les composant pour l'orchestration minimale fonctionnelle.

``` python
from investiq.domain.market_store import InMemoryMarketStore  
from tests.fixtures.market.simple import SIMPLE_TRADES  
  
trade_0 = SIMPLE_TRADES[0]  
trade_1 = SIMPLE_TRADES[1]  
trade_2 = SIMPLE_TRADES[2]  
  
market_store = InMemoryMarketStore()
market_store.on_trade_received(trade_0)
```

Avant cela je vais expliciter les hypothèses et invariants de l'experience.

I1 : Les trades arrivent dans un ordre déterministe (SIMPLE_TRADE fixture).
I2 : Unique symbole.
I3: Pas de timeframe on utilise les trade recus directement (ticks).
I4: Le warmup n'est pas encore géré.

## Hypothèse 1 

Je pensais pouvoir créer un composant `FeatureEngine` initialisé avec les différentes features nécessaires pour le run puis appeler chacune des features avec l'évènement canonique `TradeReceived`.

L'experience suivante à été menée, les conclusions sont décrite en dessous de cette dernières.

``` python
from collections.abc import Callable  
  
from investiq.domain.market_store import InMemoryMarketStore  
from investiq.events.trade_received import TradeReceived  
from sandbox.feature_declaration import returns_1, vol_3, z_score_3  
from tests.fixtures.market.simple import SIMPLE_TRADES  
  
class FeatureEngine:  
    def __init__(self, pipelines: list[Callable[..., object]]):  
        self._pipelines = pipelines  
  
    def update(self, event: TradeReceived):  
        for p in self._pipelines:  
            p(event)  
  
if __name__ == "__main__":  
    trade_0 = SIMPLE_TRADES[0]  
    trade_1 = SIMPLE_TRADES[1]  
    trade_2 = SIMPLE_TRADES[2]  
  
    market_store = InMemoryMarketStore()  
    feature_engine = FeatureEngine([returns_1, vol_3, z_score_3])  
  
    market_store.on_trade_received(trade_0)  
    feature_engine.update(trade_0)
```

Conclusion : 

Chaque feature a potentiellement une signature différente, ses dépendances sont multiple dans mon experiences les dépendances sont les suivantes : 

returns_1 : price: float, last_price: float
volatility_3 : window: liste des 3 derniers returns_1
z_score_3 : window: liste des 3 derniers volatility_3

Le modèle liste de callables recevant tous un `TradeReceived` ne possède pas assez d'information pour satisfaire les besoins d'entrée des features.

## Hypothèse 2

Est-ce qu’un besoin de fenêtre et un symbole commun suffit à rendre les features orchestrables ?

``` python
class InMemoryMarketStore:  

    def __init__(self):  
        self._trades: dict[str, list[TradeReceived]] = {}    
  
    def on_trade_received(self, event: TradeReceived) -> None:  
        symbol = event.symbol  
        if symbol in self._trades:  
            last = self._trades[event.symbol][-1]  
  
            if event.timestamp_utc < last.timestamp_utc:  
                raise ValueError(...)  
  
        self._trades.setdefault(symbol, []).append(event)  
  
	def window(self, symbol: str, size) -> tuple[float, ...]:  
	    window = self._trades[symbol][-size:]  
	    return tuple(float(p.price) for p in window)
```

```python
from math import log  
from typing import Protocol  
  
from investiq.domain.market_store import InMemoryMarketStore  
  
from tests.fixtures.market.simple import SIMPLE_TRADES  
  
class Feature(Protocol):  
    window_size: int  
    def compute(self, window: tuple[float, ...]) -> float:  
        ...  
  
class Returns1:  
    window_size: int = 2  
    def compute(self, window: tuple[float, ...]) -> float:  
        price = window[-1]  
        last_price = window[-2]  
        return log(price / last_price)  
  
  
class FeatureEngine:  
    def __init__(  
            self,  
            pipelines: list[Feature],  
            store: InMemoryMarketStore,  
    ):  
        self._pipelines = pipelines  
        self._market_store = store  
        self._features: dict[str, float] = {}  
  
    def update(self):  
        for p in self._pipelines:  
            if self._market_store.has_at_least("TEST_SYMBOL", p.window_size):  
                view = self._market_store.window("TEST_SYMBOL", p.window_size)  
                r = p.compute(window=view)  
                self._features["TEST_SYMBOL"] = r  
  
    def get(self, symbol: str) -> float:  
        if symbol not in self._features:  
            raise KeyError(f"unknown symbol={symbol}")  
        return self._features["TEST_SYMBOL"]
```

Ce modèle fonctionne uniquement pour les features dérivées du marché comme returns_1 mais il échoue dès que la source n'est plus le marché (vol_3, zscore, etc.).

Une feature a un besoin d'entrée caractérisé à la fois par une provenance et une profondeur d'historique.

---



