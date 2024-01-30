from flask import Blueprint, render_template, request, redirect, url_for, flash , session
from googleapiclient.discovery import build

import random

YOUTUBE_API_KEY = 'AIzaSyAbrVMIzmLLhHQSrMVUG8gS3d6IAYE0qVc'



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

    videos = [{'id': item['snippet']['resourceId']['videoId'], 'title': item['snippet']['title']}
              for item in playlist_items]

    return videos

views = Blueprint('views', __name__)
print('Running!')


@views.route("/")
def home():
  return render_template("index.html")


@views.route("/game", methods=['GET', 'POST'])
def game():
    if 'score' not in session:
        session['score'] = 0

    if 'answer' not in session:
        session['answer'] = 0

    while True:
        num1 = random.randint(1, 50)
        num2 = random.randint(1, 50)

        if num1 + num2 < 200:
            break

    session['num1'] = num1
    session['num2'] = num2
    
    return render_template('game.html', num1=num1, num2=num2, score=session['score'], answer=session['answer'])

@views.route("/gamesubmit", methods=['POST'])
def gamesubmit():
    user_sum = int(request.form['user_sum'])
    num1 = session['num1']
    num2 = session['num2']
    correct_sum = num1 + num2

    if user_sum == correct_sum:
        session['score'] += 1
        session['answer'] = "correct"
    else:
        session['answer'] = "wrong"
  
    
    return redirect("/game")


@views.route("/reset", methods=['POST'])
def reset_score():
    session['score'] = 0
    session['answer'] = " "
    return redirect("/game")






@views.route("/edit")
def edit():
  return redirect("https://replit.com/@Spy/Spynet")


@views.route('/nawar')
def nawar():
  teacher_links = {
    "Nawar Chapter 1":
    "https://spysnet.com/nawarch1",
    "Nawar Chapter 1 Revision":
    "https://spysnet.com/nawarch1rev",
    "Nawar Chapter 2":
    "https://spysnet.com/nawarch2"
  }

  teachername = "Nawar"
  return render_template('teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername, imgs="yes")


@views.route("/nawarch1")
def nawarch1():
      teachername = "Nawar"
      playlist_id = 'PLM-GVlebsoPXpGe3wzMN7SKYvmTr0jACa'
      videos = get_playlist_videos(playlist_id)
      return render_template('videopage.html', videos=videos ,playlist_id = playlist_id , teachername=teachername)


@views.route("/nawarch1rev")
def nawarch1rev():
      teachername = "Nawar"
      playlist_id = 'PLM-GVlebsoPXELEhVJi-nBm-oZXpE85K2'
      videos = get_playlist_videos(playlist_id)
      return render_template('videopage.html', videos=videos ,playlist_id = playlist_id , teachername=teachername)




@views.route("/nawarch2")
def nawarch2():
      teachername = "Nawar"
      playlist_id = 'PLM-GVlebsoPWU4v5bcndzPBt6e7PsiCwQ'
      videos = get_playlist_videos(playlist_id)
      return render_template('videopage.html', videos=videos ,playlist_id = playlist_id , teachername=teachername)








@views.route('/chem')
def chem():
  teacher_links = {
    "Nasser-El-Batal Chapter 1":
    "https://spysnet.com/chemch1",
    "Nasser-El-Batal Chapter 2":
    "https://spysnet.com/chemch2"
  }

  teachername = "Nasser-El-Batal"
  return render_template('teacher.html',
                         teacher_links=teacher_links, 
                         teachername=teachername,imgs="yes")

@views.route("/chemch1")
def chemch1():
      teachername = "Nasser-El-Batal"
      playlist_id = 'PLM-GVlebsoPXWpBDCzn4h0L36UNRYuFb2'
      videos = get_playlist_videos(playlist_id)
      return render_template('videopage.html', videos=videos ,playlist_id = playlist_id , teachername=teachername)

@views.route("/chemch2")
def chemch2():
      teachername = "Nasser-El-Batal"
      playlist_id = 'PLM-GVlebsoPVYwDkN3DxFcyS1QWCKfAjv'
      videos = get_playlist_videos(playlist_id)
      return render_template('videopage.html', videos=videos ,playlist_id = playlist_id , teachername=teachername)




@views.route('/sherbo')
def sherbo():
  teacher_links = {
    "Omar El Sherbeni Statics":
    "https://spysnet.com/sherbostatics"
  }

  teachername = "Sherbo"
  return render_template('teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,imgs="yes")

@views.route("/sherbostatics")
def sherbostatics():
      teachername = "Sherbo"
      playlist_id = 'PLM-GVlebsoPX_3mlaOeWIjCPY8jH8MpfJ'
      videos = get_playlist_videos(playlist_id)
      return render_template('videopage.html', videos=videos ,playlist_id = playlist_id , teachername=teachername)







@views.route('/sameh')
def sameh():
  teacher_links = {
    "Sameh Nash2t Chapter 1":
    "https://spysnet.com/samehh1",
    "Sameh Nash2t Chapter 2":
    "https://spysnet.com/samehh2"
  }

  teachername = "Sameh Nash2t"
  return render_template('teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,imgs="yes")

@views.route("/samehh1")
def samehh1():
      teachername = "Sameh Nash2t"
      playlist_id = 'PLM-GVlebsoPXd5COr54fuG-1lNCfpDdwl'
      videos = get_playlist_videos(playlist_id)
      return render_template('videopage.html', videos=videos ,playlist_id = playlist_id , teachername=teachername)



@views.route("/samehh2")
def samehh2():
      teachername = "Sameh Nash2t"
      playlist_id = 'PLM-GVlebsoPUckTjXcvKP483XHykKHH-m'
      videos = get_playlist_videos(playlist_id)
      print(videos)

      return render_template('videopage.html', videos=videos ,playlist_id = playlist_id , teachername=teachername)




@views.route('/gedo')
def gedo():
  teacher_links = {
    "Gedo":
    "https://spysnet.com/gedoo"
  }

  teachername = "Gedo"
  return render_template('teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername ,imgs="yes")
@views.route("/gedoo")
def gedoo():
      teachername = "Gedo"
      playlist_id = 'PLM-GVlebsoPWtTfznU7XPEmDv5IOcMoKx'
      videos = get_playlist_videos(playlist_id)
      return render_template('videopage.html', videos=videos ,playlist_id = playlist_id , teachername=teachername)







@views.route('/bio')
def bio():
  teacher_links = {
    "Chapter 1":
    "https://spysnet.com/bioch1",
    "Chapter 2":
    "https://spysnet.com/bioch2"
  }

  teachername = "Daif"
  return render_template('teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,imgs="yes")
@views.route("/bioch1")
def bioch1():
      teachername = "Daif"
      playlist_id = 'PLM-GVlebsoPWYFgg9hks2GaWKC2kI1r7X'
      videos = get_playlist_videos(playlist_id)
      return render_template('videopage.html', videos=videos ,playlist_id = playlist_id , teachername=teachername)



@views.route("/bioch2")
def bioch2():
      teachername = "Daif"
      playlist_id = 'PLM-GVlebsoPVXxEs5mtOyS-4QLolBXjlX'
      videos = get_playlist_videos(playlist_id)
      return render_template('videopage.html', videos=videos ,playlist_id = playlist_id , teachername=teachername)






@views.route("/english")
def english():
      teachername = "English"
      playlist_id = 'PLM-GVlebsoPUWOjoc9DyO2Jh8mclaRY1Q'
      videos = get_playlist_videos(playlist_id)
      return render_template('videopage.html', videos=videos ,playlist_id = playlist_id , teachername=teachername)









@views.route('/salama')
def salama():
  teacher_links = {
    "PreStudy":
    "https://www.youtube.com/playlist?list=PLM-GVlebsoPVEULTnn90gqVL0AL99KtU0",
    "Course 1":
    "https://www.youtube.com/playlist?list=PLM-GVlebsoPWfuCf4h_ucKPOBKjH6No-W",
    "Course 2":
    "https://www.youtube.com/playlist?list=PLM-GVlebsoPUubsCYnPGc27tihI0pz4hi",
    "Course 3":
    "https://www.youtube.com/playlist?list=PLM-GVlebsoPUSSsoABHH059FBapcSjvGg",
    "Course 4":
    "https://www.youtube.com/playlist?list=PLM-GVlebsoPXWSZDCjeDfvdMV5QXYwg4x",
    "Course 5":
    "https://www.youtube.com/playlist?list=PLM-GVlebsoPWEGxQu5D0hVrUCJjTMqYvd",
    "Course 6 (Revison)":
    "https://www.youtube.com/playlist?list=PLM-GVlebsoPWZKrvX8MvfJxfxXhKXvqR3"
  }
  teachername = "Mohamed Salama"
  return render_template('teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername , imgs="yes")





