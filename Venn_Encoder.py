from json import JSONEncoder
from Venn_Obj import VennObj

class VennEncoder(JSONEncoder):
	def default(self, obj):
		if isinstance(obj, VennObj):# problem here. can't return the list of overlapping objs
			overlap_list = []
			for i in obj.overlap:
				overlap_list.append(i.tag)
			return {"__type__": "VennObj", "tag": obj.tag, "contents": obj.contents, "overlap": overlap_list}
		return super().default(obj)