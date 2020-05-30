from django.contrib.auth.base_user import (
    AbstractBaseUser, BaseUserManager,
)
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .image import delete_previous_file,get_image_path
from django import forms
class Thread(models.Model):
    faculty_list = (('前期教養学部','前期教養学部'),('後期教養学部','後期教養学部'),('法学部','法学部'),('経済学部','経済学部'),('文学部','文学部'),('教育学部','教育学部'),('理学部','理学部'),('工学部','工学部'),('農学部','農学部'),('薬学部','薬学部'),('医学部','医学部'),)

    subject = models.CharField(max_length=100)
    code = models.CharField(max_length=100, null=True)
    faculty = models.CharField(max_length=20, null=True, choices=faculty_list)

    def __str__(self):
        return self.subject


# User-related
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class AbstractUser(AbstractBaseUser, PermissionsMixin):

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    profile_picture=models.ImageField(upload_to='profile_picture',blank=True)
    #email = models.EmailField(_('email address'), unique=True)
    email = models.EmailField(_('email address'))

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    twitter = models.CharField(_('Twitter'), max_length=50, blank=True)

    favorite_thread = models.ManyToManyField(Thread, blank=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    PICTURE_FIELD='profile_picture'
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def __str__(self):
        return self.username

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class User(AbstractUser):
    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"


class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, null=True, related_name='threads')
    message = models.TextField(max_length=3000)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', null=True)
    def __str__(self):
        return self.message


class Image(models.Model):
    @delete_previous_file
    def save(self,force_insert=False,force_update=False,using=None,update_fields=None):
        super(Image,self).save()
    def delete(self,using=None,keep_parents=False):
        super(Image,self).delete()
    picture=models.ImageField(upload_to='profile_picture')
    title=models.CharField(max_length=200)
    def __str__(self):
        return self.title

class ImageForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(ImageForm,self).__init__(*args,**kwargs)
    class Meta:
        model=Image
        fields=('picture','title',)

class Profile(models.Model):
    name=models.CharField(max_length=50)
    picture=models.ImageField(upload_to='profile_picture')
    class Meta:
        db_table='profile'
