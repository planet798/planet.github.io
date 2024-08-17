import cv2
import os


# 读取指定文件夹下的所有图片文件
def read_images_from_folder(folder_path):
    images = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg"):
            img = cv2.imread(os.path.join(folder_path, filename))
            if img is not None:
                images.append(img)
    return images


# 预处理图片（例如缩放、灰度化等）
def preprocess_image(image):
    # 缩放图片
    #resized_image = cv2.resize(image, (100, 100))
    # 灰度化
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image


# 加载人脸识别模型（这里需要根据实际情况选择合适的模型）
face_cascade = cv2.CascadeClassifier('D:/opencv/opencv/sources/data/haarcascades/haarcascade_frontalface_default.xml')

# 读取采集到的人脸图片
folder_path = "D:/opencv/capture_test"
images = read_images_from_folder(folder_path)

# 对每张图片进行人脸识别
for image in images:
    gray_image = preprocess_image(image)
    faces = face_cascade.detectMultiScale(gray_image)

    # 在原图上绘制人脸矩形框并显示
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
    cv2.imshow("Faces found", image)
    cv2.waitKey(0)

cv2.destroyAllWindows()
