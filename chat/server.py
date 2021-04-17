import socket,select
port = 12345
socket_list = []
users = {}
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('',port))
server_socket.listen(5)
socket_list.append(server_socket)
while True:
    ready_to_read,ready_to_write,in_error = select.select(socket_list,[],[],0)
    
    for sock in ready_to_read:
        if sock == server_socket:
            connect, addr = server_socket.accept()
            socket_list.append(connect)
            connect.send(("You are connected from:" + str(addr)).encode())
        else:
            try:
                data = str(sock.recv(2048))
                print(data) #optional: only if you want to see the messages
                
                if (data.startswith("b'#")):
                    users[data[3:-1].lower()]=connect
                    print ("User " + data[3:-1] +" added.")
                    connect.send(("Your user detail saved as : "+str(data[3:-1])).encode())
                elif (data.startswith("b'@")):
                    print(data[data.index(':')+1:data.index('|')])
                    users[data[3:data.index(':')].lower()].send((data[data.index('|')+1:-1].lower() + ": " + data[data.index(':')+1:data.index('|')]).encode())
            except:
                continue
server_socket.close()
