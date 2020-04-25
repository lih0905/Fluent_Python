import collections

Card = collections.namedtuple('Card', ['rank','suit'])

class FrenchDeck2(collections.abc.MutableSequence):
    ranks = [str(n) for n in range(2,11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()
    
    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                      for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]
    
    def __setitem__(self, position, value):
        self._cards[position] = value
        
    # MutableSequence를 상속하므로 이 클래스의 추상 메서드인 
    # __delitem__() 도 구현해야함
    def __delitem__(self, position):
        del self._cards[position]
        
    # insert() 또한 추상 메서드
    def insert(self, position, value):
        self._cards.insert(position, value)