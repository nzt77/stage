import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout

class LoginApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.label1 = QLabel('Username', self)
        self.username_input = QLineEdit(self)
        self.label2 = QLabel('Password', self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_button = QPushButton('Login', self)
        self.register_button = QPushButton('Register', self)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label1)
        vbox.addWidget(self.username_input)
        vbox.addWidget(self.label2)
        vbox.addWidget(self.password_input)

        hbox = QHBoxLayout()
        hbox.addWidget(self.login_button)
        hbox.addWidget(self.register_button)

        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.setWindowTitle('Simple Login/Register Interface')
        self.setGeometry(100, 100, 300, 200)

def main():
    app = QApplication(sys.argv)
    window = LoginApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
