from params import params
from utils import sql
from datetime import date,timedelta
import logging
import os
class purger():
    def __init__(self):
        self.param=params()
    def purgeImg(self):
        try:
            logging.info(f'[PurgeImg] Purging img before {date.today()-timedelta(days=2)}')
            db=sql()
            db.cursor.execute(f"select * from plottedImgs where createdTime<'{date.today()-timedelta(days=2)}'")
            data=db.cursor.fetchall()
            data=[list(a) for a in data]
            removedId=[]
            for d in data:
                id=d[0]
                path=d[1]
                try:
                    os.remove(path)
                except Exception as e:
                    logging.error(f'[PurgeImg] ID:{id}, Path:{path} Error:{e}')
                db.cursor.execute(f"delete from plottedImgs where `id`='{id}'")
            db.conn.commit()
        except Exception as e:
            db.conn.rollback()
            logging.error(f'[PurgeImg] {e}')
        finally:
            db.conn.close()
    # purge tmp file