#!flask/bin/python
#
# CoinAuth - Service for Authenticating the owner of a Bitcoin Address
# Copyright (C) 2014 Daniel Rice drice@greenmangosystems.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from flask import Flask, jsonify, abort, request, make_response, url_for
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
import bitcoin
from noncestore import NonceStore

app = Flask(__name__, static_url_path = "")
api = Api(app)

noncedb = NonceStore(60*30) #Store nonces 30 minutes which is more than enough

class ValidationAPI(Resource):
	def __init__(self):
		super(ValidationAPI, self).__init__()
	
	def get(self, nonce, btcaddress, signature):
		return { 'result': noncedb.nonce_find_and_remove(int(nonce)) }

class RequestNonceAPI(Resource):
	def __init__(self):
		super(RequestNonceAPI, self).__init__()

	def get(self):
		return { 'nonce': noncedb.generate_nonce() }

api.add_resource(RequestNonceAPI, '/coinauth/api/v0.1/requestnonce/', endpoint = 'requestnonce')
api.add_resource(ValidationAPI, '/coinauth/api/v0.1/validate/<nonce>/<btcaddress>/<signature>', endpoint = 'validate')
    
if __name__ == '__main__':
    app.run(debug = True)
