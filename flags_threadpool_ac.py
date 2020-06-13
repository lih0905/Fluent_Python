# flags_threadpool_ac.py

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
    cc_list= cc_list[:5] # 5개만 쓰자
    # 대기중인 Future 객체를 출력해서 보기 위해 max_worker=3 으로 하드코딩
    with futures.ThreadPoolExecutor(max_workers=3) as executor:
        to_do = []
        for cc in sorted(cc_list):
            # executor.submit()은 콜러블이 실행되도록 스케줄링하고
            # 이 작업을 나타내는 Future 객체를 반환
            future = executor.submit(download_one, cc)
            to_do.append(future)
            msg = 'Scheduled for {}: {}'
            print(msg.format(cc, future))
        
        results = []
        # as_completed()는 Future가 완료해될 때 해당 Future 객체 생성
        for future in futures.as_completed(to_do):
            res = future.result() # 결과 생성
            msg = '{} result: {!r}'
            print(msg.format(future, res))
            results.append(res)

    return len(list(res))

if __name__ == '__main__':
    main(download_many)
