import time
import socket
import threading



class scanThread(threading.Thread):
	def __init__(self, ip, port_min=0, port_max=65535):
		threading.Thread.__init__(self)
		assert isinstance(port_max, int) and isinstance(port_min, int)
		self.ip = ip
		self.port_min = max(0, port_min)
		self.port_max = min(65535, port_max)

	def run(self):
		return self.__checker()

	def __checker(self):
		for port in range(self.port_min, self.port_max+1):
			self.__connect(port)

	def __connect(self, port):
		socket.setdefaulttimeout(1)
		s = socket.socket()
		try:
			t_start = time.time()
			s.connect((self.ip, port))
			t_end = time.time()
			flag = True
		except:
			flag = False
		s.close()
		if flag:
			connect_time = str(int((t_end - t_start) * 1000))
			info = 'Find --> [IP]: %s, [PORT]: %s, [Connect Time]: %s' % (self.ip, port, connect_time)
			print(info)
			self.__save(info)
		return flag
	
	def __save(self, content):
		if content:
			try:
				with open('results.txt', 'a') as f:
					f.write(content + '\n')
			except:
				time.sleep(0.1)


if __name__ == '__main__':
	ip = input('Input IP(example <xxx.xxx.xxx.xxx>):\n')
	port_min = input('Input Min Port(0 by default):\n')
	try:
		port_min = int(port_min)
	except:
		print('[Warning]: Enter min port error, use 0 by default...')
		port_min = 0
	port_max = input('Input Max Port(65535 by default):\n')
	try:
		port_max = int(port_max)
	except:
		print('[Warning]: Enter max port error, use 65535 by default...')
		port_max = 65535
	
	num = 8
	interval = (port_max - port_min) // num
	for i in range(interval):
		scanThread(ip, i * num, (i + 1) * num).start()