
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys
import autorization
import register
import login
import kabinet
from users import users
from cypher import *

FPS = 144

WIDTH, HEIGHT = 1000, 800
ROWS, COLS = 8, 10
SQUARE_SIZE = WIDTH//COLS



def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col
global input_log, input_pass, xor

app = QApplication(sys.argv)


def open_main():
    global main_window
    global main_ui
    main_window = QMainWindow()
    main_ui = autorization.Ui_MainWindow()
    main_ui.setupUi(main_window)
    main_window.show()
    main_ui.pushButton.clicked.connect(open_auth)
    main_ui.pushButton_2.clicked.connect(open_reg)


def open_auth():
    global auth_window
    global auth_ui
    main_window.close()
    auth_window = QMainWindow()
    auth_ui = login.Ui_authorization()
    auth_ui.setupUi(auth_window)
    auth_window.show()
    auth_ui.loginbtn.clicked.connect(handle_auth)


def open_reg():
    global reg_window
    global reg_ui
    main_window.close()
    reg_window = QMainWindow()
    reg_ui = register.Ui_registration()
    reg_ui.setupUi(reg_window)
    reg_window.show()
    reg_ui.regbtn.clicked.connect(handle_reg)


def handle_reg():
    user = {"login": reg_ui.new_login.text(), "password": reg_ui.new_pass.text()}
    user = vigenere_encrypt(str(user), key)
    nickname = reg_ui.new_login.text()
    if len(nickname) > 12:
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Ошибка")
        msgBox.setText("Длина никнейма превысила 12 символов")
        msgBox.exec()
    elif len(nickname) == 0:
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Ошибка")
        msgBox.setText("Ничего не введено")
        msgBox.exec()
    else:
        if user in users:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Ошибка")
            msgBox.setText("Такой аккаунт уже зарегестрирован")
            msgBox.exec()
        else:
            users.append(user)
            print(users)
            open_kab()
            reg_window.close()


def handle_auth():
    user = {"login": auth_ui.input_login.text(), "password": auth_ui.input_password.text()}
    user = vigenere_encrypt(str(user), key)
    if user in users:
        open_kab()
        auth_window.close()
    else:
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Ошибка")
        msgBox.setText("Вы ввели неправильный логин или пароль")
        msgBox.exec()

def open_kab():
    global kab_window
    global kab_ui
    kab_window = QMainWindow()
    kab_ui = kabinet.Ui_kabinet()
    kab_ui.setupUi(kab_window)
    kab_ui.kabplay.clicked.connect(show_play)
    kab_ui.kabstats.clicked.connect(show_stats)
    kab_ui.exitkab.clicked.connect(exit_click)
    kab_window.show()


def show_play():
    kab_ui.stackedWidget.setCurrentWidget(kab_ui.play_window)


def show_stats():
    kab_ui.stackedWidget.setCurrentWidget(kab_ui.stats_window)


def exit_click():
    kab_window.close()
    main_window.show()


open_main()



app.exec()