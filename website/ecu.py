#Imports ------------------------------------------------------------------------------------------------------------------------


from flask import Blueprint , request , abort , redirect , render_template , jsonify , render_template_string
import os
from dotenv import load_dotenv
from datetime import datetime
import requests
import json
import time
from flask_login import current_user
import random , re
from PIL import Image, ImageDraw, ImageFont
import pytz  #Time Zone 
from pathlib import Path
from . import mail
from flask_mail import Message


#------------------------------------------------------------------------------------------------------------------------
ecu = Blueprint('ecu', __name__)
load_dotenv()

def discord_log(message):
    messageeeee = {'content': message}
    payload = json.dumps(messageeeee)
    headers = {'Content-Type': 'application/json'}
    requests.post(
        "https://discord.com/api/webhooks/1220549855185997935/mkFuF-omKjobn77rSBMPqC6cYz2ddGUZGGc0VigjLs0J43cGwApQtQUlB6s1tDuCIQnt",
        data=payload,
        headers=headers)
    
    
#English Assignment
def discord_log_english(message):
    messageeeee = {'content': message}
    payload = json.dumps(messageeeee)
    headers = {'Content-Type': 'application/json'}
    requests.post(
        "https://discord.com/api/webhooks/1301261615349628998/r2g4m5zE-xedh4tPa9OyTIshOmDxgEOPeXvcfylb4Vo0NB44NJ9pl_fDHDWznTirOC_4",
        data=payload,
        headers=headers)
    
GOOGLESEACHAPI = os.getenv('GOOGLESEACHAPI')
SERASEARCHAPI = os.getenv('SERASEARCHAPI')
UNSPLASHSEARCHAPI = os.getenv('UNSPLASHSEARCHAPI')

usproxy = {
        "http": "http://nprofi:6f0reuyu@139.171.104.74:29842",
        "https": "http://nprofi:6f0reuyu@139.171.104.74:29842"
    }


chatgptnonce = {"nonce": "Not set yet!"}

@ecu.route("/english-assignment", methods=["GET", "POST"])
def english_assignment():
    if request.method == "GET":
        client_ip = request.headers.get('X-Forwarded-For')
        if client_ip:
            client_ip = client_ip.split(',')[0].strip()
        else:
            client_ip = request.headers.get('CF-Connecting-IP', request.remote_addr)

        user_agent = request.headers.get('User-Agent')
        device_type = "Desktop" if "Windows" in user_agent else (
        "Macintosh" if "Macintosh" in user_agent else "Mobile")

        if current_user.is_authenticated:
            if current_user.stage != "4" :
                if current_user.username != 'spy' :
                    return abort(404)
            if current_user.otp == "Waiting approval" :
             return render_template('users_pages/approve.html')
            if current_user.username != 'spy' :
                discord_log(f"{client_ip} Viewed <{request.url}>  {current_user.username} {device_type} ```{user_agent}```")
        else:
            discord_log(f"{client_ip} Viewed <{request.url}> {device_type} ```{user_agent}```")

    if request.method == "POST":
        try : 
            client_ip = request.headers.get('X-Forwarded-For')
            if client_ip:
                client_ip = client_ip.split(',')[0].strip()
            else:
                client_ip = request.headers.get('CF-Connecting-IP', request.remote_addr)

            word1 = request.form.get('word1')
            word2 = request.form.get('word2')


            name_and_id = request.form.get('name')

            quality = request.form.get('quality')

            assignment = request.form.get('assignment')

            if current_user.is_authenticated:
                api = "3"
                file_name = f"EnglishPDF_{current_user.username}"
                discord_log_english(f"{current_user.username} -- Making pdf for {name_and_id} ,  assignment {assignment} with words {word1} {word2} , api = {api} , quality = {quality} , ip = {client_ip} , file name = {file_name}")

            else :
                random_number = random.randint(1, 20)
                api = "2"
                file_name = f"EnglishPDF{random_number}"
                discord_log_english(f"Not logged -- Making pdf for {name_and_id} , assignment {assignment}  with words {word1} {word2} , api = {api} , quality = {quality} , ip = {client_ip} , file name = {file_name}")
            

            if not word2:
                if assignment == "5to7" or assignment == "8to10" :
                    new_message = f'Use the 1 word : "{word1}"'
                elif assignment == "1to4":
                    return render_template("used_pages/english_assignment_error.html" , error = "Provide 2 words for assignment 1 to 4")
            else:
                if assignment == "1to4":
                    new_message = f'Use the 2 words : "{word1}" and "{word2}"'
                elif assignment == "5to7" or assignment == "8to10":
                    new_message = f'Use the 1 word : "{word1}"'


            def get_image(query , name , api):
                # API 1 = sera 2 = upsplash 3 = google search
                # discord_log_english(f"Getting image for : {query} using api {api}")
                if api == "1" :
                    url = f"https://serpapi.com/search.json?engine=google_images&ijn=0&api_key={SERASEARCHAPI}&q={query}"
                    start_time = time.time()
                    try:
                        response = requests.get(url)
                        response.raise_for_status()

                        data = response.json()


                        if "images_results" in data:

                            print("Found images in google search for word : " + query)
                            first_10_results = data["images_results"][:5]

                            random_result = random.choice(first_10_results)

                            response = requests.get(random_result.get("original"))
                            print(f"Saving {name}")
                            with open(f"./website/english/{name}.png", "wb") as file:
                                file.write(response.content)
                                elapsed_time = time.time() - start_time
                                # discord_log_english(f"Took {elapsed_time:.2f} seconds to download {name}")
                        else:
                            discord_log_english("No image results found.")
                    except requests.exceptions.RequestException as e:
                        discord_log_english(f"Error: {e}")
                elif api == "2" :
                    start_time = time.time()

                    ACCESS_KEY = UNSPLASHSEARCHAPI

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
                        discord_log_english("Failed to fetch data: "  + response.json())
                    for url in image_urls:
                        response = requests.get(url)
                        with open(f"./website/english/{name}.png", "wb") as file:
                            file.write(response.content)    
                            elapsed_time = time.time() - start_time
                            # discord_log_english(f"Took {elapsed_time:.2f} seconds to download {name}")
                elif api == "3" :
                    try :
                        start_time = time.time()

                        def google_image_search(api_key, search_engine_id, query, num=3):
                            url = "https://www.googleapis.com/customsearch/v1"
                            params = {
                                "key": api_key,
                                "cx": search_engine_id,
                                "q": query,
                                "searchType": "image",  # Set searchType to image for image search
                                "num": num,  # Number of search results
                            }
                            
                            response = requests.get(url, params=params)
                            if response.status_code == 200:
                                return response.json()
                            else:
                                response.raise_for_status()

                        # Replace with your API key and CSE ID
                        api_key = GOOGLESEACHAPI
                        search_engine_id = "f3fc9931ca6ef42f8"


                        results = google_image_search(api_key, search_engine_id, query)
                        for item in results.get("items", []):
                            random_image = random.choice(results["items"])
                            image_link = random_image["link"]

                        response = requests.get(image_link)
                        with open(f"./website/english/{name}.png", "wb") as file:
                                file.write(response.content)    
                                elapsed_time = time.time() - start_time
                                # discord_log_english(f"Took {elapsed_time:.2f} seconds to download {name}")
                    except : 
                        pass
                else :
                    discord_log_english("Choose a valid api number")
                    print("exiting...")
                    return "Choose a valid api key"

            prompt = "Hello, I would like assistance similar to how I interacted in a previous chat with ChatGPT. Here is what I typically need: Text Generation: When I provide one or more words, please give me structured information for each word in JSON format, including: Today's POWER WORD: The word itself. Definition: A clear explanation of what the word means. Part of Speech: Indicate whether it's a noun, verb, adjective, etc. Synonyms: List two or more words that mean the same or similar, as a single text string separated by commas, not as a list. Antonyms: List two or more words that mean the opposite, also as a single text string separated by commas. Related Words: Suggest words that are conceptually related, as a single text string with commas. Your OWN Sentence: Use the word in a clear example sentence.Prefix of the word(s) provided. Search: A search query I can use to find an accurate image for the word. Return everything as structured JSON text with words as an array of entries for each word. IMPORTANT DONT SAY A WORD ONLY SEND THE JSON DATA AND CAPTLIZE THE FIRST LETTER!!!, GIVE 2 synonyms and 2 antynoms only if i asked for 1 word if i asked for 2 words give 3 and 3 for each word"

            global_start_time = time.time()

            global chatgptnonce
            nonce = chatgptnonce['nonce']
            start_time = time.time()

            headers = {
                'Accept': '*/*',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json',
                'X-WP-Nonce': nonce,
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
            'newMessage': new_message,
            'newFileId': None,
            'stream': False,
        }
            response = requests.post('https://masrgpt.com/wp-json/mwai-ui/v1/chats/submit', headers=headers, json=json_data , proxies=usproxy)

            json_data = response.json()

            # print(json_data["reply"])
            elapsed_time = time.time() - start_time

            # if response.status_code == 200 :
            #     discord_log_english(f"Got Chatgpt's reply Took {elapsed_time:.2f} seconds")

            #Get correct nonce
            if response.status_code != 200 :

                headers = {
                    'accept': '*/*',
                    'content-type': 'application/json',
                    'origin': 'https://masrgpt.com',
                    'referer': 'https://masrgpt.com/chatgpt/',

                }

                response = requests.post('https://masrgpt.com/wp-json/mwai/v1/start_session', headers=headers , proxies=usproxy)

                json_data = response.json()

                nonce = json_data["restNonce"]

                chatgptnonce["nonce"] = nonce

                elapsed_time = time.time() - start_time

                # discord_log_english("Got Chaptgpt's nonce : " + nonce + f" Took {elapsed_time:.2f} seconds")


                headers = {
                    'Accept': '*/*',
                    'Connection': 'keep-alive',
                    'Content-Type': 'application/json',
                    'X-WP-Nonce': nonce,
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
                    'newMessage': new_message,
                    'newFileId': None,
                    'stream': False,
                }

                response = requests.post('https://masrgpt.com/wp-json/mwai-ui/v1/chats/submit', headers=headers, json=json_data , proxies=usproxy)

                json_data = response.json()


            data = json.loads(json_data["reply"])
            key = next((k for k in data.keys() if k.lower() in ['words', 'word']), None)


            for i, word in enumerate(data[key], start=1):
                search_term = word["Search"]
                filename = f"img{i}"
                get_image(search_term, filename , api)


            timezone = pytz.timezone("Etc/GMT-2") 
            today_date = datetime.now(timezone).strftime("%d-%m-%Y")
    #-----------------------------------------------------------------------------------------------------------------
            if assignment == '1to4' :
                fields_data_high = {
                    "Name & ID": {"text": f"{name_and_id}", "coords": (1134 , 33), "max_x": 2785 , "max_y": 166},  
                    "Date": {"text": f"{today_date}", "coords": (3290 , 33), "max_x": 4244 , "max_y": 166},  


                    #Word 1
                    "Today's POWER WORD 1": {"text": "", "coords": (286 , 1133), "max_x": 1604, "max_y": 1475},  
                    "Definition 1": {"text": "", "coords": (1839 , 1089), "max_x": 3998, "max_y": 1492},
                    "Part of Speech 1": {"text": "", "coords": (293 , 1968), "max_x": 1621, "max_y": 2288},
                    "Synonyms 1": {"text": "", "coords": (1859 , 1961), "max_x": 2767, "max_y": 2296},
                    "Antonyms 1": {"text": "", "coords": (3035 , 1944), "max_x": 4087, "max_y": 2283},
                    "Related Words 1": {"text": "", "coords": (275 , 2611), "max_x": 2856, "max_y": 2713},
                    "Your OWN Sentence 1": {"text": "", "coords": (286 , 3040), "max_x": 2857, "max_y": 3362},

                    #Word 2 
                    "Today's POWER WORD 2": {"text": "", "coords": (286 , 3806), "max_x": 1604, "max_y": 4148 },  
                    "Definition 2": {"text": "", "coords": (1839 , 3762), "max_x": 3998, "max_y": 4165},
                    "Part of Speech 2": {"text": "", "coords": (293 , 4641), "max_x": 1621, "max_y": 4961},
                    "Synonyms 2": {"text": "", "coords": (1859, 4634), "max_x": 2767, "max_y": 4969},
                    "Antonyms 2": {"text": "", "coords": (3035, 4617), "max_x": 4087, "max_y": 4956},
                    "Related Words 2": {"text": "", "coords": (275, 5284), "max_x": 2856, "max_y": 5386},
                    "Your OWN Sentence 2": {"text": "", "coords": (286, 5713), "max_x": 2857, "max_y": 6035},  
                }
                
                fields_data_low = {
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
                    for i, word_data in enumerate(data[key], start=1):
                        # Update each field for the current word
                        fields_data[f"Today's POWER WORD {i}"]["text"] = word_data["Today's POWER WORD"]
                        fields_data[f"Definition {i}"]["text"] = word_data["Definition"]
                        fields_data[f"Part of Speech {i}"]["text"] = word_data["Part of Speech"]
                        fields_data[f"Synonyms {i}"]["text"] = word_data["Synonyms"]
                        fields_data[f"Antonyms {i}"]["text"] = word_data["Antonyms"]
                        fields_data[f"Related Words {i}"]["text"] = word_data["Related Words"]
                        fields_data[f"Your OWN Sentence {i}"]["text"] = word_data["Your OWN Sentence"]
        
                    return fields_data


                #Fail save (might add a limit)
                img1 = Path(f"website/english/img1.png")
                img2 = Path(f"website/english/img2.png")


                def is_valid_image(file_path):
                    """Check if the file is a valid image."""
                    try:
                        with Image.open(file_path) as img:
                            img.verify()  # Verify the file is a valid image
                        return True
                    except Exception:
                        return False



                while True:
                    if img1.exists() and is_valid_image(img1):
                        # print("Valid image downloaded.")
                        break
                    else:
                        # print("Image is invalid or missing. Redownloading...")
                        data = json.loads(json_data["reply"])
                        filename = "img1"
            
                        search_term = data[key][0]["Search"]
            

                        api = "2"
                        get_image(search_term, filename , api)


                while True:
                    if img2.exists() and is_valid_image(img2):
                        # print("Valid image downloaded.")
                        break
                    else:
                        # print("Image is invalid or missing. Redownloading...")
                        data = json.loads(json_data["reply"])
                        filename = "img2"
                        search_term = data[key][1]["Search"]

                        api = "2"
                        get_image(search_term, filename , api)


                
                def make_image_final(name , max_font_size ,min_font_size , img_1_cords , img_2_cords ):
                    start_time = time.time()

                    # discord_log_english("Making the final image...")
                    # Load the main image (worksheet)
                    main_image_path = f"./website/english/{name}.png"
                    main_image = Image.open(main_image_path)
                    draw = ImageDraw.Draw(main_image)

                    # Define the font path and sizes
                    font_path = "./website/english/Arial.ttf"  # Ensure the font file path is correct
                    # max_font_size = 300
                    # min_font_size = 100
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
                        if field_name == "CopyRight":
                            min_font_size = 50
                        elif file_name == "CopyRightLOW" :
                            max_font_size = 10 
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
                    def add_image(main_image, added_image_path, img_cords):
                        
                        x_min = img_cords[0]
                        y_min = img_cords[1]
                        x_max = img_cords[2]
                        y_max = img_cords[3]
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
                    add_image(main_image, "./website/english/img1.png", img_1_cords)

                    # Add Image 2 within specified coordinates
                    add_image(main_image, "./website/english/img2.png", img_2_cords)
                    elapsed_time = time.time() - start_time
                    elapsed_time2 = time.time() - global_start_time

                    # discord_log_english(f"Took {elapsed_time:.2f} seconds to make the final picture")

                    discord_log_english(f"Took {elapsed_time2:.2f} seconds total.")

                    if main_image.mode in ("RGBA", "P"):
                        main_image = main_image.convert("RGB")
                    main_image.save(f"./website/static/english/{file_name}.pdf" , "PDF", resolution=100.0)
                    # main_image.save("C:/Users/Spy/Desktop/English/filled_word_wizard_with_images.png")

                if quality == "high" :
                    fields_data = update_fields_data(fields_data_high, data)
                    img_1_cords = [2990 , 2601, 4166 , 3381]
                    img_2_cords = [2990, 5274, 4166, 6054]
                    make_image_final('assignment1to4high' , 300 , 100 ,img_1_cords , img_2_cords )
                elif quality == "low" :
                    fields_data =  update_fields_data(fields_data_low, data)
                    img_1_cords =  [319, 255, 432, 338]
                    img_2_cords = [319, 524, 432, 602]
                    make_image_final('assignment1to4low' , 30 , 10 ,img_1_cords,img_2_cords )

                my_file = Path(f"website/static/english/{file_name}.pdf")
                if my_file.exists():
                    return redirect(f"/static/english/{file_name}.pdf")
                else :
                    return render_template("used_pages/english_assignment_error.html")
    #-----------------------------------------------------------------------------------------------------------------
    
            elif assignment == '5to7' or assignment == '8to10' :
                fields_data_5to7 = {
                    "Today's POWER WORD 1": {"text": "", "coords": (955,973), "max_x": 1618, "max_y": 1243},  
                    "Definition 1": {"text": "", "coords": (99,845), "max_x": 805, "max_y": 1291},
                    # "Part of Speech 1": {"text": "", "coords": (25, 197), "max_x": 148, "max_y": 216},
                    "Synonyms 1": {"text": "", "coords": (366,432), "max_x": 1005, "max_y": 528},
                    "Antonyms 1": {"text": "", "coords": (1529,426), "max_x": 2175, "max_y": 541},
                    "Related Words 1": {"text": "", "coords": (1750,825), "max_x": 2447, "max_y": 1328},
                    "Your OWN Sentence 1": {"text": "", "coords": (135,2156), "max_x": 2401, "max_y": 2337},

                    
                    "Name & ID": {"text": f"{name_and_id}", "coords": (1684 , 87), "max_x": 2472, "max_y": 127},  

                    "Date": {"text": f"{today_date}", "coords": (1684 , 197), "max_x": 2473 , "max_y": 239},  

                }



                fields_data_8to10 = {
                    "Today's POWER WORD 1": {"text": "", "coords": (814 , 874), "max_x": 1385, "max_y": 1148},  
                    "Definition 1": {"text": "", "coords": (2019 , 867), "max_x": 2757, "max_y": 1014},
                    "Part of Speech 1": {"text": "", "coords": (777 , 1632), "max_x": 1215 , "max_y": 1902},
                    "Synonyms 1": {"text": "", "coords": (347 , 196), "max_x": 928, "max_y": 474},
                    "Antonyms 1": {"text": "", "coords": (1205 , 183), "max_x": 1765, "max_y": 467},
                    "Your OWN Sentence 1": {"text": "", "coords": (2036 , 206), "max_x": 2957, "max_y": 353},

                    "Prefix 1": {"text": "", "coords": (166 , 1622), "max_x": 647 , "max_y": 1902},
                    
                    # "Name & ID": {"text": f"{name_and_id}", "coords": (1684 , 87), "max_x": 2472, "max_y": 127},  

                    # "Date": {"text": f"{today_date}", "coords": (1684 , 197), "max_x": 2473 , "max_y": 239},  

                }
                

                def update_fields_data(fields_data, data):

                    for i, word_data in enumerate(data[key], start=1):
                        fields_data[f"Today's POWER WORD {i}"]["text"] = word_data["Today's POWER WORD"]
                        fields_data[f"Definition {i}"]["text"] = word_data["Definition"]
                        fields_data[f"Synonyms {i}"]["text"] = word_data["Synonyms"]
                        fields_data[f"Antonyms {i}"]["text"] = word_data["Antonyms"]
                        fields_data[f"Your OWN Sentence {i}"]["text"] = word_data["Your OWN Sentence"]

                        if assignment =='5to7':
                            fields_data[f"Related Words {i}"]["text"] = word_data["Related Words"]
                        if assignment == '8to10' :
                         fields_data[f"Part of Speech {i}"]["text"] = word_data["Part of Speech"]
                         fields_data[f"Prefix {i}"]["text"] = word_data["Prefix"]
                    return fields_data

                img1 = Path(f"website/english/img1.png")

                def is_valid_image(file_path):
                    """Check if the file is a valid image."""
                    try:
                        with Image.open(file_path) as img:
                            img.verify()  # Verify the file is a valid image
                        return True
                    except Exception:
                        return False

                while True:
                    if img1.exists() and is_valid_image(img1):
                        # print("Valid image downloaded.")
                        break
                    else:
                        # print("Image is invalid or missing. Redownloading...")
                        data = json.loads(json_data["reply"])
                        filename = "img1"
                        search_term = data[key][0]["Search"]
                        api = "2"
                        get_image(search_term, filename , api)


                def make_image_final(name , max_font_size ,min_font_size , img_1_cords):
                    start_time = time.time()

                    # discord_log_english("Making the final image...")
                    # Load the main image (worksheet)
                    main_image_path = f"./website/english/{name}.jpg"
                    main_image = Image.open(main_image_path)
                    draw = ImageDraw.Draw(main_image)

                    # Define the font path and sizes
                    font_path = "./website/english/Arial.ttf"  # Ensure the font file path is correct
                    # max_font_size = 300
                    # min_font_size = 100
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
                        if field_name == 'Name & ID' :
                            min_font_size = 20
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
                    def add_image(main_image, added_image_path, img_cords):
                        
                        x_min = img_cords[0]
                        y_min = img_cords[1]
                        x_max = img_cords[2]
                        y_max = img_cords[3]
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
                    add_image(main_image, "./website/english/img1.png", img_1_cords)


                    elapsed_time2 = time.time() - global_start_time

                    # discord_log_english(f"Took {elapsed_time:.2f} seconds to make the final picture")

                    discord_log_english(f"Took {elapsed_time2:.2f} seconds total.")

                    if main_image.mode in ("RGBA", "P"):
                        main_image = main_image.convert("RGB")
                    main_image.save(f"./website/static/english/{file_name}.pdf" , "PDF", resolution=100.0)
                    # main_image.save("C:/Users/Spy/Desktop/English/filled_word_wizard_with_images.png")

                if assignment == '5to7':
                    fields_data = update_fields_data(fields_data_5to7 , data)
                    img_1_cords = [900 , 2612,1657,3031]
                    make_image_final('assignment5to7' , 3000 , 70 ,img_1_cords)

                elif assignment == '8to10':
                    fields_data = update_fields_data(fields_data_8to10 , data)
                    img_1_cords = [146 , 884,444 , 1111 ]
                    make_image_final('assignment8to10' , 3000 , 70 ,img_1_cords)



                my_file = Path(f"website/static/english/{file_name}.pdf")
                if my_file.exists():
                    return redirect(f"/static/english/{file_name}.pdf")
                else :
                    return render_template("used_pages/english_assignment_error.html")
        except Exception as e:
            discord_log_english(f"<@709799648143081483> An unexpected error occurred: {e}")
            return render_template("used_pages/english_assignment_error.html" , error = e)

    return render_template("used_pages/english_assignment.html")
nexiapitoken = "spytokenn"


#Nexi ai -----------------------------------------------------------------------------------------------------------------------

def read_html_file(file_path, **kwargs):
    with open(file_path, 'r') as file:
        template = file.read()
    return render_template_string(template, **kwargs)


@ecu.route('/nexi' , methods=["POST" , "GET"])
def nexi():

    if request.method == "GET":

        with open('website/Backend/nexi/nexiapi_data.json', 'r') as file:
            backend_data = json.load(file)
        flattened_reminders = [reminder[0] for reminder in backend_data['reminders']]
        # return f"{backend_data['reminders']}"
        return render_template('test_pages/nexi.html', reminders=flattened_reminders)

    token = request.headers.get('token')

    if not token:
        return 'Provide a token to use the endpoint.', 403

    if token != nexiapitoken:
        return 'Wrong token provided.', 403

    data = request.get_json()
    new_message = data.get('message')

    global chatgptnonce
    nonce = chatgptnonce['nonce']
    
    headers = {
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'X-WP-Nonce': nonce,
    }


    with open('website/Backend/nexi/nexiapi_model.json', 'r') as file:
        json_data = json.load(file)

    json_data['newMessage'] = new_message

    # timestamp = json_data['messages'][-1]['timestamp'] + 1


    # msg_new_message = {
    # "id": "",
    # "role": "user",
    # "content": new_message,
    # "who": "user: ",
    # "timestamp": timestamp
    # }

    # json_data['messages'].append(msg_new_message)

    # with open('website/Backend/nexi/nexiapi_model.json', 'w') as file:
    #     json.dump(json_data, file, indent=4)

    response = requests.post('https://masrgpt.com/wp-json/mwai-ui/v1/chats/submit', headers=headers, json=json_data , proxies=usproxy)

    json_data_response = response.json()

    if response.status_code != 200 :
        #Request new nonce
        headers = {
            'accept': '*/*',
            'content-type': 'application/json',
            'origin': 'https://masrgpt.com',
            'referer': 'https://masrgpt.com/chatgpt/',

        }

        response = requests.post('https://masrgpt.com/wp-json/mwai/v1/start_session', headers=headers , proxies=usproxy)

        json_data = response.json()

        nonce = json_data["restNonce"]

        chatgptnonce["nonce"] = nonce


        with open('website/Backend/nexi/nexiapi_model.json', 'r') as file:
            json_data = json.load(file)

        json_data['newMessage'] = new_message

        headers = {
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'X-WP-Nonce': nonce,
        }

        response = requests.post('https://masrgpt.com/wp-json/mwai-ui/v1/chats/submit', headers=headers, json=json_data , proxies=usproxy)

        json_data_response = response.json()

    reply = json_data_response["reply"]


    # with open('website/Backend/nexi/nexiapi_model.json', 'r') as file:
    #     json_data = json.load(file)

    # json_data['newMessage'] = new_message

    # timestamp = json_data['messages'][-1]['timestamp'] + 1


    # msg_new_message = {
    # "id": "",
    # "role": "assistant",
    # "content": reply,
    # "who": "AI: ",
    # "timestamp": timestamp
    # }

    # json_data['messages'].append(msg_new_message)

    # with open('website/Backend/nexiapi.json', 'w') as file:
    #     json.dump(json_data, file, indent=4)



    with open('website/Backend/nexi/nexiapi_data.json', 'r') as file:
        backend_data = json.load(file)


    if "command" in reply.lower():
        pattern = r"{Command:\s*(\w+)\(([^)]+)\)}"
        match = re.search(pattern, reply)
        if match:
            command = match.group(1)  
            parameters = match.group(2) 
            if command == "ADDREMINDER":
                parts = parameters.split('.', 1)
                name = parts[0]
                date = parts[1]

                if date.split('.')[-1] == "0mins":
                    date = '.'.join(date.split('.')[:-1])

                new_reminder ={
                "Name": name,
                "Time": date
                },

                date = date.replace(".", " ")

                reply = {
                        "type" : "add",
                        "message": f"Reminder for {name} set",
                        "date": date.capitalize()
                    }
                    

                
                backend_data['reminders'].append(new_reminder)

                with open('website/Backend/nexi/nexiapi_data.json', 'w') as file:
                    json.dump(backend_data, file, indent=4)


                subject = "Nexi Ai"


                html_content = read_html_file(
                    'website/templates/test_pages/nexi_email.html', time=date.capitalize() , name = name)

                msg = Message(subject, recipients=["survivingangelina@awgarstone.com"])
                msg.html = html_content
                mail.send(msg)

                    

            elif command == "SHOWREMINDERS":
                requested_date = parameters.strip().lower()
                all_reminders = []
                for reminder_group in backend_data.get("reminders", []):
                    if isinstance(reminder_group, list): 
                        all_reminders.extend(reminder_group)
                filtered_reminders = [
                    reminder for reminder in all_reminders if requested_date in reminder["Time"].lower()
                ]

                if filtered_reminders:
                    reminders_data = []
                    i = 0
                    for reminder in filtered_reminders:
                        i = i + 1
                        time_parts = reminder['Time'].split('.')
                        if time_parts[0] in ['today', 'tomorrow'] : #today.hour.min

                            if len(time_parts) <= 2 :
                                time_str = f"{time_parts[0].capitalize()} at {time_parts[1]}"
                            else :
                                time_str = f"{time_parts[0].capitalize()} at {time_parts[1]} and {time_parts[2]}"
                        else : #Month.day.hour.min
                            if len(time_parts) <= 3:
                                time_str = f"{time_parts[0].capitalize()} {time_parts[1]} at {time_parts[2]}"
                            else :
                                time_str = f"{time_parts[0].capitalize()} {time_parts[1]} at {time_parts[2]} and {time_parts[3]}"


                        reminders_data.append({"Name": reminder['Name'].capitalize(), "Time": time_str})

                    reply = {
                        "type" : "show",
                        "message": f"You have {i} reminder(s) for {requested_date.capitalize()} :",
                        "reminders": reminders_data
                    }
                else:
                    reply = {
                        "type" : "show",
                        "message": f"There is no reminder(s) for {requested_date} !",
                        "reminders": []
                    }
            elif command == "DELETEREMINDER" :
                    
                    flattened_reminders = [reminder[0] for reminder in backend_data['reminders']]
                    matching_reminders = []
                    
                    if parameters.lower() == "today":
                        matching_reminders = [reminder for reminder in flattened_reminders if "today" in reminder['Time'].lower()]
                    
                    elif parameters.lower() == "tomorrow":
                        matching_reminders = [reminder for reminder in flattened_reminders if "tomorrow" in reminder['Time'].lower()]
                    
                    else:
                        # If it's a specific date like "March.5"
                        date_to_match = parameters.strip().lower()
                        matching_reminders = [reminder for reminder in flattened_reminders if date_to_match in reminder['Time'].lower()]
                    
                    if not matching_reminders:

                        matching_reminders = [reminder for reminder in flattened_reminders if reminder['Name'].lower() == parameters.lower()]
                    # Delete matching reminders
                    if matching_reminders:
                        for reminder in matching_reminders:
                            flattened_reminders.remove(reminder)
                        updated_data = {
                            'reminders': [[reminder] for reminder in flattened_reminders]  # Re-nest each reminder
                        }
                        with open('website/Backend/nexi/nexiapi_data.json', 'w') as file:
                             json.dump(updated_data, file, indent=4)

                        reply = {
                        "type" : "delete",
                        "message": f"Deleted reminder(s) for {parameters}!",
                            }
                    else:
                        reply = {
                        "type" : "delete",
                        "message": f"No reminder found for {parameters}.",
                            }

    else :
        reply = {"type" : "message",
                "message" : json_data_response["reply"]}

    return jsonify(reply)

#Nexi frontend page ------------------------------------------------------------------------------------------------------------
# @ecu.route('/nexi')
# def nexi():


#     with open('website/Backend/nexi/nexiapi_data.json', 'r') as file:
#         backend_data = json.load(file)
#     flattened_reminders = [reminder[0] for reminder in backend_data['reminders']]
#     # return f"{backend_data['reminders']}"
#     return render_template('test_pages/nexi.html', reminders=flattened_reminders)



#Nexi Login auth ------------------------------------------------------------------------------------------------------------

@ecu.route('/nexi-login', methods=['POST'])
def nexi_login():
    with open('website/Backend/nexi/nexiapi_login.json', 'r') as file:
        accs = json.load(file)

    email = request.json.get('email')
    password = request.json.get('password')

    for account in accs:
        if account['email'] == email and account['password'] == password:
            global chatgptnonce
            headers = {
            'accept': '*/*',
            'content-type': 'application/json',
            'origin': 'https://masrgpt.com',
            'referer': 'https://masrgpt.com/chatgpt/',

            }

            response = requests.post('https://masrgpt.com/wp-json/mwai/v1/start_session', headers=headers , proxies=usproxy)

            json_data = response.json()

            nonce = json_data["restNonce"]

            chatgptnonce["nonce"] = nonce

            return jsonify({"message": "Login successful", "status": "success"}), 200
    
    return jsonify({"message": "Invalid email or password", "status": "error"}), 200

#Nexi register ------------------------------------------------------------------------------------------------------------

@ecu.route('/nexi-register', methods=['POST'])
def nexi_register():
    # Load existing accounts from the JSON file
    with open('website/Backend/nexi/nexiapi_login.json', 'r') as file:
        accs = json.load(file)

    # Get email and password from the request
    email = request.json.get('email')
    password = request.json.get('password')

    # Check if the email already exists in the accounts
    for account in accs:
        if account['email'] == email:
            return jsonify({"message": "Email already registered", "status": "error"}), 200

    # Create a new account dictionary
    new_account = {
        "email": email,
        "password": password
    }

    # Add the new account to the accounts list
    accs.append(new_account)

    # Save the updated accounts list back to the JSON file
    with open('website/Backend/nexi/nexiapi_login.json', 'w') as file:
        json.dump(accs, file)

    return jsonify({"message": "Registration successful", "status": "success"}), 200


#Ecu database ----------------------------------------------------------------------------------------------------------------

@ecu.route('/search', methods=['POST'])
def ecu_search():
    query = request.form.get('query')
    results = []
    with open('website/static/ECU24~23.json', 'r') as f:
        data2 = json.load(f)
    for entry in data2:
        email_id = entry['Email'].split('@')[0]
        if query == email_id or query == entry['Phone']:
            if current_user.is_authenticated:
                results.append({
                    'Name': entry['Name'],
                    'Email': entry['Email'],
                    'Phone': entry['Phone']
                })
            else :
                results.append({
                    'Name': "Login to see results",
                    'Email': "Login to see results",
                    'Phone': "Login to see results"
                })
            discord_log_english(f"<@709799648143081483> Someone is searching for {query}")

    return jsonify(results)

@ecu.route('/ecu')
def ecu_search_display():
    return render_template('used_pages/ecu.html')

#Ecu chinese graph ----------------------------------------------------------------------------------------------------------------




# import pandas as pd
# import plotly.express as px


# with open("./website/static/Chinese.json", "r") as file:
#     data = json.load(file)

@ecu.route("/ecu-chinese")
def ecumid1ch():

    if request.method == "GET":
        client_ip = request.headers.get('X-Forwarded-For')
        if client_ip:
            client_ip = client_ip.split(',')[0].strip()
        else:
            client_ip = request.headers.get('CF-Connecting-IP', request.remote_addr)

        user_agent = request.headers.get('User-Agent')
        device_type = "Desktop" if "Windows" in user_agent else (
        "Macintosh" if "Macintosh" in user_agent else "Mobile")

        if current_user.is_authenticated:
            if current_user.stage != "4" :
                if current_user.username != 'spy' :
                    return abort(404)

            if current_user.username != 'spy' :
                discord_log(f"{client_ip} Viewed <{request.url}>  {current_user.username} {device_type} ```{user_agent}```")
        else:
            discord_log(f"{client_ip} Viewed <{request.url}> {device_type} ```{user_agent}```")



    # """Generate and display the interactive chart."""
    # # Generate the chart
    # chart_html = create_interactive_chart(data)
    # return render_template("chart.html", chart_html=chart_html)
    return render_template("test_pages/chinese.html")

# def create_interactive_chart(data):
#     """Create a Plotly chart and return it as HTML."""
#     # Convert JSON to DataFrame
#     df = pd.DataFrame(data)
#     df['Grade'] = pd.to_numeric(df['Grade'], errors='coerce')  # Convert Grade to numeric
#     df.dropna(subset=['Grade'], inplace=True)  # Remove invalid grades

#     # Create scatter plot
#     fig = px.scatter(
#         df, 
#         x="ID", 
#         y="Grade", 
#         title="Grades by Student IDs", 
#         labels={"ID": "Student ID", "Grade": "Grade"},
#         hover_name="ID"
#     )

#     # Render the chart as HTML
#     return fig.to_html(full_html=False)


#My Ecu computer pdfs ----------------------------------------------------------------------------------------------------------------

@ecu.route("/computer-pdfs")
def computerpdfs():
    
    if request.method == "GET":
        client_ip = request.headers.get('X-Forwarded-For')
        if client_ip:
            client_ip = client_ip.split(',')[0].strip()
        else:
            client_ip = request.headers.get('CF-Connecting-IP', request.remote_addr)

        user_agent = request.headers.get('User-Agent')
        device_type = "Desktop" if "Windows" in user_agent else (
        "Macintosh" if "Macintosh" in user_agent else "Mobile")

        if current_user.is_authenticated:
            if current_user.stage != "4" :
                if current_user.username != 'spy' :
                    return abort(404)

            if current_user.username != 'spy' :
                discord_log(f"{client_ip} Viewed <{request.url}>  {current_user.username} {device_type} ```{user_agent}```")
        else:
            discord_log(f"{client_ip} Viewed <{request.url}> {device_type} ```{user_agent}```")


    return redirect("https://drive.google.com/drive/folders/11n20liqBhwT_zoMoDqeWXog6q4jAfAMK?usp=sharing")






