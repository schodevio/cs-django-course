from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Profile
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def make_user(username="alice", password="testpass123", email="alice@example.com"):
    return User.objects.create_user(username=username, password=password, email=email)


# ---------------------------------------------------------------------------
# Profile model / signals
# ---------------------------------------------------------------------------

class ProfileModelTests(TestCase):
    def setUp(self):
        self.user = make_user()

    def test_profile_created_on_user_save(self):
        self.assertIsInstance(self.user.profile, Profile)

    def test_profile_str(self):
        self.assertEqual(str(self.user.profile), "alice Profile")

    def test_profile_deleted_with_user(self):
        user_id = self.user.pk
        self.user.delete()
        self.assertFalse(Profile.objects.filter(user_id=user_id).exists())


# ---------------------------------------------------------------------------
# UserRegisterForm
# ---------------------------------------------------------------------------

class UserRegisterFormTests(TestCase):
    def _valid_data(self, **overrides):
        data = {
            "username": "bob",
            "email": "bob@example.com",
            "password1": "Str0ng!Pass",
            "password2": "Str0ng!Pass",
        }
        data.update(overrides)
        return data

    def test_valid_form(self):
        form = UserRegisterForm(data=self._valid_data())
        self.assertTrue(form.is_valid())

    def test_mismatched_passwords_invalid(self):
        form = UserRegisterForm(data=self._valid_data(password2="different"))
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_missing_email_invalid(self):
        form = UserRegisterForm(data=self._valid_data(email=""))
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_duplicate_username_invalid(self):
        make_user(username="bob")
        form = UserRegisterForm(data=self._valid_data())
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)


# ---------------------------------------------------------------------------
# Registration views  (new + create)
# ---------------------------------------------------------------------------

class RegistrationViewTests(TestCase):
    def test_new_returns_200(self):
        response = self.client.get(reverse("users_new"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/new.html")

    def test_new_rejects_post(self):
        response = self.client.post(reverse("users_new"))
        self.assertEqual(response.status_code, 405)

    def test_create_rejects_get(self):
        response = self.client.get(reverse("users_create"))
        self.assertEqual(response.status_code, 405)

    def test_valid_registration_creates_user_and_redirects(self):
        response = self.client.post(reverse("users_create"), {
            "username": "newuser",
            "email": "new@example.com",
            "password1": "Str0ng!Pass",
            "password2": "Str0ng!Pass",
        })
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_invalid_registration_re_renders_form(self):
        response = self.client.post(reverse("users_create"), {
            "username": "",
            "email": "bad",
            "password1": "x",
            "password2": "y",
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/new.html")


# ---------------------------------------------------------------------------
# Profile views  (profile + update_profile)
# ---------------------------------------------------------------------------

class ProfileViewTests(TestCase):
    def setUp(self):
        self.user = make_user()
        self.profile_url = reverse("users_profile")
        self.update_url = reverse("users_profile_update")

    def test_profile_redirects_when_unauthenticated(self):
        response = self.client.get(self.profile_url)
        self.assertRedirects(
            response, f"{reverse('login')}?next={self.profile_url}")

    def test_profile_returns_200_when_logged_in(self):
        self.client.login(username="alice", password="testpass123")
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/profile.html")

    def test_profile_rejects_post(self):
        self.client.login(username="alice", password="testpass123")
        response = self.client.post(self.profile_url)
        self.assertEqual(response.status_code, 405)

    def test_update_profile_rejects_get(self):
        self.client.login(username="alice", password="testpass123")
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 405)

    def test_update_profile_redirects_when_unauthenticated(self):
        response = self.client.post(self.update_url, {})
        self.assertRedirects(
            response, f"{reverse('login')}?next={self.update_url}")

    def test_valid_update_changes_username(self):
        self.client.login(username="alice", password="testpass123")
        self.client.post(self.update_url, {
            "username": "alice_updated",
            "email": "alice@example.com",
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "alice_updated")

    def test_invalid_update_re_renders_form(self):
        self.client.login(username="alice", password="testpass123")
        response = self.client.post(self.update_url, {
            "username": "",
            "email": "not-an-email",
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/profile.html")
