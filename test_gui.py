#!/usr/bin/env python3
from PyQt5.QtWidgets import QInputDialog, QApplication, QMainWindow

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
import sys
from PyQt5.QtGui import QImage, QPixmap,QIcon,QColor
from PyQt5.QtWidgets import QLabel,QWidget
from PyQt5.QtCore import Qt
import numpy as np
import pygame
from PyQt5.QtWidgets import QInputDialog, QDialog
import os
import threading
from math import ceil
import sys
import string
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.colors as mlc
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLineEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import rospy
from std_msgs.msg import String
class MineMapWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas)

        # Custom legends
        clr = [(1, 1, 1), '#0a3563', '#1592ad']
        elment = [
            Patch(facecolor='#1592ad', edgecolor='#1592ad', label='Surface Mine'),
            Patch(facecolor='#0a3563', edgecolor='#0a3563', label='Buried Mine'),
            Line2D([0], [0], marker='o', label='Robot', markersize=10, linewidth=0)
        ]

        # Axis labels
        x_axis = string.ascii_uppercase[:19]
        y_axis = [str(i) for i in range(19, 0, -1)]

        # Initialize mines and map
        self.mine = np.zeros((19, 19))
        self.img = np.zeros((19, 19), dtype=float)

        # Initialize colormap
        cmap = mlc.LinearSegmentedColormap.from_list('ColorMap', clr)
        norm = colors.BoundaryNorm([0, 1, 2, 3], cmap.N)
        self.im = self.ax.imshow(self.img, cmap=cmap, norm=norm)

        # Set up ticks and grid
        self.ax.set_xticks(np.arange(len(x_axis)), labels=x_axis)
        self.ax.set_yticks(np.arange(len(y_axis)), labels=y_axis)
        self.ax.set_xticks(np.arange(len(x_axis))-.5, minor=True)
        self.ax.set_yticks(np.arange(len(y_axis))-.5, minor=True)
        self.ax.grid(which="minor", color="k", linestyle='-', linewidth=0.1)
        self.ax.tick_params(which="minor", bottom=False, left=False)

        # Add legend
        self.ax.legend(handles=elment, loc='upper left', bbox_to_anchor=(1, 1))
        self.ax.set_title("Mines Map Representation")
        self.fig.tight_layout()

        self.marker = None
        self.canvas.draw()

    def update_mine(self, x_mine, y_mine, value):
        # print("mine:", x_mine, y_mine, value)
        x_mine = ord(x_mine) - 65
        y_mine = 19 - int(y_mine)
        
        # Update mine state
        self.mine[y_mine][x_mine] = int(value)

        # Update image data based on mines
        self.img = np.where(self.mine == 0, 0.0, 
           np.where(self.mine == 1, 1.0, 
           np.where(self.mine == 2, 2.0, 0.0)))

        # Update the image without flickering
        self.canvas.setUpdatesEnabled(False)
        self.im.set_data(self.img)
        self.canvas.draw_idle()  # Use draw_idle to optimize redraw
        self.canvas.setUpdatesEnabled(True)

    def update_robot(self, x_robot, y_robot):
        # print("robot:", x_robot, y_robot)
        if self.marker:
            self.marker.remove()
        x_robot = ord(x_robot) - 65
        y_robot = 19 - int(y_robot)
        self.marker = self.ax.plot(x_robot, y_robot, linestyle='None', marker='o', color='#1592ad')[0]

        # Update the robot position without flickering
        self.canvas.setUpdatesEnabled(False)
        self.canvas.draw_idle()  # Use draw_idle to optimize redraw
        self.canvas.setUpdatesEnabled(True)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)     
        palette = QtGui.QPalette()

        # Load the image as a QImage and convert it to RGB
        image = QtGui.QImage("imgs/mono-background.jpg")
        image = image.convertToFormat(QtGui.QImage.Format_RGB888)
        
        # Get the window size
        window_size = 2.2*MainWindow.size()

        # Calculate the scaled image
        scaled_image = image.scaled(window_size, 16, Qt.FastTransformation)

        # Create a QPixmap from the QImage
        background_image = QtGui.QPixmap.fromImage(scaled_image)

        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(background_image))
        MainWindow.setPalette(palette)
        
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.mine_map_widget = MineMapWidget(self.centralwidget)
        self.mine_map_widget.setGeometry(1000, 20, 850, 650)
        self.mine_map_widget.show() 


        # Set the central widget layout
        MainWindow.setCentralWidget(self.centralwidget)
        
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(780, 50, 400, 80))
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")

        
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(40, 700, 400, 100))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(390, 700, 400, 100))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(800, 710, 400, 100))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(1430, 710, 400, 100))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(120, 860, 400, 100))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(120, 900, 400, 100))
        self.label_10.setFont(font)


        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(1030,800, 160, 30))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
    
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")

        
        
        
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(885, 800, 70, 70))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(885, 900, 70, 70))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(750, 900, 70, 70))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(1020, 900, 70, 70))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(40, 800, 70, 70))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(750, 800, 70, 70))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(1550, 810, 70, 70))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setGeometry(QtCore.QRect(1550, 900, 70, 70))
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_9 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_9.setGeometry(QtCore.QRect(1450, 855, 70, 70))
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_10 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_10.setGeometry(QtCore.QRect(1650, 855, 70, 70))
        self.pushButton_10.setObjectName("pushButton_6")
        self.pushButton_11 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_11.setGeometry(QtCore.QRect(40, 900, 70, 70))
        self.pushButton_11.setObjectName("pushButton_6")
        MainWindow.setCentralWidget(self.centralwidget)
        
        # Table 1
        self.tableWidget_1 = QTableWidget(self.centralwidget)
        self.tableWidget_1.setGeometry(QtCore.QRect(50, 100, 202, 452))  # Position and size (x, y, width, height)
        self.tableWidget_1.setRowCount(15)  # Set the number of rows
        self.tableWidget_1.setColumnCount(2)  # Set the number of columns
        self.tableWidget_1.setObjectName("tableWidget_1")
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)  # Set the font size
        self.tableWidget_1.setFont(font)
        self.tableWidget_1.verticalHeader().setVisible(False)  # Hide vertical header if not needed
        self.tableWidget_1.horizontalHeader().setVisible(False)  # Hide vertical header if not needed
        # Create a QLabel for the title
        self.label_title = QtWidgets.QLabel(self.centralwidget)
        self.label_title.setGeometry(QtCore.QRect(40, 40, 225, 25))  # Position (x, y) and size (width, height)
        self.label_title.setText("Buried Mines")  # Set the text of the title
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)  # Align the text to the center

        # Customize the font and appearance of the title

        self.label_title.setFont(font)
        self.label_title.setStyleSheet("font-family: Consolas;color: dark;")  #

        self.tableWidget_1.setStyleSheet("""
            QTableWidget {
                background-color:180 #f0f0f0;  # Table background color
                border: 2px solid #8f8f8f;  # Outer border of the table
            }
        """)

        self.tableWidget_2 = QTableWidget(self.centralwidget)
        self.tableWidget_2.setGeometry(QtCore.QRect(400, 100, 202, 452))  # Position and size (x, y, width, height)
        self.tableWidget_2.setRowCount(15)  # Set the number of rows
        self.tableWidget_2.setColumnCount(2)  # Set the number of columns
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setFont(font)
        self.tableWidget_2.verticalHeader().setVisible(False)  # Hide vertical header if not needed
        self.tableWidget_2.horizontalHeader().setVisible(False)  # Hide vertical header if not needed
        self.tableWidget_2.setStyleSheet("""
            QTableWidget {
                background-color: #f0f0f0;  # Table background color
                border: 2px solid #8f8f8f;  # Outer border of the table
            }
        
        """)
        self.tableWidget_3 = QTableWidget(self.centralwidget)
        self.tableWidget_3.setGeometry(QtCore.QRect(700, 100, 101, 452))  # Position and size (x, y, width, height)
        self.tableWidget_3.setRowCount(15)  # Set the number of rows
        self.tableWidget_3.setColumnCount(1)  # Set the number of columns
        self.tableWidget_3.setObjectName("tableWidget_2")
        self.tableWidget_3.setFont(font)
        self.tableWidget_3.verticalHeader().setVisible(False)  # Hide vertical header if not needed
        self.tableWidget_3.horizontalHeader().setVisible(False)  # Hide vertical header if not needed
        self.tableWidget_3.setStyleSheet("""
            QTableWidget {
                background-color: #f0f0f0;  # Table background color
                border: 2px solid #8f8f8f;  # Outer border of the table
            }
        """)

        # Create QLineEdit instance
        self.text_box = QLineEdit(self.centralwidget)
        self.text_box.setPlaceholderText("1: for  buried, 2: for surface")  # Add a placeholder
        self.text_box.setGeometry(810, 100, 150, 40)  # Position and size

        # Connect a signal to print the text when it changes
        self.text_box.textChanged.connect()

        # Create a QLabel for the title
        self.label_title2 = QtWidgets.QLabel(self.centralwidget)
        self.label_title2.setGeometry(QtCore.QRect(355, 40, 300, 25))  # Position (x, y) and size (width, height)
        self.label_title2.setText("Surface Mines")  # Set the text of the title
        self.label_title2.setAlignment(QtCore.Qt.AlignCenter)  # Align the text to the center

        # Customize the font and appearance of the title
        self.label_title2.setFont(font)
        self.label_title2.setStyleSheet("font-family: Consolas;color: dark;")  

        self.label_title3 = QtWidgets.QLabel(self.centralwidget)
        self.label_title3.setGeometry(QtCore.QRect(130, 600, 400, 25))  # Position (x, y) and size (width, height)
        self.label_title3.setText("Vector Representation")  # Set the text of the title
        self.label_title3.setAlignment(QtCore.Qt.AlignCenter)  # Align the text to the center

        # Customize the font and appearance of the title
        self.label_title3.setFont(font)
        self.label_title3.setStyleSheet("font-family: Consolas;color: dark;")  #


        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.label.setStyleSheet("color: black;font-family: Consolas;")
        # self.label_2.setStyleSheet("color: black;font-weight: bold;font-family: Consolas;")
        self.label_3.setStyleSheet("color: black;font-weight: bold;font-family: Consolas;")
        self.label_4.setStyleSheet("color: black;font-weight: bold;font-family: Consolas;")
        # self.label_5.setStyleSheet("color: black;font-weight: bold;font-family: Consolas;")
        self.label_6.setStyleSheet("color: black;font-weight: bold;font-family: Consolas;")
        self.label_7.setStyleSheet("color: black;font-weight: bold;font-family: Consolas;")
        self.label_8.setStyleSheet("color: black;font-weight: bold;font-family: Consolas;")
        self.label_9.setStyleSheet("color: black;font-weight: bold;font-family: Consolas;")
        self.label_10.setStyleSheet("color: black;font-weight: bold;font-family: Consolas;")

        
        self.pushButton.setIconSize(QtCore.QSize(60, 60))  # Set a larger size for the icon
        self.pushButton.setFlat(True)
        self.pushButton_2.setIconSize(QtCore.QSize(60, 60))  # Set a larger size for the icon
        self.pushButton_2.setFlat(True) 
        self.pushButton_3.setIconSize(QtCore.QSize(60, 60))  # Set a larger size for the icon
        self.pushButton_3.setFlat(True) 
        self.pushButton_4.setIconSize(QtCore.QSize(60, 60))  # Set a larger size for the icon
        self.pushButton_4.setFlat(True)
        self.pushButton_5.setIconSize(QtCore.QSize(60, 60))  # Set a larger size for the icon
        self.pushButton_5.setFlat(True)
        self.pushButton_6.setIconSize(QtCore.QSize(60, 60))  # Set a larger size for the icon
        self.pushButton_6.setFlat(True)
        self.pushButton_7.setIconSize(QtCore.QSize(60, 60))  # Set a larger size for the icon
        self.pushButton_7.setFlat(True)
        self.pushButton_8.setIconSize(QtCore.QSize(60, 60))  # Set a larger size for the icon
        self.pushButton_8.setFlat(True)
        self.pushButton_9.setIconSize(QtCore.QSize(60, 60))  # Set a larger size for the icon
        self.pushButton_9.setFlat(True)
        self.pushButton_10.setIconSize(QtCore.QSize(60, 60))  # Set a larger size for the icon
        self.pushButton_10.setFlat(True)
        self.pushButton_11.setIconSize(QtCore.QSize(60, 60))  # Set a larger size for the icon
        self.pushButton_11.setFlat(True)
        self.pushButton_11.setIcon(QtGui.QIcon('imgs/landmine.png'))

        
        self.pushButton.setIcon(QtGui.QIcon('imgs/up-arrow.png'))  
        self.pushButton_2.setIcon(QtGui.QIcon('imgs/down-arrow.png'))
        self.pushButton_3.setIcon(QtGui.QIcon('imgs/left-arrow.png'))
        self.pushButton_4.setIcon(QtGui.QIcon('imgs/right-arrow.png'))
        self.pushButton_5.setIcon(QtGui.QIcon('imgs/joystick.png'))
        self.pushButton_6.setIcon(QtGui.QIcon('imgs/stop2.png'))
        self.pushButton_7.setIcon(QtGui.QIcon('imgs/up-gripper.png'))
        self.pushButton_8.setIcon(QtGui.QIcon('imgs/down-gripper.png'))
        self.pushButton_9.setIcon(QtGui.QIcon('imgs/hold.png'))
        self.pushButton_10.setIcon(QtGui.QIcon('imgs/release.png'))



        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(1025,850, 160, 22))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Robot Simulator"))
        self.label_3.setText(_translate("MainWindow", "Current Coordinates"))
        self.label_4.setText(_translate("MainWindow", "(0,0)"))
        self.label_6.setText(_translate("MainWindow", "Motion Control"))
        self.label_7.setText(_translate("MainWindow", "Gripper Control"))
        self.label_9.setText(_translate("MainWindow", "Speed: 0"))

class ControllerThread(threading.Thread):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.running = True
        rospy.init_node('motion', anonymous=True)
        self.controller = rospy.Publisher('/controller_states', String, queue_size=20)
    
    def run(self):
        pygame.init()
        pygame.joystick.init()
        controller = pygame.joystick.Joystick(0)
        controller.init()


        # 2 types of controls: axis and button
        axis = {}
        button = {}

        # Assign initial data values
        # Axes are initialized to 0.0
        for i in range(controller.get_numaxes()):
            axis[i] = 0.0
        # Buttons are initialized to False
        for i in range(controller.get_numbuttons()):
            button[i] = False
        for i in range(controller.get_numhats()):
            button[i] = False    

        # Deadzone values for axes
        deadzone = {0: 0.2, 1: 0.2, 2: 0.2, 3: 0.2, 4: 0, 5: 0}

        # Labels for DS4 controller axes
        AXIS_LEFT_STICK_X = 0
        AXIS_LEFT_STICK_Y = 1
        AXIS_RIGHT_STICK_X = 2
        AXIS_RIGHT_STICK_Y = 3
        AXIS_L2 = 4
        AXIS_R2 = 5

        # Labels for DS4 controller buttons
        # Note that there are 16 buttons
        BUTTON_CROSS = 0
        BUTTON_CIRCLE = 1
        BUTTON_SQUARE = 2
        BUTTON_TRIANGLE = 3

        BUTTON_SHARE = 4
        BUTTON_PS = 5
        BUTTON_OPTIONS = 6

        BUTTON_L3 = 7
        BUTTON_R3 = 8

        BUTTON_L1 = 9
        BUTTON_R1 = 10

        BUTTON_UP = 11
        BUTTON_DOWN = 12
        BUTTON_LEFT = 13
        BUTTON_RIGHT = 14

        BUTTON_PAD = 15

        # L2 and R2 are initialized to -1.0
        axis[4] = -1.0
        axis[5] = -1.0

        # Main loop
        while True:
            # Get events
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    axis[event.axis] = round(event.value, 3)
                elif event.type == pygame.JOYBUTTONDOWN:
                    button[event.button] = True
                elif event.type == pygame.JOYBUTTONUP:
                    button[event.button] = False

            # Apply deadzone
            for i in deadzone:
                if abs(axis[i]) < deadzone[i]:
                    axis[i] = 0

            if 0:
                # Print out results
                os.system('cls')
                # Buttons
                print("Square:", button[BUTTON_SQUARE])
                print("Cross:", button[BUTTON_CROSS])
                print("Circle:", button[BUTTON_CIRCLE])
                print("Triangle:", button[BUTTON_TRIANGLE])
                print("Up:", button[BUTTON_UP])
                print("Down:", button[BUTTON_DOWN])
                print("Right:", button[BUTTON_RIGHT])
                print("Left:", button[BUTTON_LEFT])
                print("L1:", button[BUTTON_L1])
                print("R1:", button[BUTTON_R1])
                print("Share:", button[BUTTON_SHARE])
                print("Options:", button[BUTTON_OPTIONS])
                print("L3:", button[BUTTON_L3])
                print("R3:", button[BUTTON_R3])
                print("PS:", button[BUTTON_PS])
                print("Touch Pad:", button[BUTTON_PAD], "\n")
                # Axes
                print("L3 X:", axis[AXIS_LEFT_STICK_X])
                print("L3 Y:", axis[AXIS_LEFT_STICK_Y])
                print("R3 X:", axis[AXIS_RIGHT_STICK_X])
                print("R3 Y:", axis[AXIS_RIGHT_STICK_Y])
                print("L2:", axis[AXIS_L2])
                print("R2:", axis[AXIS_R2])
            
            else:
                # Serializing data to be sent
                data = ""
                for i in axis:
                    data += "#" + str(i) + "@" + str(axis[i])
                for i in range(ceil(len(button) / 8)):
                    data_i = 0
                    for j in range(8):
                        index = i*8 +j
                        if index<len(button):
                            data_i += 2 ** j * button[index]
                    data += "#" + str(i + len(axis)) + "@" + str(data_i)
                data += "\n"

            print(data)
            self.controller.publish(data)


            # Limited to 30 frames per second
            clock = pygame.time.Clock()
            clock.tick(5)


class RobotSimulator(QtWidgets.QMainWindow):
    def __init__(self):

        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_slider()     
        self.controller_thread = ControllerThread(self)
        self.controller_thread.daemon = True

        self.controller_thread.start()
        self.coord_mine1 = []
        self.coord_mine2 = []

        rospy.Subscriber('/robot_location', String, self.robot_location)
        rospy.Subscriber('/mine_location', String, self.mine_location)
        self.state=1


        # Icon to the Window
        app_icon = QIcon("imgs/robot(1).png")  
        self.setWindowIcon(app_icon)
   

###################################################################################################3       
    # def show_input_dialog(self):
    #     # Create a QInputDialog instance
    #     dialog = QInputDialog(self)
    #     dialog.setWindowTitle("Mine State")
    #     dialog.setLabelText("1 for Buried 2 for Surface :")
        
    #     # Set custom position (x, y)
    #     dialog.move(800, 500)  # Adjust these coordinates as needed
        
    #     # Execute the dialog
    #     if dialog.exec_() == QDialog.Accepted:
    #         self.state = dialog.textValue()  # Use an integer
    #     else:
    #         self.state = "0"
    def robot_location(self,msg):
        #print(msg)

        x=(msg.data.split(','))[0]
        y=(msg.data.split(','))[1]
        self.ui.mine_map_widget.update_robot(x, y)
        self.ui.label_4.setText(f"({str(x)},{str(y)})")
    
    def mine_location(self,msg):
        flag = 0
        flag2 = 0
        x=(msg.data.split(','))[0]
        y=(msg.data.split(','))[1]
        
        if [x,y] in self.coord_mine1:
            flag = 1
            
        if [x,y] in self.coord_mine2:
            flag2 = 1
        
        if ((flag != 1) and (flag2 != 1 )):
            print("new mine")       
            # self.show_input_dialog()
            self.ui.label_10.setText(str(self.state))
            self.ui.mine_map_widget.update_mine(x, y,self.state)

            if self.state == "1":
                self.coord_mine1.append([x,y])
                self.populateTable1(self.coord_mine1)
            elif self.state == "2": 
                self.coord_mine2.append([x,y])
                self.populateTable2(self.coord_mine2)
        else:
            print("already detected")


    def populateTable1(self,coordinates):
        for row in range(len(coordinates)):
            for col in range(1):
                item = QTableWidgetItem(f"{coordinates[row][0]}")
                item_2 = QTableWidgetItem(f"{coordinates[row][1]}")
                self.ui.tableWidget_1.setItem(row, col, item)
                self.ui.tableWidget_1.setItem(row, col+1, item_2)
                item.setTextAlignment(QtCore.Qt.AlignCenter)  # Center align text
                item_2.setTextAlignment(QtCore.Qt.AlignCenter)  # Center align text
    
    def populateTable2(self,coordinates):
        for row in range(len(coordinates)):
            for col in range(1):
                item = QTableWidgetItem(f"{coordinates[row][0]}")
                item_2 = QTableWidgetItem(f"{coordinates[row][1]}")
                self.ui.tableWidget_2.setItem(row, col, item)
                self.ui.tableWidget_2.setItem(row, col+1, item_2)
                item.setTextAlignment(QtCore.Qt.AlignCenter)  # Center align text
                item_2.setTextAlignment(QtCore.Qt.AlignCenter)  # Center align text


    def setup_slider(self):
        self.ui.horizontalSlider.setMinimum(0)
        self.ui.horizontalSlider.setMaximum(255)
        self.ui.horizontalSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.ui.horizontalSlider.setTickInterval(10)
        self.ui.horizontalSlider.valueChanged.connect(self.update_slider_value)

    def update_slider_value(self, value):
        self.ui.label_9.setText(f"Speed: {value}")    




        
if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = RobotSimulator()
    MainWindow.show()
    MainWindow.showMaximized()
    sys.exit(app.exec_())
