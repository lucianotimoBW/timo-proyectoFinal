from .models import Blog, Page, Message
from .forms import BlogForm, CustomUserCreationForm, PageForm, MessageForm

from django.urls import reverse_lazy

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import redirect



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


# Use Django's built-in LoginView
class CustomLoginView(LoginView):
    template_name = 'blog_app/login.html'
    redirect_authenticated_user = True

# Use Django's built-in LogoutView
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
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
        user = request.user
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.save()
        return redirect('profile')
    return render(request, 'blog_app/update_profile.html')




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