from distutils.log import Log
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, DeleteView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import BaseCreateView

from .forms import TweetForm
from .models import Tweet

User = get_user_model()


class TweetCreateView(LoginRequiredMixin, CreateView):
    template_name = "tweets/tweet_create.html"
    form_class = TweetForm

    # def form_valid(self, form):
    #     self.object = Tweet(user=self.request.user)
    #     # tweet = form.save(commit=False)  # 保存せずオブジェクト生成する
    #     # tweet.user = User.objects.get(id=self.kwargs["pk"])
    #     # tweet.save()
    #     self.object.save()
    #     return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = Tweet(user=self.request.user)
        return super(BaseCreateView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("tweets:detail", kwargs={"pk": self.object.pk})


class TweetDetailView(DetailView):
    template_name = "tweets/tweet_detail.html"
    model = Tweet
    context_object_name = "tweet"
