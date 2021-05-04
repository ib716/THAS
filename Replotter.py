import sys
import numpy as np
from traits.api import Instance
from mayavi import mlab
from mayavi.core.ui.api import MlabSceneModel
from PyQt5 import (QtCore, QtGui, QtWidgets)
from PyQt5.QtCore import QProcess
from PyQt5.QtWidgets import (QWidget, QDesktopWidget, QMessageBox, QApplication)


count = 0
########## Main Setup ###########
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Plotter")
        MainWindow.resize(580, 240) # Initial Window Dimensions
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Icon.ico"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")



        ########## Labels ##########
        self.FrameLabel = QtWidgets.QLabel(self.centralwidget)
        self.FrameLabel.setGeometry(QtCore.QRect(30, 27, 200, 20))
        self.FrameLabel.setObjectName("FrameLabel")
        self.nLabel = QtWidgets.QLabel(self.centralwidget)
        self.nLabel.setGeometry(QtCore.QRect(35, 100, 20, 20))
        self.nLabel.setObjectName("nLabel")
        self.rLabel = QtWidgets.QLabel(self.centralwidget)
        self.rLabel.setGeometry(QtCore.QRect(135, 100, 20, 20))
        self.rLabel.setObjectName("rLabel")
        self.sLabel = QtWidgets.QLabel(self.centralwidget)
        self.sLabel.setGeometry(QtCore.QRect(235, 100, 20, 20))
        self.sLabel.setObjectName("sLabel")



        ########## Text Inputs ##########
        self.FrameInput = QtWidgets.QLineEdit(self.centralwidget)
        self.FrameInput.setGeometry(QtCore.QRect(180, 20, 145, 40))
        self.FrameInput.setObjectName("FrameInput")

        self.nSpinner = QtWidgets.QLineEdit(self.centralwidget)
        self.nSpinner.setGeometry(QtCore.QRect(66, 87, 60, 50))
        self.nSpinner.setObjectName("nSpinner")

        self.rSpinner = QtWidgets.QLineEdit(self.centralwidget)
        self.rSpinner.setGeometry(QtCore.QRect(166, 87, 60, 50))
        self.rSpinner.setObjectName("rSpinner")

        self.sSpinner = QtWidgets.QLineEdit(self.centralwidget)
        self.sSpinner.setGeometry(QtCore.QRect(266, 87, 60, 50))
        self.sSpinner.setObjectName("sSpinner")



        ########## Buttons ##########        
        self.PlotButton = QtWidgets.QPushButton(self.centralwidget)
        self.PlotButton.setGeometry(QtCore.QRect(350, 87, 200, 50))
        self.PlotButton.setObjectName("PlotButton")
        self.PlotButton.setStyleSheet('QPushButton {background-color: #A3C1DA; color: blue;}')
        self.PlotButton.clicked.connect(self.Plot)
        


        ########## Text Outputs ##########
        self.scrollArea = QtWidgets.QScrollArea(MainWindow)
        self.scrollArea.setGeometry(QtCore.QRect(30, 160, 520, 60)) # Location and Dimensions
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        self.OutputText = QtWidgets.QTextEdit(self.scrollArea)
        self.OutputText.setGeometry(QtCore.QRect(0, 0, 520, 60)) # Location and Dimensions
        self.OutputText.setObjectName("OutputText")
        self.OutputText.setFontPointSize(10)



        ########## Setup ###########
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)



    ########## Protocol ##########
    def Plot(self):        
        global n1
        global r1
        global f1
        global s1        
        global count

        count += 1
        f1 = int(self.FrameInput.text()) # Value of f frame to use
        n1 = float(self.nSpinner.text()) # Value of n template to use
        r1 = float(self.rSpinner.text()) # Value of r template to use
        s1 = int(self.sSpinner.text()) # Value of s template to use

        answer = QtWidgets.QMessageBox.question(
            self.centralwidget, 'Replot', 'Are you sure you are ready to execute Replotter from Initilisation Settings?',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)

        if answer == QtWidgets.QMessageBox.Yes:
            global fname1
            fname1 = (f'n={n1}, r={r1}, f={f1}, s={s1}.txt')
            self.OutputText.append(f'Loading files under - {fname1}')

            try:
                Scene = (f'scene{count}')
                self.OutputText.append(f'Scene number - {Scene}')
                Scene = Instance(MlabSceneModel, ())

                CountArray1 = np.loadtxt(f".Data files - Copy/Count Data/{fname1}")
                XArray1 = np.loadtxt(f".Data files - Copy/X Data/{fname1}")
                YArray1 = np.loadtxt(f".Data files - Copy/Y Data/{fname1}")
                ZArray1 = np.loadtxt(f".Data files - Copy/Z Data/{fname1}")

                def draw_scene(scene):
                    mlab.figure(figure=scene.mayavi_scene)
                    pnts1 = mlab.points3d(XArray1, YArray1, ZArray1, CountArray1, colormap="copper", mode='point', figure=scene.mayavi_scene)
                    pnts1.actor.actor.property.render_points_as_spheres = True
                    pnts1.actor.actor.property.point_size = 5.0
                    mlab.title(f'{fname1}')
                    mlab.show()

                draw_scene(Scene)

            except:
                self.OutputText.append('Selected files cannot be found')
                count -= 1

        else:
            pass



    ########## Window Setup ##########
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Replotter       (created by I.T.Booth)"))

        self.FrameLabel.setText(_translate("MainWindow", "Frames Processed"))
        self.nLabel.setText(_translate("MainWindow", "n ="))
        self.rLabel.setText(_translate("MainWindow", "r ="))
        self.sLabel.setText(_translate("MainWindow", "s ="))

        self.PlotButton.setText(_translate("MainWindow", "Plot Interactive 3D"))



########## Execute above protocol ##########
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ag = QDesktopWidget().availableGeometry()
    sg = QDesktopWidget().screenGeometry()
    widget = MainWindow.geometry()
    x = 0.1 * (ag.width() - widget.width())
    y = 0.5 * ag.height() - widget.height()
    MainWindow.move(x, y)
    MainWindow.show()
    sys.exit(app.exec_())