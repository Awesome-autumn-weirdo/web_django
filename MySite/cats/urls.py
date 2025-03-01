from django.urls import path, re_path, register_converter
from cats import views, converters
register_converter(converters.FourDigitYearConverter,"year4")
urlpatterns = [
    path('', views.index,name='home'),
    path('memes/<int:meme_id>/', views.categories, name='memes'),
    path('memes/<slug:meme_slug>/', views.categories_by_slug,name='memes'),
    #re_path(r'^archive/(?P<year>[0-9]{4})/', views.archive),
    path('archive/<year4:year>/', views.archive,name='archive'),
]

