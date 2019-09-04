import uuid
import glob
from utils import sql
class modelUidGenerator():
    def __init__(self):
        self.uid=str(uuid.uuid1())
        param=params()
        while len(glob.glob((param.modelpath+"/"+self.uid+"*")))!=0:
            self.uid=str(uuid.uuid1())

def changeModelStatus(mid,status):
    try:
        db=sql()
        db.cursor.execute(f"update models set `status` = '{status}' where `mid`='{mid}'")
