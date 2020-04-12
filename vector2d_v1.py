# vector2d_v1.py 
from array import array
import math

class Vector2d:
    typecode = 'd' # Vector2d와 bytes 간의 변환에 사용하는 클래스 속성
    
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y) # 미리 실수로 변환하는 센스
        
    def __iter__(self): # 이걸 구현하면 x,y = my_vector 처럼 쓸 수 있다.
        return (i for i in (self.x, self.y))
    
    def __repr__(self):
        class_name = type(self).__name__
        return '{}({!r}, {!r})'.format(class_name, *self)
    
    def __str__(self):
        return str(tuple(self))
    
    def __bytes__(self):
        return (bytes([ord(self.typecode)])+
               bytes(array(self.typecode, self)))
    
    def __eq__(self, other):
        return tuple(self) == tuple(other)
    
    def __abs__(self):
        return math.hypot(self.x, self.y)
    
    def __bool__(self):
        return bool(abs(self))
    
    @classmethod # 클래스 메서드
    def frombytes(cls, octets): # self 매개변수가 없고 대신 자신이 cls로 전달됨
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(*memv)