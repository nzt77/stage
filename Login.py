import sys
import requests
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout

class SimpleApp(QWidget):
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

        self.login_button.clicked.connect(self.on_login)
        self.register_button.clicked.connect(self.on_register)

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

    def on_login(self):
        data = {
            'username': self.username_input.text(),
            'password': self.password_input.text()
        }
        response = requests.post('http://127.0.0.1:8000/login', json=data)
        print(response.json())

    def on_register(self):
        data = {
            'username': self.username_input.text(),
            'password': self.password_input.text()
        }
        response = requests.post('http://127.0.0.1:8000/register', json=data)
        print(response.json())

def main():
    app = QApplication(sys.argv)
    window = SimpleApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
