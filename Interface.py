#interface pyqt5

from PyQt6.QtWidgets import QApplication, QMainWindow

app = QApplication([])
window = QMainWindow()
window.setGeometry(100, 100, 600, 400) 
window.setWindowTitle('Interface Vide PyQt6')
window.show()
app.exec()
