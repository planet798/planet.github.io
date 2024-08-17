English:

Hello everyone, this is my first time uploading a small project on GitHub, it's a coursework assignment from my university, and I also want to record it. The title is "Face Recognition Attendance Remote Punch Card Software".

The purpose of this project is to design the sending and receiving ends, based on the face recognition module and laptop camera, to develop a face recognition attendance remote punch card software. The sending end collects the facial video and sends it to the receiving end. On the receiving end, the face recognition module is used to identify the person. Note: It is to identify who the person is, not face detection. The identified person needs to be captured and stored in the database (punch-in time, name, using OpenGauss database). It is required to reproduce at least 2 face recognition technologies.

The software used in this project is mainly concentrated on Python, PyCharm, OpenGauss, DataStudio, and it is presented in the form of a webpage, by inserting Streamlit into PyCharm, which is a simple software for designing webpages, very easy to use, but it is difficult to design complex webpages.

The main program is divided into three parts, namely register.py and the pages folder's baiduapi.py, face.py, all three files need to be executed in the terminal by running 'streamlit run 'xxx', the rest of the test.py are for testing purposes and are not very useful. register.py is a simulated user registration page. When you input your ID number and name, you are considered registered. Then, the computer's webcam will take a photo of you as the registration photo, which will be named in the format "{id}.jpg" and saved to a certain folder for future facial recognition. When OpenGauss is running, the registered user data will be sent to the data source "school" in OpenGauss, so these tables must be created in advance. If the ID is repeated, an error will occur.

baiduapi.py is a method for facial recognition. I called the Baidu Cloud's facial recognition API and used the existing functions for facial recognition. face.py is the second method for facial recognition. I used the face_recognition library in Python and called the face_compare function to achieve the same facial recognition function.

The process of the two methods is actually similar. After running streamlit run xxx, a page will appear, which will ask you to input your ID number. Then, real-time video capture will be performed by calling the computer's webcam. Clicking "take photo" will capture the current photo and store it in temp_path. Then, the photo captured by register.py will be compared with the photo stored in temp_path. If the matching degree exceeds a certain threshold, it will display that you have successfully punched in, and it will display your ID number and name input in register.py, as well as the current local time. Of course, this information will also be stored in the database OpenGauss for attendance tracking. Another table in the school data source, attendence, will also need to be created in advance using SQL language.



中文：
    大家好，这是我第一次上传github的一个小项目，是我在大学里的一个课设作业，也是想记录一下，题目是“人脸识别考勤远程打卡软件 ”。
    本次项目旨在设计发送端、接收端两个部分，基于人脸识别模块和笔记本摄像头，开发人脸识别考勤远程打卡软件，发送端采集到人脸视频
并发给接收端，在接收端基于人脸识别模块完成人脸识别。注意：是识别出这个人是谁，不是人脸检测。识别出的人需要抓图并存入数据库
（打卡时间、人名，使用openGauss 数据库），要求复现至少 2 种人脸识别技术。
    本次项目用到的技术软件集中在python, pycharm, opengauss, datastudio，最后是以网页的形式呈现的，是在pycharm里面插入streamlit，
这是一个简单的设计网页的软件，十分精简好用，但是用来设计复杂的网页有些困难。
    主要程序分为三个部分分别为register.py和文件夹pages中的baiduapi.py, face.py，三个文件均需要在终端用streamlit run 'xxx'来执行，
其余的test.py均是测试用的，用处不大。
    register.py是一个模拟用户注册页面，输入自己的工号id和姓名name,就算是注册成功，然后电脑摄像头会拍摄一张当前的照片作为登记照片，
以'{id}.jpg'形式命名并且传到某一处文件夹为之后的人脸识别作铺垫；并且在opengauss开启的状况下，注册的用户数据会传入到opengauss里面的
数据源school中的一张表格employees中，所以这些表也要提前建好,如果id重复则会报错。
    baiduapi.py是一种实现人脸识别的方法，我调用了百度云的人脸识别api，利用现成的功能进行人脸识别；face.py则是第二种人脸识别的方法，
我利用了python中的face_recognition库，调用了其中的face_compare函数,同样也能达到人脸识别的功能。
    而两种方法的过程其实差不多，首先streamlit run xxx后出现页面，会让你输入工号id，然后则是通过调用电脑摄像头对你进行实时的视频采集，
点击take photo，会截取当时的照片并存储在temp_path，然后将这张截取的照片与之前register.py拍摄保存的照片进行比对，如果匹配程度超过
某一个阈值，则会显示打卡成功，并且会显示register.py输入的id和name，以及打卡的当地时间。当然打卡的这些信息同样也会存入到数据库opengauss中
school数据源的另一张表attendence中，所以也要提前用sql语言建好表格。
