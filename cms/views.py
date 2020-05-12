from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import (
    LoginView, LogoutView,
)
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url, redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import (
    CreateView, UpdateView,
)
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView,
)

from .mixins import OnlyYouMixin
from .forms import (
    LoginForm, UserCreateForm, UserUpdateForm, ThreadForm, PostForm
)
from .models import Thread, Post



UserModel = get_user_model()

class TopView(TemplateView):
    template_name = 'cms/top.html'


class Login(LoginView):
    form_class = LoginForm
    template_name = 'cms/login.html'


class Logout(LogoutView):
    pass


class UserCreate(CreateView):
    form_class = UserCreateForm
    template_name = 'cms/signup.html'
    success_url = reverse_lazy('cms:top')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user
        return HttpResponseRedirect(self.get_success_url())


class UserUpdate(OnlyYouMixin, UpdateView):
    model = UserModel
    form_class = UserUpdateForm
    template_name = 'cms/user_update.html'

    def get_success_url(self):
        return resolve_url('cms:user_detail', pk=self.kwargs['pk'])


class UserDetail(DetailView):
    model = UserModel
    template_name = 'cms/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context


class UserList(ListView):
    model = UserModel
    template_name = 'cms/user_list.html'


class UserDelete(OnlyYouMixin, DeleteView):
    model = UserModel
    template_name = 'cms/user_delete.html'
    success_url = reverse_lazy('cms:top')


class ThreadListView(ListView):
    model = Thread    # Thread.objects.all()を裏側でやってくれてる
    template_name = "cms/thread.html"

def post_list(request, pk):
    per_page = 10

    thread = get_object_or_404(Thread,pk=pk)
    post_list= Post.objects.filter(thread=thread)
    form = PostForm(request.POST or None)

    if form.is_valid():
        post = form.save(commit=False)
        post.thread = thread
        post.save()
        return redirect('cms:post', pk=thread.pk)

    context = {'form': form, 'post_list': post_list}
    return render(request, 'cms/post.html', context)