import tkinter as tk
from tkinter import messagebox
import random

class Minesweeper(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("240x260")
        self.title("mineswepper.exe")
        self.resizable(False, False)
        self.rows = 10
        self.columns = 10
        self.bomb_amount = 20
        self.flag_true_list = []
        self.flag_false_list = []
        self.original_bomb_list = []
        self.found_bomb_list = []
        self.open_list = []
        self.create_blocks()
        self.bomb_generate()

        self.menu = tk.Menu(self)
        self.menu.add_command(label="reset", command=self.remake) 
        self.menu_widgets = self.menu
        self.config(menu=self.menu)  

    def create_blocks(self):
        for row in range(self.rows):
            for col in range(self.columns):
                btn = tk.Button(self, width=2, height=1, bg="grey")
                btn.config(command=lambda row=row, col=col: self.click(row, col))
                btn.bind("<Button-3>", lambda event, row=row, col=col: self.flag(event, row, col))
                btn.grid(row=row, column=col)

    def bomb_generate(self):
        f = 0
        while f < self.bomb_amount:
            x = random.randint(0,9)
            y = random.randint(0,9)
            if (x,y) not in self.original_bomb_list:
                self.original_bomb_list.append((x,y))
                f += 1

    def remake(self):
        for widget in self.winfo_children():
            if widget != self.menu:  
                widget.destroy()
        self.original_bomb_list = []
        self.found_bomb_list = []
        self.open_list = []
        self.flag_true_list = []
        self.flag_false_list = []
        self.create_blocks()
        self.bomb_generate()

    def click(self, row, col):
        print((row, col))
        if (row, col) in self.original_bomb_list:
            btn = tk.Button(self, width=2, height=1, bg="red")
            btn.config(state="disabled")
            btn.grid(row=row, column=col)
            messagebox.showwarning("Message", "You Lose! Try again?")
            self.remake()
        else:
            self.open_block(row, col)
    def open_block(self, row, col):
        if row<0 or col<0 or row>=self.rows or col>=self.columns:
            pass
        elif (row, col) in self.open_list or (row, col) in self.flag_false_list or (row, col) in self.flag_true_list:
            pass
        else:
            count = 0
            l = [(row-1, col-1), (row-1, col), (row-1, col+1), (row, col-1), (row, col+1), (row+1, col-1), (row+1, col),(row+1, col+1)]
            for around in l:
                if around in self.original_bomb_list:
                    count += 1
            if count == 0:
                btn = tk.Button(self, width=2, height=1, bg="white")
                btn.config(state="disabled")
                btn.grid(row=row, column=col)
                self.open_list.append((row, col))
                for i, _ in enumerate(l):
                    if (l[i][0], l[i][1]) not in self.open_list:
                        self.open_block(l[i][0], l[i][1])
            else:
                btn = tk.Button(self, width=2, height=1, text=count)
                btn.config(state="disabled")
                btn.grid(row=row, column=col)
                self.open_list.append((row, col))

    def flag(self, event, row, col):
        if (row, col) in self.flag_true_list:
            self.flag_true_list.remove((row, col))
            self.found_bomb_list.remove((row, col))
            btn = tk.Button(self, width=2, height=1, bg="grey")
            btn.config(state="normal")
            btn.config(command=lambda row=row, col=col: self.click(row, col))
            btn.bind("<Button-3>", lambda event, row=row, col=col: self.flag(event, row, col))
            btn.grid(row=row, column=col)
        elif (row, col) in self.flag_false_list:
            self.flag_false_list.remove((row, col))
            btn = tk.Button(self, width=2, height=1, bg="grey")
            btn.config(state="normal")
            btn.config(command=lambda row=row, col=col: self.click(row, col))
            btn.bind("<Button-3>", lambda event, row=row, col=col: self.flag(event, row, col))
            btn.grid(row=row, column=col)
        else:
            btn = tk.Button(self, width=2, height=1, bg="blue")
            btn.config(state="normal")
            btn.config(command=lambda row=row, col=col: self.click(row, col))
            btn.bind("<Button-3>", lambda event, row=row, col=col: self.flag(event, row, col))
            btn.grid(row=row, column=col)
            if (row, col) in self.original_bomb_list:
                self.found_bomb_list.append((row, col))
                self.flag_true_list.append((row, col))
            else:
                self.flag_false_list.append((row, col))
            if len(self.found_bomb_list) == self.bomb_amount:
                messagebox.showinfo("Message", "You Win! Try again?")
                self.remake()

if __name__ == "__main__":
    root = Minesweeper()
    menu=tk.Menu(root)  
    menu.add_command(label="Hello")  
    root.mainloop()