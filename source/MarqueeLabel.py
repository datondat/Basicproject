from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPainter

class MarqueeLabel(QLabel):
    def __init__(self, text, parent=None, speed=40, step=2):
        super().__init__(parent)
        self._full_text = text
        self._offset = 0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._scroll_text)
        self._timer.start(speed)
        self.setStyleSheet("color: #fff; font-size: 18px; font-weight: bold;")
        self._step = step
        self.setText(text)

    def setText(self, text):
        self._full_text = text
        self._offset = 0
        super().setText(text)
        self.update()

    def _scroll_text(self):
        metrics = self.fontMetrics()
        text_width = metrics.horizontalAdvance(self._full_text + "   ")
        label_width = self.width()
        if text_width <= label_width:
            self._offset = 0
            self.update()
            return
        self._offset += self._step
        if self._offset > text_width:
            self._offset = 0
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        metrics = self.fontMetrics()
        gap = "   "
        scroll_text = self._full_text + gap
        text_width = metrics.horizontalAdvance(scroll_text)
        x = -self._offset
        y = int((self.height() + metrics.ascent() - metrics.descent()) / 2)
        painter.setPen(self.palette().color(self.foregroundRole()))
        while x < self.width():
            painter.drawText(x, y, scroll_text)
            x += text_width