# -*- coding: utf-8 -*-
import streamlit as st
import re
import cv2  # 导入OpenCV库
import os
from PIL import Image


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

        photo = capture_and_save_photo(id)
        if photo:
            # 显示图片
            st.image(photo, caption=f'Photo of {name}', use_column_width=True)

    else:
        st.error("请输入正确的姓名和工号")