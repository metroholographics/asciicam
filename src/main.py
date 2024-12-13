import numpy as np
import cv2 as cv
import time

font = cv.FONT_HERSHEY_PLAIN

#ascii_chars = '''  .:-=+*#%@'''
ascii_chars = ''' .`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'''

desired_fps = 12
frame_time = 1 / desired_fps

step = 15
intensity_threshold = 200
COLOR_WHITE = (255,255,255)

def main():
	cap = cv.VideoCapture(0)
	if not cap.isOpened():
		print("Cannot open camera")
		exit()

	height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
	width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
	channels = 3
	
	prev = 0;

	while True:
		time_elapsed = time.time() - prev;
		ret, frame = cap.read()

		if not ret:
			print("Can't recieve frame (stream end?). Exiting...")
			break

		if time_elapsed > frame_time:
			prev = time.time()
			gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

			ascii_img = np.zeros((height, width, channels), dtype=np.uint8)
			for i in range(0, frame.shape[1], step):
				for j in range(0, frame.shape[0], step):
					b = int(frame[j,i,0])
					g = int(frame[j,i,1])
					r = int(frame[j,i,2])
					frame_color = (b,g,r)

					val = gray[j,i]
					if val < intensity_threshold:
						char = ascii_chars[val % len(ascii_chars)]
						cv.putText(ascii_img, char, (i,j), font, 0.7, frame_color ,1, cv.LINE_AA)

			cv.imshow('ascii_img', ascii_img)

		if cv.waitKey(1) == ord('q'):
			break

	cap.release()
	cv.destroyAllWindows()

if __name__ == "__main__":
	main()