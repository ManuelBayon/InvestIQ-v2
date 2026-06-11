# Besoin concret

- Référence mondiale commune pour comparer temps évènements.
- Ordering cohérent
- Mesure correcte des latences
- Reproductibilité
- Synchronisation règlementaire (HFT)
- Monotonicité pratique
- Résistance au perturbations

---
# Temps atomique international (TAI)

Le TAI sert fondamentalement à fournir une échelle de temps continue et extrêmement stable basée sur une transition particulière de l’atome de césium-133.

Une seconde correspond à 9 162 631 770 oscillations.

Environ 500 horloges dans plus de 70 laboratoires maintiennent cette échelle.

---
# Temps universel (UT1)

- UT1 est une coordonnée temporelle dérivée d’une orientation astronomique.
- UT1 est basé sur l'orientation instantanée réelle de la terre.
- Le cycle fondamentale de UT1 correspond à la rotation quotidienne de la terre bien qu'elle soit adapté à la rotation annuelle de la terre autour du soleil dans les méthodes avancés.
- UT1 est physiquement pertinente mais pas parfaitement stable.

---
# Temps universel coordonné (UTC)

Le rôle d'UTC est essentiellement de fournir une référence mondiale stable.

Elle est construite afin de satisfaire 2 contraintes : 

1. La seconde UTC est égale à la seconde du TAI.
2. UTC doit être à moins de 0.9s du temps universel (UT1).

Grâce à un mécanisme d'ajustement mis en œuvre chaque fois que nécessaire, UTC est décalé d'une seconde pour satisfaire la contrainte (2) ci-dessus.

Depuis le 1er janvier 2017, jour de la dernière insertion d'une seconde intercalaire au temps universel coordonné (UTC), le TAI est en avance de 37 secondes sur l'UTC. Ces 37 secondes proviennent des 10 secondes de différence initiales plus 27 ajouts se secondes intercalaires à l'UTC depuis 1972.

---
# Heure UNIX / POSIX

L'heure Unix ou heure POSIX est une mesure du temps fondée sur le nombre de secondes écoulées depuis le 1er janvier 1970 00:00:00 UTC, hors secondes intercalaires.

Elle est principalement utilisé dans les système qui respectent la norme POSIX, dont les systèmes de type UNIX, d'où son nom.

NB : la date du 1er janvier 1970 00:00:00 UTC est appelée "époque UNIX".

Elle est très utilisé dans les systèmes informatiques car ces derniers ont besoin de simplicité opérationnelle et de modèle de temps linéaire simple à manipuler plus que d'une fidélité astronomique parfaite.

---
# Représentation du temps

Les échelles de temps sont essentiellement des systèmes de coordonnées temporelles.

Année, mois, jour, heures, minutes, secondes ne sont que des représentations calendaires humaines appliquées à ces échelles de temps.

---
# Le temps dans les systèmes informatiques mondiaux

## Temps coordonné mondial

>Sert à répondre : "quand ?"

Dans la plupart des systèmes **non HFT** on manipule du temps POSIX aligné sur UTC.

Les secondes intercalaires sont souvent ignorées opérationnellement dans la plupart des applications de trading **non HFT**.

Le drift des oscillateurs locaux est régulièrement corrigé via des mécanismes de synchronisation tels que NTP afin de maintenir l’erreur temporelle sous une certaine tolérance.

Pour communiquer vers ou depuis le monde extérieur on projette ou normalise le temps de POSIX vers UTC ou inversement de UTC vers POSIX
```python
2025-05-08T15:00:00Z <=> 1746716400
```
où Z = UTC.

## Temps monotone local

>Sert à répondre "combien de temps ?"

- mesure de durée
- latence
- timers
- benchmarking
- scheduling

---
# Trading 

Dans le monde réel : 

- Fuseaux horaires
- Passage heure d'été / heure d'hiver

Pour savoir si un évènement mondial est arrivé avant ou après un autre le plus simple est de convertir tous les temps locaux au format UTC et de comparer les temps UTC.

Aussi, il est important de ne pas confondre les temps correspondant à des évènements de nature différentes même si ils sont liés à la même information brute.

Par exemple pour l'émission d'une donnée de marché, il faut clairement séparer : 

- temps exchange  
- temps réception  
- temps traitement  
- temps décision
- etc.

Ces différents temps ne représentent pas la même causalité.

---
# InvestIQ

Dans mon système je ne fais pas de HFT et même en live ce qui compte pour moi avant tout c'est le timestamp de la donnée de marché. 

`time == timestamp du tick`.



