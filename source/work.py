import sys

from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout,
    QLineEdit, QPushButton, QHBoxLayout, QCheckBox, QFrame, QStackedLayout, QSizePolicy
)
from PySide6.QtCore import Qt,Signal


class SummaryCard(QFrame):
    def __init__(self, title, amount, color):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet(f"""
            QFrame {{
                background: {color};
                border-radius: 16px;
                border: none;
                margin-bottom: 4px;
            }}
        """)
        layout = QVBoxLayout(self)
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("font-size: 14px; color: #ffffff;")
        lbl_amount = QLabel(amount)
        lbl_amount.setStyleSheet("font-size: 20px; font-weight: bold; color: #ffffff;")
        layout.addWidget(lbl_title)
        layout.addWidget(lbl_amount)

class Work(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Money Manager")
        self.setGeometry(500, 200, 400, 730)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(10)

        # Top - Balance summary
        balance_card = QFrame()
        balance_card.setFrameShape(QFrame.StyledPanel)
        balance_card.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                           stop:0 #36d1c4, stop:1 #50c9c3);
                border-radius: 20px;
            }
        """)
        bal_layout = QVBoxLayout(balance_card)
        bal_layout.setContentsMargins(20, 16, 20, 16)
        bal_layout.setSpacing(6)
        lbl_balance = QLabel("Total Balance")
        lbl_balance.setStyleSheet("font-size: 16px; color: #e6f2f0;")
        lbl_balance_amt = QLabel("$2,340.00")
        lbl_balance_amt.setStyleSheet("font-size: 32px; font-weight: bold; color: #fff;")
        bal_layout.addWidget(lbl_balance)
        bal_layout.addWidget(lbl_balance_amt)
        main_layout.addWidget(balance_card)


        summary_cards = QHBoxLayout()
        summary_cards.setSpacing(12)
        card_data = [
            ("Income", "+ $3,000", "#64b6f7"),
            ("Expense", "- $660", "#f66d6d"),
            ("Other", "$0", "#f2c94c"),
        ]
        for title, amount, color in card_data:
            card = SummaryCard(title, amount, color)
            card.setFixedHeight(70)
            card.setFixedWidth(110)
            summary_cards.addWidget(card)
        main_layout.addLayout(summary_cards)

        self.stacked_layout = QStackedLayout()
        for page_name in ["Home", "Transactions", "Stats", "Settings"]:
            page = QWidget()
            page_layout = QVBoxLayout(page)
            label = QLabel(page_name)
            label.setAlignment(Qt.AlignCenter)
            label.setFont(QFont("Arial", 20, QFont.Bold))
            page_layout.addWidget(label)
            self.stacked_layout.addWidget(page)
        main_layout.addLayout(self.stacked_layout, stretch=1)

        # Floating Add Button
        btn_add = QPushButton("+")
        btn_add.setStyleSheet("""
            QPushButton {
                background-color: #36d1c4;
                color: #fff;
                border-radius: 30px;
                font-size: 32px;
                font-weight: bold;
                width: 60px; height: 60px;
                border: 4px solid #fff;
            }
            QPushButton:hover {
                background-color: #50c9c3;
            }
        """)
        btn_add.setFixedSize(60, 60)
        btn_add.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        float_btn_layout = QHBoxLayout()
        float_btn_layout.addStretch()
        float_btn_layout.addWidget(btn_add)
        float_btn_layout.addStretch()
        main_layout.addLayout(float_btn_layout)

        main_layout.addSpacing(12)

        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(0)
        nav_buttons = [
            ("Home", "🏠"),
            ("Transactions", "💳"),
            ("Add", ""),
            ("Stats", "📊"),
            ("Settings", "⚙️")
        ]
        for idx, (name, icon) in enumerate(nav_buttons):
            if name == "Add":
                nav_layout.addSpacing(70)
                continue
            btn = QPushButton(icon)
            btn.setFixedHeight(40)
            btn.setStyleSheet("""
                QPushButton {
                    color: #36d1c4;
                    background: transparent;
                    border: 2px solid #36d1c4;
                    border-radius: 16px;
                    font-size: 22px;
                    margin: 0 8px;
                }
                QPushButton:pressed {
                    color: #50c9c3;
                    border-color: #50c9c3;
                }
            """)
            btn.clicked.connect(lambda checked, i=idx if idx < 2 else idx - 1: self.stacked_layout.setCurrentIndex(i))
            nav_layout.addWidget(btn)
        main_layout.addLayout(nav_layout)