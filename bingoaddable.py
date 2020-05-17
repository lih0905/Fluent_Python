# bingoaddable.py

import itertools # 표준 라이브러리를 구현한 모듈보다 먼저 임포트

from tombola import Tombola
from bingo import BingoCage

class AddableBingoCage(BingoCage):

    def __add__(self, other):
        if isinstance(other, Tombola): # Tombola를 상속한 객체에만 작동
            return AddableBingoCage(self.inspect() + other.inspect())
        else:
            return NotImplemented
    
    def __iadd__(self, other):
        if isinstance(other, Tombola):
            other_iterable = other.inspect()
        else:
            try:
                other_iterable = iter(other) # Tombola 객체가 아닐 때는 반복자 시도
            except TypeError: # 실패할 때는 사용자가 문제를 해결할 방법을 명확히 제시
                self_cls = type(self).__name__
                msg = 'right operand in += must be {!r} or an iterable'
                raise TypeError(msg.format(self_cls))
        self.load(other_iterable) # self에 other를 추가 적재
        return self # 할당 연산 특별 메서드는 반드시 self를 반환!