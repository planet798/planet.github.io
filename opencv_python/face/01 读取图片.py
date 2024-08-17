 #导入cv模块
import cv2 as cv
#读取图片
img = cv.imread('th.jpg')
#显示图片
cv.imshow('read.jpg',img)
#等待
cv.waitKey(0)
#释放内存
cv.destroyAllWindows()