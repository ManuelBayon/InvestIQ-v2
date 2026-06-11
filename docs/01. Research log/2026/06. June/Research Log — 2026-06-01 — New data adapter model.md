J'ai décidé de supprimer le tickaggregator car je me suis rendu compte qu'avoir des bougies d'une durée x n'était pas important pour moi actuellement ce dont j'ai besoin c'est de la dernière et éventuellemenrt des dernières données de marché pour calculer des indicateurs par contre les regrouper et simplifier en OHCLV n'était pas importnat et constituait une perte dinformation significative deplus si j'en ait vraiment besoin je peux toujours le faire mais plutot sous forme de feature.

Par conséquent mon évènement canonique éxogène devient `TickDataAvailable` avec un payload qui sera un `dict[str, list[rawTick]]`.

---
Je me posais du coup comme question, a qui incombe la responsabilité de remplir les champs run_id et event_id qui sont commun a tous les évènements, déjà ce qui me paraissait évident c'est que la source de vérité pour ces 2 champs devait être unique et modifiable par une seule entité via éventuellement une méthode d'accès controllé. 

J'avais comme idée de passer aux composants produisant des évènements canoniques un composant qui détient les champs communs aux évènements canoniques et qui complete levenenemnt brut pas exemple 

Pour :
```python
TickDataAvailable(  
    run_id=,  
    event_id=,  
    causation_id=None,  
    meta_data={},  
    payload=list_raw_ticks  
)
```

- `causation_id` est None,
- `meta_data` est optionnel et vide pour l'instant,
- payload contient la liste des ticks reçu pour chaque `symbol` auquel on est abonné,

Le composant en question appelé par exemple `CanonicalEventFactory` complète systématiquement les champs commun prévus comme run_id et event_id.

---
`IBLiveMarketDataFeed` = pousser les ticks recu et canonisé en `RawTick` dans la queue, ordonné par instrument (symbol).

`CanonicalEventQueue` = transport / frontière entre la normalisation apres réception market data et la boucle évènementiel et orchestrateur.





