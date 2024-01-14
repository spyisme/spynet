from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from googleapiclient.discovery import build
import random
import json
import requests
from flask_login import login_user, logout_user, login_required
from .models import User
from werkzeug.security import check_password_hash , generate_password_hash
from . import db
from functools import lru_cache
import subprocess

views = Blueprint('views', __name__)
print('Running!')






@views.route('/restart')
def restart():
    try:
        # Change the path to your restart.bat file
        bat_file_path = r"C:\Users\Spy\Downloads\Restart.bat"
        
        # Run the restart.bat file using subprocess
        subprocess.run([bat_file_path], shell=True, check=True)
        
        return 'Restart command executed successfully!'
    
    except subprocess.CalledProcessError as e:
        return f'Error executing restart command: {e}', 500


@views.route('/update')
def update():
    try:
        # Change the path to your restart.bat file
        bat_file_path = r"C:\Users\Spy\Downloads\Updateonly.bat"
        
        # Run the restart.bat file using subprocess
        subprocess.run([bat_file_path], shell=True, check=True)
        
        return 'Restart command executed successfully!'
    
    except subprocess.CalledProcessError as e:
        return f'Error executing restart command: {e}', 500


@views.route('/push')
def push():
    try:
        # Change the path to your restart.bat file
        bat_file_path = r"C:\Users\Spy\Downloads\Push.bat"
        
        # Run the restart.bat file using subprocess
        subprocess.run([bat_file_path], shell=True, check=True)
        
        return 'Restart command executed successfully!'
    
    except subprocess.CalledProcessError as e:
        return f'Error executing restart command: {e}', 500







@views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember')  # Assuming you have a checkbox named 'remember' in your login form

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user, remember=remember == 'on')  # Convert the string 'on' to boolean
            flash('Login successful!', category='success')
            return redirect(url_for('views.home'))

        else:
            flash('Login unsuccessful. Please check your username and password.', category='error')

    return render_template('test_pages/login.html')


# @views.route('/logout')
# @login_required
# def logout():
#   logout_user()
#   return redirect(url_for('views.home'))



# @views.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         hashed_password = generate_password_hash(password, method='scrypt')

#         new_user = User(username=username, password=hashed_password)
#         db.session.add(new_user)
#         db.session.commit()

#         flash('Account created successfully!', category='success')
#         return redirect(url_for('views.home'))

#     return render_template('test_pages/register.html')

YOUTUBE_API_KEY = 'AIzaSyAbrVMIzmLLhHQSrMVUG8gS3d6IAYE0qVc'


def convert_duration(duration):
    duration = duration[2:]  # Remove 'PT' at the beginning
    hours, minutes, seconds = 0, 0, 0

    if 'H' in duration:
        hours = int(duration.split('H')[0])
        duration = duration.split('H')[1]

    if 'M' in duration:
        minutes = int(duration.split('M')[0])
        duration = duration.split('M')[1]

    if 'S' in duration:
        seconds = int(duration.split('S')[0])

    formatted_duration = '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
    return formatted_duration


def get_playlist_videos(playlist_id):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY, static_discovery=False)

    # Fetch the playlist items
    playlist_items = []
    next_page_token = None

    while True:
        playlist_request = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=50,  # Adjust as needed
            pageToken=next_page_token
        )
        playlist_response = playlist_request.execute()

        playlist_items.extend(playlist_response['items'])
        next_page_token = playlist_response.get('nextPageToken')

        if not next_page_token:
            break

    videos = []

    for index, item in enumerate(playlist_items):
        video_id = item['snippet']['resourceId']['videoId']

        # Get video details to retrieve the duration
        video_request = youtube.videos().list(
            part='contentDetails',
            id=video_id
        )
        video_response = video_request.execute()
        try :
          video_duration = video_response['items'][0]['contentDetails']['duration']
        except IndexError:
          video_duration = "N/a"
        formatted_duration = convert_duration(video_duration)
        video_title = item['snippet']['title']

        videos.append({
            'id': video_id,
            'title': video_title,
            'duration': formatted_duration,
            'jsid': index + 1
        })

    return videos






@views.route('/all')
def display_links():
    return redirect("/") 





@views.route("/")
def home():
    lines = ["physics", "chemistry","math", "arabic","geology", "biology","english" , "german"]
    return render_template('used_pages/all.html', lines=lines, teachername="All")

@views.route('/favicon.ico')
def favicon():
    return redirect("/static/favicon.ico") 


@views.route('/testt')
def testtt():
    return render_template('test.html')



@views.route('/watch')
def watwatchch():
    vidoid = request.args.get('id')
    return render_template('used_pages/videoplayeryt.html',videoid=vidoid)


#Physics --------------------------------------------------------------------------------------------------------------------------
@views.route('/physics')
def Physics():
  teacher_links = {
  "Nawar": ("/nawar", "Nawar"),
  }
  teachername = "Physics"
  return render_template('used_pages/teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")
@views.route('/nawar')
def nawar():
  teacher_links = {
  "Nawar Chapter 1": ("/nawarch1", "Chapter 1"),
    "Nawar Chapter 1 Revision": ("nawarch1rev", "Revision 1"),
    "Nawar Chapter 2": ("nawarch2", "Chapter 2"),
    "Nawar Chapter 2 Revision": ("nawarch2rev", "Revision 2"),
    "Nawar Chapter 3": ("nawarch3", "Chapter 3"),
    "Nawar Files": ("nawarpdfs", "Google Drive")
  }
  teachername = "Physics"
  return render_template('used_pages/teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")
@views.route("/nawarch1")
def nawarch1():
  teachername = "Chapter 1"
  playlist_id = 'PLM-GVlebsoPXpGe3wzMN7SKYvmTr0jACa'
  with open("website/templates/teachers/nawarch1.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/nawarch1update")
def nawarch1update():
    return createtxtfile("nawarch1" , "PLM-GVlebsoPXpGe3wzMN7SKYvmTr0jACa")





@views.route("/nawarch1rev")
def nawarch1rev():
  teachername = "Revision 1"
  playlist_id = 'PLM-GVlebsoPXELEhVJi-nBm-oZXpE85K2'
  with open("website/templates/teachers/nawarch1rev.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/nawarch1revupdate")
def nawarch1revupdate():
    return createtxtfile("nawarch1rev" , "PLM-GVlebsoPXELEhVJi-nBm-oZXpE85K2")



@views.route("/nawarch2rev")
def nawarch2rev():
  teachername = "Revision 2"
  playlist_id = 'PLM-GVlebsoPVAd_O1EYC8ORRkYGQ_latH'
  with open("website/templates/teachers/nawarch2rev.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)

@views.route("/nawarch2revupdate")
def nawarch2revupdate():
    return createtxtfile("nawarch2rev" , "PLM-GVlebsoPVAd_O1EYC8ORRkYGQ_latH")



@views.route("/nawarch2")
def nawarch2():
  teachername = "Chapter 2"
  playlist_id = 'PLM-GVlebsoPWU4v5bcndzPBt6e7PsiCwQ'
  with open("website/templates/teachers/nawarch2.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/nawarch2update")
def nawarch2update():
    return createtxtfile("nawarch2" , "PLM-GVlebsoPWU4v5bcndzPBt6e7PsiCwQ")






@views.route("/nawarch3")
def nawarch3():
  teachername = "Chapter 3"
  playlist_id = 'PLM-GVlebsoPXwGQGxiTBmNCzD4E_BgDCo'
  with open("website/templates/teachers/nawarch3.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/nawarch3update")
def nawarch3update():
    return createtxtfile("nawarch3" , "PLM-GVlebsoPXwGQGxiTBmNCzD4E_BgDCo")









#Chemistry --------------------------------------------------------------------------------------------------------------------------
@views.route('/chemistry')
def chem():
  teacher_links = {
     "Nasser-El-Batal": ("nasser", "Nasser-El-Batal")
  }
  teachername = "Chemistry"
  return render_template('used_pages/teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")




nasserlinks = {
    "Nasser-El-Batal Chapter 1": ("chemch1", "Chapter 1", "PLM-GVlebsoPXWpBDCzn4h0L36UNRYuFb2"),
    "Nasser-El-Batal Chapter 2": ("chemch2", "Chapter 2", "PLM-GVlebsoPVYwDkN3DxFcyS1QWCKfAjv"),
    "Nasser-El-Batal Chapter 3": ("chemch3", "Chapter 3", "PLM-GVlebsoPVXmash3q9sfG5bsD3Mt88x"),
    "Nasser-El-Batal Chapter 4": ("chemch4", "Chapter 4", "PLM-GVlebsoPXBmTFLVyH4mWaxQELcIQ8C")
}


@views.route('/nasser')
def nasser():
  teacher_links = {key: (value[0], value[1]) for key, value in nasserlinks.items()}
  teacher_links["Nasser-El-Batal Files"] = ("chempdfs", "Google Drive")
  teachername = "Chemistry"
  return render_template('used_pages/teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")


@views.route("/chemch<int:i>update")
def update_route(i):
    chapter_name = f"chemch{i}"
    playlist_id = nasserlinks.get(f"Nasser-El-Batal Chapter {i}", ("", "", ""))[2]

    return createtxtfile(chapter_name, playlist_id)


@views.route("/chemch<int:i>")
def nasservids(i):
  teachername = f"Chapter {i}"
  playlist_id = nasserlinks.get(f"Nasser-El-Batal Chapter {i}", ("", "", ""))[2]
  with open(f"website/templates/teachers/chemch{i}.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)




#Math --------------------------------------------------------------------------------------------------------------------------
@views.route('/math')
def math():
  teacher_links = {
  "Sherbo": ("/sherbo", "Omar sherbeni"),
    "Salama": ("salama", "Mohamed Salama")
  }
  teachername = "Math"
  return render_template('used_pages/teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")
@views.route('/sherbo')
def sherbo():
  teacher_links = {
    "Sherbo Statics": ("sherbostatics", "Statics"),
    "Sherbo Calculus": ("sherbocalc", "Calculus"),
    "Sherbo Files": ("sherbopdfs", "Google Drive")
  }
  teachername = "Math"
  return render_template('used_pages/teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")
@views.route("/sherbostatics")
def sherbostatics():
  teachername = "Sherbo Statics"
  playlist_id="PLM-GVlebsoPX_3mlaOeWIjCPY8jH8MpfJ"
  with open("website/templates/teachers/sherbostatics.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)

@views.route("/sherbostaticsupdate")
def sherbostaticsupdate():
    return createtxtfile("sherbostatics" , "PLM-GVlebsoPX_3mlaOeWIjCPY8jH8MpfJ")



@views.route("/sherbocalc")
def sherbocalc():
  teachername = "Sherbo Calculus"
  playlist_id = 'PLM-GVlebsoPXrU733HavPf8k-P5h_aFFq'
  with open("website/templates/teachers/sherbocalc.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)

@views.route("/sherbocalcupdate")
def sherbocalcupdate():
    return createtxtfile("sherbocalc" , "PLM-GVlebsoPXrU733HavPf8k-P5h_aFFq")




salama_info = {
    # "PreStudy": {"id": 'PLM-GVlebsoPVEULTnn90gqVL0AL99KtU0'},
    "Course 1": {"id": 'PLM-GVlebsoPWfuCf4h_ucKPOBKjH6No-W'},
    "Course 2": {"id": 'PLM-GVlebsoPUubsCYnPGc27tihI0pz4hi'},
    "Course 3": {"id": 'PLM-GVlebsoPUSSsoABHH059FBapcSjvGg'},
    "Course 4": {"id": 'PLM-GVlebsoPXWSZDCjeDfvdMV5QXYwg4x'},
    "Course 5": {"id": 'PLM-GVlebsoPWEGxQu5D0hVrUCJjTMqYvd'},
    "Course 6": {"id": 'PLM-GVlebsoPWZKrvX8MvfJxfxXhKXvqR3'},
    "Course 7": {"id": 'PLM-GVlebsoPUobUeuNIWsitKeP-aHOwif'},
    "Course 8": {"id": 'PLM-GVlebsoPUqwS3-Ij-pHBq4_aoEAwMZ'},
    "Course 9": {"id": 'PLM-GVlebsoPXe2kZo_cM06BZWXwdSxQ7B'},
    "Course 10": {"id": 'PLM-GVlebsoPXZmghd3uMqZWx6wlLZDiiu'},
    "Course 11": {"id": 'PLM-GVlebsoPVB0u2fWqO9ep3cuBp_8zTW'},
    "Course 12": {"id": 'PLM-GVlebsoPU0BwzCsqsPQfKMSPZauuFl'},
    "Course 13": {"id": 'PLM-GVlebsoPURAU8nu_tU2dphnGXxZeMM'},
    "Course 14": {"id": 'PLM-GVlebsoPXnRQBjkDqUUAXDKyUJqK9-'},
    "Course 15": {"id": 'PLM-GVlebsoPWCqnSBAANAy8Wn89lbLmqt'},
    "Course 16": {"id": 'PLM-GVlebsoPUF0Px3a00jPzFLwJwkpgBw'},
    "Course 17": {"id": 'PLM-GVlebsoPXMiQ12yf0u8yXhwuFTAR0h'},
    "Course 18": {"id": 'PLM-GVlebsoPV0RRzBKVtugIVlvEKmmHQn'},
    "Course 19": {"id": 'PLM-GVlebsoPW0boxDQxqLZz8gbmxhGZvP'},


}


@views.route("/salamach<int:course_number>update")
def salamacoursesupdate(course_number):
    course_key = f"Course {course_number}"
    if course_key not in salama_info:
        return redirect(url_for('views.display_links'))
    playlist_id = salama_info[course_key]["id"]

    return  createtxtfile(f"salama{course_key}", playlist_id)


@views.route('/salama')
def salama():
    
    teacher_links = {course: (f"/salamach{i}", course) for i, (course, _) in enumerate(salama_info.items(), start=1)}
    teachername = "Math"
    return render_template('used_pages/teacher.html', teacher_links=teacher_links, teachername=teachername, imgs="yes")

@views.route("/salamach<int:course_number>")
def salamach(course_number):
    course_key = f"Course {course_number}"
    if course_key not in salama_info:
        return redirect(url_for('views.display_links'))
    teachername = course_key
    playlist_id = salama_info[course_key]["id"]
    # videos = get_playlist_videos(playlist_id)
    with open(f"website/templates/teachers/salama{course_key}.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
    return render_template('used_pages/videopage.html', videos=videos, playlist_id=playlist_id, teachername=teachername)









#Arabic --------------------------------------------------------------------------------------------------------------------------
@views.route('/arabic')
def gedo():
  teacher_links = {
    "Gedo": ("gedoo", "Gedo"),
}
  teachername = "Arabic"
  return render_template('used_pages/teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")
import ast


@views.route("/gedoo")
def gedoo2():
    playlist_id = 'PLM-GVlebsoPXBcSNcLjkmcQG53hQYTvui'
    teachername= "Gedo"
    with open("website/templates/teachers/gedo.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
    return render_template('used_pages/videopage.html',
                           videos=videos,
                           playlist_id=playlist_id,
                           teachername=teachername)


@views.route("/gedoupdate")
def gedoupdate():
    return createtxtfile("gedo" , "PLM-GVlebsoPXBcSNcLjkmcQG53hQYTvui")

def createtxtfile(name ,playlist_id ):
    videos = get_playlist_videos(playlist_id)
    with open(f"website/templates/teachers/{name}.txt", 'w' , encoding='utf-8') as file:
        file.write(str(videos))
    return videos  




#Geology --------------------------------------------------------------------------------------------------------------------------
@views.route('/geology')
def geology():
  teacher_links = {
    "Sameh Nash2t": ("sameh", "Sameh Nash2t"),
    "Gio maged": ("giomaged", "Gio maged")
  }
  teachername = "Geology"
  return render_template('used_pages/teacher.html',
                          teacher_links=teacher_links,
                          teachername=teachername,
                          imgs="yes")

@views.route('/sameh')
def sameh():
  teacher_links = {
    "Sameh Nash2t Chapter 1": ("samehh1", "Chapter 1"),
    "Sameh Nash2t Chapter 2": ("samehh2", "Chapter 2"),
    "Sameh Nash2t Chapter 3": ("samehh3", "Chapter 3"),
    "Sameh Nash2t Chapter 4": ("samehh4", "Chapter 4"),
  }
  teachername = "Geology"
  return render_template('used_pages/teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")
@views.route("/samehh1")
def samehh1():
  teachername = "Chapter 1"
  playlist_id = 'PLM-GVlebsoPXd5COr54fuG-1lNCfpDdwl'
  videos = get_playlist_videos(playlist_id)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)
@views.route("/samehh2")
def samehh2():
  teachername = "Chapter 2"
  playlist_id = 'PLM-GVlebsoPUckTjXcvKP483XHykKHH-m'
  videos = get_playlist_videos(playlist_id)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)
@views.route("/samehh3")
def samehh3():
  teachername = "Chapter 3"
  playlist_id = 'PLM-GVlebsoPX1xJ0JSvE7gLfkPEKIo3kA'
  videos = get_playlist_videos(playlist_id)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)
@views.route("/samehh4")
def samehh4():
  teachername = "Chapter 4"
  playlist_id = 'PLM-GVlebsoPX_zFeoKW57nOoPlLUMlxZR'
  videos = get_playlist_videos(playlist_id)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)
@views.route("/giomaged")
def giomaged():
  teachername = "Gio maged"
  playlist_id = 'PLM-GVlebsoPXh1obVV3aWysV7wXlN3yET'
  videos = get_playlist_videos(playlist_id)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)











#Biology----------------------------------------------------------------------------------------------------------------------
@views.route('/biology')
def bio():
  teacher_links = {
     "Daif": ("daif", "Mohamed Daif"),
  }
  teachername = "Biology"
  return render_template('used_pages/teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")


bio_links = {
    "Chapter 1": ("bioch1", "S2 Not Available", "PLM-GVlebsoPWYFgg9hks2GaWKC2kI1r7X"),
    "Chapter 2": ("bioch2", "Chapter 2", "PLM-GVlebsoPVXxEs5mtOyS-4QLolBXjlX"),
    "Chapter 3": ("bioch3", "Chapter 3", "PLM-GVlebsoPV0ylAbm7LFlKCD9_X0CGEK"),
}

@views.route('/daif')
def biology():
    teacher_links = {key: (value[0], value[1]) for key, value in bio_links.items()}
    # teacher_links["Daif Files"] = ("biopdfs", "Google Drive") 
    teachername = "Biology"
    return render_template('used_pages/teacher.html',
                           teacher_links=teacher_links,
                           teachername=teachername,
                           imgs="yes")


@views.route("/bioch<int:i>")
def bioch(i):
    teachername = f"Chapter {i}"
    playlist_id = bio_links.get(f"Chapter {i}", ("", "", ""))[2]
    with open(f"website/templates/teachers/bioch{i}.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
    return render_template('used_pages/videopage.html',
                           videos=videos,
                           playlist_id=playlist_id,
                           teachername=teachername)







#-----------------------------------------------------------------------------------------------------------

@views.route('/english')
def english():
  teacher_links = {
     "English": ("englishh", "Ahmed Salah"),

  }
  teachername = "English"
  return render_template('used_pages/teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")


@views.route("/englishh")
def englishh():
  teachername = "English"
  playlist_id = 'PLM-GVlebsoPUWOjoc9DyO2Jh8mclaRY1Q'
  with open("website/templates/teachers/englishh.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)

@views.route("/englishhupdate")
def englishhupdate():
    return createtxtfile("englishh" , "PLM-GVlebsoPUWOjoc9DyO2Jh8mclaRY1Q")










@views.route('/german')
def german():
  teacher_links = {
     "German": ("germann", "Abd El Moez"),
     "German Files": ("germanpdfs", "Google Drive"),

  }
  teachername = "German"
  return render_template('used_pages/teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")

@views.route("/germann")
def germann():
  teachername = "German"
  playlist_id = 'PLM-GVlebsoPWNh__WI8QAIN2xQjawgB4i'
  with open("website/templates/teachers/germann.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)

@views.route("/germannupdate")
def germannupdate():
    return createtxtfile("germann" , "PLM-GVlebsoPWNh__WI8QAIN2xQjawgB4i")










