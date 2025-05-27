from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QLabel, QPushButton,
    QFrame, QSizePolicy, QMessageBox, QDialog, QComboBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from PySide6.QtCore import Qt, QTimer
from card_dialog import AddCardDialog
from consql import DatabaseConnector
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

        lbl_month = QLabel(f"{month_label} Summary")
        lbl_month.setStyleSheet("font-size: 20px; color: #36d1c4; font-weight: bold;")
        lbl_month.setAlignment(Qt.AlignmentFlag.AlignLeft)
        top_layout.addWidget(lbl_month)

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
        self.resize(420, 750)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.outer_layout = QVBoxLayout(central_widget)
        self.outer_layout.setContentsMargins(0, 0, 0, 0)
        self.outer_layout.setSpacing(0)

        # Month Selector ComboBox
        self.month_combo = QComboBox()
        self.month_combo.setStyleSheet("font-size: 16px; margin: 8px;")
        self.month_combo.currentTextChanged.connect(self.on_month_changed)
        self.outer_layout.addWidget(self.month_combo, 0)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(16, 16, 16, 16)
        self.content_layout.setSpacing(10)
        self.outer_layout.addWidget(self.content_widget, 1)

        # Navigation bar
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
        self.available_months = []
        self.load_months()
        self.show_home(self.get_selected_month())

    def load_months(self):
        db = DatabaseConnector()
        try:
            db.cursor.execute(
                "SELECT DISTINCT DATE_FORMAT(dates, '%Y-%m') as month "
                "FROM ngay WHERE user_id = %s ORDER BY month DESC",
                (self.user_id,)
            )
            months = [row[0] for row in db.cursor.fetchall()]
        finally:
            db.close()
        self.month_combo.clear()
        self.month_combo.addItems(months)
        self.available_months = months
        if months:
            self.month_combo.setCurrentIndex(0)

    def get_selected_month(self):
        if self.month_combo.count() == 0:
            return None
        return self.month_combo.currentText()

    def on_month_changed(self, month):
        self.show_home(month)

    def show_home(self, selected_month=None):
        self.clear_content()
        self.home_widgets = []

        if not selected_month:
            selected_month = self.get_selected_month()
        if not selected_month:
            label = QLabel("No data for any month.")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("font-size: 18px; color: #36d1c4;")
            self.content_layout.addWidget(label)
            return

        card_totals = self.get_month_summary(selected_month)
        all_info = self.get_all_info_for_month(selected_month)
        month_widget = MonthSummaryWidget(selected_month, card_totals)
        self.content_layout.addWidget(month_widget)
        self.home_widgets.append(month_widget)

        # Entries as interactive cards
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

        color_map = {
            "Income": "#64b6f7",
            "Expense": "#f66d6d",
            "Other": "#f2c94c",
        }
        for row in all_info:
            title = row[2] if len(row) > 2 else ""
            money = row[4] if len(row) > 4 else 0
            date_str = row[3] if len(row) > 3 else ""
            card_type = row[5] if len(row) > 5 else ""
            color = color_map.get(card_type, "#36d1c4")
            btn = SummaryCardButton(f"{title} ({date_str})", f"{float(money):,.0f} VND", color)
            btn.clicked.connect(lambda checked, t=title: self.show_message(f"{t} card clicked!"))
            scroll_width = scroll_area.viewport().width()
            left_margin, _, right_margin, _ = self.content_layout.getContentsMargins()
            card_width = max(scroll_width - left_margin - right_margin, 100)
            btn.setFixedWidth(card_width)
            summary_container.addWidget(btn)

        QTimer.singleShot(0, self.resize_all_cards)

    def get_month_summary(self, month):
        totals = {'Income': 0, 'Expense': 0, 'Other': 0}
        rows = []  # Ensure 'rows' is defined even if the SQL fails
        db = DatabaseConnector()
        try:
            sql = (
                "SELECT `type`, SUM(money) FROM ngay "
                "WHERE user_id = %s AND DATE_FORMAT(dates, '%Y-%m') = %s "
                "GROUP BY `type`"
            )
            db.cursor.execute(sql, (self.user_id, month))
            rows = db.cursor.fetchall()
            print("DEBUG: Summary for", month, ":", rows)
        finally:
            db.close()
        for typ, total in rows:
            totals[typ] = float(total)
        totals['balance'] = totals['Income'] + totals['Other'] - totals['Expense']
        return totals

    def add_summary_card(self):
        dialog = AddCardDialog(self)
        if dialog.exec() == QDialog.Accepted:
            title, amount, card_type, date_str = dialog.get_values()
            try:
                float_amount = float(amount.replace(",", "").replace("$", ""))
            except ValueError:
                QMessageBox.warning(self, "Input Error", "Amount must be a number.")
                return

            db = DatabaseConnector()
            try:
                db.cursor.execute(
                    "INSERT INTO ngay (user_id, title, dates, money, `type`) VALUES (%s, %s, %s, %s, %s)",
                    (self.user_id, title, date_str, float_amount, card_type)
                )
                db.conn.commit()
            except Exception as e:
                QMessageBox.critical(self, "Database Error", f"Could not save card: {e}")
                return
            finally:
                db.close()

            self.load_months()
            if date_str[:7] in self.available_months:
                self.month_combo.setCurrentText(date_str[:7])
            self.show_home(self.get_selected_month())

    def get_all_info_for_month(self, month):
        db = DatabaseConnector()
        try:
            sql = (
                "SELECT * FROM ngay "
                "WHERE user_id = %s AND DATE_FORMAT(dates, '%Y-%m') = %s "
                "ORDER BY dates DESC, id DESC"
            )
            db.cursor.execute(sql, (self.user_id, month))
            rows = db.cursor.fetchall()
        finally:
            db.close()
        return rows

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

    def add_summary_card(self):
        dialog = AddCardDialog(self)
        if dialog.exec() == QDialog.Accepted:
            title, amount, card_type, date_str = dialog.get_values()
            try:
                float_amount = float(amount.replace(",", "").replace("$", ""))
            except ValueError:
                QMessageBox.warning(self, "Input Error", "Amount must be a number.")
                return

            db = DatabaseConnector()
            try:
                db.cursor.execute(
                    "INSERT INTO ngay (user_id, title, dates, money, `type`) VALUES (%s, %s, %s, %s, %s)",
                    (self.user_id, title, date_str, float_amount, card_type)
                )
                db.conn.commit()
            except Exception as e:
                QMessageBox.critical(self, "Database Error", f"Could not save card: {e}")
                db.close()
                return
            db.close()

            self.load_months()
            if date_str[:7] in self.available_months:
                self.month_combo.setCurrentText(date_str[:7])
            self.show_home(self.get_selected_month())

    def on_home_clicked(self):
        self.show_home()

    def on_stats_clicked(self):
        self.clear_content()
        # Get selected month's summary
        selected_month = self.get_selected_month()
        if not selected_month:
            label = QLabel("No data for any month.")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("font-size: 18px; color: #36d1c4;")
            self.content_layout.addWidget(label)
            return

        card_totals = self.get_month_summary(selected_month)
        pie = ReportPieWidget(
            card_totals.get('Income', 0),
            card_totals.get('Expense', 0),
            card_totals.get('Other', 0)
        )
        self.content_layout.addWidget(pie)

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
class ReportPieWidget(QWidget):
    def __init__(self, income, expense, other, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.canvas = FigureCanvas(plt.Figure(figsize=(4, 4)))
        layout.addWidget(self.canvas)
        self.ax = self.canvas.figure.subplots()
        self.draw_pie(income, expense, other)

    def draw_pie(self, income, expense, other):
        self.ax.clear()
        labels = ['Income', 'Expense', 'Other']
        sizes = [income, expense, other]
        colors = ['#64b6f7', '#f66d6d', '#f2c94c']
        explode = [0.05 if size > 0 else 0 for size in sizes]
        filtered = [(l, s, c, e) for l, s, c, e in zip(labels, sizes, colors, explode) if s > 0]
        if filtered:
            labels, sizes, colors, explode = zip(*filtered)
            self.ax.pie(
                sizes, labels=labels, colors=colors, explode=explode,
                autopct='%1.1f%%', startangle=90, counterclock=False
            )
        else:
            self.ax.text(0.5, 0.5, "No data", ha='center', va='center', fontsize=16)
        self.ax.set_title("Income vs Expense vs Other")
        self.canvas.draw()