from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404

from cats.models import Cats, Category, TagPost

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

def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Cats.Status.PUBLISHED)
    data = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }
    return render(request, 'cats/index.html',
                  context=data)

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
        'cat_selected': 0,

    }
    return render(request, 'cats/index.html',
                  context=data)

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

def show_category(request, cat_slug):
    category = get_object_or_404(Category,
                                 slug=cat_slug)
    posts = Cats.published.filter(cat_id=category.pk)
    data = {
        'title': f'Рубрика: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }
    return render(request, 'cats/index.html',
                  context=data)

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
