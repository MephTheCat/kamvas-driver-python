from usb_device   import *
from huion_tablet import *
from evdev_tablet import *
from time         import sleep

import config as cfg

def range_lerp(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

def compute_pixel_location(x, y):
	px_x, px_y = 0, 0
	
	if (x < cfg.tablet_min[0]):
		px_x = 0
	elif (x > cfg.tablet_max[0]):
		px_x = cfg.tablet_res[0]
	else:
		px_x = range_lerp(x + cfg.tablet_pre_offset[0], cfg.tablet_min[0], cfg.tablet_max[0], 0, cfg.tablet_res[0])
		px_x += cfg.tablet_post_offset[0]
	
	if (y < cfg.tablet_min[1]):
		px_y = 0
	elif (y > cfg.tablet_max[1]):
		px_y = cfg.tablet_res[1]
	else:
		px_y = range_lerp(y + cfg.tablet_pre_offset[1], cfg.tablet_min[1], cfg.tablet_max[1], 0, cfg.tablet_res[1])
		px_y += cfg.tablet_post_offset[1]
	
	px_x = int(px_x + cfg.tablet_screen_pos[0])
	px_y = int(px_y + cfg.tablet_screen_pos[1])
	
	return (px_x, px_y)

def main():
	tablet = HuionTablet(cfg.vendor, cfg.product)
	
	if not tablet.setup():
		print("Unable to setup tablet")
		return False
	
	print("Huion Kamvas Evdev Calibration Helper")
	print("Tap the pen on the screen, and the detected position is printed")
	
	try:
		down = False
		while not sleep(1.0/50.0):
			data = tablet.poll()
			data = tablet.interpret_packet(data)
			
			if data:
				if data["pen_buttons"][0] and not down:
					down = True
					x, y = data['coords'][0], data['coords'][1]
					print("Tap at ({0}, {1})".format(x, y))
				elif data["pen_buttons"][0] and down:
					down = False
	except KeyboardInterrupt:
		print("Shutting down")

if __name__ == "__main__":
	main()
