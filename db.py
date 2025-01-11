from os import error
import sqlite3
from tarfile import data_filter
from datetime import datetime

def get_subject_id_by_name(subject_name):
    try:
        # Sử dụng ngữ cảnh 'with' để đảm bảo đóng kết nối tự động
        with sqlite3.connect('info.db') as connection:
            cursor = connection.cursor()
            
            # Thực hiện truy vấn lấy subject_id
            cursor.execute("SELECT subject_id FROM all_subjects WHERE subject_name = ?", (subject_name,))
            result = cursor.fetchone()
            
            # Kiểm tra nếu kết quả không tồn tại
            if result is None:
                print(f"Subject '{subject_name}' not found in database.")
                return None
            
            # Trả về subject_id
            return result[0]
    except sqlite3.Error as e:
        # In lỗi chi tiết nếu có vấn đề trong quá trình truy vấn
        print(f"Database error: {e}")
        return None

def get_classes_by_subject_phase(subject_name,phase):
    connection = sqlite3.connect('info.db')
    cursor = connection.cursor()
    try:
        if phase == 'Sáng':
            cursor.execute("SELECT * FROM classes WHERE class_name = ? AND time_start < '12:30' ORDER BY teacher", (subject_name,))
        elif phase == 'Chiều':
            cursor.execute("SELECT * FROM classes WHERE class_name = ? AND time_start > '12:30' ORDER BY teacher", (subject_name,))
        data = cursor.fetchall()
    except error:
        print(f"Error: {error}")
        data = []
    finally:
        # Đảm bảo kết nối được đóng sau khi hoàn thành
        connection.close()
    return data

def get_classes_by_subject_weekday(subject_name,weekday):
    connection = sqlite3.connect('info.db')
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM classes WHERE class_name = ? AND weekday = ? ORDER BY teacher", (subject_name,weekday))
        data = cursor.fetchall()
    except:
        print("Get subject's Name Error!")
        data = []
    finally:
        # Đảm bảo kết nối được đóng sau khi hoàn thành
        connection.close()
    return data

def get_classes_by_subject_teacher(subject_name,teacher):
    connection = sqlite3.connect('info.db')
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM classes WHERE class_name = ? AND teacher = ? ORDER BY teacher", (subject_name,teacher))
        data = cursor.fetchall()
    except:
        print("Get subject's Name Error!")
        data = []
    finally:
        # Đảm bảo kết nối được đóng sau khi hoàn thành
        connection.close()
    return data

def get_subject_id_by_faculty_subject_name(faculty_name,subject_name):
    try:
        with sqlite3.connect('info.db') as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT subject_id FROM subjects_by_faculty_semester WHERE faculty_name = ? AND subject_name = ?", (faculty_name,subject_name))
            data = cursor.fetchone()[0]
    except sqlite3.Error as e:
        # In ra chi tiết lỗi nếu có vấn đề
        print(f"Update Faculties Table Failed! Error: {e}")
        data = []
    return data
    
def get_subjects_by_faculty_semester(faculty_name,semester):
    try:
        with sqlite3.connect('info.db') as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT subject_name FROM subjects_by_faculty_semester WHERE faculty_name = ? AND semester = ?", (faculty_name,semester))
            data = [item[0] for item in cursor.fetchall()]
    except sqlite3.Error as e:
        # In ra chi tiết lỗi nếu có vấn đề
        print(f"Update Faculties Table Failed! Error: {e}")
        data = []
    return data

def get_semester_by_faculty(faculty_name):
    try:
        with sqlite3.connect('info.db') as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT DISTINCT semester FROM subjects_by_faculty_semester WHERE faculty_name = ?", (faculty_name,))
            data = [item[0] for item in cursor.fetchall()]
    except sqlite3.Error as e:
        # In ra chi tiết lỗi nếu có vấn đề
        print(f"Update Faculties Table Failed! Error: {e}")
        data = []
    return data

def get_all_faculty():
    try:
        with sqlite3.connect('info.db') as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT faculty_name FROM faculties")
            data = [item[0] for item in cursor.fetchall()]
    except sqlite3.Error as e:
        # In ra chi tiết lỗi nếu có vấn đề
        print(f"Update Faculties Table Failed! Error: {e}")
        data = []
    return data

def update_subjects_by_faculty_semester(faculty_name,class_info=[]):
    try:
        with sqlite3.connect('info.db') as connection:
            cursor = connection.cursor()
            for classes_by_semester in class_info:
                for class_by_semester in classes_by_semester:
                    cursor.execute("INSERT INTO subjects_by_faculty_semester (faculty_name, semester, subject_id, subject_name) VALUES (?,?,?,?)", (faculty_name,class_by_semester[0],class_by_semester[1],class_by_semester[2]))
            connection.commit()
    except sqlite3.Error as e:
        # In ra chi tiết lỗi nếu có vấn đề
        print(f"Update Faculties Table Failed! Error: {e}")

def update_faculty_table(faculty_info):
    try:
        with sqlite3.connect('info.db') as connection:
            cursor = connection.cursor()
            for faculty_id, faculty_name in faculty_info:
                cursor.execute("SELECT * FROM faculties WHERE faculty_id = ?", (faculty_id,))
                check_faculty_exist = cursor.fetchone()
                if not check_faculty_exist:
                    #Nếu khoa chưa tồn tại
                    cursor.execute("INSERT INTO faculties (faculty_id,faculty_name) VALUES (?,?)", (faculty_id,faculty_name))
                else:
                    pass
            connection.commit()
            print("Cập nhật khoa thành công!")
    except sqlite3.Error as e:
        # In ra chi tiết lỗi nếu có vấn đề
        print(f"Update Faculties Table Failed! Error: {e}")

def find_subject(text):
    with sqlite3.connect('info.db') as connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM all_subjects WHERE subject_name LIKE ?", ('%' + text + '%',))
            data = cursor.fetchall()
            data_filtered = [("",subject[0],subject[1]) for subject in data]
        except sqlite3.Error as e:
            print("Error: " + str(e))
            data_filtered = []
    return data_filtered
    
def update_all_subjects_table(data=[]):
    try:
        with sqlite3.connect('info.db') as connection:
            cursor = connection.cursor()
            for subject in data:
                cursor.execute("SELECT * FROM all_subjects WHERE subject_id = ?", (subject[0],))
                if not cursor.fetchone():
                    cursor.execute("SELECT * FROM all_subjects WHERE subject_name = ?", (subject[1],))
                    if not cursor.fetchone():
                        cursor.execute("INSERT INTO all_subjects (subject_id, subject_name) VALUES (?,?)", subject)
                    else:
                        pass
                else:
                    cursor.execute("UPDATE all_subjects SET subject_name = ? WHERE subject_id = ?", (subject[1], subject[0]))
            connection.commit()
    except sqlite3.Error as e:
        # In ra chi tiết lỗi nếu có vấn đề
        print(f"Update All Subjects Table Failed! Error: {e}")

def update_database(subject_id,subject_name,class_list=[]):
    with sqlite3.connect('info.db') as connection:
        cursor = connection.cursor()
        try:
            # Bước 1: Kiểm tra mã môn đã có chưa
            cursor.execute("SELECT * FROM subjects WHERE subject_id = ?", (subject_id,))
            course = cursor.fetchone()
            if course:
                #Mã môn đã có
                cursor.execute("DELETE FROM classes WHERE class_name = ?", (subject_name,))
                for class_info in class_list:
                    cursor.execute("INSERT INTO classes (subject_id,class_id,class_name,teacher,weekday,time_start,time_end,room) VALUES (?,?,?,?,?,?,?,?)", class_info)
            else:
                #Mã môn chưa có
                cursor.execute("INSERT INTO subjects VALUES (?,?)", (subject_id,subject_name))
                for class_info in class_list:
                    cursor.execute("INSERT INTO classes (subject_id,class_id,class_name,teacher,weekday,time_start,time_end,room) VALUES (?,?,?,?,?,?,?,?)", class_info)
            connection.commit()
            print("Cập nhật thành công!")
        except sqlite3.Error as e:
            print("Error: " + str(e))

def get_subjects_name():
    connection = sqlite3.connect('info.db')
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT subject_name FROM subjects")
        data = [subject[0] for subject in cursor.fetchall()]
    except:
        print("Get subject's Name Error!")
        data = []
    finally:
        # Đảm bảo kết nối được đóng sau khi hoàn thành
        connection.close()
    return data

def get_all_subjects_name():
    connection = sqlite3.connect('info.db')
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT subject_name FROM all_subjects")
        data = [subject[0] for subject in cursor.fetchall()]
    except:
        print("Get subject's Name Error!")
        data = []
    finally:
        # Đảm bảo kết nối được đóng sau khi hoàn thành
        connection.close()
    return data

def get_subjects_id_name():
    connection = sqlite3.connect('info.db')
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM subjects")
        data = cursor.fetchall()
    except:
        print("Get subject's Name Error!")
        data = []
    finally:
        # Đảm bảo kết nối được đóng sau khi hoàn thành
        connection.close()
    return data

def get_classes(subject_name):
    connection = sqlite3.connect('info.db')
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM classes WHERE class_name = ? ORDER BY teacher", (subject_name,))
        data = cursor.fetchall()
    except:
        print("Get subject's Name Error!")
        data = []
    finally:
        # Đảm bảo kết nối được đóng sau khi hoàn thành
        connection.close()
    return data

def add_class(class_info):
    try:
        with sqlite3.connect('info.db') as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO classes (subject_id,class_id,class_name,teacher,weekday,time_start,time_end,room) VALUES (?,?,?,?,?,?,?,?)", class_info)
            connection.commit()
    except sqlite3.Error as e:
        # In ra chi tiết lỗi nếu có vấn đề
        print(f"Add Class Failed! Error: {e}")
        
def add_subject(subject_info):
    try:
        with sqlite3.connect('info.db') as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO subjects VALUES (?, ?)", subject_info)
            connection.commit()
            print(f"Added subject: {subject_info}")
    except sqlite3.Error as e:
        print(f"Add Subject Failed! Error: {e}")
        
def delete_subject(subject_name):
    try:
        with sqlite3.connect('info.db') as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM subjects WHERE subject_name = ?", (subject_name,))
            cursor.execute("DELETE FROM classes WHERE class_name = ?", (subject_name,))
            connection.commit()
    except sqlite3.Error as e:
        print("Delete Subject Failed!" + e)
        
def delete_class(class_id):
    try:
        with sqlite3.connect('info.db') as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM classes WHERE class_id = ?", (class_id,))
            connection.commit()
    except sqlite3.Error as e:
        print("Delete Class Failed!" + e)

def delete_class_all():
    try:
        with sqlite3.connect('info.db') as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM subjects")
            cursor.execute("DELETE FROM classes")
            connection.commit()
            return True
    except sqlite3.Error as e:
        print("Delete All Class Failed!" + str(e))
        return False
        
def class_count(class_name):
    connection = sqlite3.connect('info.db')
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM classes WHERE class_name = ?", (class_name,))
        count = cursor.fetchone()[0]
    except:
        print("Get subject's Name Error!")
        count = 0
    finally:
        # Đảm bảo kết nối được đóng sau khi hoàn thành
        connection.close()
    return count

def check_login(username, password):
    connection = sqlite3.connect('info.db')
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        data = cursor.fetchone()
        if data:
            return True
    except:
        print("Check login Error!")
    finally:
        connection.close()
    return False

def get_teachers(subject_name):
    connection = sqlite3.connect('info.db')
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT DISTINCT teacher FROM classes WHERE class_name = ? AND teacher IS NOT NULL", (subject_name,))
        data = cursor.fetchall()
    except:
        print("Get teachers's Name Error!")
        data = []
    finally:
        # Đảm bảo kết nối được đóng sau khi hoàn thành
        connection.close()
    return data

def get_weekdays(subject_name):
    connection = sqlite3.connect('info.db')
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT DISTINCT weekday FROM classes WHERE class_name = ? AND weekday IS NOT NULL ORDER BY weekday", (subject_name,))
        data = cursor.fetchall()
    except:
        print("Get teachers's Name Error!")
        data = []
    finally:
        # Đảm bảo kết nối được đóng sau khi hoàn thành
        connection.close()
    return data
