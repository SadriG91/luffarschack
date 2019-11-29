import itertools
from pathlib import Path
import tkinter as tk
import tkinter.messagebox as messagebox
import numpy as np
import pandas as pd
from get_size import get_grid_size
import time
import re
import os


import threading


def create_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()





import socket

HOST = '127.0.0.1'
PORT = 62222
connection_established = False
conn, addr = None, None


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

def receive_data():
    while True:
        data = conn.recv(1024).decode()
        print(data)




def waiting_for_connection():
    global connection_established, conn, addr
    conn, addr = s.accept() #wait for connection, blocking method
    print("Client has joined succesfully!")
    connection_established = True
    receive_data()

create_thread(waiting_for_connection)


# This is to create files with today's date and time so 
# we can save games to those files
timestr = time.strftime("Score Board %Y_%m_%d_Time_%H_%M")
folder = Path('Record')
folder.mkdir(exist_ok=True)
record= open("Record\{}.txt".format(timestr),"w+")


# Here we define our variables that we will be using
size=get_grid_size()
board = [None]*(size*size)
games_played=0
moves_played=0
player_X_won=0
player_O_won=0
games_draw=0
number_of_plays=0
avg_moves_played=0
player_X_percentage_won=0
player_O_percentage_won=0
draw_percentage=0
draw_percentage=0
player_X_plays_win=0
player_O_plays_win=0
avg_plays_win_X=0
avg_plays_win_O=0
dataset=None

# This function will read our stats that we have previously saved
def import_stats(self):

    stats = open("Stats/stats.txt", "r+")
    lines=stats.readlines()

    if not len(lines)==0:
        first_line=lines[0]
        global games_played
        games_played=int(re.sub("\D", "", first_line))    
        second_line=lines[1]
        global moves_played
        moves_played=int(re.sub("\D", "", second_line))
        fourth_line=lines[3]
        global player_X_won
        player_X_won=int(re.sub("\D", "", fourth_line))
        fifth_line=lines[4]
        global player_X_plays_win
        player_X_plays_win=int(re.sub("\D", "", fifth_line))
        sixth_line=lines[5]
        global player_O_won
        player_O_won=int(re.sub("\D", "", sixth_line))
        seventh_line=lines[6]
        global player_O_plays_win
        player_O_plays_win=int(re.sub("\D", "", seventh_line))
        eighth_line=lines[7]
        global games_draw
        games_draw=int(re.sub("\D", "", eighth_line))
   

    
        
    if player_X_won == 0:
        player_X_percentage_won=0
        avg_plays_win_X=0
    else:
        player_X_percentage_won=float(float(player_X_won)/float(games_played)*100)
        avg_plays_win_X=player_X_plays_win/player_X_won

    if player_O_won == 0:
        player_O_percentage_won=0
        avg_plays_win_O=0
    else:
        player_O_percentage_won=float(float(player_O_won)/float(games_played)*100)
        avg_plays_win_O=player_O_plays_win/player_O_won
        
    if games_draw !=0:
        draw_percentage=float(float(games_draw)/float(games_played)*100)
        
    else:
        draw_percentage=0
        

    
    X_stats=[player_X_won, player_O_won, games_draw, player_X_percentage_won, draw_percentage, avg_plays_win_X ]
    O_stats=[player_O_won, player_X_won, games_draw, player_O_percentage_won, draw_percentage, avg_plays_win_O]
    array_X=np.array(X_stats)
    array_O=np.array(O_stats)
    global dataset
    dataset=pd.DataFrame((array_X, array_O), columns=["Wins", "Losses", "Draw", "Andel Win", "Andel Draw", "Avg plays for win"],
                                             index=["X", "O",])
    print(dataset)
    
# This function is very self explanatory and it basically deletes content of a file
def clearFile(file):
    file.seek(0)
    file.truncate()
# This function will write our statistics to the stats file
def write_to_history(self):
        folder = Path('Stats')
        folder.mkdir(exist_ok=True)
        stats = open("Stats/stats.txt", "w")    
        stats.write("Games played so far: {}.\n".format(games_played))
        stats.write("Number of moves played so far: {}.\n".format(moves_played))
        avg_moves_played=moves_played/games_played
        stats.write("Averages plays per game: {}.\n".format(avg_moves_played))
        stats.write("Player X has won: {} game(s).\n".format(player_X_won))
        stats.write("Player X played moves in games won: {}.\n".format(player_X_plays_win))
        stats.write("Player O has won: {} games(s).\n".format(player_O_won))
        stats.write("Player O played moves in games won: {}.\n".format(player_O_plays_win))
        stats.write("Games draw: {}.\n\n".format(games_draw))
        
        if player_X_won == 0:
            player_X_percentage_won=0
            avg_plays_win_X=0
        else:
            player_X_percentage_won=float(float(player_X_won)/float(games_played)*100)
            avg_plays_win_X=player_X_plays_win/player_X_won

        if player_O_won == 0:
            player_O_percentage_won=0
            avg_plays_win_O=0
        else:
            player_O_percentage_won=float(float(player_O_won)/float(games_played)*100)
            avg_plays_win_O=player_O_plays_win/player_O_won
        
        if games_draw !=0:
            draw_percentage=float(float(games_draw)/float(games_played)*100)
        
        else:
            draw_percentage=0

        X_stats=[player_X_won, player_O_won, games_draw, player_X_percentage_won, draw_percentage, player_X_plays_win, avg_plays_win_X ]
        O_stats=[player_O_won, player_X_won, games_draw, player_O_percentage_won, draw_percentage, player_X_plays_win, avg_plays_win_O]
        array_X=np.array(X_stats)
        array_O=np.array(O_stats)
        global dataset
        dataset=pd.DataFrame((array_X, array_O), columns=["Wins", "Losses", "Draw", "Andel Win", "Andel Draw","Moves in wins","Avg plays for win"],
                                                 index=["X", "O",])

        
        
        stats.write(dataset.to_string())
        stats.close()

# This is the class where we create our GUI for the game 
class luffarschackApp(tk.Frame):
    
    buttons = []
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.players = itertools.cycle(["X", "O"])
        self.player = next(self.players)
        self.create_board()
        import_stats(self)
        self.buttons = []

    def get_command_fn(self, button, row, col):
        
        def on_click():
            position = row * size + col
            button["text"] = board[position] = self.player
            button.config(state=tk.DISABLED)
            played_position=position+1
            if connection_established == True:
                send_data = "{}-{}-{}-{}-{}".format(row, size, col, self.player,button).encode()
                conn.send(send_data)
            win_game=False
            global number_of_plays
            number_of_plays=number_of_plays+1
            global games_played
            print("Play number {}.\n\n".format(number_of_plays))
            record.write("Play number {}.\n\n".format(number_of_plays))
            print("Player {} played position number {}.\n\n".format(self.player,played_position))
            record.write("Player {} played position number {}.\n\n".format(self.player,played_position))
            print_board(board)
            if has_won(board, self.player):
                win_game=True
                messagebox.showinfo("Game Over", "Player {} won the game".format(self.player))
                record.write("Player {} won the game!\n".format(self.player))
                record.write("Number of plays in game is {}.".format(number_of_plays))
                record.close()
                games_played=games_played+1
                print("Total number of games is {}.".format(games_played))
                global moves_played
                moves_played=moves_played+number_of_plays
                global avg_moves_played
                avg_moves_played=moves_played/games_played
                
            
                
                if self.player=="X":
                    global player_X_won
                    player_X_won=player_X_won+1
                    global player_X_plays_win
                    player_X_plays_win=player_X_plays_win+number_of_plays
                    print("Player X has won {} times.".format(player_X_won))
                        
                else:
                    global player_O_won
                    player_O_won=player_O_won+1
                    global player_O_plays_win
                    player_O_plays_win=player_O_plays_win+number_of_plays
                    print("Player O has won {} times.".format(player_O_won))
                    
                root.destroy()
                write_to_history(self)
            if is_draw(board) and win_game == False:
                messagebox.showinfo("Game Over", "It's a draw!")
                record.write("Number of plays in game is {}.".format(number_of_plays))
                record.close()
                games_played=games_played+1
                global games_draw
                games_draw=games_draw+1
                avg_moves_played=moves_played/games_played
                root.destroy()
                write_to_history(self)
            
            self.player = next(self.players)
        return on_click
        
      
    


    def client_exit(self):
        exit()

    def open_file(self):
        file=Path("stats/stats.txt")
        os.startfile(file)
        
    def open_folder(self):
        folder=Path("record")
        os.startfile(folder)


    def create_board(self):
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)
        file = tk.Menu(menu)
        file.add_command(label="Show Stats", command=self.open_file)
        file.add_command(label="Show previous games", command=self.open_folder)
        file.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label="File", menu=file)

        for position in range(size*size):
            button = tk.Button(self, text=" ")
            self.buttons.append(button)
            row= position // size
            column = position % size
            button.grid(row=row, column=column)
            button["command"] = self.get_command_fn(button, row, column)
            button.config(width=5, height=2)

# This function prints our board to the terminal and also to our file for previous games
def print_board(board):
    for index, cell in enumerate(board, start=1):
        print("{:^6}".format(cell if cell else index), 
        end="\n\n" if index % size == 0 else '')

        grid_in_file="{:^6}".format(cell if cell else index)
        end="\n\n" if index % size == 0 else ''        
        record.write(grid_in_file)
        record.write(end)       
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
root.title("Luffarschack")
root.minsize(250,200)

app = luffarschackApp(master=root)

app.mainloop()
