import socket
client_socket = socket.socket()
port = 12345
client_socket.connect(('127.0.0.1',port))
recv_msg = client_socket.recv(1024)
print(recv_msg)
send_msg = input("Enter your user name(prefix with #):")
client_socket.send(send_msg.encode())

while True:
    recv_msg = client_socket.recv(1024)
    recv_msg=str(recv_msg)
    print(recv_msg[2:-1])
    
    send_msg = input("Send your message in format [@user:message] ")
    if send_msg == 'exit':
        break;
    else:
        client_socket.send(send_msg.encode())
    
client_socket.close()
