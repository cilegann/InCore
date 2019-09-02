import time
import threading
class algo():
    def __init__(self,uid,n):
        self.uid=uid
        self.n=n

    def trainWrp(self):
        self.train_algo()
        print("Done")

    def train(self):
        self.trd=threading.Thread(target=self.trainWrp)
        self.trd.start()
        self.trd.name=str(self.uid)
        return True
        
    def train_algo(self):
        for i in range(self.n):
            print(f"[{self.uid}] {i}")
            time.sleep(1)