from Venn_Obj import VennObj
import json
from Venn_Encoder import VennEncoder
from Venn_Decoder import VennDecoder

class VennController:

	def __init__(self):
		self.sets = []# list containing each set object
		self.all_elements = []# tracker list for each unique element in the set
		self.total_elements = 0# number of elements in the tracker list
		self.num_sets = 0
		self.set_size_avrg = 0

	#writes the contents of self.sets to a file
	def save_sets(self, filename):
		with open(filename, 'w') as file:
			for i in self.sets:
				temp = json.dumps(i, cls=VennEncoder)
				file.write(temp + "\n")

	#loads the contents from a file to self.sets and sets other variables accordingly
	def load_sets(self, filename):
		try:
			with open(filename, 'r') as file:
				self.sets = []
				self.all_elements = []
				self.total_elements = 0
				self.num_sets = 0
				self.set_size_avrg = 0
				for line in file.readlines():
					temp = json.loads(line, cls=VennDecoder)
					self.sets.append(temp)
					self.num_sets += 1
			for i in self.sets:# for each imported set
				for j in i.contents:# correct the controller value trackers
					if j not in self.all_elements:
						self.all_elements.append(j)
						self.total_elements += 1
				correct_overlap = []
				for k in i.overlap:# correct the overlapping sets
					correct_overlap.append(self.search_set(k))
				i.overlap = correct_overlap
			self.set_size_avrg = self.get_average_set_size()
			return True
		except:
			return False
			

	#returns a set with the given tag
	def search_set(self, tag):
		for i in self.sets:
			if i.tag == tag:
				return i
		return None

	#creates a set with the given tag and list of contents, and a list of sets with overlapping contents
	def create_set(self, tag, contents):
		if self.search_set(tag):
			return False # make an error class?
		new_set = VennObj(tag, contents)
		for i in contents:
			if i not in self.all_elements:# add any new elements to the tracker list
				self.all_elements.append(i)
				self.total_elements += 1

			for j in self.sets:# tie any overlapping sets together
				if i in j.contents and j not in new_set.overlap:
					new_set.overlap.append(j)
					j.overlap.append(new_set)
					#print("sets " + j.tag + " and the new set " + new_set.tag + " have overlapping contents")
		self.sets.append(new_set)
		self.num_sets += 1
		self.set_size_avrg = self.get_average_set_size()
		return True

	#returns a list of all sets containing the given list of elements
	def retrieve_sets(self, elements):
		matching_sets = []
		match_found = True
		for i in self.sets:
			for j in elements:
				if j not in i.contents:
					match_found = False
					break
			if match_found == True:
				matching_sets.append(i)
			match_found = True
		return matching_sets

	#returns a list containing the elements contained in both sets with the given tags
	def retrieve_intersect(self, tag1, tag2):
		set_check1 = self.search_set(tag1)
		set_check2 = self.search_set(tag2)
		if set_check1 and set_check2:
			return [i for i in set_check1.contents if i in set_check2.contents]
		else:
			#raise setNotFound error
			return []

	#deletes a set with the given tag and its exclusive elements
	def delete_set(self, tag):
		set_check = self.search_set(tag)
		if set_check:
			for i in set_check.overlap:
				non_exclusive = []# fills with elements non-exclusive to the set
				# deleted so as to isolate which elements need to be removed
				# from the tracker list
				for j in set_check.contents:
					#print("checking contents of " + i.tag + " for the value " + str(j))
					if j in i.contents and j not in non_exclusive:
						#print("found " + str(j) + " in contents of " + i.tag)
						non_exclusive.append(j)
				i.overlap.remove(set_check)
				for j in non_exclusive:
					set_check.contents.remove(j)
			#print("local is now " + str(set_check.contents))
			for i in set_check.contents:
				#print("deleting " + str(i) + " from all_elements")
				self.all_elements.remove(i)
				self.total_elements -= 1
			self.sets.remove(set_check)
			self.num_sets -=1
			#print("all_elements now includes " + str(self.all_elements))
			self.set_size_avrg = self.get_average_set_size()
			return True
		else:
			return False

	#deletes the given element from all sets
	def delete_element(self, element):
		sets_containing = self.retrieve_sets([element])
		if len(sets_containing) == 0:
			return False
		self.all_elements.remove(element)
		self.total_elements -= 1
		num_sets = len(sets_containing)
		for i in range(0, num_sets):
			for j in range(i + 1, num_sets):
				#disconnect any sets that no longer overlap after element removal
				if len(self.retrieve_intersect(sets_containing[i].tag, sets_containing[j].tag)) == 1:
					#print("sets " + sets_containing[i].tag + " and " + sets_containing[j].tag + " no longer share elements")
					sets_containing[i].overlap.remove(sets_containing[j])
					sets_containing[j].overlap.remove(sets_containing[i])
		#afterwhich we remove the element from each set containing it
		for i in sets_containing:
			#print("removing " + str(element) + " from set with tag " + i.tag)
			i.contents.remove(element)
			if len(i.contents) == 0:#delete any set without remaining elements
				#print("set with tag " + i.tag + " no longer has any elements and will be deleted")
				self.delete_set(i.tag)# this can probably be a simple .remove from
				# self.sets, since I think everything delete_set covers would
				# have already been done at this point, save for adjusting num_sets
		print("all_elements now includes " + str(self.all_elements))
		self.set_size_avrg = self.get_average_set_size()
		return True


	def update_set(self, tag, new_tag, new_contents):
		set_check = self.search_set(tag)
		if set_check:

			'''new_contents = list(set_check.contents)
			for i in to_remove:
				new_contents = [x for x in new_contents if x != i]
			for j in to_add:
				new_contents.append(j)'''

			for i in self.sets:
				if i != set_check:
					# have to correct any changes in overlapping sets
					if set_check in i.overlap:
						# easiest to just assume the overlap is gone
						i.overlap.remove(set_check)
						set_check.overlap.remove(i)
					for j in new_contents:
						# before rechecking for overlap any making the
						# correction if some is found
						if j in i.contents:
							i.overlap.append(set_check)
							set_check.overlap.append(i)
							break
			set_check.tag = new_tag
			set_check.contents = new_contents
			self.set_size_avrg = self.get_average_set_size()
			return True
		else:
			return False

	def get_average_set_size(self):
		set_size_sum = 0
		if self.num_sets == 0:
			return 0

		for i in self.sets:
			set_size_sum += len(i.contents)
		return set_size_sum / self.num_sets


#BUG LIST HERE:
