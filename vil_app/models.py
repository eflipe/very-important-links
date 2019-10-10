from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField('Nombre', max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Page(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField("Título", blank=True, null=True, max_length=555)
    url = models.URLField("URL")
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    fecha_agregado = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    # published_date = models.DateTimeField(blank=True, null=True)
    #
    # def publish(self):
    #     self.published_date = timezone.now()
    #     self.save()

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    # Links UserProfile to a User model instance
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
