from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'memes'
urlpatterns = [
    path('', views.welcome_view, name='welcome'),
    path('top/', views.top_view, name='top'),
    path('main/', views.MainView.as_view(), name='main'),
    path('meme/add/', login_required(views.AddMemeView.as_view()), name='meme-add'),
    path('user/<int:user_id>/memes/', views.user_memes_view, name='user-memes'),
    path('meme/<int:meme_id>/', views.meme_details_view, name='detail'),
    path('meme/<int:meme_id>/like/<int:thumb_up>/', views.like_view, name='like')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
