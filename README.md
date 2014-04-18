CoinAuth
========

A service for authenticating the owner of a Bitcoin address

The purpose of this project is to create a method for an app or web service to verify that a person is in fact the owner of a particular Bitcoin address. In other words, to verify that they are in posession of the private key for a particular Bitcoin address without providing the private key.

Basic flow of this service is as follows:
-Client requests a token from the service
-Service responds with token
-Client responds with token, bitcoin public address, and token signature
-Service responds with verification results (success or failure of challeng response for supplied bitcoin address)

Service is built on top of Flask-RESTful http://flask-restful.readthedocs.org/en/latest/
