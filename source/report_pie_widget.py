from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class ReportPieWidget(QWidget):
    def __init__(self, income, expense, other, title="", parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.setStyleSheet("background: #f7f7f7; border-radius: 20px;")
        self.canvas = FigureCanvas(plt.Figure())
        layout.addWidget(self.canvas)
        self.ax = self.canvas.figure.subplots()
        self.draw_pie(income, expense, other)

    def draw_pie(self, income, expense, other):
        self.canvas.figure.set_facecolor("#f7f7f7")
        self.ax.set_facecolor("#f7f7f7")
        self.ax.clear()
        self.ax.set_aspect("equal", adjustable="datalim")
        labels = ['Income', 'Expense', 'Other']
        sizes = [income, expense, other]
        colors = ['#64b6f7', '#f66d6d', '#f2c94c']
        explode = [0.05 if size > 0 else 0 for size in sizes]
        filtered = [(l, s, c, e) for l, s, c, e in zip(labels, sizes, colors, explode) if s > 0]
        if filtered:
            labels, sizes, colors, explode = zip(*filtered)
            wedges, texts, autotexts = self.ax.pie(
                sizes, labels=labels, colors=colors, explode=explode,
                autopct='%1.1f%%', startangle=90, counterclock=False,
                wedgeprops=dict(edgecolor='#f7f7f7', linewidth=2)
            )
            for text in texts + autotexts:
                text.set_color("#222")
        else:
            self.ax.text(0.5, 0.5, "No data", ha='center', va='center', fontsize=16, color="#222")
        self.ax.set_title("")
        self.canvas.figure.tight_layout()
        self.canvas.draw()