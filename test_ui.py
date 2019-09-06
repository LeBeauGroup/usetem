import sys
from PyQt5.QtWidgets import QDialog, QApplication
from useTEM_ui import Ui_Dialog

class AppWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.show()



if __name__ == '__main__':

    print('this')
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec_())