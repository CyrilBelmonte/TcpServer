# Import socket module
import socket


def Main():
    # local host IP '127.0.0.1'
    host = '127.0.0.1'
    # Define the port on which you want to connect
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to server on local computer
    s.connect((host, port))

    # message you send to server
    message = "Test"
    while True:

        # message sent to server
        s.send(message.encode('utf-8'))
        print("Message send ", str(message.encode('utf-8')))
        # messaga received from server
        data = s.recv(3000000)

        # print the received message
        # here it would be a reverse of sent message
        print('Received from the server :', str(data.decode('utf-8')))

        # ask the client whether he wants to continue
        ans = input('\nDo you want to continue(y/n) :')

        if ans == 'y':
            mess = input("Send ? ")
            s.send(mess.encode('utf-8'))
            continue
        else:
            break
    # close the connection
    s.close()


if __name__ == '__main__':
    Main()
