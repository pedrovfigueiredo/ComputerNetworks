import socket
import select
import os

serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_sock.bind(('localhost', 12345))
serv_sock.listen(1)
inputs = [serv_sock]
outputs = []
timeout = 1
while True:
	readable, writable, exceptional = select.select(inputs, outputs, inputs, timeout)

	for s in readable:
		if s is serv_sock:  # new client connect
			connection, client_address = serv_sock.accept()
			print('New client from %s:%d' % client_address)
			inputs.append(connection)
		else:
			data = s.recv(1024)
			if data:
				output = ''
				if data == 'DIR':
					for f in os.listdir('./'):
						output += f + '\n'
				elif data.startswith('DL'):
					filename = './' + data[3:]
					if os.path.isfile(filename):
						with open(filename, 'r') as f:
							output = f.read()
					elif os.path.isdir(filename):
						output = 'Error: Cannot download a directory'
					else:
						output = 'Error: File not found'
				elif data.startswith('FIND'):
					filename = './' + data[5:]
					output = str(os.path.isfile(filename))
				else:
					output = 'Command not found'

				s.sendall(output)
			else:
				s.close()
				inputs.remove(s)
