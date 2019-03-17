from django.urls import path

from django.views import generic

from twitter import views

app_name = 'twitter'
urlpatterns = [
    # path('', generic.TemplateView.as_view(template_name='twitter/index.html'),
    #      name='index'),
    path('', views.TweetListView.as_view(), name='index'),
    path('register/', views.RegisterView.as_view(),name='register'),
    path('compose/', views.ComposeView.as_view(), name='compose'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('user/<int:pk>/', views.AuthorDetailView.as_view(),name='author-detail'),
    path('tweet/<int:pk>/', views.TweetDetailView.as_view(), name='tweet-detail'),
    path('message/new', views.MessageFormView.as_view(), name='compose-message'),
    path('message/<int:pk>', views.MessageDetailView.as_view(), name='message-detail'),
    path('message/', views.MessageListView.as_view(), name='messages'),
]