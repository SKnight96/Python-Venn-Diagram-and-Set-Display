from unittest import TestCase
from unittest import main
from Venn_Controller import VennController
from Venn_Obj import VennObj

#run these tests with the line [ python -m unittest -v Venn_Controller_Test.py ]
#from CMD opened to the Venn Diagram Project folder

class ControllerTest(TestCase):
	def setUp(self):
		self.Controller = VennController()

	def test_create_search_set(self):

		self.assertTrue(self.Controller.create_set("test", [1, 2, 3]), "can create new set")

		self.assertEqual(self.Controller.total_elements, 3, "correct number of elements")

		self.assertFalse(self.Controller.create_set("test", [4, 5, 6]), "cannot create set with existing tag")

		self.assertIsNotNone(self.Controller.search_set("test"), "can find existing tag")

		self.assertIsNone(self.Controller.search_set("fail"), "cannot find nonexistant tag")

		self.Controller.create_set("test_another", [3, 4, 5])
		self.assertEqual(self.Controller.total_elements, 5, "correct number of elements after new addition")

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

	def test_retrieve_intersect(self):
		self.Controller.create_set("test_1", [1, 2, 3, 4])
		self.Controller.create_set("test_2", [3, 4, 5, 6, 7])
		expected_list = [3, 4]

		self.assertEqual(self.Controller.retrieve_intersect("test_1", "test_2"), expected_list, "correct elements of overlapping sets")

		self.assertEqual(self.Controller.retrieve_intersect("test_1", "test_3"), [], "no elements with invalid tag")

		self.Controller.create_set("test_3", [5, 6, 7])
		self.assertEqual(self.Controller.retrieve_intersect("test_1", "test_3"), [], "no elements with no overlap")

	def test_delete_set(self):
		self.Controller.create_set("test", [1, 2, 3])
		self.Controller.create_set("test_another", [3, 4, 5])
		self.Controller.create_set("test_one_more", [4, 5, 6, 7])

		self.assertFalse(self.Controller.delete_set("bad_test"), "set with tag does not exist")

		self.assertTrue(self.Controller.delete_set("test_another"), "set with tag is found and removed")

		self.assertEqual(self.Controller.total_elements, 7, "correct element total count after set removal")

		self.assertEqual(self.Controller.all_elements, [1, 2, 3, 4, 5, 6, 7], "correct element list after set removal")

		expected_set_1 = VennObj("test", [1, 2, 3])
		expected_set_2 = VennObj("test_one_more", [4, 5, 6, 7])
		result_1 = self.Controller.retrieve_sets([3])
		self.assertEqual(result_1, [expected_set_1], "overlapping set still contains value after set removal")
		result_2 = self.Controller.retrieve_sets([4, 5])
		self.assertEqual(result_2, [expected_set_2], "overlapping set still contains value after set removal")

		self.Controller.create_set("one_last_set", [6, 7, 8, 9])
		expected_set_3 = VennObj("one_last_set", [6, 7, 8, 9])
		self.assertEqual(self.Controller.total_elements, 9, "correct element total count before set removal")

		self.Controller.delete_set("test_one_more")
		self.assertEqual(self.Controller.total_elements, 7, "correct element total count after set removal")

		self.assertEqual(self.Controller.all_elements, [1, 2, 3, 6, 7, 8, 9], "correct element list after set removal")

	def test_delete_element(self):
		self.Controller.create_set("test_1", [1, 2, 3, 4])
		self.Controller.create_set("test_2", [3, 4, 5, 6, 7])
		self.Controller.create_set("test_3", [5, 6, 7])
		
		self.assertFalse(self.Controller.delete_element(8), "nothing deleted with nonexistant element")

		self.assertTrue(self.Controller.delete_element(3), "deletes given element")

		self.assertEqual(self.Controller.all_elements, [1, 2, 4, 5, 6, 7], "element removed from all elements list")

		self.assertEqual(self.Controller.total_elements, 6, "correct total element count")

		expected_set_1 = VennObj("test_1", [1, 2, 4])
		self.assertEqual(self.Controller.search_set("test_1"), expected_set_1, "element removed from set")

		self.assertTrue(self.Controller.search_set("test_2") in self.Controller.search_set("test_1").overlap, "sets retaining overlap remain paired")

		self.Controller.delete_element(4)
		self.assertFalse(self.Controller.search_set("test_2") in self.Controller.search_set("test_1").overlap, "sets unpaired after removing overlap")

		self.Controller.delete_element(1)
		self.Controller.delete_element(2)
		self.assertIsNone(self.Controller.search_set("test_1"), "set deleted after all elements removed")

		self.assertEqual(self.Controller.all_elements, [5, 6, 7], "element removed from all elements list")

		self.assertEqual(self.Controller.total_elements, 3, "correct total element count")

	def test_update_set(self):
		self.Controller.create_set("test_1", [1, 2, 3, 4])
		self.Controller.create_set("test_2", [3, 4, 5, 6, 7])
		self.Controller.create_set("test_3", [5, 6, 7])

		self.assertTrue(self.Controller.update_set("test_1", "test_new", [1, 2, 3, 4]), "calls update_set successfully")

		self.assertIsNotNone(self.Controller.search_set("test_new"), "returns set with new tag")

		self.assertIsNone(self.Controller.search_set("test_1"), "set with old tag no longer exists")

		self.assertFalse(self.Controller.update_set("bad_test", "test_new", [1]), "can't update nonexistant set")

		self.Controller.update_set("test_new", "test_new", [1, 2])
		expected_set_1 = self.Controller.search_set("test_new")
		expected_set_2 = self.Controller.search_set("test_2")
		self.assertEqual(expected_set_1.contents, [1, 2], "set has updated contents")

		self.assertFalse(expected_set_1 in expected_set_2.overlap, "updated set no longer overlaps with other set")

		self.assertFalse(expected_set_2 in expected_set_1.overlap, "updated set no longer overlaps with other set")

		self.Controller.update_set("test_new", "test_new", [1, 2, 5])
		expected_set_3 = self.Controller.search_set("test_3")
		self.assertTrue(expected_set_1 in expected_set_2.overlap, "updated set now overlaps with other set")

		self.assertTrue(expected_set_1 in expected_set_3.overlap, "updated set now overlaps with other set")

		self.assertTrue(expected_set_3 in expected_set_1.overlap, "updated set now overlaps with other set")


if __name__ == '__main__':
	unittest.main()