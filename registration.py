registry = []

def register(func):
    print('running register(%s)' % func)
    registry.append(func)
    return func

@register
def f1():
    print('running f1()')

@register
def f2():
    print('running f2()')

def f3():
    print('running f3()')

def main():
    print('running main()')
    print('registry ->', registry)
    f1() # 이 경우 register()가 원래 함수를 반환하므로 f1()이 실행됨
    f2()
    f3()

if __name__=='__main__':
    main()
