# 你是接手這個東西的小可愛麼 (*´･д･)?
# 是的話恭喜你哦 (✧≖‿ゝ≖)
# 不是的話趕緊關掉回地球吧 這裡很可怕的 (°ཀ°)
# 大部分代碼和架構都是在喝了一瓶酒才開始寫ㄉ ( ´∀｀)つt[ ]
# 寫的時候只有我和神知道在幹嘛  (༼•̀ɷ•́༽)
# 現在只有神知道了 ( ￣ 3￣)y▂ξ
# 代碼成分：酒精 (80%)、尼古丁 (10%)、肝(6%)、青春歲月(3%)，以及一點點的 flask,sql,sklearn,keras,matplotlib (1%)

from flask import Flask
from flask_restful import Api
import logging
import sys
from params import params

par=params()

#import API
from resources.dataService.upload import Upload
from resources.dataService.download import Download
from resources.dataService.getColumn import getColumn
from resources.dataService.getFileStatus import getFileStatus
from resources.dataService.delete import DeleteFile


app = Flask(__name__)
api = Api(app)

# bind api
api.add_resource(Upload, "/data/upload")
api.add_resource(Download,'/data/download')
api.add_resource(getColumn,'/data/getcol')
api.add_resource(getFileStatus,'/data/getstatus')
api.add_resource(DeleteFile,'/data/delete')

if __name__ == "__main__":

    if '--debug' in sys.argv:
        logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')
    else:
        logging.basicConfig(level=logging.INFO , format='[%(levelname)s] %(message)s')
    logging.info(f'InCore running at port {par.port}')
    app.run(debug='--debug' in sys.argv,port=par.port,host='0.0.0.0')
    

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

# 觀自在菩薩。行深般若波羅蜜多時。照見五蘊皆空。度一切苦厄。舍利子。色不異空。空不異色。色即是空。空即是色。受想行識。亦復如是。舍利子。是諸法空相。不生不滅。不垢不淨。不增不減。是故空中無色。無受想行識。無眼耳鼻舌身意。無色聲香味觸法。無眼界。乃至無意識界。無無明。亦無無明盡。乃至無老死。亦無老死盡。無苦集滅道。無智亦無得。以無所得故。菩提薩埵。依般若波羅蜜多故。心無罣礙。無罣礙故。無有恐怖。遠離顛倒夢想。究竟涅槃。三世諸佛。依般若波羅蜜多故。得阿耨多羅三藐三菩提。故知般若波羅蜜多。是大神咒。是大明咒。是無上咒。是無等等咒。能除一切苦。真實不虛。故說般若波羅蜜多咒。即說咒曰。
# 揭諦揭諦　波羅揭諦　波羅僧揭諦　菩提薩婆訶

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
