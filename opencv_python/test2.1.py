import os.path
import streamlit as st
import cv2
import numpy as np
import face_recognition
from time import strftime, localtime
from PIL import Image

def get_current_time():
    return strftime("%Y-%m-%d %H:%M:%S", localtime())


def take_photo():
    # 捕获摄像头当前帧
    ret, frame = cap.read()
    if ret:
        # 转换颜色空间
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # 将图像转换为 numpy 数组，并确保是8位
        image_array = np.array(rgb_image, dtype=np.uint8)
        # 显示摄像头画面
        st.image(Image.fromarray(image_array), caption='上传图片', use_column_width=True)
    else:
        st.write("无法从摄像头捕获画面，请检查摄像头连接。")


st.sidebar.markdown(" ")
st.title("打卡界面")
id = st.text_input("请输入你的工号", key="id")
# 图片存储的基础路径
base_path = r"D:/opencv/capture_test"
# 按钮让用户提交工号
submit_button = st.button("提交")

# 使用Session State来跟踪按钮状态
if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = False


if submit_button:
    image_path = os.path.join(base_path, f"{id}.jpg")
    st.session_state.button_clicked = True
    if os.path.isfile(image_path):
        st.image(image_path, use_column_width= True)


states = False
if st.session_state.button_clicked:
    submit_button2 = st.button("拍照")
    if submit_button2:
        image_path = os.path.join(base_path, f"{id}.jpg")
        cap = cv2.VideoCapture(0)
        take_photo()
        ret,final_image = cap.read()
        if ret:
            cv2.imwrite(os.path.join(base_path, f"{id}_current.jpg"), final_image)

        known_face = face_recognition.load_image_file(image_path)
        known_face_encoding = face_recognition.face_encodings(known_face)[0]
        current_image = face_recognition.load_image_file(os.path.join(base_path, f"{id}_current.jpg"))
        current_face_encoding = face_recognition.face_encodings(current_image)[0]

        states = True

        if states:
            if current_face_encoding is not None:
                # submit_button3 = st.button("上传")
                results = face_recognition.compare_faces([known_face_encoding], current_face_encoding)
                if results[0]:
                    st.markdown(f"{id}打卡成功，打卡时间：{get_current_time()}")
                else:
                    st.error("打卡失败，请确定是本人操作")

        cap.release()