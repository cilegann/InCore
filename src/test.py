from service.dataService.utils import getColType
from service.visualizeService.core.dataViz import dataViz
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
        "name":"2D circle",
        "lib":"bokeh",
        "target":"data",
        "algo":"",
        "data":{
            "x":1,
            "y":1,
            "value":0
        },
        "description":"2D scatter with circle markers"
    }
    try:
        v=dataViz(algoInfo,{'x':'a','y':'b','value':'c'},'nlp')
    except Exception as e:
        logging.error(e)
    print(v.data)

if __name__=='__main__':
    test_viz()