from django import forms
from .models import Topic, Post

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, ROLE_CHOICES

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Роль")

    class Meta:
        model = User
        fields = ["username", "email", "role", "password1", "password2"]

from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']
