import tkinter as tk
import cv2
import easyocr
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

        # ## run the ocr  
        # reader = easyocr.Reader(['en'])
        # result = reader.readtext(
        #         img,
        #     )

        # # LLM parsing

        items = extract_items(img)
        # print as output
        ocr_result.config(text=items)

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

    # output label
    output_label = tk.Label(root, text="",fg="blue")
    output_label.pack(pady=20)

    # ocr result
    ocr_result = tk.Label(root, text="")
    ocr_result.pack(pady=20)

    # Start the GUI event loop
    root.mainloop()
