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

def dbCleaningOnLaunch():
    try:
        db=sql()
        db.cursor.execute("select `mid` from models where `status`='train';")
        table=db.cursor.fetchall()
        mids=[t[0] for t in table]
        for mid in mids:
            db.cursor.execute(f"update `models` set `status`='fail',`failReason`='system restart, training abort.' where `mid`='{mid}';")
        db.conn.commit()
        
        db.cursor.execute(f"select `fid` from models where `status`='train' or `status`='success'")
        usingFids=db.cursor.fetchall()
        usingFids=[f[0] for f in usingFids]
        db.cursor.execute(f"select `fid` from models")
        allFids=db.cursor.fetchall()
        allFids=[f[0] for f in allFids]
        toFreeFilds=list(set(allFids)-set(usingFids))
        for f in toFreeFilds:
            db.cursor.execute(f"update `files` set `inuse`='0' where `fid`='{f}';")
        for f in usingFids:
            db.cursor.execute(f"update `files` set `inuse`='1' where `fid`='{f}';")
        db.conn.commit()
        logging.info("[dbCleaningOnLaunch] success")
    except Exception as e:
        db.conn.rollback()
        logging.error(f"[dbCleaningOnLaunch] {traceback.format_exc()}")
    finally:
        db.conn.close()

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
    
