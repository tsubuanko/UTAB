from django.urls import path
from django.conf.urls.static import static
from . import views
from django.conf.urls.static import settings
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
        path('password_reset_form/',views.PasswordReset.as_view(),name='password_reset'),
    path('password_reset/done/',views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',views.PasswordResetConfirm.as_view(),name='password_reset_confirm'),
    path('reset/done/',views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('thread/', views.ThreadListView.as_view(), name='thread'),
    path('thread/<int:pk>/', views.post_list, name='post'),
    path('thread/add/', views.add_thread, name='thread_add'),
    path('user/<int:pk>/favorite_thread/', views.favorite_thread, name='favorite_thread'),
    path('thread/<int:pk>/add_favorite/', views.add_favorite, name='add_favorite'),
    path('thread/<int:pk>/remove_favorite/', views.remove_favorite, name='remove_favorite'),
    path('thread_list/<int:pk>/', views.ThreadListView_filter.as_view(), name='thread_filter'),
    path('faculty/', views.faculty_list, name='faculty'),
]
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)