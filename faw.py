#!/usr/bin/env python3
# April 3, 2022 17:00
# faw.py

# Copyright (c) Norman Davie

import random

class FindAWord:
    
    def __init__(self, rows, columns, wordlist):
        
        self.rows      = rows
        self.columns   = columns
        self.wordlist  = wordlist.copy()
        self._wordlist = wordlist.copy()
        self.solution  = []
        
        # make all our words lowercase
        for i in range(len(self.wordlist)):
            self.wordlist[i]  = self.wordlist[i].lower()
            self._wordlist[i] = self._wordlist[i].lower()
            
        
        # create a random grid of uppercase letters
        self.grid = [ ]
        alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

            
        for _ in range(rows):
            random.shuffle(alphabet)
            self.grid.append(list(alphabet[:columns]))
             
    def get_grid(self):
        return self.grid
    
    def get_words(self):
        return self._wordlist
    
    def get_solution(self):
        return self.solution    
    
    def add_solution(self, word, r, c, xinc, yinc):
        self.solution.append([word, r, c, xinc, yinc])
        
    def available_directions(self, word, r, c):
        """
        Determine what directions we can
        put our word; doesn't check to see
        if it would clobber an existing word
        """
        l = len(word)
                            
        directions = []
        
        if c < self.columns - l:
            # ACROSS
            directions.append((1, 0))
            # UP DIAGONAL FORWARD
            if r > l:
                directions.append((1, -1))
            
        if c > l:
            # BACKWARD
            directions.append((-1, 0))
            # UP DIAGONAL BACKWARD
            if r > l:
                directions.append((-1, -1))
            
        if r > l:
            # UP
            directions.append((0, -1))
         
        if r < self.columns - l:
            # DOWN
            directions.append((0, 1))
            if c > self.columns - l:
                # DOWN DIAGONAL BACKWARDS
                directions.append((-1, 1))
                
            if c < self.columns - l:
                # DOWN DIAGONAL FORWARD
                directions.append((1, 1))
          
        return directions
    
    def would_clobber_existing_word(self, word, r, c, xinc, yinc):
        """
        Checks to see if we would clobber an existing word
        NOTE: doesn't check the first character since we can
        share that with an existing word
        """
        clobber = False
        # don't check first character
        # we may be reusing it
        x = c + xinc
        y = r + yinc
        for _ in range(1,len(word)):
            if self.grid[y][x].islower():
                clobber = True
                break
            x += xinc
            y += yinc
        return clobber
    
    def find_free(self):
        """
        Find all the free spots on the grid
        """
        slots = []
        # find horizontal spots
        size = 0;
        for r in range(self.rows):
            for c in range(self.columns):
                if self.grid[r][c].isupper():
                    if c != self.columns-1:
                        size += 1
                    else:
                        size -= 1
                        if size > 3:
                            slots.append([size, r, c-size, 1, 0])
                            
                        size = 0
                else:
                    size -= 1
                    if size > 3:
                        slots.append([size, r, c-size, 1, 0])
                    size = 0
 
        # find vertical spots
        size = 0;
        for c in range(self.columns):
            for r in range(self.rows):
                if self.grid[r][c].isupper():
                    if r != self.rows-1:
                        size += 1
                    else:
                        size -= 1
                        if size > 3:
                            slots.append([size, r-size, c, 0, 1])
                            
                        size = 0
                else:
                    size -= 1
                    if size > 3:
                        slots.append([size, r-size, c, 0, 1])
                    size = 0
                    
        return slots
 
    def insert_word(self, word, r, c, xinc, yinc):
        """
        inserts a word into the grid
        NOTE: you need to confirm you won't clobber
        an existing word, this routine will generate
        an exception if you do
        """
        l = len(word)
        
        r1=r
        c1=c
        
        for i in range(l):
            if self.grid[r][c].islower():
                print("CLOBBER WOULD OCCUR!")
                print(f"word: {word} ({r1}, {c1}) ({xinc}, {yinc})")
                exit(0)
                
            self.grid[r][c] = word[i]
            r += yinc
            c += xinc
                        

    def simple_insert(self, word):
        """
        Look through the grid for the first character
        in our word, if it's found, then randomly
        select a direction for the word and insert it
        """
        
        # random jump around grid
        
        positions = []
        for r in range(self.rows):
            for c in range(self.columns):
                positions.append((r,c))
      
        random.shuffle(positions)
       
        # find first letter if already present
        # while randomly searching through grid
        
        for i in range(len(positions)):
            r, c = positions[i]
            if self.grid[r][c] == word[0].upper():
                
                # we found the first letter
                # what directions can we put the word?

                dir = self.available_directions(word, r,c)                   
                
                while True:
                    if len(dir) == 0:
                        break
                    
                    #print(r,c,word, dir)
                    #input()
                    
                    random.shuffle(dir)
                    xinc, yinc = dir[0]
                    
                        
                    #print(dir[0])
                    
                    if self.would_clobber_existing_word(word, r, c, xinc, yinc):
                        #print(dir[0] + " would clobber")
                        dir.remove(dir[0])
                        #print("new list", dir)
                        continue
                    
                    self.add_solution(word, r, c, xinc, yinc)
                    #print(f"simple {word} ({r}, {c}), {xinc} {yinc}")
                    self.insert_word(word, r, c, xinc, yinc)

                    return True
                
        return False
        

    def generate(self):
        """
        Generate the puzzle.
        It's possible that no solution is possible with
        the currently generated random characters, so it
        will retry if it can't do it
        If we have 200 failures, it will not generate a grid
        Returns words we could not put in the puzzle
        """
        solution_found = False
        max_failures = 200
        failures = 0
        while not solution_found:
            
            if not solution_found:
                failures += 1
                if failures > max_failures:
                    break
                
            self.wordlist = self._wordlist.copy()
            
            random.shuffle(self.wordlist)
            self.wordlist.sort(key=len, reverse=True)
            wl = self.wordlist.copy()
            for w in wl:
                # find the first letter of our
                # word and insert it there if
                # possible
                
                if self.simple_insert(w):
                    self.wordlist.remove(w)
                else:
                    #print("Could not simple insert "+w)

                    available_spaces = self.find_free()
                    random.shuffle(available_spaces)
                    l = len(w)
                    for s in available_spaces:
                        size, r, c, xinc, yinc = s    
                        if size > l:
                            #print(f"force {w} ({r}, {c}), {xinc} {yinc}")

                            self.insert_word(w, r, c, xinc, yinc)

                            self.wordlist.remove(w)
                            self.add_solution(w, r, c, xinc, yinc)
                            
                            break
          
            #self.print_grid()
            
            for r in range(self.rows):
                for c in range(self.columns):
                    self.grid[r][c] = self.grid[r][c].upper()
            
            solution_found =  len(self.wordlist) == 0
        
        return self.wordlist        


          


    
        
        
        