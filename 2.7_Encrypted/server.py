"""
Author: Harel Teva Artzy

Program name: Socket Server

Description: Connects to a client and gets one of 4 commands from them: TIME, RAND, NAME, or EXIT and sends the
client the answer (the time, a random 1-10 number, the server's name or disconnects the client). The server
can hold up to 1 client at a time but infinite clients 1 after 1 while running.

Date: 27/10/2025
"""


import socket
import os
import logging
from cryptography.fernet import InvalidToken
from functions import *
from protocol import *


QUEUE_LEN = 1
IP = '0.0.0.0'
PORT = 8081


def main():
    """
    A function that starts up a server on the computer and can be connected to a client from any ip. The client sends a command
    and the server checks if the command is known to it. The server can have 1 client at a time but infinite clients and commands per client.
    """
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        my_socket.bind((IP, PORT))
        my_socket.listen(QUEUE_LEN)
        logging.info("Server is up and running")
        print("Server is up and running")

        while True:
            client_socket, client_address = my_socket.accept()
            logging.info(f"Connection established with {client_address}")
            print(f"Connection established with {client_address}")

            try:
                cipher = server_handshake(client_socket)
                while True:
                    command, data = protocol_recv(client_socket, cipher)
                    request = str(command) + " " +  str(data)
                    logging.info(f"Server received {request}")

                    if not request:
                        logging.info("Client closed the connection")
                        break

                    if is_valid(command):
                        if command != "EXIT":
                            called_func = ("cmd_" + command).lower()
                            func = globals()[called_func]
                            answer = func(data.decode())

                        else:
                            answer = "Disconnected Client".encode()
                            logging.info("Connection closed")
                            print("Connection closed")

                    else:
                        logging.warning("Invalid command")
                        print("Invalid command")
                        answer = "Invalid command".encode()
                        command = "INVALID"

                    protocol_send(client_socket, cipher, command, answer)
                    if command == "EXIT":
                        break

            except (OSError, ValueError, InvalidToken) as err:
                logging.error('received socket error on client socket' + str(err))
                print('received socket error on client socket' + str(err))
            finally:
                client_socket.close()
    except socket.error as err:
        logging.error('received socket error on client socket' + str(err))
        print('received socket error on server socket' + str(err))
    finally:
        my_socket.close()
        logging.info("Server closed")


if __name__ == "__main__":
    # logging
    logging.basicConfig(
        filename="Server-Client.log",
        filemode="a",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.info("All asserts passed")
    main()