from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt

class EditCardDialog(QDialog):
    def __init__(self, entry, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Entry")
        self.entry = entry

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Title:"))
        self.title_edit = QLineEdit(entry['title'])
        layout.addWidget(self.title_edit)

        layout.addWidget(QLabel("Amount:"))
        self.amount_edit = QLineEdit(str(entry['money']))
        layout.addWidget(self.amount_edit)

        layout.addWidget(QLabel("Type:"))
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Income", "Expense", "Other"])
        self.type_combo.setCurrentText(entry['type'])
        layout.addWidget(self.type_combo)

        layout.addWidget(QLabel("Date (YYYY-MM-DD):"))
        self.date_edit = QLineEdit(str(entry['date']))
        layout.addWidget(self.date_edit)

        btns = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btns.addWidget(save_btn)
        btns.addWidget(cancel_btn)
        layout.addLayout(btns)

    def get_values(self):
        return {
            'id': self.entry['id'],
            'title': self.title_edit.text(),
            'money': self.amount_edit.text(),
            'type': self.type_combo.currentText(),
            'date': self.date_edit.text(),
        }