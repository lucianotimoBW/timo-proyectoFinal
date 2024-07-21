from django.urls import reverse_lazy
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .models import Blog, Page, Message
from .forms import BlogForm, ChangePasswordForm, CustomUserCreationForm, PageForm, MessageForm, UserProfileForm

def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, 'blog_app/blog_list.html', {'blogs': blogs})

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    return render(request, 'blog_app/blog_detail.html', {'blog': blog})

@login_required
def blog_create(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('blog_detail', pk=blog.pk)
    else:
        form = BlogForm()
    return render(request, 'blog_app/blog_form.html', {'form': form})

@login_required
def blog_edit(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog_detail', pk=blog.pk)
    else:
        form = BlogForm(instance=blog)
    return render(request, 'blog_app/blog_form.html', {'form': form})

@login_required
def blog_delete(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        blog.delete()
        return redirect('blog_list')
    return render(request, 'blog_app/blog_confirm_delete.html', {'blog': blog})

def home(request):
    blogs = Blog.objects.all()
    return render(request, 'blog_app/home.html', {'blogs': blogs})

def about(request):
    return render(request, 'blog_app/about.html')

def custom_logout(request):
    logout(request)
    return redirect('home')

class CustomLoginView(LoginView):
    template_name = 'blog_app/login.html'
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=True)  # Commit user creation
            login(request, user)
            return redirect('profile')  # Redirect to the profile page after signup
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog_app/signup.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'blog_app/profile.html', {'user': request.user})

@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid():
            user_form.save()
            return redirect('profile')
    else:
        user_form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'blog_app/edit_profile.html', {'user_form': user_form})

@login_required
def change_password(request):
    if request.method == 'POST':
        password_form = PasswordChangeForm(user=request.user, data=request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in after password change
            return redirect('profile')
    else:
        password_form = PasswordChangeForm(user=request.user)
    
    return render(request, 'blog_app/change_password.html', {'password_form': password_form})


# List all pages
def page_list(request):
    pages = Page.objects.all()
    return render(request, 'blog_app/page_list.html', {'pages': pages})

# Detail view of a single page
def page_detail(request, pk):
    page = get_object_or_404(Page, pk=pk)
    return render(request, 'blog_app/page_detail.html', {'page': page})

# Create a new page
@login_required
def page_create(request):
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.author = request.user
            page.save()
            return redirect('page_detail', pk=page.pk)
    else:
        form = PageForm()
    return render(request, 'blog_app/page_form.html', {'form': form})

# Update an existing page
@login_required
def page_update(request, pk):
    page = get_object_or_404(Page, pk=pk)
    if request.method == 'POST':
        form = PageForm(request.POST, instance=page)
        if form.is_valid():
            page = form.save()
            return redirect('page_detail', pk=page.pk)
    else:
        form = PageForm(instance=page)
    return render(request, 'blog_app/page_form.html', {'form': form})

# Delete a page
@login_required
def page_delete(request, pk):
    page = get_object_or_404(Page, pk=pk)
    if request.method == 'POST':
        page.delete()
        return redirect('page_list')
    return render(request, 'blog_app/page_confirm_delete.html', {'page': page})

# List received messages
@login_required
def message_list(request):
    messages = request.user.received_messages.all()
    return render(request, 'blog_app/message_list.html', {'messages': messages})

# View a single message
@login_required
def message_detail(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.user != message.receiver:
        return redirect('message_list')
    return render(request, 'blog_app/message_detail.html', {'message': message})

# Send a new message
@login_required
def message_send(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('message_list')
    else:
        form = MessageForm()
    return render(request, 'blog_app/message_form.html', {'form': form})
