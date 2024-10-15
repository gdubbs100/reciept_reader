import easyocr
import cohere
import cv2
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--file", type=str, help="file path to an image", default = './data/aldi.jpg'
)
parser.add_argument(
    "--message", 
    type=str, 
    help="instruct llm to parse output", 
    default="""
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
)

args = parser.parse_args()
img = cv2.imread(args.file)
reader = easyocr.Reader(['en'])
result = reader.readtext(
        img,
    )

tgt = [
    idx for idx, res in enumerate(result) 
    if res[1].lower() in ['tax invoice', 'total']
]

res = " ".join([res[1] for res in result])
print(res)


## can handle the token getting elsewhere?
with open('./cohere_token.txt', 'r') as file:
    access_token = file.read()

preamble="""You are an effective assistant with excellent attention to detail and follow instructions precisely. 
You only provide the exact requested output and do not chat."""
## set up api connection
co = cohere.Client(access_token)
response = co.chat(
    preamble=preamble,
    message=args.message + res + """
    only include shopping items. If an item is not a shopping item, call it "other".
    If weight is unavailable use 'None'. 
    Don't include weights in the item key.
    """
)
print(response.text)