import tkinter as tk
import numpy as np


# TODO: Add method that closes window/ loop when save is pressed?

RANKS = "AKQJT98765432"

class RangeMatrixEditor:
    def __init__(self, master):
        self.master = master
        master.title("Range Matrix Editor")
        
        # Filename label + entry at the top
        self.filename_var = tk.StringVar()
        self.filename_var.set("range_matrix.npy")

        tk.Label(master, text="Filename:").grid(row=0, column=0, sticky="e")
        tk.Entry(master, textvariable=self.filename_var, width=20).grid(row=0, column=1, columnspan=5, sticky="w")

        self.matrix = np.zeros((13, 13), dtype=int)
        self.canvas_cells = [[None for _ in range(13)] for _ in range(13)]

        cell_size = 35

        for i in range(13):
            for j in range(13):
                frame = tk.Frame(master, width=cell_size, height=cell_size)
                frame.grid_propagate(False)
                frame.grid(row=i+2, column=j+1)  # <--- note: i+2 now

                canvas = tk.Canvas(frame, width=cell_size, height=cell_size, bg='white', highlightthickness=1)
                canvas.pack()
                canvas.bind("<Button-1>", self._make_toggle_handler(i, j))
                self.canvas_cells[i][j] = canvas

                hand_label = self._get_hand_label(i, j)
                canvas.create_text(cell_size // 2, cell_size // 2, text=hand_label, font=("Arial", 8), fill="black")

        # Row and column headers
        for i in range(13):
            tk.Label(master, text=RANKS[i]).grid(row=1, column=i+1)        # column labels
            tk.Label(master, text=RANKS[i]).grid(row=i+2, column=0)        # row labels

        # Save/load buttons
        tk.Button(master, text="Save", command=self.save_matrix).grid(row=16, column=0, columnspan=7, sticky="ew")
        tk.Button(master, text="Load", command=self.load_matrix).grid(row=16, column=7, columnspan=7, sticky="ew")

    def _make_toggle_handler(self, i, j):
        def handler(event=None):
            self.matrix[i][j] = 1 - self.matrix[i][j]
            color = "green" if self.matrix[i][j] == 1 else "white"
            self.canvas_cells[i][j].configure(bg=color)
        return handler

    def _get_hand_label(self, i, j):
        r1 = RANKS[i]
        r2 = RANKS[j]
        if i == j:
            return r1 + r2
        elif i < j:
            return r1 + r2 + "s"
        else:
            return r2 + r1 + "o"

    def save_matrix(self):
        filename = self.filename_var.get()
        if not filename.endswith(".npy"):
            filename += ".npy"
        try:
            np.save(filename, self.matrix)
            print(f"Saved to {filename}")
        except Exception as e:
            print(f"Failed to save: {e}")

    def load_matrix(self):
        filename = self.filename_var.get()
        if not filename.endswith(".npy"):
            filename += ".npy"
        try:
            self.matrix = np.load(filename)
            for i in range(13):
                for j in range(13):
                    color = "green" if self.matrix[i][j] == 1 else "white"
                    self.canvas_cells[i][j].configure(bg=color)
            print(f"Loaded from {filename}")
        except Exception as e:
            print(f"Failed to load matrix from {filename}: {e}")


def Create_RangeChart():
    root = tk.Tk()
    app = RangeMatrixEditor(root)
    root.mainloop()
    print('File created.')


if __name__ == "__main__":
    root = tk.Tk()
    app = RangeMatrixEditor(root)
    root.mainloop()