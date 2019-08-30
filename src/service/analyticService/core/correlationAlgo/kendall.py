from service.analyticService.core.correlation import correlation

class pearson(correlation):
    def __init__(self,fid):
        super().__init__(fid,"kendall")
    def calculate(self):
        self.corr=self.df.corr(method='kendall')