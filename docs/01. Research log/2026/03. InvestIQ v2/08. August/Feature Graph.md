
Ce qui est géré : 

- Actuellement le graph d'indicateurs permet de gérer plusieurs parents et plusieurs enfants.
- A partir des dépendances (sources) ainsi que la racine il reconstruit le graph.
- La politique actuelle est la suivante : un noeud devient éligible lorsque **tous ses parents ont émis pendant le Trade courant**.

Ce qui n'est pas encore géré : 

- il ne gère pas encore les features cross asset et les problématiques qui y sont liées.
- L'intégration dans le runtime, actuellement le prototype existe dans la sanbox, je pensais créer un runtime validé et initialisé et figé au bootstrap.









