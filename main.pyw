import sys
sys.path.append('venv\Lib\site-packages')
import pyperclip as pc
from encrypter import *
from PyQt5.QtWidgets import QMessageBox

import sys

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()

N = 0x10FFFF


# offset
def get_int():
    offset = int(len(ui.lineEdit.text()))
    if offset > 9:
        return offset - 3
    elif 4 < offset < 10:
        return offset - 2
    else:
        return offset + 1


# ceasar
def coder(message, offset):
    return ''.join(chr((ord(ch) + offset) % N) for ch in message)


def decoder(message, offset):
    return ''.join(chr((ord(ch) - offset) % N) for ch in message)


# vigenere
def vigenere(text: str, key: str, encrypt=True):
    result = ''
    for i in range(len(text)):
        letter_n = ord(text[i])
        key_n = ord(key[i % len(key)])
        if encrypt:
            value = (letter_n + key_n) % N
        else:
            value = (letter_n - key_n) % N
        result += chr(value)
    return result


def vigenere_coder(text: str, key: str):
    return vigenere(text=text, key=key, encrypt=True)


def vigenere_decoder(text: str, key: str):
    return vigenere(text=text, key=key, encrypt=False)


# popup
def popup():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText("Please enter your keyword")
    msg.setInformativeText("Keyword field cannot be empty")
    msg.setWindowTitle("Error")
    msg.exec_()


# encrypter
def encrypter():
    try:
        keyword = ui.lineEdit.text()
        offset = get_int()
        message_decoder = ui.plainTextEdit.toPlainText()
        if ui.radioButton.isChecked():
            ceasar = coder(message_decoder, offset)
            message = (vigenere_coder(ceasar, keyword))
            ui.plainTextEdit.setPlainText(message)
        else:
            vigenere = vigenere_decoder(message_decoder, keyword)
            message = (decoder(vigenere, offset))
            ui.plainTextEdit.setPlainText(message)
    except ZeroDivisionError:
        popup()
        ui.lineEdit.setText("keyword")


ui.pushButton.clicked.connect(encrypter)
ui.pushButton.setShortcut("Ctrl+Return")

# copy
ui.pushButton_3.clicked.connect(
    lambda: pc.copy(ui.plainTextEdit.toPlainText()))

# reset
ui.pushButton_2.clicked.connect(lambda: ui.plainTextEdit.clear())

sys.exit(app.exec_())
