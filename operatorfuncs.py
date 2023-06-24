import math
from random import random

def power(s):
    a = s.pop()
    s.push(s.pop()**a)
def div(s):
    a = s.pop()
    s.push(s.pop()/a)
plus    = lambda s: s.push(s.pop()+s.pop())
minus   = lambda s: s.push(-s.pop()+s.pop())
mul     = lambda s: s.push(s.pop()*s.pop())


Abs     = lambda s: s.push(abs(s.pop()))
Atn     = lambda s: s.push(math.atan(s.pop()))
Cos     = lambda s: s.push(math.cos(s.pop()))
Exp     = lambda s: s.push(math.exp(s.pop()))
Int     = lambda s: s.push(math.floor(s.pop()))
Log     = lambda s: s.push(math.log(s.pop()))
Rnd     = lambda s: s.push(random())
Sin     = lambda s: s.push(math.sin(s.pop()))
Sqr     = lambda s: s.push(math.sqrt(s.pop()))
Tan     = lambda s: s.push(math.tan(s.pop()))
Chr     = lambda s: s.push(chr(int(s.pop())))
Tab     = lambda s: s.push('\t'*int(s.pop()))
def greater(s):
    a = s.pop()
    if(s.pop() > a):
        s.push(1)
    else:
        s.push(0)

def lesser(s):
    a = s.pop()
    if(s.pop() < a):
        s.push(1)
    else:
        s.push(0)

def eq(s):
    if(s.pop() == s.pop()):
        s.push(1)

    else:
        s.push(0)

def neg(s):
    s.push(-s.pop())


def greatereq(s):
    a = s.pop()
    if(s.pop() >= a):
        s.push(1)
    else:
        s.push(0)

def lessereq(s):
    a = s.pop()
    if(s.pop() <= a):
        s.push(1)
    else:
        s.push(0)

def neq(s):
    a = s.pop()
    if(s.pop() != a):
        s.push(1)
    else:
        s.push(0)


    

