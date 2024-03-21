from flask import   redirect,  Blueprint 
from flask_login import login_required


shortlinks = Blueprint('shortlinks', __name__)

#------------------------------------------------------------------------------------------------------

@shortlinks.route("/yt")
def youtube():
    return redirect("https://studio.youtube.com/") 
        

@shortlinks.route("/books")
def books():
    return redirect("https://drive.google.com/drive/folders/12OIgF6ceqUP6yxHdaX22fpQfGWvB-5e8?usp=sharing") 
              
@shortlinks.route("/tools2")
def tools2():
    return redirect("https://drive.google.com/file/d/1to3ZxSfFDN3F0VZMkNjznGXZJaGthiO-/view?usp=drive_link")   
  
@shortlinks.route("/tools")
def tools():
    return redirect("https://cdn.gilcdn.com/ContentMediaGenericFiles/c53be27cafdece4e800763625ed2e3a6-Full.zip")         

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
    return redirect("https://cdn.gilcdn.com/ContentMediaGenericFiles/cec96512c8ae6d7cc545381c1dbf421e-Full.txt") 
            

@shortlinks.route("/germanpdfs")
def germanpdfs():
    return redirect("https://drive.google.com/drive/folders/1Mfyook7uXVp0d3y85WaRUuXB_F6Or_Yn?usp=drive_link") 

@shortlinks.route("/netflix")
def netflix():
    return redirect("https://cdn.gilcdn.com/ContentMediaGenericFiles/e307db6fbd6bb5572b1ab2c47c59b2e2-Full.txt") 


