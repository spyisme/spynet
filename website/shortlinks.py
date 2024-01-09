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
        return render_template("used_pages/index.html", done_message = "done" , input1 = input1) 

@shortlinks.route("/links")
def links():
    return render_template("used_pages/index.html",links= "yes" )

@shortlinks.route("/books")
def books():
    return redirect("https://drive.google.com/drive/folders/12OIgF6ceqUP6yxHdaX22fpQfGWvB-5e8?usp=sharing") 
              
@shortlinks.route("/tools2")
def tools2():
    return redirect("https://drive.google.com/file/d/1to3ZxSfFDN3F0VZMkNjznGXZJaGthiO-/view?usp=drive_link")   
  
@shortlinks.route("/tools")
def tools():
    return redirect("https://cdn.gilcdn.com/ContentMediaGenericFiles/dfb6c51f966eedb2d3af259a31390e49-Full.zip")         

@shortlinks.route("/table")
def table():
    return redirect("https://periodic-table.tech/") 
            
@shortlinks.route("/sherbopdfs")
def sherbopdfs():
    return redirect("https://drive.google.com/drive/folders/1cEnVqh8bAFr4aqHgMdy-_TpfbEVXC0zc?usp=share_link") 
            

@shortlinks.route("/nawarpdfs")
def nawarpdfs():
    return redirect("https://drive.google.com/drive/folders/1co0YX7h8Xdg3HV4zFhf2xze9yNX-xM71?usp=drive_link") 
                 
@shortlinks.route("/chempdfs")
def chempdfs():
    return redirect("https://drive.google.com/drive/folders/1trBpK01IknkeMC9LtsCM7dyTz-9uqY0n?usp=drive_link") 


@shortlinks.route("/main")
def main():
    return redirect("https://cdn.discordapp.com/attachments/1154501683427156048/1172494252660494376/main.py?ex=6560855d&is=654e105d&hm=02f55ad84a970c8ff473bb1bc0b9ec06d8c50952ffa2748e312393cebc31b349&") 
            

@shortlinks.route("/files")
def files():
    return redirect("https://link.storjshare.io/s/jubit7purhfmiw6zi7mysb2jr4wq/spynet%2FPrivate") 
            

@shortlinks.route("/vdo")
def vdo():
    return redirect("https://cdn.discordapp.com/attachments/1192117992457257074/1192542902732210227/code.txt?ex=65a97520&is=65970020&hm=c9d5464d7b29242438c9a227cee9bddb4a5609f4df98a2b6a38c750406f7bdb4&") 
            
