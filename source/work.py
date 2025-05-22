from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout,
    QPushButton, QHBoxLayout, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt

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
        lbl_amount = QLabel(amount)
        lbl_amount.setStyleSheet("font-size: 20px; font-weight: bold; color: #fff;")
        layout.addWidget(lbl_title)
        layout.addWidget(lbl_amount)

class Work(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Money Manager")
        self.setGeometry(600, 200, 380, 700)  # Thinner window

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(16, 16, 16, 16)
        self.main_layout.setSpacing(10)

        # Top balance widget
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
        lbl_balance_amount = QLabel("$2,340.00")
        lbl_balance_amount.setStyleSheet("font-size: 36px; color: #fff; font-weight: bold;")
        balance_layout.addWidget(lbl_balance_title)
        balance_layout.addWidget(lbl_balance_amount)
        self.main_layout.addWidget(self.balance_widget)

        # --- Summary area (cards) ---
        self.summary_container = QVBoxLayout()
        self.summary_container.setSpacing(12)
        self.main_layout.addLayout(self.summary_container)

        # Initial row of three cards (Income, Expense, Other)
        row_widget = QWidget()
        row_layout = QHBoxLayout(row_widget)
        row_layout.setSpacing(12)
        card_data = [
            ("Income", "+ $3,000", "#64b6f7"),
            ("Expense", "- $660", "#f66d6d"),
            ("Other", "$0", "#f2c94c"),
        ]
        for title, amount, color in card_data:
            card = SummaryCard(title, amount, color)
            card.setFixedHeight(70)
            card.setFixedWidth(100)
            row_layout.addWidget(card)
        self.summary_container.addWidget(row_widget)

        # Filler for Home area (simulate your "Home" label)
        self.content_widget = QWidget()
        content_layout = QVBoxLayout(self.content_widget)
        content_layout.addStretch()
        lbl_home = QLabel("Home")
        lbl_home.setAlignment(Qt.AlignHCenter)
        lbl_home.setStyleSheet("font-size: 28px; color: #fff; font-weight: bold;")
        content_layout.addWidget(lbl_home)
        content_layout.addStretch()
        self.main_layout.addWidget(self.content_widget, 1)

        # --- Navigation bar with Add button and others ---
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(10)
        nav_layout.setContentsMargins(0, 10, 0, 0)

        # Home button
        self.btn_home = QPushButton("🏠")
        self.btn_home.setFixedSize(44, 44)
        self.btn_home.setStyleSheet("""
            QPushButton {
                border-radius: 14px;
                border: 2px solid #36d1c4;
                background: transparent;
                font-size: 22px;
            }
        """)
        self.btn_home.clicked.connect(self.on_home_clicked)
        nav_layout.addWidget(self.btn_home)

        # Transactions button
        self.btn_trans = QPushButton("💳")
        self.btn_trans.setFixedSize(44, 44)
        self.btn_trans.setStyleSheet("""
            QPushButton {
                border-radius: 14px;
                border: 2px solid #36d1c4;
                background: transparent;
                font-size: 22px;
            }
        """)
        self.btn_trans.clicked.connect(self.on_transactions_clicked)
        nav_layout.addWidget(self.btn_trans)

        # Add button (center)
        self.btn_add = QPushButton("+")
        self.btn_add.setFixedSize(56, 56)
        self.btn_add.setStyleSheet("""
            QPushButton {
                background-color: #36d1c4;
                color: #fff;
                border-radius: 28px;
                border: 4px solid #fff;
                font-size: 30px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #50c9c3;
            }
        """)
        self.btn_add.clicked.connect(self.add_summary_card)
        nav_layout.addWidget(self.btn_add)

        # Stats button
        self.btn_stats = QPushButton("📊")
        self.btn_stats.setFixedSize(44, 44)
        self.btn_stats.setStyleSheet("""
            QPushButton {
                border-radius: 14px;
                border: 2px solid #36d1c4;
                background: transparent;
                font-size: 22px;
            }
        """)
        self.btn_stats.clicked.connect(self.on_stats_clicked)
        nav_layout.addWidget(self.btn_stats)

        # Settings button
        self.btn_settings = QPushButton("⚙️")
        self.btn_settings.setFixedSize(44, 44)
        self.btn_settings.setStyleSheet("""
            QPushButton {
                border-radius: 14px;
                border: 2px solid #36d1c4;
                background: transparent;
                font-size: 22px;
            }
        """)
        self.btn_settings.clicked.connect(self.on_settings_clicked)
        nav_layout.addWidget(self.btn_settings)

        nav_layout.insertStretch(0, 1)
        nav_layout.addStretch(1)
        self.main_layout.addLayout(nav_layout)

    def add_summary_card(self):
        # The new card should have the same width as the window (minus margins)
        # Calculate width: window width - left/right margins
        window_width = self.geometry().width()
        # Get central widget margins
        left_margin, top_margin, right_margin, bottom_margin = self.main_layout.getContentsMargins()
        card_width = window_width - left_margin - right_margin
        if card_width < 50:  # fallback in case window is minimized
            card_width = 50
        card = SummaryCard("New Card", "$0", "#36d1c4")
        card.setFixedHeight(70)
        card.setFixedWidth(card_width)
        card.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.summary_container.addWidget(card)

    # --- Navigation button slot implementations ---
    def on_home_clicked(self):
        self.set_home_label("Home")

    def on_transactions_clicked(self):
        self.set_home_label("Transactions")

    def on_stats_clicked(self):
        self.set_home_label("Stats")

    def on_settings_clicked(self):
        self.set_home_label("Settings")

    def set_home_label(self, text):
        # Set the central label to the selected section
        for i in reversed(range(self.content_widget.layout().count())):
            widget = self.content_widget.layout().itemAt(i).widget()
            if isinstance(widget, QLabel):
                widget.setText(text)

    def resizeEvent(self, event):
        # When window is resized, also resize any new summary cards to match window width
        window_width = self.geometry().width()
        left_margin, top_margin, right_margin, bottom_margin = self.main_layout.getContentsMargins()
        card_width = window_width - left_margin - right_margin
        for i in range(self.summary_container.count()):
            w = self.summary_container.itemAt(i).widget()
            # Only resize single cards, not the first row (which is a QWidget with HBox)
            if isinstance(w, SummaryCard):
                w.setFixedWidth(card_width)
        super().resizeEvent(event)
