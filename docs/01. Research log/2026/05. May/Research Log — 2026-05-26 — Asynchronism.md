## Current focus

J'ai besoin d'asynchronisme pour pouvoir lancer plusieurs boucles en parallèle notamment à ce stade :  
- callback IBKR : recoit ticks et les pousse dans une file d'attente
- boucle secondaire : agrège les ticks en `Bar` et pousse l'évènement canonique `BarAvailable` dans la boucle évènementielle primaire.
- la boucle d'exécution primaire qui orchestre les évènements canonique en appelant le handler correspondant selon la politique d'ordre de traitement des évènements.

Le callback et les différentes boucles mentionnées ne doivent pas être bloquante car le fonctionnement voulu du programme ne pourrait pas être garanti.

Pour ce faire j'ai besoin de d'élargir mon champ de compréhension de l'asynchronisme et plus particulièrement en python.

---
#### Mode débogage spécifique (à noter)

---
## Decisions emerging

## Open questions

## Next iteration