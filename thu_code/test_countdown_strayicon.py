import sys
from PySide6.QtCore import QTimer, QDateTime
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

class CountdownApp(QWidget):
    def __init__(self):
        super().__init__()
        
        current_time = QDateTime.currentDateTime()

        # Khởi tạo ngày giờ trong tương lai (ví dụ: 2025-01-20 10:30)
        self.future_datetime = QDateTime(2025, 2, 6, 8, 0, 0)

        # Tạo các QLabel để hiển thị thời gian hiện tại, thời gian trong tương lai và thời gian còn lại
        self.current_time_label = QLabel(f"Hiện tại là:")
        self.future_time_label = QLabel(f"Ngày đăng ký học phần: {self.future_datetime.toString('yyyy-MM-dd HH:mm:ss')}")
        self.time_left_label = QLabel("Bạn còn: ")

        # Thiết lập kiểu chữ cho các nhãn
        self.current_time_label.setStyleSheet("font-size: 20px;")
        self.future_time_label.setStyleSheet("font-size: 20px;")
        self.time_left_label.setStyleSheet("font-size: 20px;")

        # Thiết lập layout
        layout = QVBoxLayout()
        layout.addWidget(self.current_time_label)
        layout.addWidget(self.future_time_label)
        layout.addWidget(self.time_left_label)
        self.setLayout(layout)

        # Khởi tạo QTimer để cập nhật thời gian mỗi giây
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Cập nhật mỗi giây

        # Thiết lập cửa sổ
        self.setWindowTitle("Countdown Timer")
        self.setGeometry(200, 200, 400, 200)

    def update_time(self):
        # Lấy thời gian hiện tại
        current_time = QDateTime.currentDateTime()
        self.current_time_label.setText(f"Hiện tại: {current_time.toString('yyyy-MM-dd HH:mm:ss')}")

        # Tính toán thời gian còn lại
        time_left = current_time.secsTo(self.future_datetime)

        if time_left > 0:
            days_left = time_left // 86400  # Số ngày còn lại
            hours_left = (time_left % 86400) // 3600  # Số giờ còn lại
            minutes_left = (time_left % 3600) // 60  # Số phút còn lại
            seconds_left = time_left % 60  # Số giây còn lại

            self.time_left_label.setText(f"Bạn còn: {days_left} days {hours_left:02}:{minutes_left:02}:{seconds_left:02}")
        else:
            self.time_left_label.setText("Time Left: Time's up!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CountdownApp()
    window.show()
    sys.exit(app.exec())