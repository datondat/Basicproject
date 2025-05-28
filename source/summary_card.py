from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from MarqueeLabel import MarqueeLabel

class SummaryCard(QFrame):
    def __init__(self, title, amount, color):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet(f"""
            QFrame {{
                background: {color};
                border-radius: 16px;
                border: none;
            }}
        """)
        layout = QVBoxLayout(self)
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("font-size: 14px; color: #fff;")
        layout.addWidget(lbl_title)
        lbl_amount = MarqueeLabel(amount)
        layout.addWidget(lbl_amount)