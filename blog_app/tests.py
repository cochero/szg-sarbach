import pytest
from django.test import Client
from datetime import date
from blog_app.models import BlogPost


@pytest.mark.django_db
class TestBlogPostModel:
    def test_str(self):
        b = BlogPost.objects.create(title="My Post", date=date.today())
        assert str(b) == "My Post"

    def test_slug_auto_generated(self):
        b = BlogPost.objects.create(title="Health Tips 2026", date=date.today())
        assert b.slug == "health-tips-2026"

    def test_post_types(self):
        BlogPost.objects.create(title="B1", date=date.today(), post_type="Blog")
        BlogPost.objects.create(title="E1", date=date.today(), post_type="Event")
        BlogPost.objects.create(title="W1", date=date.today(), post_type="WorkShop")
        assert BlogPost.objects.filter(post_type="Blog").count() == 1
        assert BlogPost.objects.filter(post_type="Event").count() == 1
        assert BlogPost.objects.filter(post_type="WorkShop").count() == 1

    def test_ordering(self):
        BlogPost.objects.create(title="Old", date=date(2025, 1, 1))
        BlogPost.objects.create(title="New", date=date(2026, 1, 1))
        posts = list(BlogPost.objects.all())
        assert posts[0].title == "New"

    def test_active_filter(self):
        BlogPost.objects.create(title="Active", date=date.today(), is_active=True)
        BlogPost.objects.create(title="Inactive", date=date.today(), is_active=False)
        assert BlogPost.objects.filter(is_active=True).count() == 1


@pytest.mark.django_db
class TestBlogPages:
    def setup_method(self):
        self.client = Client()
        self.blog = BlogPost.objects.create(
            title="Test Blog Post", date=date.today(),
            post_type="Blog", is_active=True, description="Test content"
        )
        self.event = BlogPost.objects.create(
            title="Test Event", date=date.today(),
            post_type="Event", is_active=True
        )

    def test_blog_list_page(self):
        response = self.client.get("/blogs/")
        assert response.status_code == 200

    def test_events_list_page(self):
        response = self.client.get("/events/")
        assert response.status_code == 200

    def test_workshops_list_page(self):
        response = self.client.get("/workshops/")
        assert response.status_code == 200

    def test_blog_detail_page(self):
        response = self.client.get(f"/blogs/{self.blog.slug}/")
        assert response.status_code == 200

    def test_event_detail_page(self):
        response = self.client.get(f"/event/{self.event.slug}/")
        assert response.status_code == 200

    def test_blog_detail_404(self):
        response = self.client.get("/blogs/nonexistent-post/")
        assert response.status_code == 404
