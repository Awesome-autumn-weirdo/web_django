from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
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

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True,
                            verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug':
                                               self.slug})
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Cats.Status.PUBLISHED)


class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')


class Cats(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255,
                             verbose_name="Заголовок")
    slug = models.SlugField(
        max_length=255, db_index=True,
        unique=True,
        validators = [
            MinLengthValidator(5),
            MaxLengthValidator(100),
        ]
    )
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    time_create = models.DateTimeField(auto_now_add=True,
                                       verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True,
                                       verbose_name="Время изменения")
    is_published = models.BooleanField(choices=tuple(map(lambda x:
                        (bool(x[0]), x[1]), Status.choices)),
                        default=Status.DRAFT, verbose_name="Статус")
    objects = models.Manager()
    published = PublishedModel()
    cat = models.ForeignKey('Category',
                            on_delete=models.CASCADE,
                            related_name='posts',
                            verbose_name="Категории")
    tags = models.ManyToManyField('TagPost', blank=True,
                                  related_name='tags',
                                  verbose_name="Тэги")
    owner = models.OneToOneField('Owner',
                                 on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='kot', verbose_name="Владелец")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/",
                              default=None, blank=True, null=True,
                              verbose_name="Фото")
    author = models.ForeignKey(get_user_model(),
                               on_delete=models.SET_NULL, related_name='posts',
                               null=True, default=None)

    class Meta:
        verbose_name = 'Котёночек'
        verbose_name_plural = 'Котяточки'
        ordering = ['-time_create']
        indexes = [
        models.Index(fields=['-time_create']),
    ]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        #self.slug = slugify(self.title,
                           # allow_unicode=True)
        super().save(*args, **kwargs)
