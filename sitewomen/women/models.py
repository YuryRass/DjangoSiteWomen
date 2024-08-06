from datetime import datetime

from django.db import models
from django.urls import reverse


class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)


class Women(models.Model):

    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

        @classmethod
        def variants(cls) -> tuple[tuple[bool, str]]:
            return tuple(map(lambda x: (bool(x[0]), x[1]), cls.choices))

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="SLUG")
    content = models.TextField(blank=True, verbose_name="Содержимое")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Дата и время обновления")
    is_published = models.BooleanField(
        choices=Status.variants(),
        default=Status.DRAFT,
        verbose_name="Статус"
    )
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts', verbose_name="Категория")
    tags = models.ManyToManyField('TagPost', blank=True, related_name='women', verbose_name="Теги")
    husband = models.OneToOneField('Husband', on_delete=models.SET_NULL, null=True, blank=True, related_name='woman', verbose_name="Муж",)

    objects = models.Manager()
    published = PublishedModel()

    def __str__(self) -> str:
        return (f"Women(id={self.pk}, title='{self.title}', content={self.content[:30]}, "
                f"time_create={datetime.strftime(self.time_create, '%d-%b-%Y-%H:%M:%S')}, "
                f"time_update={datetime.strftime(self.time_update, '%d-%b-%Y-%H:%M:%S')}, "
                f"is_published={self.is_published}, slug={self.slug}, cat_id={self.cat.id})"
                )

    def __repr__(self) -> str:
        return str(self)

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        ordering = ['-time_create']
        verbose_name = 'Известные женщины'
        verbose_name_plural = 'Известные женщины'
        indexes = [
            models.Index(fields=['-time_create']),
        ]


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})

    def __str__(self):
        return self.tag


class Husband(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)

    def __str__(self):
        return self.name