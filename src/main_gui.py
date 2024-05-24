import tkinter as tk
from tkinterdnd2 import TkinterDnD
from main import EncodeDecodeGui


class SteganographyGui:
    def __init__(self, root):

        self.root = root
        self.root.title("Steganography")
        self.root.geometry("700x700")

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True, fill="both")

        self.encode_frame = tk.Frame(self.root)
        self.decode_frame = tk.Frame(self.root)

        self.lsb_count = tk.IntVar(value=1)
        self.cover_path = None
        self.payload_path = None
        self.decode_button = None
        self.encode_button = None

        self.create_main_gui()

    def create_main_gui(self):
        # Create Encode button
        # Create Encode button
        self.encode_button = tk.Button(self.main_frame, text="Encode", command=self.show_encode_page, height=10,
                                       width=25)
        self.encode_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Create Decode button
        self.decode_button = tk.Button(self.main_frame, text="Decode", command=self.show_decode_page, height=10,
                                       width=25)
        self.decode_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def create_encode_gui(self):
        self.clear_frame(self.encode_frame)
        EncodeDecodeGui(self.encode_frame, self.show_main_gui, self.lsb_count)

    def show_main_gui(self):
        self.encode_frame.pack_forget()
        self.decode_frame.pack_forget()
        self.main_frame.pack(expand=True, fill="both")

    def show_encode_page(self):
        self.main_frame.pack_forget()
        self.decode_frame.pack_forget()
        self.encode_frame.pack(expand=True, fill="both")
        self.create_encode_gui()

    def decode(self):
        print("Decoding")

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = SteganographyGui(root)
    root.mainloop()
