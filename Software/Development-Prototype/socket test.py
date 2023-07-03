import socket
import time


if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 65431

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket:
        socket.connect((HOST, PORT))
        again = True
        while again:
            choice = input("Send or receive?")
            if choice == "1":
                message = input("Enter message:").encode()
                socket.send(message)
            else:
                print(socket.recv(7).decode())
            again = int(input("Again?"))
        # while True:
        #     socket.listen()
        #     player_one, player_one_address = socket.accept()
        #     player_one.sendall("What is your name?".encode())
        #     print(player_one_address)
        #     # data = player_one.recv(1024).decode()
        #     # print(data)
        #     # player_one.sendall(f"{data} my habibi".encode())
        #     player_one.close()
