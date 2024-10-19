import tkinter as tk
import cv2
import easyocr
import ast
import json

from tkinter import filedialog
from PIL import Image, ImageTk
from ocr_utils import extract_items

# Function to open file dialog and display the image
def upload_image():
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
    )
    if file_path:

        img = cv2.imread(file_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_resized = cv2.resize(img_rgb, (300, 300))
        
        # Convert the cv2 image to PIL format for displaying in Tkinter
        img_pil = Image.fromarray(img_resized)
        img_tk = ImageTk.PhotoImage(img_pil)
        panel.config(image=img_tk)
        panel.image = img_tk

        # Print the file path below the image
        output_label.config(text=f"Uploaded Image Path: {file_path}")

        items = extract_items(img)
        items = items.replace('null', 'None')
        items = ast.literal_eval(items)

        frame = tk.Frame(root)
        frame.pack(side=tk.RIGHT)
        create_editable_fields(frame, items)
        submit_btn = tk.Button(root, text="log data", command=lambda: write_json(items))
        submit_btn.pack(pady=20)

## I actually want to get the data from the entry fields
def write_json(data):
    with open('./test.json', 'w') as f:
        json.dump(data, f)

def create_editable_fields(root, data):

    for idx, (key, value) in enumerate(data.items()):
        row_label = tk.Label(root, text=key)
        row_label.grid(row=idx * (len(value) + 1), column=0, pady=10)

        for jdx, (jkey, jvalue) in enumerate(value.items()):
            label = tk.Label(root, text=f"{jkey}:")
            label.grid(row=idx * (len(value) + 1) + jdx + 1, column=1, padx=5)

            entry= tk.Entry(root)
            entry.grid(row=idx * (len(value)+1) + jdx + 1, column =1, padx=5)
            entry.insert(0, str(jvalue))


if __name__=="__main__":

    # Create main application window
    root = tk.Tk()
    root.title("Photo Uploader")

    frame = tk.Frame()
    frame.pack(pady=20, side=tk.LEFT)

    # Create a button to upload image
    upload_btn = tk.Button(frame, text="Upload Photo", command=upload_image)
    upload_btn.pack(pady=20)

    # Label to display uploaded image
    panel = tk.Label(frame)
    panel.pack(pady=20)

    # output label
    output_label = tk.Label(frame, text="",fg="blue")
    output_label.pack(pady=20)

    # Start the GUI event loop
    root.mainloop()
