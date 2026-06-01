
## Current focus

- J'ai développé le pipeline causale côté stratégie,
- J'ai testé le pipeline causale avec des composants triviaux,
- Je suis entrain de développer la partie orchestration et replay,
- J'ai créé un `Orchestrator` avec des `handler(event)` pour chaque évènement canonique,
## Hypotheses

Mes hypothèses sont les suivantes : J'ai besoin de nouvelles abstractions / composants
### Source : 

Produit des évènements exogènes canonisés (historical bars, live feed, replay journal, Ack/reject broker, Fill broker, etc.)
### Event loop :

Consomme les évènements dans un ordre donné et décide quel composant/runtime appeler ensuite.
### Orchestrator :

Coordonne la réaction du système à un évènement : dispatch, ordre causal, journalisation, génération des identités évènementielles.

### Handler :

Traite un évènement canonique spécifique et produit éventuellement de nouveaux évènements ou des transitions d'état.

---
## Current focus

- Source
- EventLoop
- Orchestrator
- Handlers 
	- `on_bar_available(event)`
## Hypotheses

- On journalise les évènements canonique reçus dans l'event-loop
- On ajoute les nouveaux évènements canoniques émis à la file dans l'event loop.

---
# Push vs pull model for events

Modèle recommandé :

```
Backtest/replay :
Source historique/journal
→ EventLoop pull les events
```

```
Live :
Live feed push les events reçus
→ Buffer/Queue
→ EventLoop pull depuis le buffer
```

