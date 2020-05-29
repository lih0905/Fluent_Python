# mirror_gen.py

import contextlib

@contextlib.contextmanager
def looking_glass():
    import sys
    original_write = sys.stdout.write
    
    def reverse_write(text):
        original_write(text[::-1])
        
    sys.stdout.write = reverse_write
    yield 'JABBERWOCKY' # with 문에서 여기에서 잠시 중단
    sys.stdout.write = original_write # with 문알 빠져나오면 yield문 이후 실행