import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout,
    QLineEdit, QPushButton, QHBoxLayout, QCheckBox
)
from PySide6.QtCore import Qt

class Login1(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.setGeometry(650, 300, 200, 250)