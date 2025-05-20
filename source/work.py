import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout,
    QHBoxLayout, QFrame
)
from PySide6.QtCore import Qt

class Card(QFrame):
    def __init__(self, title, description):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("QFrame { background: #f8f8fa; border-radius: 10px; border: 1px solid #dcdcdc; }")
        layout = QVBoxLayout()
        label_title = QLabel(title)
        label_title.setStyleSheet("font-weight: bold; font-size: 16px;")
        label_desc = QLabel(description)
        label_desc.setWordWrap(True)
        layout.addWidget(label_title)
        layout.addWidget(label_desc)
        self.setLayout(layout)

class Work(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Manage")
        self.setGeometry(500, 200, 400, 500)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Create 4 cards
        cards_data = [
            ("Card 1", "Description for card 1."),
            ("Card 2", "Description for card 2."),
            ("Card 3", "Description for card 3."),
            ("Card 4", "Description for card 4."),
        ]

        for title, desc in cards_data:
            card = Card(title, desc)
            card.setFixedHeight(80)
            main_layout.addWidget(card)
