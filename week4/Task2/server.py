import socket
import struct

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 1234)
server_sock.bind(server_address)
server_sock.listen(1)

client_sock, client_address = server_sock.accept()
print("New connection from: ")
print(client_address)

data = client_sock.recv(1024)
unpacker = struct.Struct('I I 1s')
unpacked_data = unpacker.unpack(data)

print('Processing data: {}'.format(unpacked_data))

n1 = unpacked_data[0]
n2 = unpacked_data[1]
operator = unpacked_data[2].decode('ascii')

if(operator == '+'):
    result = n1 + n2
elif(operator == '-'):
    result = n1 - n2
elif(operator == '*'):
    result = n1 * n2
elif(operator == '*'):
    result = n1 * n2
else:
    result = 0

packer = struct.Struct('I')
data_to_send = packer.pack(result)

client_sock.sendall(data_to_send)

client_sock.close()
server_sock.close()

