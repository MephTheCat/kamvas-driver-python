from usb_device   import *
from huion_tablet import *
from evdev_tablet import *
from time         import sleep
from math         import exp

import xrandr_helper
import config as cfg

def main():
	tablet = HuionTablet(cfg.vendor, cfg.product)
	evtab  = EvdevTablet(cfg.pen_name)
	
	if not tablet.setup():
		print("Unable to setup tablet")
		return False
	
	if cfg.use_xrandr:
		print("Using XRandR to configure tablet")
		
		outputs = xrandr_helper.xrandr_get_outputs()
		screen  = xrandr_helper.xrandr_get_screen()
		
		if (cfg.mapped_display in outputs) and (outputs[cfg.mapped_display]['connected']):
			print("-- Found connected output {0}".format(cfg.mapped_display))
			
			output = outputs[cfg.mapped_display]
			
			cfg.virtual_screen_res = screen['size']
			cfg.tablet_res         = output['size']
			cfg.tablet_screen_pos  = output['offset']
			
		else:
			if cfg.mapped_display in outputs:
				print("-- Output {0} found, but not connected".format(cfg.mapped_display))
			else:
				print("-- Output {0} not found".format(cfg.mapped_display))
			print("Defaulting to manual configuration")
	
	
	bus, address = tablet.get_bus_address()
	print("Found Tablet")
	print("-- Bus/Address  : {0}/{1}".format(bus, address))
	print("-- Product      : {0}".format(tablet.usb_device.get_product()))
	print("-- Firmware     : {0}".format(tablet.descriptors[0xC9]))
	print("-- Internal Mfgr: {0}".format(tablet.descriptors[0xCA]))
	
	if not evtab.setup():
		print("Unable to setup emulated tablet")
		return False
	
	print("Emulated Tablet Setup")
	print("-- Virtual screen resolution: {0}x{1}".format(*(cfg.virtual_screen_res)))
	print("-- Tablet mapped resolution : {0}x{1}".format(*(cfg.tablet_res)))
	print("-- Tablet mapped offset     : ({0}, {1})".format(*(cfg.tablet_screen_pos)))
	
	countdown = 1
	print("Sleeping {0} seconds".format(countdown))
	for i in range(countdown):
		#print(countdown-i, flush=True, end=("\n" if i==(countdown-1) else " "))
		sleep(1)
	
	print("Started the Huion Evdev Userspace Driver")
	
	poll_loop(tablet, evtab)

def poll_loop(tablet, evtab):
	history = []
	
	while not sleep(cfg.driver_update_sec):
		try:
			packet = tablet.poll()
			
			interp = tablet.interpret_packet(packet)
				
			pt = interp['coords']
			
			history.append(pt)
			
			if len(history) >= cfg.averaging_length:
				history = history[-cfg.averaging_length:]
			
			pt = [sum(x)/len(x) for x in zip(*history)]
			
			px = compute_pixel_location(pt)
			
			evtab.send_pen_active()
			evtab.send(interp['hovering'], px, interp['pressure'], interp['tilt'], interp['pen_buttons'], interp['face_buttons'])
			
		except usb.core.USBError as e:
			if e.errno == 110: # Timeout.  Pen lifted?
				evtab.send_pen_inactive()
				continue
			elif e.errno == 5: # I/O Error, tablet disconnected?
				print("Tablet disconnected")
				return
		except KeyboardInterrupt:
			print("Shutting down")
			return
	

def range_lerp(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

def compute_pixel_location(pt):
	x, y       = pt
	px_x, px_y = 0, 0
	
	# Limit X value to the calibration values
	if (x < cfg.tablet_min[0]):
		px_x = 0
	elif (x > cfg.tablet_max[0]):
		px_x = cfg.tablet_res[0]
	else:
		# If it's in the valid range, lerp the raw value to a pixel value relative to the tablet
		px_x = range_lerp(x + cfg.tablet_pre_offset[0], cfg.tablet_min[0], cfg.tablet_max[0], 0, cfg.tablet_res[0])
		px_x += cfg.tablet_post_offset[0]
	
	# Limit Y value to the calibration values
	if (y < cfg.tablet_min[1]):
		px_y = 0
	elif (y > cfg.tablet_max[1]):
		px_y = cfg.tablet_res[1]
	else:
		# If it's in the valid range, lerp the raw value to a pixel value relative to the tablet
		px_y = range_lerp(y + cfg.tablet_pre_offset[1], cfg.tablet_min[1], cfg.tablet_max[1], 0, cfg.tablet_res[1])
		px_y += cfg.tablet_post_offset[1]
	
	# Add the tablet screen offset to get the global cursor position
	px_x = int(px_x + cfg.tablet_screen_pos[0])
	px_y = int(px_y + cfg.tablet_screen_pos[1])
	
	return (px_x, px_y)

if __name__ == "__main__":
	main()
