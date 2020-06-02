# coroutil.py

from functools import wraps

def coroutine(func):
    """데커레이터: 'func'를 기동해서 첫번째 yield까지 진행한다."""
    @wraps(func)
    def primer(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen) # 제너레이터를 기동한다.
        return gen # 제너레이터를 반환한다.
    return primer