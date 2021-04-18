import socket
import PySimpleGUI as sg


def create_menu_window():
    layout = [  [sg.Text('Welcome to ChatPy')],
            [sg.Text('Enter your username'), sg.InputText()],
            [sg.Button('Ok'), sg.Button('Exit'), sg.Button('Change theme')] ]

    window = sg.Window('ChatPy', layout)

    return window

def create_options_window():
    layout = [ [sg.Text('Theme')],
            [sg.Combo(sg.theme_list(), size=(20, 20), key='-THEME-')],
            [sg.Button('Set'), sg.Button('Exit')] ]

    window = sg.Window('ChatPy', layout)

    return window

def main():

    sg.theme('DarkBlue1') # theme

    client_socket = socket.socket()
    port = 12345
    client_socket.connect(('127.0.0.1',port))
    recv_msg = client_socket.recv(1024)
    print(recv_msg)

    window = create_menu_window()
    print("TEST")

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks exit
            break
        elif event == "Change theme":
            window.close()
            window2 = create_options_window()
            event2, values2 = window2.read()
            while True:
                if event2 == sg.WIN_CLOSED or event2 == 'Exit': # if user closes window or clicks exit
                    break
                elif event2 == 'Set':
                    sg.theme(values2['-THEME-']) # set the theme
                    sg.popup('Theme changed')
                    break
            window2.close()
            window = create_menu_window()
            event, values = window.read()
            
        elif event == "Ok":
            print(values[0])
            if values[0] is not None:
                client_socket.send(("#"+values[0]).encode())
                username=str(values[0])
                break

    #send_msg = input("Enter your user name: ")

    window.close()

    layout = [  [sg.Text('Messages received')],
                [sg.Multiline(size=(50, 5), disabled=True, key='_textbox_')],
                [sg.Text('Send a message')],
                [sg.Text('Enter the addressee\'s username'), sg.InputText()],
                [sg.Text('Enter the message'), sg.InputText()],
                [sg.Button('Send'), sg.Button('Exit')] ]

    window = sg.Window('ChatPy', layout)

    while True:
        event, values = window.read()
        recv_msg = client_socket.recv(1024)
        recv_msg=str(recv_msg)
        if recv_msg: # not empty strings
            window.Element('_textbox_').Update(window.Element('_textbox_').get() + recv_msg[2:-1]) # append function
        #window.Element('_textbox_').Update(recv_msg[2:-1]) # not append function
        
        if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks exit
            break
        elif event == 'Send':
            client_socket.send(("@" + values[0] + ":" + values[1] + "|" + username).encode())

    window.close()    
    client_socket.close()
main()
    
