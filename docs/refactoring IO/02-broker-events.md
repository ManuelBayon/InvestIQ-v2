# Événements broker entrants

## Structure

Trois payloads immuables : `OrderStatusUpdated`, `FillReceived`, `CommissionReportReceived`. Conserver les noms existants évite un renommage sans gain fonctionnel. Métadonnées de réception dans l’enveloppe commune ; aucun héritage imposé depuis ExternalEvent.

`IntentGenerated` est interne : il ne fait pas partie de ces contrats.

Canonicaliser signifie stabiliser le sens, les types et les références ; cela ne nécessite pas d’effacer les faits du broker. Aucune commande, gestion de position ou coordination OCO n’est définie ici.

## Référence commune : BrokerOrderRef

| Champ proposé | Type        | Justification                                                                                                                    |
| ------------- | ----------- | -------------------------------------------------------------------------------------------------------------------------------- |
| client_id     | int         | Client API qui a soumis l’ordre ; évite de traiter orderId comme globalement unique.                                             |
| order_id      | int         | Référence API de l’ordre, fournie par les notifications.                                                                         |
| permanent_id  | int ou None | Référence persistante IBKR lorsqu’elle est disponible ; conserve le lien supplémentaire sans en faire un prérequis de réception. |

Mapping : clientId, orderId, permId. L’absence de permId est normalisée en None selon la convention source. Le contexte du run conserve le broker, le compte et la session ; cette référence n’est pas déclarée universellement unique entre tous les runs. Le simulateur fournit les mêmes propriétés de référence. BrokerOrderRef regroupe des observations d’identité : l’apparition ultérieure de permanent_id ne signifie pas un nouvel ordre.

Cette petite structure assume le contexte IBKR actuel. Une abstraction multi-broker n’est pas nécessaire maintenant. L’ordre interne et sa correspondance avec cette référence seront étudiés séparément.

## OrderStatusUpdated

Fait : état rapporté par le broker, sans garantie qu’il s’agisse d’une transition nouvelle.

| Champ proposé      | Type              | Justification                                                                                                               |
| ------------------ | ----------------- | --------------------------------------------------------------------------------------------------------------------------- |
| order_ref          | BrokerOrderRef    | Identifie l’ordre observé.                                                                                                  |
| parent_order_id    | int ou None       | Conserve la parenté rapportée, utile aux ordres attachés ; même contexte client que l’ordre. Mapping parentId, 0 vers None. |
| status             | BrokerOrderStatus | Enum explicite des états acceptés ; interdit les chaînes arbitraires.                                                       |
| filled_quantity    | Decimal           | Quantité cumulée exécutée rapportée dans cet état. Observation broker, pas création de fills.                               |
| remaining_quantity | Decimal           | Quantité restante de cet ordre rapportée par le broker ; ne signifie pas position restante du portefeuille.                 |

Mapping initial proposé des statuts, sans fusion prématurée : ApiPending → API_PENDING ; PendingSubmit → PENDING_SUBMIT ; PreSubmitted → PRE_SUBMITTED ; Submitted → SUBMITTED ; PendingCancel → PENDING_CANCEL ; ApiCancelled → API_CANCELLED ; Cancelled → CANCELLED ; Filled → FILLED ; Inactive → INACTIVE.

INACTIVE n’est pas traduit automatiquement en REJECTED. Les causes de rejet peuvent nécessiter le canal d’erreurs IBKR : ces trois événements ne couvrent pas à eux seuls tous les incidents broker.

Invariants : quantités finies et >= 0 ; statut reconnu. Ne pas imposer de monotonie ni déduire une transition des seules notifications. Parenté ne signifie pas appartenance à un groupe OCO ; aucun rôle TP/SL n’est inféré.

## FillReceived

Fait : une exécution individuelle, éventuellement partielle.

| Champ proposé | Type | Justification |
|---|---|---|
| order_ref | BrokerOrderRef | Rattache le fill à son ordre externe. |
| execution_id | str | Identité d’exécution fournie par IBKR ; conserver execId intégralement. |
| symbol | str | Même convention que TradeReceived ; rattachement explicite à l’instrument du contrat reçu avec le fill. |
| timestamp_utc | datetime UTC | Temps d’exécution communiqué par la source. |
| side | Side | Enum BUY/SELL ; normalisation BOT → BUY et SLD → SELL. |
| quantity | Decimal | Quantité exécutée par ce fill uniquement, depuis shares. |
| price | Decimal | Prix exécuté hors commissions. |

Pour le fill, lire les identifiants dans Execution plutôt que dans un état d’ordre mutable observé à un autre instant. Valider le compte reçu contre celui du run avant publication.

Invariants : execution_id et symbol non vides ; instrument attendu ; timestamp avec fuseau UTC ; quantité finie > 0 ; prix fini ; sens reconnu. Pas d’interdiction universelle des prix négatifs.

Champs retirés : parent_id (relation d’ordre, pas propriété du fill) et cumul_qty (redondant pour décrire cette exécution individuelle). Le cumul fourni par IBKR peut rester dans la trace brute si nécessaire. Aucun calcul de position ou traitement des doublons n’est implémenté dans ce contrat.

## CommissionReportReceived

Fait : rapport de commission associé à une exécution.

| Champ proposé | Type | Justification |
|---|---|---|
| execution_id | str | Clé de rattachement à l’exécution, issue de execId. |
| commission | Decimal | Montant rapporté ; ne pas imposer un signe positif qui exclurait un crédit. |
| currency | str | Devise du montant rapporté. |

Invariants : référence non vide ; commission finie ; devise non vide normalisée selon la convention retenue. Vérifier les sentinelles de l’API avant conversion : une sentinelle numérique finie n’est pas nécessairement un montant valide.

order_id et parent_id retirés : le rapport est lié à une exécution ; les recopier impose un enrichissement inutile. realized_pnl retiré du contrat minimal : mesure calculée par le broker, distincte des frais. Sa conservation éventuelle pour réconciliation sera étudiée avec la comptabilité.

Le rapport doit pouvoir être reçu avant que son fill ait été traité. La politique de répétition/révision est différée ; aucune accumulation ni règle « dernière réception gagne » n’est introduite ici.

## Normalisation et erreurs

Même règle que TradeReceived : conversion explicite avant construction, types décimaux, aucune dépendance aux objets IBKR dans le payload. En phase synthétique, une valeur invalide ou un statut inconnu lève une exception et arrête le scénario. Le wrapper utilisé et sa version doivent être confrontés à ces mappings avant implémentation.

Les références externes sont préservées sans décider de leur déduplication. Les corrections d’exécution IBKR doivent conserver leur execId complet ; leur traitement économique reste un sujet ultérieur. Aucun timestamp source n’est inventé pour un statut ou un rapport de commission qui n’en fournit pas.

## Sources techniques

- [IBKR — Order Status](https://www.interactivebrokers.com/docs/tws-api/doc/order-management/order-status) : callback et états.
- [IBKR — Execution](https://interactivebrokers.github.io/tws-api/classIBApi_1_1Execution.html) : références, side, shares, price et corrections. Référence historique correspondant aux objets utilisés ; vérifier la version d’intégration.
- [IBKR — CommissionReport](https://interactivebrokers.github.io/tws-api/classIBApi_1_1CommissionReport.html) : execId, commission, currency et realizedPNL. Référence historique.

## Décisions à valider

BrokerOrderRef ; conservation des quantités observées dans OrderStatusUpdated ; retrait du cumul du fill et du PnL du rapport de commission. La convention exacte de symbol reste celle à finaliser pour TradeReceived. Aucun nouveau contrat n’est déclaré figé par cette note.
