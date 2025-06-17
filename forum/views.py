from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Topic, Post
from .forms import TopicForm, PostForm
from django.contrib.auth.models import User

def home(request):
    categories = Category.objects.all()
    return render(request, 'forum/home.html', {'categories': categories})

def category_topics(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    topics = Topic.objects.filter(category=category)
    return render(request, 'forum/category_topics.html', {'category': category, 'topics': topics})

def topic_posts(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    posts = Post.objects.filter(topic=topic)
    return render(request, 'forum/topic_posts.html', {'topic': topic, 'posts': posts})

@login_required
def new_topic(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.category = category
            topic.author = request.user
            topic.save()
            return redirect('topic_posts', topic_id=topic.id)
    else:
        form = TopicForm()
    return render(request, 'forum/new_topic.html', {'form': form, 'category': category})

@login_required
def new_post(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.author = request.user
            post.save()
            return redirect('topic_posts', topic_id=topic.id)
    else:
        form = PostForm()
    return render(request, 'forum/new_post.html', {'form': form, 'topic': topic})

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import RegisterForm

class RegisterView(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

# ... существующие импорты и функции ...

@login_required
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    
    # Проверяем: пользователь — автор темы или админ
    if request.user == topic.author or request.user.is_superuser:
        topic.delete()
        return redirect('home')
    else:
        return redirect('topic_posts', topic_id=topic_id)


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Проверяем: пользователь — автор сообщения или админ
    if request.user == post.author or request.user.is_superuser:
        post.delete()
        return redirect('topic_posts', topic_id=post.topic.id)
    else:
        return redirect('topic_posts', topic_id=post.topic.id)

@login_required
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    
    # Теперь преподаватель тоже может удалять темы
    if request.user == topic.author or request.user.is_superuser or request.user.profile.role == 'teacher':
        topic.delete()
        return redirect('home')

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.user == post.author or request.user.is_superuser or request.user.profile.role == 'teacher':
        post.delete()
    return redirect('topic_posts', topic_id=post.topic.id)

@login_required
def teacher_page(request):
    if request.user.profile.role != 'teacher' and not request.user.is_superuser:
        return redirect('home')

    topics = Topic.objects.all()
    return render(request, 'forum/teacher_page.html', {'topics': topics})

@login_required
def edit_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    # Проверка прав
    if request.user != topic.author and not request.user.is_superuser and request.user.profile.role != 'teacher':
        return redirect('topic_posts', topic_id=topic.id)

    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return redirect('topic_posts', topic_id=topic.id)
    else:
        form = TopicForm(instance=topic)

    return render(request, 'forum/edit_topic.html', {'form': form, 'topic': topic})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Проверка прав
    if request.user != post.author and not request.user.is_superuser and request.user.profile.role != 'teacher':
        return redirect('topic_posts', topic_id=post.topic.id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('topic_posts', topic_id=post.topic.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'forum/edit_post.html', {'form': form, 'post': post})

from django.shortcuts import get_object_or_404
from .forms import ProfileForm

def profile_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    topics = Topic.objects.filter(author=user)
    posts = Post.objects.filter(author=user)
    return render(request, 'forum/profile_view.html', {
        'profile_user': user,
        'topics': topics,
        'posts': posts
    })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view', user_id=request.user.id)
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'forum/edit_profile.html', {'form': form})