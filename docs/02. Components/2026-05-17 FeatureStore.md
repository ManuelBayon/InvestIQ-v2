## Responsabilités

Mettre à jour l'état des indicateurs suite à l'ingestion d'une nouvelle `Bar`.
## Inputs

La vue du marché au step courant `market: tuple[Bar, ...]`.
## Owned state

État de l'indicateur `sma_2`, `_history: dict[str, list[float]] = {"sma_2": []}`
## Outputs

Vue immuable de l'indicateur `sma_2`, `tuple[float, ...]`.
## Garanties

Garde l'historique des valeurs de l'indicateurs dans l'ordre chronologique par rapport au bar ingérées.
## Refus

Si longueur marché < 2 `Bar`, ne met pas à jour l'indicateur, n'ajoute pas de valeur à la liste.
## Out of scope

- Ne maintient pas l'état du marché, 
- Ne prend pas de décision.

---
## Attributs

- `_history: dict[str, list[float]]`
## Méthodes

- `update(self, market: tuple[Bar, ...]) -> None`
- `view(self) -> tuple[float, ...]`

---
## Évolutions à venir

- Gestion multi indicateurs,