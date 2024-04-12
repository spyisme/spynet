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
    return redirect("https://cdn.gilcdn.com/ContentMediaGenericFiles/dd57cfa0bf90a4898dd70a4ae22b6964-Full.zip?w=1&h=1&Expires=1712933116&Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9jZG4uZ2lsY2RuLmNvbS8qIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNzEyOTMzMTE2fSwiSXBBZGRyZXNzIjp7IkFXUzpTb3VyY2VJcCI6IjUyLjE1OS4xMzguMTYwIn19fV19&Signature=LVs8cu1A6ZVTy67Q%7EbkFTo6vqlNdDwwlhrm0qUUxnCpLaKIBqTgERouT5SGnceVV5eJNt1AC43i22ztwK0JI5QmJXepAU6b6M%7E1AoLcdi82lXvvCDFzpbZAGp0Qo%7E9PglVk42VTUfKb1Bxc70kN6bBOew63sMsrk1LBjDBhWnIY6sf6BkZpyLBisyfmTx9gK992NB14EQ8CJVOmt6DuOysfH-ALd836KBa8ea4WssoHshpZXPt1fJBdPrD%7EQa8rRuXYdvEi%7EGAqgze2aIXHM%7Ew6LDrEpFHP17Z78HtpSsYnzmIMjXEv%7E7Um%7Eo1ZEbUU3oXs%7EAGQjixzvNdgcCt89uA__&Key-Pair-Id=K1FFKFZRWAZSB")         

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

      

@shortlinks.route("/files")
def files():
    return redirect("https://link.storjshare.io/s/jubit7purhfmiw6zi7mysb2jr4wq/spynet%2FPrivate") 
            

@shortlinks.route("/vdo")
def vdo():
    return redirect("https://cdn.gilcdn.com/ContentMediaGenericFiles/cec96512c8ae6d7cc545381c1dbf421e-Full.txt") 
            

