#                                                                                    #
#                                                                                    #
#                                Created by I.T.Booth                                #
# ---------------------------------------------------------------------------------- #
#                                                                                    #
#                          The Hologram Analysis System 3                            #
# ---------------------------------------------------------------------------------- #
#                                     (THAS3)                                        #
#                                                                                    #
# Attempts to match video frames against an extensive library of synthetic templates #
# Specific properties about the templates and the frames themselves can be chosen    #
# Once chosen, the program performs several operations producing plots of interest   #
# Displaying and saving the created DATA for later analysis by user if necessary     #
#                                                                                    #
#                                                                                    #



########## Program Import Requirements ###########
import sys
import time
from PyQt5 import (QtCore, QtGui, QtWidgets)
from PyQt5.QtCore import QProcess
from PyQt5.QtWidgets import (QWidget, QMessageBox, QLabel, QHBoxLayout, QApplication)
import numpy as np
from numpy import arange
import PIL
from PIL import Image, ImageEnhance, ImageFilter
import matplotlib
from matplotlib.patches import Rectangle
from matplotlib import pyplot
import matplotlib.pylab as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas 
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from math import sqrt,exp
import cv2
from mpl_toolkits.mplot3d import Axes3D
import array as arr
import keyboard
from pandas import read_csv
from scipy.optimize import curve_fit
from mayavi import mlab
from mayavi.modules.glyph import Glyph
matplotlib.use('QT5Agg')



########## Autorun callable settings ##########
background = "Back1" # Background image file name
video = "Vid1" # Video file name
videoframes = 10000 # Number of frames in video
count = 1 ## NON ALTERABLE ##
end = 11 # Number of frames to process (10) +1
nth_frame = 1000 # Taking frames every nth step (x/(end-1)) where x=total frames
contrast = 70 # Enhancing frame contrast
sharpness = 70 # Enhancing frame sharpness
brightness = 250 # Sets pixel array multiplier
tempcount = 1 # Starting template
tempend = 201 # Ending template
tempsteps = 5 # Taking templates every nth step
n = 1.0 # Synthetic template refractive index
r = 1.0 # Synthetic template radius of sphere
Location = ("n={}, r={}" .format(n, r)) ## NON ALTERABLE ##
threshold = 0.07 # Threshold value for template matching
MinMSE = 0 # Sets minimum MSE value acceptable
MaxMSE = 0 # Sets maximum MSE value acceptable

PlotX = [] ## NON ALTERABLE ##
PlotY = [] ## NON ALTERABLE ##
PlotZ = [] ## NON ALTERABLE ##
PlotTH = [] ## NON ALTERABLE ##
PlotMSE = [] ## NON ALTERABLE ##
PlotCOUNT = [] ## NON ALTERABLE ##




########## Main Setup ###########
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("ANALYSER")
        MainWindow.resize(1900, 950) # Initial Window Dimensions
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Icon.ico"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")



        ########## Labels ##########
        self.BackgroundLabel = QtWidgets.QLabel(self.centralwidget)
        self.BackgroundLabel.setGeometry(QtCore.QRect(80, 27, 100, 20))
        self.BackgroundLabel.setObjectName("BackgroundLabel")
        self.VideoLabel = QtWidgets.QLabel(self.centralwidget)
        self.VideoLabel.setGeometry(QtCore.QRect(100, 87, 100, 20))
        self.VideoLabel.setObjectName("VideoLabel")
        self.nLabel = QtWidgets.QLabel(self.centralwidget)
        self.nLabel.setGeometry(QtCore.QRect(65, 160, 20, 20))
        self.nLabel.setObjectName("nLabel")
        self.rLabel = QtWidgets.QLabel(self.centralwidget)
        self.rLabel.setGeometry(QtCore.QRect(250, 160, 20, 20))
        self.rLabel.setObjectName("rLabel")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 660, 100, 20))
        self.label_3.setObjectName("Min MSE")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(170, 660, 100, 20))
        self.label_4.setObjectName("Max MSE")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(325, 660, 100, 20))
        self.label_5.setObjectName("Threshold")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(460, 660, 120, 20))
        self.label_6.setObjectName("Template Steps")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(620, 660, 120, 20))
        self.label_7.setObjectName("Frame Steps")



        ########## Loading Bar ##########
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(25, 780, 670, 60))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")



        ########## LCDs ##########
        self.MinMSElcd = QtWidgets.QLCDNumber(self.centralwidget)
        self.MinMSElcd.setGeometry(QtCore.QRect(25, 700, 70, 40))
        self.MinMSElcd.display(0)
        self.MinMSElcd.setObjectName("MinMSElcd")
        self.MaxMSElcd = QtWidgets.QLCDNumber(self.centralwidget)
        self.MaxMSElcd.setGeometry(QtCore.QRect(175, 700, 70, 40))
        self.MaxMSElcd.display(0)
        self.MaxMSElcd.setObjectName("MaxMSElcd")
        self.Thlcd = QtWidgets.QLCDNumber(self.centralwidget)
        self.Thlcd.setGeometry(QtCore.QRect(325, 700, 70, 40))
        self.Thlcd.display(0)
        self.Thlcd.setObjectName("Thlcd")
        self.Templcd = QtWidgets.QLCDNumber(self.centralwidget)
        self.Templcd.setGeometry(QtCore.QRect(475, 700, 70, 40))
        self.Templcd.display(0)
        self.Templcd.setObjectName("Templcd")
        self.Framelcd = QtWidgets.QLCDNumber(self.centralwidget)
        self.Framelcd.setGeometry(QtCore.QRect(625, 700, 70, 40))
        self.Framelcd.display(0)
        self.Framelcd.setObjectName("Framelcd")



        ########## Sliders ##########
        self.MinMSESlider = QtWidgets.QSlider(self.centralwidget)
        self.MinMSESlider.setGeometry(QtCore.QRect(30, 250, 60, 400))
        self.MinMSESlider.setMinimum(0)
        self.MinMSESlider.setMaximum(150)
        self.MinMSESlider.setPageStep(1)
        self.MinMSESlider.setOrientation(QtCore.Qt.Vertical)
        self.MinMSESlider.setObjectName("MinMSESlider")
        self.MinMSESlider.valueChanged.connect(self.MinMSElcdUpdate)
        self.MaxMSESlider = QtWidgets.QSlider(self.centralwidget)
        self.MaxMSESlider.setGeometry(QtCore.QRect(180, 250, 60, 400))
        self.MaxMSESlider.setMinimum(0)
        self.MaxMSESlider.setMaximum(150)
        self.MaxMSESlider.setPageStep(1)
        self.MaxMSESlider.setOrientation(QtCore.Qt.Vertical)
        self.MaxMSESlider.setObjectName("MaxMSESlider")
        self.MaxMSESlider.valueChanged.connect(self.MaxMSElcdUpdate)
        self.ThSlider = QtWidgets.QSlider(self.centralwidget)
        self.ThSlider.setGeometry(QtCore.QRect(330, 250, 60, 400))
        self.ThSlider.setMinimum(0)
        self.ThSlider.setMaximum(30)
        self.ThSlider.setPageStep(1)
        self.ThSlider.setOrientation(QtCore.Qt.Vertical)
        self.ThSlider.setObjectName("ThSlider")
        self.ThSlider.valueChanged.connect(self.ThlcdUpdate)
        self.TempSlider = QtWidgets.QSlider(self.centralwidget)
        self.TempSlider.setGeometry(QtCore.QRect(480, 250, 60, 400))
        self.TempSlider.setMinimum(0)
        self.TempSlider.setMaximum(5)
        self.TempSlider.setPageStep(1)
        self.TempSlider.setOrientation(QtCore.Qt.Vertical)
        self.TempSlider.setObjectName("TempSlider")
        self.TempSlider.valueChanged.connect(self.TemplcdUpdate)
        self.FrameSlider = QtWidgets.QSlider(self.centralwidget)
        self.FrameSlider.setGeometry(QtCore.QRect(630, 250, 60, 400))
        self.FrameSlider.setMinimum(0)
        self.FrameSlider.setMaximum(200)
        self.FrameSlider.setPageStep(1)
        self.FrameSlider.setOrientation(QtCore.Qt.Vertical)
        self.FrameSlider.setObjectName("FrameSlider")
        self.FrameSlider.valueChanged.connect(self.FramelcdUpdate)



        ########## Spinners ##########
        self.nSpinner = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.nSpinner.setGeometry(QtCore.QRect(100, 150, 100, 50))
        self.nSpinner.setDecimals(1)
        self.nSpinner.setMinimum(1.0)
        self.nSpinner.setMaximum(3.0)
        self.nSpinner.setSingleStep(0.2)
        self.nSpinner.setObjectName("nSpinner")
        self.nSpinner.valueChanged.connect(self.nVal)
        self.rSpinner = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.rSpinner.setGeometry(QtCore.QRect(280, 150, 100, 50))
        self.rSpinner.setDecimals(1)
        self.rSpinner.setMinimum(1.0)
        self.rSpinner.setMaximum(2.8)
        self.rSpinner.setSingleStep(0.2)
        self.rSpinner.setObjectName("rSpinner")
        self.rSpinner.valueChanged.connect(self.rVal)



        ########## Buttons ##########
        self.RunButton = QtWidgets.QPushButton(self.centralwidget)
        self.RunButton.setGeometry(QtCore.QRect(450, 150, 120, 50))
        self.RunButton.setObjectName("RunButton")
        self.RunButton.setStyleSheet('QPushButton {background-color: #9e3920; color: blue;}')
        self.RunButton.clicked.connect(self.Run)
        self.BackgroundButton = QtWidgets.QPushButton(self.centralwidget)
        self.BackgroundButton.setGeometry(QtCore.QRect(450, 22, 120, 35))
        self.BackgroundButton.setObjectName("BackgroundButton")
        self.BackgroundButton.clicked.connect(self.Enter1)  
        self.VideoButton = QtWidgets.QPushButton(self.centralwidget)
        self.VideoButton.setGeometry(QtCore.QRect(450, 85, 120, 35))
        self.VideoButton.setObjectName("VideoButton")
        self.VideoButton.clicked.connect(self.Enter2)  
        self.TrackButton = QtWidgets.QPushButton(self.centralwidget)
        self.TrackButton.setGeometry(QtCore.QRect(300, 860, 100, 50))
        self.TrackButton.setObjectName("TrackButton")
        self.TrackButton.setStyleSheet('QPushButton {background-color: #9e3920; color: blue;}')
        self.TrackButton.clicked.connect(self.Track)
        self.PlotButton = QtWidgets.QPushButton(self.centralwidget)
        self.PlotButton.setGeometry(QtCore.QRect(450, 860, 150, 50))
        self.PlotButton.setObjectName("PlotButton")
        self.PlotButton.setStyleSheet('QPushButton {background-color: #A3C1DA; color: blue;}')
        self.PlotButton.clicked.connect(self.Plot)



        ########## Text Inputs ##########
        self.BackgroundInput = QtWidgets.QLineEdit(self.centralwidget)
        self.BackgroundInput.setGeometry(QtCore.QRect(200, 20, 200, 40))
        self.BackgroundInput.setObjectName("BackgroundInput")
        self.VideoInput = QtWidgets.QLineEdit(self.centralwidget)
        self.VideoInput.setGeometry(QtCore.QRect(200, 80, 200, 40))
        self.VideoInput.setObjectName("VideoInput")



        ########## Text Outputs ##########
        self.scrollArea = QtWidgets.QScrollArea(MainWindow)
        self.scrollArea.setGeometry(QtCore.QRect(1290, 530, 525, 390)) # Location and Dimensions
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 525, 390)) # Location and Dimensions
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.LoadingText = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)
        self.LoadingText.setGeometry(QtCore.QRect(0, 0, 525, 390)) # Location and Dimensions
        self.LoadingText.setObjectName("LoadingText")
        self.LoadingText.setFontPointSize(10)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scrollArea2 = QtWidgets.QScrollArea(MainWindow)
        self.scrollArea2.setGeometry(QtCore.QRect(720, 530, 525, 390)) # Location and Dimensions
        self.scrollArea2.setWidgetResizable(True)
        self.scrollArea2.setObjectName("scrollArea2")
        self.scrollAreaWidgetContents2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents2.setGeometry(QtCore.QRect(0, 0, 525, 390)) # Location and Dimensions
        self.scrollAreaWidgetContents2.setObjectName("scrollAreaWidgetContents2")
        self.OutputText = QtWidgets.QTextEdit(self.scrollAreaWidgetContents2)
        self.OutputText.setGeometry(QtCore.QRect(0, 0, 525, 390)) # Location and Dimensions
        self.OutputText.setObjectName("OutputText")
        self.OutputText.setFontPointSize(10)
        self.scrollArea2.setWidget(self.scrollAreaWidgetContents2)



        ########### Graphs ##########
        self.Displaytabs = QtWidgets.QTabWidget(self.centralwidget)
        self.Displaytabs.setGeometry(QtCore.QRect(720, 10, 1100, 500)) # Location and Dimensions
        self.Displaytabs.setObjectName("Displaytabs")
        self.PlotMSETH = QtWidgets.QWidget()
        self.layMSETH = QtWidgets.QHBoxLayout(self.PlotMSETH)
        self.Displaytabs.addTab(self.PlotMSETH, "")
        self.PlotMSEZ = QtWidgets.QWidget()
        self.layMSEZ = QtWidgets.QHBoxLayout(self.PlotMSEZ)
        self.Displaytabs.addTab(self.PlotMSEZ, "")
        self.PlotTHZ = QtWidgets.QWidget()
        self.layTHZ = QtWidgets.QHBoxLayout(self.PlotTHZ)
        self.Displaytabs.addTab(self.PlotTHZ, "")
        self.Plot2D = QtWidgets.QWidget()
        self.lay2D = QtWidgets.QHBoxLayout(self.Plot2D)
        self.Displaytabs.addTab(self.Plot2D, "")
        self.Plot3D = QtWidgets.QWidget()
        self.lay3D = QtWidgets.QHBoxLayout(self.Plot3D)
        self.Displaytabs.addTab(self.Plot3D, "")



        ########## Setup ###########
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.retranslateUi(MainWindow)
        self.Displaytabs.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)



    ########## Protocol To Run ##########
    # LCD events
    def MinMSElcdUpdate(self, event):
        global MinMSE
        MinMSE = event # Setting Min MSE value
        self.MinMSElcd.display(event)

    def MaxMSElcdUpdate(self, event):
        global MaxMSE
        MaxMSE = event # Setting Max MSE value
        self.MaxMSElcd.display(event)

    def ThlcdUpdate(self, event):
        global threshold 
        threshold = event/200 # Setting threshold value
        self.Thlcd.display(event/200)

    def TemplcdUpdate(self, event):
        global tempsteps
        tempsteps = event # Setting template steps
        self.Templcd.display(event)

    def FramelcdUpdate(self, event):
        global nth_frame
        nth_frame = event # Setting frame steps
        self.Framelcd.display(event)



    # Spinner events
    def nVal(self, event):
        global n
        n = round(event, 1) # Value of n template to use

    def rVal(self, event):
        global r
        r = round(event, 1) # Value of r template to use



    # Button events
    def Enter1(self):
        global background
        background = str(self.BackgroundInput.text()) # Background file to use
        print(self.BackgroundInput.text())
        self.OutputText.append('Background image chosen - {}' .format(background))

    def Enter2(self):
        global video
        video = str(self.VideoInput.text()) # Video file to use
        print(self.VideoInput.text())
        self.OutputText.append('Video file chosen - {}' .format(video))

    def Plot(self):
        x = PlotX
        y = PlotY
        z = PlotZ
        tracking = PlotCOUNT

        pts = mlab.points3d(x, y, z, tracking, colormap="copper", mode='point')
        pts.actor.actor.property.render_points_as_spheres = True
        pts.actor.actor.property.point_size = 5.0
        
        mlab.show()

    def Track(self):
        answer = QtWidgets.QMessageBox.question(
            self.centralwidget, 'Lauch Tracker', 'Are you sure you are ready to execute Tracker from Initilisation Settings?',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if answer == QtWidgets.QMessageBox.Yes:#
            self.LoadingText.setFontPointSize(20)
            self.LoadingText.append('------Tracker Launched------')
            self.LoadingText.setFontPointSize(10)
            self.Tracker()

        else:
            pass

    def Run(self):
        # Attempting to collect GUI input info to run
        # Start the Loading Bar
        # Display Output Text

        self.LoadingText.setFontPointSize(20)
        self.LoadingText.append('---Initialisation Launched---')
        self.LoadingText.setFontPointSize(10)

        global background
        self.OutputText.append('Background file chosen - {}' .format(background))
        global video
        self.OutputText.append('Video file chosen - {}' .format(video))
        global count
        global end
        end = 11
        self.OutputText.append('Number of Frames to process - {}' .format(end - 1))
        global nth_frame
        self.OutputText.append('Steps in Frames being counted - {}' .format(nth_frame))
        global contrast
        self.OutputText.append('Contrast Value - {}' .format(contrast))
        global sharpness
        self.OutputText.append('Sharpness Value - {}' .format(sharpness))
        global n
        self.OutputText.append('Template Refractive index - {}' .format(n))
        global r
        self.OutputText.append('Template sphere radius - {}' .format(r))
        global Location
        global threshold
        threshold = 0.07
        self.OutputText.append('Threshold Value - {}' .format(threshold))
        global tempsteps
        tempsteps = 5
        self.OutputText.append('Steps in Templates being counted - {}' .format(tempsteps))
        global tempcount
        global tempend
        global brightness
        global MinMSE
        global MaxMSE
        global PlotZ
        global PlotTH
        global PlotMSE



        ########## Background and Video Processing ##########
        bgd = cv2.imread('..Backgrounds/{}.png' .format(background)) # Location of background image
        bgdgray = cv2.cvtColor(bgd, cv2.COLOR_BGR2GRAY) 
        arraybgdgray = np.array(bgdgray) 
        vidcap = cv2.VideoCapture('..Videos/{}.avi' .format(video)) # Location of video



        ######### Create Frames #########
        while(count < end):
            tic = time.perf_counter() # Estimating run time starter

            # Capture frame-by-frame
            skip = nth_frame * count
            vidcap.set(1, skip)
            ret, frame = vidcap.read()

            self.LoadingText.append('Reading frame %d' % skip)

            # Operations on the frames come here
            imggray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # BGR or RGB (cast different readings)
            array1 = np.array(imggray)
            arrayDIV = np.divide(array1, arraybgdgray) * brightness
            divided = Image.fromarray(arrayDIV)
            final = divided.convert("L")

            # Image contraster
            enhancer1 = ImageEnhance.Contrast(final)
            enhanced1 = enhancer1.enhance(contrast)
            enhancer2 = ImageEnhance.Sharpness(enhanced1)
            enhanced2 = enhancer2.enhance(sharpness)

            # Save the resulting frame
            enhanced2.save("enhanced frames/frame%d.png" % count)
            self.LoadingText.append('Processed frame %d' % count)

            # Matching process
            img_rgb = cv2.imread("enhanced frames/frame%d.png" % count)
            img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
            img_to_crop = Image.open("enhanced frames/frame%d.png" % count).convert('L')

            while(tempcount < tempend):
                template = cv2.imread("templates/0.703 pix-um/n={}, r={}/img{}.png" .format(n, r, tempcount), 0) # 0.711 pix-um/
                w, h = template.shape[::-1]
                templatePIL = Image.open("templates/0.703 pix-um/n={}, r={}/img{}.png" .format(n, r, tempcount)).convert('L') # 0.711 pix-um/
                w, h = templatePIL.size

                res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                loc = np.where(res >= threshold)
                for pt in zip(*loc[::-1]):                
                    cv2.circle(img_rgb, (pt[0] + int(h/2), pt[1] + int(h/2)), 10, (0,0,255), 1)

                    # Crop matched image to size of template for MSE
                    crop = img_to_crop.crop((pt[0], pt[1], pt[0] + w, pt[1] + h))

                    crop = crop.save("cropped frames/crop f={}, s={}.png" .format(count, tempcount))
                    crop = Image.open("cropped frames/crop f={}, s={}.png" .format(count, tempcount))

                    def mse(actual, pred): 
                        actual, pred = np.array(actual), np.array(pred)
                        return np.square(np.subtract(actual,pred)).mean() 
                        
                    mse_val = mse(templatePIL, crop)

                    plot3 = [[(tempcount) for col in range(1)] for row in range(1)] # Z coordinates
                    plot4 = [[(max_val) for col in range(1)] for row in range(1)] # Threshold
                    plot5 = [[(mse_val) for col in range(1)] for row in range(1)] # MSE

                    PlotZ = PlotZ + plot3
                    PlotTH = PlotTH + plot4
                    PlotMSE = PlotMSE + plot5

                tempcount += tempsteps

            # Save the resulting matched frame
            cv2.imwrite("matched frames/frame%d.png" % count,img_rgb)

            toc = time.perf_counter() # Estimating run time stopper

            self.LoadingText.append('Matched frame %d \n' % count)
            self.LoadingText.append(f"Estimated Time Remaining: {int((toc - tic)*((end - 1) - count))} seconds")

            tempcount = 1
            count += 1
            self.progressBar.setValue(int((count/(end-1))*100)) # LoadingBar Protocol

        # Reset counter for multiple plotting events in singluar window
        count = 1
        self.LoadingText.setFontPointSize(15)
        self.LoadingText.append('\nAll Frames Created \nLoading Plots.......')
        self.LoadingText.setFontPointSize(12)

        # Arrays for Plots
        z = PlotZ
        th = PlotTH
        mse = PlotMSE

        # Output Data
        Matchval = np.mean(th)
        SDev = np.std(th)
        UDep = len(np.unique(z))
        RDep = len(z) - UDep
        MSEval = np.mean(mse)
        RecMinMSE = int(np.percentile(mse, 10))
        RecMaxMSE = int(np.percentile(mse, 90))
        RecMinTH = round(np.percentile(th, 10), 2)



        ######### MSE-TH plotter #########
        fig6 = plt.figure()

        self.canvas = FigureCanvas(fig6)
        self.axes = fig6.add_subplot()

        self.axes.axvline(RecMinMSE, color='b')
        self.axes.axvline(RecMaxMSE, color='b')
        self.axes.axhline(RecMinTH, color='b')

        self.axes.axvspan(RecMaxMSE, (np.max(mse)*1.05), facecolor='0.5', alpha = 0.5)
        self.axes.axvspan(RecMinMSE, (np.min(mse)*0.9), facecolor='0.5', alpha = 0.5)
        self.axes.add_patch(Rectangle((RecMinMSE, (np.min(th)*0.9)), (RecMaxMSE-RecMinMSE), (RecMinTH-(np.min(th)*0.9)), facecolor='0.5', alpha = 0.5))

        pnt = self.axes.scatter(mse, th, c=z, s=2)
        cbar = plt.colorbar(pnt)
        cbar.set_label("Z Axis")
        self.axes.set_title('n = {}, r = {}' .format(n, r))
        self.axes.set_xlabel('MSE Value')
        self.axes.set_ylabel('Match Value')
        self.axes.set_xlim((np.min(mse)*0.9), (np.max(mse)*1.05))
        self.axes.set_ylim((np.min(th)*0.9), (np.max(th)*1.05))
        self.axes.scatter(mse, th, c=z, s=2)
        self.axes.set_axisbelow(True)
        self.axes.minorticks_on()
        self.axes.grid(which='major', linestyle='-', linewidth='0.5', color='red')
        self.axes.grid(which='minor', linestyle='-', linewidth='0.1', color='black')

        plt.savefig('.MSE-TH Plots/MSE-Th(1) n={}, r={}.png' .format(n, r))
        self.layMSETH.addWidget(FigureCanvas(fig6))
        self.LoadingText.append('\nMSE-Th(1) Plot Created and saved')



        ######### Z-MSE plotter #########
        fig5, ax5 = plt.subplots()

        ax5.axhline(RecMinMSE, color='m')
        ax5.axhline(RecMaxMSE, color='m')
        ax5.plot(z, mse, '.', color='red', markersize=2)
        ax5.set_title('n = {}, r = {}, Average={}' .format(n, r, MSEval))
        ax5.axhspan(RecMaxMSE, (np.max(mse)*1.05), facecolor='0.5', alpha = 0.5)
        ax5.axhspan(RecMinMSE, (np.min(mse)*0.9), facecolor='0.5', alpha = 0.5)
        ax5.set_xlabel('Z Axis')
        ax5.set_ylabel('MSE Value')
        ax5.set_axisbelow(True)
        ax5.set_ylim((np.min(mse)*0.9), (np.max(mse)*1.05))
        ax5.minorticks_on()
        ax5.grid(which='major', linestyle='-', linewidth='0.5', color='blue')
        ax5.grid(which='minor', linestyle='-', linewidth='0.1', color='black')

        plt.savefig('.MSE-Z Plots/MSE-Z(1) n={}, r={}.png' .format(n, r))
        self.layMSEZ.addWidget(FigureCanvas(fig5))
        self.LoadingText.append('\nZ-MSE(1) Plot Created and saved') 



        ######### Z-Th plotter #########
        fig4, ax4 = plt.subplots()

        ax5.axhline(RecMinTH, color='m')
        ax4.plot(z, th, '.', color='red', markersize=2)
        ax4.set_title('n = {}, r = {}, Average={}' .format(n, r, Matchval))
        ax4.axhspan(RecMinTH, (np.min(th)*0.9), facecolor='0.5', alpha = 0.5)
        ax4.set_xlabel('Z Axis')
        ax4.set_ylabel('Match Value')
        ax4.set_axisbelow(True)
        ax4.set_ylim((np.min(th)*0.9), (np.max(th)*1.05))
        ax4.minorticks_on()
        ax4.grid(which='major', linestyle='-', linewidth='0.5', color='blue')
        ax4.grid(which='minor', linestyle='-', linewidth='0.1', color='black')

        plt.savefig('.Th-Z Plots/Th-Z(1) n={}, r={}.png' .format(n, r))
        self.layTHZ.addWidget(FigureCanvas(fig4))
        self.LoadingText.append('\nZ-Th(1) Plot Created and saved\n') 
        self.LoadingText.setFontPointSize(10)



        ######### Print Specifics #########
        self.OutputText.setFontPointSize(20)
        self.OutputText.append('\n \n------INPUT SPECIFICS-----')
        self.OutputText.setFontPointSize(15)
        self.OutputText.append('**Frames Settings**')
        self.OutputText.setFontPointSize(10)
        self.OutputText.append('Start - %d, End - %d , Total - %d, Steps - %d \n' % (nth_frame, nth_frame*(end-1), (end-1), nth_frame))
        self.OutputText.setFontPointSize(15)
        self.OutputText.append('**Enhancement Settings**')
        self.OutputText.setFontPointSize(10)
        self.OutputText.append('Contrast - %d, Sharpness - %d \n' % (contrast, sharpness))
        self.OutputText.setFontPointSize(15)
        self.OutputText.append('**Template Settings**')
        self.OutputText.setFontPointSize(10)
        self.OutputText.append('Folder - n={}, r={}, Threshold - {}, Steps - {} \n \n' .format(n, r, threshold, tempsteps))
        self.OutputText.setFontPointSize(20)
        
        self.OutputText.append('-----OUTPUT SPECIFICS----')
        self.OutputText.setFontPointSize(15)
        self.OutputText.append('**Matching Data**')
        self.OutputText.setFontPointSize(10)
        self.OutputText.append('Average Match Value - {}, S.Dev of Match Value - {}, Recommended Min Match Value - {} \n' .format(Matchval, SDev, RecMinTH))
        self.OutputText.setFontPointSize(15)
        self.OutputText.append('**Depth Data**')
        self.OutputText.setFontPointSize(10)
        self.OutputText.append('Total Number of Unique Depths - {}, Total Number of Repeating Depths - {} \n' .format(UDep, RDep))
        self.OutputText.setFontPointSize(15)
        self.OutputText.append('**MSE Data**')
        self.OutputText.setFontPointSize(10)
        self.OutputText.append('Average MSE Value - {}, Recommended Min MSE - {}, Recommended Max MSE - {} \n' .format(MSEval, RecMinMSE, RecMaxMSE))

        PlotZ = []
        PlotTH = []
        PlotMSE = []
        
    def Tracker(self):
        # Attempting to collect GUI input info to run
        # Start the Loading Bar
        # Display Output Text

        global background
        global video
        global videoframes
        global count
        global nth_frame
        global end
        end = int(videoframes/nth_frame) + 1 # Assuming 10,000 frames in video
        self.OutputText.append('Number of Frames to process - {}' .format(end - 1))
        self.OutputText.append('Steps in Frames being counted - {}' .format(nth_frame))
        global contrast
        self.OutputText.append('Contrast Value - {}' .format(contrast))
        global sharpness
        self.OutputText.append('Sharpness Value - {}' .format(sharpness))
        global n
        self.OutputText.append('Template Refractive index - {}' .format(n))
        global r
        self.OutputText.append('Template sphere radius - {}' .format(r))
        global Location
        global threshold
        self.OutputText.append('Threshold Value - {}' .format(threshold))
        global tempsteps
        self.OutputText.append('Steps in Templates being counted - {}' .format(tempsteps))
        global tempcount
        global tempend
        global brightness
        global MinMSE
        global MaxMSE
        global PlotX
        global PlotY
        global PlotZ
        global PlotTH
        global PlotMSE
        global PlotCOUNT



        ########## Background and Video Processing ##########
        bgd = cv2.imread('..Backgrounds/{}.png' .format(background)) # Location of background image
        bgdgray = cv2.cvtColor(bgd, cv2.COLOR_BGR2GRAY) 
        arraybgdgray = np.array(bgdgray) 
        vidcap = cv2.VideoCapture('..Videos/{}.avi' .format(video)) # Location of video



        ######### Create Frames #########
        while(count < end):
            tic = time.perf_counter() # Estimating run time starter

            # Capture frame-by-frame
            skip = nth_frame * count
            vidcap.set(1, skip)
            ret, frame = vidcap.read()

            self.LoadingText.append('Reading frame %d' % skip)

            # Operations on the frames come here
            imggray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            array1 = np.array(imggray)
            arrayDIV = np.divide(array1, arraybgdgray) * brightness
            divided = Image.fromarray(arrayDIV)
            final = divided.convert("L")

            # Image contraster
            enhancer1 = ImageEnhance.Contrast(final)
            enhanced1 = enhancer1.enhance(contrast)
            enhancer2 = ImageEnhance.Sharpness(enhanced1)
            enhanced2 = enhancer2.enhance(sharpness)

            # Save the resulting frame
            enhanced2.save("enhanced frames/frame%d.png" % count)

            self.LoadingText.append('Processed frame %d' % count)

            # Matching process
            img_rgb = cv2.imread("enhanced frames/frame%d.png" % count)
            img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
            img_to_crop = Image.open("enhanced frames/frame%d.png" % count).convert('L')

            while(tempcount < tempend):
                template = cv2.imread("templates/0.703 pix-um/n={}, r={}/img{}.png" .format(n, r, tempcount), 0) # 0.711 pix-um/
                w, h = template.shape[::-1]
                templatePIL = Image.open("templates/0.703 pix-um/n={}, r={}/img{}.png" .format(n, r, tempcount)).convert('L') # 0.711 pix-um/
                w, h = templatePIL.size

                res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                loc = np.where(res >= threshold)
                for pt in zip(*loc[::-1]):                
                    cv2.circle(img_rgb, (pt[0] + int(h/2), pt[1] + int(h/2)), 10, (0,0,255), 1)

                    # Crop matched image to size of template for MSE
                    crop = img_to_crop.crop((pt[0], pt[1], pt[0] + w, pt[1] + h))

                    crop = crop.save("cropped frames/crop f={}, s={}.png" .format(count, tempcount))
                    crop = Image.open("cropped frames/crop f={}, s={}.png" .format(count, tempcount))

                    def mse(actual, pred): 
                        actual, pred = np.array(actual), np.array(pred)
                        return np.square(np.subtract(actual,pred)).mean() 
                        
                    mse_val = mse(templatePIL, crop)


                    if (mse_val > MinMSE) and (mse_val < MaxMSE):
                        plot1 = [[(pt[0] + int(h/2)) for col in range(1)] for row in range(1)] # X coordinates
                        plot2 = [[(pt[1] + int(h/2)) for col in range(1)] for row in range(1)] # Y coordinates
                        plot3 = [[(tempcount) for col in range(1)] for row in range(1)] # Z coordinates
                        plot4 = [[(max_val) for col in range(1)] for row in range(1)] # Threshold
                        plot5 = [[(mse_val) for col in range(1)] for row in range(1)] # MSE
                        plot6 = [[(count) for col in range(1)] for row in range(1)] # Frame Counts

                        PlotX = PlotX + plot1
                        PlotY = PlotY + plot2
                        PlotZ = PlotZ + plot3
                        PlotTH = PlotTH + plot4
                        PlotMSE = PlotMSE + plot5
                        PlotCOUNT = PlotCOUNT + plot6

                tempcount += tempsteps

            # Save the resulting matched frame
            cv2.imwrite("matched frames/frame%d.png" % count,img_rgb)

            toc = time.perf_counter() # Estimating run time stopper
            self.LoadingText.append('Matched frame %d \n' % count)
            self.LoadingText.append(f"Estimated Time Remaining: {int((toc - tic)*((end - 1) - count))} seconds")

            tempcount = 1
            count += 1
            self.progressBar.setValue(int((count/(end-1))*100)) # LoadingBar Protocol

        # Reset counter for multiple plotting events in singluar window
        count = 1
        self.LoadingText.setFontPointSize(15)
        self.LoadingText.append('\nAll Frames Created \nLoading Plots.......')
        self.LoadingText.setFontPointSize(12)

        # Arrays for Plots
        x = PlotX
        y = PlotY
        z = PlotZ
        th = PlotTH
        mse = PlotMSE
        tracking = PlotCOUNT

        # Output Data
        UDep = len(np.unique(z))
        RDep = len(z) - UDep
        UX = len(np.unique(x))
        UY = len(np.unique(y))
        Matchval = np.mean(th)
        MSEval = np.mean(mse)



        ######### MSE-TH plotter #########
        fig6 = plt.figure()

        self.canvas = FigureCanvas(fig6)
        self.axes = fig6.add_subplot()

        pnt = self.axes.scatter(mse, th, c=z, s=2)
        cbar = plt.colorbar(pnt)
        cbar.set_label("Z Axis")

        self.axes.set_title('n = {}, r = {}' .format(n, r))
        self.axes.set_xlabel('MSE Value')
        self.axes.set_ylabel('Match Value')
        self.axes.scatter(mse, th, c=z, s=2)

        plt.savefig('.MSE-TH Plots/MSE-Th(2) n={}, r={}.png' .format(n, r))
        self.layMSETH.addWidget(FigureCanvas(fig6))
        self.LoadingText.append('\nMSE-Th(2) Plot Created and saved')



        ######### Z-MSE plotter #########
        fig5, ax5 = plt.subplots()

        ax5.plot(z, mse, '.', color='red', markersize=2)
        ax5.set_title('n = {}, r = {}, Average={}' .format(n, r, MSEval))
        ax5.set_xlabel('Z Axis')
        ax5.set_ylabel('MSE Value')

        plt.savefig('.MSE-Z Plots/MSE-Z(2) n={}, r={}.png' .format(n, r))
        self.layMSEZ.addWidget(FigureCanvas(fig5))
        self.LoadingText.append('\nZ-MSE(2) Plot Created and saved') 



        ######### Z-Th plotter #########
        fig4, ax4 = plt.subplots()

        ax4.plot(z, th, '.', color='red', markersize=2)
        ax4.set_title('n = {}, r = {}, Average={}' .format(n, r, Matchval))
        ax4.set_xlabel('Z Axis')
        ax4.set_ylabel('Match Value')

        plt.savefig('.Th-Z Plots/Th-Z(2) n={}, r={}.png' .format(n, r))
        self.layTHZ.addWidget(FigureCanvas(fig4))
        self.LoadingText.append('\nZ-Th(2) Plot Created and saved') 



        ######### 2D plotter #########
        fig1 = plt.figure()

        self.canvas1 = FigureCanvas(fig1)
        self.axes1 = fig1.add_subplot()

        pnt = self.axes1.scatter(mse, th, c=z, s=2)
        cbar = plt.colorbar(pnt)
        cbar.set_label("Z Axis")

        self.axes1.set_title('n={}, r={}, f={}, s={}' .format(n, r, end-1, tempsteps))
        self.axes1.set_xlabel('X Axis')
        self.axes1.set_ylabel('Y Axis')
        self.axes1.scatter(x, y, c=z, s=2)

        plt.savefig('.2D Plots/2D n={}, r={}, f={}, s={}.png' .format(n, r, end-1, tempsteps))
        self.lay2D.addWidget(FigureCanvas(fig1))
        self.LoadingText.append('\n2D Plot Created and saved')



        ######### 3D plotter #########
        fig7 = plt.figure()

        self.canvas = FigureCanvas(fig7)
        self.axes = fig7.add_subplot(111, projection='3d')

        pnt3d = self.axes.scatter(x, y, z, c=tracking, s=1)
        pnt3d.set_clim(np.min(tracking), np.max(tracking))
        cbar = plt.colorbar(pnt3d)
        cbar.set_label("Frame Number")

        self.axes.set_title('n={}, r={}, f={}, s={}.png' .format(n, r, end-1, tempsteps))
        self.axes.set_xlabel('X Axis')
        self.axes.set_ylabel('Y Axis')
        self.axes.set_zlabel('Z Axis')
        self.axes.set_zlim([0, 220])
        self.axes.scatter(x, y, z, c=tracking, s=1)

        plt.savefig('.3D Plots/3D n={}, r={}, f={}, s={}.png' .format(n, r, end-1, tempsteps))
        self.lay3D.addWidget(self.canvas)
        self.LoadingText.append('\n3D Plot Created and saved \n')



        ########## Saving DATA files ###########
        np.savetxt('.Data files/X Data/n={}, r={}, f={}, s={}.txt' .format(n, r, end-1, tempsteps), x)
        np.savetxt('.Data files/Y Data/n={}, r={}, f={}, s={}.txt' .format(n, r, end-1, tempsteps), y)
        np.savetxt('.Data files/Z Data/n={}, r={}, f={}, s={}.txt' .format(n, r, end-1, tempsteps), z)
        np.savetxt('.Data files/Count Data/n={}, r={}, f={}, s={}.txt' .format(n, r, end-1, tempsteps), tracking)
        np.savetxt('.Data files/MSE Data/co={}, sh={}, th={}.txt' .format(contrast, sharpness, threshold), mse)

        self.LoadingText.append('All data points saved')
        self.LoadingText.setFontPointSize(10)



        ######### Print Specifics #########
        self.OutputText.setFontPointSize(20)
        self.OutputText.append('\n \n------INPUT SPECIFICS-----')
        self.OutputText.setFontPointSize(15)
        self.OutputText.append('**Frames Settings**')
        self.OutputText.setFontPointSize(10)
        self.OutputText.append('Start - %d, End - %d , Total - %d, Steps - %d \n' % (nth_frame, nth_frame*(end-1), (end-1), nth_frame))
        self.OutputText.setFontPointSize(15)
        self.OutputText.append('**Enhancement Settings**')
        self.OutputText.setFontPointSize(10)
        self.OutputText.append('Contrast - %d, Sharpness - %d \n' % (contrast, sharpness))
        self.OutputText.setFontPointSize(15)
        self.OutputText.append('**Template Settings**')
        self.OutputText.setFontPointSize(10)
        self.OutputText.append('Folder - n={}, r={}, Threshold - {}, Steps - {} \n \n' .format(n, r, threshold, tempsteps))
        self.OutputText.setFontPointSize(20)
        
        self.OutputText.append('-----OUTPUT SPECIFICS----')
        self.OutputText.setFontPointSize(15)
        self.OutputText.append('**Depth Data**')
        self.OutputText.setFontPointSize(10)
        self.OutputText.append('Total Number of Unique Depths - {}, Total Number of Repeating Depths - {} \n' .format(UDep, RDep))
        self.OutputText.setFontPointSize(15)
        self.OutputText.append('**MSE Data**')
        self.OutputText.setFontPointSize(10)
        self.OutputText.append('Average MSE Value - {} \n' .format(MSEval))
        self.OutputText.setFontPointSize(15)
        self.OutputText.append('**X-Y Data**')
        self.OutputText.setFontPointSize(10)
        self.OutputText.append('Total Number of Unique X Values - {}, Total Number of Unique Y Values - {} \n \n' .format(UX, UY))


    ########## Window Setup ##########
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "The Hologram Analysis System 3        [THAS3]       (created by I.T.Booth)"))
        self.BackgroundLabel.setText(_translate("MainWindow", "Background"))
        self.VideoLabel.setText(_translate("MainWindow", "Video"))
        self.label_3.setText(_translate("MainWindow", "Min MSE"))
        self.label_4.setText(_translate("MainWindow", "Max MSE"))
        self.label_5.setText(_translate("MainWindow", "Threshold"))
        self.label_6.setText(_translate("MainWindow", "Template Steps"))
        self.label_7.setText(_translate("MainWindow", "Frame Steps"))
        self.nLabel.setText(_translate("MainWindow", "n ="))
        self.rLabel.setText(_translate("MainWindow", "r ="))

        self.RunButton.setText(_translate("MainWindow", "Initialise"))
        self.BackgroundButton.setText(_translate("MainWindow", "Enter"))
        self.VideoButton.setText(_translate("MainWindow", "Enter"))
        self.TrackButton.setText(_translate("MainWindow", "Track"))
        self.PlotButton.setText(_translate("MainWindow", "Interactive 3D"))

        self.Displaytabs.setTabText(self.Displaytabs.indexOf(self.PlotMSEZ), _translate("MainWindow", "Z-MSE"))
        self.Displaytabs.setTabText(self.Displaytabs.indexOf(self.PlotTHZ), _translate("MainWindow", "Z-Th"))
        self.Displaytabs.setTabText(self.Displaytabs.indexOf(self.PlotMSETH), _translate("MainWindow", "MSE-Th (Z)"))
        self.Displaytabs.setTabText(self.Displaytabs.indexOf(self.Plot2D), _translate("MainWindow", "2D (Z)"))
        self.Displaytabs.setTabText(self.Displaytabs.indexOf(self.Plot3D), _translate("MainWindow", "3D"))


########## Execute above protocol ##########
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())