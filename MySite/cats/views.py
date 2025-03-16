from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

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

data_db = [
    {
        'id': 1,
        'title': 'Луна',
        'content': '''Луна (Crunchy Cat) – это кошка, ставшая интернет-мемом благодаря своему уникальному внешнему виду. 
Она известна своими постоянно прищуренными глазами и слегка недовольным выражением лица.

🐱 Основные факты:
- Полное имя: Луна
- Кличка в интернете: Crunchy Cat
- Порода: Домашняя короткошёрстная (предположительно)
- Цвет шерсти: Серо-белый
- Владелец: @awfulsummers (TikTok, Twitter)

📖 Как стала знаменитой?
Луна приобрела популярность в 2023 году после того, как её хозяин выложил фотографии и видео с ней в TikTok и Twitter. 
Её выражение лица выглядело так, будто она всегда разочарована и устала от жизни, что быстро сделало её мемом.

🎭 Мемы и влияние
- Луну сравнивают с офисными работниками, которые устали от работы.
- Её лицо используют в мемах про прокрастинацию, бессонницу и неудачные жизненные моменты.
- Она стала частью интернет-культуры, наряду с другими знаменитыми мем-котами, такими как Grumpy Cat и Cursed Cat.

🔥 Интересные факты
- Несмотря на "вечно недовольное" выражение, Луна – обычная ласковая домашняя кошка.
- Она часто "Crunchy" (хрустит), потому что её шерсть выглядит немного растрёпанной.
- Хозяин иногда выкладывает новые фото, и каждый раз они становятся вирусными.

Луна – очередное подтверждение того, что кошки – короли интернета. 🐈✨''',
        'is_published': True
    },
    {'id': 2, 'title': 'Кот Максвелл', 'content': 'Биография кота Максвелла', 'is_published': False},
    {'id': 3, 'title': 'Мистер Фреш', 'content': 'Биография Мистера Фреша', 'is_published': True},
]


class MyClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b

def index(request):
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': data_db,
        'cat_selected': 0,
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

def show_post(request, post_id):
    return HttpResponse(f"Отображение статьи с id = {post_id}")

def show_category(request, cat_id):
    data = {
        'title': 'Отображение по рубрикам',
        'menu': menu,
        'posts': data_db,
        'cat_selected': cat_id,
    }
    return render(request, 'cats/index.html',
                  context=data)

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
