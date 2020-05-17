from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'cms'

urlpatterns = [
    path('', views.TopView.as_view(), name='top'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('signup/', views.UserCreate.as_view(), name='signup'),
    path('user/<int:pk>/update/', views.UserUpdate.as_view(), name='user_update'),
    path('user/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    path('user/', views.UserList.as_view(), name='user_list'),
    path('user/<int:pk>/delete/', views.UserDelete.as_view(), name='user_delete'),
    path('password_change/',views.PasswordChange.as_view(),name='password_change'),
    path('password_change/done/',views.PasswordChangeDone.as_view(),name='password_change_done'),
    path('thread/', views.ThreadListView.as_view(), name='thread'),
    path('thread/<int:pk>/', views.post_list, name='post'),
    path('thread/add/', views.add_thread, name='thread_add'),
<<<<<<< HEAD
    path("showall/",views.showall,name='showall'),
    path('upload/',views.upload,name='upload'),
]
#if settings.DEBUG:
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
=======
    path('user/<int:pk>/favorite_thread/', views.favorite_thread, name='favorite_thread'),
    path('thread/<int:pk>/add_favorite/', views.add_favorite, name='add_favorite'),
    path('thread/<int:pk>/remove_favorite/', views.remove_favorite, name='remove_favorite'),
]
>>>>>>> 16d6f5f408a1dbd370acba934706e4e4b8c70ec9
