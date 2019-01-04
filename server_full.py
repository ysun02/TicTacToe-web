#!/usr/bin/python3
#
# Wesleyan University
# COMP 332, Fall 2018
# Homework 2: Distributed tic-tac-toe game

import binascii
import random
import socket
import sys
import threading

from tictactoe import *

class Server():
    """
    Server for TicTacToe game
    """

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.backlog = 1
        self.start()

    def start(self):
        # Init server socket to listen for connections
        try:
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_sock.bind((self.host, self.port))
            server_sock.listen(self.backlog)
        except OSError as e:
            print ("Unable to open server socket: ", e)
            if server_sock:
                server_sock.close()
                sys.exit(1)

        # Wait for client connection
        while True:
            client_conn, client_addr = server_sock.accept()
            print ('Client with address has connected', client_addr)
            thread = threading.Thread(target = self.play, args = (client_conn, client_addr))
            thread.start()

    def play(self, conn, addr):
        # Send game header to client
        str_data = "\n==================\n| TicTacToe Game |\n==================\n\n"
        print(str_data, end="")
        str_data = str_data + "Enter number of rows in TicTacToe board: "
        sock_write(conn, str_data)

        # Get number of rows from client
        str_data = sock_read(conn)
        game = TicTacToe(int(str_data))
        game.display('')

        # Play game
        while True:
            str_data = sock_read(conn)
            [row, col] = game.parse_choice(str_data)
            game.move(row, col, 'o')
            game.display('User')
            if game.check_done():
                break

            [row, col] = game.server_choose()
            game.move(row, col, 'x')
            game.display('Server')
            sock_write(conn, str(row) + ',' + str(col))
            if game.check_done():
                break
def main():

    server_host = 'localhost'
    server_port = 50007

    if len(sys.argv) > 1:
        proxy_host = sys.argv[1]
        proxy_port = int(sys.argv[2])

    s = Server(server_host, server_port)

if __name__ == '__main__':
    main()
