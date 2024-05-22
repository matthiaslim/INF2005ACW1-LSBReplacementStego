import tkinter as tk
from tkinter import ttk
class SteganographyGui:
    def __init__(self,root):
        self.root = root
        self.root.title("Steganography")
        self.root.geometry("700x700")

        self.frame = tk.Frame(self.root)
        self.frame.pack(expand=True)

        # Style for buttons
        self.style = ttk.Style()
        self.style.configure("RoundedButton.TButton", padding=6, relief="flat", background="#ccc")
        self.style.map("RoundedButton.TButton",
                       background=[('active', '#bbb')],
                       relief=[('pressed', 'flat')])

        # Create Encode button
        self.encode_button = tk.Button(self.frame, text="Encode", command=self.encode, height=10,width=25)
        self.encode_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Create Decode button
        self.decode_button = tk.Button(self.frame, text="Decode", command=self.decode, height=10,width=25)
        self.decode_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def encode(self):
        print("Encoding")

    def decode(self):
        print("Decoding")

if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyGui(root)
    root.mainloop()