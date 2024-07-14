from pymongo import MongoClient

from SCIM_classes import Schema_attribute

def main():

	#Connecting to the database
	try:
		uri = "mongodb://localhost:27017/"
		client = MongoClient(uri)
	except Exception as e:
		raise Exception("The following error occured: ", e)

	#The database can be reached
	database = client["Flask-SCIM"]

	#Deleting and recreating the Storing schemas
	schemasCollection = database["schemas"]
	schemasCollection.drop()

	result = schemasCollection.insert_one(getUserSchema())
	print("Stored user schema: " + "OK" if result.acknowledged else "KO")
 
	result = schemasCollection.insert_one(getGroupSchema())
	print("Stored group schema: " + "OK" if result.acknowledged else "KO")

	#Closing the connection to the database
	client.close()

def getGroupSchema():
	#Adding the group schema
	#Adding the User Schema
	Group = {}
	Group["id"] = "urn:ietf:params:scim:schemas:core:2.0:Group"
	Group["name"] = "Group"
	Group["description"] = "Group Schema"
	Group["meta"] = {
		"resourceType":"Schema",
		"location":"/Schemas/urn:ietf:params:scim:schemas:core:2.0:Group"
	}

	Group["attributes"] = []

	displayName = Schema_attribute(
		name = "displayName",
		type = "string",
		multiValued = False,
		required = True,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "server",
		description = "A human-readable name for the Group."
	)
	Group["attributes"].append(displayName.as_dict())

	groupType = Schema_attribute(
		name = "groupType",
		type = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "Used to identify the relationship between the organization and the group. Typical values used might be 'Organization', 'Site', 'Team', but any value may be used."
	)
	Group["attributes"].append(groupType.as_dict())

	membersSubAttributes = []

	membersSubAttributes.append(Schema_attribute(
		name = "value",
		type = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "immutable",
		returned = "default",
		uniqueness = "none",
		description = "Identifier of the member of this Group."
	).as_dict())

	membersSubAttributes.append(Schema_attribute(
		name = "$ref",
		type = "reference",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "immutable",
		returned = "default",
		uniqueness = "none",
		referenceTypes = ["Group", "User"],
		description = "The URI corresponding to a SCIM resource that is a member of this Group."
	).as_dict())

	membersSubAttributes.append(Schema_attribute(
		name = "type",
		type = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "immutable",
		returned = "default",
		uniqueness = "none",
		description = "A label indicating the type of resource, e.g., 'User' or 'Group'."
	).as_dict())

	members = Schema_attribute(
		name = "members",
		type = "complex",
		multiValued = True,
		required = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "A list of members of the Group.",
		subAttributes = membersSubAttributes
	)
	Group["attributes"].append(members.as_dict())

	return Group


def getUserSchema():
	#Adding the User Schema
	User = {}
	User["id"] = "urn:ietf:params:scim:schemas:core:2.0:User"
	User["name"] = "User"
	User["description"] = "User Schema"
	User["meta"] = {
		"resourceType":"Schema",
		"location":"/Schemas/urn:ietf:params:scim:schemas:core:2.0:User"
	}

	#Adding the different attributes
	#https://datatracker.ietf.org/doc/html/rfc7643#section-4.1

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

	addressesSubAttributes = []

	addressesSubAttributes.append(Schema_attribute(
		name = "formatted",
		type = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "The full mailing address, formatted for display or use with a mailing label. This attribute MAY contain newlines."
	).as_dict())

	addressesSubAttributes.append(Schema_attribute(
		name = "streetAddress",
		type = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "The full street address component, which may include house number, street name, P.O. box, and multi-line extended street address information. This attribute MAY contain newlines."
	).as_dict())

	addressesSubAttributes.append(Schema_attribute(
		name = "locality",
		type = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "The city or locality component."
	).as_dict())

	addressesSubAttributes.append(Schema_attribute(
		name = "region",
		type = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "The state or region component."
	).as_dict())

	addressesSubAttributes.append(Schema_attribute(
		name = "postalCode",
		type = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "The zip or postal code component."
	).as_dict())

	addressesSubAttributes.append(Schema_attribute(
		name = "country",
		type = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "The country name component."
	).as_dict())

	addressesSubAttributes.append(Schema_attribute(
		name = "type",
		type = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "A label indicating the attribute's function, e.g., 'work address' or 'home address'."
	).as_dict())

	addresses = Schema_attribute(
		name = "addresses",
		type = "complex",
		multiValued = True,
		required = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "A physical mailing address for this User.",
		subAttributes = addressesSubAttributes
	)
	User["attributes"].append(addresses.as_dict())

	groupsSubAttributes = []

	groupsSubAttributes.append(Schema_attribute(
		name = "value",
		type = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readOnly",
		returned = "default",
		uniqueness = "none",
		description = "The identifier of the User's group."
	).as_dict())

	groupsSubAttributes.append(Schema_attribute(
		name = "$ref",
		type = "reference",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readOnly",
		returned = "default",
		uniqueness = "none",
		referenceTypes = ["Group"],
		description = "The URI of the corresponding 'Group' resource to which the user belongs."
	).as_dict())

	groupsSubAttributes.append(Schema_attribute(
		name = "display",
		type = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readOnly",
		returned = "default",
		uniqueness = "none",
		description = "A human-readable name, primarily used for display purposes."
	).as_dict())

	groupsSubAttributes.append(Schema_attribute(
		name = "type",
		type = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "A label indicating the attribute's function, e.g., 'direct' or 'indirect'."
	).as_dict())

	groups = Schema_attribute(
		name = "groups",
		type = "complex",
		multiValued = True,
		required = False,
		mutability = "readOnly",
		returned = "default",
		uniqueness = "none",
		description = "A list of groups to which the user belongs, either through direct membership, through nested groups, or dynamically calculated.",
		subAttributes = groupsSubAttributes
	)
	User["attributes"].append(groups.as_dict())

	entitlementsSubAttributes = []

	entitlementsSubAttributes.append(Schema_attribute(
		name = "value",
		type = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "The value of an entitlement."
	).as_dict())

	entitlementsSubAttributes.append(Schema_attribute(
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

	entitlementsSubAttributes.append(Schema_attribute(
		name = "type",
		type = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "A label indicating the attribute's function."
	).as_dict())

	entitlementsSubAttributes.append(Schema_attribute(
		name = "primary",
		type = "boolean",
		multiValued = False,
		required = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "A Boolean value indicating the 'primary' or preferred attribute value for this attribute, e.g., the preferred mailing address or primary email address. The primary attribute value 'true' MUST appear no more than once."
	).as_dict())

	entitlements = Schema_attribute(
		name = "entitlements",
		type = "complex",
		multiValued = True,
		required = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "A list of entitlements for the User that represent a thing the User has.",
		subAttributes = entitlementsSubAttributes
	)
	User["attributes"].append(entitlements.as_dict())

	rolesSubAttributes = []

	rolesSubAttributes.append(Schema_attribute(
		name = "value",
		type = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "The value of a role."
	).as_dict())

	rolesSubAttributes.append(Schema_attribute(
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

	rolesSubAttributes.append(Schema_attribute(
		name = "type",
		type = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "A label indicating the attribute's function."
	).as_dict())

	rolesSubAttributes.append(Schema_attribute(
		name = "primary",
		type = "boolean",
		multiValued = False,
		required = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "A Boolean value indicating the 'primary' or preferred attribute value for this attribute, e.g., the preferred mailing address or primary email address. The primary attribute value 'true' MUST appear no more than once."
	).as_dict())

	roles = Schema_attribute(
		name = "roles",
		type = "complex",
		multiValued = True,
		required = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "A list of roles for the User that collectively represent who the User is, e.g., 'Student', 'Faculty'.",
		subAttributes = rolesSubAttributes
	)
	User["attributes"].append(roles.as_dict())

	x509CertificatesSubAttributes = []

	x509CertificatesSubAttributes.append(Schema_attribute(
		name = "value",
		type = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "The value of an X.509 certificate."
	).as_dict())

	x509CertificatesSubAttributes.append(Schema_attribute(
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

	x509CertificatesSubAttributes.append(Schema_attribute(
		name = "type",
		type = "string",
		multiValued = False,
		required = False,
		caseExact = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "A label indicating the attribute's function."
	).as_dict())

	x509CertificatesSubAttributes.append(Schema_attribute(
		name = "primary",
		type = "boolean",
		multiValued = False,
		required = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "A Boolean value indicating the 'primary' or preferred attribute value for this attribute, e.g., the preferred mailing address or primary email address. The primary attribute value 'true' MUST appear no more than once."
	).as_dict())

	x509Certificates = Schema_attribute(
		name = "x509Certificates",
		type = "complex",
		multiValued = True,
		required = False,
		mutability = "readWrite",
		returned = "default",
		uniqueness = "none",
		description = "A list of certificates issued to the User.",
		subAttributes = x509CertificatesSubAttributes
	)
	User["attributes"].append(x509Certificates.as_dict())

	return User

if __name__ == '__main__':
	main()