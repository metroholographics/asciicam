import numpy as np
import cv2 as cv
import time

font = cv.FONT_HERSHEY_PLAIN

#ascii_chars = '''  .:-=+*#%@'''
ascii_chars = ''' .`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'''

desired_fps = 30
frame_time = 1 / desired_fps

def main():
	cap = cv.VideoCapture(0)
	if not cap.isOpened():
		print("Cannot open camera")
		exit()

	height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
	width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
	channels = 3
	

	while True:
		start_time = time.time()
		ret, frame = cap.read()

		if not ret:
			print("Can't recieve frame (stream end?). Exiting...")
			break
		gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

		#print(gray[100,100])
		ascii_img = np.zeros((height, width, channels), dtype=np.uint8)
		for i in range(0, frame.shape[1], 5):
			for j in range(0, frame.shape[0], 5):
				#print(i,j)
				#val = int((0.5 * max(frame[j, i]) + 0.5 * min(frame[j, i])))
				val = gray[j,i]
				if val < 110:
					char = ascii_chars[val % len(ascii_chars)]
					cv.putText(ascii_img, char, (i,j), font, 0.5, (255,255,255),1, cv.LINE_AA)

		cv.imshow('ascii_img', ascii_img)

		elapsed = time.time() - start_time
		if elapsed < frame_time:
			time.sleep(frame_time - elapsed)

		if cv.waitKey(1) == ord('q'):
			break

	cap.release()
	cv.destroyAllWindows()

if __name__ == "__main__":
	main()