from django.urls import path

from django.views import generic

from twitter.views import AllTwiteerView

app_name = 'twitter'
urlpatterns = [
    # path('', generic.TemplateView.as_view(template_name='twitter/index.html'),
    #      name='index'),
    path('', AllTwiteerView.as_view(), name='index')
]