from django.contrib.auth import get_user_model, SESSION_KEY
from django.test import TestCase
from django.urls import reverse

from mysite import settings


User = get_user_model()


class TestSignUpView(TestCase):
    def test_success_get(self):
        response = self.client.get(reverse('accounts:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')

    def test_success_post(self):
        post = {
            'email': 'test@example.com',
            'username': 'test',
            'password1': 'goodpass',
            'password2': 'goodpass',
        }
        response = self.client.post(reverse('accounts:signup'), post)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='test', email='test@example.com').exists())
        self.assertRedirects(response, reverse('accounts:home'), status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        self.assertIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_empty_form(self):
        post = {
            'email': '',
            'username': '',
            'password1': '',
            'password2': '',
        }
        response = self.client.post(reverse('accounts:signup'), post)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=' ', email=' ').exists())
        self.assertFormError(response, 'form', 'email', 'このフィールドは必須です。')
        self.assertFormError(response, 'form', 'username', 'このフィールドは必須です。')
        self.assertFormError(response, 'form', 'password1', 'このフィールドは必須です。')
        self.assertFormError(response, 'form', 'password2', 'このフィールドは必須です。')

    def test_failure_post_with_empty_username(self):
        post = {
            'email': 'test@example.com',
            'username': '',
            'password1': 'goodpass',
            'password2': 'goodpass',
        }
        response = self.client.post(reverse('accounts:signup'), post)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=' ', email='test@example.com').exists())
        self.assertFormError(response, 'form', 'username', 'このフィールドは必須です。')

    def test_failure_post_with_empty_email(self):
        post = {
            'email': '',
            'username': 'test',
            'password1': 'goodpass',
            'password2': 'goodpass',
        }
        response = self.client.post(reverse('accounts:signup'), post)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='test', email=' ').exists())
        self.assertFormError(response, 'form', 'email', 'このフィールドは必須です。')

    def test_failure_post_with_empty_password(self):
        post = {
            'email': 'test@example.com',
            'username': 'test',
            'password1': '',
            'password2': '',
        }
        response = self.client.post(reverse('accounts:signup'), post)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='test', email='test@example.com').exists())
        self.assertFormError(response, 'form', 'password1', 'このフィールドは必須です。')
        self.assertFormError(response, 'form', 'password2', 'このフィールドは必須です。')

    def test_failure_post_with_duplicated_user(self):
        post1 = {
            'email': 'test1@example.com',
            'username': 'test',
            'password1': 'goodpass',
            'password2': 'goodpass',
        }
        post2 = {
            'email': 'test2@example.com',
            'username': 'test',
            'password1': 'goodpass',
            'password2': 'goodpass',
        }
        self.client.post(reverse('accounts:signup'), post1)
        response = self.client.post(reverse('accounts:signup'), post2)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='test', email='test2@example.com').exists())
        self.assertFormError(response, 'form', 'username', '同じユーザー名が既に登録済みです。')

    def test_failure_post_with_invalid_email(self):
        post = {
            'email': 'test.boo',
            'username': 'test',
            'password1': 'goodpass',
            'password2': 'goodpass',
        }
        response = self.client.post(reverse('accounts:signup'), post)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='test', email='test.boo').exists())
        self.assertFormError(response, 'form', 'email', '有効なメールアドレスを入力してください。')

    def test_failure_post_with_too_short_password(self):
        post = {
            'email': 'test@example.com',
            'username': 'test',
            'password1': 'pass',
            'password2': 'pass',
        }
        response = self.client.post(reverse('accounts:signup'), post)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='test', email='test@example.com').exists())
        self.assertFormError(response, 'form', 'password2', 'このパスワードは短すぎます。最低 8 文字以上必要です。')

    def test_failure_post_with_password_similar_to_username(self):
        post = {
            'email': 'test@example.com',
            'username': 'goodpass',
            'password1': 'goodpass',
            'password2': 'goodpass',
        }
        response = self.client.post(reverse('accounts:signup'), post)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='test', email='test@example.com').exists())
        self.assertFormError(response, 'form', 'password2', 'このパスワードは ユーザー名 と似すぎています。')

    def test_failure_post_with_only_numbers_password(self):
        post = {
            'email': 'test@example.com',
            'username': 'test',
            'password1': '12345678',
            'password2': '12345678',
        }
        response = self.client.post(reverse('accounts:signup'), post)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='test', email='test@example.com').exists())
        self.assertFormError(response, 'form', 'password2', 'このパスワードは一般的すぎます。', 'このパスワードは数字しか使われていません。')

    def test_failure_post_with_mismatch_password(self):
        post = {
            'email': 'test@example.com',
            'username': 'test',
            'password1': 'goodpass',
            'password2': 'goodpath',
        }
        response = self.client.post(reverse('accounts:signup'), post)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='test', email='test@example.com').exists())
        self.assertFormError(response, 'form', 'password2', '確認用パスワードが一致しません。')


class TestHomeView(TestCase):
    def setUp(self):
        post = {
            'email': 'test@example.com',
            'username': 'test',
            'password1': 'goodpass',
            'password2': 'goodpass',
        }
        self.client.post(reverse('accounts:signup'), post)

    def test_success_get(self):
        response = self.client.get(reverse('accounts:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/home.html')


class TestLoginView(TestCase):
    def setUp(self):
        post = {
            'email': 'test@example.com',
            'username': 'test',
            'password1': 'goodpass',
            'password2': 'goodpass',
        }
        User.objects.create_user(post['username'], post['email'], post['password1'])

    def test_success_get(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_success_post(self):
        loginPost = {
            'username': 'test',
            'password': 'goodpass',
        }
        response = self.client.post(reverse('accounts:login'), loginPost)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(settings.LOGIN_REDIRECT_URL), status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        self.assertIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_not_exists_user(self):
        loginPost = {
            'username': 'te',
            'password': 'goodpass',
        }
        response = self.client.post(reverse('accounts:login'), loginPost)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', '', '正しいユーザー名とパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。')
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_empty_password(self):
        loginPost = {
            'username': 'test',
            'password': '',
        }
        response = self.client.post(reverse('accounts:login'), loginPost)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'password', 'このフィールドは必須です。')
        self.assertNotIn(SESSION_KEY, self.client.session)


class TestLogoutView(TestCase):
    def setUp(self):
        post = {
            'email': 'test@example.com',
            'username': 'test',
            'password1': 'goodpass',
            'password2': 'goodpass',
        }
        self.client.post(reverse('accounts:signup'), post)

    def test_success_get(self):
        response = self.client.get(reverse('accounts:logout'))
        self.assertRedirects(response, reverse(settings.LOGOUT_REDIRECT_URL), status_code=302, target_status_code=200)
        self.assertNotIn(SESSION_KEY, self.client.session)


class TestUserProfileView(TestCase):
    def setUp(self):
        post = {
            'email': 'test@example.com',
            'username': 'test',
            'password1': 'goodpass',
            'password2': 'goodpass',
        }
        self.client.post(reverse('accounts:signup'), post)

    def test_success_get(self):
        user = User.objects.get()
        response = self.client.get(reverse('accounts:user_profile', kwargs={'pk': user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')

    def test_failure_get_with_not_exists_user(self):
        response = self.client.get(reverse('accounts:user_profile', kwargs={'pk': 100}))
        self.assertEqual(response.status_code, 404)


class TestUserProfileEditView(TestCase):
    def setUp(self):
        post = {
            'email': 'test@example.com',
            'username': 'test',
            'password1': 'goodpass',
            'password2': 'goodpass',
        }
        self.editPost = {
            'username': 'test2',
            'email': 'test2@example.com',
            'gender': '3',
            'selfIntro': 'よろしく',
        }
        self.client.post(reverse('accounts:signup'), post)

    def test_success_get(self):
        user = User.objects.get(username='test')
        response = self.client.get(reverse('accounts:user_profile_edit', kwargs={'pk': user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile_edit.html')

    def test_success_post(self):
        user = User.objects.get(username='test')
        response = self.client.post(reverse('accounts:user_profile_edit', kwargs={'pk': user.pk}), self.editPost)
        self.assertRedirects(response, reverse('accounts:user_profile', kwargs={'pk': user.pk}), status_code=302, target_status_code=200)
        self.assertTrue(User.objects.filter(username='test2', email='test2@example.com').exists())

    def test_failure_post_with_not_exists_user(self):
        response = self.client.post(reverse('accounts:user_profile_edit', kwargs={'pk': 100}), self.editPost)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(User.objects.filter(username='test2', email='test2@example.com').exists())

    def test_failure_post_with_incorrect_user(self):
        post2 = {
            'email': 'second@example.com',
            'username': 'second',
            'password1': 'goodpass2',
            'password2': 'goodpass2',
        }
        User.objects.create_user(post2['username'], post2['email'], post2['password1'])
        user2 = User.objects.get(username='second')
        response = self.client.post(reverse('accounts:user_profile_edit', kwargs={'pk': user2.pk}), self.editPost)
        self.assertEqual(response.status_code, 403)
        self.assertFalse(User.objects.filter(username='test2', email='test2@example.com').exists())


class TestFollowView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_user(self):
        pass

    def test_failure_post_with_self(self):
        pass


class TestUnfollowView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_incorrect_user(self):
        pass


class TestFollowingListView(TestCase):
    def test_success_get(self):
        pass


class TestFollowerListView(TestCase):
    def test_success_get(self):
        pass
