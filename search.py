import requests
from urllib3.exceptions import InsecureRequestWarning
import warnings
from bs4 import BeautifulSoup

weekday_int = {
    "Thứ Hai": 2,
    "Thứ Ba": 3,
    "Thứ Tư": 4,
    "Thứ Năm": 5,
    "Thứ Sáu": 6,
    "Thứ Bảy": 7,
    "Chủ Nhật": 8,
}
int_weekday = {
    2: "Thứ Hai",
    3: "Thứ Ba",
    4: "Thứ Tư",
    5: "Thứ Năm",
    6: "Thứ Sáu",
    7: "Thứ Bảy",
    8: "Chủ Nhật",
}

# Tắt cảnh báo InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)


# URL nơi form gửi dữ liệu
url = 'https://dangky.tdc.edu.vn/TraCuuHocPhan'


def search(subject_id):
    if subject_id:
        # Dữ liệu bạn muốn gửi (payload)
        payload = {
            'ddlMonHoc': 0,          # Tham số ddlMonHoc
            'txtSearch': subject_id, # Giá trị tìm kiếm
        }

        # Gửi yêu cầu POST mà không kiểm tra chứng chỉ SSL
        response = requests.post(url, data=payload, verify=False)
        text = response.text
        soup = BeautifulSoup(text, 'html.parser')
        data = soup.find_all('tr', class_='trhover')
        class_list = []
        for item in data:
            td_list = item.find_all('td')  # Lấy tất cả các thẻ <td> trong dòng <tr>

            # Kiểm tra nếu thẻ <td> thứ 6 (td[5]) có dữ liệu (không phải rỗng)
            if td_list[5].text.strip():  # Kiểm tra xem td[5] có dữ liệu không
                # Tạo tuple với text từ các thẻ <td>
                info = td_list[5].text.strip().split(',')
                info_strip = [i.strip() for i in info]
                count = int(len(info_strip)/6)
                for i in range(count):
                    weekday = weekday_int[info_strip[0+i*7].strip()]
                    time_start = info_strip[1+i*7].split('-')[0].strip().replace('h', ':')
                    time_end = info_strip[1+i*7].split('-')[1].strip().replace('h', ':')
                    room = info_strip[2+i*7].strip()
                    class_info = (
                        "",
                        td_list[0].text.strip(),
                        td_list[1].text.strip(),
                        td_list[2].text.strip(),
                        td_list[6].text.strip(),
                        weekday,
                        time_start,
                        time_end,
                        room,
                        td_list[8].text.strip(),
                        td_list[9].text.strip(),
                    )
                    class_list.append(class_info)

        # Kiểm tra kết quả
        if response.status_code == 200:
            #print("Yêu cầu thành công!")
            return class_list
        else:
            print("Lỗi khi gửi yêu cầu:", response.status_code)
