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
    
    