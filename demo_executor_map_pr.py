# demo_executor.map.py

from time import sleep, strftime
from concurrent import futures

def display(*args): # 자신이 받은 인수 앞에 시간 출력
    print(strftime('[%H:%M:%S]'), end=' ')
    print(*args)
    
# 시작할 때 메시지를 출력하고, 인수로 받은 n초 동안 잠자고, 마지막 메시지 출력.
def loiter(n): 
    msg = '{}loiter({}): doing nothing for {}s...'
    display(msg.format('\t'*n, n, n))
    sleep(n)
    msg = '{}loiter({}): done.'
    display(msg.format('\t'*n, n))
    return n * 10

def main():
    display('Script starting.')
    executor = futures.ProcessPoolExecutor(max_workers=3)
    # worker가 3개이므로 일단은 loiter(0), loiter(1), loiter(2)만 먼저 실행
    results = executor.map(loiter, range(5)) 
    display('results:', results)
    display('Waiting for individual results:')
    for i, result in enumerate(results):
        display('result {}: {}'.format(i, result))
    
main()
