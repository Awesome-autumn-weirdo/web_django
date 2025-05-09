from django.urls import path, register_converter
from cats import views, converters
from django.contrib import admin

from cats.views import CatsCategory

register_converter(converters.FourDigitYearConverter,"year4")
urlpatterns = [
    path('', views.CatsHome.as_view(),name='home'),
    path('about/', views.about, name='about'),
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(),
         name='post'),
    path('category/<slug:cat_slug>/', CatsCategory.as_view(),
         name='category'),
    path('tag/<slug:tag_slug>/', views.show_tag_postlist,
         name='tag'),
    path('edit/<slug:slug>/', views.UpdatePage.as_view(),
         name='edit_page'),
    path('delete/<slug:slug>/', views.DeletePage.as_view(),
         name='delete_page'),

]

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Котофейник"
