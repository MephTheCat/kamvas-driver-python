import re
import subprocess

def xrandr_output_parse(line):
	r = re.search(r'^([\w+\-]+\d+)(\s+)(\w+)', line)
	
	if not r:
		return None
	
	output_name = r.group(1)
	connected   = r.group(3) == "connected"
	
	
	size        = (0, 0)
	offset      = (0, 0)
	primary     = False
	orientation = "normal"
	
	if connected:
		r       = re.search(r'^([\w+\-]+\d+)(\s+)(\w+)(\s+)(\w+)', line)
		primary = r.group(5) == "primary"
		
		r           = re.search(r'(\d+)x(\d+)\+(\d+)\+(\d+)(\s+)(\w+)?', line)
		size        = (int(r.group(1)), int(r.group(2)))
		offset      = (int(r.group(3)), int(r.group(4)))
		orientation = r.group(6) if r.group(6) else 'normal'
	
	ret = {
		'name'       : output_name,
		'connected'  : connected,
		'primary'    : primary,
		'size'       : size,
		'offset'     : offset,
		'orientation': orientation,
	}
	
	return ret

def xrandr_get_outputs():
	proc = subprocess.run("xrandr", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	
	if proc.returncode != 0:
		return None
	
	output = proc.stdout.decode('utf-8').split("\n")
	ret    = {}
	for line in output:
		info = xrandr_output_parse(line)
		if info:
			ret[info['name']] = info
	
	return ret

def xrandr_get_screen():
	proc = subprocess.run("xrandr", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	
	if proc.returncode != 0:
		return None
	
	output = proc.stdout.decode('utf-8').split("\n")[0]
	
	r = re.search(r'current\s+(\d+)\sx\s(\d+)', output)
	
	if not r:
		return None
	
	return {
		'size': (int(r.group(1)), int(r.group(2)))
	}

def main():
	print(xrandr_get_screen())
	out = xrandr_get_outputs()
	for key in out:
		print(out[key])

if __name__ == "__main__":
	main()
