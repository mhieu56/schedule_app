import requests, os, time, shutil, sys

current_version = 'v1.0'
def get_latest_version():
    github_url = "https://api.github.com/repos/mhieu56/schedule_app/releases/latest"
    
    response = requests.get(github_url)
    if response.status_code == 200:
        latest_release = response.json()
        latest_version = latest_release["tag_name"]  # Lấy tag version từ release mới nhất
        return latest_version
    else:
        print("Không thể lấy thông tin từ GitHub")
        return None

def get_latest_release():
    github_url = "https://api.github.com/repos/mhieu56/schedule_app/releases/latest"
    response = requests.get(github_url)
    if response.status_code == 200:
        latest_release = response.json()
        return latest_release
    else:
        print("Không thể lấy thông tin từ GitHub")
        return None
    
def get_asset_url(latest_release):
    # Tìm URL tải file .exe từ release
    assets = latest_release["assets"]
    for asset in assets:
        if asset["name"].endswith(".exe"):
            return asset["browser_download_url"]
    print("Không tìm thấy file .exe trong release.")
    return None

def download_file(url, filename):
    # Tải file về và lưu
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Đã tải file {filename} thành công.")
    else:
        print("Không thể tải file.")

def update_software():
    latest_release = get_latest_release()
    if latest_release:
        # Lấy URL tải về của file .exe
        asset_url = get_asset_url(latest_release)
        if asset_url:
            # Đặt tên file mới là v1.0.exe (hoặc tên tương ứng)
            filename = f"{get_latest_version()}.exe"

            # Đóng ứng dụng trước khi thay thế file cũ
            print("Đóng ứng dụng để cập nhật...")
            time.sleep(2)  # Tạm dừng một chút trước khi thay thế file

            # Tải bản cập nhật mới
            download_file(asset_url, filename)

            # Đóng ứng dụng hiện tại (nếu cần)
            print("Đang thay thế file .exe cũ...")
            current_exe = sys.argv[0]  # Lấy tên file hiện tại của ứng dụng
            shutil.move(filename, current_exe)  # Thay thế file cũ bằng file mới

            # Khởi động lại ứng dụng
            print("Khởi động lại ứng dụng...")
            os.execv(current_exe, sys.argv)  # Khởi động lại ứng dụng

# Ví dụ: Khi người dùng chọn "Cập nhật"
update_software()