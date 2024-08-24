from flask import redirect, Blueprint
from flask_login import login_required

shortlinks = Blueprint('shortlinks', __name__)

#------------------------------------------------------------------------------------------------------


@shortlinks.route("/yt")
def youtube():
    return redirect("https://studio.youtube.com/")


@shortlinks.route("/netflix2")
def netflix():
    return redirect("https://www.netflix.com/extra/activate?bid=fb132116-df39-42d1-8326-7d0636dc03cd")


@shortlinks.route("/books")
def books():
    return redirect(
        "https://drive.google.com/drive/folders/12OIgF6ceqUP6yxHdaX22fpQfGWvB-5e8?usp=sharing"
    )


@shortlinks.route("/tools2")
def tools2():
    return redirect(
        "https://drive.google.com/file/d/1to3ZxSfFDN3F0VZMkNjznGXZJaGthiO-/view?usp=drive_link"
    )


@shortlinks.route("/tools")
def tools():
    return redirect(
        "https://cdn.gilcdn.com/ContentMediaGenericFiles/16044bf8dc34aef012591bb86e6b6417-Full.zip"
    )


@shortlinks.route("/table")
def table():
    return redirect("https://periodic-table.tech/")


@shortlinks.route("/sherbopdfs")
def sherbopdfs():
    return redirect(
        "https://drive.google.com/drive/folders/1cEnVqh8bAFr4aqHgMdy-_TpfbEVXC0zc?usp=share_link"
    )


@shortlinks.route("/nawarpdfs")
def nawarpdfs():
    return redirect(
        "https://drive.google.com/drive/folders/1co0YX7h8Xdg3HV4zFhf2xze9yNX-xM71?usp=drive_link"
    )


@shortlinks.route("/chempdfs")
def chempdfs():
    return redirect(
        "https://drive.google.com/drive/folders/1trBpK01IknkeMC9LtsCM7dyTz-9uqY0n?usp=drive_link"
    )


@shortlinks.route("/files")
def files():
    return redirect(
        "https://link.storjshare.io/s/jubit7purhfmiw6zi7mysb2jr4wq/spynet%2FPrivate"
    )


@shortlinks.route("/vdo")
def vdo():
    return redirect(
        "https://cdn.gilcdn.com/ContentMediaGenericFiles/cec96512c8ae6d7cc545381c1dbf421e-Full.txt"
    )


shortlinks.route("/data")


def final():
    return redirect("https://spysnet.com/static/final.json")
