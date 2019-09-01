import time
import threading
class algo():
    def __init__(self,uid,n):
        self.uid=uid
        self.n=n
    def train(self):
        self.trd=threading.Thread(target=self.train_algo)
        self.trd.start()
        self.trd.name=str(self.uid)
        print(threading.enumerate())
        return self.trd.ident
    def train_algo(self):
        for i in range(self.n):
            print(f"[{self.uid}] {i}")
            time.sleep(1)