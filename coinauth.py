#!flask/bin/python

from flask import Flask, jsonify, abort, request, make_response, url_for
from flask.views import MethodView
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
import validatebitcoinaddress

app = Flask(__name__, static_url_path = "")
api = Api(app)

class ValidationAPI(Resource):
	def __init__(self):
		super(ValidationAPI, self).__init__()

	def get(self, token, signature):
		return { 'signature': signature }

class RequestTokenAPI(Resource):
    def __init__(self):
        super(RequestTokenAPI, self).__init__()
        
    def get(self, pubaddress):
        return { 'token': pubaddress }

api.add_resource(RequestTokenAPI, '/coinauth/api/v0.1/requesttoken/<pubaddress>', endpoint = 'requesttoken')
api.add_resource(ValidationAPI, '/coinauth/api/v0.1/validate/<token>/<signature>', endpoint = 'validate')
    
if __name__ == '__main__':
    app.run(debug = True)
