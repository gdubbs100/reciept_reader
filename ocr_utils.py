import easyocr
import cohere
import numpy as np

## OCR
def extract_text(img:np.array):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(img)
    return " ".join([res[1] for res in result])


## LLM prompts
PREAMBLE ="""
    You are an effective assistant with excellent attention to detail and follow instructions precisely. 
    You only provide the exact requested output and do not chat.
"""

BASE_MESSAGE = """
    create a json with structure: 
        {
            item (name of item): {
                "price": actual price paid for the item (real number), 
                "quantity":number purchased (integer), 
                "weight":weight of  the item (real number),
                "unit" : unit of weight (string)
            }
        } from: 
"""

EXTRA_MESSAGE = """
    only include shopping items. If an item is not a shopping item, call it "other".
    If weight is unavailable use 'None'. 
    Don't include weights in the item key.
"""

## LLM functions
def read_token():
    with open('./cohere_token.txt', 'r') as file:
        access_token = file.read()
    return access_token

# not ideal...
def create_message(base_message: str, text_to_parse: str, extra_message: str):
    return base_message + text_to_parse + extra_message

def extract_items(img):
    text_to_parse = extract_text(img)
    ## set up api connection
    access_token = read_token()
    co = cohere.Client(access_token)
    response = co.chat(
        preamble=PREAMBLE,
        message=create_message(
            BASE_MESSAGE,
            text_to_parse,
            EXTRA_MESSAGE
        )
    )
    return response.text