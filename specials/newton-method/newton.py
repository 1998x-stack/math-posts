"""Scalar Newton and safeguarded Newton. Standard library only."""
from math import isfinite

def newton(f, df, x, tol=1e-12, max_iter=50):
    for n in range(max_iter+1):
        y=f(x)
        if not isfinite(y): return x,'nonfinite',n
        if abs(y)<=tol: return x,'residual tolerance',n
        if n==max_iter: break
        d=df(x)
        if not isfinite(d) or abs(d)<1e-14: return x,'unsafe derivative',n
        z=x-y/d
        if not isfinite(z) or z==x: return x,'nonfinite or stagnation',n
        x=z
    return x,'iteration limit',max_iter

def safeguarded(f,df,a,b,xtol=1e-12,max_iter=200):
    """Continuous f on finite [a,b], with opposite endpoint signs. Return midpoint and bracket."""
    fa,fb=f(a),f(b)
    if not (isfinite(a) and isfinite(b) and a<b and isfinite(fa) and isfinite(fb) and isfinite(b-a)): raise ValueError('invalid bracket')
    if fa==0:return a,(a,a),'exact',0
    if fb==0:return b,(b,b),'exact',0
    if (fa>0)==(fb>0):raise ValueError('not a sign bracket')
    for n in range(max_iter+1):
        w=b-a; x=a+w/2
        if w<=2*xtol:return x,(a,b),'width tolerance',n
        if n==max_iter:return x,(a,b),'iteration limit',n
        if x==a or x==b:return x,(a,b),'stagnation',n
        y=f(x)
        if not isfinite(y):raise ValueError('nonfinite f')
        if y==0:return x,(x,x),'exact',n
        d=df(x); z=x-y/d if isfinite(d) and abs(d)>=1e-14 else x
        if not (a+w/4<=z<=b-w/4):z=x
        fz=f(z)
        if not isfinite(fz):raise ValueError('nonfinite f')
        if fz==0:return z,(z,z),'exact',n+1
        if (fz>0)==(fa>0):a,fa=z,fz
        else:b,fb=z,fz

if __name__=='__main__':
    import math
    f=lambda x:x*x-2; df=lambda x:2*x
    x,s,n=newton(f,df,2.);assert abs(x-math.sqrt(2))<1e-12 and s=='residual tolerance'
    assert newton(lambda x:x**3-1,lambda x:3*x*x,0)[1]=='unsafe derivative'
    assert newton(lambda x:x**3-2*x+2,lambda x:3*x*x-2,0,max_iter=10)[1]=='iteration limit'
    x,br,s,n=safeguarded(f,df,0,2);assert br[0]<=math.sqrt(2)<=br[1] and abs(x-math.sqrt(2))<=1e-12
    x,br,s,n=safeguarded(lambda x:x**3-2*x+2,lambda x:3*x*x-2,-2,0);assert abs(x**3-2*x+2)<1e-10
    print('5 numerical assertions passed')
