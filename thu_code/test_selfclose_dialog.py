# Tạo Dialog không có nút gì hết
from re import sub
import sys, json
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QListView,
    QHBoxLayout,
    QTableView,
    QLabel,
    QDialog,
    QFormLayout,
    QLineEdit,
    QHeaderView,
    QComboBox,
    QFileDialog,
)
from PySide6.QtCore import (
    Qt,
    QAbstractListModel,
    QPoint,
    QAbstractTableModel,
    QModelIndex,
    QTimer
)
from PySide6.QtGui import QFont, QImage, QPainter, QColor, QBrush, QPixmap, QIcon, QAction, QKeySequence, QShortcut
from openpyxl import Workbook
from datetime import datetime
class custom_dialog_3(QDialog):
    def __init__(self, parent=None, text="Chắc hông?"):
        super().__init__()
        self.setWindowTitle("Second Thought")
        self.setModal(True)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        self.label = QLabel(text)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("padding: 10px; font-size: 16px; color: #474a4d;")
        layout.addWidget(self.label)
        
        # Tạo một QTimer
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)  # Đảm bảo chỉ chạy một lần
        self.timer.timeout.connect(self.close)  # Đóng dialog khi timer kết thúc
        self.timer.start(2000)  # Bắt đầu đếm ngược (2 giây)

        self.setLayout(layout)
        self.resize(250, 120)

if __name__ == "__main__":
    app = QApplication([])

    dialog = custom_dialog_3()
    dialog.exec()  # Hiển thị dialog dưới dạng modal

    app.exec()