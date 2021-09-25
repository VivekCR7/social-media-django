from django.shortcuts import (
    redirect,
    render,
    get_object_or_404,
    HttpResponseRedirect
)
from django.urls.base import reverse
from django.contrib.auth.decorators import login_required
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
    ordering = ['-date_posted']
    context_object_name = 'posts'
    
class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)

        stuff = get_object_or_404(Post,id = self.kwargs['pk'])
        total = stuff.total_likes()

        liked = False
        if stuff.like.filter(id = self.request.user.id).exists():
            liked = True

        context['total_likes'] = total
        context['liked']  = liked

        return context

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

    #check for the current user who is updating the post
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    #check for the current user who is deleting the post
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

@login_required
def Like(request, pk):
    post = get_object_or_404(Post,id = request.POST.get('post_id'))
    liked = False
    if post.like.filter(id = request.user.id).exists():
        post.like.remove(request.user)
        liked = False
    else:
        post.like.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))