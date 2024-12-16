from engine import *

desired_fps = 15
app_state = App("ascii*cam",desired_fps)

COLOR_WHITE = (255,255,255)
font = cv.FONT_HERSHEY_PLAIN
ascii_char_short = '''  .:-=+*#%@'''
ascii_char_long = ''' .`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'''
font_size = 0.7
step = 10
intensity_threshold = 255

ascii_img = Ascii_Img(font, font_size, COLOR_WHITE, ascii_char_short, step, intensity_threshold)

def main():
	app_state.init_camera(0)

	while app_state.running:
		app_state.update_elapsed_time()

		ret, app_state.frame = app_state.cap.read()
		if not ret:
			print("Can't recieve frame (stream end?). Exiting...")
			break

		ascii_img.reset(app_state.height, app_state.width, app_state.channels) 

		if app_state.elapsed_time > app_state.frame_time:
			app_state.update_previous_time()
			gray_frame = app_state.get_grayscale_frame()
			
			for i in range(0, app_state.width, ascii_img.step):
				for j in range(0, app_state.height, ascii_img.step):
					frame_color = app_state.get_pixel_color(j, i)
					val = gray_frame[j,i]
					if val < ascii_img.intensity:
						ascii_img.draw_pixel_text(ascii_img.get_char(val), (i, j), frame_color)
			app_state.display_ascii_frame(ascii_img.frame)

		app_state.check_quit()

	end_app(app_state)


def end_app(app):
	if (app.cap):
		print("Releasing camera...")
		app.cap.release()
	cv.destroyAllWindows()

if __name__ == "__main__":
	main()