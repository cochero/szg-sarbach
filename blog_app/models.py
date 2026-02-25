from django.db import models
from django.utils.text import slugify


class BlogPost(models.Model):
    TYPE_CHOICES = [
        ('Blog', 'Blog'),
        ('Event', 'Event'),
        ('WorkShop', 'Workshop'),
    ]
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500, unique=True, blank=True)
    date = models.DateField()
    description = models.TextField(blank=True)
    author = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='blog/', blank=True, null=True)
    post_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='Blog')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
