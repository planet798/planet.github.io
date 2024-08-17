import cv2

class CaptureVideo(object):
	def net_video(self):
		# 获取网络视频流
		cam = cv2.VideoCapture("rtmp://mobliestream.c3tv.com:554/live/goodtv.sdp")
		while cam.isOpened():
			sucess, frame = cam.read()
			cv2.imshow("Network", frame)
			cv2.waitKey(1)
if __name__ == "__main__":
	capture_video = CaptureVideo()
	capture_video.net_video()