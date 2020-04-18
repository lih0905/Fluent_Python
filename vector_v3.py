# vector_v3.py

from array import array
import reprlib
import math
import numbers

class Vector:
    typecode = 'd'
    shortcut_names = 'xyzt'
    
    def __init__(self, components):
        # 벡터 요소를 배열로 저장
        self._components = array(self.typecode, components)
    
    """시퀀스 프로토콜 구현"""
    def __len__(self):
        return len(self._components)
    
    def __getitem__(self, index):
        cls = type(self) # 객체의 클래스를 가져옴
        if isinstance(index, slice): # index가 슬라이스이면
            return cls(self._components[index]) # Vector 객체를 생성
        elif isinstance(index, numbers.Integral): # index가 정수형이면
            return self._components[index] # 해당 항목 반환
        else:
            msg = '{cls.__name__} indices must be integers'
            raise TypeError(msg.format(cls=cls)) 
    """시퀀스 프로토콜 구현 종료"""
    
    def __getattr__(self, name):
        cls = type(self)
        if len(name) == 1: # name이 한글자이면 
            pos = cls.shortcut_names.find(name)
            if 0 <= pos < len(self._components): # 포지션이 범위 내에 있으면 배열 항목 반환
                return self._components[pos]
        msg = '{.__name__!r} object has no attribute {!r}' 
        raise AttributeError(msg.format(cls, name))
    
    def __iter__(self):
        return iter(self._components) # 반복할 수 있도록 구현
    
    def __repr__(self):
        components = reprlib.repr(self._components) # 제한된 길이로 출력
        components = components[components.find('['):-1] # 문자열 중 앞에 나오는 "array('d'," 를 제거
        return 'Vector({})'.format(components)
    
    def __str__(self):
        return str(tuple(self))
    
    def __bytes__(self):
        return (bytes([ord(self.typecode)]) + 
               bytes(self._components))
    
    def __eq__(self, other):
        return tuple(self) == tuple(other)
    
    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))
    
    def __bool__(self):
        return bool(abs(self))
    
    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv) # 언패킹할 필요가 없음