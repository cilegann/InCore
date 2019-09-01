import random
from algo import algo
from threading import Thread

def tWrapper(a):
        a.train()

class core():
    def __init__(self,n):
        self.n=n
    
    def do(self):
        uid=(random.randint(0,100))
        print(f"CORE start job {uid}")
        a=algo(uid,self.n)

        t=Thread(target=tWrapper,args=(a,))
        t.start()
        #a.train() # TO THREAD
        tid=t.ident
        print(f"UID: {uid} | IDENTY: {tid}")
        return uid,tid