class dataViz():
    def __init__(self,paramSet):
        self.paramSet=paramSet
        self.data=None
        self.figure=self.init_figure
        self.imgId=None
    def init_figure(self):
        #initial a bokeh figure instance
        pass

    def getData(self):
        #put dataframe into self.data according to paramSet
        pass

    def do_viz(self):
        #run visualization
        pass

    def saveimg(self):
        pass

    def img2bokeh(self):
        pass