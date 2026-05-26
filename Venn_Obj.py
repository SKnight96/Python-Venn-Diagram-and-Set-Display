

class VennObj():
	def __init__(self, tag, contents):
		self.tag = tag
		self.contents = contents
		self.overlap = []

	def __repr__(self):
		return f"VennObj(tag={self.tag!r}, contents={self.contents!r})"

	def __eq__(self, other):
		return self.tag == other.tag and self.contents == other.contents