''' 2048 game using tkinter '''

import tkinter as tk
import random

window=tk.Tk()
window.title("2048 game")

#initilize 4x4 grid
grid = [[0] * 4 for _ in range(4)]  
score=0 

global cell_labels
global score_label

cell_labels=[]
score_label=None

def create_widget(): #creates the frames and labels fro the grid
    global cell_labels,score_label
    
    frame= tk.Frame(window)
    frame.grid(padx=30,pady=30) #dimensions of frame

    for row in range(4):
        row_labels = []

        for col in range(4):

            label = tk.Label(frame, text="", width=4, height=2, font=('Arial', 24), bg="#cdc1b4", relief=tk.RAISED)  #label for each cell
            label.grid(row=row, column=col, padx=5, pady=5)
            row_labels.append(label)  #row of all labels

        cell_labels.append(row_labels)  #each row is added making it a 2D grid

    score_label = tk.Label(frame, text=f"Score: {score}", font=('Arial', 16),bg='#6F8FAF')
    #score_label.grid(row=0, column=0, columnspan=4, pady=5)
    score_label.grid()

def start_game():
    #adds 2/4 in random places 2 times

    add_new_tile()
    add_new_tile()
    update_grid()

def add_new_tile():
    #adds new tile after every move - 2/4
    empty_cells = [(r, c) for r in range(4) for c in range(4) if grid[r][c] == 0]  
    #above collects all cells which don't have a value(2/4) or have 0- going in row and column wise manner

    if empty_cells:
        r, c = random.choice(empty_cells)  #randomly picks a cell from the gathered cells to assign 2/4
        grid[r][c] = random.choice([2, 4])

def update_grid(): #updfates the grid to match the numbers/tiles added

    for r in range(4): #row
        for c in range(4): #colum
            value = grid[r][c]
            cell_labels[r][c].config(text=str(value) if value else "", bg=colour_tile(value))
    score_label.config(text=f"Score: {score}")

def colour_tile(value):
    #assign colours to each tile value

    colours={0:"#cdc1b4", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
            16: "#f59563", 32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72",
            256: "#edcc61", 512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"
        }
    return colours.get(value, "#3c3a32")  #default value is 3c3a32

def key_pressed(event):
    #each key will have a function to move along the grid
    key=event.keysym 
    if key in['Up','Down','Right','Left']:

        if move(key):
            add_new_tile()
            update_grid()

            if check_game_over():
                show_game_over()

def move(direction):
    #move the tiles up,down,left,right
    if direction == 'Up':
        return move_vertical(up=True)
    elif direction == 'Down':
        return move_vertical(up=False)
    elif direction == 'Left':
        return move_horizontal(left=True)
    elif direction == 'Right':
        return move_horizontal(left=False)
    
def move_vertical(up=True):  #moved tile up/down
    moved=False
    global score
    for c in range(4):
        col= [grid[r][c] for r in range(4)]

        if not up:
            col=col[ : :-1]

        new_col, moved_in_col, score_gained = merge_tiles(col)  #merges tiles, changes score

        if not up:
            new_col = new_col[::-1]

        for r in range(4):
            grid[r][c] = new_col[r]

        if moved_in_col:
            moved = True
            score += score_gained

    return moved

def move_horizontal(left=True):
    global score
    moved=False
    for r in range(4):
        row=grid[r]

        if not left:
            row=row[ : :-1]
        
        new_row, moved_in_row, score_gained = merge_tiles(row) #merges tiles, changes score

        if not left:
            new_row = new_row[ : :-1]

        grid[r] = new_row

        if moved_in_row:
            moved= True
            score+=score_gained

    return moved

def merge_tiles(tiles):
    #combines similar values when moved 

    new_tiles = [tile for tile in tiles if tile!=0] #collection of tiles which are not 0
    score_gained = 0
    moved = False

    i=0
    while i< len(new_tiles)-1:

        if new_tiles[i] == new_tiles[i+1]: #if the values are the same
            new_tiles[i]*=2
            score_gained+=new_tiles[i]  #update score to match the highest value of merged tile
            new_tiles.pop(i+1)

            moved= True
        i+=1

    new_tiles.extend([0]* (4-len(new_tiles)))  #4-len(new_tiles) - calcs how many elements are needed to make the column/row have 4 elements
    #[0] as an element is added as many times as required after computing 
    if new_tiles!=tiles:
        moved= True
    return new_tiles,moved,score_gained

def check_game_over():
    #check if no more moves are allowed

    for r in range(4):
        for c in range(4):
            if grid[r][c]==0: #more space is available hence not over
                return False
            if c < 3 and grid[r][c] == grid[r][c+1]: #if adjacent values are same - can be merged
                return False
            if r < 3 and grid[r][c] == grid[r + 1][c]: #if top/bottom values same - can be merged
                return False
    return True #if no merging possible return true 

def reset_game():
    global grid, score, frame 
    grid = [[0] * 4 for _ in range(4)]
    score=0
    add_new_tile()
    add_new_tile()
    update_grid()

    if frame is not None: #rests whole frame once the reset button is clicked
        frame.destroy()
        frame = None

def destroy():
    #system.exit()
    window.destroy()

def show_game_over():
    #dsiplay game over message
    global frame

    frame = tk.Frame(window)
    frame.grid(padx=15, pady=15)  # Use grid for layout

    message_label = tk.Label(frame, text="GAME OVER!", font=("Helvetica", 16))
    message_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))  

    reset_button = tk.Button(frame, text="Reset", command=reset_game, relief=tk.RAISED)
    reset_button.grid(row=1, column=0, padx=(10, 5), pady=10)  

    ok_button = tk.Button(frame, text="OK", relief=tk.RAISED, command=destroy)
    ok_button.grid(row=1, column=1, padx=(5, 10), pady=10)  
  
window.bind("<Key>", key_pressed)  #binds any key press to the key_pressed function

create_widget() 
start_game() 

window.mainloop()
