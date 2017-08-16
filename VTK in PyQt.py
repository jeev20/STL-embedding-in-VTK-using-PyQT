from __future__ import unicode_literals
from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *
from PyQt4.QtGui import QApplication
from vtk import *
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import sys
from timeit import default_timer as timer


try:
        _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
        def _fromUtf8(s):
                return s
try:
        _encoding = QtGui.QApplication.UnicodeUTF8
        def _translate(context, text, disambig):
                return QtGui.QApplication.translate(context, text, disambig,
_encoding)
except AttributeError:
        def _translate(context, text, disambig):
                return QtGui.QApplication.translate(context, text, disambig)  
# Global variables
s = 0
m = 0
h = 0


########### UI Main window ######################
class Ui_MainWindow(QtGui.QMainWindow):
	def __init__(self):
		super(Ui_MainWindow,self).__init__()
		self.resize(800, 720)
		
		##### Create required canvas for the vtk widget####
		self.centralwidget = QtGui.QWidget(self)
		self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
		self.setCentralWidget(self.centralwidget) 
		
		##### Create a grid layout in PyQT #####
		self.grid = QtGui.QGridLayout(self.centralwidget)
		
		####creates a VTK widget in main window #####
		self.vtkWidget = vtkobjects(self.centralwidget)
		self.vtkWidget.resize(1200,900)
		
		
		##### QT Timer widget #####
		self.timer = QtCore.QTimer(self)
		self.timer.timeout.connect(self.Time)
		
		### Font & Labels ####
		
		self.myFont=QtGui.QFont()
		self.myFont.setBold(True)
		self.myFont.setPointSize(12)
		self.myFont.setWeight(50)
		
		self.mtime = QtGui.QLabel(self.centralwidget)
		self.mtime.setText("Time")
		self.mtime.setFont(self.myFont)
		self.mtime.setAlignment(QtCore.Qt.AlignCenter)
		
		##### LCD widget #####
		self.lcd = QtGui.QLCDNumber(self.centralwidget)
		print self.Time()
		
		
		##### Adding widgets to grid layout #####
		self.grid.addWidget(self.vtkWidget,2, 2, 1, 1)
		self.grid.addWidget(self.mtime,0, 2, 1, 1)
		self.grid.addWidget(self.lcd, 1,2, 1, 1)
		
		
	
	def Time(self):
		global s,m,h
		self.timer.start(1000)
 
		if s < 59:
			s += 1
		else:
			if m < 59:
				s = 0
				m += 1
			elif m == 59 and h < 24:
				h += 1
				m = 0
				s = 0
			else:
				self.timer.stop()
		
		time = "{00}:{01}:{02}".format(h,m,s)
		
		self.lcd.setDigitCount(len(time))
		self.lcd.display(time)
		

class vtkobjects(QVTKRenderWindowInteractor):
	def __init__(self,centralwidget):
		super(vtkobjects,self).__init__(centralwidget)
		self.ren = vtk.vtkRenderer()
		self.move(10,10)
		self.GetRenderWindow().AddRenderer(self.ren)
		self.iren =self.GetRenderWindow().GetInteractor()
		self.ren.SetBackground(.3, .4, .5 )
		self.makecubes()
		self.importstl()
	
	##### How to draw primitive shapes #####
	def makecubes(self):
		self.cube = vtk.vtkCubeSource()
		self.mapper = vtk.vtkPolyDataMapper()
		self.mapper.SetInputConnection(self.cube.GetOutputPort())
			
		self.cubeActor = vtk.vtkActor()
		self.cubeActor.SetMapper(self.mapper)
		self.cubeActor.SetPosition(0, 0, -1)	
		
		r = 1
		g = 1
		b = 0
		self.cubeActor.GetProperty().SetDiffuseColor(r, g, b)
		self.cubeActor.GetProperty().SetOpacity(.20)
		self.cubeActor.GetProperty().SetSpecular(.1)
		
		### Cube rotation ###### 
		self.cubeActortransform = vtk.vtkTransform()
		self.cubeActor.SetUserTransform(self.cubeActortransform)	
		self.cubeActortransform.RotateX(0)
		self.cubeActortransform.RotateY(0)
		self.cubeActortransform.RotateZ(0)
		self.ren.AddActor(self.cubeActor)
		
	
	##### How to Import a STL file #####
	def importstl(self):
		filename2 = "Model.stl"
		
		reader = vtk.vtkSTLReader()
		reader.SetFileName(filename2)
		 
		cm1 = vtk.vtkPolyDataMapper()
		
		if vtk.VTK_MAJOR_VERSION <= 5:
			cm1.SetInput(reader.GetOutput())
			
		else:
			cm1.SetInputConnection(reader.GetOutputPort())
		 
		self.panel = vtk.vtkActor()
		self.panel.SetMapper(cm1)
		self.panel.SetPosition(0, 0, 0)	
		
		self.panel.GetProperty().SetDiffuseColor(1, 1, 0)
		self.panel.GetProperty().SetOpacity(.20)
		self.panel.GetProperty().SetSpecular(.1)
		
		##### STL rotation #####
		self.paneltransform = vtk.vtkTransform()
		self.panel.SetUserTransform(self.paneltransform)
		self.paneltransform.RotateX(0)
		self.paneltransform.RotateY(0)
		self.paneltransform.RotateZ(0)
		
		##### STL scaling #####
		prop = vtk.vtkProp3D
		self.panel.SetScale(1)
		
		##### adding render to STL import ####
		self.ren.AddActor(self.panel)
		
	
if __name__ == "__main__":
 
	app = QApplication(sys.argv)
	window = Ui_MainWindow()
	window.show()
	window.vtkWidget.iren.Initialize()
	sys.exit(app.exec_())		


