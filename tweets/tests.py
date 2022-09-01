from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from tweets.models import Tweet, Like

User = get_user_model()


class TestTweetCreateView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test", email="test@test.com", password="goodpass"
        )
        self.client.login(username="test", password="goodpass")
        self.url = reverse("tweets:create")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tweets/tweet_create.html")

    def test_success_post(self):
        post = {"content": "hello"}
        response = self.client.post(self.url, post)
        self.assertTrue(Tweet.objects.filter(content=post["content"]).exists())
        self.assertRedirects(
            response,
            reverse("accounts:home"),
            status_code=302,
            target_status_code=200,
            msg_prefix="",
            fetch_redirect_response=True,
        )

    def test_failure_post_with_empty_content(self):
        post = {"content": ""}
        response = self.client.post(self.url, post)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Tweet.objects.filter(content=post["content"]).exists())
        self.assertFormError(response, "form", "content", "このフィールドは必須です。")

    def test_failure_post_with_too_long_content(self):
        post = {"content": "a" * 141}
        response = self.client.post(self.url, post)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Tweet.objects.filter(content=post["content"]).exists())
        self.assertFormError(
            response,
            "form",
            "content",
            "この値は 140 文字以下でなければなりません( " + str(len(post["content"])) + " 文字になっています)。",
        )


class TestTweetDetailView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test", email="test@test.com", password="goodpass"
        )
        self.client.login(username="test", password="goodpass")
        post = {"content": "hello"}
        self.client.post(reverse("tweets:create"), post)

    def test_success_get(self):
        tweet = Tweet.objects.get(content="hello")
        response = self.client.get(reverse("tweets:detail", kwargs={"pk": tweet.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(tweet, response.context["tweet"])


class TestTweetDeleteView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test", email="test@test.com", password="goodpass"
        )
        self.user2 = User.objects.create_user(
            username="test2", email="test2@test.com", password="goodpass"
        )
        post = {"content": "hello"}
        Tweet.objects.create(user=self.user, content=post["content"])

    def test_success_post(self):
        self.client.login(username="test", password="goodpass")
        tweet = Tweet.objects.get(content="hello")
        response = self.client.post(reverse("tweets:delete", kwargs={"pk": tweet.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Tweet.objects.filter(content="hello").exists())

    def test_failure_post_with_not_exist_tweet(self):
        self.client.login(username="test", password="goodpass")
        response = self.client.post(reverse("tweets:delete", kwargs={"pk": 100}))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Tweet.objects.filter(content="hello").exists())

    def test_failure_post_with_incorrect_user(self):
        self.client.login(username="test2", password="goodpass")
        tweet = Tweet.objects.get(content="hello")
        response = self.client.post(reverse("tweets:delete", kwargs={"pk": tweet.pk}))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Tweet.objects.filter(content="hello").exists())


class TestFavoriteView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test", email="test@test.com", password="goodpass"
        )
        self.client.login(username="test", password="goodpass")
        post = {"content": "hello"}
        self.client.post(reverse("tweets:create"), post)
        self.tweet = Tweet.objects.get(content="hello")

    def test_success_post(self):
        response = self.client.post(reverse("tweets:like", kwargs={"pk": self.tweet.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Like.objects.filter(tweet=self.tweet).exists())

    def test_failure_post_with_not_exist_tweet(self):
        response = self.client.post(reverse("tweets:like", kwargs={"pk": 100}))
        self.assertEqual(response.status_code, 404)
        self.assertFalse(Like.objects.filter(tweet=self.tweet).exists())

    def test_failure_post_with_favorited_tweet(self):
        # 「いいね済み」のツイートに「いいね」すると「いいね解除」するように設計したので実施しない
        pass


class TestUnfavoriteView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test", email="test@test.com", password="goodpass"
        )
        self.client.login(username="test", password="goodpass")
        post = {"content": "hello"}
        self.client.post(reverse("tweets:create"), post)
        self.tweet = Tweet.objects.get(content="hello")
        self.client.post(reverse("tweets:like", kwargs={"pk": self.tweet.pk}))

    def test_success_post(self):
        response = self.client.post(reverse("tweets:unlike", kwargs={"pk": self.tweet.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Like.objects.filter(tweet=self.tweet).exists())

    def test_failure_post_with_not_exist_tweet(self):
        response = self.client.post(reverse("tweets:unlike", kwargs={"pk": 100}))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Like.objects.filter(tweet=self.tweet).exists())

    def test_failure_post_with_unfavorited_tweet(self):
        # 「いいね済み」のツイートに「いいね」すると「いいね解除」するように設計したので(いいね解除に該当する操作がないので)実施しない
        pass
