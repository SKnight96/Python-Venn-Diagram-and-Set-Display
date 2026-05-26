from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QGridLayout, QLabel, QLineEdit
import re

class VennGUIDeleteSet(QDialog):
	def __init__(self, controller):
		super().__init__()
		self.controller = controller

		self.setWindowTitle("Delete a set")

		layout = QGridLayout()
		set_name_label = QLabel("Name of the set to be deleted")
		layout.addWidget(set_name_label, 0, 0)
		self.set_name_line = QLineEdit()
		layout.addWidget(self.set_name_line, 0, 1)
		QBtn = (QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
		buttonBox = QDialogButtonBox(QBtn)
		buttonBox.accepted.connect(self.ok_button)
		buttonBox.rejected.connect(self.cancel_button)
		layout.addWidget(buttonBox, 4, 0, 2, 0)
		self.setLayout(layout)

	def ok_button(self):
		set_name = re.search(r"(\w+\s*\w*)", self.set_name_line.text())
		#need to work out how to set this up so that in can match multiple
		#words while deleting invalid preceding or trailing characters
		if set_name:
			tag = set_name.group()
			set_deleted = self.controller.delete_set(tag)
			if set_deleted == False:
				print("Error: No set with name exists")
			else:
				self.accept()
		else:
			print("Invalid naming convention")

	def cancel_button(self):
		print("Cancel")
		self.reject()