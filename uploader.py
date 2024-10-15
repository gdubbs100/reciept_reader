import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Function to open file dialog and display the image
def upload_image():
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
    )
    if file_path:
        img = Image.open(file_path)
        img = img.resize((300, 300))  # Resize the image to fit in the label
        img_tk = ImageTk.PhotoImage(img)
        panel.config(image=img_tk)
        panel.image = img_tk

if __name__=="__main__":

    # Create main application window
    root = tk.Tk()
    root.title("Photo Uploader")

    # Create a button to upload image
    upload_btn = tk.Button(root, text="Upload Photo", command=upload_image)
    upload_btn.pack(pady=20)

    # Label to display uploaded image
    panel = tk.Label(root)
    panel.pack(pady=20)

    # Start the GUI event loop
    root.mainloop()
