from service.visualizeService.core.dataVizBase import dataViz
from PIL import Image
from params import params
import uuid
from datetime import date
from utils import sql
from bokeh.embed import json_item,components

class customImg(dataViz):
    def __init__(self,img):
        try:
            self.params=params()
            self.imgId=str(uuid.uuid1())
            self.img=img
            self.algoInfo={"algoname":"CustomModelPreview","lib":"custom","friendlyname":"custom"}
            self.bokeh_fig=self.init_figure()
            self.imgWH=None
            self.component=None
        except Exception as e:
            raise Exception(f'[analyticViz][{self.algoInfo["algoname"]}]{e}')

    def convert(self):
        try:
            im = Image.fromarray(self.img)
            im.save(f'{self.params.imgpath}/{self.imgId}.png')
            self.imgWH=Image.open(f'{self.params.imgpath}/{self.imgId}.png').size
            td=date.today()
            db=sql()
            db.cursor.execute(f"INSERT INTO `incore`.`plottedImgs` (`id`, `path`, `width`, `height`, `createdTime`) VALUES ('{self.imgId}', '{self.params.imgpath}/{self.imgId}.png', '{self.imgWH[0]}', '{self.imgWH[1]}', '{td.year}-{td.month}-{td.day}');")
            db.conn.commit()
            self.bokeh_fig.image_url(url=[f"http://{self.params.host}:{self.params.port}/viz/getimg?uid={self.imgId}&action=get"], x=0, y=0, w=self.imgWH[0], h=self.imgWH[1],anchor='bottom_left')
            script,div=components(self.bokeh_fig,wrap_script=False)
            self.component=({"div":div,"script":script})
        except Exception as e:
            raise Exception(f'[convert] {e}')
        finally:
            db.conn.close()