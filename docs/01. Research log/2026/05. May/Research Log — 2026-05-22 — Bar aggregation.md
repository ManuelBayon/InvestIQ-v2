## Current focus

Je me suis créé un environnement de développement contrôlé composé de 3 fonctions utilitaires me permettant de générer de manière contrôlé les primitives de l'API d'Interactive Broker : 

- `TickData`
- `Ticker`

```python
@dataclass  
class FakeTickData:  
    time: datetime  
    tickType: int  
    price: float  
    size: float  
  
@dataclass  
class FakeTicker:  
    symbol: str  
    ticks: list[FakeTickData]

def make_fake_tick(  
        timestamp_utc: datetime,  
        price: float,  
        size: float,  
        tick_type: int = 68,  
) -> FakeTickData:  
    return FakeTickData(  
        time=timestamp_utc,  
        tickType=tick_type,  
        price=price,  
        size=size  
    )  
  
def make_fake_ticker(  
        symbol: str,  
        ticks: list[FakeTickData]  
) -> FakeTicker:  
    return FakeTicker(  
        symbol=symbol,  
        ticks=ticks,  
    )
```

## Hypotheses

### H1 — Modèle d'agréation Event-driven.

Clôture de la bougie courante sur réception d'un tick après l'heure théorique.
Exemple : bougie de 09h30 clôturé dès le premier tick reçu après 09h31.
### H3 — Uniquement ticks de type 68 (delayed last price)

### H2 — Pour commencer mono-instruments

## Experiments / prototypes

### Utilisation d'une machine à états

```python
class _STATE(StrEnum):  
    WARMUP = auto()
    ACTIVE = auto()
```

### Stateful component `TickAggregator`

- `self._ticker_state: dict[str, _STATE] = {}`
- `self._working_bars: dict[str, WorkingBar] = {}`

### Steps and transitions

#### Step 1 : `Unknown`

Description : First time this ticker is received.

```
self._working_bars[ticker.symbol] = WorkingBar()  
self._ticker_states[ticker.symbol] = _STATE.INIT
```

#### Step 2 : `_State.INIT`

Description: Initialize first `tick.time` in order to wait for a new minute to start (synchronisation).

- Set `WorkingBar.timestamp = tick[0].time`
- Set `_State.WARMUP` (transition)
#### Step 3 : `_State.WARMUP`

Description wait for `_is_new_minute(reference, current)` to return true.

- Set `_State.NEWBAR` (transition)

#### Step 4: `_State.NEW_BAR`

Description : Initialize new `WorkingBar` for that ticker, set all attributes except close.

- Set `WorkingBar.timestamp = tick[x].time`
- Set `WorkingBar.open = tick[x].price`
- Set `WorkingBar.high = tick[x].price`
- Set `WorkingBar.low = tick[x].price`
- Set `WorkingBar.volume = tick[x].size`
- Set `_State.ACTIVE` (transition)
#### Step 3.1 : `_State.ACTIVE`

Description : Wait for ticker updates

- `if tick.price > WorkingBar.high` then `WorkingBar.high = tick.price`
- `if tick.price < WorkingBar.low` update `WorkingBar.low = tick.price`
- `WorkingBar.volume += tick.size`
- if `_is_newbar(bar.open, tick.time) == True` then `_State.EMIT` (transition)
#### Step 3.2 : `_State.BAR_AVAILABLE`

- Build `BarAvailable`
- Add `BarAvailable` to list to return it at the end of function call.
- Set `_State.NEW_BAR` (transition)
## Observations
## Breakages / ambiguities

## Decisions emerging

## Open questions

## Next iteration