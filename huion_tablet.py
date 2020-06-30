import array
import struct
from   usb_device import *

class HuionTablet:
	def __init__(self, vendor_id, product_id, poll_timeout=1.0/5.0):
		self.v_id         = vendor_id
		self.p_id         = product_id
		self.usb_device   = USBDevice(self.v_id, self.p_id)
		self.poll_timeout = poll_timeout
		self.descriptors  = {
			0x64: None,
			0x65: None,
			0x6E: None,
			0x79: None,
			0x7A: None,
			0x7B: None,
			0xC8: None,
			0xC9: None,
			0xCA: None
		}
	
	def setup(self):
		if not self.usb_device.locate():
			print("Device {0:04x}:{1:04x} not found".format(self.v_id, self.p_id))
			return False
		
		self.usb_device.reset()
		
		if not self.usb_device.locate():
			print("Device {0:04x}:{1:04x} not found".format(self.v_id, self.p_id))
			return False
		
		if not self.usb_device.claim_interfaces():
			print("Unable to claim device {0:04x}:{1:04x}".format(self.v_id, self.p_id))
			return False
		
		# Originally, I prompted the user to call uclogic-probe
		# Having looked at what uclogic-probe actually does, working it in was trivial
		# Something about requesting the descriptors makes it work properly
		self.populate_descriptors()
		
		return True
	
	def get_bus_address(self):
		if self.usb_device:
			return (self.usb_device.device.bus, self.usb_device.device.address)
		return None
	
	def populate_descriptors(self):
		for desc in self.descriptors:
			self.descriptors[desc] = self.usb_device.get_string_descriptor(desc)
	
	def poll(self):
		try:
			packet = self.usb_device.read_endpoint(0)
			
			return packet
		except usb.core.USBError as e:
			raise
	
	def interpret_packet(self, packet):
		if len(packet) < 12:
			return None
		
		unpacked = struct.unpack("<BBHHHBBbb", packet.tobytes())
		
		coords = (unpacked[2] + (unpacked[5] * 0x10000), unpacked[3] + (unpacked[6] * 0x10000))
		
		out = {
			"report_id":   unpacked[0],
			"pen_buttons": [
				bool(unpacked[1] & 0b00000001),
				bool(unpacked[1] & 0b00000010),
				bool(unpacked[1] & 0b00000100),
				bool(unpacked[1] & 0b00001000),
			],
			"coords":      coords,
			"pressure":    unpacked[4],
			"tilt":        (unpacked[7], unpacked[8]),
			"hovering":    unpacked[1] == 128,
			"face_buttons": [bool((unpacked[1] == 224) and (coords[1] & x)) for x in [1, 2, 4, 8, 16, 32, 64, 128]]
		}
		
		return out
