from flask import Flask
from flask_restful import Api, Resource, reqparse
from werkzeug.datastructures import FileStorage
from params import params
from utils import tokenValidator

# app = Flask(__name__)
# api = Api(app)

param=params()

class Upload(Resource):
    def post(self):
        '''
        user: username
        type: num/cv/nlp
        file: a file
        tokenstr: keypair1
        tokenint: keypair2
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=FileStorage, location='files',required=True)
        parser.add_argument('type',type=str,required=True)
        parser.add_argument('user',type=str,required=True)
        parser.add_argument('tokenstr',type=str,required=True)
        parser.add_argument('tokenint',type=int,required=True)
        args = parser.parse_args()
        file = args['file']
        prjtype=args['type']
        user=args['user']
        tokenstr=args['tokenstr']
        tokenint=args['tokenint']

        # check token
        if not tokenValidator(tokenstr,tokenint):
            return {"status":"error","msg":"token error","data":{}},201
        
        # check filetype
        pft=param.projectFileType
        filename=file.filename
        filetype=filename[filename.rfind("."):]
        if filetype!=pft[prjtype]:
            return {"status":"error","msg":"file type error","data":{}},201
        
        

        file.save('./'+param.filepath+"/"+file.filename)
        #TODO fileID
        #TODO check file
        return file.name, 201

# api.add_resource(Upload, '/upload')


# if __name__ == '__main__':
#     app.run(debug=True,port=8787,host='0.0.0.0')