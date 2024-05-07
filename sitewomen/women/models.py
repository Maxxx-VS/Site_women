from django.db import models
from django.urls import reverse
class Women(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True) # unique делает поле уникальным, db_index делает поле индексируемым
    content = models.TextField(blank=True) # blank позволяет не передавать в content записи
    time_create = models.DateTimeField(auto_now_add=True) # auto_now_add автоматически заполняет поле в момент появления записи
    time_update = models.DateTimeField(auto_now=True) # auto_now каждый раз меняется в момент записи
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta: # класс для сортировки
        ordering = ['-time_create'] # метод сортировки
        indexes = [ # метод индексации
            models.Index(fields=['-time_create'])
        ]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug':self.slug})