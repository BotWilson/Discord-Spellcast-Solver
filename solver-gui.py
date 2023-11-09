import tkinter as tk
import solutionScript as spellCasterSolver

class SolvingWindow:
    def __init__(self):
        self.current_cell = (0, 0)
        self.highlighted_squares = {"blue": None, "red": None, "purple": None}
        self.grid_labels = []
        self.answer = spellCasterSolver.Solution()
        self.swap_value = 0 

        self.noSwapResult = None
        self.oneSwapResult = None
        self.twoSwapResult = None

    def clearBoard(self):
        for row in self.grid_labels:
            for cell in row:
                cell.config(bg='#1F2833', fg='#C5C6C7')

        for key in self.highlighted_squares:
            if not (self.highlighted_squares[key] is None):
                self.grid_labels[self.highlighted_squares[key][0]][self.highlighted_squares[key][1]].config(bg=key)

    
    def revertLetters(self):
        for result_data in [self.noSwapResult, self.oneSwapResult, self.twoSwapResult]:
            if result_data:
                swapData = result_data[3]
                for i, j, swapToLetter, swapFromLetter in swapData:
                    self.grid_labels[i][j].config(fg='#C5C6C7', text=swapFromLetter)


    def on_key(self, event): 
        self.clearBoard()

        if event.keysym == "Up":
            current_row, current_col = self.current_cell
            self.grid_labels[current_row][current_col].config(relief="raised")

            if current_row != 0:
                current_row -= 1
            
            self.current_cell = (current_row, current_col)
            self.grid_labels[current_row][current_col].config(relief="sunken")
        
        elif event.keysym == "Down":
            current_row, current_col = self.current_cell
            self.grid_labels[current_row][current_col].config(relief="raised")

            if current_row != 4:
                current_row += 1
            
            self.current_cell = (current_row, current_col)
            self.grid_labels[current_row][current_col].config(relief="sunken")

        elif event.keysym == "Left":
            current_row, current_col = self.current_cell
            self.grid_labels[current_row][current_col].config(relief="raised")

            if current_col != 0:
                current_col -= 1
            
            self.current_cell = (current_row, current_col)
            self.grid_labels[current_row][current_col].config(relief="sunken")
        
        elif event.keysym == "Right":
            current_row, current_col = self.current_cell
            self.grid_labels[current_row][current_col].config(relief="raised")

            if current_col != 4:
                current_col += 1
            
            self.current_cell = (current_row, current_col)
            self.grid_labels[current_row][current_col].config(relief="sunken")

        elif event.keysym == "BackSpace":
            current_row, current_col = self.current_cell
            self.grid_labels[current_row][current_col].config(relief="raised")

            if current_col == 0 and current_row == 0:
                pass
            elif current_col == 0:
                current_row -= 1
                current_col = 4
            else:
                current_col -= 1
            
            self.current_cell = (current_row, current_col)
            self.grid_labels[current_row][current_col].config(relief="sunken")

        elif event.char.isalpha() and len(event.char) == 1:
            self.grid_labels[self.current_cell[0]][self.current_cell[1]].config(text=event.char.upper())
            self.move_to_next_cell()
            self.revertLetters()

            self.noSwapResult = None
            self.oneSwapResult = None
            self.twoSwapResult = None

    def move_to_next_cell(self):
        current_row, current_col = self.current_cell
        self.grid_labels[current_row][current_col].config(relief="raised")

        if current_col < 4:
            current_col += 1
        elif current_row < 4:
            current_row += 1
            current_col = 0
        self.current_cell = (current_row, current_col)
        self.grid_labels[current_row][current_col].config(relief="sunken")

    def on_cell_click(self, row, col):
        self.clearBoard()

        self.grid_labels[self.current_cell[0]][self.current_cell[1]].config(relief="raised")
        self.current_cell = (row, col)
        self.grid_labels[row][col].config(relief="sunken")

    def solve_grid(self):
        self.revertLetters()
        board = self.extract_board_letters()
        doubleLetter, tripleLetter, doublePoint = self.highlighted_squares['blue'], self.highlighted_squares['red'], self.highlighted_squares['purple']

        noSwapSolution = self.answer.solve(board, doubleLetter, tripleLetter, doublePoint, 0)
        self.noSwapResult = noSwapSolution
        self.update_result(noSwapSolution, 0)

        oneSwapSolution = self.answer.solve(board, doubleLetter, tripleLetter, doublePoint, 1)
        self.oneSwapResult = oneSwapSolution
        self.update_result(oneSwapSolution, 1)

        twoSwapSolution = self.answer.solve(board, doubleLetter, tripleLetter, doublePoint, 2)
        self.twoSwapResult = twoSwapSolution
        self.update_result(twoSwapSolution, 2)

    def extract_board_letters(self):
        board_letters = []
        for row_labels in self.grid_labels:
            row_letters = [label.cget("text") for label in row_labels]
            board_letters.append(row_letters)
        return board_letters

    def highlight_square(self, color):

        self.noSwapResult = None
        self.oneSwapResult = None
        self.twoSwapResult = None

        def set_highlight_color():
            selected_cell = self.current_cell
            if selected_cell:
                row, col = selected_cell

                if not self.highlighted_squares[color] is None:
                    self.grid_labels[self.highlighted_squares[color][0]][self.highlighted_squares[color][1]].config(relief="raised", bg='#1F2833')

                if self.highlighted_squares[color] == (row, col):
                    self.grid_labels[row][col].config(relief='sunken')
                    self.highlighted_squares[color] = None
                    return

                for key in self.highlighted_squares:    
                    if self.highlighted_squares[key] == (row, col):
                        self.highlighted_squares[key] = None

                self.grid_labels[row][col].config(relief="sunken", bg=color)
                self.highlighted_squares[color] = (row, col)

        return set_highlight_color

    def update_result(self, result_data, numSwaps):
        if numSwaps == 0:
            self.result_no_swap_label.config(text=f"No Swap: {result_data[0]} - {result_data[2]} points")
        if numSwaps == 1:
            self.result_one_swap_label.config(text=f"One Swap: {result_data[0]} - {result_data[2]} points")
        if numSwaps == 2:
            self.result_two_swap_label.config(text=f"Two Swap: {result_data[0]} - {result_data[2]} points")
        

        if numSwaps == self.swap_value.get():
            letterCoords = result_data[1]
            self.grid_labels[letterCoords[0][0]][letterCoords[0][1]].config(bg='#77889e')

            for letter in letterCoords[1:]:
                self.grid_labels[letter[0]][letter[1]].config(bg='#7ea2cf')
            
            for i, j, swapToLetter, swapFromLetter in result_data[3]:
                self.grid_labels[i][j].config(fg='#FF0000', text=(swapToLetter))
        self.app.update()

    def on_swap_selection(self):
        self.clearBoard()
        self.revertLetters()

        varMap = {0: self.noSwapResult, 1: self.oneSwapResult, 2: self.twoSwapResult}
        currentValue = self.swap_value.get()
        result_data = varMap[currentValue]

        if result_data:
            letterCoords = result_data[1]
            self.grid_labels[letterCoords[0][0]][letterCoords[0][1]].config(bg='#77889e')

            for letter in letterCoords[1:]:
                self.grid_labels[letter[0]][letter[1]].config(bg='#7ea2cf')
            
            for i, j, swapToLetter, swapFromLetter in result_data[3]:
                self.grid_labels[i][j].config(fg='#FF0000', text=(swapToLetter))

    def startWindow(self):
        grid_labels = self.grid_labels

        app = tk.Tk()
        self.app = app
        app.title("Letter Grid")

        for i in range(5):
            row_labels = []
            for j in range(5):
                label = tk.Label(app, text="", width=5, height=2, borderwidth=8, relief="flat", padx=0, pady=0, bg='#1F2833')
                label.grid(row=i, column=j)
                label.bind("<Button-1>", lambda event, row=i, col=j: self.on_cell_click(row, col))
                label.config(relief='raised', fg='#C5C6C7', font=('Courier', 36))
                row_labels.append(label)
            self.grid_labels.append(row_labels)

        self.grid_labels[self.current_cell[0]][self.current_cell[1]].config(relief="sunken")

        current_selected_cell = tk.StringVar()
        current_selected_cell = self.current_cell

        app.bind("<Key>", self.on_key)
        app.focus_set()

        solve_button = tk.Button(app, text="Solve", command=self.solve_grid)
        solve_button.grid(row=6, column=0, columnspan=2)

        double_letter_button = tk.Button(app, text="Double Letter", command=self.highlight_square("blue"))
        double_letter_button.grid(row=6, column=2)

        triple_letter_button = tk.Button(app, text="Triple Letter", command=self.highlight_square("red"))
        triple_letter_button.grid(row=6, column=3)

        double_points_button = tk.Button(app, text="Double Points", command=self.highlight_square("purple"))
        double_points_button.grid(row=6, column=4)

        self.result_no_swap_label = tk.Label(app, text="No Swap: ", font=('Courier', 20))
        self.result_no_swap_label.grid(row=8, column=0, columnspan=5)

        self.result_one_swap_label = tk.Label(app, text="One Swap: ", font=('Courier', 20))
        self.result_one_swap_label.grid(row=10, column=0, columnspan=5)

        self.result_two_swap_label = tk.Label(app, text="Two Swap: ", font=('Courier', 20))
        self.result_two_swap_label.grid(row=12, column=0, columnspan=5)

        self.swap_value = tk.IntVar()

        one_swap_button = tk.Radiobutton(app, text="No Swap", variable=self.swap_value, value=0, command=self.on_swap_selection)
        two_swap_button = tk.Radiobutton(app, text="One Swap", variable=self.swap_value, value=1, command=self.on_swap_selection)
        three_swap_button = tk.Radiobutton(app, text="Two Swap", variable=self.swap_value, value=2, command=self.on_swap_selection)
        one_swap_button.select()

        one_swap_button.grid(row=14, column=0, columnspan=2)
        two_swap_button.grid(row=14, column=2, columnspan=2)
        three_swap_button.grid(row=14, column=4, columnspan=2)

        app.mainloop()
    
solverApp = SolvingWindow()
solverApp.startWindow()
