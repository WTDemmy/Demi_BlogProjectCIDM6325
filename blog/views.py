from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm


# -------------------
# Home
# -------------------
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'posts': posts})


# -------------------
# Authentication
# -------------------
def register(request):
    """User registration using Django's built-in UserCreationForm."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    """Profile page visible only to logged-in users."""
    return render(request, 'users/profile.html')

from django.contrib.auth import logout

def logout_view(request):
    """Log the user out and redirect to home with a message."""
    if request.method == "POST":
        logout(request)
        messages.success(request, "You’ve been logged out successfully 👋")
        return redirect('home')
    else:
        return redirect('home')


# -------------------
# Post Views (CRUD)
# -------------------
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author  # only author can edit


class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']  # newest first


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('post_list')  # where to go after delete

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author  # only author can delete

def about(request) -> None:
    """Render the about page."""
    return render(request, 'about.html')

def contact(request) -> None:
    """Render the contact page."""
    return render(request, 'contact.html')

"""
Tradeoff Notes:
- CBVs simplify CRUD logic and keep views consistent.
- Mixins like LoginRequiredMixin and UserPassesTestMixin restrict access.
- Registration and profile views add usability and security (role-based access).
"""
