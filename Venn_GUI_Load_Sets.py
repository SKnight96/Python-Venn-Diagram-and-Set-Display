from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QGridLayout, QLabel, QLineEdit
import re

class VennGUILoadSets(QDialog):
	def __init__(self, controller):
		super().__init__()
		self.controller = controller

		self.setWindowTitle("Load sets from...")

		layout = QGridLayout()
		save_name_label = QLabel("Name of file to load from")
		layout.addWidget(save_name_label, 0, 0)
		self.save_name_line = QLineEdit()
		layout.addWidget(self.save_name_line, 0, 1)
		QBtn = (QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
		buttonBox = QDialogButtonBox(QBtn)
		buttonBox.accepted.connect(self.ok_button)
		buttonBox.rejected.connect(self.cancel_button)
		layout.addWidget(buttonBox, 4, 0, 2, 0)
		self.setLayout(layout)

	def ok_button(self):
		file_name = re.search(r"(\w+\s*\w*)(\.json)?$", self.save_name_line.text())
		#need to work out how to set this up so that in can match multiple
		#words while deleting invalid preceding or trailing characters
		if file_name:
			load_from = file_name.group(1)
			file_loaded = self.controller.load_sets("records/" + load_from + ".json")
			if file_loaded == False:
				print("File not found")
			else:
				self.accept()
		else:
			print("Invalid naming convention")

	def cancel_button(self):
		print("Cancel")
		self.reject()