from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget, QSystemTrayIcon
from PySide6.QtCore import QTimer, QTime
from PySide6.QtGui import QIcon

class CountdownTimer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Countdown Timer")

        # Tạo layout chính
        self.layout = QVBoxLayout()

        # Hiển thị thời gian
        self.label = QLabel("00:00:00")
        self.label.setStyleSheet("font-size: 40px; color: red;")
        self.layout.addWidget(self.label)

        # Nút bắt đầu
        self.start_button = QPushButton("Start Countdown")
        self.start_button.clicked.connect(self.start_countdown)
        self.layout.addWidget(self.start_button)

        # Container widget
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        # Thời gian còn lại
        self.remaining_time = QTime(0, 0, 10)  # Đặt thời gian ban đầu là 10 giây

        # QSystemTrayIcon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("sunlight.png"))  # Đặt biểu tượng cho ứng dụng
        self.tray_icon.show()  # Hiển thị biểu tượng trên thanh hệ thống

    def start_countdown(self):
        self.timer.start(1000)  # Cập nhật mỗi giây

    def update_timer(self):
        self.remaining_time = self.remaining_time.addSecs(-1)  # Trừ đi 1 giây
        self.label.setText(self.remaining_time.toString("hh:mm:ss"))

        # Kiểm tra nếu hết thời gian
        if self.remaining_time == QTime(0, 0, 0):
            self.timer.stop()
            self.label.setText("Time's up!")
            self.label.setStyleSheet("font-size: 40px; color: green;")

            # Gửi thông báo
            self.tray_icon.showMessage(
                "Countdown Complete",
                "The countdown has finished!",
                QSystemTrayIcon.Information,  # Loại thông báo
                5000  # Hiển thị thông báo trong 5 giây
            )

if __name__ == "__main__":
    app = QApplication([])
    window = CountdownTimer()
    window.show()
    app.exec()
