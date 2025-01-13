import requests

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
    
print(get_latest_version())