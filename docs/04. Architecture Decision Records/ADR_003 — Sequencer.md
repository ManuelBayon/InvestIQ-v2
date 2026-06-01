## Context

Après avoir créé le premier sous-système causal `BarAvailable -> IntentGenerated | NoOperation` il me faut orchestrer l'injection des données de marché après canonisation (`BarAvailable`) avec comme contrainte un pipeline unifié live-backtest-replay.

Actuellement j'ai les composant suivant : 
- Les composants constituant le pipeline causale Bar to Intention.
- Un orchestrateur qui détient le mapping évènement -> handler ainsi que les handler pour chaque type d'évènement canonique
- Une event-loop en cours de développement qui détient une file d'attente pour les évènement et les différents composant peuvent ajouter un évènement notamment pour les évènements exogènes car les évènements endogènes sont récupéré par l'event-loop et ajouté directement. L'event-loop a également la responsabilité de journaliser les évènements ajouté sur la file d'attente ou vu par les handlers à définir à quel moment mais c'est elle qui journalise.
## Problem

Le problème que j'ai : 

Mon composant MarketDataFeed ne peut pas créér BarAvailable sauf si il détient run_id, event_id mais ca entrerai en conflit avec la responsabilité de récupérer les bars, la canonisation soit se faire dans une autre composant et aussi l'event-loop a aussi besoin de run_id, event_id etc.
## Decision

Création d'un composant qui détient run_id et next_event_id permettant de l'injecter dans les composants qui en ont besoin et avoir une seule source de vérité partagé.
## Consequences

Ainsi on l'état en lecture seule peut être partagé aux composants en ayant besoin.

## Alternatives considered

## Invalidation conditions
