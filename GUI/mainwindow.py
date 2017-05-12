# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(421, 472)


        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())


        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(421, 472))
        MainWindow.setMaximumSize(QtCore.QSize(421, 472))
        MainWindow.setDocumentMode(False)


        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")


        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(90, 60, 231, 191))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")

        self.horizontalSlider_1 = QtWidgets.QSlider(self.verticalLayoutWidget)
        self.horizontalSlider_1.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_1.setObjectName("horizontalSlider_1")
        self.horizontalSlider_1.setRange(0,255)
        self.verticalLayout.addWidget(self.horizontalSlider_1)

        self.horizontalSlider_2 = QtWidgets.QSlider(self.verticalLayoutWidget)
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.horizontalSlider_2.setRange(0,255)
        self.verticalLayout.addWidget(self.horizontalSlider_2)

        self.horizontalSlider_3 = QtWidgets.QSlider(self.verticalLayoutWidget)
        self.horizontalSlider_3.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_3.setObjectName("horizontalSlider_3")
        self.horizontalSlider_3.setRange(0,255)
        self.verticalLayout.addWidget(self.horizontalSlider_3)

        self.horizontalSlider_4 = QtWidgets.QSlider(self.verticalLayoutWidget)
        self.horizontalSlider_4.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_4.setObjectName("horizontalSlider_4")
        self.horizontalSlider_4.setRange(0,255)
        self.verticalLayout.addWidget(self.horizontalSlider_4)

        self.horizontalSlider_5 = QtWidgets.QSlider(self.verticalLayoutWidget)
        self.horizontalSlider_5.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_5.setObjectName("horizontalSlider_5")
        self.horizontalSlider_5.setRange(0,255)
        self.verticalLayout.addWidget(self.horizontalSlider_5)

        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralWidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(20, 60, 71, 191))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")


        self.label_1 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_1.setObjectName("label_1")
        self.verticalLayout_2.addWidget(self.label_1)

        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)

        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)

        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)

        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)





        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.centralWidget)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(320, 60, 71, 191))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_3.setSpacing(6)

        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lcdNumber_1 = QtWidgets.QLCDNumber(self.verticalLayoutWidget_3)
        self.lcdNumber_1.setObjectName("lcdNumber_1")
        self.verticalLayout_3.addWidget(self.lcdNumber_1)

        self.lcdNumber_2 = QtWidgets.QLCDNumber(self.verticalLayoutWidget_3)
        self.lcdNumber_2.setObjectName("lcdNumber_2")
        self.verticalLayout_3.addWidget(self.lcdNumber_2)

        self.lcdNumber_3 = QtWidgets.QLCDNumber(self.verticalLayoutWidget_3)
        self.lcdNumber_3.setObjectName("lcdNumber_3")
        self.verticalLayout_3.addWidget(self.lcdNumber_3)

        self.lcdNumber_4 = QtWidgets.QLCDNumber(self.verticalLayoutWidget_3)
        self.lcdNumber_4.setObjectName("lcdNumber_4")
        self.verticalLayout_3.addWidget(self.lcdNumber_4)

        self.lcdNumber_5 = QtWidgets.QLCDNumber(self.verticalLayoutWidget_3)
        self.lcdNumber_5.setObjectName("lcdNumber_5")
        self.verticalLayout_3.addWidget(self.lcdNumber_5)




        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.centralWidget)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(80, 270, 111, 111))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_4.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        self.checkBox_1 = QtWidgets.QCheckBox(self.verticalLayoutWidget_4)
        self.checkBox_1.setObjectName("checkBox_1")
        self.verticalLayout_4.addWidget(self.checkBox_1)

        self.checkBox_2 = QtWidgets.QCheckBox(self.verticalLayoutWidget_4)
        self.checkBox_2.setObjectName("checkBox_2")
        self.verticalLayout_4.addWidget(self.checkBox_2)

        self.checkBox_3 = QtWidgets.QCheckBox(self.verticalLayoutWidget_4)
        self.checkBox_3.setObjectName("checkBox_3")
        self.verticalLayout_4.addWidget(self.checkBox_3)

        self.checkBox_4 = QtWidgets.QCheckBox(self.verticalLayoutWidget_4)
        self.checkBox_4.setObjectName("checkBox_4")
        self.verticalLayout_4.addWidget(self.checkBox_4)



        self.verticalLayoutWidget_5 = QtWidgets.QWidget(self.centralWidget)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(230, 270, 111, 111))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_5.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setObjectName("verticalLayout_5")

        self.checkBox_5 = QtWidgets.QCheckBox(self.verticalLayoutWidget_5)
        self.checkBox_5.setObjectName("checkBox_5")
        self.verticalLayout_5.addWidget(self.checkBox_5)

        self.checkBox_6 = QtWidgets.QCheckBox(self.verticalLayoutWidget_5)
        self.checkBox_6.setObjectName("checkBox_6")
        self.verticalLayout_5.addWidget(self.checkBox_6)

        self.checkBox_7 = QtWidgets.QCheckBox(self.verticalLayoutWidget_5)
        self.checkBox_7.setObjectName("checkBox_7")
        self.verticalLayout_5.addWidget(self.checkBox_7)

        self.checkBox_8 = QtWidgets.QCheckBox(self.verticalLayoutWidget_5)
        self.checkBox_8.setObjectName("checkBox_8")
        self.verticalLayout_5.addWidget(self.checkBox_8)

        self.label_tittle = QtWidgets.QLabel(self.centralWidget)
        self.label_tittle.setGeometry(QtCore.QRect(50, 10, 321, 31))
        self.label_tittle.setObjectName("label_tittle")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 421, 21))
        self.menuBar.setObjectName("menuBar")
        self.menuMain = QtWidgets.QMenu(self.menuBar)
        self.menuMain.setObjectName("menuMain")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionHelp = QtWidgets.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuMain.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)
        self.menuBar.addAction(self.menuMain.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_1.setText(_translate("MainWindow", "Upper"))
        self.label_2.setText(_translate("MainWindow", "Lower"))
        self.label_3.setText(_translate("MainWindow", "Thresh"))
        self.label_4.setText(_translate("MainWindow", "Min Line Size"))
        self.label_5.setText(_translate("MainWindow", "Label5"))
        self.checkBox_1.setText(_translate("MainWindow", "CheckBox"))
        self.checkBox_2.setText(_translate("MainWindow", "CheckBox"))
        self.checkBox_3.setText(_translate("MainWindow", "CheckBox"))
        self.checkBox_4.setText(_translate("MainWindow", "CheckBox"))
        self.checkBox_5.setText(_translate("MainWindow", "CheckBox"))
        self.checkBox_6.setText(_translate("MainWindow", "CheckBox"))
        self.checkBox_7.setText(_translate("MainWindow", "CheckBox"))
        self.checkBox_8.setText(_translate("MainWindow", "CheckBox"))
        self.label_tittle.setText(_translate("MainWindow", ".................."))
        self.menuMain.setTitle(_translate("MainWindow", "Main"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionHelp.setText(_translate("MainWindow", "Help"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionAbout.setText(_translate("MainWindow", "About"))

