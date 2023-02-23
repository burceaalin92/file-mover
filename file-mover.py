import tkinter as tk
import os
import sys
import pathlib
from tkinter import filedialog
from tkinter import PhotoImage

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(pathlib.Path(__file__).parent.absolute(), relative_path)

def browse_source():
    source_folder = filedialog.askdirectory()
    source_entry.delete(0, tk.END)
    source_entry.insert(0, source_folder)
    display_files(source_folder, files_list1)

def browse_destination():
    destination_folder = filedialog.askdirectory()
    destination_entry.delete(0, tk.END)
    destination_entry.insert(0, destination_folder)


def move_files(event):
    files_list2.delete(0, tk.END)
    source_folder = source_entry.get()
    destination_folder = destination_entry.get()
    keyword = keyword_entry.get()

    if not source_folder or not destination_folder or not keyword:
        tk.messagebox.showerror("Error", "Source, Destination and Keyword are required.")
        return

    moved_files = []
    for subdir, dirs, files in os.walk(source_folder):
        for file in files:
            if keyword in file:
                file_path = os.path.join(subdir, file)
                destination_path = os.path.join(destination_folder, file)
                try:
                    os.rename(file_path, destination_path)
                except:
                    tk.messagebox.showerror("Error", "Could not move the file '{}'".format(file))
                    return
                moved_files.append(file)

    if not moved_files:
        tk.messagebox.showerror("Error", "No files matching the keyword found in the source directory.")
        return

    for file in moved_files:
        files_list2.insert(tk.END, file)

    # Call display_files to refresh the list of files in the source folder
    display_files(source_folder, files_list1)




def display_files(folder, listbox):
    listbox.delete(0, tk.END)
    for root, dirs, files in os.walk(folder):
        for file_name in files:
            listbox.insert(tk.END, os.path.join(root, file_name))


root = tk.Tk()
root.title("File Mover")

source_label = tk.Label(root, text="Source Directory:")
source_label.grid(row=0, column=0, padx=10, pady=10)

source_entry = tk.Entry(root)
source_entry.grid(row=0, column=1, padx=10, pady=10)

source_button = tk.Button(root, text="Browse", command=browse_source)
source_button.grid(row=0, column=2, padx=10, pady=10)

destination_label = tk.Label(root, text="Destination Directory:")
destination_label.grid(row=1, column=0, padx=10, pady=10)

destination_entry = tk.Entry(root)
destination_entry.grid(row=1, column=1, padx=10, pady=10)

destination_button = tk.Button(root, text="Browse", command=browse_destination)
destination_button.grid(row=1, column=2, padx=10, pady=10)

keyword_label = tk.Label(root, text="Keyword:")
keyword_label.grid(row=2, column=0, padx=10, pady=10)

keyword_entry = tk.Entry(root)
keyword_entry.grid(row=2, column=1, padx=10, pady=10)


move_button = tk.Button(root, text="Move Files", command=lambda: move_files(None))
move_button.grid(row=2, column=2, padx=10, pady=10)
move_button.bind('<Return>', move_files)
root.bind('<Return>', move_files)


files_list1 = tk.Listbox(root, width=70, height=10)
files_list1.grid(row=0, column=3, rowspan=5, padx=10, pady=10)

files_list2 = tk.Listbox(root, width=70, height=10)
files_list2.grid(row=5, column=3,  padx=10, pady=30)

logo = PhotoImage(file=resource_path("PrimeNewLogoWhite.png"))

logo_label = tk.Label(root, image=logo)
logo_label.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="S")

creator_label = tk.Label(root, text="© created by Alin Burcea", font=("Helvetica", 7))
creator_label.place(relx=0.92, rely=1, anchor="s")



root.mainloop()