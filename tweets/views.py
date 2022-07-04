from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, DeleteView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import BaseCreateView
from django.http import Http404

from .forms import TweetForm
from .models import Tweet

User = get_user_model()


class TweetCreateView(LoginRequiredMixin, CreateView):
    template_name = "tweets/tweet_create.html"
    form_class = TweetForm

    def post(self, request, *args, **kwargs):
        self.object = Tweet(user=self.request.user)
        return super(BaseCreateView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("accounts:home")


class TweetDetailView(DetailView):
    template_name = "tweets/tweet_detail.html"
    model = Tweet
    context_object_name = "tweet"


class TweetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "tweets/tweet_delete.html"
    model = Tweet
    success_url = reverse_lazy("accounts:home")

    def test_func(self):
        if Tweet.objects.filter(pk=self.kwargs["pk"]).exists():
            current_user = self.request.user
            tweet_user = Tweet.objects.filter(pk=self.kwargs["pk"]).user
            return current_user.pk == tweet_user.pk
        else:
            raise Http404
