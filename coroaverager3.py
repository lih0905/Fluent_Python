# coroaverager3.py

from collections import namedtuple

Result = namedtuple('Result', 'count average')

# 하위 제너레이터
def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield # main() 안의 클라이언트가 전송하는 값이 여기에 바인딩
        if term is None: # 종료 조건
            break
        total += term
        count += 1
        average = total/count
    return Result(count, average) #반환값은 groper()의 yield from의 값이 된다

# 대표 제너레이터
def grouper(results, key):
    while True: # 반복때마다 하나의 averager() 객체 생성
        # grouper()가 값을 받을 때마다 이 값은 yield from에 의해 averager() 객체로 전달된다
        # grouper()는 클라이언트가 전송한 값들을 averager()가 소진할 때까지 여기에서 중단
        # averager() 객체가 실행을 완료하고 반환한 값은 results[key]에 바인딩
        results[key] = yield from averager()
        
# 호출자
def main(data):
    results = {}
    for key, values in data.items():
        group = grouper(results, key) # 코루틴 생성
        next(group) # 코루틴 기동
        for value in values:
            group.send(value) # 값을 하나씩 grouper()에 전달
            # 이 값은 averager()의 term = yield 값이 된다
        group.send(None) # 이 부분이 중요!
        # None을 전달하면 현재 avergaer() 객체가 종료되고 grouper()가 실행을 재개
    
    print(results)
    report(results)

# 실행 결과 보고서
def report(results):
    for key, result in sorted(results.items()):
        group, unit = key.split(';')
        print('{:2} {:5} averaging {:.2f}{}'.format(
            result.count, group, result.average, unit))
        
data = {
    'girls;kg':
        [40.9, 38.5, 44.3, 42.2, 45.2, 41.7, 44.5, 38.0, 40.6, 44.5],
    'girls;m':
        [1.6, 1.51, 1.4, 1.3, 1.41, 1.39, 1.33, 1.46, 1.45, 1.43],
    'boys;kg':
        [39.0, 40.8, 43.2, 40.8, 43.1, 38.6, 41.4, 40.6, 36.3],
    'boys;m':
        [1.38, 1.5, 1.32, 1.25, 1.37, 1.48, 1.25, 1.49, 1.46]
}
        
if __name__ == '__main__':
    main(data)