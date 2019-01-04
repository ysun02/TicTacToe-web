#!/usr/bin/python3
#
# Wesleyan University
# COMP 332, Fall 2018
# Homework 2: Distributed tic-tac-toe game

import binascii
import random
import socket
import sys

from tictactoe import *

class Client:

    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.start()

    def start(self):
        server_sock = self.connect_to_server()
        self.play(server_sock)
        server_sock.close()

    def play(self, sock):

        # Read game header and print
        str_data = sock_read(sock)
        print(str_data)

        # Determine board size
        num_row = input()
        game = TicTacToe(int(num_row))
        game.display('')
        sock_write(sock, num_row)

        # Play game
        while True:
            [row, col] = game.user_choose()
            game.move(row, col, 'o')
            game.display('User')
            sock_write(sock, str(row) + ',' + str(col))
            if game.check_done():
                break

            str_data = sock_read(sock)
            [row, col] = game.parse_choice(str_data)
            game.move(row, col, 'x')
            game.display('Server')
            if game.check_done():
                break

    def connect_to_server(self):
        try:
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_sock.connect((self.server_host, self.server_port))
        except OSError as e:
            print("Unable to connect to socket: ", e)
            if server_sock:
                server_sock.close()
                sys.exit(1)

        return server_sock

def main():
    server_host = 'localhost'
    server_port = 50007

    if len(sys.argv) > 1:
        server_host = sys.argv[1]
        server_port = int(sys.argv[2])

    client = Client(server_host, server_port)

if __name__ == '__main__':
    main()
