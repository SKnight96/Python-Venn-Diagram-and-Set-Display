from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QGridLayout, QLabel, QLineEdit
import re

class VennGUIDeleteElement(QDialog):
	def __init__(self, controller):
		super().__init__()
		self.controller = controller

		self.setWindowTitle("Delete an element from all sets")

		layout = QGridLayout()
		element_name_label = QLabel("Element to be deleted")
		layout.addWidget(element_name_label, 0, 0)
		self.element_name_line = QLineEdit()
		layout.addWidget(self.element_name_line, 0, 1)
		QBtn = (QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
		buttonBox = QDialogButtonBox(QBtn)
		buttonBox.accepted.connect(self.ok_button)
		buttonBox.rejected.connect(self.cancel_button)
		layout.addWidget(buttonBox, 4, 0, 2, 0)
		self.setLayout(layout)

	def ok_button(self):
		element_name = re.search(r"([\w\s]+)", self.element_name_line.text())
		#will need to establish some convention for elements
		#with this current formatting elements should only be a single word
		if element_name:
			element = element_name.group()
			element_deleted = self.controller.delete_element(element)
			if element_deleted == False:
				print("That element is not contained in any sets")
			else:
				self.accept()
		else:
			print("Invalid naming convention")

	def cancel_button(self):
		print("Cancel")
		self.reject()