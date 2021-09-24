from django.shortcuts import render
from .models import Post
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.

def home(request):
    context = {
        'posts':Post.objects.all()
    }
    return render(request,'post/home.html',context)

class PostListView(ListView):
    model = Post
    template_name = 'post/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    
class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['image','caption']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['image','caption']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    #check if the current user who is updating the post
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    #check if the current user who is deleting the post
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False