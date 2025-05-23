from django import template
from django.db.models import Count

import cats.views as views
from cats.models import Category, TagPost


register = template.Library()
menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]
@register.simple_tag
def get_menu():
    return menu

@register.simple_tag()
def get_categories():
    return views.cats_db

@register.inclusion_tag('cats/list_categories.html')
def show_categories(cat_selected_id=0):
    cats = Category.objects.annotate(total=Count("posts")).filter(total__gt=0)
    return {"cats": cats, "cat_selected": cat_selected_id}

@register.inclusion_tag('cats/list_tags.html')
def show_all_tags():
    return {"tags": TagPost.objects.annotate(total=Count("tags")).filter(total__gt=0)}