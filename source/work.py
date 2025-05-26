from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout,
    QPushButton, QHBoxLayout, QFrame, QSizePolicy, QScrollArea
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

class TopSummaryWidget(QWidget):
    def __init__(self):
        super().__init__()
        top_layout = QVBoxLayout(self)
        top_layout.setSpacing(10)
        top_layout.setContentsMargins(0, 0, 0, 0)

        # Balance widget
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
        top_layout.addWidget(self.balance_widget)

        # Summary cards row
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
        top_layout.addWidget(row_widget)

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

class Work(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Money Manager")
        self.resize(380, 700)

        # Central widget with main vertical layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.outer_layout = QVBoxLayout(central_widget)
        self.outer_layout.setContentsMargins(0, 0, 0, 0)
        self.outer_layout.setSpacing(0)

        # ----- Content area -----
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(16, 16, 16, 16)
        self.content_layout.setSpacing(10)
        self.outer_layout.addWidget(self.content_widget, 1)

        # ----- Navigation Bar -----
        self.nav_bar = QHBoxLayout()
        self.nav_bar.setSpacing(10)
        self.nav_bar.setContentsMargins(0, 10, 0, 10)

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
        self.nav_bar.addWidget(self.btn_home)

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
        self.nav_bar.addWidget(self.btn_stats)

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
        self.nav_bar.addWidget(self.btn_add)

        self.btn_graph = QPushButton("📈")
        self.btn_graph.setFixedSize(44, 44)
        self.btn_graph.setStyleSheet("""
            QPushButton {
                border-radius: 14px;
                border: 2px solid #36d1c4;
                background: transparent;
                font-size: 22px;
            }
        """)
        self.btn_graph.clicked.connect(self.on_graph_clicked)
        self.nav_bar.addWidget(self.btn_graph)

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
        self.nav_bar.addWidget(self.btn_settings)

        self.nav_bar.insertStretch(0, 1)
        self.nav_bar.addStretch(1)

        # Add nav bar at the bottom
        nav_bar_widget = QWidget()
        nav_bar_widget.setLayout(self.nav_bar)
        self.outer_layout.addWidget(nav_bar_widget, 0)

        # State for restoring Home
        self.home_widgets = []
        self.home_cards = []

        self.show_home()

    def clear_content(self):
        # Remove all widgets from content_layout (except for persistent nav bar)
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            widget = item.widget()
            layout = item.layout()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
            elif layout is not None:
                while layout.count():
                    child = layout.takeAt(0)
                    if child.widget():
                        child.widget().setParent(None)
                        child.widget().deleteLater()
                del layout

    def show_home(self):
        self.clear_content()
        self.home_widgets = []
        # Top summary always on top
        self.top_summary = TopSummaryWidget()
        self.content_layout.addWidget(self.top_summary)
        self.home_widgets.append(self.top_summary)

        # Scroll Area for summary cards (added with "+")
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.summary_scroll_content = QWidget()
        self.summary_container = QVBoxLayout(self.summary_scroll_content)
        self.summary_container.setSpacing(12)
        self.scroll_area.setWidget(self.summary_scroll_content)
        self.content_layout.addWidget(self.scroll_area, 1)
        self.home_widgets.append(self.scroll_area)

        # Restore cards if present
        for btn in self.home_cards:
            self.summary_container.addWidget(btn)

        # Home label/content (at bottom)
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.addStretch()
        lbl_home = QLabel("Home")
        lbl_home.setAlignment(Qt.AlignHCenter)
        lbl_home.setStyleSheet("font-size: 28px; color: #36d1c4; font-weight: bold;")
        content_layout.addWidget(lbl_home)
        content_layout.addStretch()
        self.content_layout.addWidget(content_widget)
        self.home_widgets.append(content_widget)

    def add_summary_card(self):
        # Only add if summary_container exists (home is showing)
        if hasattr(self, "summary_container"):
            scroll_width = self.scroll_area.viewport().width() if hasattr(self, "scroll_area") else self.width()
            left_margin, _, right_margin, _ = self.content_layout.getContentsMargins()
            card_width = max(scroll_width - left_margin - right_margin, 100)
            btn = SummaryCardButton("New Card", "$0", "#36d1c4")
            btn.setFixedWidth(card_width)
            btn.clicked.connect(lambda: self.show_message("Card button clicked!"))
            self.summary_container.addWidget(btn)
            self.home_cards.append(btn)

    def on_home_clicked(self):
        self.show_home()

    def on_stats_clicked(self):
        self.clear_content()
        self.show_section_label("Stats")

    def on_graph_clicked(self):
        self.clear_content()
        self.show_section_label("Graph")

    def on_settings_clicked(self):
        self.clear_content()
        self.show_section_label("Settings")

    def show_section_label(self, name):
        section_widget = QWidget()
        layout = QVBoxLayout(section_widget)
        layout.addStretch()
        label = QLabel(f"{name} Section")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 28px; color: #36d1c4; font-weight: bold;")
        layout.addWidget(label)
        layout.addStretch()
        self.content_layout.addWidget(section_widget)

    def show_message(self, message):
        self.setWindowTitle(message)

    def resizeEvent(self, event):
        if hasattr(self, 'summary_container'):
            scroll_width = self.scroll_area.viewport().width() if hasattr(self, "scroll_area") else self.width()
            left_margin, _, right_margin, _ = self.content_layout.getContentsMargins()
            card_width = max(scroll_width - left_margin - right_margin, 100)
            for i in range(self.summary_container.count()):
                w = self.summary_container.itemAt(i).widget()
                if isinstance(w, SummaryCardButton):
                    w.setFixedWidth(card_width)
        super().resizeEvent(event)