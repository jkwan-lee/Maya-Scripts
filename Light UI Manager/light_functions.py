from PySide2 import QtGui, QtUiTools, QtCore, QtWidgets
import pymel.core as pm
import maya.cmds as mc
import mtoa.utils as mutil

def choose_color(args):
    color = QtWidgets.QColorDialog.getColor()
    if color.isValid():
        rgb_color = color.getRgbF()[:3]
        selected_light = pm.selected()
        if selected_light:
            pm.setAttr(selected_light[0] + ".color", rgb_color[0], rgb_color[1], rgb_color[2], type="double3")


def update_sample_value(args):
    saLienEdit = float(args.sampleLineEdit.text())

    if saLienEdit <= 10:
        args.sample_slider.setValue(saLienEdit)
    else:
        args.sample_slider.setRange(0, saLienEdit * 2)
        args.sample_slider.setValue(saLienEdit)


def update_sample_label(args, value):
    sample = value
    selected_light = pm.selected()
    if selected_light:
        args.sample_label.setText(f"Samples: {sample:.0f}")
        pm.setAttr(selected_light[0] + ".aiSamples", args.sample_slider.value())


def update_exposure_value(args):
    exLienEdit = float(args.exposureLineEdit.text())

    if exLienEdit <= 10:
        args.exposure_slider.setValue(exLienEdit)
    else:
        args.exposure_slider.setRange(0, exLienEdit * 2)
        args.exposure_slider.setValue(exLienEdit)


def update_exposure_label(args, value):
    exposure = value
    selected_light = pm.selected()
    if selected_light:
        args.exposure_label.setText(f"Exposure: {exposure:.2f}")
        pm.setAttr(selected_light[0]+ ".aiExposure", args.exposure_slider.value())


def update_intensity_value(args):
    intenLienEdit = float(args.intensityLineEdit.text())

    if intenLienEdit <= 10:
        args.intensity_slider.setValue(intenLienEdit)
    else:
        args.intensity_slider.setRange(0, intenLienEdit * 2)
        args.intensity_slider.setValue(intenLienEdit)


def update_intensity_label(args, value):
    intensity = value
    selected_light = pm.selected()
    if selected_light:
        args.intensity_label.setText(f"Intensity: {intensity:.2f}")
        pm.setAttr(selected_light[0] + ".intensity", args.intensity_slider.value())


