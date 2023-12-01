from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from googleapiclient.discovery import build
import random
import json
import requests
from flask_login import login_user, logout_user, login_required
from .models import User
from werkzeug.security import check_password_hash , generate_password_hash
from . import db

views = Blueprint('views', __name__)
print('Running!')










@views.route('/all')
def display_links():
    with open('website/links.txt', 'r') as file:
        lines = file.readlines()

    return render_template('teacher.html', lines=lines, teachername="All")





@views.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
      login_user(user)
      flash('Login successful!', category='success')
      return redirect(url_for('views.home'))
    else:
      flash('Login unsuccessful. Please check your username and password.',
            category='error')

  return render_template('login.html')


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

#     return render_template('register.html')

import isodate

YOUTUBE_API_KEY = 'AIzaSyAbrVMIzmLLhHQSrMVUG8gS3d6IAYE0qVc'

def chunks(lst, chunk_size):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

def get_video_details(video_ids):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

    videos = []
    for video_chunk in chunks(video_ids, 50):
        video_request = youtube.videos().list(
            part='contentDetails,snippet',
            id=','.join(video_chunk)
        )
        video_response = video_request.execute()

        for item in video_response.get('items', []):
            content_details = item.get('contentDetails', {})
            duration = content_details.get('duration', '')

            # Check if the duration is not empty before attempting to parse it
            if duration:
                parsed_duration = isodate.parse_duration(duration)
                duration_formatted = str(parsed_duration)
            else:
                duration_formatted = 'N/A'

            videos.append({
                'duration': duration_formatted,
                'title': item.get('snippet', {}).get('title', ''),
                'id': item['id']
            })

    return videos

def get_playlist_videos(playlist_id):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

    playlist_items = []
    next_page_token = None

    while True:
        playlist_request = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token)
        playlist_response = playlist_request.execute()

        playlist_items.extend(playlist_response.get('items', []))
        next_page_token = playlist_response.get('nextPageToken')

        if not next_page_token:
            break

    video_ids = [item['contentDetails']['videoId'] for item in playlist_items]
    videos = get_video_details(video_ids)

    return videos


@views.route("/")
def home():
  return render_template("index.html")



@views.route("/edit")
def edit():
  return redirect("https://replit.com/@Spy/Spynet")


@views.route('/nawar')
def nawar():
  teacher_links = {
  "Nawar Chapter 1": ("/nawarch1", "Chapter 1"),
    "Nawar Chapter 1 Revision": ("nawarch1rev", "Chapter 1 Revision"),
    "Nawar Chapter 2": ("nawarch2", "Chapter 2")
  }

  teachername = "Nawar"
  return render_template('teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")


@views.route("/nawarch1")
def nawarch1():
  teachername = "Nawar"
  playlist_id = 'PLM-GVlebsoPXpGe3wzMN7SKYvmTr0jACa'
  videos = get_playlist_videos(playlist_id)
  return render_template('videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/nawarch1rev")
def nawarch1rev():
  teachername = "Nawar"
  playlist_id = 'PLM-GVlebsoPXELEhVJi-nBm-oZXpE85K2'
  videos = get_playlist_videos(playlist_id)
  return render_template('videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/nawarch2")
def nawarch2():
  teachername = "Nawar"
  playlist_id = 'PLM-GVlebsoPWU4v5bcndzPBt6e7PsiCwQ'
  videos = get_playlist_videos(playlist_id)
  # videos += [{'url': '/nawarstorj', 'title': 'More'}]
  return render_template('videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route('/chem')
def chem():
  teacher_links = {
     "Nasser-El-Batal Chapter 1": ("chemch1", "Chapter 1"),
    "Nasser-El-Batal Chapter 2": ("chemch2", "Chapter 2"),
    "Nasser-El-Batal Chapter 3": ("chemch3", "Chapter 3")
  

  }

  teachername = "Nasser-El-Batal"
  return render_template('teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")


@views.route("/chemch1")
def chemch1():
  teachername = "Nasser-El-Batal"
  playlist_id = 'PLM-GVlebsoPXWpBDCzn4h0L36UNRYuFb2'
  videos = get_playlist_videos(playlist_id)
  return render_template('videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/chemch2")
def chemch2():
    teachername = "Nasser-El-Batal"
    playlist_id = 'PLM-GVlebsoPVYwDkN3DxFcyS1QWCKfAjv'
    videos = get_playlist_videos(playlist_id)
    #return videos
    return render_template('videopage.html',
                          videos=videos,
                          playlist_id=playlist_id,
                          teachername=teachername)



@views.route("/chemch2test")
def chemch2test():
    teachername = "Nasser-El-Batal"
    playlist_id = 'PLM-GVlebsoPVYwDkN3DxFcyS1QWCKfAjv'
    videos = get_playlist_videos(playlist_id)
    #return videos
    return render_template('videopagesplits.html',
                          videos=videos,
                          playlist_id=playlist_id,
                          teachername=teachername)
                         
@views.route("/chemch3")
def chemch3():
    teachername = "Nasser-El-Batal"
    playlist_id = 'PLM-GVlebsoPVXmash3q9sfG5bsD3Mt88x'
    videos = get_playlist_videos(playlist_id)
    # videos += [{'url': '/chemstorj', 'title': 'More'}]
    return render_template('videopage.html',
                           videos=videos,
                           playlist_id=playlist_id,
                           teachername=teachername)



@views.route('/sherbo')
def sherbo():
  teacher_links = {
    "Sherbo Statics": ("sherbostatics", "S1 --> S10"),
    "Sherbo Statics v2": ("sherbostatics2", "S11 --> Chapter 6 rev"),
    "Sherbo Calculus": ("sherbocalc", "Calculus")
  }

  teachername = "Sherbo"
  return render_template('teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")


@views.route("/sherbostatics")
def sherbostatics():
  teachername = "Sherbo Statics"
  playlist_id = 'PLM-GVlebsoPX_3mlaOeWIjCPY8jH8MpfJ'
  videos = get_playlist_videos(playlist_id)
  return render_template('videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)

@views.route("/sherbostatics2")
def sherbostatics2():
  teachername = "Sherbo Statics"
  playlist_id = 'PLM-GVlebsoPWglys60cNg_dhTJ6RzXmUR'
  videos = get_playlist_videos(playlist_id)
  return render_template('videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)



@views.route("/sherbocalc")
def sherbocalc():
  teachername = "Sherbo Calculus"
  playlist_id = 'PLM-GVlebsoPXrU733HavPf8k-P5h_aFFq'
  videos = get_playlist_videos(playlist_id)
  return render_template('videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route('/sameh')
def sameh():
  teacher_links = {
    "Sameh Nash2t Chapter 1": ("samehh1", "Chapter 1"),
    "Sameh Nash2t Chapter 2": ("samehh2", "Chapter 2"),
    "Sameh Nash2t Chapter 3": ("samehh3", "Chapter 3")

  }

  teachername = "Sameh Nash2t"
  return render_template('teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")


@views.route("/samehh1")
def samehh1():
  teachername = "Sameh Nash2t"
  playlist_id = 'PLM-GVlebsoPXd5COr54fuG-1lNCfpDdwl'
  videos = get_playlist_videos(playlist_id)
  return render_template('videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/samehh2")
def samehh2():
  teachername = "Sameh Nash2t"
  playlist_id = 'PLM-GVlebsoPUckTjXcvKP483XHykKHH-m'
  videos = get_playlist_videos(playlist_id)
  return render_template('videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/samehh3")
def samehh3():
  teachername = "Sameh Nash2t"
  playlist_id = 'PLM-GVlebsoPX1xJ0JSvE7gLfkPEKIo3kA'
  videos = get_playlist_videos(playlist_id)
  return render_template('videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)
@views.route('/gedo')
def gedo():
  teacher_links = {
    "Gedo": ("gedoo", "Gedo"),
    # Add other entries with the correct structure
}
  teachername = "Gedo"
  return render_template('teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")


@views.route("/gedoo")
def gedoo():
  teachername = "Gedo"
  playlist_id = 'PLM-GVlebsoPXBcSNcLjkmcQG53hQYTvui'
  videos = get_playlist_videos(playlist_id)
  #videos += [{'url': '/gedostorj', 'title': 'More'}]

  return render_template('videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route('/bio')
def bio():
  teacher_links = {
      "Chapter 1": ("bioch1", "Chapter 1"),
    "Chapter 2": ("bioch2", "Chapter 2"),
    "Chapter 3": ("bioch3", "Chapter 3"),


  }

  teachername = "Daif"
  return render_template('teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")


@views.route("/bioch1")
def bioch1():
  teachername = "Daif"
  playlist_id = 'PLM-GVlebsoPWYFgg9hks2GaWKC2kI1r7X'
  videos = get_playlist_videos(playlist_id)
  return render_template('videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/bioch2")
def bioch2():
  teachername = "Daif"
  playlist_id = 'PLM-GVlebsoPVXxEs5mtOyS-4QLolBXjlX'
  videos = get_playlist_videos(playlist_id)
  return render_template('videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)

@views.route("/bioch3")
def bioch3():
  teachername = "Daif"
  playlist_id = 'PLM-GVlebsoPV0ylAbm7LFlKCD9_X0CGEK'
  videos = get_playlist_videos(playlist_id)
 # videos += [{'url': '/biostorj', 'title': 'More'}]

  return render_template('videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)

@views.route("/english")
def english():
  teachername = "English"
  playlist_id = 'PLM-GVlebsoPUWOjoc9DyO2Jh8mclaRY1Q'
  videos = get_playlist_videos(playlist_id)
  return render_template('videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route('/salama')
def salama():
  teacher_links = {
  "PreStudy": ("https://spysnet.com/salamapre", "PreStudy"),
    "Course 1": ("https://spysnet.com/salamach1", "Course 1"),
    "Course 2": ("https://spysnet.com/salamach2", "Course 2"),
    "Course 3": ("https://spysnet.com/salamach3", "Course 3"),
    "Course 4": ("https://spysnet.com/salamach4", "Course 4"),
    "Course 5": ("https://spysnet.com/salamach5", "Course 5"),
    "Course 6 (Revision)": ("https://spysnet.com/salamach6", "Course 6 (Revision)"),
    "Course 7": ("https://spysnet.com/salamach7", "Course 7"),
    "Course 8": ("https://spysnet.com/salamach8", "Course 8"),
    "Course 9": ("https://spysnet.com/salamach9", "Course 9"),
    "Course 10": ("https://spysnet.com/salamach10", "Course 10"),
    "Course 11": ("https://spysnet.com/salamach11", "Course 11"),
    "Course 12": ("https://spysnet.com/salamach12", "Course 12")
  }
  teachername = "Mohamed Salama"
  return render_template('teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")


@views.route("/salamapre")
def salamapre():
  teachername = "Mohamed Salama PreStudy"
  playlist_id = 'PLM-GVlebsoPVEULTnn90gqVL0AL99KtU0'
  videos = get_playlist_videos(playlist_id)
  return render_template('videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/salamach1")
def salamach1():
  teachername = "Mohamed Salama Course 1"
  playlist_id = 'PLM-GVlebsoPWfuCf4h_ucKPOBKjH6No-W'
  videos = get_playlist_videos(playlist_id)
  return render_template('videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/salamach2")
def salamach2():
  teachername = "Mohamed Salama Course 2"
  playlist_id = 'PLM-GVlebsoPUubsCYnPGc27tihI0pz4hi'
  videos = get_playlist_videos(playlist_id)
  return render_template('videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/salamach3")
def salamach3():
  teachername = "Mohamed Salama Course 3"
  playlist_id = 'PLM-GVlebsoPUSSsoABHH059FBapcSjvGg'
  videos = get_playlist_videos(playlist_id)
  return render_template('videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/salamach4")
def salamach4():
  teachername = "Mohamed Salama Course 4"
  playlist_id = 'PLM-GVlebsoPXWSZDCjeDfvdMV5QXYwg4x'
  videos = get_playlist_videos(playlist_id)
  return render_template('videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/salamach5")
def salamach5():
  teachername = "Mohamed Salama Course 5"
  playlist_id = 'PLM-GVlebsoPWEGxQu5D0hVrUCJjTMqYvd'
  videos = get_playlist_videos(playlist_id)
  return render_template('videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/salamach6")
def salamach6():
  teachername = "Mohamed Salama Course 6"
  playlist_id = 'PLM-GVlebsoPWZKrvX8MvfJxfxXhKXvqR3'
  videos = get_playlist_videos(playlist_id)
  return render_template('videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/salamach7")
def salamach7():
  teachername = "Mohamed Salama"
  playlist_id = 'PLM-GVlebsoPUobUeuNIWsitKeP-aHOwif'
  videos = get_playlist_videos(playlist_id)
  return render_template('videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/salamach8")
def salamach8():
  teachername = "Mohamed Salama Course 8"
  playlist_id = 'PLM-GVlebsoPUqwS3-Ij-pHBq4_aoEAwMZ'
  videos = get_playlist_videos(playlist_id)
  return render_template('videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/salamach9")
def salamach9():
  teachername = "Mohamed Salama Course 9"
  playlist_id = 'PLM-GVlebsoPXe2kZo_cM06BZWXwdSxQ7B'
  videos = get_playlist_videos(playlist_id)
  return render_template('videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)




@views.route("/salamach10")
def salamach10():
  teachername = "Mohamed Salama Course 10"
  playlist_id = 'PLM-GVlebsoPXZmghd3uMqZWx6wlLZDiiu'
  videos = get_playlist_videos(playlist_id)
  return render_template('videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)



@views.route("/salamach11")
def salamach11():
  teachername = "Mohamed Salama Course 11"
  playlist_id = 'PLM-GVlebsoPVB0u2fWqO9ep3cuBp_8zTW'
  videos = get_playlist_videos(playlist_id)
 # videos += [{'url': '/salamastorj', 'title': 'More'}]

  return render_template('videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/salamach12")
def salamach12():
  teachername = "Mohamed Salama Course 12"
  playlist_id = 'PLM-GVlebsoPU0BwzCsqsPQfKMSPZauuFl'
  videos = get_playlist_videos(playlist_id)
 # videos += [{'url': '/salamastorj', 'title': 'More'}]

  return render_template('videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)




@views.route('/iframes', methods=['GET', 'POST'])
def iframes():
  url = request.args.get('url')
  if url is None:
    url = "none"
  url = url.replace("/play/", "/embed/")
  if request.method == 'POST':
    name = request.form.get('name')
    msg = f'```python main.py {url} {name}``` {name}'
    message = {'content': f'{msg}'}
    payload = json.dumps(message)
    headers = {'Content-Type': 'application/json'}
    webhook_url = "https://discord.com/api/webhooks/1170733207835115630/MpyyTLirCjBUOSHxisTsb4l7lqF7XBw-l4KEsi7DAFLAoZdUzMtGFwth67Qj3ZJCE5Oo"
    requests.post(webhook_url, data=payload, headers=headers)
    return "Message Sent!"
  return render_template('iframe.html', url=url, word="url")

@views.route('/sherboiframe', methods=['GET', 'POST'])
def sherboframe():
    url = request.args.get('url')
    url = url.replace("/play/", "/embed/")
    if request.method == 'POST':
        name =  request.form.get('name')
        if "youtube" in url.lower(): 
            url = url.split('/')[4]

            msg = f'<https://www.y2mate.com/youtube/{url}> ```{name}```'
        else: 
            msg = f'```python main.py {url} {name}``` {name}'
        message = {
                'content': f'{msg}'
            }
        payload = json.dumps(message)
        headers = {'Content-Type': 'application/json'}
        webhook_url = "https://discord.com/api/webhooks/1169342540575670292/crazeFe5z0qAozWBJOnlZfevMMQ219NVzZ-Cl6mWK9NrtBqBXc3kBzj1tJ8_KVu7UuKf"
        requests.post(webhook_url, data=payload, headers=headers)
        return "Message Sent!" 
    return render_template('iframe.html' , url = url)