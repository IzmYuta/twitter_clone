from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from tweets.models import Tweet

User = get_user_model()


class TestTweetCreateView(TestCase):
    def setUp(self):
        user = {
            "email": "test@example.com",
            "username": "test",
            "password1": "goodpass",
            "password2": "goodpass",
        }
        self.client.post(reverse("accounts:signup"), user)
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
        user = {
            "email": "test@example.com",
            "username": "test",
            "password1": "goodpass",
            "password2": "goodpass",
        }
        self.client.post(reverse("accounts:signup"), user)
        post = {"content": "hello"}
        self.client.post(reverse("tweets:create"), post)

    def test_success_get(self):
        tweet = Tweet.objects.get(content="hello")
        response = self.client.get(reverse("tweets:detail", kwargs={"pk": tweet.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(tweet, response.context["tweet"])


class TestTweetDeleteView(TestCase):
    def setUp(self):
        user1 = {
            "email": "test@example.com",
            "username": "test",
            "password1": "goodpass",
            "password2": "goodpass",
        }
        user2 = {
            "email": "test@example.com",
            "username": "second",
            "password1": "goodpass",
            "password2": "goodpass",
        }
        User.objects.create_user(user1["username"], user1["email"], user1["password1"])
        User.objects.create_user(user2["username"], user2["email"], user2["password1"])
        post = {"content": "hello"}
        user = User.objects.get(username=user1["username"])
        Tweet.objects.create(user=user, content=post["content"])

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
        self.client.login(username="second", password="goodpass")
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
