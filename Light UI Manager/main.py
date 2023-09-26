import os.path
import functools
from PySide2 import QtGui, QtUiTools, QtCore, QtWidgets
"""shiboken2: Connect between python and c++"""
from shiboken2 import wrapInstance
import pymel.core as pm
import maya.cmds as mc
import maya.OpenMayaUI as omui
import mtoa.utils as mutils
from light_functions import *


def getMayaWindow():
    """pointer to the maya main window"""

    ptr = omui.MQtUtil.mainWindow()
    if ptr:
        return wrapInstance(int(ptr), QtWidgets.QMainWindow)

def run():
    """builds UI"""
    global win
    win = GeometryGenerator(parent = getMayaWindow())

class GeometryGenerator(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(GeometryGenerator, self).__init__(parent)

        self.setFixedSize(715, 200)

        self.lightType = 'spotLight1'

        # from pysideuic--------------------------
        self.gridLayout = QtWidgets.QGridLayout()

        '''01_Obj Buttons'''
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)

        self.spotLgtBtn = QtWidgets.QRadioButton("Spot Light")
        self.horizontalLayout.addWidget(self.spotLgtBtn)

        self.areaLgtBtn = QtWidgets.QRadioButton("Area Light")
        self.horizontalLayout.addWidget(self.areaLgtBtn)

        self.pointLgtBtn = QtWidgets.QRadioButton("Point Light")
        self.horizontalLayout.addWidget(self.pointLgtBtn)

        self.DirLgtBtn = QtWidgets.QRadioButton("Directional Light")
        self.horizontalLayout.addWidget(self.DirLgtBtn)

        self.SkyLgtBtn = QtWidgets.QRadioButton("aiSkyDomeLight")
        self.horizontalLayout.addWidget(self.SkyLgtBtn)

        self.PorLgtBtn = QtWidgets.QRadioButton("aiLightPortal")
        self.horizontalLayout.addWidget(self.PorLgtBtn)

        self.horizontalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        '''02_Use Custom Name'''
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()

        self.customNameCheckBox = QtWidgets.QCheckBox("Use Custom Name")
        self.horizontalLayout_2.addWidget(self.customNameCheckBox)

        self.customNameLineEdit = QtWidgets.QLineEdit()
        self.horizontalLayout_2.addWidget(self.customNameLineEdit)

        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)

        '''03_createLightPushButton'''
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.createLightPushButton = QtWidgets.QPushButton("Create Light")
        self.horizontalLayout_3.addWidget(self.createLightPushButton)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)


        """04_create Intensity"""
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()

        self.intensity_label = QtWidgets.QLabel("Intensity:  1.00")
        self.intensity_label.setFixedWidth(85)
        self.horizontalLayout_4.addWidget(self.intensity_label)

        self.intensityLineEdit = QtWidgets.QLineEdit()
        self.intensityLineEdit.setFixedWidth(100)
        self.horizontalLayout_4.addWidget(self.intensityLineEdit)

        self.intensity_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.intensity_slider.setRange(0, 10)
        self.intensity_slider.setValue(1)
        self.horizontalLayout_4.addWidget(self.intensity_slider)
        self.gridLayout.addLayout(self.horizontalLayout_4, 3, 0, 1, 1)

        """05_create Exposure"""
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()

        self.exposure_label = QtWidgets.QLabel("Exposure: 1.00")
        self.exposure_label.setFixedWidth(85)
        self.horizontalLayout_5.addWidget(self.exposure_label)

        self.exposureLineEdit = QtWidgets.QLineEdit()
        self.exposureLineEdit.setFixedWidth(100)
        self.horizontalLayout_5.addWidget(self.exposureLineEdit)

        self.exposure_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.exposure_slider.setRange(0, 10)
        self.exposure_slider.setValue(1)
        self.horizontalLayout_5.addWidget(self.exposure_slider)
        self.gridLayout.addLayout(self.horizontalLayout_5, 4, 0, 1, 1)

        """06_create Samples"""
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()

        self.sample_label = QtWidgets.QLabel("Samples: 3")
        self.sample_label.setFixedWidth(85)
        self.horizontalLayout_6.addWidget(self.sample_label)

        self.sampleLineEdit = QtWidgets.QLineEdit()
        self.sampleLineEdit.setFixedWidth(100)
        self.horizontalLayout_6.addWidget(self.sampleLineEdit)

        self.sample_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.sample_slider.setRange(0, 10)
        self.sample_slider.setValue(1)
        self.horizontalLayout_6.addWidget(self.sample_slider)
        self.gridLayout.addLayout(self.horizontalLayout_6, 5, 0, 1, 1)


        '''07_create Choose Color'''
        self.horizontalLayout_7  = QtWidgets.QHBoxLayout()
        self.color_button = QtWidgets.QPushButton("Choose Color")
        self.horizontalLayout_7.addWidget(self.color_button)
        self.gridLayout.addLayout(self.horizontalLayout_7, 6, 0, 1, 1)


        # MANY THINGS YOU HAVE TO ADD
        self.makeConnections()
        self.setWindowTitle("Light Controlled Manager")
        self.setLayout(self.gridLayout)
        self.initUiState()
        self.show()

    def makeConnections(self):
        """Connect events in UI"""

        """functools.partial(): 원하는 문자열이나 변수를 함수에 전달가능"""
        self.spotLgtBtn.clicked.connect(functools.partial(self.radioChange, 'spotLight1'))
        self.areaLgtBtn.clicked.connect(functools.partial(self.radioChange, 'areaLight1'))
        self.pointLgtBtn.clicked.connect(functools.partial(self.radioChange, 'pointLight1'))
        self.DirLgtBtn.clicked.connect(functools.partial(self.radioChange, 'directionalLight1'))
        self.SkyLgtBtn.clicked.connect(functools.partial(self.radioChange, 'aiSkyDomeLight1'))
        self.PorLgtBtn.clicked.connect(functools.partial(self.radioChange, 'aiLightPortal1'))

        self.customNameCheckBox.stateChanged.connect(self.customNameLineEdit.setEnabled)
        self.createLightPushButton.clicked.connect(self.createLight)

        self.intensity_slider.valueChanged.connect(functools.partial(update_intensity_label, self))
        self.intensityLineEdit.editingFinished.connect(functools.partial(update_intensity_value, self))
        self.exposure_slider.valueChanged.connect(functools.partial(update_exposure_label, self))
        self.exposureLineEdit.editingFinished.connect(functools.partial(update_exposure_value, self))
        self.sample_slider.valueChanged.connect(functools.partial(update_sample_label, self))
        self.sampleLineEdit.editingFinished.connect(functools.partial(update_sample_value, self))

        self.color_button.clicked.connect(functools.partial(choose_color, self))

    def initUiState(self):
        """sets up the initial state of UI"""
        self.spotLgtBtn.toggle()
        self.customNameLineEdit.setEnabled(False)
        self.customNameLineEdit.setPlaceholderText('nameOfLight')

    def radioChange(self, lightType):
        self.lightType = lightType
        print(f"lightType: {lightType}")

    def createLight(self):
        print(f"create geometry pressed: {self.lightType}")

        finalName = self.lightType

        if self.customNameCheckBox.isChecked():
            """get a custom name"""
            customName = self.customNameLineEdit.text()

            if customName != 'nameOfLight':
                finalName = customName

        if self.lightType == 'spotLight1':
            mc.spotLight(n=finalName)
        elif self.lightType == 'areaLight1':
            mutils.createLocator('areaLight', asLight=True)
            parentName = mc.listRelatives(parent=True, fullPath=True)
            mc.rename(parentName, finalName)
        elif self.lightType == 'pointLight1':
            mc.pointLight(n=finalName)
        elif self.lightType == 'directionalLight1':
            mc.directionalLight(n=finalName)
        elif self.lightType == 'aiSkyDomeLight1':
            mutils.createLocator('aiSkyDomeLight', asLight=True)
            parentName = mc.listRelatives(parent=True, fullPath=True)
            mc.rename(parentName, finalName)
        elif self.lightType == 'aiLightPortal1':
            mutils.createLocator('aiLightPortal', asLight=True)
            parentName = mc.listRelatives(parent=True, fullPath=True)
            mc.rename(parentName, finalName)
        else:
            print('BROKEN LOGIC')

