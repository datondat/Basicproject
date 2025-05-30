from PySide6.QtWidgets import (
    QMainWindow, QLabel, QWidget, QVBoxLayout,
    QLineEdit, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt
from consql import DatabaseConnector

class ForgotPasswordWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Forgot Password")
        self.setGeometry(400, 300, 300, 220)
        cw = QWidget(self)
        layout = QVBoxLayout(cw)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(12)
        layout.setContentsMargins(12, 12, 12, 12)

        l = QLabel("Forgot Password")
        font = l.font()
        font.setPointSize(24)
        l.setFont(font)
        l.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(l)

        self.user = QLineEdit()
        self.user.setPlaceholderText("User name")
        layout.addWidget(self.user)

        self.email = QLineEdit()
        self.email.setPlaceholderText("Registered email")
        layout.addWidget(self.email)

        self.new_pwd = QLineEdit()
        self.new_pwd.setPlaceholderText("New password")
        self.new_pwd.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.new_pwd)

        self.submit = QPushButton("Reset Password")
        self.submit.setFixedSize(140, 30)
        layout.addWidget(self.submit, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.submit.clicked.connect(self.reset_password)

        self.setCentralWidget(cw)

    def reset_password(self):
        logname = self.user.text().strip()
        mail = self.email.text().strip()
        new_pass = self.new_pwd.text().strip()
        if not logname or not mail or not new_pass:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return

        db = DatabaseConnector()
        try:
            db.cursor.execute(
                "SELECT * FROM users WHERE logname=%s AND mail=%s",
                (logname, mail)
            )
            user = db.cursor.fetchone()
            if not user:
                QMessageBox.critical(self, "Error", "No user found with that username and email.")
                return

            db.cursor.execute(
                "UPDATE users SET pass=%s WHERE logname=%s AND mail=%s",
                (new_pass, logname, mail)
            )
            db.conn.commit()
            QMessageBox.information(self, "Success", "Password has been reset successfully.")
            self.close()
        finally:
            db.close()