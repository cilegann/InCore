class paramSet():
    def __init__(self):
        self.xCol=[]
        self.yCol=[]
        self.type=None # data/model
        self.params={}

class viz():
    def __init__(self,paramSet):
        self.paramSet=paramSet
        self.imgUid=None
        

    def do_viz(self):
        pass