import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
from gui import SteganographyGui
from stego_image import encode_image, decode_image
from stego_audio import encode_audio, decode_audio
import os

# Initialize main window
root = TkinterDnD.Tk()
root.title("Steganography Tool")

# Global variables for storing paths and LSB count
cover_path = None
stego_path = None
payload_path = None
lsb_count = tk.IntVar(value=1)


# Functions to handle encoding and decoding
def encode_message():
    global cover_path, payload_path, lsb_count
    if not cover_path or not payload_path:
        messagebox.showerror("Error", "Please select cover and payload files.")
        return

    try:
        if cover_path.lower().endswith(('.png', '.bmp', '.gif')):
            with open(payload_path, 'r') as f:
                text = f.read()
            output_path = filedialog.asksaveasfilename(defaultextension=".png")
            if output_path:
                encode_image(cover_path, text, lsb_count.get(), output_path)
                messagebox.showinfo("Success", f"Message encoded and saved to {output_path}")

        elif cover_path.lower().endswith(('.wav')):
            with open(payload_path, 'r') as f:
                text = f.read()
            output_path = filedialog.asksaveasfilename(defaultextension=".wav")
            if output_path:
                encode_audio(cover_path, text, lsb_count.get(), output_path)
                messagebox.showinfo("Success", f"Message encoded and saved to {output_path}")

        else:
            messagebox.showerror("Error", "Unsupported cover file type.")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def decode_message():
    global stego_path, lsb_count
    if not stego_path:
        messagebox.showerror("Error", "Please select a stego file.")
        return

    try:
        if stego_path.lower().endswith(('.png', '.bmp', '.gif')):
            message = decode_image(stego_path, lsb_count.get())
            messagebox.showinfo("Decoded Message", f"The hidden message is:\n{message}")

        elif stego_path.lower().endswith(('.wav')):
            message = decode_audio(stego_path, lsb_count.get())
            messagebox.showinfo("Decoded Message", f"The hidden message is:\n{message}")

        else:
            messagebox.showerror("Error", "Unsupported stego file type.")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# Functions to handle drag and drop
def drop_cover(event):
    global cover_path
    cover_path = event.data
    cover_label.config(text=os.path.basename(cover_path))


def drop_stego(event):
    global stego_path
    stego_path = event.data
    stego_label.config(text=os.path.basename(stego_path))


def drop_payload(event):
    global payload_path
    payload_path = event.data
    payload_label.config(text=os.path.basename(payload_path))


# Setup GUI elements
cover_label, stego_label, payload_label, lsb_scale, encode_button, decode_button = setup_gui(root, lsb_count, encode_message, decode_message, drop_cover, drop_stego, drop_payload)

root.mainloop()
