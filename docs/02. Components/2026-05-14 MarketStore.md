## Responsabilités

- Composant runtime maintenant une vue agrégée du marché.
- Ingère une Bar 
# Inputs

- 1 `Bar`
# Owned state  

- Liste des `Bar` ingérées
# Outputs

- Vue du marché immuable `tuple[Bar, ...]`
# Garanties

- timestamp strictement croissant
- ordre d'ingestion préservé
# Refus  
# Out of scope

- Pas de features
- Pas de decision stratégies
- Pas d'aggregation de ticks

---
## Attributs :

- `_history: list[Bar]`

## Méthodes :

- `__init__()`
- `ingest(self, bar: Bar) -> None`
- `view(self) -> tuple[Bar, ...]`
