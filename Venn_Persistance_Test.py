import os
from unittest import TestCase
from unittest import main
from Venn_Controller import VennController
from Venn_Obj import VennObj

#run these test with the command line [ python -m unittest -v Venn_Persistance_Test.py ]
#from the primary Venn Diagram Project directory

class PersistanceTest(TestCase):
	def setUp(self):
		self.Controller = VennController()
	
	def tearDown(self):
		file_name = "venn_test_file.json"
		save_path = "records"

		file_exists = os.path.exists(file_name)
		if os.path.exists(save_path):
			filenames = os.listdir(save_path)
			for filename in filenames:
				if ".dat" not in filename:
					continue
				save_file_path = os.path.join(save_path, filename)
				if os.path.isfile(save_file_path):
					os.remove(save_file_path)
		if file_exists:
			os.remove(file_name)

	def reset_persistence(self):
		self.Controller = VennController()

	def test_create_search_set(self):
		self.assertTrue(self.Controller.create_set("test", [1, 2, 3]), "can create new set")

		self.assertEqual(self.Controller.total_elements, 3, "correct number of elements")

		self.assertFalse(self.Controller.create_set("test", [4, 5, 6]), "cannot create set with existing tag")

		self.assertIsNotNone(self.Controller.search_set("test"), "can find existing tag")

		self.assertIsNone(self.Controller.search_set("fail"), "cannot find nonexistant tag")

		self.Controller.create_set("test_another", [3, 4, 5])
		self.assertEqual(self.Controller.total_elements, 5, "correct number of elements after new addition")

		self.Controller.save_sets("records/venn_test_file.json")
		self.reset_persistence()

		self.assertFalse(self.Controller.load_sets("venn_test_file.json"), "can't find file in improper directory")

		self.assertTrue(self.Controller.load_sets("records/venn_test_file.json"), "finds saved file")

		self.assertIsNotNone(self.Controller.search_set("test_another"), "can find existing tag")

		self.assertEqual(self.Controller.total_elements, 5, "correct number of elements after new addition")

		set_check_1 = self.Controller.search_set("test")
		set_check_2 = self.Controller.search_set("test_another")
		self.assertTrue(set_check_1 in set_check_2.overlap, "overlap restored")

	def test_retrieve_sets(self):
		self.Controller.create_set("test", [1, 2, 3])
		self.Controller.create_set("test_another", [3, 4, 5])

		expected_set_1 = VennObj("test", [1, 2, 3])
		expected_set_2 = VennObj("test_another", [3, 4, 5])
		result = self.Controller.retrieve_sets([3])
		self.assertEqual(result, [expected_set_1, expected_set_2], "correct list of sets")

		result = self.Controller.retrieve_sets([1])
		self.assertEqual(result, [expected_set_1], "correct list of sets")

		self.Controller.create_set("test_one_more", [4, 5, 6, 7])
		expected_set_3 = VennObj("test_one_more", [4, 5, 6, 7])
		result = self.Controller.retrieve_sets([5, 4])
		self.assertEqual(result, [expected_set_2, expected_set_3], "correct list of sets")

		self.Controller.save_sets("records/venn_test_file.json")
		self.reset_persistence()
		self.Controller.load_sets("records/venn_test_file.json")

		result = self.Controller.retrieve_sets([3])
		self.assertEqual(result, [expected_set_1, expected_set_2], "correct list of sets")

		result = self.Controller.retrieve_sets([5, 4])
		self.assertEqual(result, [expected_set_2, expected_set_3], "correct list of sets")

	def test_retrieve_intersect(self):
		self.Controller.create_set("test_1", [1, 2, 3, 4])
		self.Controller.create_set("test_2", [3, 4, 5, 6, 7])
		expected_list = [3, 4]

		self.assertEqual(self.Controller.retrieve_intersect("test_1", "test_2"), expected_list, "correct elements of overlapping sets")

		self.assertEqual(self.Controller.retrieve_intersect("test_1", "test_3"), [], "no elements with invalid tag")

		self.Controller.create_set("test_3", [5, 6, 7])
		self.assertEqual(self.Controller.retrieve_intersect("test_1", "test_3"), [], "no elements with no overlap")

		self.Controller.save_sets("records/venn_test_file.json")
		self.reset_persistence()
		self.Controller.load_sets("records/venn_test_file.json")

		self.assertEqual(self.Controller.retrieve_intersect("test_1", "test_2"), expected_list, "correct elements of overlapping sets")