#https://datatracker.ietf.org/doc/html/rfc7643#section-6
class Schema_attribute:
	def __init__(self, 
		name: str, 
		type: str,  
		multiValued: bool,
		description: str,
		required: bool,
		mutability: str,
		returned: str,
		uniqueness: str,
		caseExact: bool = False,
		subAttributes: list = None,
		referenceTypes: list = []
	):
		self.name = name
		self.type = str(type)
		self.subAttributes = subAttributes
		self.multiValued = multiValued
		self.description = description
		self.required = required
		self.caseExact = caseExact
		self.mutability = mutability
		self.returned = returned
		self.uniqueness = uniqueness
		self.referenceTypes = referenceTypes

	def as_dict(self):
		result = {
			"name": self.name,
			"type": self.type,
			"multiValued": self.multiValued,
			"description": self.description,
			"required": self.required,
			"caseExact": self.caseExact,
			"mutability": self.mutability,
			"returned": self.returned,
			"uniqueness": self.uniqueness
		}

		if(self.type == "reference"):
			result["referenceTypes"] = self.referenceTypes

		if(self.type == "complex"):
			result["subAttributes"] = self.subAttributes

		if(self.type == "string" or self.type == "reference"):
			result["caseExact"] = self.caseExact

		return result