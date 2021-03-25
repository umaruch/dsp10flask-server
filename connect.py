import json
import netifaces
import uuid
import socket

MAC_ADDRESS = ":".join(["{:02x}".format((uuid.getnode() >> ele) & 0xff) \
	for ele in range(0,8*6,8)][::-1])

def get_data():
	def_gw_device = netifaces.gateways()['default'][netifaces.AF_INET][1]

	ip_address = netifaces.ifaddresses(def_gw_device)[netifaces.AF_INET][0]["addr"]
	try:
		with open("devicename.txt", "r") as file:
			name = file.readline()
	except FileNotFoundError:
		with open("devicename.txt", "w") as file:
			file.write("DefaultName")
			name = "DefaultName"

	return json.dumps({
		"name": name,
		"address": ip_address,
		"mac": MAC_ADDRESS
	})


print(get_data())

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 2)

server.bind(("",65000))
print("Server started")

while True:
	try:
		conn, addr = server.recvfrom(1024)
		print("UDP message from ", addr)
		data = str.encode(get_data())
		server.sendto(data, (addr[0], 65001))
	except KeyboardInterrupt:
		break

server.close()

