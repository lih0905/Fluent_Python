# tombola.py

import abc

class Tombola(abc.ABC): # ABC 정의하기 위해 상속
    
    @abc.abstractmethod
    def load(self, iterable):
        """iterable의 항목들을 추가한다."""
        
    @abc.abstractmethod
    def pick(self):
        """무작위로 항목을 하나 제거하고 반환한다.
        객체가 비어 있을 때 이 메서드를 실행하면 'LookupError'가 발생한다.
        """
        
    def loaded(self): # ABC 에도 구상 메서드가 들어갈 수 있다
        """최소 한 개의 항목이 있으면 True, 아님 False 반환"""
        # ABC의 구상 메서드는 반드시 ABC에 정의된 인터페이스, 즉
        # ABC의 다른 구상 메서드나 추상 메서드, 혹은 프로퍼티만 사용해야 한다.
        return bool(self.inspect())
    
    def inspect(self):
        """현재 안에 있는 항목들로 구성된 정렬된 튜플 반환"""
        items = []
        while True:
            try:
                # pick() 을 계속 호출해서 Tombola 객체를 비움
                items.append(self.pick())
            except LookupError:
                break
        self.load(items) # load 메서드를 호출해서 다시 넣는다
        return tuple(sorted(items))