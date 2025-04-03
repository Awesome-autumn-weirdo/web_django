from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404

from cats.models import Cats

menu = [{'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить статью", 'url_name': 'add_page'},
    {'title': "Обратная связь", 'url_name': 'contact'},
    {'title': "Войти", 'url_name': 'login'}
]

cats_db = [
{'id': 1, 'name': 'Ждут хозяина'},
{'id': 2, 'name': 'Нашли хозяина'},
{'id': 3, 'name': 'Мемные коты'},
]

class MyClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b

def index(request):
    posts = Cats.published.all()
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,

    }
    return render(request, 'cats/index.html', context=data)

def about(request):
    return render(request, 'cats/about.html',{'title': 'О сайте', 'menu': menu})

def addpage(request):
    return HttpResponse("Добавление статьи")

def contact(request):
    return HttpResponse("Обратная связь")

def login(request):
    return HttpResponse("Авторизация")

def show_post(request, post_slug):
    post = get_object_or_404(Cats, slug=post_slug)
    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }
    return render(request, 'cats/post.html',
                  context=data)

def show_category(request, cat_id):
    data = {
        'title': 'Отображение по рубрикам',
        'menu': menu,
        'posts': Cats.published.all(),
        'cat_selected': cat_id,
    }
    return render(request, 'cats/index.html',
                  context=data)

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
