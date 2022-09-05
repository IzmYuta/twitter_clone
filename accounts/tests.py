from django.contrib.auth import get_user_model, SESSION_KEY
from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages

from mysite import settings
from tweets.models import Tweet
from .models import FriendShip, Profile

User = get_user_model()


class TestSignUpView(TestCase):
    def test_success_get(self):
        response = self.client.get(reverse("accounts:signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/signup.html")

    def test_success_post(self):
        user = {
            "email": "test@example.com",
            "username": "test",
            "password1": "goodpass",
            "password2": "goodpass",
        }
        response = self.client.post(reverse("accounts:signup"), user)
        self.assertTrue(
            User.objects.filter(username="test", email="test@example.com").exists()
        )
        self.assertRedirects(
            response,
            reverse("accounts:home"),
            status_code=302,
            target_status_code=200,
            msg_prefix="",
            fetch_redirect_response=True,
        )
        self.assertIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_empty_form(self):
        user = {
            "email": "",
            "username": "",
            "password1": "",
            "password2": "",
        }
        response = self.client.post(reverse("accounts:signup"), user)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=" ", email=" ").exists())
        self.assertFormError(response, "form", "email", "このフィールドは必須です。")
        self.assertFormError(response, "form", "username", "このフィールドは必須です。")
        self.assertFormError(response, "form", "password1", "このフィールドは必須です。")
        self.assertFormError(response, "form", "password2", "このフィールドは必須です。")

    def test_failure_post_with_empty_username(self):
        user = {
            "email": "test@example.com",
            "username": "",
            "password1": "goodpass",
            "password2": "goodpass",
        }
        response = self.client.post(reverse("accounts:signup"), user)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            User.objects.filter(username=" ", email="test@example.com").exists()
        )
        self.assertFormError(response, "form", "username", "このフィールドは必須です。")

    def test_failure_post_with_empty_email(self):
        user = {
            "email": "",
            "username": "test",
            "password1": "goodpass",
            "password2": "goodpass",
        }
        response = self.client.post(reverse("accounts:signup"), user)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="test", email=" ").exists())
        self.assertFormError(response, "form", "email", "このフィールドは必須です。")

    def test_failure_post_with_empty_password(self):
        user = {
            "email": "test@example.com",
            "username": "test",
            "password1": "",
            "password2": "",
        }
        response = self.client.post(reverse("accounts:signup"), user)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            User.objects.filter(username="test", email="test@example.com").exists()
        )
        self.assertFormError(response, "form", "password1", "このフィールドは必須です。")
        self.assertFormError(response, "form", "password2", "このフィールドは必須です。")

    def test_failure_post_with_duplicated_user(self):
        user1 = {
            "email": "test1@example.com",
            "username": "test",
            "password1": "goodpass",
            "password2": "goodpass",
        }
        user2 = {
            "email": "test2@example.com",
            "username": "test",
            "password1": "goodpass",
            "password2": "goodpass",
        }
        self.client.post(reverse("accounts:signup"), user1)
        response = self.client.post(reverse("accounts:signup"), user2)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            User.objects.filter(username="test", email="test2@example.com").exists()
        )
        self.assertFormError(response, "form", "username", "同じユーザー名が既に登録済みです。")

    def test_failure_post_with_invalid_email(self):
        user = {
            "email": "test.boo",
            "username": "test",
            "password1": "goodpass",
            "password2": "goodpass",
        }
        response = self.client.post(reverse("accounts:signup"), user)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            User.objects.filter(username="test", email="test.boo").exists()
        )
        self.assertFormError(response, "form", "email", "有効なメールアドレスを入力してください。")

    def test_failure_post_with_too_short_password(self):
        user = {
            "email": "test@example.com",
            "username": "test",
            "password1": "pass",
            "password2": "pass",
        }
        response = self.client.post(reverse("accounts:signup"), user)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            User.objects.filter(username="test", email="test@example.com").exists()
        )
        self.assertFormError(
            response, "form", "password2", "このパスワードは短すぎます。最低 8 文字以上必要です。"
        )

    def test_failure_post_with_password_similar_to_username(self):
        user = {
            "email": "test@example.com",
            "username": "goodpass",
            "password1": "goodpass",
            "password2": "goodpass",
        }
        response = self.client.post(reverse("accounts:signup"), user)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            User.objects.filter(username="test", email="test@example.com").exists()
        )
        self.assertFormError(response, "form", "password2", "このパスワードは ユーザー名 と似すぎています。")

    def test_failure_post_with_only_numbers_password(self):
        user = {
            "email": "test@example.com",
            "username": "test",
            "password1": "12345678",
            "password2": "12345678",
        }
        response = self.client.post(reverse("accounts:signup"), user)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            User.objects.filter(username="test", email="test@example.com").exists()
        )
        self.assertFormError(
            response, "form", "password2", "このパスワードは一般的すぎます。", "このパスワードは数字しか使われていません。"
        )

    def test_failure_post_with_mismatch_password(self):
        user = {
            "email": "test@example.com",
            "username": "test",
            "password1": "goodpass",
            "password2": "goodpath",
        }
        response = self.client.post(reverse("accounts:signup"), user)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            User.objects.filter(username="test", email="test@example.com").exists()
        )
        self.assertFormError(response, "form", "password2", "確認用パスワードが一致しません。")


class TestHomeView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test", email="test@test.com", password="goodpass"
        )
        self.client.login(username="test", password="goodpass")
        post = {"content": "hello"}
        post2 = {"content": "sorry"}
        self.client.post(reverse("tweets:create"), post)
        self.client.post(reverse("tweets:create"), post2)

    def test_success_get(self):
        response = self.client.get(reverse("accounts:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/home.html")
        self.assertQuerysetEqual(
            response.context["tweets"], Tweet.objects.order_by("-created_at")
        )


class TestLoginView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test", email="test@test.com", password="goodpass"
        )

    def test_success_get(self):
        response = self.client.get(reverse("accounts:signin"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/signin.html")

    def test_success_post(self):
        signinPost = {
            "username": "test",
            "password": "goodpass",
        }
        response = self.client.post(reverse("accounts:signin"), signinPost)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse(settings.LOGIN_REDIRECT_URL),
            status_code=302,
            target_status_code=200,
            msg_prefix="",
            fetch_redirect_response=True,
        )
        self.assertIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_not_exists_user(self):
        signinPost = {
            "username": "te",
            "password": "goodpass",
        }
        response = self.client.post(reverse("accounts:signin"), signinPost)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, "form", "", "正しいユーザー名とパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。"
        )
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_empty_password(self):
        signinPost = {
            "username": "test",
            "password": "",
        }
        response = self.client.post(reverse("accounts:signin"), signinPost)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", "password", "このフィールドは必須です。")
        self.assertNotIn(SESSION_KEY, self.client.session)


class TestLogoutView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test", email="test@test.com", password="goodpass"
        )
        self.client.login(username="test", password="goodpass")

    def test_success_get(self):
        response = self.client.get(reverse("accounts:signout"))
        self.assertRedirects(
            response,
            reverse(settings.LOGOUT_REDIRECT_URL),
            status_code=302,
            target_status_code=200,
        )
        self.assertNotIn(SESSION_KEY, self.client.session)


class TestUserProfileView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test", email="test@test.com", password="goodpass"
        )
        self.user2 = User.objects.create_user(
            username="test2", email="test2@test.com", password="goodpass"
        )
        self.client.login(username="test", password="goodpass")
        post = {"content": "hello"}
        post2 = {"content": "sorry"}
        self.client.post(reverse("tweets:create"), post)
        self.client.post(reverse("tweets:create"), post2)
        FriendShip.objects.create(following=self.user, followed=self.user2)
        FriendShip.objects.create(following=self.user2, followed=self.user)

    def test_success_get(self):
        response = self.client.get(
            reverse("accounts:user_profile", kwargs={"pk": self.user.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/profile.html")
        self.assertQuerysetEqual(
            response.context["tweets"],
            Tweet.objects.filter(user=self.user).order_by("-created_at"),
        )
        self.assertEqual(
            response.context["followings_num"],
            FriendShip.objects.select_related("following", "followed")
            .filter(following=self.user)
            .count(),
        )
        self.assertEqual(
            response.context["followers_num"],
            FriendShip.objects.select_related("following", "followed")
            .filter(following=self.user)
            .count(),
        )

    def test_failure_get_with_not_exists_user(self):
        response = self.client.get(reverse("accounts:user_profile", kwargs={"pk": 100}))
        self.assertEqual(response.status_code, 404)


class TestUserProfileEditView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test", email="test@test.com", password="goodpass"
        )
        self.client.login(username="test", password="goodpass")
        self.editPost = {
            "gender": 3,
            "self_intro": "よろしく",
        }

    def test_success_get(self):
        response = self.client.get(
            reverse("accounts:user_profile_edit", kwargs={"pk": self.user.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/profile_edit.html")

    def test_success_post(self):
        response = self.client.post(
            reverse("accounts:user_profile_edit", kwargs={"pk": self.user.pk}),
            self.editPost,
        )
        self.assertRedirects(
            response,
            reverse("accounts:user_profile", kwargs={"pk": self.user.pk}),
            status_code=302,
            target_status_code=200,
        )
        self.assertTrue(Profile.objects.filter(gender=3).exists())

    def test_failure_post_with_not_exists_user(self):
        response = self.client.post(
            reverse("accounts:user_profile_edit", kwargs={"pk": 100}), self.editPost
        )
        self.assertEqual(response.status_code, 404)
        self.assertFalse(Profile.objects.filter(gender=3).exists())

    def test_failure_post_with_incorrect_user(self):
        user2 = User.objects.create_user(
            username="test2", email="test2@test.com", password="goodpass"
        )
        response = self.client.post(
            reverse("accounts:user_profile_edit", kwargs={"pk": user2.pk}),
            self.editPost,
        )
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Profile.objects.filter(gender=3).exists())


class TestFollowView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test", email="test@test.com", password="goodpass"
        )
        self.user2 = User.objects.create_user(
            username="test2", email="test2@test.com", password="goodpass"
        )
        self.client.login(username="test", password="goodpass")

    def test_success_post(self):
        response = self.client.post(
            reverse("accounts:follow", kwargs={"username": "test2"}), None
        )
        self.assertRedirects(
            response,
            reverse("accounts:home"),
            status_code=302,
            target_status_code=200,
            msg_prefix="",
            fetch_redirect_response=True,
        )
        self.assertTrue(FriendShip.objects.filter(followed=self.user2).exists())

    def test_failure_post_with_not_exist_user(self):
        response = self.client.post(
            reverse("accounts:follow", kwargs={"username": "third"}), None
        )
        self.assertEqual(response.status_code, 404)
        self.assertFalse(FriendShip.objects.filter(followed=self.user2).exists())
        messages = list(get_messages(response.wsgi_request))
        message = str(messages[0])
        self.assertEqual(message, "存在しないユーザーです。")

    def test_failure_post_with_self(self):
        response = self.client.post(
            reverse("accounts:follow", kwargs={"username": "test"}), None
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(FriendShip.objects.filter(following=self.user).exists())
        messages = list(get_messages(response.wsgi_request))
        message = str(messages[0])
        self.assertEqual(message, "自分自身はフォローできません。")

    def test_failure_post_with_already_followed_user(self):
        FriendShip.objects.create(following=self.user, followed=self.user2)
        response = self.client.post(
            reverse("accounts:follow", kwargs={"username": "test2"}), None
        )
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        message = str(messages[0])
        self.assertEqual(message, "すでにフォローしています。")


class TestUnfollowView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test", email="test@test.com", password="goodpass"
        )
        self.user2 = User.objects.create_user(
            username="test2", email="test2@test.com", password="goodpass"
        )
        self.client.login(username="test", password="goodpass")
        FriendShip.objects.create(following=self.user, followed=self.user2)

    def test_success_post(self):
        response = self.client.post(
            reverse("accounts:unfollow", kwargs={"username": "test2"}), None
        )
        self.assertRedirects(
            response,
            reverse("accounts:home"),
            status_code=302,
            target_status_code=200,
            msg_prefix="",
            fetch_redirect_response=True,
        )
        self.assertFalse(FriendShip.objects.filter(followed=self.user2).exists())

    def test_failure_post_with_not_exist_user(self):
        response = self.client.post(
            reverse("accounts:unfollow", kwargs={"username": "third"}), None
        )
        self.assertEqual(response.status_code, 404)
        self.assertTrue(FriendShip.objects.filter(followed=self.user2).exists())
        messages = list(get_messages(response.wsgi_request))
        message = str(messages[0])
        self.assertEqual(message, "存在しないユーザーです。")

    def test_failure_post_with_self(self):
        response = self.client.post(
            reverse("accounts:unfollow", kwargs={"username": "test"}), None
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(FriendShip.objects.filter(following=self.user).exists())
        messages = list(get_messages(response.wsgi_request))
        message = str(messages[0])
        self.assertEqual(message, "自分自身はフォロー解除できません。")

    def test_filure_post_with_already_unfollowed_user(self):
        FriendShip.objects.filter(following=self.user, followed=self.user2).delete()
        response = self.client.post(
            reverse("accounts:unfollow", kwargs={"username": "test2"}), None
        )
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        message = str(messages[0])
        self.assertEqual(message, "無効な操作です。")


class TestFollowingListView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test", email="test@test.com", password="goodpass"
        )
        self.user2 = User.objects.create_user(
            username="test2", email="test2@test.com", password="goodpass"
        )
        self.client.login(username="test", password="goodpass")
        FriendShip.objects.create(following=self.user, followed=self.user2)

    def test_success_get(self):
        response = self.client.get(
            reverse("accounts:following_list", kwargs={"username": "test"})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/following_list.html")


class TestFollowerListView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test", email="test@test.com", password="goodpass"
        )
        self.user2 = User.objects.create_user(
            username="test2", email="test2@test.com", password="goodpass"
        )
        self.client.login(username="test", password="goodpass")
        FriendShip.objects.create(following=self.user2, followed=self.user)

    def test_success_get(self):
        response = self.client.get(
            reverse("accounts:follower_list", kwargs={"username": "test"})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/follower_list.html")
