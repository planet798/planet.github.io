import os
import streamlit as st
import face_recognition
import numpy as np
import tempfile
import psycopg2
import datetime
from time import strftime, localtime
from PIL import Image


def get_current_time():
    return strftime("%Y-%m-%d %H:%M:%S", localtime())

def capture_image():
    img_file_buffer = st.camera_input("请正视摄像头")
    if img_file_buffer is not None:
        img = Image.open(img_file_buffer)
        st.image(img, caption='上传图片', use_column_width=True)
        img_array = np.array(img)
        return img_array


# 数据库连接配置
db_config = {
    'host': '192.168.23.131',
    'port': '5432',
    'user': 'opengauss',
    'password': 'opengauss@123',
    'dbname': 'school'
}

# 连接到数据库的函数
def connect_to_database(config):
    try:
        conn = psycopg2.connect(**db_config)
        conn.set_client_encoding('UTF8')
        return conn
    except Exception as e:
        st.error(f"数据库连接失败: {e}")
        return None


# 插入数据的函数
# 插入数据的函数，增加检查当天是否已打卡的逻辑
def insert_attendence_record(conn, id, time):
    try:
        with conn.cursor() as cursor:
            # 查询employees表获取name
            sql = "SELECT name FROM employees WHERE id = %s"
            cursor.execute(sql, (id,))
            employee = cursor.fetchone()
            if employee:
                name = employee[0]

                # 检查今天是否已经打卡
                check_sql = "SELECT COUNT(*) FROM attendence WHERE id = %s AND time::date = %s"
                cursor.execute(check_sql, (id, time))
                if cursor.fetchone()[0] > 0:
                    st.write(f"{name}今天已打卡")
                    return  # 如果已打卡，返回不执行插入操作

                # 插入attendance表，包括name
                insert_sql = "INSERT INTO attendence (id, name, time) VALUES (%s, %s, %s)"
                cursor.execute(insert_sql, (id, name, time))
                conn.commit()
                st.write(f"{id}{name}打卡成功，打卡时间：{get_current_time()}")
            else:
                st.error("工号不存在，请确认后重试")
    except Exception as e:
        st.error(f"数据插入失败: {e}")


def delete_old_attendence_records(conn):
    try:
        with conn.cursor() as cursor:
            # 删除前一天的打卡记录
            delete_sql = "DELETE FROM attendence WHERE time < %s"
            cursor.execute(delete_sql, (datetime.date.today(),))
            conn.commit()
    except Exception as e:
        st.error(f"删除旧打卡记录失败: {e}")


st.sidebar.markdown(" ")
st.title("打卡界面")
id = st.text_input("请输入你的工号", key="id")
base_path = r"D:/opencv/capture_test"

img_array = capture_image()
if img_array is not None:
    # 将拍照的图片保存为临时文件
    temp_path = tempfile.NamedTemporaryFile(delete=False, dir="D:/opencv").name
    try:
        Image.fromarray(img_array).save(temp_path, 'JPEG')

        # 人脸识别处理
        known_face = face_recognition.load_image_file(os.path.join(base_path, f"{id}.jpg"))
        known_face_encoding = face_recognition.face_encodings(known_face)[0]

        current_image = face_recognition.load_image_file(temp_path)
        current_face_encodings = face_recognition.face_encodings(current_image)
        if current_face_encodings:
            current_face_encoding = current_face_encodings[0]
            results = face_recognition.compare_faces([known_face_encoding], current_face_encoding)
            if results[0]:  # 确保比较的是第一个元素，因为results是一个列表

                conn = connect_to_database(db_config)
                if conn:
                    delete_old_attendence_records(conn)
                    # 插入打卡记录
                    insert_attendence_record(conn, id, get_current_time())
                    # 关闭数据库连接
                    conn.close()

            else:
                st.error("打卡失败，请确定是本人操作")
        else:
            st.write("当前图像中未检测到人脸，请重试。")

    finally:
        # 确保临时文件被删除
        if os.path.exists(temp_path):
            os.unlink(temp_path)
