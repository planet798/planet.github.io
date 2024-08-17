# coding:utf-8
import json
import base64
import cv2
import urllib.request as urllib2

global token

def getToken():
    global token
    # 请替换以下client_id和client_secret为你自己的AK和SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=jY3enrAfnPl1vdYP0XxdWIpm&client_secret=WI8nM3IB4kg9oU69nutzgaK0paajXXlS'
    request = urllib2.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urllib2.urlopen(request)
    content = response.read()
    if (content):
        token = json.loads(content)['access_token']

def faceDetect(imgBase64):
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
    request_url = request_url + "?access_token=" + token
    request = urllib2.Request(request_url)
    request.add_header('Content-Type', 'application/json')
    # 将 imgBase64 转换为字符串
    imgBase64_str = imgBase64.decode('utf-8')
    data = json.dumps({"image": imgBase64_str, "image_type": "BASE64", "face_field": "age,beauty,expression,face_shape,gender"})
    response = urllib2.urlopen(request, data.encode('utf-8'))
    content = response.read()
    if content:
        return content

def imgToBase64(imgPath):
    with open(imgPath, "rb") as f:
        base64_data = base64.b64encode(f.read())
        return base64_data

if __name__ == "__main__":
    getToken()
    imgPath = r"D:\opencv\capture_test\001.jpg"
    imgBase64 = imgToBase64(imgPath)
    response_content = faceDetect(imgBase64)
    result = json.loads(response_content)['result']
    face_list = result['face_list'][0]
    location = face_list['location']
    age = face_list['age']
    beauty = face_list['beauty']
    expression = face_list['expression']['type']
    gender = face_list['gender']['type']

    img = cv2.imread(imgPath, cv2.IMREAD_COLOR)
    leftTopX = int(location['left'])
    leftTopY = int(location['top'])
    rightBottomX = int(leftTopX + location['width'])
    rightBottomY = int(leftTopY + location['height'])
    cv2.rectangle(img, (leftTopX, leftTopY), (rightBottomX, rightBottomY), (0, 255, 0), 2)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, "age:" + str(age), (leftTopX, leftTopY - 20), font, 0.5, (200, 255, 255), 1)
    cv2.putText(img, "gender:" + gender, (leftTopX, leftTopY - 40), font, 0.5, (200, 255, 255), 1)
    cv2.putText(img, "beauty:" + str(beauty), (leftTopX, leftTopY - 60), font, 0.5, (200, 255, 255), 1)
    cv2.putText(img, "expression:" + expression, (leftTopX, leftTopY - 80), font, 0.5, (200, 255, 255), 1)
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print("end")