#!flask/bin/python
#
# NonceStore class implements a simple interface to generate and validate
# a Nonce. It uses system ram to store any non-expired Nonces so note
# that a non-throttled API could be DDOS'd if a client repeatedly requested
# nonces. It's theoretically possible if the expiration is long enough
# the memory usage would be too high and the app would crash
#
# CoinAuth - Service for Authenticating the owner of a Bitcoin Address
# Copyright (C) 2014 Daniel Rice drice@greenmangosystems.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import itertools
from time import time
import heapq
import random
from threading import RLock

class NonceStore:
    _pq = []                         # list of entries arranged in a heap
    _entry_finder = {}               # mapping of nonces to entries
    _REMOVED = '<removed-nonce>'     # placeholder for a removed nonce
    _counter = itertools.count()     # unique sequence count
    _dblock = RLock()
    _counterlock = RLock()
    
    def __init__(self, timeoutSeconds):
        self._timeoutSeconds = timeoutSeconds
    
    def _add_nonce(self, nonce, time):
        'Add a new nonce'
        self._counterlock.acquire()
        count = next(self._counter)
        self._counterlock.release()
        entry = [time, count, nonce]
        self._dblock.acquire()
        self._entry_finder[nonce] = entry
        heapq.heappush(self._pq, entry)
        self._dblock.release()
    
    def _remove_nonce(self, nonce):
        'Mark an existing nonce as REMOVED.  Raise KeyError if not found.'
        self._dblock.acquire()
        entry = self._entry_finder.pop(nonce)
        entry[-1] = self._REMOVED
        self._dblock.release()
        
    def _remove_stale(self):
        'Remove nonces that are too old'
        self._dblock.acquire()
        iterSmallest = heapq.nsmallest(1, self._pq)
        while((len(iterSmallest)==1) and ((time() - iterSmallest[0][0]) > self._timeoutSeconds)):
            self._entry_finder.pop(iterSmallest[0][2])
            heapq.heappop(self._pq)
            iterSmallest = heapq.nsmallest(1, self._pq)
        self._dblock.release()
        
    def nonce_find_and_remove(self, nonce):
        'if found return True and remove nonce from DB, else False'
        self._remove_stale() # remove any that should be expired
        try:
            self._dblock.acquire()
            self._entry_finder[nonce]# if this doesn't exist, error is thrown
            self._remove_nonce(nonce)
            self._dblock.release()
            return True
        except KeyError:
            return False
        
    def generate_nonce(self):
        'Generate and return a new nonce. Store nonce to memory db'
        self._remove_stale() # remove any that should be expired
        newnonce = random.SystemRandom().randint(0, (2**64)-1) #64 bit number
        self._add_nonce(newnonce, time())
        return newnonce
    