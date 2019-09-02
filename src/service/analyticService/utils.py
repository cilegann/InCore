import uuid
import glob
class modelUidGenerator():
    def __init__(self):
        self.uid=str(uuid.uuid1())
        param=params()
        while len(glob.glob((param.modelpath+"/"+self.uid+"*")))!=0:
            self.uid=str(uuid.uuid1())
