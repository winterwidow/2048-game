''' 2048 game using tkinter '''

import tkinter as tk

window=tk.Tk()
window.title("2048 game")

#initilize 4x4 grid
grid = [[0] * 4 for _ in range(4)]  
score=0 

create_widget() #calls create_widget function
start_game() #calls start_game function

window.mainloop()

def create_widget(): #creates the frames and labels fro the grid

    frame= tk.Frame(window)
    frame.grid(padx=15,pady=15) #dimensions of frame

    cell_labels = []  #represents each cell in the grid

    for row in range(4):
        row_labels = []

        for col in range(4):

            label = tk.Label(frame, text="", width=4, height=2, relief=tk.RAISED)  #label for each cell
            label.grid(row=row, column=col, padx=5, pady=5)
            row_labels.append(label)  #row of all labels

        cell_labels.append(row_labels)  #each row is added making it a 2D grid

    score_label = tk.Label(window, text=f"Score: {score}")
    score_label.grid()


def start_game():

