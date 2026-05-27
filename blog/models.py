import json
from django.db import models
from django.utils import timezone
from django.urls import reverse


class Post(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('research', 'Research'),
        ('projects', 'Projects'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    summary = models.TextField(max_length=300)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})


class SiteConfig(models.Model):
    """Singleton — always use SiteConfig.get()"""
    owner_name  = models.CharField(max_length=100, default='Your Name')
    tagline     = models.CharField(max_length=200, default='researcher · builder · occasional overthinker')
    about       = models.TextField(default='I work at the intersection of things I find interesting. This is where I put them into words.')
    avatar_emoji = models.CharField(max_length=10, default='🌿')
    avatar_image = models.ImageField(upload_to='avatars/', null=True, blank=True)
    # JSON list: [{"label":"Twitter","url":"https://...","visible":true}, ...]
    socials_json = models.TextField(default='[]')

    class Meta:
        verbose_name = 'Site Config'

    def get_socials(self):
        try:
            return json.loads(self.socials_json)
        except (json.JSONDecodeError, TypeError):
            return []

    def set_socials(self, data):
        self.socials_json = json.dumps(data)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
