import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
from gui import SteganographyGui
from stego_image import encode_image, decode_image
from stego_audio import encode_audio, decode_audio
import os


class EncodeDecodeGui:

    def __init__(self, parent, back_callback, lsb_count):
        self.parent = parent
        self.back_callback = back_callback
        self.lsb_count = lsb_count

        self.cover_path = None
        self.payload_path = None

        self.create_widgets()

    def create_widgets(self):
        self.encode_back_button = tk.Button(self.parent, text="Back", command=self.back_callback)
        self.encode_back_button.pack(pady=10)

        self.payload_label = tk.Label(self.parent, text="Drag and drop your payload file here")
        self.payload_label.pack(pady=10)
        self.payload_label.drop_target_register(DND_FILES)
        self.payload_label.dnd_bind('<<Drop>>', self.drop_payload)

        self.cover_label = tk.Label(self.parent, text="Drag and drop cover file here")
        self.cover_label.pack(pady=10)
        self.cover_label.drop_target_register(DND_FILES)
        self.cover_label.dnd_bind('<<Drop>>', self.drop_cover)

        self.encode_confirm_button = tk.Button(self.parent, text="Confirm", command=self.encode_message)
        self.encode_confirm_button.pack(pady=10)

    # Functions to handle encoding and decoding
    def encode_message(self):
        # global cover_path, payload_path, lsb_count
        if not self.cover_path or not self.payload_path:
            messagebox.showerror("Error", "Please select cover and payload files.")
            return

        try:
            if self.cover_path.lower().endswith(('.png', '.bmp', '.gif')):
                with open(self.payload_path, 'r') as f:
                    text = f.read()
                output_path = filedialog.asksaveasfilename(defaultextension=".png")
                if output_path:
                    encode_image(self.cover_path, text, self.lsb_count.get(), output_path)
                    messagebox.showinfo("Success", f"Message encoded and saved to {output_path}")

            elif self.cover_path.lower().endswith(('.wav')):
                with open(self.payload_path, 'r') as f:
                    text = f.read()
                output_path = filedialog.asksaveasfilename(defaultextension=".wav")
                if output_path:
                    encode_audio(self.cover_path, text, self.lsb_count.get(), output_path)
                    messagebox.showinfo("Success", f"Message encoded and saved to {output_path}")

            else:
                messagebox.showerror("Error", "Unsupported cover file type.")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # def decode_message():
    #     global stego_path, lsb_count
    #     if not stego_path:
    #         messagebox.showerror("Error", "Please select a stego file.")
    #         return
    #
    #     try:
    #         if stego_path.lower().endswith(('.png', '.bmp', '.gif')):
    #             message = decode_image(stego_path, lsb_count.get())
    #             messagebox.showinfo("Decoded Message", f"The hidden message is:\n{message}")
    #
    #         elif stego_path.lower().endswith(('.wav')):
    #             message = decode_audio(stego_path, lsb_count.get())
    #             messagebox.showinfo("Decoded Message", f"The hidden message is:\n{message}")
    #
    #         else:
    #             messagebox.showerror("Error", "Unsupported stego file type.")
    #
    #     except Exception as e:
    #         messagebox.showerror("Error", str(e))

    # Functions to handle drag and drop
    def drop_cover(self, event):
        # global cover_path
        cover_path = event.data
        self.cover_label.config(text=os.path.basename(cover_path))

    def drop_stego(self, event):
        # global stego_path
        stego_path = event.data
        self.stego_label.config(text=os.path.basename(stego_path))

    def drop_payload(self, event):
        # global payload_path
        payload_path = event.data
        self.payload_label.config(text=os.path.basename(payload_path))

    # Setup GUI elements
    # cover_label, stego_label, payload_label, lsb_scale, encode_button, decode_button = SteganographyGui(root, lsb_count, encode_message, decode_message, drop_cover, drop_stego, drop_payload)

    # root.mainloop()
