from django.shortcuts import render, redirect
from markdown2 import markdown
from django.http import HttpResponse
from random import choice

from .forms import PageForm

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def load_page(request, title):
    try:
        content = markdown(util.get_entry(title))
        return render(request, "encyclopedia/page.html", {
            "title": title,
            "content": content,
        })
    except TypeError:
        return render(request, "encyclopedia/page.html", {
        "title": title,
        "content": f'The page "{title}" was not found.',
    })
        # return HttpResponse(f'The page "{title}" was not found.')

def search(request):
    query = request.GET.get("q")
    entries = util.list_entries()

    if query in entries:
        return redirect(f"/wiki/{query}")

    results = [entry for entry in entries if query in entry]

    if not results:
        return HttpResponse(f"No search results for {query}")

    return render(request, "encyclopedia/search_results.html", {
                        "title": "Search Results",
                        "results": results,
                        })

def create_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/edit_page.html", {
                            "form": PageForm()
        })
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("textarea")
        util.save_entry(title, content)
        return redirect(f"/wiki/{title}")

def edit_page(request, title):
    if request.method == "GET":
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit_page.html", {
                            "form": PageForm(
                                initial={'title': title, 'textarea': content}
                                )
        })

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("textarea")
        util.save_entry(title, content)
        return render(request, "encyclopedia/page.html", {
            "title": title,
            "content": content,
        })

def random_page(request):
    """
    Renderize a encyclopedia page randomly.
    """
    pages = util.list_entries()
    title = choice(pages)
    
    return redirect(f"/wiki/{title}")
