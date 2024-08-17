import requests
import json
import base64
from PIL import Image
from io import BytesIO
import os
import numpy as np
import streamlit as st
import tempfile
import psycopg2
import datetime
from time import strftime, localtime

API_KEY = "jY3enrAfnPl1vdYP0XxdWIpm"
SECRET_KEY = "WI8nM3IB4kg9oU69nutzgaK0paajXXlS"

def get_current_time():
    return strftime("%Y-%m-%d %H:%M:%S", localtime())


def main():
    st.sidebar.markdown(" ")
    st.title("打卡界面")
    user_id = st.text_input("请输入你的工号", key="id")
    img_array = capture_image()
    if user_id and img_array is not None:
        temp_path = tempfile.NamedTemporaryFile(delete=False, dir="D:/opencv").name
        try:
            image1_path = f"D:\\opencv\\capture_test\\{user_id}.jpg"
            image1 = Image.open(image1_path)
            image2 = img_array
            Image.fromarray(image2).save(temp_path, 'JPEG')

            # 将图片转换为base64编码
            buffered1 = BytesIO()
            buffered2 = BytesIO()
            image1.save(buffered1, format="JPEG")
            Image.fromarray(image2).save(buffered2, format="JPEG")
            img_str1 = base64.b64encode(buffered1.getvalue()).decode('utf-8')
            img_str2 = base64.b64encode(buffered2.getvalue()).decode('utf-8')

            url = "https://aip.baidubce.com/rest/2.0/face/v3/match?access_token=" + get_access_token()

            payload = json.dumps([
                {
                    "image": img_str1,
                    "image_type": "BASE64"
                },
                {
                    "image": img_str2,
                    "image_type": "BASE64"
                }
            ])
            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            response_data = json.loads(response.text)
            if response_data["error_code"] == 0 and response_data["result"]["score"] > 80:
                conn = connect_to_database(db_config)
                if conn:
                    delete_old_attendence_records(conn)
                    # 插入打卡记录
                    insert_attendence_record(conn, user_id, get_current_time())
                    # 关闭数据库连接
                    conn.close()

            else:
                st.error("打卡失败，请确定是本人操作")

        finally:
            # 确保临时文件被删除
            if os.path.exists(temp_path):
                os.unlink(temp_path)

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
def insert_attendence_record(conn, user_id, time):
    try:
        with conn.cursor() as cursor:
            # 查询employees表获取name
            sql = "SELECT name FROM employees WHERE id = %s"
            cursor.execute(sql, (user_id,))
            employee = cursor.fetchone()
            if employee:
                name = employee[0]

                # 检查今天是否已经打卡
                check_sql = "SELECT COUNT(*) FROM attendence WHERE id = %s AND time::date = %s"
                time = get_current_time()
                cursor.execute(check_sql, (user_id, time))

                if cursor.fetchone()[0] > 0:
                    st.write(f"{name}今天已打卡")
                    return  # 如果已打卡，返回不执行插入操作

                # 插入attendance表，包括name
                insert_sql = "INSERT INTO attendence (id, name, time) VALUES (%s, %s, %s)"
                cursor.execute(insert_sql, (user_id, name, time))
                conn.commit()
                st.write(f"{user_id}{name}打卡成功，打卡时间：{get_current_time()}")
            else:
                st.error("工号不存在，请确认后重试")
    except Exception as e:
        st.error(f"数据插入失败： {e}")



def delete_old_attendence_records(conn):
    try:
        with conn.cursor() as cursor:
            # 删除前一天的打卡记录
            delete_sql = "DELETE FROM attendence WHERE time < %s"
            cursor.execute(delete_sql, (datetime.date.today(),))
            conn.commit()
    except Exception as e:
        st.error(f"删除旧打卡记录失败: {e}")

def capture_image():
    img_file_buffer = st.camera_input("请正视摄像头")
    if img_file_buffer is not None:
        img = Image.open(img_file_buffer)
        st.image(img, caption='上传图片', use_column_width=True)
        img_array = np.array(img)
        return img_array

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

if __name__ == '__main__':
    main()
