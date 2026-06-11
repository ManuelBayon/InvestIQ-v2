Cette chaine comprends l'orchestration de : 
- MarketStore
- FeatureStore
- DecisionLayer

Le flux ressemble a quelque chose comme : 
EventLoop -> TickDataAvailable -> Orchestrator -> TickDataAvailabaleHandler -> NoOperation | IntentGenerated.

---
**Question :** A qui incombe la responsabilité d'inclure les méta donnés suivante : 
- run_id, 
- event_id, 
- causation_id,
- decision_context

plutot decision layer, handler, autre ?

**Réponse :** 

DecisionLayer  
→ produit l’intention métier  
→ produit decision_context
  
Handler / EventFactory  
→ ajoute run_id  
→ ajoute event_id  
→ ajoute causation_id  
→ ajoute meta_data

--- 
Actuellement étant toujours en recherche du contrat causal, d'une démarche de séparation des responsabilités propre je propose de mettre naivement comme contexte de décision les dernières valeur de lensemble des symboles dans le market store ainsi que la derniere valeur de chaque feature ayant produit une valeur. 

Le but étant de définir une chaine causal de décision fonctionnel et la faire évoluer selon besoin.







