
Question de design : Faut til faire porter le symbole par le RawTick, pas sur.

---

Mettre un invariant temporel pour s'assurer que les données le MarketStore soit ordonnés temporellement sinon les features ne sont pas cohérentes.

---
Sinon j'ai fait des tests sur mon FeatureStore trivial pour tester l'intégration naive Tick -> TickAvailable -> Queue -> EventLoop -> Orchesrator -> Handler Chaine causale décision.
