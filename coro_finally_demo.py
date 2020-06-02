# coro_finally_demo.py

class DemoException(Exception):
    """설명에 사용할 예외 유형"""

def demo_finally():
    print('-> coroutine started')
    try:
        while True:
            try:
                x = yield
            except DemoException:
                print('*** DemoException handled. Continuing...')
            else: # 예외가 발생하지 않으면 받은 값을 출력한다.
                print('-> coroutine received: {!r}'.format(x))
    finally:
        print('-> coroutine ending')