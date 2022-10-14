#!/usr/bin/env python3
# April 4, 2022 10:00
# faw_gui.py

# Copyright (c) Norman Davie

import os
import sys
import random
import pyautogui as ag
import time
import subprocess

# add our own custom modules to the lib path
# you'll also need an empty __init__.py file
# in the same directory

my_modules_path = os.getcwd()
if sys.path[0] != my_modules_path:
    sys.path.insert(0, my_modules_path)

import faw



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

def read_word_list2(filename, show_ignored_words = False):
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
    for l in range(len(lines)):
        word = lines[l].strip()
        try:
            if word.isalpha() and len(word) > 3:
                words_in.append(word)
            else:
                if show_ignored_words:
                    if (len(word) <= 3):
                        print(f"word '{word}' too small -- ignoring")
                    else:
                        print(f"word '{word}' contains non-alphabetic characters -- ignoring")
        except Exception as e:
            print(f"Error: {str(e)}")
     
    return words_in


def print_words(wordlist):
    """
    print the words to find
    """
    print("WORDS TO FIND:")
    l = len(wordlist)
    
    c = 0
    for i1 in range(l):
        print(f" {wordlist[i1].ljust(8).upper()}", end='')
        c += 1
        if c > 1:
            c = 0
            print("\n", end='')
    print()

def type_words(wordlist):
    """
    print the words to find
    """
    ag.type("WORDS TO FIND:")
    l = len(wordlist)
    
    c = 0
    for i1 in range(l):
        ag.type(f" {wordlist[i1].ljust(8).upper()}")
        c += 1
        if c > 1:
            c = 0
            ag.type("\n")
    print()




def format_solution(solution_list):

    w, x, y, xinc, yinc = solution_list
    x += 1
    y += 1
    
    if (xinc, yinc)   in [(1, 0)]:
        direction = "ACROSS"
    elif (xinc, yinc) in [(-1,0)]:
        direction = "BACKWARDS"
    elif (xinc, yinc) in [(0, 1)]:
        direction = "DOWN"
    elif (xinc, yinc) in [(0,-1)]:
        direction = "UP"
    elif (xinc, yinc) in [(1,-1)]:
        direction = "UP DIAGONAL FORWARD"
    elif (xinc, yinc) in [(-1,-1)]:
        direction = "UP DIAGONAL BACKWARDS"
    elif (xinc, yinc) in [(1, 1)]:
        direction = "DOWN DIAGONAL FORWARD"
    elif (xinc, yinc) in [(-1, 1)]:
        direction = "DOWN DIAGONAL BACKWARDS"
        
    return f"{w.upper():>15} ({y:2}, {x:2}) {direction}"


def LibreOfficeSetup():
    
    print("LibreOfficeSetup")
    program = r"C:\Program Files\LibreOffice\program\swriter.exe"
    subprocess.Popen([ program ], shell=False, stdout=None, stderr=None, close_fds=True)
    print("Waiting...")
    time.sleep(30)
    # ctrl-o (Open)
    # Mom Template.odt
    print("Open")
    ag.hotkey('ctrl','o')
    time.sleep(10)
    ag.typewrite('Mom Template.odt')
    ag.hotkey('enter')
    time.sleep(10)
    
def LibreOfficeRemoveText():
    print("LibreOfficeRemoveText")

    # ctrl-a  (all)
    # backspace (delete everything)
    ag.hotkey('ctrl','a')
    ag.hotkey('backspace')
    

    
def LibreOfficeWords(words_in):
    print("LibreOfficeWords")
    ag.typewrite('WORDS TO FIND:')
    ag.hotkey('enter')
    l = 0
    for w in words_in:
        if len(w) > l:
            l = len(w)
            
    l += 2
    
    c = 0
    for w in words_in:
        c += 1
        ag.typewrite(w.upper().ljust(l))
        if c >= 2:
            c = 0
            ag.hotkey('enter')

        
def LibreOfficeGrid(grid_in):
    print("LibreOfficeGrid")
    for row1 in range(len(grid_in[0])):
        a1 = "".join(grid_in[row1])
        for column1 in range(len(a1)):
            ag.typewrite(a1[column1] + " ")
            
        ag.hotkey('enter')
        
    print()

def LibreOfficeNextPage():
    print("LibreOfficeNextPage")
    ag.hotkey('ctrl','enter')
    
def LibreOfficePrint():
    print("LibreOfficePrint")
    ag.hotkey('ctrl','p')
    time.sleep(1)
    ag.hotkey('enter')

def LibreOfficeQuit():
    print("LibreOfficeQuit")
    time.sleep(3)
    ag.hotkey('ctrl','q')
    time.sleep(3)
    ag.typewrite('n')
    
if __name__ == "__main__":
    
    total_puzzles = 20
    
    LibreOfficeSetup()
  
    while total_puzzles > 0:  
        # all words list downloaded from
        # https://www.sketchengine.eu/english-word-list/#tab-id-2

        #all_words = read_word_list("english-word-list-nouns.csv")
        all_words = read_word_list2("wlist_match12.txt")

        word_size = 6
        needed_words = 10
        horizontal_size = 8
        vertical_size = 8
        
        # determine the largest word by sorting the list
        all_words.sort(key=len, reverse=False)
        
        start = 0
        while len(all_words[start]) < 2:
            start += 1
            
        end = len(all_words)-1
        
        while len(all_words[end]) > word_size:
            end -= 1
            
        print(f"{end-start} words to work with 54 pt font")
        
        
        
        # shuffle the words again

       
        LibreOfficeRemoveText()
        
        retry = True
        while retry:    
            words = all_words[start:end]
            
            for i in range(random.randrange(10, 100)):
                random.shuffle(words)
            # make the grid 5 characters larger than the
            # largest word
        
            word_start = random.randrange(0, len(words)-needed_words)

            #print(f"Start at index {word_start}")

            words = words[word_start:word_start+needed_words]
            #print(f"{words}")
            cfaw = faw.FindAWord(horizontal_size, vertical_size, words)

            # generates a puzzle
            # if any words could not be put in the
            # puzzle, then it will return the words
            # it could not place

            missing = cfaw.generate()

            # missing contains all the words that could not
            # be put in the puzzle
            
            if len(missing) != 0:
                print("FAILED TO GENERATE A SUCCESSFUL PUZZLE.  Retrying...")
                #print(missing)
                retry = True
            else:
                retry = False

        total_puzzles -= 1
        LibreOfficeRemoveText()
        # the words that were used to create the puzzle
        words = cfaw.get_words()
        
        # the puzzle
        grid = cfaw.get_grid()
        
        # the solution to the puzzle


        print_words(words)
        
        print(f"{total_puzzles} Remaining to be generated")

        
        LibreOfficeWords(words)
        

        # print the grid and beside it, print the solution
        
        for row in range(len(grid[0])):
            a = "".join(grid[row])
            for column in range(len(a)):
                print(a[column] + " ", end='')
                
            print("")
            
        print()
        
        LibreOfficeNextPage()
        LibreOfficeGrid(grid)
        LibreOfficePrint()
        
    LibreOfficeQuit()
        
