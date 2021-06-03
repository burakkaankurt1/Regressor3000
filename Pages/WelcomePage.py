from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog,QGridLayout,QComboBox, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor
from Controllers.DataPreProcessing import DataPreProcessing

class WelcomePageUI(QWidget):
    def goRegressionPage(self):
        regressionPageModel = {
            "dataPreProcessor":self.dataPreProcessor
        }
        self.appManager.switch("Regression",regressionPageModel)

    def doRegressionOnClickHandler(self):
        if self.state["idColumn"] == self.state["yColumn"]:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Hata!")
            msg.setInformativeText("Aynı kolonları seçemezsiniz!")
            msg.setWindowTitle("Hata!")
            msg.exec_()
        else:
            self.dataPreProcessor.dropColumn(self.state["idColumn"])
            self.dataPreProcessor.extractYColumn(self.state["yColumn"])
            self.dataPreProcessor.findCategoricalAndDrop()
            self.dataPreProcessor.doRegression()
            self.goRegressionPage()

    def chooseDataSetButtonOnClickHandler(self):
        file = QFileDialog.getOpenFileName(self,"Veri Seti Seç","","Csv Files (*.csv)")
        fpath = file[0]
        self.dataPreProcessor = DataPreProcessing(fpath)
        columnList = self.dataPreProcessor.getColumns()
        self.chooseIdColumnCB.clear()
        self.chooseYColumnCB.clear()
        for column in columnList:
            self.chooseIdColumnCB.addItem(column)
            self.chooseYColumnCB.addItem(column)
        self.chooseIdColumnCB.addItem("None")
        self.chooseIdColumnCB.setEnabled(True)
        self.chooseYColumnCB.setEnabled(True)
        self.doRegressionBTN.setEnabled(True)


    def chooseIdColumnCBOnChangeHandler(self,value):
        self.state["idColumn"] = value

    def chooseYColumnCBOnChangeHandler(self,value):
        self.state["yColumn"] = value

    def setupUi(self,appManager):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Dikkat!")
        msg.setInformativeText("Bu uygulama, kategorik değişkenleri veri seti içerisinden çıkarmaktadır! Sadece sayısal değişkenler ile çalışmaktadır.!")
        msg.setWindowTitle("Uyarı!")
        msg.exec_()
        self.initState()
        self.appManager = appManager
        self.setWindowTitle("Welcome")
        self.setFixedWidth(300)
        self.setFixedHeight(150)
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.chooseDataSetButton = QPushButton("Veri Seti Yükle")
        self.chooseDataSetButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.chooseIdColumnCB = QComboBox()
        self.chooseIdColumnCB.setEnabled(False)
        self.chooseYColumnCB = QComboBox()
        self.chooseYColumnCB.setEnabled(False)
        self.doRegressionBTN = QPushButton("Regresyon Uygula")
        self.doRegressionBTN.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.doRegressionBTN.setEnabled(False)
        self.layout.addWidget(self.chooseDataSetButton)
        self.layout.addWidget(self.chooseIdColumnCB)
        self.layout.addWidget(self.chooseYColumnCB)
        self.layout.addWidget(self.doRegressionBTN)
        self.show()
        self.onUiSetted()

    def onUiSetted(self):
        self.chooseDataSetButton.clicked.connect(self.chooseDataSetButtonOnClickHandler)
        self.chooseIdColumnCB.currentTextChanged.connect(self.chooseIdColumnCBOnChangeHandler)
        self.chooseYColumnCB.currentTextChanged.connect(self.chooseYColumnCBOnChangeHandler)
        self.doRegressionBTN.clicked.connect(self.doRegressionOnClickHandler)

    def initState(self):
        self.state = {
            "idColumn":"",
            "yColumn":""
        }
