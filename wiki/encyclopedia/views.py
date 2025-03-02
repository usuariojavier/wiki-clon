# encyclopedia/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from . import util
import markdown2
import random


# Create your views here.
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    
    html_content = markdown2.markdown(content)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content
    })

def search(request):
    query = request.GET.get('q', '')
    if not query:
        return redirect('encyclopedia:index')
    
    entries = util.list_entries()
    
    # Si hay una coincidencia exacta, redirigir a esa entrada
    if query in entries:
        return redirect('encyclopedia:entry', title=query)
    
    # Buscar coincidencias parciales
    matches = [entry for entry in entries if query.lower() in entry.lower()]
    
    return render(request, "encyclopedia/search.html", {
        "matches": matches,
        "query": query
    })

def new_page(request):
    if request.method == "POST":
        title = request.POST.get("title", "")
        content = request.POST.get("content", "")
        
        if not title or not content:
            return render(request, "encyclopedia/new.html", {
                "error": "Both title and content are required."
            })
        
        if title in util.list_entries():
            return render(request, "encyclopedia/new.html", {
                "error": "Encyclopedia entry already exists with this title."
            })
        
        util.save_entry(title, content)
        return redirect('encyclopedia:entry', title=title)
    
    return render(request, "encyclopedia/new.html")

def edit_page(request, title):
    if request.method == "POST":
        content = request.POST.get("content", "")
        if content:
            util.save_entry(title, content)
            return redirect('encyclopedia:entry', title=title)
    
    content = util.get_entry(title)
    if content is None:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })

def random_page(request):
    entries = util.list_entries()
    if not entries:
        return redirect('encyclopedia:index')
    
    random_title = random.choice(entries)
    return redirect('encyclopedia:entry', title=random_title)

