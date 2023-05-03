from util import autonext


def f(s: str):
    print(s)
    print(autonext(s, 'badapple'))
    print()


f('a.tar')
f('a1.tar')
f('a03.tar')
f('a.3tar')
f('a.44.tar')
f('.tar')
f('')
