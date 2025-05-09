from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
import uuid
from cats.forms import AddPostForm, UploadFileForm
from cats.models import Cats, Category, TagPost
from cats.utils import DataMixin

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
    contact_list = Cats.published.all()
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == "POST":
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
          # print(form.cleaned_data)
            form.save()
        return redirect('home')
    else:
        form = UploadFileForm()

    return render(request, 'cats/about.html',
                  {'page_obj': page_obj,'title': 'О сайте',
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

from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


class CatsHome(DataMixin,ListView):
    template_name = 'cats/index.html'
    context_object_name = 'posts'
    extra_context = {
        'title': 'Главная страница',
        'menu': menu,
        'cat_selected': 0,
    }

    def get_context_data(self, *, object_list=None,
                         **kwargs):
        return self.get_mixin_context(super().get_context_data(**kwargs),
                                      title = 'Главная страница',
                                      cat_selected = 0,)

    def get_queryset(self):
        return Cats.published.all().select_related('cat')


class CatsCategory(DataMixin,ListView):
    template_name = 'cats/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context,
                                      title='Категория- ' + cat.name,
                                      cat_selected = cat.id,)

    def get_queryset(self):
        return Cats.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')


class TagPostList(DataMixin, ListView):
    template_name = 'cats/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context,
                                      title='Тег: ' + tag.tag)

    def get_queryset(self):
         return Cats.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')


class ShowPost(DataMixin, DetailView):
    model = Cats
    template_name = 'cats/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context,
                                      title=context['post'])

    def get_object(self, queryset=None):
        return get_object_or_404(Cats.published,
                                 slug=self.kwargs[self.slug_url_kwarg])

from django.urls import reverse, reverse_lazy


class AddPage(DataMixin,CreateView):
    model = Cats
    template_name = 'cats/addpage.html'
    success_url = reverse_lazy('home')
    fields = ['title', 'slug', 'content', 'is_published',
              'cat']
    title_page = 'Добавление статьи'


class UpdatePage(DataMixin,UpdateView):
    model = Cats
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'cats/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'


class DeletePage(DataMixin,DeleteView):
    model = Cats
    template_name = 'cats/delete.html'
    success_url = reverse_lazy('home')
    context_object_name = 'post'
    title_page = 'Удаление статьи'

def contact(request):
    return HttpResponse("Обратная связь")

def login(request):
    return HttpResponse("Авторизация")


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
