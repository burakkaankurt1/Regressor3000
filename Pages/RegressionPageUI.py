from PyQt5.QtWidgets import QMessageBox,QWidget,QLineEdit , QLabel,QGroupBox , QPushButton, QVBoxLayout, QWidget, QFileDialog,QGridLayout,QComboBox, QHBoxLayout, QFormLayout, QScrollArea
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor

class RegressionPageUI(QWidget):

    def predictY(self):
        inputList = []
        for inputBox in self.inputList:
            try:
                inputList.append(float(inputBox.text()))
            except:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Hata!")
                msg.setInformativeText("Lütfen sayısal değerler girin!")
                msg.setWindowTitle("Hata!")
                msg.exec_()
                return
        predictionVal = self.dataPreprocessor.predict(inputList)
        self.plabel.setText(str(round(predictionVal,2)) + " Birim")

    def renderInputs(self):
        self.myForm = QFormLayout()
        self.labelList = []
        self.inputList = []
        self.myGroupBox = QGroupBox()
        for index,column in enumerate(self.dataPreprocessor.getColumns(),start=0):
            self.labelList.append(QLabel(column))
            self.inputList.append(QLineEdit())
            self.myForm.addRow(self.labelList[index],self.inputList[index])
        self.myGroupBox.setLayout(self.myForm)
        self.scrollArea.setWidget(self.myGroupBox)

    def setupUi(self,appManager,model):
        self.appManager = appManager
        self.dataPreprocessor = model["dataPreProcessor"]

        self.setWindowTitle("Regresyon")
        self.setFixedWidth(700)
        self.setFixedHeight(400)

        self.hlayout = QHBoxLayout()
        self.scrollArea = QScrollArea()
        self.scrollArea.setFixedWidth(400)

        self.predictButton = QPushButton()
        self.predictButton.setText("Tahmin et")

        self.vlayout = QVBoxLayout()
        self.plabel = QLabel("0")
        self.vlayout.addWidget(self.predictButton)
        self.vlayout.addWidget(self.plabel)

        self.hlayout.addWidget(self.scrollArea)
        self.hlayout.addLayout(self.vlayout)
        self.setLayout(self.hlayout)
        self.show()
        self.onUiSetted()

    def onUiSetted(self):
        self.renderInputs()
        self.predictButton.clicked.connect(self.predictY)

