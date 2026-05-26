import sys
from Venn_Controller import VennController
from Venn_GUI_Load_Sets import VennGUILoadSets
from Venn_GUI_Save_Sets import VennGUISaveSets
from Venn_GUI_Create_Set import VennGUICreateSet
from Venn_GUI_Delete_Set import VennGUIDeleteSet
from Venn_GUI_Update_Set import VennGUIUpdateSet
from Venn_GUI_Delete_Element import VennGUIDeleteElement
import triangle_third_point
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, \
 QLineEdit, QPushButton, QGridLayout, QHBoxLayout, QStackedLayout, QGraphicsScene, \
 QGraphicsView, QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsSimpleTextItem, \
 QDialog, QDialogButtonBox, QVBoxLayout, QScrollArea
from PyQt6.QtGui import QBrush, QPen, QColor, QMouseEvent

#this is the primary file from which the project gui will run
#executed with the line [ python -m Venn_GUI_Main ] from within the project directory

class VennGUIMain(QMainWindow):
	def __init__(self):
		super().__init__()
		self.controller = VennController()

		self.button_1_checked = False
		self.button_2_checked = False
		self.button_3_checked = False
		self.ellipses = [[None, ""], [None, ""], [None, ""]]

		self.mouse_x = 0
		self.mouse_y = 0
		self.setMouseTracking(True)

		self.layout = QGridLayout()

		self.label_num_sets = QLabel("try creating a few sets!")
		self.load_button = QPushButton("Load Diagram")
		self.load_button.clicked.connect(self.load_button_clicked)
		self.save_button = QPushButton("Save Diagram")
		self.save_button.clicked.connect(self.save_button_clicked)
		self.create_set_button = QPushButton("Add New Set")
		self.create_set_button.clicked.connect(self.create_set_button_clicked)
		self.delete_set_button = QPushButton("Remove Set")
		self.delete_set_button.clicked.connect(self.delete_set_button_clicked)
		self.update_set_button = QPushButton("Modify Set")
		self.update_set_button.clicked.connect(self.update_set_button_clicked)
		self.delete_element_button = QPushButton("Remove Element")
		self.delete_element_button.clicked.connect(self.delete_element_button_clicked)
		self.layout.addWidget(self.label_num_sets, 0, 0)
		self.layout.addWidget(self.load_button, 0, 1)
		self.layout.addWidget(self.save_button, 0, 2)
		self.layout.addWidget(self.create_set_button, 0, 3)
		self.layout.addWidget(self.delete_set_button, 0, 4)
		self.layout.addWidget(self.update_set_button, 0, 5)
		self.layout.addWidget(self.delete_element_button, 0, 6)

		self.set_display = QScrollArea()
		self.set_display.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
		self.set_display.setWidgetResizable(True)

		self.layout.addWidget(self.set_display, 1, 0)

		scene = QGraphicsScene(0, 1, 800, 550)

		rect = QGraphicsRectItem(0, 0, 790, 550)
		rect.setPos(0, 0)
		brush = QBrush(Qt.GlobalColor.white)
		rect.setBrush(brush)
		pen = QPen(Qt.GlobalColor.black)
		pen.setWidth(10)
		rect.setPen(pen)
		scene.addItem(rect)

		view = QGraphicsView(scene)
		view.setMouseTracking(True)
		self.layout.addWidget(view, 1, 1, 5, 6)

		#TESTING MOUSE TRACKER
		'''self.mouse_tracker = QLabel("mouse X: \nmouse Y: ")
		self.layout.addWidget(self.mouse_tracker, 2, 0)'''
		#TESTING MOUSE TRACKER


		self.scroll_intersect_1 = QScrollArea()
		self.scroll_intersect_1.setWidgetResizable(True)
		scroll_widget_1 = QWidget()
		vintersect_1 = QVBoxLayout()
		self.intersect_1 = QLabel("")
		vintersect_1.addWidget(self.intersect_1)
		scroll_widget_1.setLayout(vintersect_1)
		self.scroll_intersect_1.setWidget(scroll_widget_1)
		self.layout.addWidget(self.scroll_intersect_1, 6, 1)

		self.scroll_intersect_2 = QScrollArea()
		self.scroll_intersect_2.setWidgetResizable(True)
		scroll_widget_2 = QWidget()
		vintersect_2 = QVBoxLayout()
		self.intersect_2 = QLabel("")
		vintersect_2.addWidget(self.intersect_2)
		scroll_widget_2.setLayout(vintersect_2)
		self.scroll_intersect_2.setWidget(scroll_widget_2)
		self.layout.addWidget(self.scroll_intersect_2, 6, 2)

		self.scroll_intersect_3 = QScrollArea()
		self.scroll_intersect_3.setWidgetResizable(True)
		scroll_widget_3 = QWidget()
		vintersect_3 = QVBoxLayout()
		self.intersect_3 = QLabel("")
		vintersect_3.addWidget(self.intersect_3)
		scroll_widget_3.setLayout(vintersect_3)
		self.scroll_intersect_3.setWidget(scroll_widget_3)
		self.layout.addWidget(self.scroll_intersect_3, 6, 3)

		self.scroll_intersect_4 = QScrollArea()
		self.scroll_intersect_4.setWidgetResizable(True)
		scroll_widget_4 = QWidget()
		vintersect_4 = QVBoxLayout()
		self.intersect_4 = QLabel("")
		vintersect_4.addWidget(self.intersect_4)
		scroll_widget_4.setLayout(vintersect_4)
		self.scroll_intersect_4.setWidget(scroll_widget_4)
		self.layout.addWidget(self.scroll_intersect_4, 6, 4)

		'''self.intersect_1 = QLabel("intersection 1")
		self.layout.addWidget(self.intersect_1, 6, 1)
		self.intersect_2 = QLabel("intersection 2")
		self.layout.addWidget(self.intersect_2, 6, 2)
		self.intersect_3 = QLabel("intersection 3")
		self.layout.addWidget(self.intersect_3, 6, 3)
		self.intersect_4 = QLabel("intersection 4")
		self.layout.addWidget(self.intersect_4, 6, 4)'''

		widget = QWidget()
		widget.setMouseTracking(True)
		widget.setLayout(self.layout)
		self.setCentralWidget(widget)
		self.setWindowTitle("Venn Diagram Builder Tool")
		self.setMinimumSize(1120, 630)

	def load_button_clicked(self):
		dlg = VennGUILoadSets(self.controller)
		dlg.exec()
		#diagram draw function call here
		self.update_set_count()
		self.display_set_options()

	def save_button_clicked(self):
		dlg = VennGUISaveSets(self.controller)
		dlg.exec()

	def create_set_button_clicked(self):
		dlg = VennGUICreateSet(self.controller)
		dlg.exec()
		#diagram draw function call here
		self.update_set_count()
		self.display_set_options()

	def delete_set_button_clicked(self):
		dlg = VennGUIDeleteSet(self.controller)
		dlg.exec()
		#diagram draw function call here
		self.update_set_count()
		self.display_set_options()
		self.draw_diagram()#draw venn diagram corrosponding to checked sets

	def update_set_button_clicked(self):
		dlg = VennGUIUpdateSet(self.controller)
		dlg.exec()
		#diagram draw function call here
		self.update_set_count()
		self.display_set_options()
		self.draw_diagram()#draw venn diagram corrosponding to checked sets

	def delete_element_button_clicked(self):
		dlg = VennGUIDeleteElement(self.controller)
		dlg.exec()
		#diagram draw function call here
		self.update_set_count()
		self.display_set_options()
		self.draw_diagram()#draw venn diagram corrosponding to checked sets

	def update_set_count(self):
		self.label_num_sets.setText("There are " + str(self.controller.num_sets) \
		 + " sets in total at an average size of " + str(round(self.controller.set_size_avrg, 2)) \
		 + "\nand containing " + str(self.controller.total_elements) + " unique elements")

	def display_set_options(self):
		scroll_widget = QWidget()
		vbox = QVBoxLayout()

		'''grid_y = 0'''

		for i in self.controller.sets:
			#print(i)
			button = QPushButton(i.tag, self)
			button.desig_set = i# button tied to a designated set
			button.diagram = 0;# circle to button association
			button.setCheckable(True)
			button.clicked.connect(self.button_toggled)
			vbox.addWidget(button)
			elements = ""
			char_count = 0
			for j in i.contents:
				char_count += len(str(j)) + 3
				#note that we're gonna have a problem if any given element has more than 55 characters
				if char_count <= 44:
					elements += str(j)
					elements += " | "
				else:
					elements += "\n"
					elements += str(j)
					elements += " | "
					char_count = len(str(j)) + 3

			'''for j, value in enumerate(i.contents):
				elements += value
				char_count += len(str(j))
				if char_count >= 45 and (j + 1) != len(i.contents):
					elements += "\n"
					char_count = len(str(j))
				elif (j + 1) != len(i.contents):
					elements += ", "
			'''
			set_label = QLabel(str(elements))

			#set_label = QLabel(str(i.contents))#super basic set contents display
			vbox.addWidget(set_label)

			'''grid = QGridLayout()
			grid.addWidget(button, 0, 0)
			grid.addWidget(set_label, 1, 0)
			vbox.addLayout(grid, grid_y)
			grid_y += 1'''

		vbox.addStretch()
		scroll_widget.setLayout(vbox)
		self.set_display.setWidget(scroll_widget)
		self.button_1_checked = False
		self.button_2_checked = False
		self.button_3_checked = False
		self.ellipses[0][0] = None
		self.ellipses[0][1] = ""
		self.ellipses[1][0] = None
		self.ellipses[1][1] = ""
		self.ellipses[2][0] = None
		self.ellipses[2][1] = ""

	def button_toggled(self, checked):
		# note that will have to reset a lot of these variables when a new save is loaded
		if self.button_1_checked == False and checked == True:
			self.button_1_checked = checked
			self.ellipses[0][0] = self.sender().desig_set
			self.ellipses[0][1] = "red"
			#self.ellipse_1_info = self.sender().desig_set
			self.sender().diagram = 1#keep track of how each button ties to the diagram
			self.sender().setStyleSheet("""QPushButton:checked {
				background-color: red;
				border-style: outset;
				border-width: 2px;
				border-radius: 2px;
				border-color: black;
				min-width: 2em;
				padding: 2px;
				}""")
			print("button_1_check = " + str(checked))
			#print(self.sender().diagram)
		elif self.button_2_checked == False and checked == True:
			self.button_2_checked = checked
			self.ellipses[1][0] = self.sender().desig_set
			self.ellipses[1][1] = "blue"
			#self.ellipse_2_info = self.sender().desig_set
			self.sender().diagram = 2# dont think this actually does anything yet
			self.sender().setStyleSheet("""QPushButton:checked {
				background-color: blue;
				border-style: outset;
				border-width: 2px;
				border-radius: 2px;
				border-color: black;
				min-width: 2em;
				padding: 2px;
				}""")
			print("button_2_check = " + str(checked))
			#print(self.sender().diagram)
		elif self.button_3_checked == False and checked == True:
			self.button_3_checked = checked
			self.ellipses[2][0] = self.sender().desig_set
			self.ellipses[2][1] = "lime"
			#self.ellipse_3_info = self.sender().desig_set
			self.sender().diagram = 3
			self.sender().setStyleSheet("""QPushButton:checked {
				background-color: lime;
				border-style: outset;
				border-width: 2px;
				border-radius: 2px;
				border-color: black;
				min-width: 2em;
				padding: 2px;
				}""")
			print("button_3_check = " + str(checked))
			#print(self.sender().diagram)

		if checked == False:
			if self.sender().diagram == 1:
				self.button_1_checked = False
				self.ellipses[0][0] = None
				self.ellipses[0][1] = ""
				#self.ellipse_1_info = None
				self.sender().diagram = 0
			elif self.sender().diagram == 2:
				self.button_2_checked = False
				self.ellipses[1][0] = None
				self.ellipses[1][1] = ""
				#self.ellipse_2_info = None
				self.sender().diagram = 0
			elif self.sender().diagram == 3:
				self.button_3_checked = False
				self.ellipses[2][0] = None
				self.ellipses[2][1] = ""
				#self.ellipse_3_info = None
				self.sender().diagram = 0

		if self.button_1_checked and self.button_2_checked and self.button_3_checked:
			for i in self.set_display.findChildren(QPushButton):
				if not i.isChecked():#disable checking the unused buttons
					i.setCheckable(False)
		else:
			for i in self.set_display.findChildren(QPushButton):
				if not i.isChecked():#reenable checking the unused buttons
					i.setCheckable(True)

		#list intersections
		if self.button_1_checked and self.button_2_checked:
			set_1 = self.ellipses[0][0].tag
			set_2 = self.ellipses[1][0].tag
			intersection = list(set(self.ellipses[0][0].contents).intersection(self.ellipses[1][0].contents))
			self.intersect_1.setText(set_1 + " ∩ " + set_2 + "\n" + str(intersection))
		else:
			self.intersect_1.setText("")
		if self.button_1_checked and self.button_3_checked:
			set_1 = self.ellipses[0][0].tag
			set_3 = self.ellipses[2][0].tag
			intersection = list(set(self.ellipses[0][0].contents).intersection(self.ellipses[2][0].contents))
			self.intersect_2.setText(set_1 + " ∩ " + set_3 + "\n" + str(intersection))
		else:
			self.intersect_2.setText("")
		if self.button_2_checked and self.button_3_checked:
			set_2 = self.ellipses[1][0].tag
			set_3 = self.ellipses[2][0].tag
			intersection = list(set(self.ellipses[1][0].contents).intersection(self.ellipses[2][0].contents))
			self.intersect_3.setText(set_2 + " ∩ " + set_3 + "\n" + str(intersection))
		else:
			self.intersect_3.setText("")
		if self.button_1_checked and self.button_2_checked and self.button_3_checked:
			set_1 = self.ellipses[0][0].tag
			set_2 = self.ellipses[1][0].tag
			set_3 = self.ellipses[2][0].tag
			intersection = list(set(self.ellipses[0][0].contents).intersection(self.ellipses[1][0].contents, self.ellipses[2][0].contents))
			self.intersect_4.setText("∩ all\n" + str(intersection))
		else:
			self.intersect_4.setText("")


		self.draw_diagram()#draw venn diagram corrosponding to checked sets

	'''def mouseMoveEvent(self, mouse):
		#self.mouse_x = mouse.position().x()
		#self.mouse_y = mouse.position().y()
		#self.mouse_tracker.setText("Mouse X: " + str(self.mouse_x) + "\nMouse Y: "\
		#	+ str(self.mouse_y))
		mouse_pos = mouse.position().toPoint()
		self.mouse_tracker.setText(f"Mouse at: {mouse_pos.x()}, {mouse_pos.y()}")
		#print("mouse movement detected")
		#this is only being triggered when we mouse of the window bottom or right edge
		#probably need to subclass the scene and override its mouseMoveEvent

		#think toss this all. being too difficult. just display intersections at bottom of scene'''


	def draw_diagram(self):
		scene = QGraphicsScene(0, 1, 800, 550)
		#rectangle center: x = 395, y = 275
		#only one circle: drawn at 395, 275
		#two circles: c1 at 263, 275. c2 at 527, 275
		#three circles: c1 at 263, 367. c2 at 527, 367. c3 at 395, 183
		rect = QGraphicsRectItem(0, 0, 790, 550)
		rect.setPos(0, 0)
		brush = QBrush(Qt.GlobalColor.white)
		rect.setBrush(brush)
		pen = QPen(Qt.GlobalColor.black)
		pen.setWidth(10)
		rect.setPen(pen)
		scene.addItem(rect)

		base_size = 200

		ellipses_to_draw = 0
		tab = 1
		ellipse_1_tag = ""
		ellipse_2_tag = ""
		ellipse_3_tag = ""
		for i in self.ellipses:
			if i[0]:
				ellipses_to_draw += 1
				if tab == 1:
					ellipse_1_tag = i[0].tag
					set_size = len(i[0].contents)
					relative_size = set_size / self.controller.set_size_avrg
					ellipse_size_1 = base_size * relative_size
					ellipse_center = (ellipse_size_1 / 2) * -1
					#weird hack, but the next line sets where the ellipse is drawn in the scene
					ellipse_1 = QGraphicsEllipseItem(263, 167, ellipse_size_1, ellipse_size_1)
					ellipse_1.setPen(QPen(QColor(i[1])))
					#and the next line sets the position of the ellipse center
					ellipse_1.setPos(ellipse_center, ellipse_center)
					scene.addItem(ellipse_1)
					set_tag_1 = QGraphicsSimpleTextItem(ellipse_1_tag)
					set_tag_1.setPos(263, 167)
					scene.addItem(set_tag_1)
					tab = 2
				elif tab == 2:
					ellipse_2_tag = i[0].tag
					set_size = len(i[0].contents)
					relative_size = set_size / self.controller.set_size_avrg
					ellipse_size_2 = base_size * relative_size
					ellipse_center = (ellipse_size_2 / 2) * -1
					#the number of items in the first two circle's intersection
					size_intersect = len(self.controller.retrieve_intersect(ellipse_1_tag, ellipse_2_tag))
					#the percentage of those circles contents which the intersect represents
					size_intersect_percentile = size_intersect / len(i[0].contents)
					#radius of each circle
					ellipse_radii_1 = ellipse_size_1 / 2
					ellipse_radii_2 = ellipse_size_2 / 2
					#the measurement in units of the line across the widest point in the circle overlap
					overlap = size_intersect_percentile * ellipse_size_2
					#the distance to which the circles need to be drawn from each other to
					#accurately represent their overlap to scale
					distance = overlap + (ellipse_radii_1 - overlap) + (ellipse_radii_2 - overlap)
					ellipse_2 = QGraphicsEllipseItem(263 + distance, 167, ellipse_size_2, ellipse_size_2)
					ellipse_2.setPen(QPen(QColor(i[1])))
					ellipse_2.setPos(ellipse_center, ellipse_center)
					scene.addItem(ellipse_2)
					set_tag_2 = QGraphicsSimpleTextItem(ellipse_2_tag)
					set_tag_2.setPos(263 + distance, 167)
					scene.addItem(set_tag_2)
					tab = 3
				elif tab == 3:
					ellipse_3_tag = i[0].tag
					set_size = len(i[0].contents)
					relative_size = set_size / self.controller.set_size_avrg
					ellipse_size_3 = base_size * relative_size
					ellipse_center = (ellipse_size_3 / 2) * -1
					ellipse_radii_3 = ellipse_size_3 / 2
					#intersection of ellipses 1 and 3
					size_intersect = len(self.controller.retrieve_intersect(ellipse_1_tag, ellipse_3_tag))
					size_intersect_percentile = size_intersect / len(i[0].contents)
					#overlap and distance of ellipses 1 and 3
					overlap_13 = size_intersect_percentile * ellipse_size_3
					distance_13 = overlap_13 + (ellipse_radii_1 - overlap_13) + (ellipse_radii_3 - overlap_13)

					#intersection of ellipses 2 and 3
					size_intersect = len(self.controller.retrieve_intersect(ellipse_2_tag, ellipse_3_tag))
					size_intersect_percentile = size_intersect / len(i[0].contents)
					#overlap and distance of ellipses 2 and 3
					overlap_23 = size_intersect_percentile * ellipse_size_3
					distance_23 = overlap_23 + (ellipse_radii_2 - overlap_23) + (ellipse_radii_3 - overlap_23)

					#use the distances to get coordinates placement of ellipse 3
					third_point = triangle_third_point.get_third_point(263, 263 + distance, 167, distance_13, distance_23)
					ellipse_3 = QGraphicsEllipseItem(third_point[0], third_point[1], ellipse_size_3, ellipse_size_3)
					ellipse_3.setPen(QPen(QColor(i[1])))
					ellipse_3.setPos(ellipse_center, ellipse_center)
					scene.addItem(ellipse_3)
					set_tag_3 = QGraphicsSimpleTextItem(ellipse_3_tag)
					set_tag_3.setPos(third_point[0], third_point[1])
					scene.addItem(set_tag_3)		

		view = QGraphicsView(scene)
		#get and delete the old display
		to_remove = self.layout.itemAtPosition(1, 1)
		self.layout.removeWidget(to_remove.widget())
		#display the new diagram
		self.layout.addWidget(view, 1, 1, 5, 6)


def main():
	app = QApplication(sys.argv)
	window = VennGUIMain()
	window.show()
	app.exec()

if __name__ == '__main__':
	main()

#BUG LIST HERE:

#tests need to be done regarding what variables to reset when loading files
#or other options