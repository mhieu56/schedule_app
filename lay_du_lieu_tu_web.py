import re
import requests
from urllib3.exceptions import InsecureRequestWarning
import warnings
from bs4 import BeautifulSoup
import db

# Gửi yêu cầu POST mà không kiểm tra chứng chỉ SSL
# Đọc nội dung từ file txt
with open('demo_body_html.txt', 'r', encoding='utf-8') as file:
    text = file.read()
    
soup = BeautifulSoup(text, 'html.parser')

#Phần lấy mã khoa và tên khoa
faculty_element = soup.find('option', attrs={'value': re.compile(r'^CDCQK24.+')})
# Lấy giá trị của thuộc tính 'value'
faculty_id = faculty_element.get('value') if faculty_element else None
# Lấy nội dung văn bản giữa thẻ <option>
faculty_name = faculty_element.text if faculty_element else None

#Phần lấy học kỳ và danh sách môn
data_raw = soup.find_all('table', attrs={'id':re.compile(r'.*grvHocphan$')})
#Danh sách học kỳ
semester_element_list = soup.find_all('span',attrs={'class':'title'})
semester_list = [item.text for item in semester_element_list]

#list môn học tổng
subject_by_semester = []

i = 0

for semester_table in data_raw:
    table_soup = BeautifulSoup(str(semester_table), 'html.parser')
    semester_subjects = []
    subject_id_list = table_soup.find_all('span', attrs={'id':re.compile(r'.*lblCurriculumID$')})
    subject_name_list = table_soup.find_all('span', attrs={'id':re.compile(r'.*lblCurriculumName$')})
    for id, name in zip(subject_id_list,subject_name_list):
        semester_subjects.append((semester_list[i],id.text, name.text))
    i += 1
    subject_by_semester.append(semester_subjects)

# for i in range(len(subject_id_list)):
#     print(f'{subject_id_list[i].text} - {subject_name_list[i].text}')

db.update_faculty_table([(faculty_id,faculty_name)])
db.update_subjects_by_faculty_semester(faculty_name,subject_by_semester)