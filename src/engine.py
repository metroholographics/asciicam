import numpy as np
import cv2 as cv
import time

class App():
	def __init__(self, name, fps):
		self.name = name
		self.fps = fps
		self.frame_time = 1 / fps
		self.previous_time = 0
		self.elapsed_time = 0

		self.cap = None
		self.height = None
		self.width = None
		self.channels = 3
		self.frame = None
		self.running = True

	def init_camera(self, camera):
		cap = cv.VideoCapture(camera)
		if not cap.isOpened():
			print("Cannot open camera")
			exit()
		self.cap = cap
		self.width = self.get_capture_width()
		self.height = self.get_capture_height()

	def get_capture_height(self):
		return int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))

	def get_capture_width(self):
		return int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH))

	def update_elapsed_time(self):
		self.elapsed_time = time.time() - self.previous_time;

	def update_previous_time(self):
		self.previous_time = time.time()

	def get_grayscale_frame(self):
		return cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)

	def get_pixel_color(self, w, h):
		b = int(self.frame[w,h,0])
		g = int(self.frame[w,h,1])
		r = int(self.frame[w,h,2])
		return (b,g,r)

	def display_ascii_frame(self, frame):
		cv.imshow(self.name, frame)

	def check_quit(self):
		if cv.waitKey(1) == ord('q'):
			self.running = False

class Ascii_Img():
	def __init__(self, size, color, char_set, step, intensity):
		self.frame = None
		self.font = cv.FONT_HERSHEY_PLAIN
		self.size = size
		self.color = color
		self.char_set = char_set
		self.step = step
		self.intensity = intensity
		self.color_mode = 0

	def reset(self, height, width, channels):
		self.frame = np.zeros((height, width, channels), dtype=np.uint8)

	def get_char(self, val):
		scale = len(self.char_set) / 256
		index = int(val * scale)
		return self.char_set[min(index, len(self.char_set) - 1)]

	def draw_pixel_text(self, char, dest, color=False):
		if color:
			self.color = color
		cv.putText(self.frame, char, dest, self.font, self.size, self.color, 1, cv.LINE_AA)



