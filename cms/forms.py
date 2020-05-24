from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from .models import Thread, Post

UserModel = get_user_model()


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.fields['username'].widget.attrs['class'] = 'input'
       self.fields['password'].widget.attrs['class'] = 'input'
       self.fields['username'].widget.attrs['placeholder'] = 'Name'
       self.fields['password'].widget.attrs['placeholder'] = 'Password'


class UserCreateForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'input'
        self.fields['username'].widget.attrs['placeholder'] = 'Name'
        self.fields['email'].widget.attrs['placeholder'] = 'xxx@g.ecc.u-tokyo.ac.jp'
        self.fields['password1'].widget.attrs['placeholder'] = 'at least 8 characters'
        self.fields['password2'].widget.attrs['placeholder'] = 'confirmation'

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ('username', 'first_name', 'last_name', 'email', 'twitter')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'input'


class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs['class']='form-control'


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ("subject","code","faculty")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].widget.attrs['class'] = 'input'
        self.fields['code'].widget.attrs['class'] = 'input'
        self.fields['faculty'].widget.attrs['class'] = 'select'
        

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("message",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'].widget.attrs['class'] = 'textarea'
        self.fields['message'].widget.attrs['placeholder'] = 'テキストを入力'

