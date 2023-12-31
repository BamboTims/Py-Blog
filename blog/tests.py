from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Post


# Create your tests here.
class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = get_user_model().objects.create_user(
            username="testuser", email="test@gmail.com", password="secret"
        )
        cls.post = Post.objects.create(
            title="A good book", body="Nice body!!!", author=cls.user
        )

    def test_post_model(self):
        self.assertEqual(self.post.title, "A good book")
        self.assertEqual(self.post.author.username, "testuser")
        self.assertEqual(self.post.body, "Nice body!!!")
        self.assertEqual(str(self.post), "A good book")
        self.assertEqual(self.post.get_absolute_url(), "/post/1/")

    def test_url_exists_at_correct_location_listview(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_detailview(self):
        response = self.client.get("/post/1/")
        self.assertEqual(response.status_code, 200)

    def test_post_listview(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nice body!!!")
        self.assertTemplateUsed(response, "home.html")

    def test_post_detailview(self):
        response = self.client.get(reverse("post-detail", kwargs={"pk": self.post.pk}))
        no_response = self.client.get("/post/10000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Nice body!!!")
        self.assertTemplateUsed(response, "post-detail.html")

    def test_post_createview(self):
        response = self.client.post(
            reverse("post-new"),
            {"title": "New title", "body": "New text", "author": self.user.id},
        )
        self.assertEqual(response.status_code, 302)

    def test_post_updateview(self):
        response = self.client.post(
            reverse("post-edit", args="1"),
            {"title": "Updated title", "body": "Updated text"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, "Updated title")
        self.assertEqual(Post.objects.last().body, "Updated text")

    def test_post_deleteview(self):
        response = self.client.post(reverse("post-delete", args="1"))
        self.assertEqual(response.status_code, 302)
