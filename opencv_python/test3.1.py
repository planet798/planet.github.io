import requests
import json
import base64
from PIL import Image
from io import BytesIO
import cv2
import streamlit as st

API_KEY = "jY3enrAfnPl1vdYP0XxdWIpm"
SECRET_KEY = "WI8nM3IB4kg9oU69nutzgaK0paajXXlS"

def main():
    st.sidebar.markdown(" ")
    st.title("打卡界面")
    user_id = st.text_input("请输入你的工号", key="id")
    submit_button = st.button("提交")
    if user_id and submit_button:
        # 根据工号读取图片
        image1_path = f"D:\\opencv\\capture_test\\{user_id}.jpg"
        image1 = Image.open(image1_path)

        # 从摄像头捕获一张图像并保存为image2
        image2 = capture_image()
        if image2 is not None:
            # 将捕获的图像保存到指定位置
            image2.save(f"D:\\opencv\\temp\\{user_id}_temp.jpg")

            # 将图片转换为base64编码
            buffered1 = BytesIO()
            buffered2 = BytesIO()
            image1.save(buffered1, format="JPEG")
            image2.save(buffered2, format="JPEG")
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

            st.write(response.text)
        else:
            st.write("未能捕获摄像头图像")

def capture_image():
    # 打开摄像头
    cap = cv2.VideoCapture(0)

    # 检查摄像头是否成功打开
    if not cap.isOpened():
        print("无法打开摄像头")
        return None

    # 从摄像头捕获一帧图像
    ret, frame = cap.read()

    # 释放摄像头资源
    cap.release()

    # 如果成功捕获到图像，则返回图像，否则返回None
    if ret:
        return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    else:
        return None

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
