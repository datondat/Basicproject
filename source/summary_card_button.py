from PySide6.QtWidgets import QPushButton

class SummaryCardButton(QPushButton):
    def __init__(self, title, amount, color):
        super().__init__(f"{title}\n{amount}")
        self.setFixedHeight(70)
        self.setStyleSheet(f"""
            QPushButton {{
                background: {color};
                border-radius: 16px;
                border: none;
                color: #fff;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
            }}
            QPushButton:hover {{
                background: #24c1b4;
            }}
        """)