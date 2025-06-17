from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Главная страница — список категорий
    path('category/<int:category_id>/', views.category_topics, name='category_topics'),
    path('topic/<int:topic_id>/', views.topic_posts, name='topic_posts'),
    path('topic/new/<int:category_id>/', views.new_topic, name='new_topic'),
    path('post/new/<int:topic_id>/', views.new_post, name='new_post'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<int:category_id>/', views.category_topics, name='category_topics'),
    path('topic/<int:topic_id>/', views.topic_posts, name='topic_posts'),
    path('topic/new/<int:category_id>/', views.new_topic, name='new_topic'),
    path('post/new/<int:topic_id>/', views.new_post, name='new_post'),

    # Удаление
    path('topic/delete/<int:topic_id>/', views.delete_topic, name='delete_topic'),
    path('post/delete/<int:post_id>/', views.delete_post, name='delete_post'),

    # Редактирование
    path('topic/edit/<int:topic_id>/', views.edit_topic, name='edit_topic'),
    path('post/edit/<int:post_id>/', views.edit_post, name='edit_post'),


    path('teacher/', views.teacher_page, name='teacher_page'),

    path('profile/<int:user_id>/', views.profile_view, name='profile_view'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]