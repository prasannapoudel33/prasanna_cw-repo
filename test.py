from tkinter import *
from tkinter import filedialog, messagebox
import tkinter as tk
from PIL import Image, ImageTk
import os
from stegano import lsb

root = Tk()
root.title("Steganography Tool")
root.geometry("700x500")
root.configure(bg="#36454F")

filename = None  # Define filename as a global variable
secret = None  # Initialize secret variable for holding the steganographed image

def showimage():
    global filename
    file = filedialog.askopenfile(initialdir=os.getcwd(), title='Select Image File',
                                  filetype=(("PNG file", "*.png"), ("JPG File", "*.jpg"), ("All file", "*.*")))
    if file:
        filename = file.name  # Store the file name
        img = Image.open(filename)

        # Convert JPEG to PNG if necessary
        if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
            temp_filename = os.path.splitext(filename)[0] + '.png'  # Change file extension to .png
            img = img.convert('RGB')  # Convert image to RGB mode if it's not
            img.save(temp_filename)
            filename = temp_filename  # Update filename to the new PNG file

        img = ImageTk.PhotoImage(img)
        lbl.configure(image=img, width=250, height=250)
        lbl.img = img
    else:
        filename = None  # Ensure filename is None if no file is selected

def Hide():
    global filename
    global secret
    if filename is None:
        messagebox.showerror("Error", "No image selected. Please select an image first.")
        return
    message = text1.get(1.0, END)
    secret = lsb.hide(filename, message)
    text1.delete(1.0, END)  # Clear the text after hiding data

def Show():
    global filename
    if filename is None:
        messagebox.showerror("Error", "No image selected. Please select an image first.")
        return
    try:
        clear_message = lsb.reveal(filename)
        text1.delete(1.0, END)
        text1.insert(END, clear_message)
    except IndexError as e:
        text1.delete(1.0, END)
        text1.insert(END, "No hidden message found or message cannot be decoded.")

def reset():
    global filename
    global secret
    filename = None
    secret = None
    lbl.configure(image="", width=250, height=250)
    text1.delete(1.0, END)

def save():
    global secret
    if secret is None:
        messagebox.showerror("Error", "No hidden data to save. Please hide data first.")
        return
    filename_parts = os.path.splitext(filename)
    if secret.mode == 'RGBA':
        secret = secret.convert('RGB')
    new_filename = f"{filename_parts[0]}_stegno{filename_parts[1]}"
    secret.save(new_filename)
    reset()  # Reset the image and text after saving

# Icons and logos
image_icon = PhotoImage(file="logo.jpg")  # Ensure you have this file in your directory or update the path accordingly
root.iconphoto(False, image_icon)

logo = PhotoImage(file="logo.png")  # Ensure you have this file in your directory or update the path accordingly
Label(root, image=logo, bg="#2f4155").place(x=10, y=0)

Label(root, text="Ethical Hacking", bg="#2d4155", fg="white", font="arial 25 bold").place(x=100, y=20)

# First frame for image display
f = Frame(root, bd=3, bg="black", width=340, height=280, relief=GROOVE)
f.place(x=10, y=80)

lbl = Label(f, bg="black")
lbl.place(x=40, y=10)

# Second frame for text
frame2 = Frame(root, bd=3, width=340, height=280, bg="white", relief=GROOVE)
frame2.place(x=350, y=80)

text1 = Text(frame2, font="Roboto 20", bg="white", fg="black", relief=GROOVE, wrap=WORD)
text1.place(x=0, y=0, width=320, height=295)

scrollbar1 = Scrollbar(frame2)
scrollbar1.place(x=320, y=0, height=300)
scrollbar1.configure(command=text1.yview)
text1.configure(yscrollcommand=scrollbar1.set)

# Frame for image operations
frame3 = Frame(root, bd=3, bg="#2f4155", width=330, height=100, relief=GROOVE)
frame3.place(x=10, y=370)

Button(frame3, text="Open Image", width=10, height=2, font="arial 14 bold", command=showimage).place(x=20, y=30)
Button(frame3, text="Save Image", width=10, height=2, font="arial 14 bold", command=save).place(x=180, y=30)
Label(frame3, text="Picture, Image, Photo File", bg="#2f4155", fg="yellow").place(x=20, y=5)

# Frame for data operations
frame4 = Frame(root, bd=3, bg="#2f4155", width=330, height=100, relief=GROOVE)
frame4.place(x=360, y=370)

Button(frame4, text="Hide", width=6, height=2, font="arial 14 bold", command=Hide).place(x=20, y=30)
Button(frame4, text="Show", width=6, height=2, font="arial 14 bold", command=Show).place(x=180, y=30)
Button(frame4, text="Clear", width=6, height=2, font="arial 14 bold", command=reset).place(x=100, y=30)  # Clear All button
Label(frame4, text="Steganography Operations", bg="#2f4155", fg="yellow").place(x=20, y=5)

root.mainloop()
