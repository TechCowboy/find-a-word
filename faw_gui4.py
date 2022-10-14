import os
import sys
import random
import PySimpleGUI as sg

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

def remove_words_from_list(word, word_list):

    try:
        word_list.remove(word)
    except:
        pass
    return word_list        
    
def ask_if_play_again():
    layout = [
                [sg.T("Do you want to play again or Quit?")],
                [sg.B("New Game", key="new_game"), sg.B("Quit")]
             ]

    event, values = sg.Window("Play Again?", layout, modal=True).read(close=True)
    return True if event == "new_game" else False
def main():
    
    # all words list downloaded from
    # https://www.sketchengine.eu/english-word-list/#tab-id-2
    
    all_words = read_word_list("english-word-list-nouns.csv")
    
    # lets make sure our window is large
    # enough for the word list
    
    window = sg.theme("light blue")
    
    text_font = ("Courier", 20, 'bold')
    text_colour = "black"
    
    solved_color = "red"

    word_listbox = "word_list"
    graph_key = "graph"

    # All the stuff inside your window.
    
    # Column 2
    column_2 = [ [sg.Text("Word List", font=text_font, text_color=text_colour)],
                 [sg.Listbox('word list', key=word_listbox, size=(WORDS,WORDS), enable_events=True)] ]
    
    #column_1 = sg.T('', key="text_field", font=text_font, text_color=text_colour, background_color="white")
    column_1 = sg.Graph(canvas_size=(GRID_WIDTH, GRID_HEIGHT),
                    graph_bottom_left=(0, GRID_HEIGHT),
                    graph_top_right=(GRID_WIDTH, 0),
                    background_color='#FCF2EA',
                    key=graph_key, enable_events=True)
    layout = [
                [column_1, sg.Column(column_2)]
             ]
    
    
    # Create the Window
    window = sg.Window('Find-a-word - PySimpleGUI', layout,finalize=True, resizable=True)
    # Event Loop to process "events" and get the "values" of the inputs
    
    repeat = True
    
    graph = window['graph']
    
    char_width  = GRID_WIDTH / COLS
    char_height = GRID_HEIGHT / ROWS
    
    closed = False
    
    while repeat:
        
        graph.DrawRectangle((0, 0), (GRID_WIDTH, GRID_HEIGHT), line_color='#FCF2EA', fill_color='#FCF2EA')
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
        
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                position = (col*char_width + char_width/2, row*char_height+char_height/2)
                graph.DrawText(grid[col][row], location=position, font=text_font, color=text_colour)
        
        window[word_listbox].update(words)
        
        # generate the display
        unsolved = True
        while unsolved:
            event, values = window.read()
            print(event, values)
            if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
                repeat = False
                closed = True
                break
            
            if event == word_listbox:
                word = values[word_listbox]
                print(f"word {word}")
                words = remove_words_from_list(word, words)
                window[word_listbox].update(words)
                
            if event == graph_key:
                position = values[graph_key]
                col = position[0] // char_width
                row = position[1] // char_height
                
                for solved in solution:
                    if col == solved[1] and row == solved[2]:
                        for i in range(len(solved[0])):
                            position = (col*char_width + char_width/2, row*char_height+char_height/2)
                            graph.DrawRectangle((col*char_width, row*char_height - char_height/4), (col*char_width + char_width, row*char_height+char_height), line_color='black', fill_color='white')
                            graph.DrawText(solved[0][i].upper(), location=position, color=solved_color, font=text_font)
                            col += solved[4]
                            row += solved[3]
                        words = remove_words_from_list(solved[0], words)
                        window[word_listbox].update(words)
                        unsolved = len(words) > 0
                        break
 
        if unsolved == False:
            sg.Popup('Game Over', 'You Won!!')
        
        if not closed:
            repeat = ask_if_play_again()
        
    window.close()
    
if __name__ == "__main__":
    main()    
