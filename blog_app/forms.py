from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Blog, Page, Message

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'subtitle', 'content', 'image']  # Include image field
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title', 'content']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'subject', 'body']

class UserProfileForm(UserChangeForm):
    password = None  # Hide the password field

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']