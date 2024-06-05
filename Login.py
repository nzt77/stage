import sys
import requests
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox

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

    def show_message(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec()

    def on_login(self):
        data = {
            'username': self.username_input.text(),
            'password': self.password_input.text()
        }
        response = requests.post('http://127.0.0.1:8000/login', json=data)
        if response.status_code == 200:
            self.show_message("Success", "Connexion réussie")
        else:
            self.show_message("Error", response.json().get("detail", "Erreur inconnue"))

    def on_register(self):
        data = {
            'username': self.username_input.text(),
            'password': self.password_input.text()
        }
        response = requests.post('http://127.0.0.1:8000/register', json=data)
        if response.status_code == 200:
            self.show_message("Success", "Utilisateur créé avec succès")
        else:
            self.show_message("Error", response.json().get("detail", "Erreur inconnue"))

def main():
    app = QApplication(sys.argv)
    window = SimpleApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
