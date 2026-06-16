From IBKR documentation
https://interactivebrokers.github.io/tws-api/interfaceIBApi_1_1EWrapper.html#a27ec36f07dff982f50968c8a8887d676

**PendingSubmit** - indicates that you have transmitted the order, but have not yet received confirmation that it has been accepted by the order destination.

**PreSubmitted** - indicates that a ***simulated order*** type has been accepted by the IB system and that this order has yet to be elected. The order is held in the IB system until the election criteria are met. At that time the order is transmitted to the order destination as specified.

**Submitted** - indicates that your order has been accepted by the system.

**PendingCancel** - indicates that you have sent a request to cancel the order but have not yet received cancel confirmation from the order destination.
At this point, your order is not confirmed canceled. It is not guaranteed that the cancellation will be successful.

**Cancelled** - indicates that the balance of your order has been confirmed canceled by the IB system. This could occur unexpectedly when IB or the destination has rejected your order.

**ApiCancelled** - after an order has been submitted and before it has been acknowledged, an API client client can request its cancelation, producing this state.

**Filled** - indicates that the order has been completely filled. Market orders executions will not always trigger a Filled status.

**Inactive** - indicates that the order was received by the system but is no longer active because it was rejected or canceled.






