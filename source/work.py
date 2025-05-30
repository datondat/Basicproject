import warnings
warnings.filterwarnings(
    "ignore",
    message="Ignoring fixed [xy] limits to fulfill fixed data aspect with adjustable data limits."
)

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QLabel, QPushButton,
    QSizePolicy, QMessageBox, QDialog, QComboBox, QInputDialog
)
from PySide6.QtCore import Qt, QTimer

from card_dialog import AddCardDialog
from consql import DatabaseConnector

from summary_card import SummaryCard
from edit_card_dialog import EditCardDialog
from month_summary_widget import MonthSummaryWidget
from summary_card_button import SummaryCardButton
from report_pie_widget import ReportPieWidget
from report_bar_widget import ReportBarWidget

class Work(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Money Manager")
        self.resize(420, 750)
        info = self.get_user_info()
        self.username = info.get("username", "Unknown")
        self.email = info.get("email", "Unknown")
        self.nickname = info.get("nickname", "No nickname")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.outer_layout = QVBoxLayout(central_widget)
        self.outer_layout.setContentsMargins(0, 0, 0, 0)
        self.outer_layout.setSpacing(0)

        self.month_combo = QComboBox()
        self.month_combo.setStyleSheet("font-size: 16px; margin: 8px;")
        self.month_combo.currentTextChanged.connect(self.on_month_changed)
        self.outer_layout.addWidget(self.month_combo, 0)

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
        self.available_months = []
        self.all_time_pie_widget = None
        self.all_time_label_widget = None
        self.load_months()
        self.show_home(self.get_selected_month())

    def get_user_info(self):
        db = DatabaseConnector()
        try:
            db.cursor.execute(
                "SELECT logname, mail, nickname FROM users WHERE id = %s",
                (self.user_id,)
            )
            row = db.cursor.fetchone()
        finally:
            db.close()
        if row:
            return {
                "username": row[0] or "Unknown",
                "email": row[1] or "Unknown",
                "nickname": row[2] or "No nickname"
            }
        return {"username": "Unknown", "email": "Unknown", "nickname": "No nickname"}

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
            entry = {
                'id': row[0],
                'title': row[2],
                'date': row[3],
                'money': row[4],
                'type': row[5]
            }
            btn.clicked.connect(lambda checked, e=entry: self.edit_entry_dialog(e, selected_month))
            scroll_width = scroll_area.viewport().width()
            left_margin, _, right_margin, _ = self.content_layout.getContentsMargins()
            card_width = max(scroll_width - left_margin - right_margin, 100)
            btn.setFixedWidth(card_width)
            summary_container.addWidget(btn)

        QTimer.singleShot(0, self.resize_all_cards)

    def get_month_summary(self, month):
        totals = {'Income': 0, 'Expense': 0, 'Other': 0}
        rows = []
        db = DatabaseConnector()
        try:
            sql = (
                "SELECT `type`, SUM(money) FROM ngay "
                "WHERE user_id = %s AND DATE_FORMAT(dates, '%Y-%m') = %s "
                "GROUP BY `type`"
            )
            db.cursor.execute(sql, (self.user_id, month))
            rows = db.cursor.fetchall()
        finally:
            db.close()
        for typ, total in rows:
            totals[typ] = float(total)
        totals['balance'] = totals['Income'] + totals['Other'] - totals['Expense']
        return totals

    def get_month_totals(self, month):
        totals = {'Income': 0, 'Expense': 0, 'Other': 0}
        db = DatabaseConnector()
        try:
            sql = (
                "SELECT `type`, SUM(money) FROM ngay "
                "WHERE user_id = %s AND DATE_FORMAT(dates, '%Y-%m') = %s "
                "GROUP BY `type`"
            )
            db.cursor.execute(sql, (self.user_id, month))
            rows = db.cursor.fetchall()
        finally:
            db.close()
        for typ, total in rows:
            totals[typ] = float(total)
        return totals

    def get_all_time_totals(self):
        db = DatabaseConnector()
        totals = {'Income': 0, 'Expense': 0, 'Other': 0}
        rows = []
        try:
            sql = (
                "SELECT `type`, SUM(money) FROM ngay "
                "WHERE user_id = %s GROUP BY `type`"
            )
            db.cursor.execute(sql, (self.user_id,))
            rows = db.cursor.fetchall()
        finally:
            db.close()
        for typ, total in rows:
            totals[typ] = float(total)
        return totals

    def show_all_time_totals(self):
        totals = self.get_all_time_totals()
        for attr in ['all_time_pie_widget', 'all_time_label_widget']:
            widget = getattr(self, attr, None)
            if widget is not None:
                try:
                    self.content_layout.removeWidget(widget)
                    widget.deleteLater()
                except RuntimeError:
                    pass
                setattr(self, attr, None)

        self.all_time_pie_widget = ReportPieWidget(
            totals.get('Income', 0),
            totals.get('Expense', 0),
            totals.get('Other', 0),
            title=""
        )
        self.content_layout.addWidget(self.all_time_pie_widget)

        msg = (
            f"All-Time Income: {totals['Income']:,.0f} VND\n"
            f"All-Time Expense: {totals['Expense']:,.0f} VND\n"
            f"All-Time Other: {totals['Other']:,.0f} VND\n"
            f"All-Time Balance: {(totals['Income'] + totals['Other'] - totals['Expense']):,.0f} VND"
        )
        self.all_time_label_widget = QLabel(msg)
        self.all_time_label_widget.setStyleSheet("font-size: 16px; color: #36d1c4; font-weight: bold;")
        self.all_time_label_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content_layout.addWidget(self.all_time_label_widget)

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

    def on_home_clicked(self):
        self.show_home()

    def on_stats_clicked(self):
        self.clear_content()
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
            card_totals.get('Other', 0),
            title=""
        )
        self.content_layout.addWidget(pie)

        btn_all_time = QPushButton("Show All-Time Totals")
        btn_all_time.setStyleSheet("""
            QPushButton {
                background: #36d1c4; color: #fff; border-radius: 14px;
                font-size: 16px; padding: 8px 16px;
            }
            QPushButton:hover { background: #24c1b4; }
        """)
        btn_all_time.clicked.connect(self.show_all_time_totals)
        self.content_layout.addWidget(btn_all_time)

    def on_graph_clicked(self):
        self.clear_content()
        selected_month = self.get_selected_month()
        if not selected_month:
            label = QLabel("No data for any month.")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("font-size: 18px; color: #36d1c4;")
            self.content_layout.addWidget(label)
            return

        from datetime import datetime
        from dateutil.relativedelta import relativedelta

        this_month = selected_month
        prev_month = (datetime.strptime(this_month, "%Y-%m") - relativedelta(months=1)).strftime("%Y-%m")

        this_data = self.get_month_totals(this_month)
        prev_data = self.get_month_totals(prev_month)

        categories = ["Income", "Expense", "Other"]
        this_values = [this_data.get(cat, 0) for cat in categories]
        prev_values = [prev_data.get(cat, 0) for cat in categories]

        bar_widget = ReportBarWidget(categories, this_values, prev_values)
        self.content_layout.addWidget(bar_widget)

    def on_settings_clicked(self):
        self.clear_content()
        self.show_user_settings()

    def show_user_settings(self):
        section_widget = QWidget()
        layout = QVBoxLayout(section_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        avatar_size = 80
        avatar_bg_color = "#36d1c4"
        avatar_text_color = "#fff"
        initial = (self.username[0].upper() if self.username else "U")
        avatar_label = QLabel(initial)
        avatar_label.setFixedSize(avatar_size, avatar_size)
        avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar_label.setStyleSheet(f"""
            QLabel {{
                background: {avatar_bg_color};
                color: {avatar_text_color};
                border-radius: {avatar_size//2}px;
                font-size: 42px;
                font-weight: bold;
            }}
        """)
        layout.addWidget(avatar_label, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(12)

        lbl_title = QLabel("User Information")
        lbl_title.setStyleSheet("font-size: 28px; color: #24b9d2; font-weight: bold;")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_title)

        lbl_username = QLabel(f"Tên đăng nhập: {self.username}")
        lbl_username.setStyleSheet("font-size: 19px; color: #14a37f; font-weight: bold;")
        layout.addWidget(lbl_username)

        lbl_email = QLabel(f"Email: {self.email}")
        lbl_email.setStyleSheet("font-size: 19px; color: #407ba7; font-style: italic;")
        layout.addWidget(lbl_email)

        self.lbl_nickname = QLabel(f"Nickname: {self.nickname}")
        self.lbl_nickname.setStyleSheet("font-size: 19px; color: #e4a317; font-weight: bold;")
        layout.addWidget(self.lbl_nickname)

        btn_change_nickname = QPushButton("Change Nickname")
        btn_change_nickname.setStyleSheet("""
            QPushButton {
                background: #36d1c4; color: #fff; border-radius: 12px;
                font-size: 15px; padding: 6px 16px;
            }
            QPushButton:hover { background: #24b9d2; }
        """)
        btn_change_nickname.clicked.connect(self.open_nickname_dialog)
        layout.addWidget(btn_change_nickname, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(30)

        btn_logout = QPushButton("Log out")
        btn_logout.setStyleSheet("""
            QPushButton {
                background: #f66d6d; color: #fff; border-radius: 14px;
                font-size: 18px; padding: 10px 32px;
            }
            QPushButton:hover { background: #e43d3d; }
        """)
        btn_logout.clicked.connect(self.logout)
        layout.addWidget(btn_logout, alignment=Qt.AlignmentFlag.AlignCenter)

        self.content_layout.addWidget(section_widget)

    def open_nickname_dialog(self):
        current_nick = self.nickname
        new_nick, ok = QInputDialog.getText(self, "Change Nickname", "Enter new nickname:", text=current_nick)
        if ok and new_nick.strip():
            db = DatabaseConnector()
            try:
                db.cursor.execute(
                    "UPDATE users SET nickname = %s WHERE id = %s",
                    (new_nick.strip(), self.user_id)
                )
                db.conn.commit()
            except Exception as e:
                QMessageBox.critical(self, "Database Error", f"Could not update nickname: {e}")
                return
            finally:
                db.close()
            self.nickname = new_nick.strip()
            self.lbl_nickname.setText(f"Nickname: {self.nickname}")
            QMessageBox.information(self, "Nickname Changed", "Your nickname has been updated!")

    def logout(self):
        QMessageBox.information(self, "Logout", "You have been logged out!")
        self.close()

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

    def edit_entry_dialog(self, entry, selected_month):
        dialog = EditCardDialog(entry, self)
        if dialog.exec() == QDialog.Accepted:
            updated = dialog.get_values()
            try:
                db = DatabaseConnector()
                db.cursor.execute(
                    "UPDATE ngay SET title=%s, dates=%s, money=%s, type=%s WHERE id=%s AND user_id=%s",
                    (updated['title'], updated['date'], float(updated['money']), updated['type'], updated['id'],
                     self.user_id)
                )
                db.conn.commit()
            except Exception as e:
                QMessageBox.critical(self, "Database Error", f"Could not update entry: {e}")
            finally:
                db.close()
            self.show_home(selected_month)