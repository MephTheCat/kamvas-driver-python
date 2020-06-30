from libevdev import *
import config as cfg

class EvdevTablet:
	def __init__(self, dev_name):
		self.v_input = None
		self.name    = dev_name
		self.buttons = [False, False, False, False, False, False, False, False]
	
	def setup(self):
		dev = Device()
		dev.name = self.name
		
		dev.enable(INPUT_PROP_DIRECT)
		dev.enable(EV_KEY.BTN_TOUCH)
		dev.enable(EV_KEY.BTN_TOOL_PEN)
		dev.enable(EV_KEY.BTN_STYLUS)
		dev.enable(EV_KEY.BTN_STYLUS2)
		
		dev.enable(EV_ABS.ABS_X, InputAbsInfo(minimum=0, maximum=cfg.virtual_screen_res[0]))
		dev.enable(EV_ABS.ABS_Y, InputAbsInfo(minimum=0, maximum=cfg.virtual_screen_res[1]))
		dev.enable(EV_ABS.ABS_TILT_X, InputAbsInfo(minimum=cfg.pen_min_tilt, maximum=cfg.pen_max_tilt))
		dev.enable(EV_ABS.ABS_TILT_Y, InputAbsInfo(minimum=cfg.pen_min_tilt, maximum=cfg.pen_max_tilt))
		dev.enable(EV_ABS.ABS_PRESSURE, InputAbsInfo(minimum=0, maximum=cfg.tablet_max_pressure))
		
		for i in range(len(cfg.face_buttons)):
			if cfg.face_buttons[i] != None:
				if type(cfg.face_buttons[i]) is tuple:
					for evt in cfg.face_buttons[i]:
						dev.enable(evt)
				else:
					dev.enable(cfg.face_buttons[i])
		
		dev.enable(EV_SYN.SYN_REPORT)
		
		self.v_input = dev.create_uinput_device()
		if self.v_input:
			return True
	
	def send_pen_active(self):
		self.v_input.send_events([
			InputEvent(EV_KEY.BTN_TOOL_PEN, value=1),
			InputEvent(EV_SYN.SYN_REPORT, value=0)
		])
	
	def send_pen_inactive(self):
		self.v_input.send_events([
			InputEvent(EV_KEY.BTN_TOOL_PEN, value=0),
			InputEvent(EV_SYN.SYN_REPORT, value=0)
		])
	
	def send(self, hovering, pen_pos, pen_pressure, pen_tilt, pen_buttons, face_buttons):
		stylus_1 = pen_buttons[1]
		stylus_2 = pen_buttons[2]
		
		if cfg.stylus_btn_swap:
			stylus_1, stylus_2 = stylus_2, stylus_1
		
		events = [
			InputEvent(EV_ABS.ABS_X, value=pen_pos[0]),
			InputEvent(EV_ABS.ABS_Y, value=pen_pos[1]),
			InputEvent(EV_ABS.ABS_TILT_X, value=pen_tilt[0]),
			InputEvent(EV_ABS.ABS_TILT_Y, value=pen_tilt[1]),
			InputEvent(EV_ABS.ABS_PRESSURE, value=pen_pressure),
			
			InputEvent(EV_KEY.BTN_TOUCH, value=pen_buttons[0]),
			InputEvent(EV_KEY.BTN_STYLUS, value=stylus_1),
			InputEvent(EV_KEY.BTN_STYLUS2, value=stylus_2)
		]
		
		for i in range(len(face_buttons)):
			if i > len(cfg.face_buttons):
				break
			if face_buttons[i] != self.buttons[i]:
				if cfg.face_buttons[i] != None:
					if type(cfg.face_buttons[i]) is tuple:
						for evt in cfg.face_buttons[i]:
							events.append(InputEvent(evt, value=face_buttons[i]))
					else:
						events.append(InputEvent(cfg.face_buttons[i], value=face_buttons[i]))
		
		self.v_input.send_events(events + [InputEvent(EV_SYN.SYN_REPORT, value=0)])
		
		self.buttons = face_buttons
