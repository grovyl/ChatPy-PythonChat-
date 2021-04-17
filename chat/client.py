import socket
import PySimpleGUI as sg

sg.theme('DarkBlue1')

client_socket = socket.socket()
port = 12345
client_socket.connect(('127.0.0.1',port))
recv_msg = client_socket.recv(1024)
print(recv_msg)

layout = [  [sg.Text('Welcome to PyChat')],
            [sg.Text('Enter your username'), sg.InputText()],
            [sg.Button('Ok'), sg.Button('Exit')] ]

window = sg.Window('PyChat', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks exit
        break
    elif event == "Ok":
        print(values[0])
        if values[0] is not None:
            client_socket.send(("#"+values[0]).encode())
            username=str(values[0])
            break

#send_msg = input("Enter your user name: ")

window.close()

layout = [  [sg.Text('Send a message')],
            [sg.Text('Enter the addressee\'s username'), sg.InputText()],
            [sg.Text('Enter the message'), sg.InputText()],
            [sg.Multiline(size=(50, 5), disabled=True, key='_textbox_')],
            [sg.Button('Send'), sg.Button('Exit')] ]

window = sg.Window('PyChat', layout)

while True:
    event, values = window.read()
    recv_msg = client_socket.recv(1024)
    recv_msg=str(recv_msg)
    #window.Element('_textbox_').Update(window.Element('_textbox_').get() + "\n" + recv_msg[2:-1]) # append function
    window.Element('_textbox_').Update(recv_msg[2:-1])
    
    if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks exit
        break
    elif event == 'Send':
        client_socket.send(("@" + values[0] + ":" + values[1] + "|" + username).encode())

window.close()    
client_socket.close()
