import json

class json_helper():
	def getAsJSONObject(self, obj):
	    output = ""
	    if obj:
	        output = json.dumps(obj)
	    return output

	def getAsJSON(self, result):
	    output = ""
	    if result:
	        output = json.dumps([p.to_dict() for p in result])
	    return output