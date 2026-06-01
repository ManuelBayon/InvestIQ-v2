
Je développe actuellement la méthode qui produit le signal d'ouverture / fermeture d'une nouvelle bougie.

Paramètre exogène : résolution bougie (1min, 5 min, etc.).

Hypothèse : 1
Temps entre deux appel de la méthode <= résolution bougie.

Limite associé à l'hypothèse 1 : comportement non garanti et potentiellement incohérent si la fréquence rafraichissement est supérieure à la résolution demandé. 

---
Expérience cas limite hypothèse 1: 

- Temps entre deux appels = 1min
- Instant d'invocation de la méthode xx:yy:30.

La méthode sera appelé toutes les minutes mais à la 30ème seconde dans ce cas le modèle est potentiellement encore pire que le précédent modèle basé sur une delta temporel.

Conclusions : 

- La propriété temps entre deux appels inférieur n'est pas la bonne. 
- Il faudrait que la méthode soit appelé au plus proche de 0 seconde de la nouvelle minute que possible en admettant que la résolution des bougies ne puissent pas être inférieure à 1 min avec ce modèle.

---
Hypothèse 2 : Invocation méthode au plus proche de la seconde 0.

---
# moyen de mise en œuvre de l'hypothèse 2

La solution choisie est la suivante : Scheduler externe produisant l'évènement canonique `BarBoundaryReached` et le pousse dans la boucle évènementielle principale.

Cette solution me permet de simplifier le modèle tout en rendant l'implémentation du signal produit interchangeable et composable au bootstrap.

Conceptuellement la source de temps est configuré au démarrage et tourne indépendamment, lorsqu'elle détecte qu'une nouvelle bar doit être émise elle pousse l'évènement correspondant la boucle évènementielle et cette dernière en fonction de sa politique d'ordre de traitement appel le handler associé qui fait appel au tickaggregator demande la clôture de la working bar courante.

Ceci produit à un intervalle défini à l'avance des bougies immuables.

En revanche les modèles de décision, risque etc. ont besoin de connaître le prix courant du marché il faut donc distinguer bougies historique et bougie courante.

La bougie courante peut contenir OHCLV ou alors la liste de tous les ticks pour la dernière période par exemple 1 minute etc a définir.












