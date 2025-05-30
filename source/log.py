import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout,
    QLineEdit, QPushButton, QHBoxLayout, QCheckBox, QMessageBox
)
from PySide6.QtCore import Qt
from consql import DatabaseConnector
from work import Work
from forgot_password import ForgotPasswordWindow

class Log_in(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.setGeometry(650, 300, 200, 250)

        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(12)
        layout.setContentsMargins(25, 25, 25, 25)

        l = QLabel("LOG IN", self)
        font = l.font()
        font.setPointSize(25)
        l.setFont(font)
        l.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(l)

        self.username = QLineEdit(self)
        self.username.setPlaceholderText("Username")
        layout.addWidget(self.username)

        self.password = QLineEdit(self)
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password)

        self.show_password_checkbox = QCheckBox("Show password", self)
        self.show_password_checkbox.toggled.connect(self.toggle_password_visibility)
        layout.addWidget(self.show_password_checkbox)

        self.login_btn = QPushButton("Login", self)
        layout.addWidget(self.login_btn)
        self.login_btn.clicked.connect(self.handle_login)

        forgot_layout = QHBoxLayout()
        forgot_layout.addStretch()
        self.forgot_btn = QPushButton("Forgot password?", self)
        self.forgot_btn.setFlat(True)
        self.forgot_btn.setStyleSheet("QPushButton { color: #007bff; text-decoration: underline; border: none; background: none; }")
        self.forgot_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.forgot_btn.clicked.connect(self.open_forgot_password)
        forgot_layout.addWidget(self.forgot_btn)
        forgot_layout.addStretch()
        layout.addLayout(forgot_layout)

        register_layout = QHBoxLayout()
        register_layout.addStretch()
        self.register_btn = QPushButton("Register", self)
        self.register_btn.setFlat(True)
        self.register_btn.setStyleSheet("QPushButton { color: #28a745; text-decoration: underline; border: none; background: none; }")
        self.register_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.register_btn.clicked.connect(self.open_register_form)
        register_layout.addWidget(self.register_btn)
        register_layout.addStretch()
        layout.addLayout(register_layout)

        self.setCentralWidget(central_widget)

    def toggle_password_visibility(self, checked):
        if checked:
            self.password.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password.setEchoMode(QLineEdit.EchoMode.Password)

    def handle_login(self):
        username = self.username.text()
        password = self.password.text()
        db = DatabaseConnector(database='basic_project')
        success = db.check(username, password)
        if success:
            QMessageBox.information(self, "Login Successful", f"Welcome, {username}!")
            db = DatabaseConnector()
            user_id = db.get_user_id(username)
            self.workingframe = Work(user_id)
            self.workingframe.show()
            self.hide()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

    def open_forgot_password(self):
        self.forgot_form = ForgotPasswordWindow()
        self.forgot_form.show()

    def open_register_form(self):
        from regist import RegisterForm
        self.register_form = RegisterForm()
        self.register_form.registration_successful.connect(self.on_registration_successful)
        self.register_form.show()
        self.hide()

    def on_registration_successful(self):
        self.show()
        QMessageBox.information(self, "Registration Complete", "Registration successful! Please log in.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Log_in()
    window.show()
    app.exec()