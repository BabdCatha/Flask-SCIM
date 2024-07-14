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

	User = getUserSchema()
	Resources.append(User)

	responseDict["Resources"] = Resources
	responseDict["totalResults"] = len(Resources)

	response = Response(
		response=json.dumps(responseDict),
		status=200,
		mimetype="application/scim+json"
	)

	return response

def getUserSchema():
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
		type = "string",
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
		type = "string",
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
		type = "string",
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
		type = "string",
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
		type = "string",
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
		type = "string",
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
		type = "string",
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
		type = "complex",
		multiValued = False,
		required = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "The components of the user's name",
		subAttributes = nameSubAttributes
	)
	User["attributes"].append(name.as_dict())

	displayName = Schema_attribute(
		name = "displayName",
		type = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "The name of the User, suitable for display to end-users.  The name SHOULD be the full name of the User being described, if known."
	)
	User["attributes"].append(displayName.as_dict())

	nickName = Schema_attribute(
		name = "nickName",
		type = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "The casual way to address the user in real life, e.g., 'Bob' or 'Bobby' instead of 'Robert'.  This attribute SHOULD NOT be used to represent a User's username (e.g., 'bjensen' or 'mpepperidge')."
	)
	User["attributes"].append(nickName.as_dict())

	profileUrl = Schema_attribute(
		name = "profileUrl",
		type = "reference",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		referenceTypes = ["external"],
		description = "A fully qualified URL pointing to a page representing the User's online profile."
	)
	User["attributes"].append(profileUrl.as_dict())

	title = Schema_attribute(
		name = "title",
		type = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "The user's title, such as 'Vice President.'"
	)
	User["attributes"].append(title.as_dict())

	userType = Schema_attribute(
		name = "userType",
		type = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "Used to identify the relationship between the organization and the user. Typical values used might be 'Contractor', 'Employee', 'Intern', 'Temp', 'External', and 'Unknown', but any value may be used."
	)
	User["attributes"].append(userType.as_dict())

	preferredLanguage = Schema_attribute(
		name = "preferredLanguage",
		type = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "Indicates the User's preferred written or spoken language.  Generally used for selecting a localized user interface; e.g., 'en_US' specifies the language English and country US."
	)
	User["attributes"].append(preferredLanguage.as_dict())

	locale = Schema_attribute(
		name = "locale",
		type = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "Used to indicate the User's default location for purposes of localizing items such as currency, date time format, or numerical representations."
	)
	User["attributes"].append(locale.as_dict())

	timezone = Schema_attribute(
		name = "timezone",
		type = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "The User's time zone in the 'Olson' time zone database format, e.g., 'America/Los_Angeles'."
	)
	User["attributes"].append(timezone.as_dict())

	active = Schema_attribute(
		name = "active",
		type = "boolean",
		multiValued = False,
		required = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "A Boolean value indicating the User's administrative status."
	)
	User["attributes"].append(active.as_dict())

	password = Schema_attribute(
		name = "password",
		type = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "writeOnly",
		returned = "never",
		uniqueness = "none",
		description = "The User's cleartext password. This attribute is intended to be used as a means to specify an initial password when creating a new User or to reset an existing User's password."
	)
	User["attributes"].append(password.as_dict())

	emailsSubAttributes = []

	emailsSubAttributes.append(Schema_attribute(
		name = "value",
		type = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "Email address for the user. The value SHOULD be canonicalized by the service provider, e.g., 'bjensen@example.com' instead of 'bjensen@EXAMPLE.COM'."
	).as_dict())

	emailsSubAttributes.append(Schema_attribute(
		name = "display",
		type = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "A human-readable name, primarily used for display purposes."
	).as_dict())

	emailsSubAttributes.append(Schema_attribute(
		name = "type",
		type = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "A label indicating the attribute's function, e.g., 'work' or 'home'."
	).as_dict())

	emailsSubAttributes.append(Schema_attribute(
		name = "primary",
		type = "boolean",
		multiValued = False,
		required = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "A Boolean value indicating the 'primary' or preferred attribute value for this attribute, e.g., the preferred mailing address or primary email address.  The primary attribute value 'true' MUST appear no more than once."
	).as_dict())

	emails = Schema_attribute(
		name = "emails",
		type = "complex",
		multiValued = True,
		required = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "Email addresses for the user. The value SHOULD be canonicalized by the service provider, e.g., 'bjensen@example.com' instead of 'bjensen@EXAMPLE.COM'.",
		subAttributes = emailsSubAttributes
	)
	User["attributes"].append(emails.as_dict())

	phoneNumbersSubAttributes = []

	phoneNumbersSubAttributes.append(Schema_attribute(
		name = "value",
		type = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "Phone number of the User."
	).as_dict())

	phoneNumbersSubAttributes.append(Schema_attribute(
		name = "display",
		type = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "A human-readable name, primarily used for display purposes."
	).as_dict())

	phoneNumbersSubAttributes.append(Schema_attribute(
		name = "type",
		type = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "A label indicating the attribute's function, e.g., 'work' or 'home'."
	).as_dict())

	phoneNumbersSubAttributes.append(Schema_attribute(
		name = "primary",
		type = "boolean",
		multiValued = False,
		required = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "A Boolean value indicating the 'primary' or preferred attribute value for this attribute, e.g., the preferred or primary phone number.  The primary attribute value 'true' MUST appear no more than once."
	).as_dict())

	phoneNumbers = Schema_attribute(
		name = "phoneNumbers",
		type = "complex",
		multiValued = True,
		required = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "Phone numbers for the User. The value SHOULD be canonicalized by the service provider according to the format specified in RFC 3966, e.g., 'tel:+1-201-555-0123'.",
		subAttributes = phoneNumbersSubAttributes
	)
	User["attributes"].append(phoneNumbers.as_dict())

	imsSubAttributes = []

	imsSubAttributes.append(Schema_attribute(
		name = "value",
		type = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "Instant messaging address for the User."
	).as_dict())

	imsSubAttributes.append(Schema_attribute(
		name = "display",
		type = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "A human-readable name, primarily used for display purposes."
	).as_dict())

	imsSubAttributes.append(Schema_attribute(
		name = "type",
		type = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "A label indicating the attribute's function, e.g., 'aim', 'gtalk', 'xmpp'."
	).as_dict())

	imsSubAttributes.append(Schema_attribute(
		name = "primary",
		type = "boolean",
		multiValued = False,
		required = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "A Boolean value indicating the 'primary' or preferred attribute value for this attribute, e.g., the preferred instant messaging address.  The primary attribute value 'true' MUST appear no more than once."
	).as_dict())

	ims = Schema_attribute(
		name = "ims",
		type = "complex",
		multiValued = True,
		required = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "Instant messaging addresses for the User.",
		subAttributes = imsSubAttributes
	)
	User["attributes"].append(ims.as_dict())

	photosSubAttributes = []

	photosSubAttributes.append(Schema_attribute(
		name = "value",
		type = "reference",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		referenceTypes = ["external"],
		description = "URLs of a photo of the User."
	).as_dict())

	photosSubAttributes.append(Schema_attribute(
		name = "display",
		type = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "A human-readable name, primarily used for display purposes."
	).as_dict())

	photosSubAttributes.append(Schema_attribute(
		name = "type",
		type = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "A label indicating the attribute's function, i.e., 'photo' or 'thumbnail'."
	).as_dict())

	photosSubAttributes.append(Schema_attribute(
		name = "primary",
		type = "boolean",
		multiValued = False,
		required = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "A Boolean value indicating the 'primary' or preferred attribute value for this attribute, e.g., the preferred profile picture.  The primary attribute value 'true' MUST appear no more than once."
	).as_dict())

	photos = Schema_attribute(
		name = "photos",
		type = "complex",
		multiValued = True,
		required = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "URLs of photos of the User.",
		subAttributes = photosSubAttributes
	)
	User["attributes"].append(photos.as_dict())

	return User