from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone


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
