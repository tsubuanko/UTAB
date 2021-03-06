from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView,PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView,
)
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url, redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView,
)
from django.db.models import Q
from django.views.generic import ListView
from functools import reduce
from operator import and_
from .mixins import OnlyYouMixin
from .forms import (
    LoginForm, UserCreateForm, UserUpdateForm, MyPasswordChangeForm, ThreadForm, PostForm, 
)
from .models import Thread, Post, Document 



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
            # email=form.cleaned_data['email'],
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


class PasswordReset(PasswordResetView):
    #subject_template_name='cms/templates/mail_template/subject.txt'
    success_url=reverse_lazy('cms:password_reset_done')
    #email_template_name='cms/password_reset_email.txt'
    template_name='registration/password_reset_form.html'

class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    success_url=reverse_lazy('cms:password_reset_complete')
    template_name='registration/password_reset_confirm.html'


class ThreadListView(ListView):
    model = Thread
    template_name = "cms/thread.html"


def post_list(request, pk):
    per_page = 10

    thread = get_object_or_404(Thread,pk=pk)
    post_list = Post.objects.filter(thread=thread)
    post_list = post_list[::-1]
    form = PostForm(request.POST or None)
    user = request.user
    favorite_list = user.favorite_thread.all()
    favorite_flag = True if thread in favorite_list else False

    if form.is_valid():
        post = form.save(commit=False)
        post.thread = thread
        post.created_by = user
        post.save()
        return redirect('cms:post', pk=thread.pk)

    context = {'form': form, 'post_list': post_list, 'thread': thread, 'favorite_flag': favorite_flag}
    return render(request, 'cms/post.html', context)


def add_thread(request):
    form = ThreadForm(request.POST or None)

    if form.is_valid():
        thread = form.save()
        #thread.save()
        return redirect('cms:faculty')

    context = {'form': form,}
    return render(request, 'cms/thread_add.html', context)


def favorite_thread(request, pk):
    user = request.user
    thread_list = user.favorite_thread.all()
    context = {'thread_list': thread_list, 'user': user}
    return render(request, 'cms/favorite_thread.html', context)


def add_favorite(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    user = request.user
    user.favorite_thread.add(thread)
    user.save()
    return redirect('cms:post', pk=thread.pk)


def remove_favorite(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    user = request.user
    user.favorite_thread.remove(thread)
    user.save()
    return redirect('cms:post', pk=thread.pk)


class ThreadListView_filter(ListView):
    model = Thread
    template_name = "cms/thread_list.html"
    def get_context_data(self, **kwargs):
        faculty_id=self.kwargs['pk']
        faculty_dic={1:'前期教養学部',2:'後期教養学部',3:'法学部',4:'経済学部',5:'文学部',6:'教育学部',7:'理学部',8:'工学部',9:'農学部',10:'薬学部',11:'医学部'}
        faculty=faculty_dic[faculty_id]
        context = super().get_context_data(**kwargs)
        context['faculty'] = faculty
        context['query']=self.request.GET.get('q','')
        """👆検索ワード(列)を取得"""
        return context
    """検索を実行(スレッド名と授業コード両方で検索かけてます)"""
    def get_queryset(self):
        word_set=self.request.GET.get('q','')
        params=self.parse_search_params(word_set)
        #print(f"params={params}")
        if params==[]:
            return Thread.objects.all()
        else:
            query=reduce(
                lambda x,y:x&y,
                list(map(lambda z:Q(subject__icontains=z)|Q(code__icontains=z),params))
            )
            return Thread.objects.filter(query)

    """検索ワード(列)を整形してlistにする"""
    def parse_search_params(self,words:str):
        search_words=words.replace('　', ' ').split()
        for i in range(len(search_words)):
            search_words[i]=search_words[i].strip(' ')
        return search_words
        

def faculty_list(request):
    return render(request, 'cms/faculty.html')

"""FileUpload"""
class DocumentCreateView(CreateView):
    model=Document
    fields=['upload',]
    success_url=reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        documents=Document.objects.all()
        context['documents']=documents
        return context
