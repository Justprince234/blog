from django.urls import path

from blog_app import views

app_name = 'blog_app'

urlpatterns = [
    path('category/<slug:slug>', views.blog_category, name='blog_category'),
    path('search/', views.search, name='search'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('', views.post_list, name='home'),
]