from flask import Flask
from flask import json
from flask import request

from SCIM_classes import Schema_attribute

from route_schemas import route_schemas

app = Flask(__name__)

#Root of the server
@app.route("/")
def root():
	return "/"

##Service Provider Configuration Endpoints (https://datatracker.ietf.org/doc/html/rfc7644#section-4)
#ServiceProviderConfig
@app.route("/ServiceProviderConfig", methods=["GET"])
def ServiceProviderConfig():

	responseDict = {"schemas":["urn:ietf:params:scim:schemas:core:2.0:ServiceProviderConfig"]}

	#Adding the different capabilities of the server
	#https://datatracker.ietf.org/doc/html/rfc7643#section-5
	responseDict["patch"] = {"supported":False}

	responseDict["bulk"] = {
		"supported":False,
		"maxOperations":0,
		"maxPayloadSize":0
	}

	responseDict["filter"] = {
		"supported":False,
		"maxResults":0
	}

	responseDict["changePassword"] = {"supported":False}

	responseDict["etag"] = {"supported":False}

	responseDict["authenticationSchemes"] = []
	responseDict["authenticationSchemes"].append({
		"type":"httpbasic",
		"name":"HTTP Basic Auth",
		"description":"HTTP Basic Auth Scheme. Base64($Username:$Password)"
	})

	response = app.response_class(
		response=json.dumps(responseDict),
		status=200,
		mimetype="application/scim+json"
	)

	return response

app.register_blueprint(route_schemas)

#main driver function
if __name__ == '__main__':
	app.run()