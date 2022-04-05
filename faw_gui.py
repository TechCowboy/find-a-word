#!/usr/bin/env python3
# April 4, 2022 10:00
# faw_gui.py

# Copyright (c) Norman Davie

import os
import sys
import random

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

def print_words(wordlist):
    """
    print the words to find
    """
    print("WORDS TO FIND:\n\t", end='')
    l = len(wordlist)
    
    c = 0
    for i in range(l):
        print(f"{wordlist[i].upper():15}", end='')
        c += 1
        if c > 4:
            c = 0
            print("\n\t", end='')
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

    
if __name__ == "__main__":
    
    # all words list downloaded from
    # https://www.sketchengine.eu/english-word-list/#tab-id-2

    all_words = read_word_list("english-word-list-nouns.csv")

    # all the words are in a list now
    # randomize the list and then take the first
    # 10 words
    random.shuffle(all_words)

    words = all_words[:20]

    # determine the largest word by sorting the list
    words.sort(key=len, reverse=True)
    largest = len(words[0])

    # shuffle the words again
    random.shuffle(words)

    # make the grid 5 characters larger than the
    # largest word

    faw = faw.FindAWord(largest+5, largest+5, words)

    # generates a puzzle
    # if any words could not be put in the
    # puzzle, then it will return the words
    # it could not place

    missing = faw.generate()

    # missing contains all the words that could not
    # be put in the puzzle
    
    if len(missing) != 0:
        print("FAILED TO GENERATE A SUCCESSFUL PUZZLE.")
        print(missing)
        
    # the words that were used to create the puzzle
    words = faw.get_words()
    
    # the puzzle
    grid = faw.get_grid()
    
    # the solution to the puzzle
    solution = faw.get_solution()

    print_words(words)

    # print the grid and beside it, print the solution
    
    for row in range(len(grid[0])):
        a = "".join(grid[row])
        for column in range(len(a)):
            print(a[column] + " ", end="")
        if row > len(solution)-1:
            print()
        else:         
            print(f"     {format_solution(solution[row])}")

    a = "".join(grid[0])
    blank = " "*len(a)*2

    for row in range(len(grid[0]), len(solution)):    
        print(f"{blank}     {format_solution(solution[row])}")
        
    print()