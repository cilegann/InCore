# 你是接手這個東西的小可愛麼 (*´･д･)?
# 是的話恭喜你哦 (✧≖‿ゝ≖)
# 不是的話趕緊關掉回地球吧 這裡很可怕的 (°ཀ°)
# 大部分代碼和架構都是在喝了一瓶酒才開始寫ㄉ ( ´∀｀)つt[ ]
# 寫的時候只有我和神知道在幹嘛  (༼•̀ɷ•́༽)
# 現在只有神知道了 ( ￣ 3￣)y▂ξ
# 代碼成分：酒精 (80%)、尼古丁 (10%)、肝(6%)、青春歲月(3%)，以及一點點的 flask,sql,sklearn,keras,matplotlib (1%)
import os
from flask import Flask
from flask_restful import Api
import logging
import sys
sys.dont_write_bytecode = True #disable __pycache__
from params import params
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from purge import purger 
from controller.getConfig import getDataProjectType,getDataExtensionType
from controller.autoDeploy import gitPull
from service.dataService.controller.upload import Upload
from service.dataService.controller.download import Download
from service.dataService.controller.getColumn import getColumn
from service.dataService.controller.getFileStatus import getFileStatus
from service.dataService.controller.delete import DeleteFile

from service.visualizeService.controller.getImg import getImg
from service.visualizeService.controller.dataViz import getDataVizAlgoList,doDataViz

from service.analyticService.controller.preprocess import getPreprocessAlgoList,doPreprocess,previewPreprocess
from service.analyticService.controller.correlation import doCorrelation,getCorrelationAlgoList
from service.analyticService.controller.analytic import getAnalyticAlgoList,getAnalyticAlgoParam

par=params()
app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources=r"/*")

# bind api
api.add_resource(getDataProjectType,"/sys/dataproject")
api.add_resource(getDataExtensionType,"/sys/dataextension")

api.add_resource(Upload, "/data/upload")
api.add_resource(Download,'/data/download')
api.add_resource(getColumn,'/data/getcol')
api.add_resource(getFileStatus,'/data/getstatus')
api.add_resource(DeleteFile,'/data/delete')

api.add_resource(getImg,'/viz/getimg')
api.add_resource(getDataVizAlgoList,'/viz/data/getalgo')
api.add_resource(doDataViz,'/viz/data/do')

api.add_resource(getPreprocessAlgoList,'/preprocess/getalgo')
api.add_resource(doPreprocess,'/preprocess/do')
api.add_resource(previewPreprocess,'/preprocess/preview')
api.add_resource(getCorrelationAlgoList,'/correlation/getalgo')
api.add_resource(doCorrelation,'/correlation/do')

api.add_resource(getAnalyticAlgoList,'/analytic/getalgo')
api.add_resource(getAnalyticAlgoParam,'/analytic/getparam')

def purge():
    purger().purgeImg()

if __name__ == "__main__":
    if '--deploy' in sys.argv:
        api.add_resource(gitPull,'/autodeploy/git')
    if '--debug' in sys.argv:
        api.add_resource(gitPull,'/autodeploy/git')
        logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')
    else:
        logging.basicConfig(level=logging.INFO , format='[%(levelname)s] %(message)s')
    logging.info(f'InCore running at port {par.port}')
    scheduler = BackgroundScheduler()
    scheduler.add_job(purge, 'cron',day_of_week='0-6', hour=1, minute=27)
    scheduler.start()
    if '--port' not in sys.argv:
        port=par.port
    else:
        port=int(sys.argv[sys.argv.index('--port')+1])
    app.run(debug='--debug' in sys.argv,port=port,host='0.0.0.0')
    

#   █████▒█    ██  ▄████▄   ██ ▄█▀       ██████╗ ██╗   ██╗ ██████╗
# ▓██   ▒ ██  ▓██▒▒██▀ ▀█   ██▄█▒        ██╔══██╗██║   ██║██╔════╝
# ▒████ ░▓██  ▒██░▒▓█    ▄ ▓███▄░        ██████╔╝██║   ██║██║  ███╗
# ░▓█▒  ░▓▓█  ░██░▒▓▓▄ ▄██▒▓██ █▄        ██╔══██╗██║   ██║██║   ██║
# ░▒█░   ▒▒█████▓ ▒ ▓███▀ ░▒██▒ █▄       ██████╔╝╚██████╔╝╚██████╔╝
#  ▒ ░   ░▒▓▒ ▒ ▒ ░ ░▒ ▒  ░▒ ▒▒ ▓▒       ╚═════╝  ╚═════╝  ╚═════╝
#  ░     ░░▒░ ░ ░   ░  ▒   ░ ░▒ ▒░
#  ░ ░    ░░░ ░ ░ ░        ░ ░░ ░
#           ░     ░ ░      ░  ░
#                 ░
#


#                       _oo0oo_
#                      o8888888o
#                      88" . "88
#                      (| -_- |)
#                      0\  =  /0
#                    ___/`---'\___
#                  .' \\|     |# '.
#                 / \\|||  :  |||# \
#                / _||||| -:- |||||- \
#               |   | \\\  -  #/ |   |
#               | \_|  ''\---/''  |_/ |
#               \  .-\__  '-'  ___/-. /
#             ___'. .'  /--.--\  `. .'___
#          ."" '<  `.___\_<|>_/___.' >' "".
#         | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#         \  \ `_.   \_ __\ /__ _/   .-` /  /
#     =====`-.____`.___ \_____/___.-`___.-'=====
#                       `=---='
#
#
#     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#               佛祖保佑         永无BUG
#



#                               |~~~~~~~|
#                               |       |
#                               |       |
#                               |       |
#                               |       |
#                               |       |
#    |~.\\\_\~~~~~~~~~~~~~~xx~~~         ~~~~~~~~~~~~~~~~~~~~~/_#;~|
#    |  \  o \_         ,XXXXX),                         _..-~ o /  |
#    |    ~~\  ~-.     XXXXX`)))),                 _.--~~   .-~~~   |
#     ~~~~~~~`\   ~\~~~XXX' _/ ';))     |~~~~~~..-~     _.-~ ~~~~~~~
#              `\   ~~--`_\~\, ;;;\)__.---.~~~      _.-~
#                ~-.       `:;;/;; \          _..-~~
#                   ~-._      `''        /-~-~
#                       `\              /  /
#                         |         ,   | |
#                          |  '        /  |
#                           \/;          |
#                            ;;          |
#                            `;   .       |
#                            |~~~-----.....|
#                           | \             \
#                          | /\~~--...__    |
#                          (|  `\       __-\|
#                          ||    \_   /~    |
#                          |)     \~-'      |
#                           |      | \      '
#                           |      |  \    :
#                            \     |  |    |
#                             |    )  (    )
#                              \  /;  /\  |
#                              |    |/   |
#                              |    |   |
#                               \  .'  ||
#                               |  |  | |
#                               (  | |  |
#                               |   \ \ |
#                               || o `.)|
#                               |`\\\\) |
#                               |       |
#                               |       |
#
#                           耶穌保佑    永無BUG

#        _.---,._,'
#       /' _.--.<
#         /'     `'
#       /' _.---._____
#       \.'   ___, .-'`
#           /'    \\             
#         /'       `-.           
#        |                       
#        |                   .-'~~~`-.
#        |                 .'         `.
#        |                 |  R  I  P  |
#        |                 |           |
#        |                 |   LIVER   |
#        |                 |   LUNGS   |
#        |                 |   TIMES   |
#        |                 |           |
#         \              \\|           |//
#   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
