# InvestIQ v2

Personal R&D project exploring the design of a deterministic event-driven trading runtime.

## Objectives

The goal is not to build a profitable trading strategy.

The objective is to understand how professional trading systems are constructed by focusing on:

- deterministic processing,
- explicit state ownership,
- event-driven architecture,
- unified pipeline across backtest, live and replay,
- replayability,
- auditability,
- reproducible research workflows (code, tests, experiments and documentation are versioned together).

Core principle:

make quantitative research reproducible by linking results to a specific commit, configuration and set of parameters.

same code + same configuration + same input events = same observable behavior

## Current Architecture

- The runtime consumes canonical events from a central queue and processes them sequentially through dedicated handlers.
- External systems publish data into the runtime as canonical events.

## Current flow:

RawTick
→ TickDataAvailable
→ MarketStore
→ FeatureStore
→ DecisionLayer
→ IntentGenerated

## Current Scope

Implemented:
- canonical event queue
- event loop
- orchestrator
- market data ingestion
- market store
- feature store
- decision layer integration
- event journal
- runtime tests

In progress:

- order submission
