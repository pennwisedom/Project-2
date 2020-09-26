import markdown2
from django.shortcuts import render
from django import forms

from . import util

class NewSearchForm(forms.Form):
    searchword = forms.CharField(label="searchword")


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