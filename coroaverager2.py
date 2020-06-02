# coroaverager2.py

from collections import namedtuple

Result = namedtuple('Result', 'count average')

def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield
        if term is None:
            break # 값을 반환하려면 코루틴이 정상적으로 종료되어야 한다.
            # 따라서 이 averager 버전에서는 루프를 빠져나오는 조건을 검사한다.
        total += term
        count += 1
        average = total/count
    return Result(count, average) # nametuple 반환