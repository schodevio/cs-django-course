from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Post


def make_user(username="alice", password="testpass123"):
    return User.objects.create_user(username=username, password=password)


def make_post(author, title="Test Post", content="Some content"):
    return Post.objects.create(author=author, title=title, content=content)


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------

class PostModelTests(TestCase):
    def setUp(self):
        self.user = make_user()
        self.post = make_post(self.user)

    def test_str_returns_title(self):
        self.assertEqual(str(self.post), self.post.title)

    def test_get_absolute_url(self):
        url = self.post.get_absolute_url()
        self.assertEqual(url, reverse(
            "blog_post", kwargs={"pk": self.post.pk}))


# ---------------------------------------------------------------------------
# PostListView  (home)
# ---------------------------------------------------------------------------

class PostListViewTests(TestCase):
    def setUp(self):
        self.user = make_user()
        for i in range(7):
            make_post(self.user, title=f"Post {i}")

    def test_home_status_200(self):
        response = self.client.get(reverse("blog_home"))
        self.assertEqual(response.status_code, 200)

    def test_home_uses_correct_template(self):
        response = self.client.get(reverse("blog_home"))
        self.assertTemplateUsed(response, "blog/home.html")

    def test_home_paginates_by_5(self):
        response = self.client.get(reverse("blog_home"))
        self.assertEqual(len(response.context["posts"]), 5)

    def test_home_second_page(self):
        response = self.client.get(reverse("blog_home") + "?page=2")
        self.assertEqual(len(response.context["posts"]), 2)


# ---------------------------------------------------------------------------
# UserPostListView
# ---------------------------------------------------------------------------

class UserPostListViewTests(TestCase):
    def setUp(self):
        self.user = make_user()
        self.other = make_user(username="bob")
        for i in range(3):
            make_post(self.user, title=f"Alice post {i}")
        make_post(self.other, title="Bob post")

    def test_shows_only_user_posts(self):
        url = reverse("blog_user_posts", kwargs={
                      "username": self.user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        for post in response.context["posts"]:
            self.assertEqual(post.author, self.user)

    def test_unknown_user_returns_404(self):
        url = reverse("blog_user_posts", kwargs={"username": "nobody"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


# ---------------------------------------------------------------------------
# PostDetailView
# ---------------------------------------------------------------------------

class PostDetailViewTests(TestCase):
    def setUp(self):
        self.user = make_user()
        self.post = make_post(self.user)

    def test_detail_status_200(self):
        url = reverse("blog_post", kwargs={"pk": self.post.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_404_for_missing_post(self):
        url = reverse("blog_post", kwargs={"pk": 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


# ---------------------------------------------------------------------------
# PostCreateView
# ---------------------------------------------------------------------------

class PostCreateViewTests(TestCase):
    def setUp(self):
        self.user = make_user()
        self.url = reverse("blog_new_post")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")

    def test_logged_in_can_get_form(self):
        self.client.login(username="alice", password="testpass123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_post_sets_author(self):
        self.client.login(username="alice", password="testpass123")
        self.client.post(self.url, {"title": "New", "content": "Body"})
        post = Post.objects.get(title="New")
        self.assertEqual(post.author, self.user)


# ---------------------------------------------------------------------------
# PostUpdateView
# ---------------------------------------------------------------------------

class PostUpdateViewTests(TestCase):
    def setUp(self):
        self.author = make_user()
        self.other = make_user(username="bob")
        self.post = make_post(self.author)
        self.url = reverse("blog_edit_post", kwargs={"pk": self.post.pk})

    def test_owner_can_update(self):
        self.client.login(username="alice", password="testpass123")
        response = self.client.post(
            self.url, {"title": "Updated", "content": "New body"})
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Updated")

    def test_non_owner_gets_403(self):
        self.client.login(username="bob", password="testpass123")
        response = self.client.post(
            self.url, {"title": "Hacked", "content": "x"})
        self.assertEqual(response.status_code, 403)


# ---------------------------------------------------------------------------
# PostDeleteView
# ---------------------------------------------------------------------------

class PostDeleteViewTests(TestCase):
    def setUp(self):
        self.author = make_user()
        self.other = make_user(username="bob")
        self.post = make_post(self.author)
        self.url = reverse("blog_delete_post", kwargs={"pk": self.post.pk})

    def test_owner_can_delete(self):
        self.client.login(username="alice", password="testpass123")
        self.client.post(self.url)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_non_owner_gets_403(self):
        self.client.login(username="bob", password="testpass123")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())


# ---------------------------------------------------------------------------
# About view
# ---------------------------------------------------------------------------

class AboutViewTests(TestCase):
    def test_about_status_200(self):
        response = self.client.get(reverse("blog_about"))
        self.assertEqual(response.status_code, 200)

    def test_about_uses_correct_template(self):
        response = self.client.get(reverse("blog_about"))
        self.assertTemplateUsed(response, "blog/about.html")
