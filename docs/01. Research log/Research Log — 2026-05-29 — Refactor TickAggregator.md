# Context 

Suite à la définition de la frontière matérialisé par le RawTickBuffer, TickAggregator ne dépend plus des schémas de données définis dans le package `ib_insync`.

Aussi, la nécessité de pousser en amont de la file le tick précédement traité a mis en lumière une défaillance du modèle actuel.

Pour finir, je n'arrivais à garder le modèle complet du TickAggregator et les modifications n'étaient pas forcément réalisé en total maitrise.

Pour répondre au points mentionnés ci dessus j'ai décidé de factoriser et tester les sous système composant le TickAggregator puis teste l'intégration de ces derniers.

---
# Refactor n°1

Jusqu'à présent le signal de cloture / ouverture d'une nouvelle bar était basé sur une différence de temsp (timedelta). Le problème avec ce type de signal est que le signal "drift" se décale dans le temps.

Exemple : 1er tick de la bougie reçu à 09:00:15, pour des bougies de 1min, la cloture / ouverture se produirait au premier reçu après 09:01:15 si le premier tick recu est a 09:01:25 on dévie et c'est assez problématique et en plus relativement simple à corriger.

L'objectif de ce refactor est de produire une méthode qui produit un signal plus propre même si il n'est pas optimal. L'idée c'est de ne plus dépendre des ticks recu mais de controler le temps utc et lorsqu'une nouvelle minute est détectée on cloture directement la bougie en cours même si aucun tick n'a été reçu. 

Biensur on pourrait se dire ok mais qu'en est-il de la synchronisation entre les données émises par l'exchange et le temps local et oui comme dit ce modèle n'est pas parfait, ci après un exemple pour l'illustrer.

Première question : quelle référence temporelle, protocole de syncrhonisation temportelle, heure du pc, etc.

Seconde question : à quelle fréquence rafraichir le tickaggregator, à priori dépend de la tolérance max.

Pour l'exemple nous prenons une référence temporelle arbitraire (heure pc) et une fréquence de raffraichissement de max toute les secondes.

Imaginons que je souhaite produire des bougies de 1 minute.

heure pc passe de 09:00:59 à 09:01:00.x -> signal cloture/ouverture de la bougie même si aucun tick n'a été reçu.


