from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QWidget
from PyQt6.QtGui import QFont
from datetime import datetime

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 450, 300)
        self.setWindowTitle('Reception')

        self.setStyleSheet("background-color: #2c3e50;")  

        self.widget = QWidget()
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)

        self.textbox = QLineEdit()
        self.textbox.setStyleSheet("background-color: white; border-radius: 10px; padding: 8px;") 
        self.layout.addWidget(self.textbox)

        self.enter_button = QPushButton("Entrer")
        self.enter_button.setFixedWidth(100) 
        self.enter_button.setFixedHeight(50)
        self.enter_button.clicked.connect(self.enter)
        self.enter_button.setStyleSheet("QPushButton {background-color: #27ae60; border-radius: 15px; color: white; font-weight: bold;} QPushButton:hover {background-color: #2ecc71;}")  # Style pour le bouton Entrer
        self.layout.addWidget(self.enter_button)

        self.exit_button = QPushButton("Sortir")
        self.exit_button.setFixedWidth(100)  
        self.exit_button.setFixedHeight(50)  
        self.exit_button.clicked.connect(self.exit)
        self.exit_button.setStyleSheet("QPushButton {background-color: #c0392b; border-radius: 15px; color: white; font-weight: bold;} QPushButton:hover {background-color: #e74c3c;}")  # Style pour le bouton Sortir
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

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
