from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class ReportBarWidget(QWidget):
    def __init__(self, labels, this_month_vals, prev_month_vals, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.setStyleSheet("background: #f7f7f7; border-radius: 20px;")
        self.canvas = FigureCanvas(plt.Figure())
        layout.addWidget(self.canvas)
        self.ax = self.canvas.figure.subplots()
        self.draw_bar(labels, this_month_vals, prev_month_vals)

    def draw_bar(self, labels, this_month_vals, prev_month_vals):
        import numpy as np
        this_thousands = [v / 1000 for v in this_month_vals]
        prev_thousands = [v / 1000 for v in prev_month_vals]

        x = np.arange(len(labels))
        width = 0.35
        self.canvas.figure.set_facecolor("#f7f7f7")
        self.ax.set_facecolor("#f7f7f7")
        self.ax.clear()
        bars1 = self.ax.bar(x - width/2, this_thousands, width, label="This Month", color="#36d1c4")
        bars2 = self.ax.bar(x + width/2, prev_thousands, width, label="Previous Month", color="#64b6f7")
        self.ax.set_xticks(x)
        self.ax.set_xticklabels(labels)
        self.ax.legend()
        self.ax.set_ylabel("Số tiền (nghìn VND)")
        self.ax.set_title("")
        max_y = max(this_thousands + prev_thousands + [0])
        self.ax.set_ylim(0, max_y * 1.15 if max_y > 0 else 1)
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                if height != 0:
                    self.ax.annotate(f'{height:,.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9, color="#222"
                    )
        self.canvas.figure.tight_layout()
        self.canvas.draw()

    def resizeEvent(self, event):
        self.canvas.figure.tight_layout()
        self.canvas.draw()
        super().resizeEvent(event)