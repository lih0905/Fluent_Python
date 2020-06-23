#-*- coding:utf-8 -*-

import threading
import itertools
import time
import sys

class Signal: # 외부에서 스레드를 제어하기 위해 사용할 go 속성만 있는 가변 객체
    go = True

def spin(msg, signal):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'): # 무한 루프
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status)) # 문자열 길이만큼 백스페이스 문자를
        # 반복해서 앞으로 이동 시킴
        time.sleep(.1)
        if not signal.go: # go == False 면 루프 종료
            break
    # 공백 문자로 덮어쓰고 다시 커서를 처음으로 이동해서 메세지 출력행 청소
    write(' ' * len(status) + '\x08' * len(status))

def slow_function():
    # 입출력을 위해 장시간 기다리는 것처럼 보이게 만든다.
    time.sleep(3)
    # 주 스레드에서 sleep() 함수를 호출할 때 GIL이 해제되므로
    # 두번째 스레드가 진행
    return 42

def supervisor(): 
    # 이 함수는 두번째 스레드를 만들고, 스레드 객체를 출력하고,
    # 시간이 오래 걸리는 연산을 수행하고 나서 스스로 스레드 제거
    signal = Signal()
    spinner = threading.Thread(target=spin,
                               args=('thinking!', signal))
    print('spinner object:', spinner) # 두번째 스레드 객체 출력
    spinner.start() # 두번째 스레드 실행
    result = slow_function() # slow_function() 실행
    # 그러면 주 스레드가 블로킹되고 그동안 두번째 스레드가 
    # 텍스트 스피너 애니메이션을 보여준다.
    signal.go = False # signal의 상태 변경
    spinner.join() # spinner 스레드가 끝날 때까지 기다린다
    return result

def main():
    result = supervisor() # supervisor() 실행
    print('Answer:', result)

if __name__ == '__main__':
    main()

