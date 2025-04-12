from django.db import models
from django.urls import reverse

class Owner(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    m_count = models.IntegerField(blank=True,
                                  default=0)
    def __str__(self):
        return self.name

class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug':
                                          self.slug})
    def __str__(self):
        return self.tag

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug':
                                               self.slug})
    def __str__(self):
        return self.name

class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Cats.Status.PUBLISHED)

class Cats(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255,
                             verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, db_index=True,
                            unique=True)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT)
    objects = models.Manager()
    published = PublishedModel()
    cat = models.ForeignKey('Category',
                            on_delete=models.CASCADE,
                            related_name='posts')
    tags = models.ManyToManyField('TagPost', blank=True,
                                  related_name='tags')
    owner = models.OneToOneField('Owner',
                                 on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='kot')

    class Meta:
        ordering = ['-time_create']
        indexes = [
        models.Index(fields=['-time_create']),
    ]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    def __str__(self):
        return self.title
