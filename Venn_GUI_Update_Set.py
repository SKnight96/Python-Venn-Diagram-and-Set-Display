from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QGridLayout, QLabel, QLineEdit
import re

class VennGUIUpdateSet(QDialog):
	def __init__(self, controller):
		super().__init__()
		self.controller = controller

		self.setWindowTitle("Update set contents")

		layout = QGridLayout()
		set_name_label = QLabel("Name of set to be updated")
		layout.addWidget(set_name_label, 0, 0)
		self.set_name_line = QLineEdit()
		layout.addWidget(self.set_name_line, 0, 1)
		new_set_name_label = QLabel("New name of the set")
		layout.addWidget(new_set_name_label, 1, 0)
		self.new_set_name_line = QLineEdit()
		layout.addWidget(self.new_set_name_line, 1, 1)
		elements_add_label = QLabel("Set elements to add, seperated by dashes -")
		layout.addWidget(elements_add_label, 2, 0)
		self.elements_add_line = QLineEdit()
		layout.addWidget(self.elements_add_line, 2, 1)
		elements_remove_label = QLabel("Set elements to remove, seperated by dashes -")
		layout.addWidget(elements_remove_label, 3, 0)
		self.elements_remove_line = QLineEdit()
		layout.addWidget(self.elements_remove_line, 3, 1)
		QBtn = (QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
		buttonBox = QDialogButtonBox(QBtn)
		buttonBox.accepted.connect(self.ok_button)
		buttonBox.rejected.connect(self.cancel_button)
		layout.addWidget(buttonBox, 4, 0, 2, 0)
		self.setLayout(layout)

	def ok_button(self):
		#set_name = re.search(r"(\w+\s*\w*)", self.set_name_line.text())
		set_name = re.search(r"(\w+[ \w+]*)", self.set_name_line.text())
		#new_set_name = re.search(r"(\w+\s*\w*)", self.new_set_name_line.text())
		new_set_name = re.search(r"(\w+[ \w+]*)", self.new_set_name_line.text())
		#need to work out how to set this up so that in can match multiple
		#words while deleting invalid preceding or trailing characters
		if set_name and new_set_name:
			tag = set_name.group()
			new_tag = new_set_name.group()
			to_add = self.elements_add_line.text().split("-")
			to_remove = self.elements_remove_line.text().split("-")
			stripped_to_add = []
			stripped_to_remove = []
			for i in to_add:#remove any preceding or trailing spaces
				#stripped.append(i.strip())
				element = i.strip()
				if len(element) <= 40:
					stripped_to_add.append(element)
				else:
					print("Element '" + str(element) +"' is too long (greater than 40 characters) and was omitted")

				#stripped_to_add.append(i.strip())
			for j in to_remove:
				stripped_to_remove.append(j.strip())
			check_tag = self.controller.search_set(tag)
			if check_tag:
				old_contents = list(check_tag.contents)
				new_contents = []
				for i in old_contents:
					if i not in stripped_to_remove:
						new_contents.append(i)
					#new_contents = [x for x in old_contents if x != i]
				for j in stripped_to_add:
					if j != '':
						print("Adding " + str(j))
						new_contents.append(j)
				print("The modified set will be given the contents: " + str(new_contents))
				self.controller.update_set(tag, new_tag, new_contents)
				self.accept()
			else:
				print("Error: No set with name exists")
		else:
			print("Invalid naming convention")

	def cancel_button(self):
		print("Cancel")
		self.reject()