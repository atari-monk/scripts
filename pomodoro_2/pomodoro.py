import time
import tkinter as tk
from tkinter import messagebox

def show_popup():
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', 1)
    messagebox.showinfo("Pomodoro", "Time to take a break!")

def pomodoro_timer(minutes):
    time.sleep(minutes * 60)
    show_popup()

if __name__ == "__main__":
    pomodoro_timer(0.05)
