import markdown2
from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def display_page(request, title):
    if not util.get_entry(title):
        return render(request, "encyclopedia/notfound.html", {"title": title
        })
    else:    
        return render(request, "encyclopedia/page.html", {
            "entry": markdown2.markdown(util.get_entry(title)), "title": title
        })