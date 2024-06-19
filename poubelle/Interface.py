from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QWidget, QGraphicsOpacityEffect, QLabel, QHBoxLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QPropertyAnimation, Qt
from datetime import datetime

class HoverButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.effect)
        self.animation = QPropertyAnimation(self.effect, b"opacity")



    def enterEvent(self, event):
        self.animation.stop()
        self.animation.setDuration(500)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0.5)
        self.animation.start()

    def leaveEvent(self, event):
        self.animation.stop()
        self.animation.setDuration(500)
        self.animation.setStartValue(0.5)
        self.animation.setEndValue(1)
        self.animation.start()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 150)
        self.setWindowOpacity(0.9)
        self.setWindowTitle('Reception')

        self.setStyleSheet("background-color: #2c3e50;")  

        self.widget = QWidget()
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)

        self.label = QLabel("Veuillez entrer votre nom :")
        self.label.setStyleSheet("color: white; font-size: 16px;")
        self.layout.addWidget(self.label)
        self.label.move(50, 0)


        self.textbox = QLineEdit()
        self.textbox.setStyleSheet("background-color: white; border-radius: 10px; padding: 8px;") 
        self.layout.addWidget(self.textbox)

        button_layout = QHBoxLayout()

        self.enter_button = HoverButton("Entrer")
        self.enter_button.setFixedWidth(100) 
        self.enter_button.setFixedHeight(50)
        self.enter_button.clicked.connect(self.enter)
        self.enter_button.setStyleSheet("QPushButton {background-color: #27ae60; border-radius: 15px; color: white; font-weight: bold;} QPushButton:hover {background-color: #2ecc71;}")  # Style pour le bouton Entrer
        self.layout.addWidget(self.enter_button)

        self.exit_button = HoverButton("Sortir")
        self.exit_button.setFixedWidth(100)  
        self.exit_button.setFixedHeight(50)  
        self.exit_button.clicked.connect(self.exit)
        self.exit_button.setStyleSheet("QPushButton {background-color: #c0392b; border-radius: 15px; color: white; font-weight: bold;} QPushButton:hover {background-color: #e74c3c;}")  # Style pour le bouton Sortir
        self.layout.addWidget(self.exit_button)

        button_layout.addWidget(self.enter_button)
        button_layout.addWidget(self.exit_button)
        self.layout.addLayout(button_layout)


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
