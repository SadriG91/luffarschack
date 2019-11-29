#import itertools
#from pathlib import Path
import tkinter as tk
import tkinter.messagebox as messagebox
import numpy as np
import pandas as pd
from get_size import get_grid_size
#import time
#import re
import os
import threading
import socket


# Here we define our variables that we will be using
size = get_grid_size()
host = '127.0.0.1'
port = 62222
s = None
connection_established = False
conn, addr = None, None


def connect_to_socket(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print("Connected to {host}:{port}".format(host=host, port=port))
    return sock

def listen_to_socket(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(1)
    print("Listening to {host}:{port}".format(host=host, port=port))
    return sock

def receive_data():
    while True:
        #if (connection_established is True and conn):
        if (os.getenv('GAME_MODE', None) == "server"):
            data = conn.recv(1024).decode()
        elif(os.getenv('GAME_MODE', None) == "client"):
            data = sock.recv(1024).decode()
        else:
            data = sock.recv(1024).decode()
        print(data)
        data_split = data.split('-')
        received_position = int(data_split[0])
        received_player = str(data_split[1])
        if received_player != app.player:
            blocked_buttons = app.buttons
            for button in blocked_buttons:
                button.config(state=tk.DISABLED)
        else:
            pass
        app.mark_button(received_position, received_player)



def waiting_for_connection():
    global connection_established, conn, addr
    conn, addr = sock.accept() #wait for connection, blocking method
    print("Client has joined succesfully!")
    connection_established = True
    receive_data()


received_position = None
received_player = None



if (os.getenv('GAME_MODE', None) == "client"):
    sock = connect_to_socket(host, port)
    t = threading.Thread(target=receive_data)
    t.daemon = True
    t.start()
elif (os.getenv('GAME_MODE', None) == "server"):
    sock = listen_to_socket(host, port)
    t = threading.Thread(target=waiting_for_connection)
    t.daemon = True
    t.start()
else:
    sock = connect_to_socket(host, port)





# This is the class where we create our GUI for the game 
class luffarschackApp(tk.Frame):
    
    board = [ None ] * size * size
    buttons = [ None ] * size * size

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        #self.players = itertools.cycle(["X", "O"])
        if (os.getenv('GAME_MODE', None) == "server"):
            self.player = "X"
        if (os.getenv('GAME_MODE', None) == "client"):
            self.player = "O"
        #self.socket = socket
        self.create_board()
        
        
    
    def get_command_fn(self, button, row, col):
        def on_click():
            position = row * size + col
            button["text"] = self.board[position] = self.player
            button.config(state=tk.DISABLED)
            send_data = "{}-{}".format(position, self.player).encode()
            if (os.getenv('GAME_MODE', None) == "client"): 
                sock.send(send_data)
            if (os.getenv('GAME_MODE', None) == "server"):
                conn.send(send_data)
            win_game=False
            
            
            if has_won(self.board, self.player):
                win_game=True
                messagebox.showinfo("Game Over", "Player {} won the game".format(self.player))         
                root.destroy()

            if is_draw(self.board) and win_game == False:
                messagebox.showinfo("Game Over", "It's a draw!")
                root.destroy()
            
            #self.player = next(self.players)
        return on_click


    def client_exit(self):
        exit()


    def create_board(self):
        
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)
        file = tk.Menu(menu)
        file.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label="File", menu=file)

        for position in range(size*size):
            button = tk.Button(self, text=" ")
            row= position // size
            column = position % size
            button.grid(row=row, column=column)
            button["command"] = self.get_command_fn(button, row, column)
            button.config(width=5, height=2)
            self.buttons[position] = button


    def mark_button(self, position, player):
        marked_button = self.buttons[position]
        marked_button["text"] = player
        marked_button.config(state=tk.DISABLED)

 
# This function checks if it's draw
def is_draw(board):
    return all (board[position] is not None for position in range (size*size))
    
# This function checks if a player have won
def has_won(board, player):
    def has_combination(combination, symbol):
        return all(board[row * size + col] == symbol for row, col in combination)

    if size == 3:

        winning_patterns = [
        lambda row, col: [(row-1, col), (row, col), (row+1, col)] if 0 < row < size-1 else None,
        lambda row, col: [(row, col-1), (row, col), (row, col+1)] if 0 < col < size-1 else None,
        lambda row, col: [(row-1, col-1), (row, col), (row+1, col+1)] if 0 < row < size-1 and 0 < col < size-1 else None,
        lambda row, col: [(row-1, col+1), (row, col), (row+1, col-1)] if 0 < row < size-1 and 0 < col < size-1 else None,
        ]

    elif size == 15:
        winning_patterns = [
        lambda row, col: [(row-2, col), (row-1, col), (row, col), (row+1, col), (row+2, col)] if 1 < row < size-2 else None,
        lambda row, col: [(row, col-2), (row, col-1), (row, col), (row, col+1), (row, col+2)] if 1 < col < size-2 else None,
        lambda row, col: [(row-2, col-2), (row-1, col-1), (row, col), (row+1, col+1), (row+2, col+2)] if 1 < row < size-2 and 1 < col < size-2 else None,
        lambda row, col: [(row-2, col+2), (row-1, col+1), (row, col), (row+1, col-1), (row+2, col-2)] if 1 < row < size-2 and 1 < col < size-2 else None,
        ]
    
    combinations = (pattern(position // size, position % size) for pattern in winning_patterns for position in range (size*size))
    return any (has_combination(combination, player) for combination in combinations if combination is not None)




root = tk.Tk()
root.iconbitmap("icon.ico")
root.title("Luffarschack " + os.getenv('GAME_MODE', "client"))
root.minsize(250,200)
app = luffarschackApp(master=root)


app.mainloop()