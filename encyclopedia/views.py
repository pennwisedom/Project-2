from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def display_page(request, title):
    return render(request, "encyclopedia/page.html", {
        "entry": util.get_entry(title), "title": title
    })