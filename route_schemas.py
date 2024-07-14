from flask import Blueprint
from flask import json
from flask import request
from flask import Response
from flask import stream_with_context
from pymongo import MongoClient

from SCIM_classes import Schema_attribute

route_schemas = Blueprint("route_schemas", __name__)

#Schemas (User, Group)
#https://developer.4me.com/v1/scim/schemas/
@route_schemas.route("/Schemas", methods=["GET"])
def Schemas():

	#Connecting to the database
	try:
		uri = "mongodb://localhost:27017/"
		client = MongoClient(uri)
	except Exception as e:
		raise Exception("The following error occured: ", e)

	#The database can be reached
	database = client["Flask-SCIM"]
	collection = database["schemas"]

	responseDict = {"schemas":["urn:ietf:params:scim:api:messages:2.0:ListResponse"]}

	Resources = []

	#Finding all schemas stored in the database
	results = collection.find()
	for document in results:
		if(document is not None):
			del document["_id"]
			Resources.append(document)

	responseDict["Resources"] = Resources
	responseDict["totalResults"] = len(Resources)

	response = Response(
		response=json.dumps(responseDict),
		status=200,
		mimetype="application/scim+json"
	)

	#Closing the connection to the database
	client.close()

	return response

@route_schemas.route("/Schemas/<urn>", methods=["GET"])
def Schema(urn):

	#Connecting to the database
	try:
		uri = "mongodb://localhost:27017/"
		client = MongoClient(uri)
	except Exception as e:
		raise Exception("The following error occured: ", e)

	#The database can be reached
	database = client["Flask-SCIM"]
	collection = database["schemas"]

	responseDict = getSchemaFromDatabase(collection, urn)

	if(responseDict is None):
		responseDict = {
			"status":404,
			"schemas": [
				"urn:ietf:params:scim:api:messages:2.0:Error"
			],
			"detail":"Resource '" + urn + "' does not exist."
		}
	else:
		responseDict["schemas"] = ["urn:ietf:params:scim:schemas:core:2.0:Schema"]

	response = Response(
		response=json.dumps(responseDict),
		status=200,
		mimetype="application/scim+json"
	)

	#Closing the connection to the database
	client.close()

	return response


def getSchemaFromDatabase(collection, id):

	result = collection.find_one({"id": id})

	#Removing the _id key returned by MongoDB
	if(result is not None):
		del result["_id"]

	return result