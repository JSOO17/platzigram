"""Users Views"""

# Django
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, FormView, UpdateView, View
from django.contrib.auth import views as auth_views
from django.urls import reverse, reverse_lazy

# Forms
from users.forms import SignUpForm

# Models
from django.contrib.auth.models import User
from posts.models import Post
from users.models import Profile, Follows
from django.db.models import Count
from django.shortcuts import redirect

# Templates
TEMPLATE_LOGIN = 'users/login.html'
TEMPLATE_SIGNUP = 'users/signup.html'
TEMPLATE_UPDATE_PROFILE = 'users/update_profile.html'

# URLs
FEED = 'posts:feed'
LOGIN = 'users:login'
UPDATE_PROFILE = 'users:update'
UPDATE_DETAIL = 'users:detail'

# Constants
NAME_METHOD_POST = 'POST'
NAME_FIELD_USERNAME = 'username'
NAME_FIELD_PASSWORD = 'password'
NAME_FIELD_FIRST_NAME = 'first_name'
NAME_FIELD_LAST_NAME = 'last_name'
NAME_FIELD_EMAIL = 'email'
NAME_FIELD_WEBSITE = 'website'
NAME_FIELD_PHONE_NUMBER = 'phone_number'
NAME_FIELD_BIOGRAPHY = 'biography'
NAME_FIELD_PICTURE = 'picture'
NAME_FIELD_CONFIRMATION_PASSWORD = 'password_confirmation'

class LoginView(auth_views.LoginView):
    """Login View"""

    template_name = TEMPLATE_LOGIN


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):

    template_name = LOGIN

class LetFollowView(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        username = kwargs['username']
        u = User.objects.get(username=username)
        followed = Profile.objects.get(user=u)
        Follows.objects.get(followed=followed, follower=request.user.profile).delete()

        url = reverse(UPDATE_DETAIL, kwargs={
            'username': self.kwargs['username']
        })

        return redirect(url)

class FollowView(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        username = kwargs['username']
        u = User.objects.get(username=username)
        followed = Profile.objects.get(user=u)
        follows = Follows(followed=followed, follower=request.user.profile)
        follows.save()
    
        url = reverse(UPDATE_DETAIL, kwargs={
            'username': self.kwargs['username']
        })

        return redirect(url)

class SignupView(FormView):

    template_name = TEMPLATE_SIGNUP
    form_class = SignUpForm
    success_url = reverse_lazy(LOGIN)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class UpdateProfileView(LoginRequiredMixin, UpdateView):

    template_name = TEMPLATE_UPDATE_PROFILE
    model = Profile
    fields = ['website', 'biography', 'phone_number', 'picture']

    def get_object(self):
        return self.request.user.profile

    def get_success_url(self):
        username = self.object.user.username
        return reverse(UPDATE_DETAIL, kwargs={
            'username': username
        })

class UserDetailView(LoginRequiredMixin ,DetailView):
    template_name = 'users/detail.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    queryset = User.objects.annotate(number_of_posts=Count('post'))
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        """Add user's posts to context"""
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context["posts"] = Post.objects.filter(user=user).order_by('-modified')
        if self.request.user != user:
            context["follows"] = Follows.objects.filter(
                follower=self.request.user.profile,
                followed=user.profile
            ).first()

        return context
