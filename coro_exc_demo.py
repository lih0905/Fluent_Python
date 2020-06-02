class DemoException(Exception):
    """설명에 사용할 예외 유형"""

def demo_exc_handling():
    print('-> coroutine started')
    while True:
        try:
            x = yield
        except DemoException:
            print('*** DemoException handled. Continuing...')
        else: # 예외가 발생하지 않으면 받은 값을 출력한다.
            print('-> coroutine received: {!r}'.format(x))
    raise RuntimeError('This line should never run.') # 이 코드는 실행되지 않음
                
