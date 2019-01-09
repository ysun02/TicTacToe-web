#!/usr/bin/python3
#
# Wesleyan University
# COMP 332, Fall 2018
# Homework 2: Distributed tic-tac-toe game

import binascii
import random
import socket
import sys

def sock_read(sock):
    bin_data = b''
    while True:
        bin_data += sock.recv(4096)
        try:
            bin_data.decode('utf-8').index('DONE')
            break
        except ValueError:
            pass

    return bin_data[:-4].decode('utf-8')

def sock_write(sock, str_data):
    str_data = str_data + 'DONE'
    bin_data = str_data.encode('utf-8')
    sock.send(bin_data)

class Board():
    """
    TicTacToe game board
    """

    def __init__(self, n):
        self.n = n
        self.null = '_'
        self.board = [[self.null for i in range(n)] for j in range(n)]

    def mark_square(self, row, col, user):
        self.board[row][col] = user

    def empty_square(self, row, col):
        if self.board[row][col] == self.null:
            return True
        else:
            return False

    def check_full(self):
        for row in range(self.n):
            for col in range(self.n):
                if self.board[row][col] == self.null:
                    return False
        return True

    def check_winner(self):
        # Check rows
        for row in range(self.n):
            symbol = self.board[row][0]
            winner = True
            for col in range(self.n):
                if self.board[row][col] != symbol:
                    winner = False
                    break
            if winner == True and symbol != self.null:
                return symbol

        # Check columns
        for col in range(self.n):
            symbol = self.board[0][col]
            winner = True
            for row in range(self.n):
                if self.board[row][col] != symbol:
                    winner = False
                    break
            if winner == True and symbol != self.null:
                return symbol

        # Check diagonals
        symbol = self.board[0][0]
        winner = True
        for col in range(self.n):
            if self.board[col][col] != symbol:
                winner = False
                break
        if winner == True and symbol != self.null:
            return symbol

        symbol = self.board[0][self.n-1]
        winner = True
        for col in range(self.n):
            if self.board[col][self.n-col-1] != symbol:
                winner = False
                break

        if winner == True and symbol != self.null:
            return symbol

        return self.null

    def display_board(self, player):
        print(player)
        for row in range(self.n):
            for col in range(self.n):
                print(self.board[row][col], " ", end="")
            print("")

        print("")

class TicTacToe():
    """
    TicTacToe game
    """

    def __init__(self, n):
        self.n = n
        self.board = Board(n)

    def display(self, player):
        self.board.display_board(player)

    def check_done(self):
        win_status = self.board.check_winner()
        full_status = self.board.check_full()

        if win_status != self.board.null:
            print("Winner: ", win_status, "!")
            return True
        elif full_status == True:
            print('Game over: board is full')
            return True
        else:
            return False

    def valid_move(self, row, col):
        if self.board.empty_square(row, col):
            return True
        else:
            return False

    def query_user(self):
        string = "Choose row [0-" + str(self.n-1) + "]: "
        row = input(string)
        while int(row) < 0 or int(row) >= self.n:
            row = input("Enter row: ")

        string = "Choose col [0-" + str(self.n-1) + "]: "
        col = input(string)
        while int(col) < 0 or int(col) >= self.n:
            col = input("Enter col: ")

        return [int(row), int(col)]

    def user_choose(self):
        [row, col] = self.query_user()
        while self.valid_move(row, col) == False:
            [row, col] = self.query_user()
        return [row, col]

    def query_rand(self):
        row = random.randint(0, self.n - 1)
        col = random.randint(0, self.n - 1)
        return [row, col]

    def server_choose(self):
        [row, col] = self.query_rand()
        while self.valid_move(row, col) == False:
            [row, col] = self.query_rand()
        return[row, col]

    def move(self, row, col, marker):
        self.board.mark_square(row, col, marker)

    def parse_choice(self, str_data):
        [row, col] = str_data.split(',')
        return [int(row), int(col)]

