from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
import uuid
from cats.forms import AddPostForm, UploadFileForm
from cats.models import Cats, Category, TagPost, UploadFiles

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
def handle_uploaded_file(f):
    name = f.name
    ext = ''
    if '.' in name:
        ext = name[name.rindex('.'):]
    name = name[:name.rindex('.')]
    suffix = str(uuid.uuid4())

    with (open(f"uploads/{name}_{suffix}{ext}", "wb+")
          as destination):
        for chunk in f.chunks(): destination.write(chunk)

def about(request):
    if request.method == "POST":
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
          # print(form.cleaned_data)
            form.save()
        return redirect('home')
    else:
        form = UploadFileForm()

    return render(request, 'cats/about.html',
                  {'title': 'О сайте',
                   'menu': menu, 'form': form})

def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
         form = AddPostForm()

    return render(request, 'cats/addpage.html',
                  {'title': 'Добавление статьи', 'menu': menu,
                   'form': form})

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
