import socket
import struct

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 1234)
client_sock.connect(server_address)

values = (2, 5, b'+')
packer = struct.Struct('I I 1s')
packed_data = packer.pack(*values)


client_sock.sendall(packed_data)

data = client_sock.recv(1024)

unpacker = struct.Struct('I')
unpacked_data = unpacker.unpack(data)

print('Result: {}'.format(unpacked_data[0]))

client_sock.close()
