from resources.dataService.utils import getColType
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

if __name__=='__main__':
    test_getsql()