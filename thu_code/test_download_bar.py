import sys
import requests
from PySide6.QtWidgets import QApplication, QWidget, QProgressBar, QVBoxLayout, QPushButton

class Downloader(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Downloader with Progress')
        self.setGeometry(300, 300, 400, 150)

        # Layout and ProgressBar setup
        self.layout = QVBoxLayout(self)
        self.progress_bar = QProgressBar(self)
        self.layout.addWidget(self.progress_bar)

        self.button = QPushButton("Tải bản cập nhật", self)
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.start_download)

    def start_download(self):
        download_url = "https://github.com/mhieu56/schedule_app/releases/download/v1.0/v1.0.exe"
        filename = "v1.0.exe"
        self.download_file_with_progress(download_url, filename)

    def download_file_with_progress(self, url, filename):
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))

        # Thiết lập thanh tiến trình
        self.progress_bar.setMaximum(total_size)
        self.progress_bar.setValue(0)

        with open(filename, "wb") as f:
            for data in response.iter_content(chunk_size=1024):
                f.write(data)
                self.progress_bar.setValue(self.progress_bar.value() + len(data))
        
        print(f"Đã tải xong: {filename}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Downloader()
    window.show()
    sys.exit(app.exec())
