import usb.core
import usb.util

class USBDevice:
	def __init__(self, vendor_id, product_id):
		self.v_id       = vendor_id
		self.p_id       = product_id
		self.device     = None
		self.endpoints  = []
		self.interfaces = []
	
	def reset(self):
		if self.device:
			self.device.reset()
	
	def locate(self):
		self.device = usb.core.find(idVendor=self.v_id, idProduct=self.p_id)
		
		if not self.device:
			return False
		
		for config in self.device:
			for iface in config:
				self.interfaces.append(iface)
		
		for iface in self.interfaces:
			for endpoint in iface:
				if endpoint:
					self.endpoints.append(endpoint)
		
		return True
	
	def get_string_descriptor(self, idx):
		try:
			if self.device:
				return usb.util.get_string(self.device, idx)
			return None
		except usb.core.USBError as e:
			if e.errno == 32:
				return "Pipe Error"
		except UnicodeDecodeError as e:
			return "Unicode Error"
	
	def get_product(self):
		return self.get_string_descriptor(self.device.iProduct)
	
	def claim_interfaces(self):
		for iface in self.interfaces:
			if self.device.is_kernel_driver_active(iface.index):
				self.device.detach_kernel_driver(iface.index)
				usb.util.claim_interface(self.device, iface.index)
				
				print("Interface {0} claimed".format(iface.index))
		
		return True
	
	def read_endpoint(self, ep_id):
		if ep_id >= len(self.endpoints):
			return None
		
		ep = self.endpoints[ep_id]
		data = self.device.read(ep.bEndpointAddress, ep.wMaxPacketSize, timeout=100)
		
		return data
