from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QGridLayout, QLabel, QLineEdit
import re

class VennGUICreateSet(QDialog):
	def __init__(self, controller):
		super().__init__()
		self.controller = controller

		self.setWindowTitle("Add a new set")

		layout = QGridLayout()
		set_name_label = QLabel("Name of the new set")
		layout.addWidget(set_name_label, 0, 0)
		self.set_name_line = QLineEdit()
		layout.addWidget(self.set_name_line, 0, 1)
		set_contents_label = QLabel("The contents of the set, seperated by dashes -")
		layout.addWidget(set_contents_label, 1, 0)
		self.set_contents_line = QLineEdit()
		layout.addWidget(self.set_contents_line, 1, 1)
		QBtn = (QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
		buttonBox = QDialogButtonBox(QBtn)
		buttonBox.accepted.connect(self.ok_button)
		buttonBox.rejected.connect(self.cancel_button)
		layout.addWidget(buttonBox, 4, 0, 2, 0)
		self.setLayout(layout)

	def ok_button(self):
		set_name = re.search(r"(\w+[ \w+]*)", self.set_name_line.text())
		#need to work out how to set this up so that in can match multiple
		#words while deleting invalid preceding or trailing characters
		if set_name:
			tag = set_name.group()
			#print(tag)
			contents = self.set_contents_line.text().split("-")
			#print(contents)
			if contents[0] != '':
				stripped = []
				for i in contents:#remove any preceding or trailing spaces
					element = i.strip()
					if len(element) <= 40:
						stripped.append(element)
					else:
						print("Element '" + str(element) +"' is too long (greater than 40 characters) and was omitted")
				new_set = self.controller.create_set(tag, stripped)
				#new_set = self.controller.create_set(tag, contents)
				if new_set == False:
					print("Error: Set with name already exists")
				else:
					self.accept()
			else:
				print("Error: Contents of set must contain one or more items")
		else:
			print("Invalid naming convention")

	def cancel_button(self):
		print("Cancel")
		self.reject()