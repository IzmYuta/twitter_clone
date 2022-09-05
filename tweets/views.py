from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, DeleteView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from django.shortcuts import get_object_or_404

from django.http import Http404, JsonResponse

from .forms import TweetForm
from .models import Tweet, Like

User = get_user_model()


class TweetCreateView(LoginRequiredMixin, CreateView):
    template_name = "tweets/tweet_create.html"
    form_class = TweetForm
    success_url = reverse_lazy("accounts:home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


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
            tweet_user = Tweet.objects.get(pk=self.kwargs["pk"]).user
            return current_user.pk == tweet_user.pk
        else:
            raise Http404


@login_required
@require_POST
def like_view(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk)
    Like.objects.get_or_create(tweet=tweet, user=request.user)
    liked = True

    context = {
        "tweet_id": tweet.id,
        "liked": liked,
        "count": tweet.like_set.count(),
    }

    return JsonResponse(context)


@login_required
@require_POST
def unlike_view(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk)
    if like := Like.objects.filter(tweet=tweet, user=request.user).select_related(
        "tweet", "user"
    ):
        like.delete()
    liked = False

    context = {
        "tweet_id": tweet.id,
        "liked": liked,
        "count": tweet.like_set.count(),
    }

    return JsonResponse(context)
