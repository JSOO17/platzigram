"""Posts views!"""

# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, View
from django.urls import reverse, reverse_lazy

# Forms
from posts.forms import PostForm

# Models
from posts.models import Like, Post
from django.shortcuts import redirect


# URLs
FEED = 'posts:feed'

# Templates
TEMPLATE_FEED = 'posts/feed.html'
TEMPLATE_NEW_POST = 'posts/new.html'
TEMPLATE_DETAIL = 'posts/detail.html'

# Constants
NAME_METHOD_POST = 'POST'


class PostFeedView(LoginRequiredMixin, ListView):

    template_name = TEMPLATE_FEED
    model = Post
    ordering = ('-created',)
    paginate_by = 30
    context_object_name = 'posts'

class PostDetailView(LoginRequiredMixin, DetailView):
    template_name = TEMPLATE_DETAIL
    queryset = Post.objects.all()
    context_object_name = 'post'

class CreatePostView(LoginRequiredMixin, CreateView):
    """Create a new post"""

    template_name = TEMPLATE_NEW_POST
    form_class = PostForm
    success_url = reverse_lazy(FEED)

    def get_context_data(self, **kwargs):
        """Add user and profile to context"""
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["profile"] = self.request.user.profile
        return context
    
class LikeView(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        post = Post.objects.get(pk=pk)
        like = Like(post=post, profile=request.user.profile)
        like.save()
    
        url = reverse(request.path, kwargs={
            'username': self.kwargs['username']
        })

        return redirect(url)