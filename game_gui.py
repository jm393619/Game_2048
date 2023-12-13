import tkinter as tk
import game_cli
from tkinter import messagebox


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geo = "300x300+300+50"
        self.geometry(self.geo)
        self.title('2048')
        self.config(bg='#a9dec1')

        self.button1 = tk.Button(text='New Game', font=(None, 15), width=10, command=self.new_game)
        self.button1.pack(pady=(40, 0))

        self.button2 = tk.Button(text='Settings', font=(None, 15), width=10, command=self.settings)
        self.button2.pack(pady=(20, 0))

        self.button3 = tk.Button(text='Quit', font=(None, 15), width=10, command=self.quit)
        self.button3.pack(pady=(20, 0))

        self.var = tk.IntVar(value=4)

    def new_game(self):
        game = Game(self)
        # game.after(10, game.lift)
        game.grab_set()

    def settings(self):
        sets = Settings(self)
        sets.grab_set()

    def quit(self):
        self.destroy()


class Settings(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.geometry(parent.winfo_geometry())

        self.protocol('WM_DELETE_WINDOW', self._quit)

        self.label_frame = tk.LabelFrame(self, text='Difficulty level')
        self.label_frame.pack(pady=(20, 0))

        self.radio1 = tk.Radiobutton(self.label_frame, text='Classic(4x4)', value=4, variable=self.parent.var)
        self.radio1.pack(anchor=tk.W)

        self.radio2 = tk.Radiobutton(self.label_frame, text='Big(5x5)', value=5, variable=self.parent.var)
        self.radio2.pack(anchor=tk.W)

        self.radio3 = tk.Radiobutton(self.label_frame, text='Bigger(6x6)', value=6, variable=self.parent.var)
        self.radio3.pack(anchor=tk.W)

        self.button = tk.Button(self, text='Quit', font=(None, 15), width=15, command=self._return)
        self.button.pack(pady=(40, 40))

        parent.withdraw()

    def _return(self):
        geo = self.winfo_geometry()
        self.parent.geometry(geo)
        self.parent.deiconify()
        self.destroy()

    def _quit(self):
        self.destroy()
        self.parent.destroy()


class Game(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.focus_force()
        self.g = game_cli.Game(self.parent.var.get())

        length = self.g.dim * 115 + 10

        self.protocol('WM_DELETE_WINDOW', self._quit)
        parent.withdraw()

        self.geometry(f"{length}x{length}+300+50")
        self.title('2048')

        # Create frame with labels
        self.frame = tk.Frame(self, background='green')
        self.frame.pack(padx=10, pady=10)

        # Create menu
        self.bar_menu = tk.Menu()
        self.config(menu=self.bar_menu)

        self.options = tk.Menu(self.bar_menu)
        self.bar_menu.add_cascade(label='options', menu=self.options)
        self.options.add_command(label='new game', command=self.new_game)
        self.options.add_command(label='undo', command=self.undo)
        self.options.add_command(label='exit', command=self.exit)

        # Create dictionary with labels
        self.d = {}
        self.d_fun = {'a': self.g.move_left, 'w': self.g.move_up, 'd': self.g.move_right, 's': self.g.move_down}

        self.colors = {0: "#fcfbfb", 2: '#737df7', 4: "#47c464", 8: "#f6f344", 16: "#d86334", 32: "#d634d8",
                       64: '#d634d8', 128: "#8759cd", 256: "#2ad927", 512: "#e161a1", 1024: "#636262", 2048: "#20a657",
                       4096: "#fcfbfb", 8192: '#737df7', 16384: "#47c464", 32768: "#f6f344", 65536: "#d86334",
                       131072: "#d634d8", 262144: '#d634d8'}

        for k1, i in enumerate(self.g.board[1:-1], 1):
            for k2, j in enumerate(i[1:-1], 1):

                self.d[f"{k1}-{k2}"] = tk.Label(self.frame, text=str(j), width=6, height=3, font=(None, 20))
                self.d[f"{k1}-{k2}"].grid(row=k1, column=k2, pady=5, padx=5)

                n = self.g.board[k1][k2]
                self.d[f"{k1}-{k2}"].config(text=n, bg=self.colors[n])

        self.bind("<Left>", func=lambda x: self.move_('a'))
        self.bind("<Up>", func=lambda x: self.move_('w'))
        self.bind("<Right>", func=lambda x: self.move_('d'))
        self.bind("<Down>", func=lambda x: self.move_('s'))

    def undo(self):
        for i, j in self.g.cache.items():
            k, m = i.split('-')
            self.g.board[int(k)][int(m)] = j

        self.update_board()

    def _quit(self):
        self.destroy()
        self.parent.destroy()

    def exit(self):
        self.parent.geometry(self.parent.geo)
        self.parent.deiconify()
        self.destroy()

    def update_board(self):
        for i in range(1, self.g.dim+1):
            for j in range(1, self.g.dim+1):

                n = self.g.board[i][j]
                self.d[f"{i}-{j}"].config(text=n, bg=self.colors[n])

    def new_game(self):
        self.g.new_game()
        self.update_board()

    def move_(self, x):

        self.g.cache = self.g.set_cache()

        was_shift = self.d_fun[x]()

        if was_shift:
            self.g.set_number(1)

        self.update_board()

        over = self.g.is_game_over()

        if over:
            messagebox.showinfo(title='INFO', message='Game Over')


if __name__ == '__main__':
    app = App()
    app.mainloop()
