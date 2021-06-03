import sys
from PyQt5.QtWidgets import QApplication, QWidget


from Pages.WelcomePage import WelcomePageUI
from Pages.RegressionPageUI import RegressionPageUI


class AppManager():
    def __init__(self):
        app = QApplication(sys.argv)
        self.ActivePage = WelcomePageUI()
        self.ActivePage.setupUi(self)
        sys.exit(app.exec_())

    def switch(self,newWindow,model):
        self.ActivePage.close()
        if(newWindow == "Regression"):
            self.ActivePage = RegressionPageUI()
        self.ActivePage.setupUi(self,model)

def load_app():
    appManager = AppManager()

load_app()
