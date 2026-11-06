"""APERÇU POUR REVUE — non intégré au moteur.

Destination proposée : contracts/inputs pour les événements canoniques.
Les références techniques et le registre restent dans adapters/ibkr.
OrderStatus et son mapping doivent encore être validés.
Les validations d'exécution seront ajoutées dans les fichiers définitifs.
"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import StrEnum


# contracts/order_id.py
@dataclass(frozen=True, slots=True)
class OrderId:
    """Identité globale, opaque et stable d'un ordre logique.

    Créée avant soumission. Le générateur est extérieur au contrat.
    Exemple de génération : UUID ; aucun identifiant IBKR ici.
    """

    value: str


# contracts/side.py
class Side(StrEnum):
    BUY = "BUY"
    SELL = "SELL"


# Type provisoire pour cet aperçu : enum à définir avant intégration.
OrderStatus = str


# contracts/inputs/order_status_received.py
@dataclass(frozen=True, slots=True)
class OrderStatusReceived:
    """Observation broker après corrélation vers l'ordre interne.

    Quantités finies et >= 0. remaining_quantity concerne cet ordre,
    pas la position du portefeuille. Une réception peut être répétée.
    """

    order_id: OrderId  # Identité interne obtenue via le registre.
    status: OrderStatus  # État normalisé ; mapping encore à valider.
    filled_quantity: Decimal  # Cumul exécuté annoncé par le broker.
    remaining_quantity: Decimal  # Reliquat annoncé pour cet ordre.


# contracts/inputs/execution_received.py
@dataclass(frozen=True, slots=True)
class ExecutionReceived:
    """Une exécution individuelle rapportée, hors commissions.

    execution_id et symbol non vides ; timestamp conscient du fuseau UTC ;
    quantité finie > 0 ; prix fini ; side dans BUY/SELL.
    L'identité d'exécution est externe, qualifiée par la source du run.
    """

    order_id: OrderId  # Ordre interne corrélé avant publication.
    execution_id: str  # Référence source intégrale, sans transformation.
    symbol: str  # Instrument effectivement rapporté par la source.
    timestamp_utc: datetime  # Temps d'exécution source, normalisé en UTC.
    side: Side  # Sens rapporté ; BOT/SLD deviennent BUY/SELL pour IBKR.
    quantity: Decimal  # Quantité de ce fill uniquement, pas un cumul.
    price: Decimal  # Prix exécuté hors commissions.


# contracts/inputs/execution_commission_received.py
@dataclass(frozen=True, slots=True)
class ExecutionCommissionReceived:
    """Commission rapportée pour une exécution.

    Référence et devise non vides ; montant fini, éventuellement négatif.
    Peut précéder le traitement de l'exécution correspondante.
    """

    execution_id: str  # Même référence source que ExecutionReceived.
    commission: Decimal  # Montant rapporté, sans calcul de PnL.
    currency: str  # Devise du montant.


# adapters/ibkr : futur registre, hors contrats canoniques.
# Références techniques (clientId, orderId, permId) -> OrderId interne.
# Correspondance initiale enregistrée avant transmission ; enrichie ensuite.
# Corrélation inconnue : exception en phase synthétique.
# run_id, sequence et received_at_utc appartiennent à l'enveloppe séparée.
