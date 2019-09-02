from service.analyticService.core.correlationAlgo.correlationBase import correlation

class pearson(correlation):
    def __init__(self,fid):
        super().__init__(fid,"kendall","Kendall Tau Correlation Coefficient")
    def calculate(self):
        self.corr=self.df.corr(method='kendall')