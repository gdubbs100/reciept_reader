import tkinter as tk
import cv2
import easyocr
import ast
import json

from tkinter import filedialog
from PIL import Image, ImageTk
from datetime import datetime, date
from ocr_utils import extract_items

entry_dict = dict()
COUNTER = 0
BASE_ATTRIBUTES = {
    'price':0.0,
    'quantity':0,
    'weight':0.0,
    'unit':'g',
    'name':''
}

# Function to open file dialog and display the image
def upload_image():

    # get the file
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
    )
    if file_path:
        # disable the button
        upload_btn.config(state="disabled")

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

        save_button = tk.Button(frame, text="Save to JSON", command=save_to_json)
        save_button.pack(side="left",pady=10)

        new_upload_btn = tk.Button(frame, text="New upload", command=lambda: new_upload(frame))
        new_upload_btn.pack(side="left",pady=10)

        create_entries(frame, items)


def new_upload(frame):
    frame.destroy()
    upload_btn.config(state="normal")

def remove_frame(frame, item):
    frame.destroy()
    del entry_dict[item]

## can I make this more generic to handle new items and items from ocr output???
def add_entry_frame(parent):
    global COUNTER
    COUNTER +=1
    item = f"new_item_{COUNTER}"
    item_frame = tk.LabelFrame(parent, text=item)
    item_frame.pack(padx=10, pady=5, fill="both", expand=True)

    remove_btn = tk.Button(item_frame, text="Remove item", 
        command=lambda f=item_frame,i=item: remove_frame(item_frame, item))
    remove_btn.pack(side="right", padx=5, pady=5)

    entry_dict[item] = {}
    for attribute, value in BASE_ATTRIBUTES.items():
        # Create a label and entry for each attribute (price, quantity, etc.)
        label = tk.Label(item_frame, text=f"{attribute.capitalize()}:")
        label.pack(side="left", padx=5, pady=5)

        entry = tk.Entry(item_frame)
        try:
            entry.insert(0, str(value))  # Insert the current value
            entry.pack(side="left", padx=5, pady=5)
        except:
            print(f"something went wrong with: {value}")
            entry = None
        
        # Save the entry widget reference in entry_dict
        entry_dict[item][attribute] = entry

# Function to create the Entry fields dynamically from the items dictionary
def create_entries(parent, nested_dict):
    ## new item button
    add_item_btn = tk.Button(
        parent, text="Add item", 
        command=lambda f=parent:add_entry_frame(f))
    add_item_btn.pack(side="left", padx=5, pady=5)

    ## include the date
    date_label = tk.Label(parent, text=f"Date:")
    date_label.pack(side="top", padx=5, pady=5)
    entry_dict['date'] = tk.Entry(parent)
    entry_dict['date'].insert(0, date.today())
    entry_dict['date'].pack(side="top", padx=5, pady=5)

    ## include entry for the shop
    shop_label = tk.Label(parent, text=f"Shop:")
    shop_label.pack(side="top", padx=5, pady=5)
    entry_dict['shop'] = tk.Entry(parent)
    entry_dict['shop'].pack(side="top", padx=5, pady=5)

    ## iterate through dict items
    for item, attributes in nested_dict.items():
        # Create a labeled frame for each item
        item_frame = tk.LabelFrame(parent, text=item)
        item_frame.pack(padx=10, pady=5, fill="both", expand=True)

        remove_btn = tk.Button(item_frame, text="Remove item", 
            command=lambda f=item_frame,i=item: remove_frame(item_frame, item))
        remove_btn.pack(side="right", padx=5, pady=5)
        
        entry_dict[item] = {}
        attributes['name'] = item
        for attribute, value in attributes.items():
            # Create a label and entry for each attribute (price, quantity, etc.)
            label = tk.Label(item_frame, text=f"{attribute.capitalize()}:")
            label.pack(side="left", padx=5, pady=5)

            entry = tk.Entry(item_frame)
            try:
                entry.insert(0, str(value))  # Insert the current value
                entry.pack(side="left", padx=5, pady=5)
            except:
                print(f"something went wrong with: {value}")
                entry = None
            
            # Save the entry widget reference in entry_dict
            entry_dict[item][attribute] = entry


# Function to save edits and export to a JSON file
def save_to_json():
    updated_data = {}
    filename = f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}_{entry_dict['shop'].get().lower()}.json"
    
    # Iterate through the entry_dict and collect updated values
    for key, attributes in entry_dict.items():
        ## log the first two bits of data
        if key in ['date', 'shop']:
            updated_data[key] = attributes.get()
        ## iterate through the items
        else:
            item = attributes["name"].get()
            updated_data[item] = {}
            for attribute, entry_widget in attributes.items():
                value = entry_widget.get()

                # Convert values back to appropriate types
                if attribute == "price" or attribute == "weight":
                    updated_data[item][attribute] = float(value)
                elif attribute == "quantity":
                    updated_data[item][attribute] = int(value)
                elif attribute == "name":
                    pass
                else:  # 'unit' is a string
                    updated_data[item][attribute] = value.lower()

    # Write the updated data to a JSON file
    with open(f"./data/ocr_output/{filename}", 'w') as f:
        json.dump(updated_data, f, indent=4)
    
    print(f"Saved to ./data/ocr_output/{filename}")

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
