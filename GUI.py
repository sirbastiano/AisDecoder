import sys
from PyQt5.QtWidgets import QWidget, QApplication


class MainWindow(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("ARGO - AIS Decoder")


app = QApplication(sys.argv)

main_window = MainWindow()
main_window.show()

sys.exit(app.exec_())