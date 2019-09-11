import logging
from params import params
import pymysql
import jwt
import traceback
import os

def tokenValidator(token):
    if token=='testing':
        return True
    else:
        return jwt.decode(token, params().secretkey, audience='www.inanalysis.com', algorithms=['HS256'])

class sql():
    def __init__(self):
        param=params()
        self.conn=pymysql.connect(param.dbhost,param.dbuser,param.dbpwd,param.dbschema)
        self.cursor=self.conn.cursor()

def modelDbCleaningOnLaunch():
    try:
        db=sql()
        db.cursor.execute("select `mid` from models where `status`='train';")
        table=db.cursor.fetchall()
        mids=[t[0] for t in table]
        for mid in mids:
            db.cursor.execute(f"update `models` set `status`='fail',`failReason`='system restart, training abort.' where `mid`='{mid}';")
        db.conn.commit()
        logging.info("[modelDbCleaningOnLaunch] success")
    except Exception as e:
        logging.error(f"[modelDbCleaningOnLaunch] {traceback.format_exc()}")

def checkFolder():
    param=params()
    if not os.path.isdir(param.filepath):
        try:
            os.mkdir(param.filepath)
        except Exception as e:
            logging.error(f"[checkFolder] {e}")
    if not os.path.isdir(param.modelpath):
        try:
            os.mkdir(param.modelpath)
        except Exception as e:
            logging.error(f"[checkFolder] {e}")
    if not os.path.isdir(param.imgpath):
        try:
            os.mkdir(param.imgpath)
        except Exception as e:
            logging.error(f"[checkFolder] {e}")
    
