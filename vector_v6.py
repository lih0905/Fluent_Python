# vector_v6.py

from array import array
import reprlib
import math
import numbers
import functools
import operator
import itertools # chain() 함수를 사용하기 위함

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
        
    def __setattr__(self, name, value):
        cls = type(self)
        if len(name) == 1:
            if name in cls.shortcut_names:
                error = 'readonly attribute {attr_name!r}' # xyzt 중 하나는 구체적으로 오류 발생
            elif name.islower():
                error = "can't set attributes 'a' to 'z' in {cls_name!r}" # 그외 소문자면 일반적 메세지 오류 발생
            else:
                error = ''
            if error:
                msg = error.format(cls_name=cls.__name__, attr_name=name)
                raise AttributeError(msg)
        # 에러가 발생하지 않을 때는 정상적으로 __setattr__() 메서드 호출
        super().__setattr__(name, value) 
        
    def angle(self, n):
        r = math.sqrt(sum(x * x for x in self[n:]))
        a = math.atan2(r, self[n-1])
        if (n == len(self) - 1) and (self[-1]<0):
            return math.pi * 2 - a
        else:
            return a
        
    def angles(self):
        return (self.angle(n) for n in range(1, len(self)))
    
    def __format__(self, fmt_spec=''):
        if fmt_spec.endswith('h'): # 초구면좌표
            fmt_spec = fmt_spec[:-1]
            coords = itertools.chain([abs(self)],
                                    self.angles()) 
            outer_fmt = '<{}>'
        else:
            coords = self
            outer_fmt = '({})'
        components = (format(c, fmt_spec) for c in coords)
        return outer_fmt.format(', '.join(components))
    
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
        if len(self) != len(other): # 길이가 다르면 False
            return False
        for a, b in zip(self, other): # 제너레이터로부터 하나씩 비교
            if a != b:
                return False
        return True
    
    def __hash__(self):
        hashes = (hash(x) for x in self._components) # 제너레이터 표현식 이용
        return functools.reduce(operator.xor, hasehs, 0) # 초기값을 0으로 함
    
    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))
    
    def __bool__(self):
        return bool(abs(self))
    
    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv) # 언패킹할 필요가 없음
    
    # -x 구현
    def __neg__(self):
        return Vector(-x for x in self)
    
    # +x 구현
    def __pos__(self):
        return Vector(self)