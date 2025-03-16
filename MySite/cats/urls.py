from django.urls import path, register_converter
from cats import views, converters
register_converter(converters.FourDigitYearConverter,"year4")
urlpatterns = [
    path('', views.index,name='home'),
    path('about/', views.about, name='about'),
    path('addpage/', views.addpage, name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('post/<int:post_id>/', views.show_post, name='post'),
    path('category/<int:cat_id>/', views.show_category, name='category'),
]

