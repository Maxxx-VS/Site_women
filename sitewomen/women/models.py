from django.db import models
from django.urls import reverse

class PublishedManager(models.Manager): # класс для отображения только опубликованных женщин
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)

class Women(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликованно'

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True) # unique делает поле уникальным, db_index делает поле индексируемым
    content = models.TextField(blank=True) # blank позволяет не передавать в content записи
    time_create = models.DateTimeField(auto_now_add=True) # auto_now_add автоматически заполняет поле в момент появления записи
    time_update = models.DateTimeField(auto_now=True) # auto_now каждый раз меняется в момент записи
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT)
    cat = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='posts') # формируем свзь многие-к-одному
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags') # формируем свзь многие-к-многим
    husband = models.OneToOneField('Husband', on_delete=models.SET_NULL, null=True, blank=True, related_name='woman')

    objects = models.Manager() # менеджер по умолчанию
    published = PublishedManager() # менеджер собственный

    def __str__(self):
        return self.title

    class Meta: # класс для сортировки
        ordering = ['-time_create'] # метод сортировки
        indexes = [ # метод индексации
            models.Index(fields=['-time_create'])
        ]

    def get_absolute_url(self): # формирует url адрес для каждой записи
        return reverse('post', kwargs={'post_slug':self.slug})

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self): # формирует url адрес для каждой записи
        return reverse('tag', kwargs={'tag_slug':self.slug})


class Husband(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    m_count = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.name