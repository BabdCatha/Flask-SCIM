from flask import Flask
from flask import json
from flask import request

from SCIM_classes import Schema_attribute

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

#Schemas (User, Group)
#https://developer.4me.com/v1/scim/schemas/
@app.route("/Schemas", methods=["GET"])
def Schemas():

	responseDict = {"schemas":["urn:ietf:params:scim:schemas:core:2.0:Schema"]}

	Resources = []

	#Adding the User Schema
	User = {}
	User["id"] = "urn:ietf:params:scim:schemas:core:2.0:User"
	User["name"] = "User"
	User["description"] = "User Schema"
	User["meta"] = {
		"resourceType":"Schema",
		"location":request.url_rule.rule + "/urn:ietf:params:scim:schemas:core:2.0:User"
	}

	#Adding the different attributes
	#https://datatracker.ietf.org/doc/html/rfc7643#section-4.1
	UserAttributes = []

	User["attributes"] = []

	userName = Schema_attribute(
		name = "userName",
		attributeType = "string",
		multiValued = False,
		required = True,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "server",
		description = "Unique identifier for user"
	)
	User["attributes"].append(userName.as_dict())

	nameSubAttributes = []

	name = Schema_attribute(
		name = "name",
		attributeType = "complex",
		multiValued = False,
		required = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "The components of the user's name",
		subAttributes = nameSubAttributes
	)
	User["attributes"].append(name.as_dict())

	Resources.append(User)

	responseDict["Resources"] = Resources
	responseDict["totalResults"] = len(Resources)

	response = app.response_class(
		response=json.dumps(responseDict),
		status=200,
		mimetype="application/scim+json"
	)

	return response

#main driver function
if __name__ == '__main__':
	app.run()