from service.dataService.utils import getColType
from service.visualizeService.core.dataViz import dataViz
# from service.visualizeService.core.dataVizAlgo.lineXY import lineXY
import logging
import pymysql
from params import params 
from utils import sql
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')
csvid='./files/num.csv'
tsvid='./files/nlp.tsv'
zipid='./files/cv'

def test_getColType():
    gct=getColType(csvid,'num').get()

def test_getsql():
    db=sql()
    db.cursor.execute(f"select * from files;")
    table=db.cursor.fetchall()
    table=[[tt for tt in t] for t in table]
    print(table)

def test_viz():
    algoInfo={
        "name":"2D line",
        "lib":"bokeh",
        "algo":"lineXY",
        "data":{
            "x":1,
            "y":1,
            "value":0
        },
        "description":"2D scatter with circle markers"
    }
    import importlib
    module = importlib.import_module("service.visualizeService.core.dataVizAlgo.lineXY")
    algo=getattr(module,'lineXY')
    try:
        v=algo(algoInfo,{'x':'a','y':'b','value':'c'},'num')
    except Exception as e:
        logging.error(e)
    print(v.data)

def testPurger():
    from apscheduler.schedulers.background import BackgroundScheduler
    from purge import purger 
    def purge():
        purger().purgeImg()
    scheduler = BackgroundScheduler()
    scheduler.add_job(purge, 'cron',day_of_week='0-6', hour=1, minute=24)
    scheduler.start()

if __name__=='__main__':
    testPurger()