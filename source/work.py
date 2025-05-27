from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QLabel, QPushButton,
    QFrame, QSizePolicy, QMessageBox
)
from PySide6.QtCore import Qt, QTimer
from card_dialog import AddCardDialog
from consql import DatabaseConnector
from PySide6.QtWidgets import QDialog
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

class MonthSummaryWidget(QWidget):
    def __init__(self, month_label, card_totals):
        super().__init__()
        top_layout = QVBoxLayout(self)
        top_layout.setSpacing(10)
        top_layout.setContentsMargins(0, 0, 0, 0)

        lbl_month = QLabel(month_label)
        lbl_month.setStyleSheet("font-size: 20px; color: #36d1c4; font-weight: bold;")
        lbl_month.setAlignment(Qt.AlignmentFlag.AlignLeft)
        top_layout.addWidget(lbl_month)

        # Balance card at the top
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

        # 3 cards row (Income, Expense, Other)
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
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Money Manager")
        self.resize(380, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.outer_layout = QVBoxLayout(central_widget)
        self.outer_layout.setContentsMargins(0, 0, 0, 0)
        self.outer_layout.setSpacing(0)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(16, 16, 16, 16)
        self.content_layout.setSpacing(10)
        self.outer_layout.addWidget(self.content_widget, 1)

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

        nav_bar_widget = QWidget()
        nav_bar_widget.setLayout(self.nav_bar)
        self.outer_layout.addWidget(nav_bar_widget, 0)

        self.home_widgets = []
        self.home_cards = []

        self.show_home()

    def clear_content(self):
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

    def get_monthly_summary(self):
        db = DatabaseConnector()
        monthly = {}
        try:
            # Use concatenated string, not triple quotes (avoid indentation/space issues)
            sql = (
                "SELECT DATE_FORMAT(dates, '%Y-%m') AS year_month, type, SUM(money) "
                "FROM ngay "
                "WHERE user_id = %s "
                "GROUP BY DATE_FORMAT(dates, '%Y-%m'), type "
                "ORDER BY DATE_FORMAT(dates, '%Y-%m') DESC"
            )
            db.cursor.execute(sql, (self.user_id,))
            rows = db.cursor.fetchall()
        finally:
            db.close()

        for ym, typ, total in rows:
            if ym not in monthly:
                monthly[ym] = {'Income': 0, 'Expense': 0, 'Other': 0}
            monthly[ym][typ] = total

        for ym, vals in monthly.items():
            balance = vals.get('Income', 0) + vals.get('Other', 0) - vals.get('Expense', 0)
            vals['balance'] = balance

        return monthly

    def show_home(self):
        self.clear_content()
        self.home_widgets = []

        # Get monthly card values from SQL
        monthly = self.get_monthly_summary()
        for ym, card_totals in monthly.items():
            month_label = ym
            month_widget = MonthSummaryWidget(month_label, card_totals)
            self.content_layout.addWidget(month_widget)
            self.home_widgets.append(month_widget)

            # Transactions for this month
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            summary_scroll_content = QWidget()
            summary_scroll_content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
            summary_container = QVBoxLayout(summary_scroll_content)
            summary_container.setSpacing(12)
            summary_container.setAlignment(Qt.AlignmentFlag.AlignTop)
            scroll_area.setWidget(summary_scroll_content)
            self.content_layout.addWidget(scroll_area, 1)
            self.home_widgets.append(scroll_area)

            db = DatabaseConnector()
            try:
                sql = (
                    "SELECT title, money, dates, type FROM ngay "
                    "WHERE user_id = %s AND DATE_FORMAT(dates, '%Y-%m') = %s "
                    "ORDER BY dates DESC, id DESC"
                )
                db.cursor.execute(sql, (self.user_id, ym))
                cards = db.cursor.fetchall()
            finally:
                db.close()

            color_map = {
                "Income": "#64b6f7",
                "Expense": "#f66d6d",
                "Other": "#f2c94c",
            }
            for title, money, date_str, card_type in cards:
                color = color_map.get(card_type, "#36d1c4")
                btn = SummaryCardButton(f"{title} ({date_str})", f"{money:,.0f} VND", color)
                btn.clicked.connect(lambda checked, t=title: self.show_message(f"{t} card clicked!"))
                scroll_width = scroll_area.viewport().width()
                left_margin, _, right_margin, _ = self.content_layout.getContentsMargins()
                card_width = max(scroll_width - left_margin - right_margin, 100)
                btn.setFixedWidth(card_width)
                summary_container.addWidget(btn)

        QTimer.singleShot(0, self.resize_all_cards)

    def add_summary_card(self):
        dialog = AddCardDialog(self)
        if dialog.exec() == QDialog.Accepted:
            title, amount, card_type, date_str = dialog.get_values()
            try:
                float_amount = float(amount.replace(",", "").replace("$", ""))
            except ValueError:
                QMessageBox.warning(self, "Input Error", "Amount must be a number.")
                return

            color_map = {
                "Income": "#64b6f7",
                "Expense": "#f66d6d",
                "Other": "#f2c94c",
            }
            color = color_map.get(card_type, "#36d1c4")

            db = DatabaseConnector()
            try:
                db.cursor.execute(
                    "INSERT INTO ngay (user_id, title, dates, money, type) VALUES (%s, %s, %s, %s, %s)",
                    (self.user_id, title, date_str, float_amount, card_type)
                )
                db.conn.commit()
            except Exception as e:
                QMessageBox.critical(self, "Database Error", f"Could not save card: {e}")
                db.close()
                return
            db.close()

            # Refresh the home screen to update totals and cards
            self.show_home()

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
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 28px; color: #36d1c4; font-weight: bold;")
        layout.addWidget(label)
        layout.addStretch()
        self.content_layout.addWidget(section_widget)

    def show_message(self, message):
        self.setWindowTitle(message)

    def resizeEvent(self, event):
        self.resize_all_cards()
        super().resizeEvent(event)

    def resize_all_cards(self):
        # This will resize all SummaryCardButton widgets in all summary_containers
        for i in range(self.content_layout.count()):
            widget = self.content_layout.itemAt(i).widget()
            if isinstance(widget, QScrollArea):
                scroll_width = widget.viewport().width()
                left_margin, _, right_margin, _ = self.content_layout.getContentsMargins()
                card_width = max(scroll_width - left_margin - right_margin, 100)
                scroll_content = widget.widget()
                if scroll_content and isinstance(scroll_content.layout(), QVBoxLayout):
                    layout = scroll_content.layout()
                    for j in range(layout.count()):
                        w = layout.itemAt(j).widget()
                        if isinstance(w, SummaryCardButton):
                            w.setFixedWidth(card_width)