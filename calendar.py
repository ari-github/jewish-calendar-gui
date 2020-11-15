from PyQt5 import QtCore
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton, QHBoxLayout, QApplication

from zmanim.hebrew_calendar.jewish_date import JewishDate
from hebrew_date_format import HebrewDateFormatter
import sys


class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.title = 'לוח שנה'
        self.setWindowTitle(self.title)

        self.init_head_layout()

        self.vb = QVBoxLayout()

        self.table = QWidget()
        self.label = QLabel()
        self.table.setMinimumSize(400, 400)

        self.vb.addLayout(self.head_layout, 0)
        self.vb.addWidget(self.table, 1)
        self.vb.addWidget(self.label, 0)

        self.table_headers = [' יום א\'', 'יום ב\'', 'יום ג\'', 'יום ד\'', 'יום ה\'', 'יום ו\'', 'שבת']

        self.cell_width = (self.table.geometry().width()) / 7
        self.cell_height = (self.table.geometry().height()) / 7

        self.recs = dict()
        self.recs_head = dict()

        self.choice_date = JewishDate()

        self.choice_rec = None

        self.setLayout(self.vb)

    def paintEvent(self, event):
        if self.choice_date < JewishDate(3761, 11, 1):
            self.choice_date = JewishDate(3761, 11, 1)

        if self.choice_date > JewishDate(9999, 6, 29):
            self.choice_date = JewishDate(9999, 6, 29)

        painter = QPainter(self)
        self.paint_table(painter)
        self.paint_headers(painter)
        self.paint_date(painter)
        self.update_date()

    def update_date(self):
        hdf = HebrewDateFormatter()
        self.label.setText(hdf.format(self.choice_date) + '\n' + str(self.choice_date.gregorian_date))

        self.year_label.setText(hdf.format_hebrew_number(self.choice_date.jewish_year))
        self.month_label.setText(hdf.format_month(self.choice_date))
        self.day_label.setText(hdf.format_hebrew_number(self.choice_date.jewish_day))

    def paint_table(self, painter):
        self.cell_width = (self.table.geometry().width()) / 7
        self.cell_height = (self.table.geometry().height()) / 7

        painter.setPen(QColor(230, 230, 230))
        c = 0
        for x in range(7):
            for y in reversed(range(7)):
                r = QRect(y * self.cell_width + self.table.geometry().x(),
                          x * self.cell_height + self.table.geometry().y(),
                          self.cell_width, self.cell_height)
                r.x()
                if x == 0:
                    painter.setBrush(QColor(242, 243, 244))
                    self.recs_head[6 - y] = r
                else:
                    painter.setBrush(Qt.white)
                    self.recs[c] = r
                    c += 1
                painter.drawRect(r)

    def paint_headers(self, painter):
        painter.setPen(QColor(0, 0, 0))
        painter.setFont(QFont('SansSerif', 10))

        for index in self.recs_head:
            painter.drawText(self.recs_head[index], Qt.AlignCenter, self.table_headers[index])

    def paint_date(self, painter):
        hdf = HebrewDateFormatter()
        start_date = JewishDate(self.choice_date.jewish_year, self.choice_date.jewish_month, 1)
        start_date.back(start_date.day_of_week - 1)

        painter.setFont(QFont('SansSerif', 10))
        for index in self.recs:
            if self.choice_date.jewish_month == start_date.jewish_month:
                painter.setPen(QColor(0, 0, 0))
            else:
                painter.setPen(QColor(125, 125, 125))
            if self.choice_date == start_date:
                self.choice_rec = index
                painter.setPen(Qt.NoPen)
                painter.setBrush(QColor(62, 149, 207))
                painter.drawRect(self.recs[self.choice_rec])
                painter.setPen(QColor(255, 255, 255))

            text = hdf.format_hebrew_number(start_date.jewish_day)
            painter.drawText(self.recs[index], Qt.AlignCenter, text)
            start_date.forward()

    def keyPressEvent(self, event):
        if event.key() == 16777235:
            moves = - 7
        elif event.key() == Qt.Key_Down:
            moves = 7
        elif event.key() == Qt.Key_Right:
            moves = -1
        elif event.key() == Qt.Key_Left:
            moves = 1
        else:
            return
        self.increase_date(moves)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.buttons() == QtCore.Qt.LeftButton:
            for index in self.recs:
                rec = self.recs[index]
                if rec.x() <= event.x() <= rec.width() + rec.x() and rec.y() <= event.y() <= rec.height() + rec.y():
                    self.increase_date(index - self.choice_rec)
                    break

    def increase_date(self, increment):
        try:
            self.choice_date.forward(increment)
            self.update()
        except:
            pass

    def set_date(self, year, month, day):
        try:
            self.choice_date = JewishDate(year, month, day)
            self.update()
        except:
            pass

    def init_head_layout(self):
        self.year_up = QPushButton('>')
        self.year_up.clicked.connect(self.year_up_click)
        self.year_up.setFocusPolicy(QtCore.Qt.NoFocus)

        self.year_down = QPushButton('<')
        self.year_down.clicked.connect(self.year_down_click)
        self.year_down.setFocusPolicy(QtCore.Qt.NoFocus)

        self.month_up = QPushButton('>')
        self.month_up.clicked.connect(self.month_up_click)
        self.month_up.setFocusPolicy(QtCore.Qt.NoFocus)

        self.month_down = QPushButton('<')
        self.month_down.clicked.connect(self.month_down_click)
        self.month_down.setFocusPolicy(QtCore.Qt.NoFocus)

        self.day_up = QPushButton('>')
        self.day_up.clicked.connect(self.day_up_click)
        self.day_up.setFocusPolicy(QtCore.Qt.NoFocus)

        self.day_down = QPushButton('<')
        self.day_down.clicked.connect(self.day_down_click)
        self.day_down.setFocusPolicy(QtCore.Qt.NoFocus)

        self.year_up.setMaximumWidth(50)
        self.year_down.setMaximumWidth(50)

        self.month_up.setMaximumWidth(50)
        self.month_down.setMaximumWidth(50)

        self.day_up.setMaximumWidth(50)
        self.day_down.setMaximumWidth(50)

        font = QFont('SansSerif', 10)
        font.setBold(True)
        self.year_label = QLabel()
        self.year_label.setAlignment(Qt.AlignCenter)
        self.year_label.setFont(font)
        self.year_label.setFixedWidth(100)

        self.month_label = QLabel()
        self.month_label.setAlignment(Qt.AlignCenter)
        self.month_label.setFont(font)
        self.month_label.setFixedWidth(60)

        self.day_label = QLabel()
        self.day_label.setAlignment(Qt.AlignCenter)
        self.day_label.setFont(QFont(font))
        self.day_label.setFixedWidth(50)

        self.head_layout = QHBoxLayout()

        self.head_layout.addWidget(self.day_down, 1, Qt.AlignRight)
        self.head_layout.addWidget(self.day_label, 0, Qt.AlignHCenter)
        self.head_layout.addWidget(self.day_up, 1, Qt.AlignLeft)

        self.head_layout.addWidget(self.month_down, 1, Qt.AlignRight)
        self.head_layout.addWidget(self.month_label, 0, Qt.AlignHCenter)
        self.head_layout.addWidget(self.month_up, 1, Qt.AlignLeft)

        self.head_layout.addWidget(self.year_down, 1, Qt.AlignRight)
        self.head_layout.addWidget(self.year_label, 0, Qt.AlignHCenter)
        self.head_layout.addWidget(self.year_up, 1, Qt.AlignLeft)

    def year_up_click(self):
        self.set_date(self.choice_date.jewish_year + 1, self.choice_date.jewish_month, self.choice_date.jewish_day)

    def year_down_click(self):
        self.set_date(self.choice_date.jewish_year - 1, self.choice_date.jewish_month, self.choice_date.jewish_day)

    def month_up_click(self):
        year = self.choice_date.jewish_year
        month = self.choice_date.jewish_month + 1
        if month == 7:
            year += 1
        if month == self.choice_date.months_in_jewish_year() + 1:
            month = 1

        self.set_date(year, month, self.choice_date.jewish_day)

    def month_down_click(self):
        year = self.choice_date.jewish_year
        month = self.choice_date.jewish_month - 1
        if month == 6:
            year -= 1
        if month == 0:
            month = self.choice_date.months_in_jewish_year()

        self.set_date(year, month, self.choice_date.jewish_day)

    def day_up_click(self):
        self.increase_date(1)

    def day_down_click(self):
        self.increase_date(-1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setLayoutDirection(Qt.RightToLeft)
    window = Window()
    window.show()
    sys.exit(app.exec())
