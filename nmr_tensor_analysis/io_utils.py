import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog

def select_file():
    filename = filedialog.askopenfilename(
        title="Select an excel file",
        filetypes=[('excel file', '*.xlsx *.xls')]
    )
    if filename:
        data = pd.read_excel(filename, header=None)
        print("Data loaded")
        return data

def select_folder_to_save():
    base_path = filedialog.askdirectory(title="Select a folder to save")
    if base_path:
        if os.path.exists(base_path):
            print(f"Selected folder: {base_path}")
            return base_path
        else:
            print("The folder does not exist.")
            return None
    else:
        print("No folder selected.")
        return None

def ask_best_rank():
    best_rank = simpledialog.askfloat("Rank value", "Best rank value")
    if best_rank is not None:
        return int(best_rank)
    else:
        return None