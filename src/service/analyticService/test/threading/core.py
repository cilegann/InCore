import random
from algo import algo
from threading import Thread
import threading
import ctypes 

def tWrapper(a):
    a.train()

# class threade(threading.Thread): 
#     def __init__(self, *args, **kwargs): 
#         threading.Thread.__init__(self, *args, **kwargs) 
              
#     def get_id(self): 
#         # returns id of the respective thread 
#         if hasattr(self, '_thread_id'): 
#             return self._thread_id 
#         for id, thread in threading._active.items(): 
#             if thread is self: 
#                 return id
   
#     def raise_exception(self): 
#         thread_id = self.get_id() 
#         res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 
#               ctypes.py_object(SystemExit)) 
#         if res > 1: 
#             ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0) 
#             print('Exception raise failure') 

class core():
    def __init__(self,n):
        self.n=n
    
    def do(self):
        uid=(random.randint(0,100))
        print(f"CORE start job {uid}")
        a=algo(uid,self.n)
        tid=a.train()
        print(f"UID: {uid} | IDENTY: {tid}")
        print(threading.enumerate())
        return uid,tid