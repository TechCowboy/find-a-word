#!/usr/bin/env python3
# April 4, 2022 17:00
# faw_gui2.py

# Copyright (c) Norman Davie

import os
import sys
import random

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    
import pygame
from pygame._sdl2 import messagebox

# add our own custom modules to the lib path
# you'll also need an empty __init__.py file
# in the same directory

my_modules_path = os.getcwd()
if sys.path[0] != my_modules_path:
    sys.path.insert(0, my_modules_path)

from faw import FindAWord

WIN_WIDTH     = 800
GRID_WIDTH, GRID_HEIGHT = 600, 600
ROWS, COLS    = 20, 20
WORDS         = 20

pygame.font.init()

GRID_FONT            = pygame.font.SysFont("Courier Bold", 35)
WORD_FONT            = pygame.font.SysFont("Courier", 20)

BG_COLOR             = "white"
WORD_COLOR           = "black"
FOUND_COLOR          = "red"
RECT_BORDER_COLOR    = "black"
RECT_FILL_COLOR      = "white"

def read_word_list(filename, show_ignored_words = False):
    """
    read words from a CSV file
    the 2nd column contains the word
    actual data doesn't start
    until line 5
    """
    lines = []
    with open(filename, "r") as f:
        lines = f.readlines()
    
    words_in = []
    for l in range(5, len(lines)):
        word = lines[l].strip()
        word = word.split(";")
        try:
            if word[1].isalpha() and len(word[1]) > 3:
                words_in.append(word[1])
            else:
                if show_ignored_words:
                    if (len(word[1]) <= 3):
                        print(f"word '{word[1]}' too small -- ignoring")
                    else:
                        print(f"word '{word[1]}' contains non-alphabetic characters -- ignoring")
        except Exception as e:
            print(f"Error: {str(e)}")
     
    return words_in


def draw(win, grid, words, found_solutions, found_words):
    # fill the background
    win.fill(BG_COLOR)
    
    # the size of each grid box
    size = GRID_WIDTH // ROWS
    
    rows = len(grid)
    cols = len(grid[0])
    
    for r in range(rows):
        y = size * r
        for c in range(cols):
            x = size * c
            
            pygame.draw.rect(win, RECT_FILL_COLOR, (x,y, size, size))
            pygame.draw.rect(win, RECT_BORDER_COLOR, (x,y, size, size),2)

            # if a word has been found, make it red
            red = False
            if (r,c) in found_solutions:
                red = True
            
            if red:
                text = GRID_FONT.render(grid[r][c], True, FOUND_COLOR)
            else:
                text = GRID_FONT.render(grid[r][c], True, WORD_COLOR)
            
            # center the character in the grid box
            winx = x + (size/2 - text.get_width()/2)
            winy = y + (size/2 - text.get_height()/2)            
            
            win.blit(text, (winx, winy))
  
    # print the word list
    text1 = "WORDS:"
    text = WORD_FONT.render(text1, True, WORD_COLOR)
    winx = size * cols + 5
    winy = 0
    win.blit(text, (winx, winy))
    
    winx = size * cols + 10 
    winy += text.get_height() * 2
    
    for r, w in enumerate(words):
        # if the word has been found, make it red
        if w in found_words:
            text = WORD_FONT.render(w, True, FOUND_COLOR)
        else:
            text = WORD_FONT.render(w, True, WORD_COLOR)
        win.blit(text, (winx, winy))
        winy += text.get_height()
          
    pygame.display.update()

def get_grid_position(mouse_pos):
    """
    Convert mouse position to
    a grid position (row, column)
    """
    mouse_x, mouse_y = mouse_pos
    
    size = GRID_WIDTH // ROWS
    
    r = mouse_y // size
    c = mouse_x // size
    
    return (r,c)
    
def game_window(win, grid, words, solution):
    run = True
    
    solutions = []
    found_solutions = []
    found_words = []
    again = False
    
    for s in solution:
        w, r, c, xinc, yinc = s
        solutions.append((r,c))
    
    while run:
        for event in pygame.event.get():
            
            # has someone clicked the close button?
            if event.type == pygame.QUIT:
                run = False
                break
            
            # have we received a mouse down event?
            
            if event.type == pygame.MOUSEBUTTONUP:
                r,c = get_grid_position(pygame.mouse.get_pos())

                # don't check if we're outside the grid
                if r >= ROWS or c >= COLS:
                    continue
                
                # is the letter we clicked on the first
                # letter of a word that is in the solution
                # at the correct location?
                
                for s in solution:
                    w, r1, c1, xinc, yinc = s
                    if (r,c) == (r1, c1):
                        # add the word to the found list
                        found_words.append(w)
                        
                        # for each character, and it to the
                        # found solution list
                        for _ in range(len(w)):
                            if not (r1, c1) in found_solutions:    
                                found_solutions.append((r1,c1))
                            r1 += yinc
                            c1 += xinc
                
        draw(win, grid, words, found_solutions, found_words)
        
        # have all the words been found?
        
        if len(found_words) == len(solutions):
            answer = messagebox(
                "Do you want to play again?",
                "You Won!",
                info=True,
                buttons=("Yes", "No"),
                return_button=0,
                escape_button=1,
            )
            if answer == 0:
                # respawn with a new grid
                again = True
            else:
                # quit the application
                again = False
            
            # leave the window processing
            run = False
    
    return again
    
def main():
    
    # all words list downloaded from
    # https://www.sketchengine.eu/english-word-list/#tab-id-2
    
    all_words = read_word_list("english-word-list-nouns.csv")
    
    # get started creating a graphical GUI
    
    pygame.init()
    
    # lets make sure our window is large
    # enough for the word list
    
    text1 = "X"
    text = WORD_FONT.render(text1, True, WORD_COLOR)
    word_list_height = text.get_height() * WORDS + 3
    win_height  = 600
    if word_list_height > win_height:
        win_height = word_list_height
    
    # create the window
    
    win = pygame.display.set_mode((WIN_WIDTH, win_height))
    
    pygame.display.set_caption("Find a word! - PyGame")

    # keep repeating until user quits

    repeat = True
    while repeat:
        
        # all the words are in a list now
        # randomize the list 
        random.shuffle(all_words)

        # grab the first 'WORDS' random words
        words = all_words[:WORDS]

        # shuffle the words again
        random.shuffle(words)

        faw = FindAWord(ROWS, COLS, words)

        # generates a puzzle
        # if any words could not be put in the
        # puzzle, then it will return the words
        # it could not place

        missing = faw.generate()

        # missing should be an empty list
        if len(missing) != 0:
            print("FAILED TO GENERATE A SUCCESSFUL PUZZLE.")
            print(missing)
            exit(-1)
            

        # get the words used in the grid
        words = faw.get_words()
        
        # get the puzzle that was generated
        grid = faw.get_grid()
        
        # get the position of all the words
        solution = faw.get_solution()
        
        # generate the display
        repeat = game_window(win, grid, words, solution)
        
    pygame.quit()
    
if __name__ == "__main__":
    main()    
    
    
    

    
    
    
