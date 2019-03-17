from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView

from twitter import forms
from twitter.models import Tweet


class TweetListView(ListView):
    queryset = Tweet.objects.all().order_by('creation_date')
    template_name = 'twitter/index.html'
    #context_object_name = 'tweets'


# class TweetListView(View):
#
#     def get(self, request):
#         tweets = Tweet.objects.all().order_by('-creation_date')
#         return render(request, 'twitter/index.html', {'tweets': tweets})

class RegisterView(View):
    form_class = forms.UserRegisterForm
    template_name = 'twitter/register.html'

    def get(self, request):
        return render(request, 'twitter/register.html',
                      {'form': forms.UserRegisterForm()})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            return redirect('/')

        return render(request, self.template_name, {'form': form})


class ComposeView(LoginRequiredMixin, CreateView):
    model = Tweet
    form_class = forms.TweetForm
    success_url = reverse_lazy('twitter:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)