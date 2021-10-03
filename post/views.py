from post.forms import CommentForm
from django.shortcuts import (
    redirect,
    render,
    get_object_or_404,
    HttpResponseRedirect
)
from django.urls.base import reverse
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'post/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'post/home.html'
    ordering = ['-date_posted']
    context_object_name = 'posts'


@login_required
def PostDetailView(request, pk):
    post = get_object_or_404(Post, id=pk)

    # get_the_likes
    total = post.total_likes()
    liked = False
    if post.like.filter(id=request.user.id).exists():
        liked = True

    # list of active comments
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()

            return redirect(post.get_absolute_url() + "#" + str(new_comment.id))
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'total_likes': total,
        'liked': liked,
    }
    return render(request, 'post/post_detail.html', context)

# handle reply


def reply_page(request):
    if request.method == "POST":

        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = request.POST.get('post_id')
            parent_id = request.POST.get('parent')
            post_url = request.POST.get('post_url')

            reply = form.save(commit=False)
            reply.author = request.user
            reply.post = Post(id=post_id)
            reply.parent = Comment(id=parent_id)
            reply.save()

            return redirect(post_url+"#"+str(reply.id))

    return redirect("/")


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['image', 'video', 'caption']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['image', 'video', 'caption']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # check for the current user who is updating the post
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    # check for the current user who is deleting the post
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def CommentDeleteView(request,pk):
    comment = Comment.objects.get(id = pk)
    post_id = comment.post.id
    comment.delete()
    return redirect(reverse('post-detail', args=[post_id]))


@login_required
def Like(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.like.filter(id=request.user.id).exists():
        post.like.remove(request.user)
        liked = False
    else:
        post.like.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))
