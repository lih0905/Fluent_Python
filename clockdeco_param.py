import time

DEFAULT_FMT = '[{elapsed:0.8f}s] {name}({args}) -> {result}'

def clock(fmt=DEFAULT_FMT): # 매개변수화된 데커레이터 팩토리
    def decorate(func): # 실제 데커레이터
        def clocked(*_args): #데커레이트된 함수를 래핑
            t0 = time.time()
            _result = func(*_args) # 함수의 실제 연산 결과
            elapsed = time.time() - t0
            name = func.__name__
            args = ', '.join(repr(arg) for arg in _args)
            result = repr(_result) # _result를 문자화
            print(fmt.format(**locals())) # fmt가 clocked()의 지역 변수를 모두 참조
            return _result # clocked는 데커레이트된 함수를 대체하므로, 원래 함수가 반환하는 값을 반환
        return clocked
    return decorate


if __name__=='__main__':
    
    @clock()
    def snooze(seconds):
        time.sleep(seconds)
        
    for i in range(3):
        snooze(.123)