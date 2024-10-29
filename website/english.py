from PIL import Image, ImageDraw, ImageFont
import requests
import random
import json

def get_image(query , name , api):
    print(f"Getting image for : {query} using api {api}")
    if api == 1 :
        url = f"https://serpapi.com/search.json?engine=google_images&ijn=0&api_key=da75049319abb43ed97ac5e729c1e1cac35280e3d214de6962674b7c0dc9d09a&q={query}"

        try:
            # Send GET request to SerpApi
            response = requests.get(url)
            response.raise_for_status()

            # Parse JSON response
            data = response.json()

            # Check for 'images_results' in the response data
            if "images_results" in data:
                # Retrieve the first 10 results
                first_10_results = data["images_results"][:30]

                # Select a random image result from the first 10
                random_result = random.choice(first_10_results)

                # Print the 'original' URL of the random result
                # print( random_result.get("original"))
                response = requests.get(random_result.get("original"))
                print(f"Saving {name}")
                with open(f"./website/english/{name}.png", "wb") as file:
                    file.write(response.content)
            else:
                print("No image results found.")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
    elif api == 2 :
        ACCESS_KEY = 'FXdShCO15K4YL4s6myacxoVdl75PjlGBi_sT23CHOGI'

        url = 'https://api.unsplash.com/search/photos'

        headers = {'Authorization': f'Client-ID {ACCESS_KEY}'}

        params = {
            'query': query,
            'per_page': 1
        }

        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            image_urls = [photo['urls']['regular'] for photo in data['results']]

        else:
            print("Failed to fetch data:", response.json())
        for url in image_urls:
            response = requests.get(url)
            with open(f"./website/english/{name}.png", "wb") as file:
                file.write(response.content)    

    else :
        print("Choose a valid api number")
        print("exiting...")
        exit()

prompt = "Hello, I would like assistance similar to how I interacted in a previous chat with ChatGPT. Here’s what I typically need: Text Generation: When I provide two or more words, please give me structured information for each word in JSON format, including: Today's POWER WORD: The word itself. Definition: A clear explanation of what the word means. Part of Speech: Indicate whether it's a noun, verb, adjective, etc. Synonyms: List two or more words that mean the same or similar, as a single text string separated by commas, not as a list. Antonyms: List two or more words that mean the opposite, also as a single text string separated by commas. Related Words: Suggest words that are conceptually related, as a single text string with commas. Your OWN Sentence: Use the word in a clear example sentence. Search: A search query I can use to find an accurate image for the word. Return everything as structured JSON text with words as an array of entries for each word. IMPORTANT DONT SAY A WORD ONLY SEND THE JSON DATA!!!"


import argparse

# Initialize the parser
parser = argparse.ArgumentParser(description="Process input words, name and ID, and API choice.")

# Adding arguments
parser.add_argument("words", type=str, help="Input words")
parser.add_argument("name_and_id", type=str, help="Name and ID (e.g., Amr Ayman 192400300)")
parser.add_argument("api", type=int, choices=[1, 2], help="Choose API Number (1 for accurate results but limited, 2 for unlimited)")

parser.add_argument("outputname", type=str, help="File name")

parser.add_argument("nonce", type=str, help="Wordpress nonce needs to be done manual")


# Parsing arguments
args = parser.parse_args()

# Accessing values
words = args.words
name_and_id = args.name_and_id
api = args.api
outputname = args.outputname

nonce = args.nonce


print("nonce = " + nonce)
print("outputname = " + outputname)


print("\nWaiting for Chatgpt's Response")

headers = {
    'Accept': '*/*',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'X-WP-Nonce': f'{nonce}',
}

json_data = {
    'botId': 'default',
    'customId': None,
    'session': 'N/A',
    'chatId': '1',
    'contextId': 1,
    'messages': [
        {
            'id': '',
            'role': 'assistant',
            'content': f'{prompt}',
            'who': 'AI: ',
            'timestamp': 1,
        },
    ],
    'newMessage': f'{words}',
    'newFileId': None,
    'stream': False,
}

response = requests.post('https://masrgpt.com/wp-json/mwai-ui/v1/chats/submit', headers=headers, json=json_data)


json_data = response.json()


# print(json_data["reply"])



data = json.loads(json_data["reply"])
for i, word in enumerate(data["words"], start=1):
    search_term = word["Search"]
    filename = f"img{i}"
    get_image(search_term, filename , api)



fields_data = {
    "Name & ID": {"text": f"{name_and_id}", "coords": (100 , 10), "max_x": 330, "max_y": 30},  
    #Word 1
    "Today's POWER WORD 1": {"text": "", "coords": (25, 120), "max_x": 144, "max_y": 166},  
    "Definition 1": {"text": "", "coords": (172, 117), "max_x": 442, "max_y": 166},
    "Part of Speech 1": {"text": "", "coords": (25, 197), "max_x": 148, "max_y": 216},
    "Synonyms 1": {"text": "", "coords": (172, 195), "max_x": 295, "max_y": 213},
    "Antonyms 1": {"text": "", "coords": (315, 197), "max_x": 435, "max_y": 213},
    "Related Words 1": {"text": "", "coords": (25, 250), "max_x": 290, "max_y": 260},
    "Your OWN Sentence 1": {"text": "", "coords": (26, 296), "max_x": 289, "max_y": 334},

    #Word 2 
    "Today's POWER WORD 2": {"text": "", "coords": (25, 383), "max_x": 144, "max_y": 429 },  
    "Definition 2": {"text": "", "coords": (176 , 387), "max_x": 434, "max_y": 424},
    "Part of Speech 2": {"text": "", "coords": (25 , 463), "max_x": 148, "max_y": 482},
    "Synonyms 2": {"text": "", "coords": (172, 463), "max_x": 295, "max_y": 477},
    "Antonyms 2": {"text": "", "coords": (315, 457), "max_x": 435, "max_y": 484},
    "Related Words 2": {"text": "", "coords": (25, 510), "max_x": 290, "max_y": 527},
    "Your OWN Sentence 2": {"text": "", "coords": (26, 560), "max_x": 289, "max_y": 596},  
}

def update_fields_data(fields_data, data):
    for i, word_data in enumerate(data["words"], start=1):
        # Update each field for the current word
        fields_data[f"Today's POWER WORD {i}"]["text"] = word_data["Today's POWER WORD"]
        fields_data[f"Definition {i}"]["text"] = word_data["Definition"]
        fields_data[f"Part of Speech {i}"]["text"] = word_data["Part of Speech"]
        fields_data[f"Synonyms {i}"]["text"] = word_data["Synonyms"]
        fields_data[f"Antonyms {i}"]["text"] = word_data["Antonyms"]
        fields_data[f"Related Words {i}"]["text"] = word_data["Related Words"]
        fields_data[f"Your OWN Sentence {i}"]["text"] = word_data["Your OWN Sentence"]
    
    return fields_data

# Example usage
updated_fields_data = update_fields_data(fields_data, data)



def make_image_final():
    # Load the main image (worksheet)
    main_image_path = "./website/english/main.png"
    main_image = Image.open(main_image_path)
    draw = ImageDraw.Draw(main_image)

    # Define the font path and sizes
    font_path = "./website/english/Arial.ttf"  # Ensure the font file path is correct
    max_font_size = 30
    min_font_size = 10
    # Function to add wrapped text to fit within specified max x and max y
    def add_wrapped_text(draw, text, coords, max_x, max_y, font_path, max_font_size, min_font_size):
        font_size = max_font_size
        font = ImageFont.truetype(font_path, font_size)
        max_width = max_x - coords[0]
        max_height = max_y - coords[1]

        # Adjust font size to fit within width and height
        while (draw.textlength(text, font=font) > max_width or font.getbbox(text)[3] > max_height) and font_size > min_font_size:
            font_size -= 1
            font = ImageFont.truetype(font_path, font_size)

        # Prepare for word wrapping within the box
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if draw.textlength(test_line, font=font) <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        y_text = coords[1]
        line_height = font.getbbox("A")[3]
        for line in lines:
            if y_text + line_height > max_y:
                break
            draw.text((coords[0], y_text), line, font=font, fill="black")
            y_text += line_height

    # Add text fields
    for field_name, field_info in fields_data.items():
        add_wrapped_text(
            draw,
            field_info["text"],
            field_info["coords"],
            field_info["max_x"],
            field_info["max_y"],
            font_path,
            max_font_size,
            min_font_size
        )

    # Function to add an image within a defined box
    def add_image(main_image, added_image_path, x_min, y_min, x_max, y_max):
        added_image = Image.open(added_image_path)
        max_width = x_max - x_min
        max_height = y_max - y_min

        # Resize added image to fit within max width and max height
        added_image.thumbnail((max_width, max_height))
        
        # Calculate position to center the image within the area
        center_x = x_min + (max_width - added_image.width) // 2
        center_y = y_min + (max_height - added_image.height) // 2
        
        # Paste the image onto the main image
        main_image.paste(added_image, (center_x, center_y))

    # Add Image 1 within specified coordinates
    add_image(main_image, "./website/english/img1.png", 319, 255, 432, 338)

    # Add Image 2 within specified coordinates
    add_image(main_image, "./website/english/img2.png", 319, 524, 432, 602)

    # main_image.show()
    main_image.save(f"./website/static/english/{outputname}.png")
    main_image.open()
    # main_image.save("C:/Users/Spy/Desktop/English/filled_word_wizard_with_images.png")


make_image_final()