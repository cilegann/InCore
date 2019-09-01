from flask import Flask
from flask_restful import Api
from controller import controller,stop
import sys
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources=r"/*")

# bind api
api.add_resource(controller,"/train")
api.add_resource(stop,"/stop")
app.run(debug=True,port=8787,host='0.0.0.0')