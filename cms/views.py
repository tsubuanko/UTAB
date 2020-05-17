from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
)
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url, redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView,
)

from .mixins import OnlyYouMixin
from .forms import (
    LoginForm, UserCreateForm, UserUpdateForm, MyPasswordChangeForm, ThreadForm, PostForm,
)
from .models import Thread, Post, Image, ImageForm



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
        print(self.request.POST['next'])
        if self.request.POST['next']=='back':
            return render(self.request,'cms/signup.html',{'form':form})
        elif self.request.POST['next']=='confirm':
            return render(self.request,'cms/signup_confirm.html',{'form':form})
        elif self.request.POST['next']=='regist':
            form.save()
            user = form.save()
            user=authenticate(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password1'],
            )
            login(self.request, user)
            return super().form_valid(form)
        else:
            return HttpResponseRedirect(self.get_success_url())


class signup_confirm(CreateView):
    form_class = UserCreateForm
    template_name = 'cms/signup_confirm.html'


class UserUpdate(OnlyYouMixin, UpdateView):
    model = UserModel
    form_class = UserUpdateForm
    template_name = 'cms/user_update.html'

    def get_success_url(self):
        return resolve_url('cms:user_detail', pk=self.kwargs['pk'])


class OnlyYouMixin(UserPassesTestMixin):
    raise_exception=True

    def test_func(self):
        user=self.request.user
        return user.pk==self.kwargs['pk'] or user.is_superuser


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


class PasswordChange(PasswordChangeView):
    form_class=MyPasswordChangeForm
    success_url=reverse_lazy('cms:password_change_done')
    template_name='cms/password_change_form.html'


class PasswordChangeDone(PasswordChangeDoneView):
    """パスワードを変更しました"""
    template_name='cms/password_change_done.html'


class ThreadListView(ListView):
    model = Thread
    template_name = "cms/thread.html"


def post_list(request, pk):
    per_page = 10

    thread = get_object_or_404(Thread,pk=pk)
    post_list= Post.objects.filter(thread=thread)
    form = PostForm(request.POST or None)

    if form.is_valid():
        post = form.save(commit=False)
        post.thread = thread
        post.created_by = request.user
        post.save()
        return redirect('cms:post', pk=thread.pk)

    context = {'form': form, 'post_list': post_list}
    return render(request, 'cms/post.html', context)


def add_thread(request):
    form = ThreadForm(request.POST or None)

    if form.is_valid():
        thread = form.save()
        #thread.save()
        return redirect('cms:thread')

    context = {'form': form,}
    return render(request, 'cms/thread_add.html', context)


def showall(request):
    images=Image.objects.all()
    context={'Images':images}
    return render(request,'cms/showall.html',context)

def upload(request):
    #if request.method=='POST':
        form=ImageForm(request.POST,request.FILES)
        if form.is_valid():
            image=form.save()
            image_gen=request.FILES['picture']
            return redirect("cms:showall")
        else:
            form=ImageForm()
        context={'form':form}
        return render(request,'cms/upload.html',context)