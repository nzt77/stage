<<<<<<< HEAD
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QWidget
from datetime import datetime

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle('Reception')

        self.widget = QWidget()
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)

        self.textbox = QLineEdit()
        self.layout.addWidget(self.textbox)

        self.enter_button = QPushButton("Entrer")
        self.enter_button.clicked.connect(self.enter)
        self.layout.addWidget(self.enter_button)

        self.exit_button = QPushButton("Sortir")
        self.exit_button.clicked.connect(self.exit)
        self.layout.addWidget(self.exit_button)

        self.setCentralWidget(self.widget)

    def enter(self):
        self.log_action("entre")

    def exit(self):
        self.log_action("sorti")

    def log_action(self, action):
        name = self.textbox.text()
        time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        with open("log.txt", "a") as file:
            file.write(f"{name}, {action}, {time}\n")
=======
from PyQt6.QtWidgets import QApplication, QMainWindow
>>>>>>> 9b915e9c084e31b39eb3b10fb3e9cbc97297ed10

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
