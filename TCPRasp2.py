# Import socket module
import socket


def Main():
    # local host IP '127.0.0.1'
    host = '127.0.0.1'

    # Define the port on which you want to connect
    port = 12346

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to server on local computer
    s.connect((host, port))

    # message you send to server
    message = "0;RASP;127.0.0.1;CAR;"

    s.send(message.encode('utf-8'))
    print("Message send ", str(message.encode('utf-8')))

    index = 1

    while True:

        # messaga received from server
        data = s.recv(1024)
        print(data.decode('utf-8'))
        # print the received message
        # here it would be a reverse of sent message

        if data.decode('utf-8') == "close":
            break
    # close the connection
    s.close()


if __name__ == '__main__':
    Main()
