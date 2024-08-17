# -*- coding: utf-8 -*-
import streamlit as st
import psycopg2  # 假设使用psycopg2作为数据库连接库
import re
import cv2  # 导入OpenCV库
import os
from PIL import Image

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

# 检查id是否存在的函数
def check_id_exists(conn, id):
    with conn.cursor() as cursor:
        # 执行查询，检查id是否存在
        sql = "SELECT COUNT(*) FROM employees WHERE id = %s"
        cursor.execute(sql, (id,))
        return cursor.fetchone()[0] > 0


# 插入数据的函数
def insert_data(conn, id, name):
    try:
        if check_id_exists(conn, id):
            st.error("id已被占用，请重新输入")
            return  # 直接返回，不再执行插入操作
        with conn.cursor() as cursor:
            # st.write(f"准备插入的姓名: {name}")
            # 假设你的school数据源中有一个名为employees的表，包含id和name字段
            sql = "INSERT INTO employees (id, name) VALUES (%s, %s)"
            cursor.execute(sql, (id, name))
            conn.commit()
            st.write(f"恭喜{id} {name}成功入职！")
    except Exception as e:
        st.error(f"数据插入失败: {e}")


def capture_and_save_photo(id):
    save_path = "D:/opencv/capture_test"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    cap = cv2.VideoCapture(0)
    try:
        ret, frame = cap.read()
        if ret:
            filename = os.path.join(save_path, f"{id}.jpg")
            cv2.imwrite(filename, frame)
            print(f"Photo saved as {filename}")
            # 转换为PIL图像以在Streamlit中显示
            image = Image.open(filename)
            return image
        else:
            print("Failed to capture image")
            return None
    finally:
        cap.release()


# 主界面
st.sidebar.markdown(' ')
st.title("欢迎入职界面")

id = st.text_input("Your ID", key="id")
name = st.text_input("Your name", key="name")
submit_button = st.button("提交")

if submit_button:
    # 正则表达式匹配任意数量的中文字符或英文字母
    name_pattern = re.compile(r'^[\u4e00-\u9fa5a-zA-Z]*$')
    # 正则表达式匹配数字
    id_pattern = re.compile(r'^\d+$')

    if name_pattern.match(name) and id_pattern.match(id):
        # 连接数据库
        conn = connect_to_database(db_config)
        if conn:
            # 插入数据
            insert_data(conn, id, name)
            photo = capture_and_save_photo(id)
            if photo:
                # 显示图片
                st.image(photo, caption=f'Photo of {name}', use_column_width=True)
            # 关闭数据库连接
            conn.close()
    else:
        st.error("请输入正确的姓名和工号")