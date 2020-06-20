#-*- coding:utf-8 -*-
# flags_threadpool.py

from concurrent import futures

# flags 모듈의 함수들 재사용
from flags import save_flag, get_flag, show, main

# ThreadPoolExecutor에서 사용할 최대 스레드 수
MAX_WORKERS = 20

# 하나의 이미지를 내려받을 함수
def download_one(cc):
    image = get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + '.PNG')
    return cc

def download_many(cc_list):
    # ThreadPoolExecutor 객체 생성
    with futures.ProcessPoolExecutor() as executor:
        # map 메서드는 여러 스레드에 의해 download_one() 함수를 동시에 호출한다
        # 내장된 map() 함수와 비슷젠하며, 각 함수가 반환한 값을 다담은 제너레이터 반환
        res = executor.map(download_one, sorted(cc_list))
    
    # 결과 반환. 호출한 함수중 하나라도 예외를 발생시키면 여기서 에러 발생
    return len(list(res))

if __name__ == '__main__':
    main(download_many)
