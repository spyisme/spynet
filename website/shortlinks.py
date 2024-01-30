import os , sys , threading
from flask import Flask, render_template, request, redirect, url_for , Blueprint , flash
import requests
from pytube import Playlist
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
def append_text_to_file(file_path, text_to_append, text2):
    try:
        with open(file_path, 'a') as file , open("links.txt", 'a') as file2:
            file.write(f"""
@shortlinks.route("/{text_to_append}")
def {text_to_append}():
    return redirect("{text2}") 
            """+ "\n")
            file2.write(text_to_append + "\n")
            print("New url added")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
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
    item_id = request.args.get('id')
    target_line = f"""@shortlinks.route("/{item_id}")"""
    delete_lines_after_target_line("website/shortlinks.py", target_line, 3)
    delete_lines_after_target_line("links.txt", item_id, 1)
    restart_server_with_delay("main.py")
    return redirect("https://spysnet.com/all")



@shortlinks.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        input1 = request.form['input1']
        input2 = request.form['input2']
        found = search_word_in_file(input1)
      
        if not found:
            append_text_to_file("website/shortlinks.py", input1, input2)
            restart_server_with_delay("main.py")
          
        else:
            return redirect(url_for("shortlinks.display_links"))
    return redirect(url_for("shortlinks.shlinks", input1=input1))


#------------------------------------------------------------------------------------------------------
@shortlinks.route('/all')
def display_links():
    with open('links.txt', 'r') as file:
        lines = file.readlines()

    return render_template('teacher.html', lines=lines, teachername="All")

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
              

@shortlinks.route("/tools")
def tools():
    return redirect("https://drive.google.com/file/d/1to3ZxSfFDN3F0VZMkNjznGXZJaGthiO-/view?usp=drive_link")         

@shortlinks.route("/table")
def table():
    return redirect("https://periodic-table.tech/") 
            

@shortlinks.route("/sherbopdfs")
def sherbopdfs():
    return redirect("https://drive.google.com/drive/folders/1cEnVqh8bAFr4aqHgMdy-_TpfbEVXC0zc?usp=share_link") 
            

            

            
