from urllib import request

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView

from twitter import forms
from twitter.forms import TweetForm, AddCommentForm, MessageForm
from twitter.models import Tweet, Comment, Message


class TweetListView(ListView):
    def get(self, request):
        tweets = Tweet.objects.all().order_by('-creation_date')
        return render(request, 'twitter/index.html', {'tweets': tweets})


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        tweets = Tweet.objects.filter(author=request.user).order_by('-creation_date')
        return render(request,'twitter/profile.html', {'tweets': tweets})


class AuthorDetailView(View):
    def get(self, request, pk):
        tweets = Tweet.objects.filter(author=pk).order_by('-creation_date')
        return render(request, 'twitter/user_tweet.html', {'tweets': tweets})


class TweetDetailView(View):
    def get(self, request, pk):
        tweet = Tweet.objects.get(pk=pk)
        add_comment = AddCommentForm
        return render(request, 'twitter/tweet_detail.html', {'tweet': tweet, 'add_comment': add_comment})

    def post(self, request, pk):
        form = forms.AddCommentForm(request.POST)
        tweet = Tweet.objects.get(pk=pk)
        if form.is_valid():
            content = form.cleaned_data.get('content')
            new_comment = Comment(content=content, author=request.user, tweet=tweet)
            new_comment.save()
            form = forms.AddCommentForm()
        return render(request, 'twitter/tweet_detail.html', {'tweet': tweet, 'add_comment': form})


class MessageFormView(View):
    def get(self, request):
        form = MessageForm
        return render(request, 'twitter/message_form.html', {'form': form})

    def post(self, request):
        form = forms.MessageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            recipient = form.cleaned_data.get('recipient')
            new_message = Message(title=title, content=content, recipient=recipient, sender=request.user)
            new_message.save()
            form = forms.MessageForm()
        return render(request, 'twitter/message_form.html', {'form': form})


class MessageDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        query_set = Message.objects.filter(
            blocked=False).filter(
            Q(recipient=request.user) | Q(sender=request.user))
        msg = get_object_or_404(query_set, pk=pk)
        if msg.recipient.pk == request.user.pk:
            msg.read = True
            msg.save()
        return render(request, 'twitter/message_detail.html', {'msg': msg})


class MessageListView(LoginRequiredMixin, View):
    def get(self, request):
        received = Message.objects.filter(
            recipient=request.user, blocked=False).order_by('-date_send')
        sent = Message.objects.filter(
            sender=request.user, blocked=False).order_by('-date_send')
        return render(request, 'twitter/messages.html',
                      {'received': received, 'sent': sent})

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