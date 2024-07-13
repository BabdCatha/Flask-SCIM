from flask import Blueprint
from flask import json
from flask import request
from flask import Response
from flask import stream_with_context

from SCIM_classes import Schema_attribute

route_schemas = Blueprint("route_schemas", __name__)

#Schemas (User, Group)
#https://developer.4me.com/v1/scim/schemas/
@route_schemas.route("/Schemas", methods=["GET"])
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

	nameSubAttributes.append(Schema_attribute(
		name = "formatted",
		attributeType = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "The full name, including all middle names, titles, and suffixes as appropriate, formatted for display (e.g., 'Ms. Barbara J Jensen, III')."
	).as_dict())

	nameSubAttributes.append(Schema_attribute(
		name = "familyName",
		attributeType = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "The family name of the User, or last name in most Western languages (e.g., 'Jensen' given the full name 'Ms. Barbara J Jensen, III')."
	).as_dict())

	nameSubAttributes.append(Schema_attribute(
		name = "givenName",
		attributeType = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "The given name of the User, or first name in most Western languages (e.g., 'Barbara' given the full name 'Ms. Barbara J Jensen, III')."
	).as_dict())

	nameSubAttributes.append(Schema_attribute(
		name = "middleName",
		attributeType = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "The middle name(s) of the User (e.g., 'Jane' given the full name 'Ms. Barbara J Jensen, III')."
	).as_dict())

	nameSubAttributes.append(Schema_attribute(
		name = "honorificPrefix",
		attributeType = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "The honorific prefix(es) of the User, or title in most Western languages (e.g., 'Ms.' given the full name 'Ms. Barbara J Jensen, III')."
	).as_dict())

	nameSubAttributes.append(Schema_attribute(
		name = "honorificSuffix",
		attributeType = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "The honorific suffix(es) of the User, or suffix in most Western languages (e.g., 'III' given the full name 'Ms. Barbara J Jensen, III')."
	).as_dict())

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

	response = Response(
		response=json.dumps(responseDict),
		status=200,
		mimetype="application/scim+json"
	)

	return response