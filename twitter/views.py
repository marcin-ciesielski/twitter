from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.generic import ListView

from twitter import forms
from twitter.models import Tweet


class AllTwiteerView(ListView):
    template_name = 'twitter/index.html'
    context_object_name = 'tweets'

    def get_queryset(self):
        return Tweet.objects.all().order_by('creation_date')


class RegisterView(View):

    def get(self, request):
        return render(request, 'twitter/register.html',
                      {'form': forms.UserRegisterForm()})