import tkinter as tk

class PopupWindow:
    def __init__(self, message):
        self.root = tk.Tk()
        self.root.title("Popup Window")
        self.label = tk.Label(self.root, text=message)
        self.label.pack(padx=10, pady=10)
        self.root.geometry("300x100")

    def show(self):
        self.root.mainloop()