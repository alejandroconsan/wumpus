#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 13:15:13 2020

@author: masterblaze
"""

import matplotlib.pyplot as plt
import os
import random
import time

from blessed import Terminal



ROW_NUMBER = 10
COLUMN_NUMBER = 10
HOLE_NUMBER = 10
ARROWS = 5

sense_msg = {'wumpus': 'The Wumpus is here!!!!.',
             'wumpus_close': 'I smell the Wumpus. It is close...',
             'hole_close': 'I feel a breeze. I should move with caution',
             'gold_close': 'I see something blazing.',
             'gold': 'I found a pice of gold here!!',
             'wall': 'I`ve hit against a wall.',
             'killed': 'The Wumpus screamed so loud. I`ve killed it.',
             'hole_death': 'You have fallen into a hole. GAME OVER',
             'wumpus_death': 'The wumpus killed you. GAME OVER',
             'empty': 'I have no arrows left!!!'}
actions_list = ['MOVE', 'COUNTERCLOCKWISE', 'CLOCKWISE', 'SHOOT']


## ============================================================================
## ---BOARD--------------------------------------------------------------------
## ============================================================================
class Board():
    def __init__(self, n_rows = ROW_NUMBER, n_columns = COLUMN_NUMBER, n_holes = HOLE_NUMBER):
        self.n_rows = n_rows 
        self.n_columns = n_columns
        self.n_holes = n_holes
        self.game_board = []
        self.pre_gameboard = []
        self.map = []
        
    def create(self):
        '''This function enerates intial condition randomly. Value 0 in the
        matrix means empty cells, value 1 means the presence of Wumpus, 
        value 2 means the the presence of gold in the cell and value 3 means 
        the presence of a hole in the cell.'''
        
        self.pre_gameboard.append(1)  # 1--> Wumpus
        self.pre_gameboard.append(2)  # 2--> Gold
        self.pre_gameboard += [3] * self.n_holes  # 3 --> Holes
        self.pre_gameboard += \
            [0] * (self.n_rows * self.n_columns - len(self.pre_gameboard) - 1)
        random.shuffle(self.pre_gameboard)
        self.pre_gameboard.insert(0,0)  # Spawn cell is always empty
        
        for i_row in range(self.n_rows):
            self.game_board.append(self.pre_gameboard[0:self.n_columns])
            del self.pre_gameboard[0:self.n_columns]
        for i_row in range(self.n_rows):
            self.map.append([0] * self.n_columns)
            
    def get_square_info(self, i_row, i_col):
        return self.game_board[i_row][i_col]
    
    def update_map(self, i_row, i_col):
        self.map[i_row][i_col] = 1
        plt.imshow(self.map, cmap='binary')
        plt.pause(0.05)
        plt.show(block=False)
        
        
## ============================================================================
## ---PLAYER-------------------------------------------------------------------
## ============================================================================         
class Player():
    def __init__(self,n_arrows=ARROWS):
        self.row_position = 0
        self.column_position = 0
        self.orientation = 3  # 1--> up, 2--> right, 3--> down, 4--> left
        self.n_arrows = n_arrows
        self.wumpus_alive = True
        self.gold_in_bag = False
    def get_pos(self):
        return self.row_position, self.column_position, self.orientation
    
    def turn(self, direction):
        if direction == 'counterclockwise':
            if self.orientation == 1:
                self.orientation = 4
            else:
                self.orientation -= 1
        elif direction == 'clockwise':
            if self.orientation == 4:
                self.orientation = 1
            else:
                self.orientation += 1
    
    def move(self, board):
        '''This function changes the position of the player taking into acount
        its orientation and the boundaries of the game board. It updates the
        player coordinates and returns True if player is  blocked by a wall'''
        if self.orientation == 1:
            if self.row_position == 0:
                self.row_position = 0
                is_wall = True
            else:
                self.row_position -= 1
                is_wall = False
        if self.orientation == 2:
            if self.column_position == board.n_columns-1:
                self.column_position = board.n_columns-1
                is_wall = True
            else:
                self.column_position += 1
                is_wall = False
        if self.orientation == 3:
            if self.row_position == board.n_rows-1:
                self.row_position = board.n_rows-1
                is_wall = True
            else:
                self.row_position += 1
                is_wall = False
        if self.orientation == 4:
            if self.column_position == 0:
                self.column_position = 0
                is_wall = True
            else:
                self.column_position -= 1
                is_wall = False
        return is_wall
            
    def dead_or_alive(self,board):
        cell_state =\
            board.get_square_info(self.row_position, self.column_position)
        if cell_state == 1 and self.wumpus_alive:
            return False, cell_state
        elif cell_state == 1 and not self.wumpus_alive:
            return True, cell_state
        elif cell_state == 3:
            return False, cell_state
        if cell_state == 2:
            return True, cell_state
        else:
            return True, cell_state

    def shoot(self, board):
        self.n_arrows -= 1  # si pasa de 0 no puede volver a disparar
        if self.orientation == 1:
            for i_row in range(0, self.row_position):
                if board.get_square_info(i_row, self.column_position) == 1:
                    self.wumpus_alive = False
                    return True
        if self.orientation == 2:
            for i_col in range(self.column_position, board.n_columns-1):
                if board.get_square_info(self.row_position, i_col) == 1:
                    self.wumpus_alive = False
                    return True
        if self.orientation == 3:
            for i_row in range(self.row_position, board.n_rows-1):
                if board.get_square_info(i_row, self.column_position) == 1:
                    self.wumpus_alive = False
                    return True
        if self.orientation == 4:
            for i_col in range(0, self.column_position):
                if board.get_square_info(self.row_position, i_col) == 1:
                    self.wumpus_alive = False
                    return True   
        return False
    
    def sensing(self, board):
        environment = []
        if self.row_position > 0:  # upper cell
            environment.append(board.get_square_info(
                max(0, self.row_position-1),
                self.column_position))
        if self.row_position < board.n_rows-1:  # lower_cell
            environment.append(board.get_square_info(
                min(board.n_rows-1, self.row_position+1),
                self.column_position))
        if self.column_position > 0:  # left_cell
            environment.append(board.get_square_info(
                self.row_position,
                max(self.column_position-1, 0)))
        if self.column_position < board.n_rows-1:  # right_cell
            environment.append(board.get_square_info(
                self.row_position,
                min(self.column_position+1, board.n_rows-1)))
        return environment
    
    
## ============================================================================
## ---USER INTERFACE-----------------------------------------------------------
## ============================================================================
class UI():
    def __init__(self):
        self.term = Terminal()
        self.choice = None
    def drawtop(self):
        print(self.term.green('=============================='))
        print(self.term.green('       HUNT THE WUMPUS'))
        print(self.term.green('=============================='))
        
    def mainmenu(self):
        print('\nPRESS ANY KEY + INTRO TO START:')
        input()
        self.clear_screen()
    
    def ingame(self, player):
        print('I am in row %d and column number %d' % \
              (player.row_position, player.column_position))
        if player.orientation == 1:
            print('I am looking up.')
        elif player.orientation == 2:
            print('I am looking to the right.')
        elif player.orientation == 3:
            print('I am looking down.')
        elif player.orientation == 4:
            print('I am looking to the left.')
        print('I have %d arrows' % player.n_arrows)
        if player.wumpus_alive:
            print('The Wumpus is still alive')
        else:
            print(self.term.green('The Wumpus is dead.'))
        if player.gold_in_bag:
            print(self.term.yellow('I have a piece of gold.'))
        
        exit_position = player.row_position == 0 and player.column_position == 0
        self.choice = None
        while self.choice is None:
            if exit_position and player.gold_in_bag:
                print('What should I do now? I can "MOVE" fordward, turn "CLOCKWISE", turn "COUNTERCLOCKWISE",\
                  "SHOOT" or "EXIT"')
            else:    
                print('What should I do now? I can "MOVE" fordward, turn "CLOCKWISE", turn "COUNTERCLOCKWISE",\n \
                  or "SHOOT"')
            self.choice = input('Type an action: ')
            print(self.choice)
            if self.choice in actions_list:
                return self.choice
            elif self.choice == 'EXIT':
                if exit_position and player.gold_in_bag:
                    self.game_won()
                else:
                    self.choice = None
                    print(self.term.yellow('I can`t exit now. I must be in the initial position with the gold.'))
            else:
                self.choice = None
                print('I don`t understand!')
               
        
    def sensing_info(self, sensing_data):
        for data in sensing_data:
            if data == 1:
                print(self.term.blue(sense_msg['wumpus_close']))
            elif data == 2:
                print(self.term.blue(sense_msg['gold_close']))
            elif data == 3:
                print(self.term.blue(sense_msg['hole_close']) )
    
    def display_msg(self, msg_ref):
        print(self.term.yellow(sense_msg[msg_ref]))
        
    def game_won(self):
        print(self.term.green('CONGRATULATIONS YOU PASS DE THE LEVEL\nPRESS ANY KEY + INTRO TO EXIT:'))
        input()
        os.exit()
        
    def game_over(self, circumstance):
        if circumstance == 1:
            print(self.term.red(sense_msg['wumpus_death']))
        else:
            print(self.term.red(sense_msg['hole_death']))   
        print(self.term.red('\nPRESS ANY KEY + INTRO TO EXIT:'))
        input()
        os.exit()
    
    def clear_screen(self):
        os.system('cls' if os.name=='nt' else 'clear')
        self.drawtop()
    
## ============================================================================
## --- MAIN -------------------------------------------------------------------
## ============================================================================
        
def event_manager(board, player, ui):    
    action = ui.ingame(player)
    if action == actions_list[0]:
        if player.move(board):
            ui.display_msg('wall')
            time.sleep(0.5)
        else:
            player_alive, reason = player.dead_or_alive(board)
            if player_alive:
                board.update_map(player.row_position, player.column_position)
                if reason == 1:
                    ui.display_msg('wumpus')
                elif reason == 2:
                    ui.display_msg('gold')
                    player.gold_in_bag = True
            else:
                ui.game_over(reason)
    elif action == actions_list[1]:
        player.turn('counterclockwise')
    elif action == actions_list[2]:
        player.turn('clockwise')
    elif action == actions_list[3]:
        if player.n_arrows>0:
            killed = player.shoot(board)
            if killed:
                ui.display_msg('killed')
        else:
            ui.display_msg('empty')


def main():
    ui = UI()
    ui.mainmenu()
    
    board = Board()
    board.create()
    
    player = Player()
    board.update_map(player.row_position, player.column_position)
    
    #Gameloop
    while True:
        ui.clear_screen()
        sensing_data = player.sensing(board)
        ui.sensing_info(sensing_data)
        print(board.game_board)
        event_manager(board, player, ui)


if __name__ == "__main__":
    main()