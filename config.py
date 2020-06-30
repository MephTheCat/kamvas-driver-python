from libevdev import *
from math     import exp

tablet_kamvas_13 = {
	"pen_name": "Huion Kamvas 13",
	"vendor"  : 0x256C,
	"product" : 0x006D,
	
	"use_xrandr"         : True,
	"mapped_display"     : "DisplayPort-0",
	
	"tablet_res"         : (1920, 1080),
	"tablet_pre_offset"  : (0, 0),
	"tablet_post_offset" : (0, 0),
	"tablet_max"         : (58749, 33500),
	"tablet_min"         : (247, 0),
	"tablet_screen_pos"  : (1600, 0),
	"tablet_pen_res"     : 5080,
	"tablet_max_pressure": 8191,
	
	"pen_min_tilt": -60,
	"pen_max_tilt": 60,
	
	"virtual_screen_res": [1600 + 1920, 1080],
	
	"face_buttons": [
		(EV_KEY.KEY_LEFTCTRL, EV_KEY.KEY_Z),
		None,
		None,
		None,
		None,
		None,
		None,
		None
	],
	
	"driver_update_sec": 1/500.0,
	"averaging_length": 8,
	
	"rotation":           "normal",
	"stylus_btn_swap":    True,
}

working_tablet = tablet_kamvas_13


pen_name            = working_tablet["pen_name"]
vendor              = working_tablet["vendor"]
product             = working_tablet["product"]
tablet_res          = working_tablet["tablet_res"]
tablet_pre_offset   = working_tablet["tablet_pre_offset"]
tablet_post_offset  = working_tablet["tablet_post_offset"]
tablet_max          = working_tablet["tablet_max"]
tablet_min          = working_tablet["tablet_min"]
tablet_screen_pos   = working_tablet["tablet_screen_pos"]
tablet_pen_res      = working_tablet["tablet_pen_res"]
tablet_max_pressure = working_tablet["tablet_max_pressure"]
pen_min_tilt        = working_tablet["pen_min_tilt"]
pen_max_tilt        = working_tablet["pen_max_tilt"]
virtual_screen_res  = working_tablet["virtual_screen_res"]
driver_update_sec   = working_tablet["driver_update_sec"]
face_buttons        = working_tablet["face_buttons"]
averaging_length    = working_tablet["averaging_length"]
rotation            = working_tablet["rotation"]
use_xrandr          = working_tablet["use_xrandr"]
mapped_display      = working_tablet["mapped_display"]
stylus_btn_swap     = working_tablet["stylus_btn_swap"]
