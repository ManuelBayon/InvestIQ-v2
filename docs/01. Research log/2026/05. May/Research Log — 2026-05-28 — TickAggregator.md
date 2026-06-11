# Current focus

Je suis entrain de façonner mes boucles asyncio et du coup refaire le `TickAggregator`. Ce dernier était directement appelé par le callback avec les `Ticker ib_insync`, mais dorénavant la frontière se fait par RawTickBuffer. 

Dans la première version, `TickAggregator` ajoutait le tick traité dans certaines étapes de la machine à état en première position de la queue quand le même tick devait être lu par plusieurs état de la FSM.

Il faut donc que je trouve une solution propre à ce problème ma première idée, un peu naive fut de réinsérer le tick en première position de la file mais ceci casse l'architecture et la responsabilité suivante : le callback pousse dans la queue via une méthode de mutation controllé, le TickAggregator récupère les ticks via une méthode controllé et la Queue est responsable de la mutation de son propre état et représente la frontière entre l'api externe ib_insync et mon système.

# Solution

Finalement : j'ai supprimé des transitions inutiles pour garder que INIT, WARMUP et ACTIVE, NEW_BAR et BAR_AVAILABLE ont été respectivement intégré au handler de WARMUP et ACTIVE.