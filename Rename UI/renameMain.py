import os
import functools
from PySide2 import QtGui, QtUiTools, QtCore, QtWidgets
"""shiboken2: Connect between python and c++"""
from shiboken2 import wrapInstance
import logging
import pymel.core as pm
import maya.OpenMayaUI as omui

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

def getMayaWindow():
    """pointer to the maya main window"""

    ptr = omui.MQtUtil.mainWindow()
    if ptr:
        return wrapInstance(int(ptr), QtWidgets.QMainWindow)

def run():
    """builds UI"""
    global win
    win = ControllerLibraryUI(parent = getMayaWindow())

class ControllerLibraryUI(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(ControllerLibraryUI, self).__init__(parent)

        self.setFixedSize(615, 65)

        self.Layout = QtWidgets.QGridLayout()

        self.gridLayout = QtWidgets.QGridLayout()

        self.initial_numName = None

        # Start Label
        self.verticalLayout = QtWidgets.QVBoxLayout()

        self.startLabel = QtWidgets.QLabel("START")
        self.startLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.verticalLayout.addWidget(self.startLabel)
        self.startLineEdit = QtWidgets.QLineEdit("1")

        self.verticalLayout.addWidget(self.startLineEdit)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        # Padding Number
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()

        self.padLabel = QtWidgets.QLabel("PADDING")
        self.padLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.padLabel)
        self.padLineEdit = QtWidgets.QLineEdit("3")
        self.verticalLayout_2.addWidget(self.padLineEdit)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 1, 1, 1)

        # Rename Line Edit
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()

        self.renameLabel = QtWidgets.QLabel("RENAME EDIT")
        self.renameLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.renameLabel)
        self.horizontalLayout = QtWidgets.QHBoxLayout()

        self.reLineEdit = QtWidgets.QLineEdit()

        self.horizontalLayout.addWidget(self.reLineEdit)
        self.reButton = QtWidgets.QPushButton("RE")

        self.horizontalLayout.addWidget(self.reButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout_4, 0, 2, 1, 1)

        # Surfix Label
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()

        self.surfixLabel = QtWidgets.QLabel("SURFIX")
        self.surfixLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.verticalLayout_6.addWidget(self.surfixLabel)
        self.comboBox = QtWidgets.QComboBox()

        itemList = ["", "_gr", "_loc", "_joint", "_anim", "_crv", "_ik", "_rig", "_geo", "_set", "_lgt"]

        for i in itemList:
            self.comboBox.addItem(i)

        self.verticalLayout_6.addWidget(self.comboBox)
        self.gridLayout.addLayout(self.verticalLayout_6, 0, 3, 1, 1)

        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(2, 5)
        self.gridLayout.setColumnStretch(3, 1)

        self.Layout.addLayout(self.gridLayout, 0, 0, 1, 1)


        # MANY THINGS YOU HAVE TO ADD
        self.makeConnections()
        self.setWindowTitle("Rename")
        self.setLayout(self.Layout)
        self.initUiState()
        self.show()

    def initUiState(self):
        pass

    def makeConnections(self):
        """Connect events in our UI"""
        self.reButton.clicked.connect(self.btnClicked)
        self.comboBox.currentTextChanged.connect(self.surfixItem)

    def surfixItem(self):
        """"""
        selectedText = self.comboBox.currentText()

        # print(f"hello {selectedText}")

        return selectedText

    def btnClicked(self):
        sel = pm.selected()
        customName = self.reLineEdit.text()
        staName = self.startLineEdit.text()
        padName = self.padLineEdit.text()
        selText = self.surfixItem()

        if self.initial_numName is None or staName or padName:
            try:
                self.initial_numName = staName.zfill(int(padName))
            except:
                self.initial_numName = staName

        numName = self.initial_numName  # ex) 1001 or 001

        for obj in sel:
            preName = pm.rename(obj, f"{customName}_{numName}{selText}")
            numName = self.increment_numName(numName)  # Increment numName for the next object


    def increment_numName(self, numName):
        """
        Increment the numName in the format "000X"
        """
        num = int(numName)                      # ex) int(1001) = 1001, int(001) = 1
        num += 1                                # ex) 1002       , 2
        return str(num).zfill(len(numName))     # ex) 1002       , 002
