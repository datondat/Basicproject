import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout,
    QLineEdit, QPushButton, QHBoxLayout, QCheckBox
)
from PySide6.QtCore import Qt,Signal
from work import Work

class Register(QMainWindow):
    ok_clicked = Signal()
    signup_clicked=Signal()
    def __init__(self):
        super().__init__()

        self.setWindowTitle("dialog")
        self.setGeometry(650, 300, 300, 100)

        central_widget=QWidget(self)
        layout=QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(12)
        layout.setContentsMargins(12,12,12,12)

        l=QLabel("This account is not exist, check your account again or sign up!!")
        font = l.font()
        font.setPointSize(12)
        l.setFont(font)
        l.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(l)

        btl=QHBoxLayout()
        btl.setSpacing(10)
        btl.setContentsMargins(5,5,5,5)

        b=QPushButton("OK")
        b.clicked.connect(self.ok_pressed)
        b1=QPushButton("Sign up")
        b1.clicked.connect(self.sign_up_pressed)

        btl.addWidget(b)
        btl.addWidget(b1)

        layout.addLayout(btl)

        self.setCentralWidget(central_widget)
    def ok_pressed(self):
        self.ok_clicked.emit()
        self.close()

    def sign_up_pressed(self):
        self.signup_clicked.emit()
        self.close()

class RegisterForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register")
        self.setGeometry(400, 300, 200, 300)
        cw = QWidget(self)
        layout = QVBoxLayout(cw)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(12)
        layout.setContentsMargins(12, 12, 12, 12)

        l = QLabel("Register")
        font = l.font()
        font.setPointSize(24)
        l.setFont(font)
        l.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(l)

        self.name = QLineEdit()
        self.name.setPlaceholderText("Full name")
        layout.addWidget(self.name)

        self.user = QLineEdit()
        self.user.setPlaceholderText("User name")
        layout.addWidget(self.user)

        self.pwd = QLineEdit()
        self.pwd.setPlaceholderText("Password")
        self.pwd.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.pwd)

        self.email = QLineEdit()
        self.email.setPlaceholderText("Gmail")
        layout.addWidget(self.email)

        self.submit=QPushButton("Sign up")
        self.submit.setFixedSize(100, 20)
        layout.addWidget(self.submit, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.submit.clicked.connect(self.working_frame)


        self.setCentralWidget(cw)

    def working_frame(self):
        self.working_frame = Work()
        self.working_frame.show()
        self.close()