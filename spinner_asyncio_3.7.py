#!/usr/bin/env python3

# spinner_asyncio.py

# credits: Example by Luciano Ramalho inspired by
# Michele Simionato's multiprocessing example in the python-list:
# https://mail.python.org/pipermail/python-list/2009-February/538048.html

# BEGIN SPINNER_ASYNCIO
import asyncio
import itertools

async def spin(msg):  # <1>
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        print(status, flush=True, end='\r')
        try:
            await asyncio.sleep(.1)  # <2>
        except asyncio.CancelledError:  # <3>
            break
    print(' ' * len(status), end='\r')


async def slow_function():  # <4>
    # pretend waiting a long time for I/O
    await asyncio.sleep(3)  # <5>
    return 42


async def supervisor():  # <6>
    spinner = asyncio.create_task(spin('thinking!'))  # <7>
    time.sleep(3)
    print('spinner object:', spinner)  # <8>
    result = await slow_function()  # await는 메인과 spinner사이의 제어권을 주고 받는다.
    spinner.cancel()  # <10>
    return result


def main():
    result = asyncio.run(supervisor())  # <11>
    print('Answer:', result)


if __name__ == '__main__':
    main()
# END SPINNER_ASYNCIO
