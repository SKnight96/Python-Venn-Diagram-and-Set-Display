from json import JSONDecoder
from Venn_Obj import VennObj

class VennDecoder(JSONDecoder):
	def __init__(self, *args, **kwargs):
		super().__init__(object_hook=self.object_hook, *args, **kwargs)

	def object_hook(self, dct):
		if '__type__' in dct and dct['__type__'] == 'VennObj':
			venn_obj = VennObj(dct['tag'], dct['contents'])
			venn_obj.overlap = dct['overlap']
			return venn_obj
		return dct