from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.index,name='index'),
    path('about/',views.about,name='about'),
    path('category/<slug:category_name_slug>/',views.show_category,name='show_category'),
    path('add_category/',views.add_category,name='add_category'),
    path('<category>/add_page/',views.add_page,name='add_page'),
]
