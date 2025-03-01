from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

# Create your views here.
def index(request):
    return HttpResponse("Страница приложения cats.")

#def categories(request):
#    return HttpResponse(f"<h1>Статьи по категориям</h1>")

def categories(request, meme_id):
    return HttpResponse(f"<h1>Статьи по категориям</h1><p >id:{meme_id}</p>")

#def categories_by_slug(request, meme_slug):
#    return HttpResponse(f"<h1>Статьи по категориям</h1><p >slug:{ meme_slug }</p>")

def categories_by_slug(request, meme_slug):
    if request.GET:
        print(request.GET)
    return HttpResponse(f"<h1>Статьи по категориям</h1><p >slug: {meme_slug}</p>")

def archive(request, year):
    if year > 2025:
        url_redirect = reverse('memes', args=('Luna',))
        return HttpResponsePermanentRedirect(url_redirect)
    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
