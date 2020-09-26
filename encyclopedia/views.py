import markdown2
import random

from django.shortcuts import render, redirect
from django import forms

from . import util

class NewSearchForm(forms.Form):
    searchword = forms.CharField(label="searchword")

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    body = forms.CharField(label= '', widget=forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
        })

# Displays a page if it exists, else displays Not Found.
def display_page(request, title):
    if not util.get_entry(title):
        return render(request, "encyclopedia/notfound.html", {"title": title
        })
    else:    
        return render(request, "encyclopedia/page.html", {
            "entry": markdown2.markdown(util.get_entry(title)), "title": title
            })

# Search Function, goes to page or returns a list of possible results.
def search(request):
    if request.method == "POST":
        entries = util.list_entries()
        searchlist = []
        for entry in entries:
            searchlist.append(entry.lower())

        form = NewSearchForm(request.POST)

        if form.is_valid():
            word = form.cleaned_data["searchword"]
                        
            if word.lower() in searchlist:
                return render(request, "encyclopedia/page.html", {
                    "entry": markdown2.markdown(util.get_entry(word)), "title": word
                    })
            
            else: 
                results = []
                for i in searchlist:
                    if word in i:
                        results.append(i)

                return render(request, "encyclopedia/search.html", { 
                    "results": results
                    })  

# Goes to a Random Page
def random_page(request):
    pagelist = util.list_entries()
    selected = random.choice(pagelist)
    return redirect(display_page, title=selected)

# Creates a New Page
def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/newpage.html", {
            "form": NewPageForm()
        })

    elif request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"]
            entries = []

            for entry in util.list_entries():
                entries.append(entry.lower())
                                    
            if title.lower() in entries:
                error = True
                return render(request, "encyclopedia/newpage.html", {
                    "form": form, "error": error, "title": title 
                })
            
            else:
                util.save_entry(title, body)
                success = True
                return render(request, "encyclopedia/index.html", {"success": success, "title": title, "entries": util.list_entries()})