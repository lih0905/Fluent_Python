# lotto.py

import random
from tombola import Tombola

class LotteryBlower(Tombola):
    def __init__(self, iterable):
        self._balls = list(iterable) # 사본으로 저장
        
    def load(self, iterable):
        self._balls.extend(iterable)
        
    def pick(self):
        try:
            pos = random.randrange(len(self._balls))
        except ValueError:
            raise LookupError('pick from empty BingCage')
        return self._balls.pop(pos)
    
    def loaded(self):
        return bool(self._balls)
    
    def inspect(self):
        return tuple(sorted(self._balls))