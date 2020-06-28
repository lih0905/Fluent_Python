#-*- coding:utf-8 -*-

import asyncio
import itertools
import sys

@asyncio.coroutine # asyncio에 사용할 코루틴은 @asyncio.coroutine으로 데커레이트해야한다.
def spin(msg): # signal 인수 불필요
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status)) 
        try:
            yield from asyncio.sleep(.1) # 이벤트 루프를 블로킹하지 않고 잠자기 위해
            # time.sleep 대신 yield from asyncio.sleep 사용
        except asyncio.CancelledError: # spin()이 깨어난 후 
            # asyncio.CancelledError 예외가 발생하면 루프 종료
            break
    write(' ' * len(status) + '\x08' * len(status))

@asyncio.coroutine 
def slow_function():
    # slow_function()은 이제 코루틴으로서, 코루틴이 잠자면서 입출력을 수행하는 체 하는 동안
    # 이벤트 루프가 진행될 수 있게 하기 위해 yield from을 사용한다.
    yield from asyncio.sleep(3) # 메인 루프의 제어 흐름을 처리한다
    return 42

@asyncio.coroutine 
def supervisor(): 
    # supervisor()도 코루틴이므로 yield from을 이용해 slow_function() 구동 가능
    # asyncio.async()는 spin() 코루틴의 실행을 스케줄링하고 Task 객체 안에 넣어 즉시 반환
    spinner = asyncio.async(spin('thinking!')) 
    print('spinner object:', spinner) # Task 객체 출력
    result = yield from slow_function() # 함수를 구동해서 완료되면 반환된 값 가져온다
    # 그동안에 이벤트 루프는 계속 실행된다. slow_function()이 yield from asyncio.sleep()을 실행해서
    # 메인 루프로 제어권을 넘기기 때문이다.
    spinner.cancel() # Task객체는 cancel() 메서드를 호출해서 취소할 수 있다.
    # 그러면 코루틴이 중단된 곳의 yield from에서 asyncio.CancelledError 예외가 발생한다.
    # 코루틴은 예외를 잡아서 지연시키거나 취소 요청을 거부할 수 있다.
    return result

def main():
    loop = asyncio.get_event_loop() # 이벤트 루프에 대한 참조를 가져온다.
    result = loop.run_until_complete(supervisor()) # supervisor() 코루틴을 구동해서 완료한다.
    loop.close()
    print('Answer:', result)

if __name__ == '__main__':
    main()