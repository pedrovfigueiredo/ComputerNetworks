import socket

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect(('localhost', 12345))
while True:
    message = raw_input('Message: ')
    if message == 'EXIT':
        client_sock.close()
        break

    client_sock.sendall(message)
    response = client_sock.recv(1024 * 10)

    if message.startswith('DL') and (not response.startswith('Error')):
        filename = message[3:] + '_downloaded'
        with open(filename, 'w') as f:
            f.write(response)
            print filename + ' was created successfully'
    else:
        print response
