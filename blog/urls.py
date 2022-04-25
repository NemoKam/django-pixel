from django.urls import path
from django.conf.urls import include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete , name='post_delete'),
    path('setcookie/' , views.setcookie , name='setcookie'),
    path('getcookie/' , views.getcookie , name='getcookie'),
    path('play/',views.play , name='play')
]
if settings.DEBUG:
        urlpatterns+=static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)   
urlpatterns += [
    path('', include('django.contrib.auth.urls')),
]