import os , sys , threading
from flask import Flask, render_template, request, redirect, url_for , Blueprint , flash ,  send_file
import requests
from pytube import Playlist
import youtube_dl
import requests
import os
from flask_login import login_required
from lxml import html



shortlinks = Blueprint('shortlinks', __name__)

#Link shortner -------------------------------------------------------------------------

def delete_lines_after_target_line(file_path, target_line, number):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        for i, line in enumerate(lines):
            if line.strip() == target_line:
                del lines[i:i + number]
                break
        with open(file_path, 'w') as file:
            file.writelines(lines)

        print(f"Deleted {number} lines after '{target_line}' from {file_path}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def restart_server_with_delay(restart_script_path):
    def restart_server():
        os.execl(sys.executable, sys.executable, restart_script_path, *sys.argv[1:])
    restart_thread=threading.Thread(target=lambda:threading.Timer(2,restart_server).start())
    restart_thread.start()
#----------------------------------------------------------------------------------------
def append_text_to_filepy(text_to_append, text2):
    try:
        with open("website/shortlinks.py", 'a') as file:
            file.write(f"""
@shortlinks.route("/{text_to_append}")
def {text_to_append}():
    return redirect("{text2}") 
            """+ "\n")
            print("New url added")
    except FileNotFoundError:
        print("File not found: shortlinks.py")
    except Exception as e:
        print(f"An error occurred: {str(e)}")




def append_text_to_file(text_to_append, text2):
    try:
        with open("links.txt", 'a') as file2 :
            file2.write(text_to_append + "\n")
            print("New url added")
    except FileNotFoundError:
        print("File not found: links.txt")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
#----------------------------------------------------------------------------------------
def search_word_in_file(target_word):
    try:
        with open("links.txt", 'r') as file:
            lines = file.readlines()
            for line in lines:
                if target_word in line:
                    return True
        return False
    except FileNotFoundError:
        print("File not found")
        return False
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False
#-------------------------------------------------------------------------------------
@shortlinks.route("/delete")
def delete():
    with open('website/links.txt', 'r') as file:
      lines = file.readlines()
    item_id = request.args.get('id')
    target_line = f"""@shortlinks.route("/{item_id}")"""
    delete_lines_after_target_line("website/shortlinks.py", target_line, 3)
    delete_lines_after_target_line("links.txt", item_id, 1)
    restart_server_with_delay("main.py")
    return render_template("teacher.html",alert= "true" , lines=lines, teachername="All")



@shortlinks.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        input1 = request.form['input1']
        input2 = request.form['input2']
        checkbox = request.form.getlist('check') 
        found = search_word_in_file(input1)
      
        if not found:
          if 'edit' in checkbox:
              print(checkbox)
              append_text_to_file(input1, input2)
              append_text_to_filepy(input1, input2)
              restart_server_with_delay("main.py")
          else:
            append_text_to_filepy(input1, input2)
            restart_server_with_delay("main.py")
          
        else:
            return redirect(url_for("views.home"))
    return redirect(url_for("shortlinks.shlinks", input1=input1))


#------------------------------------------------------------------------------------------------------


@shortlinks.route('/yourlink')
def shlinks():
        input1 = request.args.get('input1')
        return render_template("index.html", done_message = "done" , input1 = input1) 


@shortlinks.route("/links")
def links():
    return render_template("index.html",links= "yes" )


    

@shortlinks.route("/books")
def books():
    return redirect("https://drive.google.com/drive/u/0/folders/1HJRe2ejazmPYWGDojfViz-3izr-tQ26k") 
              
@shortlinks.route("/tools2")
def tools2():
    return redirect("https://drive.google.com/file/d/1to3ZxSfFDN3F0VZMkNjznGXZJaGthiO-/view?usp=drive_link")   
  
@shortlinks.route("/tools")
def tools():
    return redirect("https://img.guildedcdn.com/ContentMediaGenericFiles/24e7000cfbd9e65c52566c6a6b868332-Full.zip")         

@shortlinks.route("/table")
def table():
    return redirect("https://periodic-table.tech/") 
            

@shortlinks.route("/sherbopdfs")
def sherbopdfs():
    return redirect("https://drive.google.com/drive/folders/1cEnVqh8bAFr4aqHgMdy-_TpfbEVXC0zc?usp=share_link") 
            

            

@shortlinks.route("/nawarpdfs")
def nawarpdfs():
    return redirect("https://drive.google.com/drive/folders/1co0YX7h8Xdg3HV4zFhf2xze9yNX-xM71?usp=drive_link") 
            

            

            

@shortlinks.route("/cars")
def cars():
    return redirect("https://link.storjshare.io/s/jusqtijcg4gfmzpxdhkynz4xwl4q/judee%2FCopy%20of%20Cars%20(2006)%20Full%20Arabic%201080p%20.ahmadalsheikhly.com.mp4") 
            



            
# def get_links(teacher_dict):
#   links_list = []

#   def get_href_from_xpath(html_content, xpath):
#       root = html.fromstring(html_content)
#       elements = root.xpath(xpath)
#       if elements:
#           return elements[0].get('href')
#       return None

#   for teacher, url in teacher_dict.items():
#       response = requests.get(url)

#       if response.status_code == 200:
#           html_content = response.text
#           xpath = "/html/body/ul[2]/a"          
#           href_value = get_href_from_xpath(html_content, xpath)

#           if href_value:
#               playlist_link = f"{href_value}"
#               links_list.append(playlist_link)
#              # print(f"Checked videos from {url}")
#           else:
#               # print(f"Failed to find href value in {url}")
#               break

#   return links_list

# xpath_template = "/html/body/ul/li[{}]"

# # Function to scrape and store href in a dictionary until an error occurs
# def scrape_website(url):
#   spylinks = {}
#   try:
#       index = 1
#       while True:
#           xpath = xpath_template.format(index)
#           response = requests.get(url)
#           response.raise_for_status()  # Raise an HTTPError for bad requests
#           tree = html.fromstring(response.content)
#           href = tree.xpath(xpath + "/a/@href")

#           if not href:
#               break

#           spylinks[f"Teacher {index}"] = href[0]
#           index += 1
#   except requests.exceptions.HTTPError as e:
#       print(f"HTTP error: {e}")
#   except Exception as e:
#       print(f"An error occurred: {e}")

#   return spylinks



# def get_playlist_items(playlist_url):
#     ydl_opts = {
#         'quiet': True,
#         'extract_flat': True,
#     }

#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         result = ydl.extract_info(playlist_url, download=False)
#         return result.get('entries', [])

# def get_playlist_name(playlist_url):
#     ydl_opts = {
#         'quiet': True,
#         'extract_flat': True,
#     }

#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         result = ydl.extract_info(playlist_url, download=False)
#         return result.get('title')

# def save_items_to_dict(playlist_name, items):
#     titles_dict = {'playlist_name': playlist_name, 'titles': [{'title': item['title'], 'url': item['url']} for item in items]}
#     return titles_dict

# def count_videos_in_playlist(items):
#     return len(items)

# def count_total_videos(combined_dict):
#     total_videos = 0
#     for playlist_data in combined_dict.values():
#         total_videos += count_videos_in_playlist(playlist_data['titles'])
#     return total_videos

# def items(playlist_links):
#     combined_dict = {}

#     for playlist_link in playlist_links:
#         items = get_playlist_items(playlist_link)

#         if items:
#             playlist_name = get_playlist_name(playlist_link)
#             playlist_dict = save_items_to_dict(playlist_name, items)
#             combined_dict[playlist_link] = playlist_dict

#     total_videos = count_total_videos(combined_dict)
#     return combined_dict, total_videos

# def get_links_and_items(teacher):
#     linkspy = get_links(scrape_website(f"https://spysnet.com/{teacher}"))
#     result_links = linkspy
#     final = items(result_links)
#     return final
@shortlinks.route("/list/<teacher>")
def list(teacher):
    return "Out of Service"

@shortlinks.route("/update")
def update():
    return "Out of Service"

# @shortlinks.route("/list/<teacher>")
# def list(teacher):
#     html_filename = f"{teacher}_list.html"
#     templates_folder = os.path.join(os.getcwd(), "website/templates/list")
#     html_filepath = os.path.join(templates_folder, html_filename)

#     return send_file(html_filepath)

# @shortlinks.route("/update")
# @login_required
# def update():
#     teacher = request.args.get("teacher")

#     if not teacher:
#         return "Error: 'teacher' parameter is required for update."

#     final, total_videos = get_links_and_items(teacher)  # Unpack the tuple
#     html_filename = f"{teacher}_list.html"
#     templates_folder = os.path.join(os.getcwd(), "website/templates/list")
#     html_filepath = os.path.join(templates_folder, html_filename)

#     with open(html_filepath, 'w') as file:
#         file.write(render_template("list.html", final=final, total_videos=total_videos, teacher=teacher))

#     return f'HTML file for {teacher} has been updated. <a href="https://spysnet.com/list/{teacher}">Teacher List</a>'






@shortlinks.route("/main")
def main():
    return redirect("https://cdn.discordapp.com/attachments/1154501683427156048/1172494252660494376/main.py?ex=6560855d&is=654e105d&hm=02f55ad84a970c8ff473bb1bc0b9ec06d8c50952ffa2748e312393cebc31b349&") 
            

            

            

            
