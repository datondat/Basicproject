from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from summary_card import SummaryCard
from PySide6.QtCore import Qt

class MonthSummaryWidget(QWidget):
    def __init__(self, month_label, card_totals):
        super().__init__()
        top_layout = QVBoxLayout(self)
        top_layout.setSpacing(10)
        top_layout.setContentsMargins(0, 0, 0, 0)

        lbl_month = QLabel(f"{month_label} Summary")
        lbl_month.setStyleSheet("font-size: 20px; color: #36d1c4; font-weight: bold;")
        lbl_month.setAlignment(Qt.AlignmentFlag.AlignLeft)
        top_layout.addWidget(lbl_month)

        from PySide6.QtWidgets import QFrame  # Only used here

        self.balance_widget = QFrame()
        self.balance_widget.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #36d1c4, stop:1 #5bdfb6);
                border-radius: 32px;
            }
        """)
        balance_layout = QVBoxLayout(self.balance_widget)
        balance_layout.setContentsMargins(24, 20, 24, 20)
        balance_layout.setSpacing(6)
        lbl_balance_title = QLabel("Total Balance")
        lbl_balance_title.setStyleSheet("font-size: 20px; color: #fff;")
        lbl_balance_amount = QLabel(f"{card_totals['balance']:,.0f} VND")
        lbl_balance_amount.setStyleSheet("font-size: 36px; color: #fff; font-weight: bold;")
        balance_layout.addWidget(lbl_balance_title)
        balance_layout.addWidget(lbl_balance_amount)
        top_layout.addWidget(self.balance_widget)

        row_widget = QWidget()
        row_layout = QHBoxLayout(row_widget)
        row_layout.setSpacing(12)
        card_data = [
            ("Income", f"+ {card_totals['Income']:,.0f} VND", "#64b6f7"),
            ("Expense", f"- {card_totals['Expense']:,.0f} VND", "#f66d6d"),
            ("Other", f"{card_totals['Other']:,.0f} VND", "#f2c94c"),
        ]
        for title, amount, color in card_data:
            card = SummaryCard(title, amount, color)
            card.setFixedHeight(70)
            card.setFixedWidth(100)
            row_layout.addWidget(card)
        top_layout.addWidget(row_widget)