import uuid
import glob
from utils import sql
from params import params

class modelUidGenerator():
    def __init__(self):
        self.uid=str(uuid.uuid1())
        param=params()
        while len(glob.glob((param.modelpath+"/"+self.uid+"*")))!=0:
            self.uid=str(uuid.uuid1())

def getModelInfo(mid):
    try:
        db=sql()
        db.cursor.execute(f"select * from models where `mid`='{mid}'")
        data=db.cursor.fetchall()
        data=[[tt for tt in t] for t in data]
        if len(data)==0:
            raise Exception(f'[getModelInfo] model {mid} not found')
        return data
    except Exception as e:
        raise Exception(f'[getModelInfo]{e}')
    finally:
        db.conn.close()

def changeModelStatus(mid,status):
    statusList= ['train','fail','success']
    if status not in statusList:
        raise Exception("[changeModelStatus] invalid status")
    try:
        db=sql()
        db.cursor.execute(f"update models set `status` = '{status}' where `mid`='{mid}'")
        db.conn.commit()
    except Exception as e:
        db.conn.rollback()
        raise Exception(f"[changeModelStatus] {e}")
    finally:
        db.conn.close()