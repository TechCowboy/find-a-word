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
    print("WORDS TO FIND:\n", end='')
    l = len(wordlist)
    
    c = 0
    for i in range(l):
        print(f" {wordlist[i].upper()}\t", end='')
        c += 1
        if c > 1:
            c = 0
            print("\n", end='')
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

    retry = True
    
    while retry:    
        words = all_words[start:end]
        print("Shuffling...")
        
        for i in range(random.randrange(10, 100)):
            random.shuffle(words)
        # make the grid 5 characters larger than the
        # largest word
    
        word_start = random.randrange(0, len(words)-needed_words)

        print(f"Start at index {word_start}")

        words = words[word_start:word_start+needed_words]
        print(f"{words}")
        cfaw = faw.FindAWord(horizontal_size, vertical_size, words)

        # generates a puzzle
        # if any words could not be put in the
        # puzzle, then it will return the words
        # it could not place

        missing = cfaw.generate()

        # missing contains all the words that could not
        # be put in the puzzle
        
        if len(missing) != 0:
            print("FAILED TO GENERATE A SUCCESSFUL PUZZLE.")
            print(missing)
            retry = True
        else:
            retry = False
            
    # the words that were used to create the puzzle
    words = cfaw.get_words()
    
    # the puzzle
    grid = cfaw.get_grid()
    
    # the solution to the puzzle


    print_words(words)

    # print the grid and beside it, print the solution
    
    for row in range(len(grid[0])):
        a = "".join(grid[row])
        for column in range(len(a)):
            print(a[column] + " ", end='')
            
        print("")

    
        
    print()
    
    #solution = faw.get_solution()
    #for row in range(len(solution)):    
    #    print(f"{format_solution(solution[row])}")