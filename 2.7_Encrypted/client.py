"""
Author: Harel Teva Artzy

Program name: Socket Client

Description: Connects to a server and sends it commands, it then receives the answers from the server and prints them.

Date: 27/10/2025
"""

import socket
import os
import logging
from cryptography.fernet import InvalidToken
from protocol import *


SERVER_IP = '127.0.0.1'
SERVER_PORT = 8081


def main():

    """
    A function that connects to a socket on the same computer and sends it a 4 letter long command, it then prints the response and logs it.
    It also stops when prompted "EXIT". The client can send infinite amount of commands.
    """
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        my_socket.connect((SERVER_IP, SERVER_PORT))
        cipher = client_handshake(my_socket)
        while True:
            msg = input("Enter a command: ")
            if " " in msg:
                cmd, data = msg.split(" ", 1)
            else:
                cmd = msg
                data = ""
            protocol_send(my_socket, cipher, cmd, data.encode())
            logging.info(f"Client sent {msg}")


            cmd, data = protocol_recv(my_socket, cipher)

            if cmd == "SCREENSHOT":
                logging.info(f"Client received {len(data)} bytes")
                with open("received_screen.jpg", "wb") as f:
                    f.write(data)

                print("Screenshot saved as received_screen.jpg")
                continue

            if cmd == "EXIT":
                logging.info(f"Client received {data}")
                print(data.decode())
                logging.info("Connection closed")
                break

            print(data.decode())
            logging.info(f"Client received {data}")

    except (OSError, ValueError, InvalidToken) as err:
        logging.error("socket error: " + str(err))
        print("socket error: " + str(err))
    finally:
        my_socket.close()

if __name__ == "__main__":
    # logging
    logging.basicConfig(
        filename="Server-Client.log",
        filemode="a",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    main()