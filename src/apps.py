from flask import Flask
from flask_restful import Api

'''
@ import API
'''
from resources.dataService.upload import Upload

app = Flask(__name__)
api = Api(app)

api.add_resource(Upload, "/upload")

if __name__ == "__main__":
    app.run(debug=True,port=8787,host='0.0.0.0')