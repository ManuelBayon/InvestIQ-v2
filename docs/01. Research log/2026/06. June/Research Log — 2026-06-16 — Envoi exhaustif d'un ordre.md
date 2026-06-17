 Exemple : Envoie d'un ordre

Étape 1 :
``` python
IB.placeOrder(contract, order)
```

Étape 2 :
```python
Client.placeOrder(orderId, contract, order)
```

Étape 3 :
``` python
Client.send(*field)

def send(self, *fields, makeEmpty=True):  
    """
    Serialize and send the given fields using the IB socket protocol.
    """ 
    
    if not self.isConnected():  
        raise ConnectionError('Not connected')  
  
    msg = io.StringIO()  
    empty = (None, UNSET_INTEGER, UNSET_DOUBLE) if makeEmpty else (None,)  
    for field in fields:  
        typ = type(field)  
        if field in empty:  
            s = ''  
        elif typ is str:  
            s = field  
        elif type is int:  
            s = str(field)  
        elif typ is float:  
            s = 'Infinite' if field == math.inf else str(field)  
        elif typ is bool:  
            s = '1' if field else '0'  
        elif typ is list:  
            # list of TagValue  
            s = ''.join(f'{v.tag}={v.value};' for v in field)  
        elif isinstance(field, Contract):  
            c = field  
            s = '\0'.join(str(f) for f in (  
                c.conId, c.symbol, c.secType,  
                c.lastTradeDateOrContractMonth, c.strike,  
                c.right, c.multiplier, c.exchange,  
                c.primaryExchange, c.currency,  
                c.localSymbol, c.tradingClass))  
        else:  
            s = str(field)  
        msg.write(s)  
        msg.write('\0')  
    self.sendMsg(msg.getvalue())
```

Étape 4 : 
```python
Client.sendMsg(msg)

def sendMsg(self, msg: str):  
    
    loop = getLoop()  
    t = loop.time()  
    times = self._timeQ  
    msgs = self._msgQ  
    
    while times and t - times[0] > self.RequestsInterval:  
        times.popleft()  
    
    if msg:  
        msgs.append(msg)  
    
    while msgs and (len(times) < self.MaxRequests or not self.MaxRequests):  
        msg = msgs.popleft()  
        self.conn.sendMsg(self._prefix(msg.encode()))  
        times.append(t)  
        if self._logger.isEnabledFor(logging.DEBUG):  
            self._logger.debug('>>> %s', msg[:-1].replace('\0', ','))  
    
    if msgs:  
        if not self._isThrottling:  
            self._isThrottling = True  
            self.throttleStart.emit()  
            self._logger.debug('Started to throttle requests')  
        loop.call_at(  
            times[0] + self.RequestsInterval,  
            self.sendMsg, None)  
    else:  
        if self._isThrottling:  
            self._isThrottling = False  
            self.throttleEnd.emit()  
            self._logger.debug('Stopped to throttle requests')
```