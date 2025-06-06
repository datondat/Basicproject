from PySide6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from work import Work
import os
from email_bot import EmailBot
from consql import DatabaseConnector

class RegisterForm(QMainWindow):
    registration_successful = Signal()

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

        self.email = QLineEdit()
        self.email.setPlaceholderText("Gmail")
        layout.addWidget(self.email)

        self.user = QLineEdit()
        self.user.setPlaceholderText("User name")
        layout.addWidget(self.user)

        self.pwd = QLineEdit()
        self.pwd.setPlaceholderText("Password")
        self.pwd.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.pwd)

        self.submit = QPushButton("Sign up")
        self.submit.setFixedSize(100, 20)
        layout.addWidget(self.submit, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.submit.clicked.connect(self.first)

        self.setCentralWidget(cw)

    def first(self):
        fullname = self.name.text()
        mail = self.email.text()
        username = self.user.text()
        password = self.pwd.text()
        try:
            if DatabaseConnector().addus(fullname, mail, username, password):
                bot = EmailBot(
                    smtp_server="smtp.gmail.com",
                    smtp_port=587,
                    bot_email=os.getenv("BOT_EMAIL"),
                    bot_password=os.getenv("BOT_APP_PASSWORD")
                )
                subject = "Welcome to MyApp!"
                message = f"Hello {fullname},\n\nYour registration was successful. Welcome to MyApp!"
                if bot.send(mail, subject, message):
                    QMessageBox.information(self, "Sign up Successful", f"Welcome, {username}!")
                    self.registration_successful.emit()
                    self.close()
                else:
                    QMessageBox.warning(self, "Email Failed",
                                        "Registration succeeded, but failed to send welcome email.")
            else:
                QMessageBox.warning(self, "Sign up Failed", "Registration failed. Try another username.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")