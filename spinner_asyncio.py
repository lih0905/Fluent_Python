#-*- coding:utf-8 -*-

import asyncio
import itertools
import sys

@asyncio.coroutine #
def spin(msg):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'): # 무한 루프
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status)) # 문자열 길이만큼 백스페이스 문자를
        # 반복해서 앞으로 이동 시킴
        try:
            yield from asyncio.sleep(.1)
        except asyncio.CancelledError:
            break
    write(' ' * len(status) + '\x08' * len(status))

@asyncio.coroutine #
def slow_function():
    # 입출력을 위해 장시간 기다리는 것처럼 보이게 만든다.
    yield from asyncio.sleep(3)
    return 42

@asyncio.coroutine #
def supervisor(): 
    # 이 함수는 두번째 스레드를 만들고, 스레드 객체를 출력하고,
    # 시간이 오래 걸리는 연산을 수행하고 나서 스스로 스레드 제거
    spinner = asyncio.async(spin('thinking!'))
    print('spinner object:', spinner) # 두번째 스레드 객체 출력
    result = yield from slow_function()
    spinner.cancel() # spinner 스레드가 끝날 때까지 기다린다
    return result

def main():
    loop = asyncio.get_event_loop()
    result = loop.run_util_complete(supervisor())
    loop.close()
    print('Answer:', result)

if __name__ == '__main__':
    main()

