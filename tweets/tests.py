from django.test import TestCase
from django.urls import reverse

from tweets.models import Tweet


class TestTweetCreateView(TestCase):
    def setUp(self):
        post = {
            "email": "test@example.com",
            "username": "test",
            "password1": "goodpass",
            "password2": "goodpass",
        }
        self.client.post(reverse("accounts:signup"), post)

    def test_success_get(self):
        response = self.client.get(reverse("tweets:create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tweets/tweet_create.html")

    def test_success_post(self):
        post = {"content": "hello"}
        response = self.client.post(reverse("tweets:create"), post)
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
        response = self.client.post(reverse("tweets:create"), post)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Tweet.objects.filter(content=post["content"]).exists())
        self.assertFormError(response, "form", "content", "このフィールドは必須です。")

    def test_failure_post_with_too_long_content(self):
        post = {
            "content": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        }
        response = self.client.post(reverse("tweets:create"), post)
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
        post = {
            "email": "test@example.com",
            "username": "test",
            "password1": "goodpass",
            "password2": "goodpass",
        }
        self.client.post(reverse("accounts:signup"), post)
        post = {"content": "hello"}
        self.client.post(reverse("tweets:create"), post)

    def test_success_get(self):
        tweet = Tweet.objects.get(content="hello")
        response = self.client.get(reverse("tweets:detail", kwargs={"pk": tweet.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(tweet, response.context["tweet"])


class TestTweetDeleteView(TestCase):
    def setUp(self):
        post = {
            "email": "test@example.com",
            "username": "test",
            "password1": "goodpass",
            "password2": "goodpass",
        }
        self.client.post(reverse("accounts:signup"), post)
        post = {"content": "hello"}
        self.client.post(reverse("tweets:create"), post)

    def test_success_post(self):
        tweet = Tweet.objects.get(content="hello")
        response = self.client.post(reverse("tweets:delete", kwargs={"pk": tweet.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Tweet.objects.filter(content="hello").exists())

    def test_failure_post_with_not_exist_tweet(self):
        response = self.client.post(reverse("tweets:delete", kwargs={"pk": 100}))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Tweet.objects.filter(content="hello").exists())

    def test_failure_post_with_incorrect_user(self):
        post2 = {
            "email": "test@example.com",
            "username": "second",
            "password1": "goodpass",
            "password2": "goodpass",
        }
        self.client.post(reverse("accounts:signup"), post2)
        tweet = Tweet.objects.get(content="hello")
        response = self.client.post(reverse("tweets:delete", kwargs={"pk": tweet.pk}))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Tweet.objects.filter(content="hello").exists())


class TestFavoriteView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_favorited_tweet(self):
        pass


class TestUnfavoriteView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_unfavorited_tweet(self):
        pass
