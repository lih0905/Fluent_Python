# mirror.py

class LookingGlass:
    
    def __enter__(self):
        import sys
        self.original_write = sys.stdout.write # 나중에 사용하기 위해 객체 속성에 원래 sys.stdout.write() 메서드 객체를 저장
        sys.stdout.write = self.reverse_write
        return 'JABBERWOCKY' # 타겟 변수에 무언가를 저장히기 위해 문자열 반환
    
    def reverse_write(self, text): 
        # text 인수를 거꾸로 뒤집고 나서 원래 sys.stdout.write() 메서드 호출
        self.original_write(text[::-1])
        
    def __exit__(self, exc_type, exc_value, traceback):
        import sys
        sys.stdout.write = self.original_write # sys.stdout.write() 를 원래 메서드로 변경
        if exc_type is ZeroDivisionError:
            print('Please DO NOT divide by zero!')
            return True # 예외가 처리되었음을 알려준다.
        # __exit__() 가 None이나 True 이외의 값을 반환하면 with 블록에서 발생한 예외가 상위 코드로 전달됨
   
    