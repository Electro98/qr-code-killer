import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget,QVBoxLayout, QPushButton, QTextEdit, QLabel


def Push_Button_file_dialog_funct(self):
    push_button_file_dialog = QPushButton()
    push_button_file_dialog.setText("Выбрать картинку")
    push_button_file_dialog.setMinimumSize(QtCore.QSize(100, 40))
    push_button_file_dialog.clicked.connect(self.file_dialog)
    self.vbox.addWidget(push_button_file_dialog)


#def text_edit_file_dialog_funct(self):
#    text_edit_file_dialog = QTextEdit()
#    text_edit_file_dialog.setMinimumSize(QtCore.QSize(400, 40))
#    self.text_edit_file_dialog = text_edit_file_dialog
#    self.vbox.addWidget(self.text_edit_file_dialog)



class MainWindowForFileDialog (QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.resize(500, 500)
        self.setWindowTitle("QR App")
        self.centralWidget = QWidget(self)
        self.centralWidget.resize(500, 500)
        self.vbox = QVBoxLayout(self.centralWidget)
        Push_Button_file_dialog_funct(self)
#        text_edit_file_dialog_funct(self)


    def file_dialog(self):
        dialog_name = "Выберите файл"
        folder_init_name = "/Users/yana/PycharmProjects/PythonApp"
        filename = QFileDialog.getOpenFileName(self, dialog_name, folder_init_name)
        self.text_edit_file_dialog.setText(str(filename))



def main():
    app = QApplication(sys.argv)
    main = MainWindowForFileDialog()
    main.show()
    app.exec_()


if __name__ == "__main__":
    main()