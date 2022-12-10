# Author: philip00000000

# simple image viewer
# Usage:
# use arrow key left and right to change image
# use h key to hide or show title bar of the window
# esc key to quit program

import sys
import os
import tkinter as tk100
import keyboard
from PIL import Image, ImageTk

# create the main window
root = tk.Tk()
root.geometry("500x500")
hide_title_bar = False

def get_png_jpg_files_from_working_directory():
    # Get the current working directory
    cwd = os.getcwd()
    # Get a list of all files and directories in the current directory
    all_items = os.listdir(cwd)
    # Filter the list to only include files (not directories)
    files = [item for item in all_items if os.path.isfile(os.path.join(cwd, item))]
    filtered_list = list(filter(lambda s: s.endswith(".png") or s.endswith(".jpg"), files))
    return filtered_list

# create a list of items to be displayed
items = get_png_jpg_files_from_working_directory()
current_item = 0

def change_image():
    if root.winfo_width() > 1 and root.winfo_height() > 1:
        global image
        root.title(items[current_item]) # set title bar of root window
        image = Image.open(items[current_item])
        if (image.width > root.winfo_width() or image.height > root.winfo_height()) and \
            image.height > image.width:
            ratio = root.winfo_height() / image.height
            new_size = image.width * ratio
            image = image.resize((int(new_size), root.winfo_height()))
        elif (image.width > root.winfo_width() or image.height > root.winfo_height()) and \
            image.width > image.height:
            ratio = root.winfo_width() / image.width
            new_size = image.height * ratio
            image = image.resize((root.winfo_width(), int(new_size)))
        image = ImageTk.PhotoImage(image)
        image_label.config(image=image)

# create a function to switch to the next item in the list
def next_item():
    global current_item
    current_item += 1
    if current_item >= len(items):
        current_item = 0
    change_image()

# create a function to switch to the previous item in the list
def previous_item():
    global current_item
    current_item -= 1
    if current_item < 0:
        current_item = len(items) - 1
    change_image()

# check if folder contains images
if len(items) == 0:
    sys.exit("Empty folder, folder contains no .png or .jpg files")

# check if any command-line arguments were passed, if yes use it as first image
if len(sys.argv) > 1:
    # check if the variable is a string
    if type(sys.argv[1]) == str:
        # check if "sys.argv[1]" is in the list(contains all .png and .jpg files in the folder)
        if sys.argv[1] in items:
            # Get the index of the first occurrence of the string "sys.argv[1]" in the list
            current_item = items.index(sys.argv[1])
        else:
            sys.exit("Argument passed dose not exist in the folder as a .jpg or .png file")
    else:
        sys.exit("Argument passed, not a string")

first_image = items[current_item]
root.title(first_image) # set title bar of root window
# open the image and convert it to a format that can be used by tkinter
image = Image.open(first_image)
image = ImageTk.PhotoImage(image)
# create a frame widget so that the label is in the middle of the window
frame=tk.Frame(root)
frame.grid(row=0, column=0, sticky="NW")
# create an image label to display the image
image_label = tk.Label(root, image=image)
image_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Define the function to be called when the left or right arrow key is pressed
def move(direction):
    if direction == "right":
        # Perform the action for moving left
        next_item()
    elif direction == "left":
        # Perform the action for moving right
        previous_item()
    elif direction == "hide": # Hide the title bar of the window
        global hide_title_bar
        if hide_title_bar == False:
            root.overrideredirect(True)
            hide_title_bar = True
        else: # elif hide_title_bar == True:
            root.overrideredirect(False)
            hide_title_bar = False
    elif direction == "esc":
        root.destroy()

# Listen for the left and right arrow keys to be pressed
keyboard.on_press_key("left", lambda _: move("left"))
keyboard.on_press_key("right", lambda _: move("right"))
keyboard.on_press_key("h", lambda _: move("hide"))
keyboard.on_press_key("esc", lambda _: move("esc"))

# Define a function to handle the <Configure> event (The size of the widget changed)
def handle_resize(event):
    change_image()

# Bind the function to the <Configure> event on the root window
root.bind("<Configure>", handle_resize)

# run the main event loop
root.mainloop()
